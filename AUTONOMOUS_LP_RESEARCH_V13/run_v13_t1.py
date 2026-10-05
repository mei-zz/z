from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import multiprocessing as mp
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import run_v13 as runner

OUT = runner.OUT
ROOT = runner.ROOT
DRIVER_REL = Path(__file__).resolve().relative_to(ROOT).as_posix()
TRAJECTORY_NPZ = OUT / "t1_teacher_trajectory_cora.npz"
TRAJECTORY_JSON = OUT / "t1_teacher_trajectory_cora.json"
SELECTION_NPZ = OUT / "t1_registered_selections_cora.npz"
SELECTION_JSON = OUT / "t1_registered_selections_cora.json"
SELECTION_DIR = OUT / "t1_selections_cora"


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


def import_context(dataset="cora"):
    import experiment_v8 as v8
    full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash = v8.dataset_context(dataset)
    return v8, full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash


def assert_i1_generalization_go():
    path = OUT / "pubmed_generalization_status.json"
    if not path.exists():
        raise RuntimeError("I1 cross-dataset gate is not available; wait for PubMed Stage 3")
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("state") != "GENERALIZATION_GO" or state.get("test_evaluated") is not False:
        raise RuntimeError(f"I1 is not confirmed for Phase 2: {state.get('state')}")


def capture_teacher_trajectory():
    """Capture train-pool scores after each of ten Graph-hard teacher epochs."""
    assert_i1_generalization_go()
    driver_hash = sha256_file(__file__)
    if TRAJECTORY_NPZ.exists() and TRAJECTORY_JSON.exists():
        meta = json.loads(TRAJECTORY_JSON.read_text(encoding="utf-8"))
        if meta.get("driver_sha256") == driver_hash and meta.get("state") == "COMPLETE":
            return meta

    import torch
    import run_v13 as local_runner
    v8, _full, view, pool, frozen_scores, pool_hash, _vp, valid_neg, valid_hash = import_context("cora")
    train_graph = view.train_graph()
    train_edges = {local_runner.canonical(edge) for edge in train_graph.edges()}
    if any(local_runner.canonical(pair) in train_edges for pair in pool.reshape(-1, 2)):
        raise RuntimeError("T1 trajectory pool contains a message-passing edge")
    if pool.shape != (len(view.train_pos), 20, 2):
        raise RuntimeError(f"Unexpected frozen Cora train pool shape: {pool.shape}")

    selected = v8.selected_edges(
        {"method": "GRAPH_HARD", "seed": 0, "alpha": None},
        pool, frozen_scores, view.train_pos,
    )
    from dcdlp import train as train_module
    original_score_pairs = train_module.score_pairs
    snapshots = []
    _fixed_valid_pos, fixed_valid_neg, _fixed_valid_hash = v8.engine.validation_arrays()
    expected_validation_negatives = v8.v61.array_hash(fixed_valid_neg.reshape(-1, 2))

    def capture_score_pairs(model, x, edge_index, pairs, batch_size=0):
        scored = original_score_pairs(model, x, edge_index, pairs, batch_size=batch_size)
        pair_array = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
        if len(snapshots) < 10 and v8.v61.array_hash(pair_array) == expected_validation_negatives:
            model.eval()
            candidate_tensor = torch.as_tensor(
                pool.reshape(-1, 2), dtype=torch.long, device=x.device
            )
            with torch.no_grad():
                candidate_logits = model(
                    x, edge_index, candidate_tensor, remove_target_edges=False
                )["logit"]
            values = candidate_logits.detach().float().cpu().numpy().reshape(pool.shape[:2])
            if values.shape != pool.shape[:2] or not np.isfinite(values).all():
                raise RuntimeError("Invalid per-epoch scores for the frozen T1 train pool")
            snapshots.append(values)
        return scored

    train_module.score_pairs = capture_score_pairs
    task = {
        "job_id": "V13-I2-T1-TEACHER-CORA-SEED0",
        "candidate_id": "V13_I2_T1_TEACHER_CORA_SEED0",
        "arm": "BASELINE",
        "innovation": "T1 Persistent Hardness Selection",
        "family": "negative-hardness-trajectory",
        "definition": "Ten-epoch Graph-hard Raw-HG DCDLP teacher; capture every frozen train-pool candidate score after epochs 1-10",
        "purpose": "train-only teacher trajectory; not a candidate result",
        "stage": "phase2_teacher",
        "dataset": "cora",
        "seed": 0,
        "epochs": 10,
        "sampler": "GRAPH_HARD",
        "stage1": False,
        "research_context": "Graph-hard sampler context; same frozen Cora split, train pool, and validation candidates",
    }
    try:
        teacher = local_runner.run_one(task)
    finally:
        train_module.score_pairs = original_score_pairs
    if len(snapshots) != 10:
        raise RuntimeError(f"Expected 10 train-pool snapshots, captured {len(snapshots)}")
    if int(teacher.get("train_record", {}).get("epoch_count", -1)) != 10:
        raise RuntimeError("T1 teacher did not complete exactly ten epochs")
    if teacher.get("test_evaluated") is not False:
        raise RuntimeError("T1 teacher unexpectedly evaluated test data")

    trajectory = np.stack(snapshots, axis=0).astype(np.float32, copy=False)
    np.savez_compressed(TRAJECTORY_NPZ, scores=trajectory)
    meta = {
        "state": "COMPLETE",
        "dataset": "cora",
        "teacher_seed": 0,
        "teacher_sampler": "GRAPH_HARD",
        "teacher_epochs": 10,
        "captured_epochs": list(range(1, 11)),
        "train_pool_shape": list(pool.shape),
        "train_pool_hash": pool_hash,
        "validation_candidate_hash": valid_hash,
        "teacher_selected_negative_hash": teacher.get("selected_negative_hash"),
        "trajectory_shape": list(trajectory.shape),
        "trajectory_sha256": sha256_file(TRAJECTORY_NPZ),
        "trajectory_score_array_hash": v8.v61.array_hash(trajectory),
        "teacher_checkpoint_sha256": teacher.get("checkpoint_sha256"),
        "teacher_epoch_count": int(teacher["train_record"]["epoch_count"]),
        "source_hashes": teacher.get("source_hashes", {}),
        "driver_sha256": driver_hash,
        "test_evaluated": False,
        "completed_at_utc": utc_now(),
    }
    atomic_json(TRAJECTORY_JSON, meta)
    return meta


