from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import math
import multiprocessing as mp
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import run_v13 as runner

OUT = runner.OUT
ROOT = runner.ROOT
sys.path.insert(0, str(OUT / "candidate_patches"))
import phaseb_hooks_v13 as l1_hooks

DRIVER_REL = Path(__file__).resolve().relative_to(ROOT).as_posix()
HOOK_PATH = OUT / "candidate_patches" / "phaseb_hooks_v13.py"
HOOK_REL = HOOK_PATH.resolve().relative_to(ROOT).as_posix()
STATUS_JSON = OUT / "l1_phaseb_status.json"
RESULTS_JSON = OUT / "l1_phaseb_stage1_results.json"
SELECTION_DIR = OUT / "l1_phaseb_selections_cora"
SELECTION_PATH = SELECTION_DIR / "QTHS25.npy"
SELECTION_META = SELECTION_DIR / "QTHS25.json"

EXPECTED_CONTEXT = {
    "split": "c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a",
    "pool": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
    "validation": "aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455",
}
STRONG_BASELINE = "Cora Raw-HG DCDLP + QTHS25 + BCE"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def assert_prerequisites():
    pubmed_path = OUT / "pubmed_generalization_status.json"
    t1_path = OUT / "t1_phaseb_status.json"
    if not pubmed_path.exists() or not t1_path.exists():
        raise RuntimeError("Completed PubMed and Family T records are required before Family L")
    pubmed = json.loads(pubmed_path.read_text(encoding="utf-8"))
    t1 = json.loads(t1_path.read_text(encoding="utf-8"))
    if (pubmed.get("state") != "GENERALIZATION_REJECT"
            or int(pubmed.get("completed", -1)) != int(pubmed.get("total", -2))
            or pubmed.get("test_evaluated") is not False):
        raise RuntimeError("Family L requires the complete, test-sealed PubMed decision")
    if (t1.get("state") != "STAGE1_REJECT"
            or int(t1.get("completed", -1)) != 7
            or int(t1.get("total", -1)) != 7
            or t1.get("test_evaluated") is not False):
        raise RuntimeError("Family L requires the complete, test-sealed T1 Stage 1 decision")


def import_context():
    import experiment_v8 as v8
    full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash = v8.dataset_context("cora")
    observed = {
        "split": v8.base.split_hash(view),
        "pool": pool_hash,
        "validation": valid_hash,
    }
    if observed != EXPECTED_CONTEXT:
        raise RuntimeError(f"Frozen Cora context mismatch: {observed}")
    if pool.shape != (len(view.train_pos), 20, 2):
        raise RuntimeError(f"Unexpected fixed train-only pool shape: {pool.shape}")
    if v8.v61.array_hash(pool) != pool_hash:
        raise RuntimeError("Frozen candidate-pool array hash mismatch")
    return v8, full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash


def prepare_selection():
    v8, _full, view, pool, scores, pool_hash, _vp, _vn, valid_hash = import_context()
    selected = v8.selected_edges(
        {"method": "QTHS25", "seed": 0, "alpha": None}, pool, scores, view.train_pos
    )
    selected = np.asarray(selected, dtype=np.int64).reshape(-1, 2)
    if selected.shape != (len(view.train_pos), 2):
        raise RuntimeError(f"Unexpected QTHS25 negative shape: {selected.shape}")
    selected_hash = v8.v61.array_hash(selected)
    SELECTION_DIR.mkdir(parents=True, exist_ok=True)
    if SELECTION_PATH.exists():
        saved = np.load(SELECTION_PATH, allow_pickle=False)
        if v8.v61.array_hash(saved) != selected_hash:
            raise RuntimeError("Existing Family L QTHS25 override does not match the frozen selection")
    else:
        temp_path = SELECTION_PATH.with_suffix(".npy.tmp")
        with temp_path.open("wb") as stream:
            np.save(stream, selected, allow_pickle=False)
        temp_path.replace(SELECTION_PATH)
    meta = {
        "state": "COMPLETE",
        "dataset": "cora",
        "seed": 0,
        "sampler": "QTHS25",
        "split_hash": v8.base.split_hash(view),
        "train_pool_hash": pool_hash,
        "validation_candidate_hash": valid_hash,
        "selected_negative_hash": selected_hash,
        "selected_file_sha256": sha256_file(SELECTION_PATH),
        "driver_sha256": sha256_file(__file__),
        "test_evaluated": False,
        "created_at_utc": utc_now(),
    }
    if SELECTION_META.exists():
        prior = json.loads(SELECTION_META.read_text(encoding="utf-8"))
        for key in ("split_hash", "train_pool_hash", "validation_candidate_hash", "selected_negative_hash"):
            if prior.get(key) != meta[key]:
                raise RuntimeError(f"Existing Family L selection metadata mismatch: {key}")
    atomic_json(SELECTION_META, meta)
    return meta


