from __future__ import annotations
import argparse
import concurrent.futures as cf
import csv
import hashlib
import json
import multiprocessing as mp
import time
from datetime import datetime, timezone
from pathlib import Path
import run_v13 as runner

OUT = runner.OUT
ROOT = runner.ROOT
DRIVER_REL = Path(__file__).resolve().relative_to(ROOT).as_posix()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def make_task(stage, candidate, arm, seed):
    suffix = f"_s{seed}" if stage == "stage3" else ""
    return {
        "job_id": f"V13-{stage.upper()}-{candidate}{suffix}",
        "candidate_id": f"V13_{stage.upper()}_{candidate}{suffix}",
        "arm": arm,
        "innovation": "ECR",
        "family": "ECR-evidence-calibrated-score-residual",
        "definition": {
            "BASELINE": "Raw-HG DCDLP + QTHS25 + BCE, matched strong baseline",
            "ECR_FULL": "ECR full: 24 Raw-HG pair features + standardized degree/CN + target-masked cross density + one raw×structure interaction",
            "ECR_SHUFFLED": "Parameter- and compute-matched ECR with evidence rows deterministically shuffled across target pairs",
        }[arm],
        "purpose": "candidate" if arm == "ECR_FULL" else ("matched mechanism control" if arm == "ECR_SHUFFLED" else "matched strong baseline"),
        "stage": stage,
        "dataset": "cora",
        "seed": int(seed),
        "epochs": 10,
        "sampler": "QTHS25",
        "priority": "P1",
        "estimated_cost": "2 Stage-1-equivalents",
        "status": "QUEUED",
        "gpu_mem_estimate": "under 1 GiB per process",
        "stage1": stage == "stage2",
        "strong_baseline_identity": "Cora Raw-HG DCDLP + QTHS25 + BCE",
    }


def all_tasks(stage):
    seeds = [0] if stage == "stage2" else [0, 1, 2]
    tasks = []
    for seed in seeds:
        suffix = f"_s{seed}" if stage == "stage3" else ""
        for candidate, arm in (("BASELINE", "BASELINE"), ("ECR_FULL", "ECR_FULL"), ("ECR_SHUFFLED", "ECR_SHUFFLED")):
            tasks.append(make_task(stage, candidate, arm, seed))
    return tasks


def run_worker(task, driver_hash):
    result = runner.run_one(task)
    result.setdefault("source_hashes", {})[DRIVER_REL] = driver_hash
    result["confirmation_driver_sha256"] = driver_hash
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    runner.atomic_json(folder / "result.json", result)
    return result


def reusable(task, driver_hash):
    path = OUT / "experiments" / task["candidate_id"] / task["arm"] / "result.json"
    if not path.exists():
        return None
    try:
        row = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if row.get("job_id") != task["job_id"] or row.get("state") != "COMPLETE":
        return None
    if int(row.get("epochs", -1)) != task["epochs"] or int(row.get("train_record", {}).get("epoch_count", -1)) != task["epochs"]:
        return None
    if row.get("source_hashes", {}).get(DRIVER_REL) != driver_hash:
        return None
    if row.get("test_evaluated") is not False:
        return None
    return row