def _hardness_percentiles(scores):
    scores = np.asarray(scores, dtype=np.float64)
    if scores.ndim != 3 or scores.shape[0] != 10 or scores.shape[2] != 20:
        raise RuntimeError(f"Expected [10, positives, 20] teacher scores, got {scores.shape}")
    if not np.isfinite(scores).all():
        raise RuntimeError("Teacher trajectory contains non-finite scores")
    # Within each positive's fixed pool, percentile 1 is the highest-scored (hardest) negative.
    order = np.argsort(scores, axis=2, kind="stable")
    ranks = np.argsort(order, axis=2, kind="stable")
    return ranks.astype(np.float32) / 19.0


def build_selections():
    driver_hash = sha256_file(__file__)
    if not TRAJECTORY_NPZ.exists() or not TRAJECTORY_JSON.exists():
        raise RuntimeError("T1 teacher trajectory is missing; run --mode teacher first")
    trajectory_meta = json.loads(TRAJECTORY_JSON.read_text(encoding="utf-8"))
    if trajectory_meta.get("state") != "COMPLETE" or trajectory_meta.get("test_evaluated") is not False:
        raise RuntimeError("T1 teacher trajectory metadata is not complete validation-only evidence")
    if trajectory_meta.get("driver_sha256") != sha256_file(__file__):
        raise RuntimeError("T1 teacher trajectory was captured by a different driver revision")
    with np.load(TRAJECTORY_NPZ, allow_pickle=False) as archive:
        scores = archive["scores"].copy()
    v8, _full, view, pool, frozen_scores, pool_hash, _vp, _vn, valid_hash = import_context("cora")
    if pool_hash != trajectory_meta.get("train_pool_hash") or valid_hash != trajectory_meta.get("validation_candidate_hash"):
        raise RuntimeError("T1 trajectory context differs from the current frozen Cora context")
    if tuple(scores.shape) != (10, *pool.shape[:2]):
        raise RuntimeError(f"T1 trajectory shape/context mismatch: {scores.shape}")
    ranks = _hardness_percentiles(scores)
    rows = np.arange(len(pool))
    persistent_ids = ranks.min(axis=0).argmax(axis=1)
    final_ids = np.argmax(ranks[-1], axis=1)
    mean_ids = np.argmax(ranks.mean(axis=0), axis=1)

    rng = np.random.default_rng(13002026)
    shuffled_ranks = np.empty_like(ranks)
    for epoch in range(ranks.shape[0]):
        permutations = np.argsort(rng.random(ranks[epoch].shape), axis=1, kind="stable")
        shuffled_ranks[epoch] = np.take_along_axis(ranks[epoch], permutations, axis=1)
    shuffled_ids = shuffled_ranks.min(axis=0).argmax(axis=1)

    # Match final-teacher hardness at a predeclared 20%-wide within-query percentile band.
    final_bins = np.minimum((ranks[-1] * 5).astype(np.int64), 4)
    target_bins = final_bins[rows, persistent_ids]
    rankmatched_ids = np.empty(len(pool), dtype=np.int64)
    for row, target_bin in enumerate(target_bins):
        eligible = np.flatnonzero(final_bins[row] == target_bin)
        alternatives = eligible[eligible != persistent_ids[row]]
        choices = alternatives if len(alternatives) else eligible
        rankmatched_ids[row] = choices[int(rng.integers(0, len(choices)))]

    selected = {
        "GRAPH_HARD": v8.selected_edges({"method": "GRAPH_HARD", "seed": 0, "alpha": None}, pool, frozen_scores, view.train_pos),
        "T1_PERSISTENT": pool[rows, persistent_ids].copy(),
        "T1_FINAL_SNAPSHOT": pool[rows, final_ids].copy(),
        "T1_MEAN_RANK": pool[rows, mean_ids].copy(),
        "T1_TRAJECTORY_SHUFFLED": pool[rows, shuffled_ids].copy(),
        "T1_FINAL_RANK_MATCHED": pool[rows, rankmatched_ids].copy(),
        "SH75": v8.selected_edges({"method": "SH75", "seed": 0, "alpha": None}, pool, frozen_scores, view.train_pos),
        "QTHS25": v8.selected_edges({"method": "QTHS25", "seed": 0, "alpha": None}, pool, frozen_scores, view.train_pos),
    }
    array_hashes = {name: v8.v61.array_hash(array) for name, array in selected.items()}
    np.savez_compressed(SELECTION_NPZ, **selected)
    SELECTION_DIR.mkdir(parents=True, exist_ok=True)
    for name, array in selected.items():
        np.save(SELECTION_DIR / f"{name}.npy", np.asarray(array, dtype=np.int64), allow_pickle=False)
    meta = {
        "state": "COMPLETE",
        "dataset": "cora",
        "selection_rule": "argmax_n min_t within-positive hardness_percentile(t,n), with hardest percentile 1",
        "trajectory_shuffle": "independently permute the 20 candidate ranks within each positive at every teacher epoch, preserving each epoch's rank multiset",
        "final_rank_match": "randomly choose a candidate in the same predeclared 20%-wide final-rank percentile bin as T1, excluding T1 where possible",
        "train_pool_hash": pool_hash,
        "validation_candidate_hash": valid_hash,
        "trajectory_sha256": trajectory_meta["trajectory_sha256"],
        "selected_negative_hashes": array_hashes,
        "selections_file_sha256": sha256_file(SELECTION_NPZ),
        "test_evaluated": False,
        "driver_sha256": driver_hash,
        "created_at_utc": utc_now(),
    }
    atomic_json(SELECTION_JSON, meta)
    return meta