def stage1_tasks(selection_meta):
    specs = [
        ("QTHS25_BASELINE", "BASELINE", "QTHS25 plus the registered BCE baseline", "strong baseline"),
        ("L1_EXPECTED_MRR", "L1_EXPECTED_MRR", "Fixed-set expected reciprocal-rank surrogate over 20 candidates", "candidate"),
        ("L1_INDEP_BCE", "L1_INDEP_BCE", "Independent BCE over the same fixed 20 candidates", "compute control C1"),
        ("L1_LISTWISE_RANDOM", "L1_LISTWISE_RANDOM", "Softmax listwise loss over a random 20-draw set from the fixed pool", "objective control C2"),
        ("L1_REPEAT_BCE", "L1_REPEAT_BCE", "Twenty repeated K=1 BCE draws from the fixed pool", "compute control C3"),
    ]
    tasks = []
    for name, arm, definition, purpose in specs:
        tasks.append({
            "job_id": f"V13-PHASEB-L1-STAGE1-{name}-s0",
            "candidate_id": "V13_PHASEB_L1_STAGE1_s0",
            "arm": arm,
            "definition": definition,
            "purpose": purpose,
            "stage": "phase1_phaseb_l1_stage1",
            "dataset": "cora",
            "seed": 0,
            "epochs": 5,
            "sampler": "QTHS25",
            "negative_override_path": str(SELECTION_PATH),
            "negative_override_hash": selection_meta["selected_negative_hash"],
            "priority": "P1",
            "status": "QUEUED",
            "stage1": True,
            "strong_baseline_identity": STRONG_BASELINE,
            "research_context": (
                "Same frozen Cora split, train-only 20-candidate pool, QTHS25 selected negatives, "
                "validation candidates, backbone, seed, and five-epoch budget. Candidate and three "
                "objective controls score the same 20 candidates per training positive."
            ),
            "selection_file_sha256": selection_meta["selected_file_sha256"],
        })
    return tasks


def source_hashes():
    paths = [
        ROOT / "src/dcdlp/train.py",
        ROOT / "src/dcdlp/models/dcdlp.py",
        ROOT / "src/dcdlp/evaluate.py",
        ROOT / "src/dcdlp/evaluation/ranking.py",
        ROOT / "HYPERGRAPH_RESEARCH/QTHS_V8_PAPER/experiment_v8.py",
        ROOT / "AUTONOMOUS_LP_RESEARCH_V13/run_v13.py",
        Path(__file__).resolve(),
        HOOK_PATH,
    ]
    return {str(path.relative_to(ROOT)): sha256_file(path) for path in paths}


def execute_task(task, driver_hash, hook_hash):
    runner.worker_init()
    import experiment_v8 as v8

    v8_module, _full, view, pool, _scores, pool_hash, _vp, _vn, valid_hash = import_context()
    selected = np.load(task["negative_override_path"], allow_pickle=False)
    if v8_module.v61.array_hash(selected) != task["negative_override_hash"]:
        raise RuntimeError(f"Registered QTHS25 negative hash mismatch for {task['job_id']}")
    if (v8.base.split_hash(view) != EXPECTED_CONTEXT["split"]
            or pool_hash != EXPECTED_CONTEXT["pool"]
            or valid_hash != EXPECTED_CONTEXT["validation"]):
        raise RuntimeError("Worker loaded a different frozen Cora context")

    old_factory = runner.loss_hook
    l1_hooks.configure(task["arm"], view.train_pos, pool, runner)
    l1_hooks.install_hooks()
    runner.install_hooks()
    runner.loss_hook = lambda arm: l1_hooks.loss_hook_factory(arm, runner, old_factory)
    try:
        result = runner.run_one(task)
    finally:
        runner.loss_hook = old_factory

    result.setdefault("source_hashes", {})[DRIVER_REL] = driver_hash
    result["source_hashes"][HOOK_REL] = hook_hash
    result["l1_driver_sha256"] = driver_hash
    result["l1_hooks_sha256"] = hook_hash
    result["l1_candidate_pool_size"] = 20 if task["arm"].startswith("L1_") else 1
    result["l1_objective"] = task["arm"]
    result["research_context"] = task["research_context"]
    result["test_evaluated"] = False
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    runner.atomic_json(folder / "result.json", result)
    return result


