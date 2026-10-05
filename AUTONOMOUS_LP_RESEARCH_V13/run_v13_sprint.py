from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import multiprocessing as mp
import os
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import run_v13 as runner

ROOT = runner.ROOT
OUT = runner.OUT
DEVICE_ID = "Tesla V100-PCIE-16GB"
BASELINE_ID = "Cora Raw-HG DCDLP + QTHS25 + BCE"
LEDGER_FIELDS = [
    "exp_id", "timestamp_utc", "candidate_id", "family", "parent_state",
    "dataset", "seed", "epochs", "change_summary", "baseline_mrr",
    "candidate_mrr", "delta", "control_mrr", "params", "runtime_s",
    "peak_gpu_mb", "decision", "novelty_status", "checkpoint_sha256",
    "source_hashes", "notes",
]


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    runner.atomic_json(Path(path), value)


def read_json(path, default=None):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def sample_resources(stop, samples):
    while not stop.is_set():
        try:
            raw = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used", "--format=csv,noheader,nounits"],
                text=True, stderr=subprocess.DEVNULL, timeout=3,
            ).strip().splitlines()[0]
            util, mem = [float(v.strip()) for v in raw.split(",")]
            load = os.getloadavg() if hasattr(os, "getloadavg") else None
            samples.append({"time": time.time(), "gpu_util_percent": util,
                            "gpu_memory_used_mb": mem, "load_average": load})
        except Exception as exc:
            samples.append({"time": time.time(), "sample_error": repr(exc)})
        stop.wait(0.75)


def sample_summary(samples):
    good = [s for s in samples if "gpu_util_percent" in s]
    if not good:
        return {"samples": len(samples), "gpu_util_mean_percent": None,
                "gpu_util_peak_percent": None, "gpu_memory_peak_mb": None,
                "cpu_load_average_mean": None}
    loads = [s["load_average"][0] for s in good if s.get("load_average")]
    return {
        "samples": len(samples),
        "gpu_util_mean_percent": sum(s["gpu_util_percent"] for s in good) / len(good),
        "gpu_util_peak_percent": max(s["gpu_util_percent"] for s in good),
        "gpu_memory_peak_mb": max(s["gpu_memory_used_mb"] for s in good),
        "cpu_load_average_mean": sum(loads) / len(loads) if loads else None,
    }


def write_queue(tasks, completed, failures, running):
    fields = ["job_id", "candidate:arm", "stage", "dataset", "seed", "priority",
              "estimated_cost", "status", "gpu_mem_estimate", "start_time", "end_time", "result"]
    rows = ["\t".join(fields)]
    for task in tasks:
        jid = task["job_id"]
        state = "COMPLETE" if jid in completed else (
            "FAILED" if jid in failures else ("RUNNING" if jid in running else "QUEUED")
        )
        result = failures.get(jid, f"experiments/{task['candidate_id']}/{task['arm']}/result.json"
                              if state == "COMPLETE" else "")
        values = [jid, task["candidate_id"] + ":" + task["arm"], task["stage"],
                  task.get("dataset", "cora"), str(task.get("seed", 0)),
                  str(task.get("priority", 0)), str(task.get("estimated_cost", "1 Stage1-eq")),
                  state, task.get("gpu_mem_estimate", "small-Cora"),
                  task.get("started_at", ""), task.get("ended_at", ""), str(result)]
        rows.append("\t".join(values))
    (OUT / "EXPERIMENT_QUEUE.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")


