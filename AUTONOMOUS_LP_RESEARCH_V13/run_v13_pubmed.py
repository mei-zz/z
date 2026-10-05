from __future__ import annotations
import argparse
import concurrent.futures as cf
import hashlib
import json
import multiprocessing as mp
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


def make_tasks():
    tasks = []
    for seed in range(3):
        for candidate, arm in (("BASELINE", "BASELINE"), ("ECR_FULL", "ECR_FULL"), ("ECR_SHUFFLED", "ECR_SHUFFLED")):
            tasks.append({
                "job_id": f"V13-PUBMED-{candidate}_s{seed}",
                "candidate_id": f"V13_PUBMED_{candidate}_s{seed}",
                "arm": arm,
                "innovation": "ECR",
                "family": "ECR-evidence-calibrated-score-residual",
                "definition": {
                    "BASELINE": "PubMed Raw-HG DCDLP + QTHS25 + BCE; matched strong baseline",
                    "ECR_FULL": "PubMed ECR full: 24 Raw-HG pair features + standardized degree/CN + target-masked cross density + one Raw-HG×structure interaction",
                    "ECR_SHUFFLED": "PubMed parameter-matched ECR with evidence rows deterministically shuffled across target pairs",
                }[arm],
                "purpose": "candidate" if arm == "ECR_FULL" else ("matched mechanism control" if arm == "ECR_SHUFFLED" else "matched strong baseline"),
                "stage": "pubmed_generalization",
                "dataset": "pubmed",
                "seed": seed,
                "epochs": 10,
                "sampler": "QTHS25",
                "priority": "P1",
                "estimated_cost": "2 Stage-1-equivalents",
                "status": "QUEUED",
                "gpu_mem_estimate": "measured on PubMed worker batch",
                "stage1": False,
                "strong_baseline_identity": "Cora Raw-HG DCDLP + QTHS25 + BCE",
            })
    return tasks


def execute(task, driver_hash):
    row = runner.run_one(task)
    row.setdefault("source_hashes", {})[DRIVER_REL] = driver_hash
    row["generalization_driver_sha256"] = driver_hash
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    runner.atomic_json(folder / "result.json", row)
    return row


def summary(rows):
    by_seed = {}
    for row in rows:
        if row.get("state") == "COMPLETE":
            by_seed.setdefault(int(row["seed"]), {})[row["arm"]] = row
    paired = []
    for seed, arms in sorted(by_seed.items()):
        if not all(arm in arms for arm in ("BASELINE", "ECR_FULL", "ECR_SHUFFLED")):
            continue
        base = float(arms["BASELINE"]["validation_metrics"]["mrr"])
        candidate = float(arms["ECR_FULL"]["validation_metrics"]["mrr"])
        control = float(arms["ECR_SHUFFLED"]["validation_metrics"]["mrr"])
        context_keys = ("split_hash", "train_pool_hash", "validation_candidate_hash", "selected_negative_hash")
        mismatches = [key for key in context_keys if len({arms[arm].get(key) for arm in ("BASELINE", "ECR_FULL", "ECR_SHUFFLED")}) != 1]
        source_maps = [json.dumps(arms[arm].get("source_hashes", {}), sort_keys=True) for arm in ("BASELINE", "ECR_FULL", "ECR_SHUFFLED")]
        if len(set(source_maps)) != 1:
            mismatches.append("source_hashes")
        if mismatches:
            raise RuntimeError(f"PubMed seed {seed} arm context mismatch: {mismatches}")
        paired.append({"seed": seed, "baseline_mrr": base, "candidate_mrr": candidate,
                       "matched_control_mrr": control, "delta": candidate-base,
                       "control_delta": candidate-control})
    complete = len(paired) == 3
    wins = sum(row["delta"] > 0 for row in paired)
    control_wins = sum(row["control_delta"] > 0 for row in paired)
    mean_gain = sum(row["delta"] for row in paired) / len(paired) if paired else None
    mean_control_gain = sum(row["control_delta"] for row in paired) / len(paired) if paired else None
    go = complete and wins >= 2 and mean_gain > 0 and control_wins >= 2 and mean_control_gain > 0
    return {"state": "GENERALIZATION_GO" if go else ("GENERALIZATION_REJECT" if complete else "INFRASTRUCTURE_FAILURE"),
            "go": bool(go), "dataset": "pubmed", "wins_vs_baseline": wins,
            "mean_gain": mean_gain, "control_wins": control_wins,
            "mean_gain_vs_control": mean_control_gain, "paired": paired,
            "test_evaluated": False}