def _task(stage, name, arm, selection_name, dataset="cora", seed=0, epochs=5):
    selection_path = SELECTION_DIR / f"{selection_name}.npy"
    if dataset != "cora":
        selection_path = OUT / f"t1_selections_{dataset}" / f"{selection_name}.npy"
    return {
        "job_id": f"V13-I2-T1-{stage.upper()}-{name}-s{seed}",
        "candidate_id": f"V13_I2_T1_{stage.upper()}_{name}_s{seed}",
        "arm": arm,
        "innovation": "T1 Persistent Hardness Selection",
        "family": "negative-hardness-trajectory",
        "definition": name,
        "purpose": "candidate" if name in {"I2_T1", "I1_PLUS_T1"} else "registered baseline or mechanism control",
        "stage": f"phase2_{stage}",
        "dataset": dataset,
        "seed": int(seed),
        "epochs": int(epochs),
        "sampler": selection_name,
        "negative_override_path": str(selection_path),
        "priority": "P1",
        "status": "QUEUED",
        "stage1": stage == "stage1" and dataset == "cora",
        "research_context": "Graph-hard sampler context; identical frozen split, train pool, and validation candidates",
    }


def execute_task(task, driver_hash):
    selected = np.load(task["negative_override_path"], allow_pickle=False)
    import experiment_v8 as v8
    actual_hash = v8.v61.array_hash(selected)
    task["negative_override_hash"] = actual_hash
    result = runner.run_one(task)
    result.setdefault("source_hashes", {})[DRIVER_REL] = driver_hash
    result["phase2_driver_sha256"] = driver_hash
    result["research_context"] = task["research_context"]
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    runner.atomic_json(folder / "result.json", result)
    return result


