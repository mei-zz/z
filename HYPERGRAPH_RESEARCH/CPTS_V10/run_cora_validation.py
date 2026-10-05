"""Run only registered Cora validation arms; test use remains disabled."""
from __future__ import annotations

import concurrent.futures as cf
import json
import multiprocessing as mp
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "HYPERGRAPH_RESEARCH" / "CPTS_V10"
HR = ROOT / "HYPERGRAPH_RESEARCH"
V71 = HR / "QTHS_V7_1"
V8DIR = HR / "QTHS_V8_PAPER"
sys.path[:0] = [str(ROOT / "src"), str(HR / "QTHS_V8_PAPER")]
import experiment_v8 as v8  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def task_key(method, seed):
    return f"CORA_GCN_{method}_SEED{seed}".lower()


def state_file(method, seed):
    return OUT / "STATE" / f"{task_key(method, seed)}.json"


def worker(task):
    v8.worker_init()
    import torch

    method, seed = task["method"], int(task["seed"])
    original_load = v8.configure_backbone("gcn")
    started = time.perf_counter()
    state = state_file(method, seed)
    try:
        full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash = v8.dataset_context("cora")
        ids = np.asarray(task["selected_indices"], dtype=np.int64)
        if ids.shape != (len(view.train_pos),):
            raise RuntimeError(f"Bad selector size {ids.shape}")
        selected = pool[np.arange(len(pool)), ids].copy()
        if len(selected) != len(view.train_pos):
            raise RuntimeError("One selected training negative is required per positive")
        _, forbidden = v8.v61.make_train_forbidden(view)
        if any(v8.v61.canonical_edge(pair) in forbidden for pair in selected):
            raise RuntimeError("Selector emitted a train-forbidden pair")
        v8.engine.candidate_pool = pool
        v8.engine.candidate_pool_hash = pool_hash
        v8.engine.validation_candidate_hash = valid_hash
        run_rel = Path("HYPERGRAPH_RESEARCH") / "CPTS_V10" / "RUNS" / "CORA" / "GCN" / method / f"seed{seed}"
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
        rec = v8.engine.train_one(
            view, method, seed, selected, run_rel.as_posix(), valid_pos, valid_neg,
            initialize_from_v6=False, dataset_name="cora", hypergraph_mode="raw",
        )
        metrics, params = v8.metric_for_checkpoint(rec["checkpoint"], view, valid_pos, valid_neg)
        if abs(metrics["mrr"] - float(rec["epoch10_validation_mrr"])) > 1e-9:
            raise RuntimeError("Epoch-10 validation metric did not reproduce")
        torch.cuda.synchronize()
        result = {
            "state": "COMPLETE", "task": {"method": method, "seed": seed, "stage": "cora_validation"},
            "training_record": rec, "validation_metrics": metrics, "trainable_parameters": params,
            "train_pool_hash": pool_hash, "validation_candidate_hash": valid_hash,
            "peak_gpu_memory_mb": float(torch.cuda.max_memory_allocated() / 1024**2),
            "wall_seconds": time.perf_counter() - started, "test_evaluated": False,
        }
        write_json(state, result)
        return result
    except Exception as exc:
        result = {"state": "FAILED", "method": method, "seed": seed,
                  "error": repr(exc), "traceback": traceback.format_exc()}
        write_json(state, result)
        raise
    finally:
        v8.v61.load_json = original_load


def cached_validation():
    v71 = read_json(V71 / "results.json")["cora"]["validation"]["runs"]
    v8r = read_json(V8DIR / "results.json")
    out = {}
    names = {"UNIFORM": "C0_UNIFORM", "GRAPH_HARD": "C1_GRAPH_HARD", "RANDOM_VETO": "C2_RANDOM_VETO", "QTHS25": "C3_QTHS25"}
    for name, key in names.items():
        out[name] = {str(seed): float(v71[key][str(seed)]["validation_metrics"]["mrr"]) for seed in (0, 1, 2)}
    out["SH75"] = {str(seed): float(v) for seed, v in enumerate(v8r["semi_hard_control"]["by_seed"])}
    return out


