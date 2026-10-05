from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import multiprocessing as mp
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import run_v13 as runner

OUT = runner.OUT
ROOT = runner.ROOT
DRIVER_REL = Path(__file__).resolve().relative_to(ROOT).as_posix()
STATUS_JSON = OUT / "t1_phaseb_status.json"
RESULTS_JSON = OUT / "t1_phaseb_stage1_results.json"
TRAJECTORY_NPZ = OUT / "t1_phaseb_teacher_trajectory_cora.npz"
TRAJECTORY_JSON = OUT / "t1_phaseb_teacher_trajectory_cora.json"
SELECTION_NPZ = OUT / "t1_phaseb_registered_selections_cora.npz"
SELECTION_JSON = OUT / "t1_phaseb_registered_selections_cora.json"
SELECTION_DIR = OUT / "t1_phaseb_selections_cora"


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


def assert_phaseb_eligible():
    path = OUT / "pubmed_generalization_status.json"
    if not path.exists():
        raise RuntimeError("The completed PubMed I1 generalization decision is missing")
    state = json.loads(path.read_text(encoding="utf-8"))
    if (state.get("state") != "GENERALIZATION_REJECT"
            or state.get("test_evaluated") is not False
            or int(state.get("completed", -1)) != int(state.get("total", -2))):
        raise RuntimeError(
            "Phase B T1 requires the completed, test-sealed ECR rejection; "
            f"observed {state.get('state')}"
        )


def import_context(dataset="cora"):
    import experiment_v8 as v8
    full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash = v8.dataset_context(dataset)
    return v8, full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash


def capture_teacher_trajectory():
    """Capture scores for the same frozen train-only negative pool after epochs 1-10."""
    assert_phaseb_eligible()
    driver_hash = sha256_file(__file__)
    if TRAJECTORY_NPZ.exists() and TRAJECTORY_JSON.exists():
        meta = json.loads(TRAJECTORY_JSON.read_text(encoding="utf-8"))
        if meta.get("driver_sha256") == driver_hash and meta.get("state") == "COMPLETE":
            return meta

    import torch
    import run_v13 as local_runner

    _v8, _full, view, pool, frozen_scores, pool_hash, _valid_pos, _valid_neg, valid_hash = import_context("cora")
    train_graph = view.train_graph()
    train_edges = {local_runner.canonical(edge) for edge in train_graph.edges()}
    if any(local_runner.canonical(pair) in train_edges for pair in pool.reshape(-1, 2)):
        raise RuntimeError("T1 trajectory pool contains a training/message edge")
    if pool.shape != (len(view.train_pos), 20, 2):
        raise RuntimeError(f"Unexpected frozen Cora train pool shape: {pool.shape}")

    _v8, _full, view, pool, frozen_scores, _pool_hash, _valid_pos, _valid_neg, _valid_hash = import_context("cora")
    selected = _v8.selected_edges(
        {"method": "GRAPH_HARD", "seed": 0, "alpha": None},
        pool, frozen_scores, view.train_pos,
    )
    from dcdlp import train as train_module

    original_score_pairs = train_module.score_pairs
    snapshots = []
    _fixed_valid_pos, fixed_valid_neg, _fixed_valid_hash = _v8.engine.validation_arrays()
    expected_validation_negatives = _v8.v61.array_hash(fixed_valid_neg.reshape(-1, 2))

    def capture_score_pairs(model, x, edge_index, pairs, batch_size=0):
        scored = original_score_pairs(model, x, edge_index, pairs, batch_size=batch_size)
        pair_array = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
        if len(snapshots) < 10 and _v8.v61.array_hash(pair_array) == expected_validation_negatives:
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
        "job_id": "V13-PHASEB-T1-TEACHER-CORA-SEED0",
        "candidate_id": "V13_PHASEB_T1_TEACHER_CORA_SEED0",
        "arm": "BASELINE",
        "innovation": "T1 Persistent Hardness Selection",
        "family": "negative-hardness-trajectory",
        "definition": "Ten-epoch Graph-hard Raw-HG DCDLP teacher; capture every frozen train-pool candidate score after epochs 1-10",
        "purpose": "train-only teacher trajectory; not a candidate result",
        "stage": "phase1_phaseb_t1_teacher",
        "dataset": "cora",
        "seed": 0,
        "epochs": 10,
        "sampler": "GRAPH_HARD",
        "stage1": False,
        "strong_baseline_identity": "Cora Raw-HG DCDLP + QTHS25 + BCE",
        "research_context": "Phase B T1 teacher; frozen Cora split, train-only candidate pool, and validation candidates",
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

    teacher.setdefault("source_hashes", {})[DRIVER_REL] = driver_hash
    teacher["phaseb_driver_sha256"] = driver_hash
    teacher["test_evaluated"] = False
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    runner.atomic_json(folder / "result.json", teacher)

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
        "trajectory_score_array_hash": _v8.v61.array_hash(trajectory),
        "teacher_checkpoint_sha256": teacher.get("checkpoint_sha256"),
        "teacher_epoch_count": int(teacher["train_record"]["epoch_count"]),
        "source_hashes": teacher.get("source_hashes", {}),
        "driver_sha256": driver_hash,
        "test_evaluated": False,
        "completed_at_utc": utc_now(),
    }
    atomic_json(TRAJECTORY_JSON, meta)
    return meta