def summarize(stage, results):
    by_seed = {}
    for row in results:
        if row.get("state") == "COMPLETE":
            by_seed.setdefault(int(row["seed"]), {})[row["arm"]] = row
    paired = []
    for seed, arms in sorted(by_seed.items()):
        if not all(k in arms for k in ("BASELINE", "ECR_FULL", "ECR_SHUFFLED")):
            continue
        base = float(arms["BASELINE"]["validation_metrics"]["mrr"])
        cand = float(arms["ECR_FULL"]["validation_metrics"]["mrr"])
        ctrl = float(arms["ECR_SHUFFLED"]["validation_metrics"]["mrr"])
        paired.append({"seed": seed, "baseline_mrr": base, "candidate_mrr": cand,
                       "matched_control_mrr": ctrl, "delta": cand - base,
                       "control_delta": cand - ctrl})
    complete = len(paired) == (1 if stage == "stage2" else 3)
    if stage == "stage2" and paired:
        row = paired[0]
        effect = row["delta"] >= 0.003 or (row["baseline_mrr"] > 0 and row["delta"] / row["baseline_mrr"] >= 0.01)
        control_win = row["candidate_mrr"] > row["matched_control_mrr"]
        go = complete and effect and row["candidate_mrr"] > row["baseline_mrr"] and control_win
        return {"state": "STAGE2_GO" if go else ("STAGE2_REJECT" if complete else "INFRASTRUCTURE_FAILURE"),
                "go": bool(go), "effect_gate": bool(effect), "mechanism_control_pass": bool(control_win),
                "paired": paired, "test_evaluated": False}
    if stage == "stage3" and paired:
        wins = sum(p["delta"] > 0 for p in paired)
        control_wins = sum(p["control_delta"] > 0 for p in paired)
        mean_gain = sum(p["delta"] for p in paired) / len(paired)
        mean_control_gain = sum(p["control_delta"] for p in paired) / len(paired)
        go = complete and wins >= 2 and mean_gain > 0 and control_wins >= 2 and mean_control_gain > 0
        return {"state": "LOCAL_GO" if go else ("STAGE3_REJECT" if complete else "INFRASTRUCTURE_FAILURE"),
                "go": bool(go), "wins_vs_baseline": wins, "mean_gain": mean_gain,
                "control_wins": control_wins, "mean_gain_vs_control": mean_control_gain,
                "paired": paired, "test_evaluated": False}
    return {"state": "INFRASTRUCTURE_FAILURE", "go": False, "paired": paired, "test_evaluated": False}


def run_stage(stage, workers):
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = all_tasks(stage)
    driver_hash = file_hash(__file__)
    results = []
    pending = []
    for task in tasks:
        prior = reusable(task, driver_hash)
        if prior is None:
            pending.append(task)
        else:
            results.append(prior)
    status_path = OUT / f"{stage}_confirm_status.json"
    result_path = OUT / f"{stage}_confirm_results.json"
    runner.atomic_json(status_path, {"state": "RUNNING", "stage": stage,
                                    "completed": len(results), "total": len(tasks),
                                    "workers": min(workers, len(pending)), "test_evaluated": False,
                                    "started_at_utc": utc_now(), "driver_sha256": driver_hash})
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(workers, len(pending)),
                                    mp_context=mp.get_context("spawn"),
                                    initializer=runner.worker_init) as pool:
            futures = {pool.submit(run_worker, task, driver_hash): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    row = future.result()
                except Exception as exc:
                    row = {**task, "state": "FAILED", "error": repr(exc),
                           "test_evaluated": False, "completed_at_utc": utc_now()}
                results.append(row)
                runner.atomic_json(result_path, {"stage": stage, "results": results,
                                                "decision": summarize(stage, results),
                                                "test_evaluated": False,
                                                "driver_sha256": driver_hash})
                runner.atomic_json(status_path, {"state": "RUNNING", "stage": stage,
                                                "completed": sum(r.get("state") == "COMPLETE" for r in results),
                                                "total": len(tasks), "failed": [r.get("job_id") for r in results if r.get("state") != "COMPLETE"],
                                                "workers": min(workers, len(pending)), "test_evaluated": False,
                                                "updated_at_utc": utc_now(), "driver_sha256": driver_hash})
    decision = summarize(stage, results)
    payload = {"stage": stage, "results": sorted(results, key=lambda r: (int(r["seed"]), r["arm"])),
               "decision": decision, "test_evaluated": False, "driver_sha256": driver_hash,
               "completed_at_utc": utc_now()}
    runner.atomic_json(result_path, payload)
    runner.atomic_json(status_path, {"state": decision["state"], "stage": stage,
                                    "completed": sum(r.get("state") == "COMPLETE" for r in results),
                                    "total": len(tasks), "decision": decision,
                                    "test_evaluated": False, "updated_at_utc": utc_now(),
                                    "driver_sha256": driver_hash})
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("stage2", "stage3"), required=True)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise SystemExit("workers must be between 1 and 8")
    payload = run_stage(args.stage, args.workers)
    print(json.dumps({"stage": payload["stage"], "decision": payload["decision"],
                      "results": [{"job_id": r.get("job_id"), "state": r.get("state"),
                                   "mrr": r.get("validation_metrics", {}).get("mrr"),
                                   "epochs": r.get("train_record", {}).get("epoch_count"),
                                   "test_evaluated": r.get("test_evaluated")} for r in payload["results"]]},
                     indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