def summarize(records):
    baseline = cached_validation()
    methods = dict(baseline)
    for method in ("CPTS", "GLOBAL_CPTS", "MATCHED_Q", "RANDOM_MATCHED"):
        methods[method] = {}
        for seed in (0, 1, 2):
            rec = read_json(state_file(method, seed))
            if rec.get("state") != "COMPLETE":
                raise RuntimeError(f"Missing completed state for {method} seed {seed}")
            methods[method][str(seed)] = float(rec["validation_metrics"]["mrr"])
    deltas = {name: [methods["CPTS"][str(s)] - methods[name][str(s)] for s in (0, 1, 2)]
              for name in ("GRAPH_HARD", "QTHS25", "SH75", "GLOBAL_CPTS", "MATCHED_Q", "RANDOM_MATCHED")}
    means = {name: float(np.mean(list(vals.values()))) for name, vals in methods.items()}
    wins = {name: int(sum(x > 0 for x in d)) for name, d in deltas.items()}
    graph_go = means["CPTS"] > means["GRAPH_HARD"] and wins["GRAPH_HARD"] >= 2
    sh75_dom = means["CPTS"] < means["SH75"] - .005
    qths_go = wins["QTHS25"] >= 2
    adaptivity = (wins["MATCHED_Q"] >= 2 and np.mean(deltas["MATCHED_Q"]) > 0
                  and wins["RANDOM_MATCHED"] >= 2)
    global_delta = float(np.mean(deltas["GLOBAL_CPTS"]))
    local_adaptivity = global_delta > .001
    if not graph_go:
        decision = "CPTS_REJECT"
    elif sh75_dom:
        decision = "SH75_DOMINATES"
    elif not qths_go:
        decision = "CPTS_REJECT"
    elif not adaptivity:
        decision = "LOCAL_ADAPTIVITY_UNCONFIRMED"
    else:
        decision = "GO"
    result = {
        "state": "CORA_VALIDATION_COMPLETE", "methods_mrr_by_seed": methods,
        "mean_mrr": means, "cpts_paired_delta_by_seed": deltas,
        "cpts_wins": wins, "first_gate_graph_hard": graph_go,
        "sh75_dominates": sh75_dom, "qths_gate": qths_go,
        "matched_controls_gate": adaptivity, "cpts_minus_global_cpts_mean": global_delta,
        "local_adaptivity_confirmed": local_adaptivity,
        "final_decision_at_validation": decision, "test_evaluated": False,
    }
    write_json(OUT / "cora_validation_results.json", result)
    lines = ["# Cora validation", "", "STRICT_TRAIN_ONLY; seeds 0–2; fixed epoch 10; test disabled. Frozen V7.1/V8 arms are reused after pool, candidate and protocol hashes were confirmed by the training harness.", "", "| Method | Seed 0 | Seed 1 | Seed 2 | Mean |", "|---|---:|---:|---:|---:|"]
    for method, values in methods.items():
        lines.append(f"| {method} | {values['0']:.6f} | {values['1']:.6f} | {values['2']:.6f} | {means[method]:.6f} |")
    lines += ["", "## CPTS paired comparisons", "", "| Comparator | Seed deltas | Mean delta | Wins/3 |", "|---|---|---:|---:|"]
    for method, ds in deltas.items():
        lines.append(f"| {method} | {[round(x,6) for x in ds]} | {np.mean(ds):+.6f} | {wins[method]}/3 |")
    lines += ["", f"Validation decision: **{decision}**. Test remains disabled in this phase.", ""]
    (OUT / "03_CORA_VALIDATION.md").write_text("\n".join(lines), encoding="utf-8")
    return result


def main():
    info = v8.base.ensure_expected_runtime()
    if not __import__("torch").cuda.is_available():
        raise RuntimeError("CUDA unavailable")
    selector_file = OUT / "cora_selector_indices.npz"
    with np.load(selector_file, allow_pickle=False) as z:
        arms = {
            "CPTS": z["cpts"].copy(), "GLOBAL_CPTS": z["global_cpts"].copy(),
            "MATCHED_Q": z["matched_q"].copy(),
            "RANDOM_MATCHED": {str(s): z[f"random_matched_s{s}"].copy() for s in (0, 1, 2)},
        }
    tasks = []
    for method in ("CPTS", "GLOBAL_CPTS", "MATCHED_Q", "RANDOM_MATCHED"):
        for seed in (0, 1, 2):
            ids = arms[method][str(seed)] if method == "RANDOM_MATCHED" else arms[method]
            task = {"method": method, "seed": seed, "selected_indices": ids.tolist()}
            tasks.append(task)
    status = {"state": "RUNNING", "stage": "CORA_VALIDATION", "workers": 6,
              "gpu": info.get("gpu"), "cpu_count": os.cpu_count(), "total_jobs": len(tasks),
              "completed_jobs": 0, "test_enabled": False}
    write_json(OUT / "status.json", status)
    combined = read_json(OUT / "results.json")
    combined.update({"study_status": "CORA_VALIDATION_RUNNING", "training_started": True,
                     "cora_validation_jobs": 12, "test_evaluated": False,
                     "resource_profile": {"workers": 6, "gpu": info.get("gpu"), "cpu_count": os.cpu_count()}})
    write_json(OUT / "results.json", combined)
    with cf.ProcessPoolExecutor(max_workers=6, mp_context=mp.get_context("spawn")) as pool:
        futures = {pool.submit(worker, task): task for task in tasks}
        for future in cf.as_completed(futures):
            record = future.result()
            status["completed_jobs"] += 1
            status["last_completed"] = record["task"]
            status["last_job_wall_seconds"] = record["wall_seconds"]
            write_json(OUT / "status.json", status)
    summary = summarize(tasks)
    status.update({"state": "CORA_VALIDATION_COMPLETE", "completed_jobs": len(tasks),
                   "decision": summary["final_decision_at_validation"]})
    write_json(OUT / "status.json", status)
    combined = read_json(OUT / "results.json")
    combined.update({"study_status": "CORA_VALIDATION_COMPLETE", "cora_validation": summary,
                     "final_decision_at_validation": summary["final_decision_at_validation"]})
    write_json(OUT / "results.json", combined)
    print(json.dumps(status, indent=2), flush=True)


if __name__ == "__main__":
    main()