def append_ledger(results, stage, baseline=None, control_map=None, novelty="NOT_SEARCHED"):
    import csv
    path = OUT / "EXPERIMENT_LEDGER.tsv"
    old = list(csv.DictReader(path.open("r", encoding="utf-8-sig"), delimiter="\t")) if path.exists() else []
    seen = {row.get("exp_id") for row in old}
    with path.open("a", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=LEDGER_FIELDS, delimiter="\t", extrasaction="ignore")
        for item in results:
            if item.get("job_id") in seen:
                continue
            metric = item.get("validation_metrics", {}).get("mrr")
            b = baseline
            delta = None if metric is None or b is None else float(metric) - float(b)
            writer.writerow({
                "exp_id": item.get("job_id"), "timestamp_utc": item.get("completed_at_utc"),
                "candidate_id": item.get("candidate_id"), "family": item.get("family"),
                "parent_state": stage, "dataset": item.get("dataset"),
                "seed": item.get("seed"), "epochs": item.get("epochs"),
                "change_summary": item.get("definition"),
                "baseline_mrr": "" if b is None else b,
                "candidate_mrr": "" if metric is None else metric,
                "delta": "" if delta is None else delta,
                "control_mrr": "" if control_map is None else control_map.get(item.get("arm"), ""),
                "params": item.get("trainable_parameters", ""),
                "runtime_s": item.get("total_wall_seconds", ""),
                "peak_gpu_mb": item.get("peak_gpu_memory_mb", ""),
                "decision": item.get("decision", item.get("state")),
                "novelty_status": novelty, "checkpoint_sha256": item.get("checkpoint_sha256", ""),
                "source_hashes": json.dumps(item.get("source_hashes", {}), sort_keys=True),
                "notes": "test_evaluated=false; fixed split/pool/validation candidates; test sealed",
            })


def record_aggregate(key, payload, results, equivalent_count=0, diagnostic=False):
    aggregate = read_json(OUT / "results.json", {})
    aggregate.setdefault("experiments", [])
    old = {r.get("job_id") for r in aggregate["experiments"]}
    aggregate["experiments"].extend(r for r in results if r.get("job_id") not in old)
    aggregate[key] = payload
    aggregate["test_evaluated"] = False
    aggregate["total_training_jobs"] = len(aggregate["experiments"])
    aggregate.setdefault("diagnostic_training_jobs", 0)
    aggregate.setdefault("phasea_stage1_equivalents", 0.0)
    aggregate.setdefault("phaseb_stage1_equivalents", 0.0)
    if diagnostic:
        aggregate["diagnostic_training_jobs"] += len([r for r in results if r.get("state") == "COMPLETE"])
    if key.startswith("phasea"):
        aggregate["phasea_stage1_equivalents"] += equivalent_count
    if key.startswith("phaseb"):
        aggregate["phaseb_stage1_equivalents"] += equivalent_count
    aggregate["updated_at_utc"] = utc_now()
    atomic_json(OUT / "results.json", aggregate)


def make_task(job_id, candidate, arm, stage, definition, epochs=5, sampler="QTHS25",
              seed=0, stage1=True, family="evidence-composition", **extra):
    return {
        "job_id": job_id, "candidate_id": candidate, "arm": arm, "stage": stage,
        "definition": definition, "purpose": definition, "family": family,
        "dataset": "cora", "seed": seed, "epochs": epochs, "sampler": sampler,
        "stage1": stage1, "strong_baseline_identity": BASELINE_ID,
        "priority": 1, "estimated_cost": f"{epochs / 5:.1f} Stage1-eq",
        "gpu_mem_estimate": "Cora <1 GB per process", **extra,
    }