def hardness_percentiles(scores):
    scores = np.asarray(scores, dtype=np.float64)
    if scores.ndim != 3 or scores.shape[0] != 10 or scores.shape[2] != 20:
        raise RuntimeError(f"Expected [10, positives, 20] teacher scores, got {scores.shape}")
    if not np.isfinite(scores).all():
        raise RuntimeError("Teacher trajectory contains non-finite scores")
    # Within each positive's frozen 20-candidate pool, 1.0 is the hardest negative.
    order = np.argsort(scores, axis=2, kind="stable")
    ranks = np.argsort(order, axis=2, kind="stable")
    return ranks.astype(np.float32) / 19.0


def build_selections():
    driver_hash = sha256_file(__file__)
    if not TRAJECTORY_NPZ.exists() or not TRAJECTORY_JSON.exists():
        raise RuntimeError("T1 teacher trajectory is missing")
    trajectory_meta = json.loads(TRAJECTORY_JSON.read_text(encoding="utf-8"))
    if (trajectory_meta.get("state") != "COMPLETE"
            or trajectory_meta.get("test_evaluated") is not False
            or trajectory_meta.get("driver_sha256") != driver_hash):
        raise RuntimeError("T1 teacher trajectory metadata does not match this Phase B driver")
    with np.load(TRAJECTORY_NPZ, allow_pickle=False) as archive:
        scores = archive["scores"].copy()
    v8, _full, view, pool, frozen_scores, pool_hash, _vp, _vn, valid_hash = import_context("cora")
    if pool_hash != trajectory_meta.get("train_pool_hash") or valid_hash != trajectory_meta.get("validation_candidate_hash"):
        raise RuntimeError("T1 trajectory context differs from the current frozen Cora context")
    if tuple(scores.shape) != (10, *pool.shape[:2]):
        raise RuntimeError(f"T1 trajectory shape/context mismatch: {scores.shape}")

    ranks = hardness_percentiles(scores)
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

    # Match final-teacher hardness within a predeclared 20%-wide percentile band.
    final_bins = np.minimum((ranks[-1] * 5).astype(np.int64), 4)
    target_bins = final_bins[rows, persistent_ids]
    rankmatched_ids = np.empty(len(pool), dtype=np.int64)
    for row, target_bin in enumerate(target_bins):
        eligible = np.flatnonzero(final_bins[row] == target_bin)
        alternatives = eligible[eligible != persistent_ids[row]]
        choices = alternatives if len(alternatives) else eligible
        rankmatched_ids[row] = choices[int(rng.integers(0, len(choices)))]

    selected = {
        "QTHS25": v8.selected_edges({"method": "QTHS25", "seed": 0, "alpha": None}, pool, frozen_scores, view.train_pos),
        "T1_PERSISTENT": pool[rows, persistent_ids].copy(),
        "T1_FINAL_SNAPSHOT": pool[rows, final_ids].copy(),
        "T1_MEAN_RANK": pool[rows, mean_ids].copy(),
        "T1_TRAJECTORY_SHUFFLED": pool[rows, shuffled_ids].copy(),
        "T1_FINAL_RANK_MATCHED": pool[rows, rankmatched_ids].copy(),
        "SH75": v8.selected_edges({"method": "SH75", "seed": 0, "alpha": None}, pool, frozen_scores, view.train_pos),
    }
    train_edges = {runner.canonical(edge) for edge in view.train_graph().edges()}
    for name, array in selected.items():
        if array.shape != (len(view.train_pos), 2):
            raise RuntimeError(f"{name} selection has an invalid shape: {array.shape}")
        if any(runner.canonical(edge) in train_edges for edge in array):
            raise RuntimeError(f"{name} selection contains a train/message edge")

    hashes = {name: v8.v61.array_hash(array) for name, array in selected.items()}
    np.savez_compressed(SELECTION_NPZ, **selected)
    SELECTION_DIR.mkdir(parents=True, exist_ok=True)
    for name, array in selected.items():
        np.save(SELECTION_DIR / f"{name}.npy", np.asarray(array, dtype=np.int64), allow_pickle=False)
    meta = {
        "state": "COMPLETE",
        "dataset": "cora",
        "selection_rule": "argmax_n min_t within-positive hardness_percentile(t,n), with hardest percentile 1",
        "trajectory_shuffle": "independently permute candidate ranks within each positive at every teacher epoch",
        "final_rank_match": "random candidate in the same 20%-wide final-rank bin as T1, excluding T1 where possible",
        "train_pool_hash": pool_hash,
        "validation_candidate_hash": valid_hash,
        "trajectory_sha256": trajectory_meta["trajectory_sha256"],
        "selected_negative_hashes": hashes,
        "selections_file_sha256": sha256_file(SELECTION_NPZ),
        "driver_sha256": driver_hash,
        "test_evaluated": False,
        "created_at_utc": utc_now(),
    }
    atomic_json(SELECTION_JSON, meta)
    return meta