def run(workers):
    tasks = make_tasks()
    driver_hash = file_hash(__file__)
    result_path = OUT / "pubmed_generalization_results.json"
    status_path = OUT / "pubmed_generalization_status.json"
    rows, pending = [], []
    for task in tasks:
        path = OUT / "experiments" / task["candidate_id"] / task["arm"] / "result.json"
        prior = None
        if path.exists():
            try:
                prior = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                prior = None
        valid = (prior is not None and prior.get("state") == "COMPLETE"
                 and prior.get("job_id") == task["job_id"]
                 and int(prior.get("epochs", -1)) == 10
                 and int(prior.get("train_record", {}).get("epoch_count", -1)) == 10
                 and prior.get("source_hashes", {}).get(DRIVER_REL) == driver_hash
                 and prior.get("test_evaluated") is False)
        if valid:
            rows.append(prior)
        else:
            pending.append(task)
    runner.atomic_json(status_path, {"state": "RUNNING", "dataset": "pubmed",
                                    "completed": len(rows), "total": len(tasks),
                                    "workers": min(workers, len(pending)),
                                    "test_evaluated": False, "started_at_utc": utc_now(),
                                    "driver_sha256": driver_hash})
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(workers, len(pending)),
                                    mp_context=mp.get_context("spawn"),
                                    initializer=runner.worker_init) as pool:
            futures = {pool.submit(execute, task, driver_hash): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    row = future.result()
                except Exception as exc:
                    row = {**task, "state": "FAILED", "error": repr(exc),
                           "test_evaluated": False, "completed_at_utc": utc_now()}
                rows.append(row)
                runner.atomic_json(result_path, {"dataset": "pubmed", "results": rows,
                                                "decision": summary(rows), "test_evaluated": False,
                                                "driver_sha256": driver_hash})
                runner.atomic_json(status_path, {"state": "RUNNING", "dataset": "pubmed",
                                                "completed": sum(r.get("state") == "COMPLETE" for r in rows),
                                                "total": len(tasks), "failed": [r.get("job_id") for r in rows if r.get("state") != "COMPLETE"],
                                                "workers": min(workers, len(pending)), "test_evaluated": False,
                                                "updated_at_utc": utc_now(), "driver_sha256": driver_hash})
    decision = summary(rows)
    payload = {"dataset": "pubmed", "results": sorted(rows, key=lambda row: (row["seed"], row["arm"])),
               "decision": decision, "test_evaluated": False,
               "driver_sha256": driver_hash, "completed_at_utc": utc_now()}
    runner.atomic_json(result_path, payload)
    runner.atomic_json(status_path, {"state": decision["state"], "dataset": "pubmed",
                                    "completed": sum(r.get("state") == "COMPLETE" for r in rows),
                                    "total": len(tasks), "decision": decision,
                                    "test_evaluated": False, "updated_at_utc": utc_now(),
                                    "driver_sha256": driver_hash})
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise SystemExit("workers must be between 1 and 8")
    payload = run(args.workers)
    print(json.dumps({"dataset": "pubmed", "decision": payload["decision"],
                      "results": [{"job_id": row.get("job_id"), "state": row.get("state"),
                                   "seed": row.get("seed"), "arm": row.get("arm"),
                                   "mrr": row.get("validation_metrics", {}).get("mrr"),
                                   "epochs": row.get("train_record", {}).get("epoch_count"),
                                   "test_evaluated": row.get("test_evaluated")} for row in payload["results"]]},
                     indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