def summarize_stage1(rows, driver_hash, hook_hash):
    names = (
        "QTHS25_BASELINE",
        "L1_EXPECTED_MRR",
        "L1_INDEP_BCE",
        "L1_LISTWISE_RANDOM",
        "L1_REPEAT_BCE",
    )
    by_name = {row.get("definition"): row for row in rows if row.get("state") == "COMPLETE"}
    missing = [name for name in names if name not in by_name]
    if missing:
        return {
            "state": "RUNNING" if len(rows) < len(names) else "INFRASTRUCTURE_FAILURE",
            "go": False,
            "missing": missing,
            "test_evaluated": False,
        }
    all_rows = [by_name[name] for name in names]
    for row in all_rows:
        if (int(row.get("epochs", -1)) != 5
                or int(row.get("train_record", {}).get("epoch_count", -1)) != 5
                or row.get("test_evaluated") is not False
                or row.get("l1_driver_sha256") != driver_hash
                or row.get("l1_hooks_sha256") != hook_hash):
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                    "invalid_job": row.get("job_id"), "test_evaluated": False}
    for key in ("split_hash", "train_pool_hash", "validation_candidate_hash", "selected_negative_hash"):
        if len({row.get(key) for row in all_rows}) != 1:
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                    "context_mismatch": key, "test_evaluated": False}
    if len({int(row.get("trainable_parameters", -1)) for row in all_rows}) != 1:
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                "context_mismatch": "trainable_parameters", "test_evaluated": False}
    source_maps = {json.dumps(row.get("source_hashes", {}), sort_keys=True) for row in all_rows}
    if len(source_maps) != 1:
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                "context_mismatch": "source_hashes", "test_evaluated": False}

    def m(name):
        return float(by_name[name]["validation_metrics"]["mrr"])

    baseline = m("QTHS25_BASELINE")
    candidate = m("L1_EXPECTED_MRR")
    controls = {
        "independent_bce": m("L1_INDEP_BCE"),
        "random_set_listwise": m("L1_LISTWISE_RANDOM"),
        "repeated_k1_bce": m("L1_REPEAT_BCE"),
    }
    delta = candidate - baseline
    relative_delta = delta / baseline if baseline else float("-inf")
    gain_gate = delta >= 0.003 or relative_delta >= 0.01
    controls_pass = all(candidate > value for value in controls.values())
    go = gain_gate and controls_pass
    return {
        "state": "STAGE1_GO" if go else "STAGE1_REJECT",
        "go": bool(go),
        "baseline_mrr": baseline,
        "candidate_mrr": candidate,
        "delta_vs_qths25": delta,
        "relative_delta_vs_qths25": relative_delta,
        "stage1_gain_gate": bool(gain_gate),
        "compute_control_mrr": controls,
        "compute_control_margins": {name: candidate - value for name, value in controls.items()},
        "compute_controls_pass": bool(controls_pass),
        "all_mrr": {name: m(name) for name in names},
        "parameters": int(by_name["QTHS25_BASELINE"]["trainable_parameters"]),
        "fixed_train_pool_size": 20,
        "common_negative_hash": all_rows[0].get("selected_negative_hash"),
        "test_evaluated": False,
    }