def make_task(name, selection_name, selection_meta):
    selection_path = SELECTION_DIR / f"{selection_name}.npy"
    array = np.load(selection_path, allow_pickle=False)
    return {
        "job_id": f"V13-PHASEB-T1-STAGE1-{name}-s0",
        "candidate_id": f"V13_PHASEB_T1_STAGE1_{name}_s0",
        "arm": "BASELINE",
        "innovation": "T1 Persistent Hardness Selection",
        "family": "negative-hardness-trajectory",
        "definition": name,
        "purpose": "candidate" if name == "T1_PERSISTENT" else ("strong baseline" if name == "QTHS25_BASELINE" else "registered mechanism/control"),
        "stage": "phase1_phaseb_stage1",
        "dataset": "cora",
        "seed": 0,
        "epochs": 5,
        "sampler": selection_name,
        "negative_override_path": str(selection_path),
        "negative_override_hash": selection_meta["selected_negative_hashes"][selection_name],
        "priority": "P1",
        "status": "QUEUED",
        "stage1": True,
        "strong_baseline_identity": "Cora Raw-HG DCDLP + QTHS25 + BCE",
        "research_context": "Same frozen Cora split, train pool, validation candidates, backbone, loss, and five-epoch budget; only selected train negatives differ",
        "t1_trajectory_sha256": selection_meta["trajectory_sha256"],
        "t1_selection_file_sha256": selection_meta["selections_file_sha256"],
    }


def stage1_tasks(selection_meta):
    specs = [
        ("QTHS25_BASELINE", "QTHS25"),
        ("T1_PERSISTENT", "T1_PERSISTENT"),
        ("T1_FINAL_SNAPSHOT", "T1_FINAL_SNAPSHOT"),
        ("T1_MEAN_RANK", "T1_MEAN_RANK"),
        ("T1_TRAJECTORY_SHUFFLED", "T1_TRAJECTORY_SHUFFLED"),
        ("T1_FINAL_RANK_MATCHED", "T1_FINAL_RANK_MATCHED"),
        ("SH75_CONTROL", "SH75"),
    ]
    return [make_task(name, selection, selection_meta) for name, selection in specs]