def stage1_tasks():
    specs = [
        ("BASELINE_GRAPH_HARD", "BASELINE", "GRAPH_HARD"),
        ("I1_ECR_GRAPH_HARD", "ECR_FULL", "GRAPH_HARD"),
        ("I2_T1", "BASELINE", "T1_PERSISTENT"),
        ("I1_PLUS_T1", "ECR_FULL", "T1_PERSISTENT"),
        ("T1_FINAL_SNAPSHOT", "BASELINE", "T1_FINAL_SNAPSHOT"),
        ("T1_MEAN_RANK", "BASELINE", "T1_MEAN_RANK"),
        ("T1_TRAJECTORY_SHUFFLED", "BASELINE", "T1_TRAJECTORY_SHUFFLED"),
        ("T1_FINAL_RANK_MATCHED", "BASELINE", "T1_FINAL_RANK_MATCHED"),
        ("I1_PLUS_T1_TRAJECTORY_SHUFFLED", "ECR_FULL", "T1_TRAJECTORY_SHUFFLED"),
        ("SH75_CONTROL", "BASELINE", "SH75"),
        ("QTHS25_CONTROL", "BASELINE", "QTHS25"),
    ]
    return [_task("stage1", name, arm, selection, epochs=5) for name, arm, selection in specs]


def summarize_stage1(rows):
    by_name = {row.get("definition"): row for row in rows if row.get("state") == "COMPLETE"}
    required = ("BASELINE_GRAPH_HARD", "I1_ECR_GRAPH_HARD", "I2_T1", "I1_PLUS_T1",
                "T1_TRAJECTORY_SHUFFLED", "T1_FINAL_RANK_MATCHED", "I1_PLUS_T1_TRAJECTORY_SHUFFLED")
    if any(name not in by_name for name in required):
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False, "test_evaluated": False}
    all_rows = list(by_name.values())
    for key in ("split_hash", "train_pool_hash", "validation_candidate_hash"):
        if len({row.get(key) for row in all_rows}) != 1:
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                    "context_mismatch": key, "test_evaluated": False}
    source_maps = {json.dumps(row.get("source_hashes", {}), sort_keys=True) for row in all_rows}
    if len(source_maps) != 1:
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                "context_mismatch": "source_hashes", "test_evaluated": False}
    for left, right in (("BASELINE_GRAPH_HARD", "I1_ECR_GRAPH_HARD"),
                        ("I2_T1", "I1_PLUS_T1"),
                        ("T1_TRAJECTORY_SHUFFLED", "I1_PLUS_T1_TRAJECTORY_SHUFFLED")):
        if by_name[left].get("selected_negative_hash") != by_name[right].get("selected_negative_hash"):
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                    "sample_mismatch": [left, right], "test_evaluated": False}
    def m(name):
        return float(by_name[name]["validation_metrics"]["mrr"])
    baseline, i1, t1, combo = m("BASELINE_GRAPH_HARD"), m("I1_ECR_GRAPH_HARD"), m("I2_T1"), m("I1_PLUS_T1")
    shuffle, rankmatched = m("T1_TRAJECTORY_SHUFFLED"), m("T1_FINAL_RANK_MATCHED")
    combo_shuffle = m("I1_PLUS_T1_TRAJECTORY_SHUFFLED")
    standalone_delta, additive_delta = t1 - baseline, combo - i1
    standalone_gate = standalone_delta >= 0.003 or (baseline > 0 and standalone_delta / baseline >= 0.01)
    additive_gate = additive_delta >= 0.002
    mechanism = t1 > shuffle and t1 > rankmatched and combo > combo_shuffle
    go = mechanism and (standalone_gate or additive_gate)
    return {
        "state": "STAGE1_GO" if go else "STAGE1_REJECT",
        "go": bool(go),
        "baseline_graph_hard_mrr": baseline,
        "i1_ecr_graph_hard_mrr": i1,
        "i2_t1_mrr": t1,
        "i1_plus_t1_mrr": combo,
        "t1_trajectory_shuffled_mrr": shuffle,
        "t1_final_rank_matched_mrr": rankmatched,
        "i1_plus_t1_shuffled_mrr": combo_shuffle,
        "standalone_delta": standalone_delta,
        "additive_delta": additive_delta,
        "standalone_gate": bool(standalone_gate),
        "additive_gate": bool(additive_gate),
        "mechanism_controls_pass": bool(mechanism),
        "all_results": {name: m(name) for name in sorted(by_name)},
        "test_evaluated": False,
    }