def run_batch(stage, tasks, workers, *, with_resources=True):
    OUT.mkdir(parents=True, exist_ok=True)
    pf = runner.preflight()
    stop = threading.Event()
    samples = []
    sampler_thread = None
    if with_resources:
        sampler_thread = threading.Thread(target=sample_resources, args=(stop, samples), daemon=True)
        sampler_thread.start()

    results, complete, failures, running = [], set(), {}, set()
    pending = []
    source_hash = runner.sha256_file(Path(__file__).with_name("run_v13.py"))
    for task in tasks:
        result_file = OUT / "experiments" / task["candidate_id"] / task["arm"] / "result.json"
        prior = read_json(result_file, {})
        if (prior.get("state") == "COMPLETE" and prior.get("job_id") == task["job_id"]
                and prior.get("source_hashes", {}).get("AUTONOMOUS_LP_RESEARCH_V13/run_v13.py") == source_hash):
            results.append(prior)
            complete.add(task["job_id"])
        else:
            pending.append(task)
    running = {t["job_id"] for t in pending}
    write_queue(tasks, complete, failures, running)
    started_utc = utc_now()
    atomic_json(OUT / "status.json", {
        "state": "RUNNING", "phase": stage, "completed": len(complete),
        "total": len(tasks), "failed_jobs": failures, "test_evaluated": False,
        "gpu": pf["gpu"], "worker_count": workers, "started_at_utc": started_utc,
    })
    start = time.perf_counter()
    try:
        if pending:
            with cf.ProcessPoolExecutor(max_workers=min(workers, len(pending)),
                                        mp_context=mp.get_context("spawn"),
                                        initializer=runner.worker_init) as pool:
                future_tasks = {pool.submit(runner.run_one, t): t for t in pending}
                for future in cf.as_completed(future_tasks):
                    task = future_tasks[future]
                    running.discard(task["job_id"])
                    task["ended_at"] = utc_now()
                    try:
                        item = future.result()
                    except Exception as exc:
                        item = {**task, "state": "FAILED", "error": repr(exc),
                                "completed_at_utc": utc_now(), "test_evaluated": False}
                    results.append(item)
                    if item.get("state") == "COMPLETE":
                        complete.add(task["job_id"])
                    else:
                        failures[task["job_id"]] = item.get("error", "unknown failure")
                    write_queue(tasks, complete, failures, running)
                    atomic_json(OUT / "status.json", {
                        "state": "RUNNING", "phase": stage, "completed": len(complete),
                        "total": len(tasks), "failed_jobs": failures, "test_evaluated": False,
                        "gpu": pf["gpu"], "worker_count": workers, "updated_at_utc": utc_now(),
                    })
                    print(f"{stage}: {len(complete)}/{len(tasks)} complete; {task['job_id']}={item.get('state')}",
                          flush=True)
    finally:
        stop.set()
        if sampler_thread:
            sampler_thread.join(timeout=3)
    wall = time.perf_counter() - start
    resources = sample_summary(samples)
    results.sort(key=lambda r: r.get("job_id", ""))
    output = {
        "stage": stage, "state": "COMPLETE" if not failures else "COMPLETED_WITH_FAILURES",
        "worker_count": workers, "requested_jobs": len(tasks), "completed_jobs": len(complete),
        "failed_jobs": failures, "wall_seconds": wall, "jobs_per_minute": len(complete) / max(wall, 1e-6) * 60,
        "resource_samples": resources, "preflight": pf, "started_at_utc": started_utc,
        "completed_at_utc": utc_now(), "test_evaluated": False, "results": results,
    }
    atomic_json(OUT / f"{stage}_results.json", output)
    write_queue(tasks, complete, failures, set())
    atomic_json(OUT / "status.json", {
        "state": output["state"], "phase": stage, "completed": len(complete),
        "total": len(tasks), "failed_jobs": failures, "test_evaluated": False,
        "gpu": pf["gpu"], "worker_count": workers, "updated_at_utc": utc_now(),
    })
    return output


def run_parallel_benchmark():
    rows = []
    for workers in (1, 2, 4, 8):
        tasks = [
            make_task(f"V13-PAR-{workers}-{i:02d}", f"PAR_C{workers}_J{i:02d}",
                      "BASELINE", "parallel_benchmark",
                      "one-epoch QTHS25 baseline throughput diagnostic; excluded from Stage1-equivalent search budget",
                      epochs=1, stage1=False, family="diagnostic")
            for i in range(1, workers + 1)
        ]
        out = run_batch(f"parallel_c{workers}", tasks, workers)
        rows.append({
            "concurrency": workers, "jobs": len(tasks), "completed": out["completed_jobs"],
            "wall_seconds": out["wall_seconds"], "jobs_per_minute": out["jobs_per_minute"],
            **out["resource_samples"], "failures": out["failed_jobs"],
        })
        append_ledger(out["results"], f"DIAGNOSTIC_PARALLEL_C{workers}")
        record_aggregate(f"parallel_benchmark_c{workers}", out, out["results"], diagnostic=True)
    eligible = [r for r in rows if r["completed"] == r["jobs"] and not r["failures"]]
    best = max((r["jobs_per_minute"] for r in eligible), default=0)
    chosen = max((r["concurrency"] for r in eligible
                  if r["jobs_per_minute"] >= 0.90 * best
                  and (r.get("gpu_memory_peak_mb") or 0) < 0.80 * 16384), default=1)
    report = {
        "definition": "Each concurrency tier trained n independent, one-epoch Cora seed0 QTHS25 baseline replicas; tiers were run sequentially and only within-tier jobs overlapped. These are throughput diagnostics, not Stage1 experiments.",
        "tiers": rows, "selected_workers": chosen,
        "selection_rule": "highest concurrency within 10% of best jobs/minute, all jobs complete, no OOM, and sampled peak memory under 80% of V100 16GB",
        "completed_at_utc": utc_now(),
    }
    atomic_json(OUT / "parallelization_benchmark.json", report)
    return report