def execute_task(task, driver_hash):
    task = dict(task)
    selected = np.load(task["negative_override_path"], allow_pickle=False)
    import experiment_v8 as v8
    observed = v8.v61.array_hash(selected)
    if observed != task["negative_override_hash"]:
        raise RuntimeError(f"Registered negative-selection hash mismatch for {task['job_id']}")
    result = runner.run_one(task)
    result.setdefault("source_hashes", {})[DRIVER_REL] = driver_hash
    result["phaseb_driver_sha256"] = driver_hash
    result["research_context"] = task["research_context"]
    result["test_evaluated"] = False
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    runner.atomic_json(folder / "result.json", result)
    return result


def summarize_stage1(rows):
    names = (
        "QTHS25_BASELINE",
        "T1_PERSISTENT",
        "T1_FINAL_SNAPSHOT",
        "T1_MEAN_RANK",
        "T1_TRAJECTORY_SHUFFLED",
        "T1_FINAL_RANK_MATCHED",
        "SH75_CONTROL",
    )
    by_name = {row.get("definition"): row for row in rows if row.get("state") == "COMPLETE"}
    if any(name not in by_name for name in names):
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False, "test_evaluated": False,
                "missing": [name for name in names if name not in by_name]}
    all_rows = [by_name[name] for name in names]
    for row in all_rows:
        if (int(row.get("epochs", -1)) != 5
                or int(row.get("train_record", {}).get("epoch_count", -1)) != 5
                or row.get("test_evaluated") is not False
                or row.get("phaseb_driver_sha256") != sha256_file(__file__)):
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False, "test_evaluated": False,
                    "invalid_job": row.get("job_id")}
    for key in ("split_hash", "train_pool_hash", "validation_candidate_hash"):
        if len({row.get(key) for row in all_rows}) != 1:
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False, "test_evaluated": False,
                    "context_mismatch": key}
    if len({int(row.get("trainable_parameters", -1)) for row in all_rows}) != 1:
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False, "test_evaluated": False,
                "context_mismatch": "trainable_parameters"}
    source_maps = {json.dumps(row.get("source_hashes", {}), sort_keys=True) for row in all_rows}
    if len(source_maps) != 1:
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False, "test_evaluated": False,
                "context_mismatch": "source_hashes"}

    def m(name):
        return float(by_name[name]["validation_metrics"]["mrr"])

    baseline = m("QTHS25_BASELINE")
    candidate = m("T1_PERSISTENT")
    shuffled = m("T1_TRAJECTORY_SHUFFLED")
    rankmatched = m("T1_FINAL_RANK_MATCHED")
    delta = candidate - baseline
    relative_delta = delta / baseline if baseline else float("-inf")
    stage1_gain = delta >= 0.003 or relative_delta >= 0.01
    mechanism = candidate > shuffled and candidate > rankmatched
    go = stage1_gain and mechanism
    return {
        "state": "STAGE1_GO" if go else "STAGE1_REJECT",
        "go": bool(go),
        "baseline_mrr": baseline,
        "candidate_mrr": candidate,
        "delta_vs_qths25": delta,
        "relative_delta_vs_qths25": relative_delta,
        "stage1_gain_gate": bool(stage1_gain),
        "trajectory_shuffled_mrr": shuffled,
        "final_rank_matched_mrr": rankmatched,
        "mechanism_controls_pass": bool(mechanism),
        "control_margins": {
            "vs_trajectory_shuffled": candidate - shuffled,
            "vs_final_rank_matched": candidate - rankmatched,
            "vs_final_snapshot": candidate - m("T1_FINAL_SNAPSHOT"),
            "vs_mean_rank": candidate - m("T1_MEAN_RANK"),
            "vs_sh75": candidate - m("SH75_CONTROL"),
        },
        "all_mrr": {name: m(name) for name in names},
        "parameters": int(by_name["QTHS25_BASELINE"]["trainable_parameters"]),
        "test_evaluated": False,
    }