def run_stage1(workers, selection_meta):
    assert_prerequisites()
    driver_hash = sha256_file(__file__)
    hook_hash = sha256_file(HOOK_PATH)
    tasks = stage1_tasks(selection_meta)
    prior_rows = []
    if RESULTS_JSON.exists():
        try:
            prior_rows = json.loads(RESULTS_JSON.read_text(encoding="utf-8")).get("results", [])
        except Exception:
            prior_rows = []
    prior_by_job = {row.get("job_id"): row for row in prior_rows}
    results, pending = [], []
    for task in tasks:
        prior = prior_by_job.get(task["job_id"])
        valid = (
            prior is not None
            and prior.get("state") == "COMPLETE"
            and int(prior.get("epochs", -1)) == 5
            and int(prior.get("train_record", {}).get("epoch_count", -1)) == 5
            and prior.get("l1_driver_sha256") == driver_hash
            and prior.get("l1_hooks_sha256") == hook_hash
            and prior.get("selected_negative_hash") == task["negative_override_hash"]
            and prior.get("test_evaluated") is False
        )
        if valid:
            results.append(prior)
        else:
            pending.append(task)

    atomic_json(STATUS_JSON, {
        "state": "STAGE1_RUNNING",
        "stage": "phase1_phaseb_l1_stage1",
        "completed": len(results),
        "total": len(tasks),
        "workers": min(workers, len(pending)),
        "failed": [],
        "test_evaluated": False,
        "driver_sha256": driver_hash,
        "hooks_sha256": hook_hash,
        "updated_at_utc": utc_now(),
    })
    if pending:
        with cf.ProcessPoolExecutor(
            max_workers=min(workers, len(pending)),
            mp_context=mp.get_context("spawn"),
            initializer=runner.worker_init,
        ) as executor:
            futures = {executor.submit(execute_task, task, driver_hash, hook_hash): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    row = future.result()
                except Exception as exc:
                    row = {
                        **task,
                        "state": "FAILED",
                        "error": repr(exc),
                        "traceback": traceback.format_exc(),
                        "test_evaluated": False,
                        "completed_at_utc": utc_now(),
                    }
                results.append(row)
                decision = summarize_stage1(results, driver_hash, hook_hash)
                atomic_json(RESULTS_JSON, {
                    "stage": "phase1_phaseb_l1_stage1",
                    "results": results,
                    "decision": decision,
                    "test_evaluated": False,
                    "driver_sha256": driver_hash,
                    "hooks_sha256": hook_hash,
                })
                atomic_json(STATUS_JSON, {
                    "state": "STAGE1_RUNNING",
                    "stage": "phase1_phaseb_l1_stage1",
                    "completed": sum(row.get("state") == "COMPLETE" for row in results),
                    "total": len(tasks),
                    "workers": min(workers, len(pending)),
                    "failed": [row.get("job_id") for row in results if row.get("state") != "COMPLETE"],
                    "test_evaluated": False,
                    "driver_sha256": driver_hash,
                    "hooks_sha256": hook_hash,
                    "updated_at_utc": utc_now(),
                })

    decision = summarize_stage1(results, driver_hash, hook_hash)
    atomic_json(RESULTS_JSON, {
        "stage": "phase1_phaseb_l1_stage1",
        "results": sorted(results, key=lambda row: row.get("job_id", "")),
        "decision": decision,
        "test_evaluated": False,
        "driver_sha256": driver_hash,
        "hooks_sha256": hook_hash,
        "completed_at_utc": utc_now(),
    })
    final_state = decision["state"]
    atomic_json(STATUS_JSON, {
        "state": final_state,
        "stage": "phase1_phaseb_l1_stage1",
        "completed": sum(row.get("state") == "COMPLETE" for row in results),
        "total": len(tasks),
        "decision": decision,
        "test_evaluated": False,
        "driver_sha256": driver_hash,
        "hooks_sha256": hook_hash,
        "updated_at_utc": utc_now(),
    })
    return {"decision": decision, "results": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    assert_prerequisites()
    selection_meta = prepare_selection()
    if args.preflight_only:
        print(json.dumps({
            "state": "PREFLIGHT_PASS",
            "selection": selection_meta,
            "driver_sha256": sha256_file(__file__),
            "hooks_sha256": sha256_file(HOOK_PATH),
            "test_evaluated": False,
        }, indent=2))
        return
    result = run_stage1(max(1, int(args.workers)), selection_meta)
    print(json.dumps(result["decision"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