def phasea_tasks():
    arms = [
        ("BASELINE", "A0 fresh QTHS25+BCE baseline"),
        ("ECR_RAW", "A1 raw-HG pair evidence only; 24 zero-initialized linear coefficients (3 × branch_dim 8)"),
        ("ECR_STRUCT", "A2 separately standardized degree/CN scalar evidence only; two zero-initialized coefficients"),
        ("ECR_DENSITY", "A3 target-masked cross-exclusive-neighborhood density only; one zero-initialized coefficient"),
        ("ECR_SHUFFLED", "A4 full evidence-calibration form with all evidence rows deterministically shuffled across target pairs"),
        ("ECR_FULL", "A5 full ECR; raw-HG + degree/CN + cross-density + one raw×structure interaction"),
    ]
    return [make_task(f"V13-A-{i:02d}", "ECR", arm, "phasea_ecr", definition,
                      family="evidence-composition", priority=i)
            for i, (arm, definition) in enumerate(arms)]


def summarize_arms(output):
    return {item["arm"]: item for item in output["results"] if item.get("state") == "COMPLETE"}


def run_phase_a(workers):
    out = run_batch("phasea_ecr", phasea_tasks(), workers)
    by = summarize_arms(out)
    if set(("BASELINE", "ECR_RAW", "ECR_STRUCT", "ECR_DENSITY", "ECR_SHUFFLED", "ECR_FULL")) - set(by):
        decision = {"state": "INFRASTRUCTURE_FAILURE", "go": False}
    else:
        base = float(by["BASELINE"]["validation_metrics"]["mrr"])
        singles = {k: float(by[k]["validation_metrics"]["mrr"]) for k in ("ECR_RAW", "ECR_STRUCT", "ECR_DENSITY")}
        full = float(by["ECR_FULL"]["validation_metrics"]["mrr"])
        shuffled = float(by["ECR_SHUFFLED"]["validation_metrics"]["mrr"])
        best_single = max(singles.values())
        delta = full - base
        comp_gain = full - best_single
        params = int(by["ECR_FULL"]["trainable_parameters"]) - int(by["BASELINE"]["trainable_parameters"])
        decision = {
            "state": "ECR_STAGE1_GO" if delta >= 0.003 and comp_gain >= 0.002 and full > shuffled else "ECR_REJECT",
            "go": bool(delta >= 0.003 and comp_gain >= 0.002 and full > shuffled),
            "baseline_mrr": base, "full_mrr": full, "delta": delta,
            "single_mrr": singles, "best_single_mrr": best_single,
            "full_minus_best_single": comp_gain, "shuffled_control_mrr": shuffled,
            "beats_shuffled": full > shuffled, "new_parameters": params,
            "parameter_fraction_percent": 100.0 * params / int(by["BASELINE"]["trainable_parameters"]),
            "gate": {"absolute_delta_ge_0.003": delta >= 0.003,
                     "additive_delta_ge_0.002": comp_gain >= 0.002,
                     "beats_shuffled": full > shuffled},
            "test_evaluated": False,
        }
    atomic_json(OUT / "phasea_decision.json", decision)
    base_metric = decision.get("baseline_mrr")
    control_map = {}
    if decision.get("go"):
        control_map["ECR_FULL"] = decision["shuffled_control_mrr"]
    elif "ECR_FULL" in by:
        control_map["ECR_FULL"] = decision.get("shuffled_control_mrr", "")
    append_ledger(out["results"], "PHASE_A_ECR", base_metric, control_map)
    record_aggregate("phasea_decision", decision, out["results"], equivalent_count=out["completed_jobs"])
    return decision