def run_stage1(workers, selection_meta):
    assert_phaseb_eligible()
    driver_hash = sha256_file(__file__)
    tasks = stage1_tasks(selection_meta)
    import experiment_v8 as v8

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
            and prior.get("source_hashes", {}).get(DRIVER_REL) == driver_hash
            and prior.get("selected_negative_hash") == task["negative_override_hash"]
            and prior.get("test_evaluated") is False
        )
        if valid:
            results.append(prior)
        else:
            pending.append(task)

    atomic_json(STATUS_JSON, {
        "state": "STAGE1_RUNNING",
        "stage": "phase1_phaseb_t1_stage1",
        "completed": len(results),
        "total": len(tasks),
        "workers": min(workers, len(pending)),
        "failed": [],
        "test_evaluated": False,
        "driver_sha256": driver_hash,
        "updated_at_utc": utc_now(),
    })
    if pending:
        with cf.ProcessPoolExecutor(
            max_workers=min(workers, len(pending)),
            mp_context=mp.get_context("spawn"),
            initializer=runner.worker_init,
        ) as executor:
            futures = {executor.submit(execute_task, task, driver_hash): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    row = future.result()
                except Exception as exc:
                    row = {
                        **task,
                        "state": "FAILED",
                        "error": repr(exc),
                        "test_evaluated": False,
                        "completed_at_utc": utc_now(),
                    }
                results.append(row)
                decision = summarize_stage1(results)
                atomic_json(RESULTS_JSON, {
                    "stage": "phase1_phaseb_t1_stage1",
                    "results": results,
                    "decision": decision,
                    "test_evaluated": False,
                    "driver_sha256": driver_hash,
                })
                atomic_json(STATUS_JSON, {
                    "state": "STAGE1_RUNNING",
                    "stage": "phase1_phaseb_t1_stage1",
                    "completed": sum(row.get("state") == "COMPLETE" for row in results),
                    "total": len(tasks),
                    "workers": min(workers, len(pending)),
                    "failed": [row.get("job_id") for row in results if row.get("state") != "COMPLETE"],
                    "test_evaluated": False,
                    "driver_sha256": driver_hash,
                    "updated_at_utc": utc_now(),
                })

    decision = summarize_stage1(results)
    atomic_json(RESULTS_JSON, {
        "stage": "phase1_phaseb_t1_stage1",
        "results": sorted(results, key=lambda row: row.get("job_id", "")),
        "decision": decision,
        "test_evaluated": False,
        "driver_sha256": driver_hash,
        "completed_at_utc": utc_now(),
    })
    atomic_json(STATUS_JSON, {
        "state": decision["state"],
        "stage": "phase1_phaseb_t1_stage1",
        "completed": sum(row.get("state") == "COMPLETE" for row in results),
        "total": len(tasks),
        "decision": decision,
        "test_evaluated": False,
        "driver_sha256": driver_hash,
        "updated_at_utc": utc_now(),
    })
    return {"decision": decision, "results": results}


def run_all(workers):
    assert_phaseb_eligible()
    atomic_json(STATUS_JSON, {
        "state": "TEACHER_RUNNING",
        "stage": "phase1_phaseb_t1_teacher",
        "completed": 0,
        "total": 1,
        "workers": 1,
        "test_evaluated": False,
        "driver_sha256": sha256_file(__file__),
        "started_at_utc": utc_now(),
    })
    teacher = capture_teacher_trajectory()
    atomic_json(STATUS_JSON, {
        "state": "TEACHER_COMPLETE",
        "stage": "phase1_phaseb_t1_teacher",
        "completed": 1,
        "total": 1,
        "workers": 0,
        "test_evaluated": False,
        "teacher_trajectory_sha256": teacher["trajectory_sha256"],
        "driver_sha256": sha256_file(__file__),
        "updated_at_utc": utc_now(),
    })
    selections = build_selections()
    return run_stage1(workers, selections)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        raise SystemExit("workers must be between 1 and 8")
    try:
        result = run_all(args.workers)
        print(json.dumps({
            "status": json.loads(STATUS_JSON.read_text(encoding="utf-8")),
            "decision": result["decision"],
        }, indent=2, ensure_ascii=False), flush=True)
    except Exception as exc:
        atomic_json(STATUS_JSON, {
            "state": "INFRASTRUCTURE_FAILURE",
            "stage": "phase1_phaseb_t1",
            "error": repr(exc),
            "test_evaluated": False,
            "driver_sha256": sha256_file(__file__),
            "updated_at_utc": utc_now(),
        })
        print(f"Phase B T1 failed: {exc}", file=sys.stderr, flush=True)
        raise


if __name__ == "__main__":
    main()