def run_stage1(workers=8):
    assert_i1_generalization_go()
    driver_hash = sha256_file(__file__)
    if not TRAJECTORY_JSON.exists() or not TRAJECTORY_NPZ.exists():
        raise RuntimeError("T1 trajectory is missing; run --mode teacher as a separate process first")
    trajectory_meta = json.loads(TRAJECTORY_JSON.read_text(encoding="utf-8"))
    if trajectory_meta.get("driver_sha256") != driver_hash:
        raise RuntimeError("T1 trajectory uses another driver revision; rerun --mode teacher first")
    if not SELECTION_NPZ.exists() or not SELECTION_JSON.exists():
        raise RuntimeError("T1 selection arrays are missing; rerun --mode teacher to build them")
    selection_meta = json.loads(SELECTION_JSON.read_text(encoding="utf-8"))
    if selection_meta.get("driver_sha256") != driver_hash:
        build_selections()
    tasks = stage1_tasks()
    import experiment_v8 as v8
    for task in tasks:
        selected = np.load(task["negative_override_path"], allow_pickle=False)
        task["negative_override_hash"] = v8.v61.array_hash(selected)
    results_path = OUT / "t1_stage1_results.json"
    status_path = OUT / "t1_stage1_status.json"
    prior_rows = []
    if results_path.exists():
        try:
            prior_rows = json.loads(results_path.read_text(encoding="utf-8")).get("results", [])
        except Exception:
            prior_rows = []
    by_job = {row.get("job_id"): row for row in prior_rows}
    results, pending = [], []
    for task in tasks:
        prior = by_job.get(task["job_id"])
        valid = (prior is not None and prior.get("state") == "COMPLETE"
                 and int(prior.get("epochs", -1)) == 5
                 and int(prior.get("train_record", {}).get("epoch_count", -1)) == 5
                 and prior.get("source_hashes", {}).get(DRIVER_REL) == driver_hash
                 and prior.get("selected_negative_hash") == task["negative_override_hash"]
                 and prior.get("test_evaluated") is False)
        if valid:
            results.append(prior)
        else:
            pending.append(task)
    atomic_json(status_path, {"state": "RUNNING", "completed": len(results), "total": len(tasks),
                              "workers": min(workers, len(pending)), "test_evaluated": False,
                              "driver_sha256": driver_hash, "started_at_utc": utc_now()})
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(workers, len(pending)),
                                    mp_context=mp.get_context("spawn"),
                                    initializer=runner.worker_init) as executor:
            futures = {executor.submit(execute_task, task, driver_hash): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    row = future.result()
                except Exception as exc:
                    row = {**task, "state": "FAILED", "error": repr(exc), "test_evaluated": False,
                           "completed_at_utc": utc_now()}
                results.append(row)
                decision = summarize_stage1(results)
                atomic_json(results_path, {"stage": "stage1", "results": results,
                                          "decision": decision, "test_evaluated": False,
                                          "driver_sha256": driver_hash})
                atomic_json(status_path, {"state": "RUNNING", "completed": sum(r.get("state") == "COMPLETE" for r in results),
                                         "total": len(tasks), "workers": min(workers, len(pending)),
                                         "failed": [r.get("job_id") for r in results if r.get("state") != "COMPLETE"],
                                         "test_evaluated": False, "driver_sha256": driver_hash,
                                         "updated_at_utc": utc_now()})
    decision = summarize_stage1(results)
    atomic_json(results_path, {"stage": "stage1", "results": sorted(results, key=lambda r: r.get("job_id", "")),
                              "decision": decision, "test_evaluated": False,
                              "driver_sha256": driver_hash, "completed_at_utc": utc_now()})
    atomic_json(status_path, {"state": decision["state"], "completed": sum(r.get("state") == "COMPLETE" for r in results),
                              "total": len(tasks), "decision": decision, "test_evaluated": False,
                              "driver_sha256": driver_hash, "updated_at_utc": utc_now()})
    return {"decision": decision, "results": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("teacher", "stage1"), required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise SystemExit("workers must be between 1 and 8")
    if args.mode == "teacher":
        value = capture_teacher_trajectory()
        build_selections()
        print(json.dumps({"teacher": value, "selections": json.loads(SELECTION_JSON.read_text(encoding="utf-8"))},
                         indent=2, ensure_ascii=False), flush=True)
    else:
        value = run_stage1(args.workers)
        print(json.dumps({"decision": value["decision"], "results": [
            {"job_id": row.get("job_id"), "state": row.get("state"),
             "mrr": row.get("validation_metrics", {}).get("mrr"),
             "epochs": row.get("train_record", {}).get("epoch_count"),
             "test_evaluated": row.get("test_evaluated")} for row in value["results"]]},
            indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