def run_factorized(workers):
    # Reuse only exact fixed-context results with matching source, epochs, seed, sampler and selected negatives.
    phase = read_json(OUT / "phasea_ecr_results.json", {})
    by = summarize_arms(phase)
    if not all(k in by for k in ("BASELINE", "ECR_RAW", "ECR_STRUCT")):
        return {"state": "REJECTED_INVALID_REUSE", "reason": "baseline and both singles must be complete"}
    ref = by["BASELINE"]
    reuse = {"B0_BASELINE": "BASELINE", "B1_SEMANTIC": "ECR_RAW", "B2_STRUCTURAL": "ECR_STRUCT"}
    reused = {}
    for alias, arm in reuse.items():
        row = by[arm]
        for key in ("dataset", "seed", "epochs", "sampler", "split_hash", "train_pool_hash",
                    "validation_candidate_hash", "selected_negative_hash", "test_evaluated"):
            if row.get(key) != ref.get(key):
                return {"state": "REJECTED_INVALID_REUSE", "reason": f"{arm} context mismatch in {key}"}
        reused[alias] = {**row, "reused_as": alias, "reused_from": row.get("job_id"),
                         "reuse_validated": True, "reused_baseline_context": True}
    tasks = [
        make_task("V13-B-04", "FACTORIZED", "FACT_ADD", "phasea_factorized",
                  "B3 additive semantic Raw-HG evidence plus structural calibration", family="evidence-composition"),
        make_task("V13-B-05", "FACTORIZED", "FACT_INTERACT", "phasea_factorized",
                  "B4 factorized semantic×structural interaction", family="evidence-composition"),
    ]
    out = run_batch("phasea_factorized", tasks, workers)
    trained = summarize_arms(out)
    if not all(k in trained for k in ("FACT_ADD", "FACT_INTERACT")):
        decision = {"state": "INFRASTRUCTURE_FAILURE", "go": False, "reused": reused}
    else:
        base = float(reused["B0_BASELINE"]["validation_metrics"]["mrr"])
        sem = float(reused["B1_SEMANTIC"]["validation_metrics"]["mrr"])
        struct = float(reused["B2_STRUCTURAL"]["validation_metrics"]["mrr"])
        additive = float(trained["FACT_ADD"]["validation_metrics"]["mrr"])
        factored = float(trained["FACT_INTERACT"]["validation_metrics"]["mrr"])
        delta = factored - base
        additive_gain = factored - additive
        go = delta >= max(0.003, 0.01 * base) and additive_gain >= 0.002 and factored > max(sem, struct)
        decision = {
            "state": "FACTORIZED_STAGE1_GO" if go else "FACTOR_COMPOSITION_REJECT",
            "go": go, "baseline_mrr": base, "semantic_mrr": sem, "structural_mrr": struct,
            "additive_mrr": additive, "factorized_mrr": factored,
            "delta": delta, "factorized_minus_additive": additive_gain,
            "factorized_beats_best_single": factored > max(sem, struct),
            "reused": reused, "test_evaluated": False,
        }
    atomic_json(OUT / "phasea_factorized_decision.json", decision)
    actual = out["results"]
    control_map = {"FACT_INTERACT": decision.get("additive_mrr", "")}
    append_ledger(actual, "PHASE_A_FACTORIZED", decision.get("baseline_mrr"), control_map)
    record_aggregate("phasea_factorized_decision", decision, actual, equivalent_count=out["completed_jobs"])
    return decision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--phase-a", action="store_true")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--all-phase-a", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise SystemExit("workers must be in [1,8]")
    OUT.mkdir(parents=True, exist_ok=True)
    if args.benchmark:
        print(json.dumps(run_parallel_benchmark(), indent=2), flush=True)
    elif args.phase_a:
        decision = run_phase_a(args.workers)
        print(json.dumps(decision, indent=2), flush=True)
        if not decision.get("go"):
            decision_b = run_factorized(args.workers)
            print(json.dumps(decision_b, indent=2), flush=True)
    elif args.all_phase_a:
        bench = run_parallel_benchmark()
        workers = bench["selected_workers"]
        decision = run_phase_a(workers)
        if not decision.get("go"):
            decision_b = run_factorized(workers)
        else:
            decision_b = {"state": "SKIPPED_ECR_STAGE1_GO"}
        print(json.dumps({"benchmark": bench, "ECR": decision, "factorized": decision_b}, indent=2), flush=True)
    else:
        parser.error("choose --benchmark, --phase-a or --all-phase-a")


if __name__ == "__main__":
    main()


