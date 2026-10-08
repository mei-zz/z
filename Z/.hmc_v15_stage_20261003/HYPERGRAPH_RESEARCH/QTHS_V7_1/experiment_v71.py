"""V7.1 locked QTHS reproduction and gated AQTHS experiment.

The existing V6.1/V6.2 training harness is reused without modifying its files.
All selector inputs are train-only arrays; held-out candidates are evaluation-only.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V7_1"
V61 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
V6 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6"
V62 = ROOT / "HYPERGRAPH_RESEARCH" / "CODNS_V6_2"
V7 = ROOT / "HYPERGRAPH_RESEARCH" / "HARDNESS_V7"
sys.path[:0] = [str(ROOT / "src"), str(V61), str(V62), str(V7)]

import run_negative_v6_1 as v61  # noqa: E402
import run_codns_v6_2 as engine  # noqa: E402
import train_hardness_v7 as v7  # noqa: E402

SEEDS = (0, 1, 2)
EPOCHS = 10
QTHS_ALPHA = 0.25
POOL_PER_POSITIVE = 20
TRAIN_POOL_SEED = 20261002
TRAIN_GROUP_SEED = 20261003
VALID_POOL_SEED = 72200
TEST_POOL_SEED = 999


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def split_hash(view) -> str:
    return hashlib.sha256(
        (v61.array_hash(view.train_pos) + v61.array_hash(view.features) + str(view.num_nodes)).encode("ascii")
    ).hexdigest()


def status(phase: str, current: str | None = None, **extra) -> None:
    old = read_json(OUT / "status.json") if (OUT / "status.json").exists() else {}
    state = "COMPLETE" if phase == "complete" else "RUNNING"
    if state != "FAILED":
        old.pop("error", None)
    old.update({"state": state, "phase": phase, "current": current,
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
    old.update(extra)
    write_json(OUT / "status.json", old)


def runtime_record() -> dict:
    import torch
    import torch_geometric

    return {
        "python": sys.version.split()[0],
        "torch": str(torch.__version__),
        "torch_cuda_build": str(torch.version.cuda),
        "cuda_available": bool(torch.cuda.is_available()),
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "pyg": str(torch_geometric.__version__),
        "numpy": str(np.__version__),
        "protocol": "STRICT_TRAIN_ONLY",
        "checkpoint_rule": "FIXED_EPOCH_10",
    }


def ensure_expected_runtime() -> dict:
    import torch

    info = runtime_record()
    if not torch.cuda.is_available() or "V100" not in str(info["gpu"]):
        raise RuntimeError(f"CUDA V100 preflight failed: {info}")
    if info["pyg"] != "2.5.3":
        raise RuntimeError(f"Locked environment preflight expected PyG 2.5.3: {info}")
    if str(torch.__version__).startswith("2.3.1") and str(torch.version.cuda) == "12.1":
        info["environment_route"] = "LOCKED_TORCH_2_3_1_CUDA_12_1"
        info["environment_repro_blocked"] = False
        return info
    if os.environ.get("QTHS_ENV_REPRO_BLOCKED") == "1" and str(torch.__version__).startswith("2.8.0") and str(torch.version.cuda) == "12.8":
        info["environment_route"] = "ACTIVE_TORCH_2_8_FALLBACK"
        info["environment_repro_blocked"] = True
        info["environment_block_reason"] = os.environ.get("QTHS_ENV_BLOCK_REASON", "Torch 2.3.1+cu121 CUDA smoke test failed")
        return info
    raise RuntimeError(f"Locked environment preflight expected torch 2.3.1/cu121; fallback needs explicit block marker: {info}")


def init_dataset(name: str):
    import torch
    from torch_geometric.data.data import Data
    from dcdlp.data.loaders import load_dataset

    # Required for PyG processed caches under modern torch weights-only loading.
    if hasattr(torch.serialization, "add_safe_globals"):
        torch.serialization.add_safe_globals([Data])
    full = load_dataset(name, ROOT / "data", "standard", 0)
    return full, v61.TrainOnlyView(full)


def make_eval_candidates(full, split: str) -> tuple[np.ndarray, np.ndarray, str]:
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling

    positives = np.asarray(getattr(full, f"{split}_pos"), dtype=np.int64).copy()
    if split == "valid" and full.name.lower() == "cora":
        cache = V6 / "fixed_validation_candidates.npz"
        meta_path = V6 / "fixed_validation_candidates.json"
        with np.load(cache, allow_pickle=False) as z:
            cached_pos = z["valid_positive"].copy()
            negatives = z["valid_negative_candidates"].copy()
        expected = read_json(meta_path)["negative_candidates_hash"]
        if not np.array_equal(positives, cached_pos):
            raise RuntimeError("Cora locked validation positives differ from the frozen V6 candidates")
        digest = v61.array_hash(negatives)
        if digest != expected or negatives.shape != (len(positives), 20, 2):
            raise RuntimeError("Cora fixed validation candidate cache failed its V6 hash/shape audit")
        return positives, negatives, digest

    seed = VALID_POOL_SEED if split == "valid" else TEST_POOL_SEED
    pool = uniform_negative_sampling(
        full.num_nodes, full.all_positive, max(20 * len(positives), 20), seed,
    )
    negatives = grouped_negatives(positives, pool, 20, seed + 1)
    if negatives.shape != (len(positives), 20, 2):
        raise RuntimeError(f"Unexpected {split} candidate shape for {full.name}: {negatives.shape}")
    return positives, negatives, v61.array_hash(negatives)


def training_pool(view) -> tuple[np.ndarray, str]:
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling

    forbidden_rows, forbidden = v61.make_train_forbidden(view)
    raw = uniform_negative_sampling(
        view.num_nodes, forbidden_rows, len(view.train_pos) * POOL_PER_POSITIVE, TRAIN_POOL_SEED,
    )
    pool = grouped_negatives(view.train_pos, raw, POOL_PER_POSITIVE, TRAIN_GROUP_SEED)
    if pool.shape != (len(view.train_pos), POOL_PER_POSITIVE, 2):
        raise RuntimeError(f"Unexpected train pool shape for {view.name}: {pool.shape}")
    if any(v61.canonical_edge(pair) in forbidden for pair in pool.reshape(-1, 2)):
        raise RuntimeError(f"{view.name} train-only pool contains a train/message edge")
    return pool, v61.array_hash(pool)


def run_model(dataset: str, view, method: str, seed: int, selected: np.ndarray | None,
              pool: np.ndarray, pool_hash: str, valid_pos: np.ndarray,
              valid_neg: np.ndarray, valid_hash: str,
              hypergraph_mode: str = "raw") -> dict:
    engine.candidate_pool = pool
    engine.candidate_pool_hash = pool_hash
    engine.validation_candidate_hash = valid_hash
    out_dir = OUT / "RUNS" / dataset.upper() / method / f"seed{seed}"
    rel = str(out_dir.relative_to(ROOT)).replace("\\", "/")
    status(f"{dataset.lower()}_training", f"{method}_seed{seed}",
           train_pool_hash=pool_hash, validation_candidate_hash=valid_hash)
    rec = engine.train_one(
        view, f"{dataset}_{method}", seed, selected, rel, valid_pos, valid_neg,
        initialize_from_v6=False, dataset_name=dataset.lower(), hypergraph_mode=hypergraph_mode,
    )
    metric = engine.eval_fixed_candidates(rec["checkpoint"], view, valid_pos, valid_neg)
    if not np.isclose(float(metric["mrr"]), float(rec["epoch10_validation_mrr"]), rtol=0, atol=1e-10):
        raise RuntimeError(f"{dataset}/{method}/seed{seed}: fixed-candidate validation differs from epoch-10 trace")
    checkpoint_path = safe_path(rec["checkpoint"])
    return {
        **rec,
        "checkpoint": str(checkpoint_path),
        "checkpoint_file_sha256": file_hash(checkpoint_path),
        "validation_metrics": metric,
        "validation_candidate_hash": valid_hash,
        "train_pool_hash": pool_hash,
        "split_hash": split_hash(view),
    }


def summarize(records: dict, methods: tuple[str, ...], seeds=SEEDS) -> dict:
    metrics = ("mrr", "hits10", "mean_positive_rank")
    def metric_values(record: dict) -> dict:
        return record.get("validation_metrics", record)

    summary = {}
    for method in methods:
        per_seed = {}
        for seed in seeds:
            rec = records[method][str(seed)]
            values = rec.get("validation_metrics", rec)
            per_seed[str(seed)] = {key: float(values[key]) for key in metrics if key in values}
        summary[method] = {"by_seed": per_seed}
        for key in metrics:
            vals = [per_seed[str(seed)][key] for seed in seeds if key in per_seed[str(seed)]]
            if len(vals) == len(seeds):
                summary[method][f"mean_{key}"] = float(np.mean(vals))
                summary[method][f"sample_std_{key}"] = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    paired = {}
    if methods:
        baseline = methods[0]
        for method in methods[1:]:
            deltas = [
                float(metric_values(records[method][str(seed)])["mrr"] -
                      metric_values(records[baseline][str(seed)])["mrr"])
                for seed in seeds if str(seed) in records.get(method, {}) and str(seed) in records.get(baseline, {})
            ]
            paired[f"{method}_minus_{baseline}"] = {
                "by_seed": deltas,
                "mean": float(np.mean(deltas)) if deltas else None,
                "sample_std": float(np.std(deltas, ddof=1)) if len(deltas) > 1 else (0.0 if deltas else None),
            }
    return {"methods": summary, "paired_mrr_deltas_vs_first_method": paired}


def write_cora_report(result: dict) -> None:
    block = result["cora"]
    val = block.get("validation", {})
    test = block.get("test", {})
    lines = [
        "# Cora locked reproduction — V7.1", "",
        "Frozen protocol: STRICT_TRAIN_ONLY, 20 train candidates per positive, one selected negative per train positive per epoch, fixed epoch 10, QTHS25 alpha=0.25. All arms share one runtime, split, train pool and evaluation candidate arrays.", "",
        f"- Runtime: {json.dumps(result.get('environment', {}), ensure_ascii=False)}",
        f"- Split hash: `{block.get('split_hash')}`; train-pool hash: `{block.get('train_pool_hash')}`; validation candidates: `{block.get('validation_candidate_hash')}`.",
        f"- Frozen Graph-teacher state hash: `{block.get('teacher_state_hash')}`; cached Graph-teacher score hash: `{block.get('teacher_scores_hash')}`.", "",
        "## Validation MRR", "", "| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |", "|---|---:|---:|---:|---:|---:|",
    ]
    for method, row in val.get("summary", {}).get("methods", {}).items():
        values = [row["by_seed"][str(s)]["mrr"] for s in SEEDS]
        lines.append(f"| {method} | " + " | ".join(f"{x:.6f}" for x in values) + f" | {row['mean_mrr']:.6f} | {row['sample_std_mrr']:.6f} |")
    lines += ["", "## Test MRR (opened once after validation freeze)", "", "| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |", "|---|---:|---:|---:|---:|---:|"]
    for method, row in test.get("summary", {}).get("methods", {}).items():
        values = [row["by_seed"][str(s)]["mrr"] for s in SEEDS]
        lines.append(f"| {method} | " + " | ".join(f"{x:.6f}" for x in values) + f" | {row['mean_mrr']:.6f} | {row['sample_std_mrr']:.6f} |")
    lines += ["", f"- Locked reproduction: **{block.get('locked_reproduction_status', 'PENDING')}**.",
              f"- Test candidate hash: `{test.get('candidate_hash', 'not opened')}`.",
              f"- Paired test deltas: `{json.dumps(test.get('paired_mrr_deltas', {}), ensure_ascii=False)}`.", ""]
    (OUT / "01_CORA_FULL_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")


def cora_locked_reproduction(result: dict) -> bool:
    block = result["cora"]
    methods = ("C0_UNIFORM", "C1_GRAPH_HARD", "C2_RANDOM_VETO", "C3_QTHS25")
    validation = block.get("validation", {}).get("summary", {}).get("methods", {})
    test = block.get("test", {}).get("summary", {}).get("methods", {})
    if not all(m in validation and m in test for m in methods):
        return False
    qths = [test["C3_QTHS25"]["by_seed"][str(s)]["mrr"] for s in SEEDS]
    graph = [test["C1_GRAPH_HARD"]["by_seed"][str(s)]["mrr"] for s in SEEDS]
    random_veto = [test["C2_RANDOM_VETO"]["by_seed"][str(s)]["mrr"] for s in SEEDS]
    return bool(np.mean(qths) > np.mean(graph) and sum(a > b for a, b in zip(qths, graph)) >= 2
                and np.mean(qths) >= np.mean(random_veto))


def run_cora(result: dict) -> bool:
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling

    full, view = init_dataset("cora")
    archive_path = V61 / "strict_train_candidates_and_selections.npz"
    with np.load(archive_path, allow_pickle=False) as z:
        pool_data = {key: z[key].copy() for key in z.files}
    pool = pool_data["negative_candidates"]
    scores = pool_data["score_graph"]
    if not np.array_equal(view.train_pos, pool_data["train_positive"]):
        raise RuntimeError("Regenerated Cora training split differs from the frozen V6.1 train positives")
    if pool.shape != (len(view.train_pos), 20, 2) or v61.array_hash(pool) != read_json(V61 / "strict_pool_metadata.json")["candidate_pool_hash"]:
        raise RuntimeError("Cora frozen train-only candidate-pool hash/shape audit failed")
    meta = read_json(V61 / "strict_pool_metadata.json")
    valid_pos, valid_neg, valid_hash = make_eval_candidates(full, "valid")
    expected_val_hash = read_json(V6 / "fixed_validation_candidates.json")["negative_candidates_hash"]
    if valid_hash != expected_val_hash:
        raise RuntimeError("Cora validation candidate hash differs from the locked V6 cache")
    qths_idx, qths_meta = v7.make_ids(pool, scores, view.train_pos, QTHS_ALPHA)
    if "a4_indices" in pool_data and not np.array_equal(pool_data["a4_indices"], qths_idx):
        # V6.1 A4 is a hypergraph-veto selector, not QTHS; record the distinction explicitly.
        qths_meta["distinct_from_v61_a4_hypergraph_veto_indices"] = True
    rows = np.arange(len(view.train_pos))
    graph_hard = pool[np.arange(len(rows)), np.argmax(scores, axis=1)].copy()
    qths = pool[np.arange(len(rows)), qths_idx].copy()
    selections = {
        "C0_UNIFORM": None,
        "C1_GRAPH_HARD": graph_hard,
        "C2_RANDOM_VETO": None,
        "C3_QTHS25": qths,
    }
    block = result.setdefault("cora", {})
    block.update({
        "state": "RUNNING",
        "train_pool_hash": v61.array_hash(pool),
        "split_hash": split_hash(view),
        "validation_candidate_hash": valid_hash,
        "train_positive_hash": v61.array_hash(view.train_pos),
        "teacher_scores_hash": v61.array_hash(scores),
        "teacher_state_hash": read_json(V7 / "results.json").get("teacher_hashes", {}).get("Graph"),
        "teacher_cache_metadata": meta.get("teacher_records", {}).get("Graph", {}),
        "qths_selection": qths_meta,
        "validation": {"runs": {}},
        "locked_protocol": "STRICT_TRAIN_ONLY",
        "epoch_count": EPOCHS,
        "test_evaluated": False,
    })
    save_results(result)
    for method in ("C0_UNIFORM", "C1_GRAPH_HARD", "C2_RANDOM_VETO", "C3_QTHS25"):
        for seed in SEEDS:
            if method == "C2_RANDOM_VETO":
                selected = pool_data[f"S_A3_seed{seed}"].copy()
            else:
                selected = selections[method]
            rec = run_model("cora", view, method, seed, selected, pool, block["train_pool_hash"],
                            valid_pos, valid_neg, valid_hash, hypergraph_mode="raw")
            block["validation"]["runs"].setdefault(method, {})[str(seed)] = rec
            block["validation"]["summary"] = summarize(block["validation"]["runs"],
                                                           tuple(m for m in ("C0_UNIFORM", "C1_GRAPH_HARD", "C2_RANDOM_VETO", "C3_QTHS25")
                                                                 if m in block["validation"]["runs"] and len(block["validation"]["runs"][m]) == 3))
            save_results(result)
    block["validation"]["summary"] = summarize(block["validation"]["runs"],
                                                   ("C0_UNIFORM", "C1_GRAPH_HARD", "C2_RANDOM_VETO", "C3_QTHS25"))
    block["validation"]["state"] = "COMPLETE"
    save_results(result)

    # The validation rule is registered before a shared test candidate set is created.
    test_gate_open = all(len(block["validation"]["runs"][m]) == 3 for m in selections)
    if not test_gate_open:
        raise RuntimeError("Cora validation suite is incomplete; test gate remains closed")
    test_pos = np.asarray(full.test_pos, dtype=np.int64).copy()
    test_pool = uniform_negative_sampling(
        full.num_nodes, full.all_positive, 20 * len(test_pos), TEST_POOL_SEED,
    )
    test_neg = grouped_negatives(test_pos, test_pool, 20, TEST_POOL_SEED + 1)
    test_hash = v61.array_hash(test_neg)
    expected_test_hash = read_json(V6 / "results.json")["test_results"]["shared_candidate_hash"]
    if test_hash != expected_test_hash:
        raise RuntimeError(f"Cora one-time test candidate hash mismatch: {test_hash} != {expected_test_hash}")
    eval_path = OUT / "EVALUATION" / "cora_test_candidates.npz"
    eval_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(eval_path, test_positive=test_pos, test_negative_candidates=test_neg)
    previous_test = block.get("test", {})
    if previous_test.get("candidate_hash") == test_hash:
        test_result = previous_test
        test_result["state"] = "RUNNING"
        test_result.setdefault("by_method_seed", {})
    else:
        test_result = {"state": "RUNNING", "candidate_hash": test_hash, "test_positive_hash": v61.array_hash(test_pos),
                       "positive_count": int(len(test_pos)), "negative_count_per_positive": 20,
                       "created_after_validation_freeze": True, "test_evaluated_once": True,
                       "by_method_seed": {}}
    block["test"] = test_result
    block["test_evaluated"] = True
    save_results(result)
    for method in selections:
        for seed in SEEDS:
            if str(seed) in test_result["by_method_seed"].get(method, {}):
                continue
            run = block["validation"]["runs"][method][str(seed)]
            metric = engine.eval_fixed_candidates(run["checkpoint"], view, test_pos, test_neg)
            test_result["by_method_seed"].setdefault(method, {})[str(seed)] = {
                **metric, "checkpoint": run["checkpoint"], "checkpoint_file_sha256": run["checkpoint_file_sha256"],
                "candidate_hash": test_hash,
            }
            save_results(result)
    test_result["summary"] = summarize(test_result["by_method_seed"], tuple(selections))
    test_result["paired_mrr_deltas"] = {
        f"{method}_minus_{baseline}_by_seed": [
            float(test_result["by_method_seed"][method][str(seed)]["mrr"] -
                  test_result["by_method_seed"][baseline][str(seed)]["mrr"])
            for seed in SEEDS
        ]
        for baseline in ("C1_GRAPH_HARD", "C2_RANDOM_VETO")
        for method in ("C3_QTHS25",)
    }
    test_result["paired_mrr_deltas"].update({
        f"{method}_minus_C0_UNIFORM_by_seed": [
            float(test_result["by_method_seed"][method][str(seed)]["mrr"] -
                  test_result["by_method_seed"]["C0_UNIFORM"][str(seed)]["mrr"])
            for seed in SEEDS
        ] for method in ("C1_GRAPH_HARD", "C2_RANDOM_VETO", "C3_QTHS25")
    })
    test_result["paired_mrr_delta_summary"] = {
        key: {"mean": float(np.mean(values)), "sample_std": float(np.std(values, ddof=1)),
              "by_seed": values}
        for key, values in test_result["paired_mrr_deltas"].items()
    }
    test_result["state"] = "COMPLETE"
    qths_mrr = [test_result["by_method_seed"]["C3_QTHS25"][str(s)]["mrr"] for s in SEEDS]
    graph_mrr = [test_result["by_method_seed"]["C1_GRAPH_HARD"][str(s)]["mrr"] for s in SEEDS]
    veto_mrr = [test_result["by_method_seed"]["C2_RANDOM_VETO"][str(s)]["mrr"] for s in SEEDS]
    test_result["locked_gate_details"] = {
        "QTHS25_mean_mrr": float(np.mean(qths_mrr)),
        "Graph_hard_mean_mrr": float(np.mean(graph_mrr)),
        "Random_veto_mean_mrr": float(np.mean(veto_mrr)),
        "QTHS25_wins_vs_graph_hard": int(sum(a > b for a, b in zip(qths_mrr, graph_mrr))),
        "QTHS25_wins_vs_random_veto": int(sum(a > b for a, b in zip(qths_mrr, veto_mrr))),
        "QTHS25_beats_graph_hard_mean": bool(np.mean(qths_mrr) > np.mean(graph_mrr)),
        "QTHS25_beats_random_veto_mean_or_ties": bool(np.mean(qths_mrr) >= np.mean(veto_mrr)),
    }
    block["locked_reproduction_status"] = "PASS" if cora_locked_reproduction(result) else "FAIL"
    block["state"] = "LOCKED_REPRODUCTION_COMPLETE"
    save_results(result)
    write_cora_report(result)
    status("cora_locked_reproduction_complete", None, decision=block["locked_reproduction_status"],
           test_candidate_hash=test_hash, test_evaluated=True)
    return block["locked_reproduction_status"] == "PASS"


def preflight_audit() -> dict:
    full, view = init_dataset("cora")
    with np.load(V61 / "strict_train_candidates_and_selections.npz", allow_pickle=False) as z:
        pool = z["negative_candidates"].copy()
        train_pos = z["train_positive"].copy()
        scores = z["score_graph"].copy()
    metadata = read_json(V61 / "strict_pool_metadata.json")
    valid_pos, valid_neg, valid_hash = make_eval_candidates(full, "valid")
    forbidden_rows, forbidden = v61.make_train_forbidden(view)
    if not np.array_equal(view.train_pos, train_pos):
        raise RuntimeError("Preflight Cora train split differs from V6.1 frozen split")
    if v61.array_hash(pool) != metadata["candidate_pool_hash"]:
        raise RuntimeError("Preflight Cora candidate pool differs from frozen V6.1 hash")
    if v61.array_hash(valid_neg) != read_json(V6 / "fixed_validation_candidates.json")["negative_candidates_hash"]:
        raise RuntimeError("Preflight Cora validation candidates differ from fixed V6 candidates")
    if any(v61.canonical_edge(pair) in forbidden for pair in pool.reshape(-1, 2)):
        raise RuntimeError("Preflight train-only candidate pool includes a train/message edge")
    if scores.shape != pool.shape[:2] or len(valid_pos) != len(full.valid_pos):
        raise RuntimeError("Preflight teacher/evaluation array shape mismatch")
    required = [V61 / "strict_train_candidates_and_selections.npz",
                V61 / "strict_pool_metadata.json", V6 / "fixed_validation_candidates.npz",
                V6 / "fixed_validation_candidates.json", V6 / "results.json",
                v61.BASELINE / "H" / "config.json"]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Preflight required files missing: " + ", ".join(missing))
    return {
        "state": "PASS", "runtime": runtime_record(),
        "split_hash": split_hash(view), "train_positive_hash": v61.array_hash(view.train_pos),
        "train_pool_hash": v61.array_hash(pool), "validation_candidate_hash": valid_hash,
        "teacher_scores_hash": v61.array_hash(scores), "train_positive_count": int(len(view.train_pos)),
        "validation_positive_count": int(len(valid_pos)), "validation_candidates_shape": list(valid_neg.shape),
        "training_forbidden_count": int(len(forbidden_rows)), "train_pool_uses_train_only_filter": True,
        "test_candidates_created": False, "test_metrics_evaluated": False,
    }


def save_results(result: dict) -> None:
    write_json(OUT / "results.json", result)


def random_veto(pool: np.ndarray, scores: np.ndarray, seed: int) -> np.ndarray:
    order = np.argsort(-scores, axis=1, kind="stable")[:, :2]
    rng = np.random.default_rng(400_000 + int(seed) * 10_000 + 7_710)
    veto = rng.integers(0, 2, size=len(pool))
    return pool[np.arange(len(pool)), order[np.arange(len(pool)), 1 - veto]].copy()


def graph_teacher(dataset: str, full, view, pool: np.ndarray, pool_hash: str,
                  valid_pos: np.ndarray, valid_neg: np.ndarray, valid_hash: str) -> tuple[np.ndarray, dict]:
    import torch
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs

    # Dataset-specific teachers are trained only on the training view with uniform train-pool draws.
    rec = run_model(dataset, view, "GRAPH_TEACHER", 0, None, pool, pool_hash,
                    valid_pos, valid_neg, valid_hash, hypergraph_mode="disabled")
    model, _ = load_checkpoint_model(rec["checkpoint"], device="cuda")
    x = torch.as_tensor(view.features, dtype=torch.float32, device="cuda")
    edge_index = edge_index_from_graph(view.train_graph(), torch.device("cuda"))
    with torch.no_grad():
        output = score_pairs(model, x, edge_index, pool.reshape(-1, 2), batch_size=8192)
        scores = np.asarray(output["logit"], dtype=np.float32).reshape(len(pool), pool.shape[1])
    del model
    torch.cuda.empty_cache()
    record = {
        "checkpoint": rec["checkpoint"],
        "checkpoint_file_sha256": rec["checkpoint_file_sha256"],
        "model_state_hash": rec["model_state_hash"],
        "train_pool_hash": pool_hash,
        "scores_hash": v61.array_hash(scores),
        "validation_candidate_hash": valid_hash,
        "split_hash": split_hash(view),
        "trained_with_uniform_train_pool": True,
        "heldout_positive_identities_passed_to_teacher_or_sampler": False,
    }
    cache = OUT / "TEACHERS" / dataset.lower()
    cache.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache / "graph_teacher_scores.npz", scores=scores, candidates=pool)
    write_json(cache / "graph_teacher.json", record)
    return scores, record


def report_dataset(name: str, block: dict) -> None:
    lines = [
        f"# {name} V7.1 results", "",
        f"- Split hash: `{block.get('split_hash')}`; train pool hash: `{block.get('train_pool_hash')}`; validation candidate hash: `{block.get('validation_candidate_hash')}`; test candidate hash: `{block.get('test_candidate_hash')}`.",
        f"- Runtime: `{block.get('runtime')}`; fixed epoch: 10; evaluation candidates shared across all methods.", "",
    ]
    for phase in ("validation", "test"):
        summary = block.get(phase, {}).get("summary", {}).get("methods", {})
        if not summary:
            continue
        available_seeds = sorted({int(seed) for row in summary.values()
                                  for seed in row.get("by_seed", {})})
        seed_headers = " | ".join(f"Seed {seed}" for seed in available_seeds)
        separator = " | ".join(["---:"] * (len(available_seeds) + 2))
        lines += [f"## {phase.title()} MRR", "", f"| Method | {seed_headers} | Mean | Sample SD |",
                  f"|---|{separator}|"]
        for method, row in summary.items():
            vals = [row.get("by_seed", {}).get(str(seed), {}).get("mrr") for seed in available_seeds]
            rendered = [f"{x:.6f}" if x is not None else "—" for x in vals]
            lines.append(f"| {method} | " + " | ".join(rendered) +
                         f" | {row['mean_mrr']:.6f} | {row['sample_std_mrr']:.6f} |")
        lines.append("")
    lines.append(f"- Transfer assessment: `{block.get('transfer_assessment', 'PENDING')}`.")
    target = "02_CITESEER_FULL_RESULTS.md" if name.lower() == "citeseer" else "03_PUBMED_SCREEN.md"
    (OUT / target).write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_citeseer(result: dict) -> dict:
    full, view = init_dataset("citeseer")
    valid_pos, valid_neg, valid_hash = make_eval_candidates(full, "valid")
    pool, pool_hash = training_pool(view)
    scores, teacher = graph_teacher("citeseer", full, view, pool, pool_hash,
                                    valid_pos, valid_neg, valid_hash)
    qths_idx, qths_meta = v7.make_ids(pool, scores, view.train_pos, QTHS_ALPHA)
    graph_hard = pool[np.arange(len(pool)), np.argmax(scores, axis=1)].copy()
    qths = pool[np.arange(len(pool)), qths_idx].copy()
    previous_test = result.get("citeseer", {}).get("test", {})
    block = {
        "state": "RUNNING", "dataset": "citeseer", "runtime": result["environment"]["torch"],
        "split_hash": split_hash(view), "train_pool_hash": pool_hash,
        "train_positive_hash": v61.array_hash(view.train_pos),
        "validation_candidate_hash": valid_hash, "teacher": teacher,
        "qths_rule": qths_meta, "validation": {"runs": {}},
        "test_evaluated": False, "test_candidate_hash": None,
    }
    if previous_test:
        block["test"] = previous_test
    result["citeseer"] = block
    save_results(result)
    methods = ("C1_GRAPH_HARD", "C2_RANDOM_VETO", "C3_QTHS25")
    for method in methods:
        for seed in SEEDS:
            selected = graph_hard if method == "C1_GRAPH_HARD" else (
                random_veto(pool, scores, seed) if method == "C2_RANDOM_VETO" else qths
            )
            rec = run_model("citeseer", view, method, seed, selected, pool, pool_hash,
                            valid_pos, valid_neg, valid_hash, hypergraph_mode="raw")
            block["validation"]["runs"].setdefault(method, {})[str(seed)] = rec
            save_results(result)
    block["validation"]["summary"] = summarize(block["validation"]["runs"], methods)
    block["validation"]["state"] = "COMPLETE"

    # Test candidates are materialized only after every validation checkpoint is frozen.
    test_pos, test_neg, test_hash = make_eval_candidates(full, "test")
    eval_path = OUT / "EVALUATION" / "citeseer_test_candidates.npz"
    eval_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(eval_path, test_positive=test_pos, test_negative_candidates=test_neg)
    if previous_test.get("candidate_hash") == test_hash:
        test_block = previous_test
        test_block["state"] = "RUNNING"
        test_block.setdefault("by_method_seed", {})
    else:
        test_block = {"state": "RUNNING", "candidate_hash": test_hash,
                      "test_positive_hash": v61.array_hash(test_pos), "positive_count": int(len(test_pos)),
                      "negative_count_per_positive": 20, "created_after_validation_freeze": True,
                      "test_evaluated_once": True, "by_method_seed": {}}
    block["test"] = test_block
    block["test_candidate_hash"] = test_hash
    block["test_evaluated"] = True
    save_results(result)
    for method in methods:
        for seed in SEEDS:
            if str(seed) in test_block["by_method_seed"].get(method, {}):
                continue
            rec = block["validation"]["runs"][method][str(seed)]
            metric = engine.eval_fixed_candidates(rec["checkpoint"], view, test_pos, test_neg)
            test_block["by_method_seed"].setdefault(method, {})[str(seed)] = {
                **metric, "checkpoint": rec["checkpoint"],
                "checkpoint_file_sha256": rec["checkpoint_file_sha256"], "candidate_hash": test_hash,
            }
            save_results(result)
    test_block["summary"] = summarize(test_block["by_method_seed"], methods)
    test_block["paired_mrr_deltas"] = {
        f"C3_QTHS25_minus_{baseline}_by_seed": [
            float(test_block["by_method_seed"]["C3_QTHS25"][str(seed)]["mrr"] -
                  test_block["by_method_seed"][baseline][str(seed)]["mrr"])
            for seed in SEEDS
        ] for baseline in ("C1_GRAPH_HARD", "C2_RANDOM_VETO")
    }
    test_block["paired_mrr_delta_summary"] = {
        key: {"mean": float(np.mean(values)), "sample_std": float(np.std(values, ddof=1)),
              "by_seed": values}
        for key, values in test_block["paired_mrr_deltas"].items()
    }
    test_block["state"] = "COMPLETE"
    val_mean = block["validation"]["summary"]["methods"]
    test_mean = test_block["summary"]["methods"]
    val_wins = sum(val_mean["C3_QTHS25"]["by_seed"][str(s)]["mrr"] >
                   val_mean["C1_GRAPH_HARD"]["by_seed"][str(s)]["mrr"] for s in SEEDS)
    test_wins = sum(test_mean["C3_QTHS25"]["by_seed"][str(s)]["mrr"] >
                    test_mean["C1_GRAPH_HARD"]["by_seed"][str(s)]["mrr"] for s in SEEDS)
    val_positive = val_mean["C3_QTHS25"]["mean_mrr"] > val_mean["C1_GRAPH_HARD"]["mean_mrr"]
    test_positive = test_mean["C3_QTHS25"]["mean_mrr"] > test_mean["C1_GRAPH_HARD"]["mean_mrr"]
    block["transfer_assessment"] = {
        "positive_mean_on_validation": bool(val_positive), "positive_mean_on_test": bool(test_positive),
        "validation_wins_vs_graph_hard": int(val_wins), "test_wins_vs_graph_hard": int(test_wins),
        "supported": bool(val_positive or test_positive),
        "fully_reverse": bool(not val_positive and not test_positive and val_wins == 0 and test_wins == 0),
        "rule": "positive if validation OR test mean beats Graph-hard; report both without tuning",
    }
    block["state"] = "COMPLETE"
    save_results(result)
    report_dataset("Citeseer", block)
    status("citeseer_complete", None, transfer=block["transfer_assessment"])
    return block


def run_pubmed(result: dict) -> dict:
    full, view = init_dataset("pubmed")
    valid_pos, valid_neg, valid_hash = make_eval_candidates(full, "valid")
    pool, pool_hash = training_pool(view)
    scores, teacher = graph_teacher("pubmed", full, view, pool, pool_hash,
                                    valid_pos, valid_neg, valid_hash)
    qths_idx, qths_meta = v7.make_ids(pool, scores, view.train_pos, QTHS_ALPHA)
    graph_hard = pool[np.arange(len(pool)), np.argmax(scores, axis=1)].copy()
    qths = pool[np.arange(len(pool)), qths_idx].copy()
    methods = ("C1_GRAPH_HARD", "C3_QTHS25")
    block = {
        "state": "RUNNING", "dataset": "pubmed", "runtime": result["environment"]["torch"],
        "split_hash": split_hash(view), "train_pool_hash": pool_hash,
        "train_positive_hash": v61.array_hash(view.train_pos),
        "validation_candidate_hash": valid_hash, "teacher": teacher,
        "qths_rule": qths_meta, "validation": {"runs": {}},
        "seed": 0, "test_evaluated": False,
    }
    result["pubmed"] = block
    save_results(result)
    for method, selected in (("C1_GRAPH_HARD", graph_hard), ("C3_QTHS25", qths)):
        rec = run_model("pubmed", view, method, 0, selected, pool, pool_hash,
                        valid_pos, valid_neg, valid_hash, hypergraph_mode="raw")
        block["validation"]["runs"].setdefault(method, {})["0"] = rec
        save_results(result)
    block["validation"]["summary"] = summarize(block["validation"]["runs"], methods, seeds=(0,))
    graph_mrr = block["validation"]["summary"]["methods"]["C1_GRAPH_HARD"]["mean_mrr"]
    qths_mrr = block["validation"]["summary"]["methods"]["C3_QTHS25"]["mean_mrr"]
    block["screen_status"] = "THIRD_DATASET_POSITIVE_SIGNAL" if qths_mrr > graph_mrr else "THIRD_DATASET_INCONCLUSIVE"
    block["qths_minus_graph_hard"] = float(qths_mrr - graph_mrr)
    block["state"] = "COMPLETE"
    save_results(result)
    report_dataset("PubMed", block)
    status("pubmed_complete", None, screen=block["screen_status"])
    return block


def local_rank_values(scores: np.ndarray) -> np.ndarray:
    scores = np.asarray(scores)
    order = np.argsort(scores, axis=1, kind="stable")
    ranks = np.empty(scores.shape, dtype=np.float64)
    ranks[np.arange(len(scores))[:, None], order] = np.arange(scores.shape[1], dtype=np.float64)[None, :] / max(1, scores.shape[1] - 1)
    return ranks


def selected_ids(pool: np.ndarray, selected: np.ndarray) -> np.ndarray:
    ids = np.empty(len(pool), dtype=np.int64)
    for row, candidates in enumerate(pool):
        lookup = {v61.canonical_edge(edge): col for col, edge in enumerate(candidates)}
        key = v61.canonical_edge(selected[row])
        if key not in lookup:
            raise RuntimeError(f"selected pair is not in candidate row {row}")
        ids[row] = lookup[key]
    return ids


def rg_summary(values: np.ndarray) -> dict:
    return {"mean_Rg": float(np.mean(values)), "median_Rg": float(np.median(values)),
            "p90_Rg": float(np.quantile(values, 0.90)), "p90_Rg_method": "linear"}


def build_hmc(pool: np.ndarray, scores: np.ndarray, train_pos: np.ndarray,
              target_ids: np.ndarray, seed: int) -> tuple[np.ndarray, dict]:
    rank = local_rank_values(scores)
    order = np.argsort(-scores, axis=1, kind="stable")[:, :2]
    target_rg = rank[np.arange(len(pool)), target_ids]
    target = rg_summary(target_rg)
    n = len(pool)
    runner_count = int(round(QTHS_ALPHA * 2 * n))
    rng = np.random.default_rng(731_500 + int(seed) * 10_000)
    best_ids = None
    best_loss = float("inf")
    best_stat = None
    # Randomized constrained resampling matches the locked QTHS hardness quantiles.
    for trial in range(2048):
        runners = rng.choice(n, size=runner_count, replace=False)
        ids = order[:, 0].copy()
        ids[runners] = order[runners, 1]
        rg = rank[np.arange(n), ids]
        stat = rg_summary(rg)
        loss = (abs(stat["mean_Rg"] - target["mean_Rg"]) +
                abs(stat["median_Rg"] - target["median_Rg"]) +
                abs(stat["p90_Rg"] - target["p90_Rg"]))
        if loss < best_loss:
            best_ids, best_loss, best_stat = ids, loss, stat
        if loss <= 1e-12:
            break
    selected = pool[np.arange(n), best_ids].copy()
    return selected, {
        "method": "randomized top-two resampling with fixed QTHS occurrence count",
        "seed": int(seed), "trials": trial + 1, "runner_up_rows": int(runner_count),
        "target_QTHS_Rg": target, "matched_Rg": best_stat,
        "absolute_quantile_error_sum": float(best_loss),
        "selected_negative_hash": v61.array_hash(selected),
    }


def gini_from_histogram(hist: np.ndarray, node_count: int, total_incidence: int) -> float:
    cumulative = 0
    weighted_positions = 0.0
    for value, number in enumerate(hist):
        if number <= 0:
            continue
        position_sum = number * cumulative + number * (number + 1) / 2
        weighted_positions += value * position_sum
        cumulative += int(number)
    if total_incidence == 0 or node_count == 0:
        return 0.0
    return float(2 * weighted_positions / (node_count * total_incidence) - (node_count + 1) / node_count)


def diversity_vector(selected: np.ndarray, num_nodes: int, degree: np.ndarray) -> dict:
    endpoint_counts = np.bincount(selected.reshape(-1), minlength=num_nodes).astype(np.int64)
    hist = np.bincount(endpoint_counts)
    hub_nodes = np.lexsort((np.arange(num_nodes), -degree))[:max(1, int(math.ceil(0.10 * num_nodes)))]
    hub = np.zeros(num_nodes, dtype=bool)
    hub[hub_nodes] = True
    return {
        "unique_endpoint_ratio": float(np.count_nonzero(endpoint_counts) / selected.size),
        "endpoint_gini": gini_from_histogram(hist, num_nodes, int(endpoint_counts.sum())),
        "hub_endpoint_ratio": float(np.mean(hub[selected])),
        "endpoint_counts": endpoint_counts,
        "histogram": hist,
        "hub_mask": hub,
    }


def build_dmc(pool: np.ndarray, scores: np.ndarray, train_pos: np.ndarray,
              qths_selected: np.ndarray, degree: np.ndarray, seed: int) -> tuple[np.ndarray, dict]:
    n, candidate_count, _ = pool.shape
    rank = local_rank_values(scores)
    qths_stats = v7.summarize(pool, scores, qths_selected, degree)
    target = {key: float(qths_stats[key]) for key in
              ("unique_endpoint_ratio", "endpoint_gini", "hub_endpoint_ratio")}
    ids = np.argmax(scores, axis=1).astype(np.int64)
    counts = np.bincount(pool[np.arange(n), ids].reshape(-1), minlength=len(degree)).astype(np.int64)
    hist = np.bincount(counts).astype(np.int64)
    hub_nodes = np.lexsort((np.arange(len(degree)), -degree))[:max(1, int(math.ceil(0.10 * len(degree))))]
    hub = np.zeros(len(degree), dtype=bool)
    hub[hub_nodes] = True
    hub_count = int(np.count_nonzero(hub[pool[np.arange(n), ids]]))
    sum_rg = float(rank[np.arange(n), ids].sum())

    def objective(local_hist: np.ndarray, local_hub: int, local_sum_rg: float) -> tuple[float, dict]:
        metrics = {
            "unique_endpoint_ratio": float((len(degree) - int(local_hist[0])) / (2 * n)),
            "endpoint_gini": gini_from_histogram(local_hist, len(degree), 2 * n),
            "hub_endpoint_ratio": float(local_hub / (2 * n)),
            "mean_Rg": float(local_sum_rg / n),
        }
        # Diversity is the matching constraint; rank hardness breaks close ties toward Graph-hard.
        loss = (((metrics["unique_endpoint_ratio"] - target["unique_endpoint_ratio"]) / 0.005) ** 2 +
                ((metrics["endpoint_gini"] - target["endpoint_gini"]) / 0.01) ** 2 +
                ((metrics["hub_endpoint_ratio"] - target["hub_endpoint_ratio"]) / 0.01) ** 2 +
                0.05 * (1.0 - metrics["mean_Rg"]))
        return float(loss), metrics

    best_loss, current_metrics = objective(hist, hub_count, sum_rg)
    rng = np.random.default_rng(744_100 + int(seed) * 10_000)
    sweeps = []
    for sweep in range(5):
        changed = 0
        for row in rng.permutation(n):
            old_id = int(ids[row])
            old_pair = pool[row, old_id]
            old_rg = float(rank[row, old_id])
            row_best = old_id
            row_best_loss = best_loss
            row_best_state = None
            for candidate_id in range(candidate_count):
                if candidate_id == old_id:
                    continue
                new_pair = pool[row, candidate_id]
                delta = {}
                for node in map(int, old_pair):
                    delta[node] = delta.get(node, 0) - 1
                for node in map(int, new_pair):
                    delta[node] = delta.get(node, 0) + 1
                delta = {node: value for node, value in delta.items() if value}
                if not delta:
                    new_hist = hist
                else:
                    new_hist = hist.copy()
                    for node, change in delta.items():
                        before = int(counts[node])
                        after = before + change
                        if after < 0:
                            raise RuntimeError("DMC endpoint count underflow")
                        needed = after + 1
                        if needed > len(new_hist):
                            new_hist = np.pad(new_hist, (0, needed - len(new_hist)))
                        new_hist[before] -= 1
                        new_hist[after] += 1
                local_hub = hub_count - int(np.count_nonzero(hub[old_pair])) + int(np.count_nonzero(hub[new_pair]))
                local_sum = sum_rg - old_rg + float(rank[row, candidate_id])
                loss, _ = objective(new_hist, local_hub, local_sum)
                if loss + 1e-12 < row_best_loss:
                    row_best, row_best_loss = candidate_id, loss
                    row_best_state = (new_hist, local_hub, local_sum, delta)
            if row_best != old_id and row_best_state is not None:
                hist, hub_count, sum_rg, delta = row_best_state
                for node, change in delta.items():
                    counts[node] += change
                ids[row] = row_best
                best_loss = row_best_loss
                changed += 1
        current_loss, current_metrics = objective(hist, hub_count, sum_rg)
        sweeps.append({"sweep": sweep + 1, "changed_rows": changed, "objective": current_loss,
                       "metrics": current_metrics})
        if changed == 0:
            break
    selected = pool[np.arange(n), ids].copy()
    return selected, {
        "method": "constrained random coordinate resampling over the frozen 20-candidate train pool",
        "seed": int(seed), "target_QTHS_diversity": target,
        "matched_diversity_and_hardness": current_metrics,
        "absolute_target_error": {key: float(current_metrics[key] - target[key]) for key in target},
        "sweeps": sweeps, "selected_negative_hash": v61.array_hash(selected),
    }


def run_mechanism_controls(result: dict) -> dict:
    block = result["cora"]
    full, view = init_dataset("cora")
    with np.load(V61 / "strict_train_candidates_and_selections.npz", allow_pickle=False) as z:
        archive = {key: z[key].copy() for key in z.files}
    pool, scores = archive["negative_candidates"], archive["score_graph"]
    valid_pos, valid_neg, valid_hash = make_eval_candidates(full, "valid")
    qths_idx, _ = v7.make_ids(pool, scores, view.train_pos, QTHS_ALPHA)
    qths_selected = pool[np.arange(len(pool)), qths_idx].copy()
    train_graph = view.train_graph()
    degree = np.asarray([train_graph.degree(node) for node in range(view.num_nodes)], dtype=np.int64)
    methods = ("GRAPH_HARD", "RANDOM_VETO", "HMC", "QTHS25", "DMC")
    records = {"GRAPH_HARD": block["validation"]["runs"]["C1_GRAPH_HARD"],
               "RANDOM_VETO": block["validation"]["runs"]["C2_RANDOM_VETO"],
               "QTHS25": block["validation"]["runs"]["C3_QTHS25"],
               "HMC": {}, "DMC": {}}
    diagnostics = {"HMC": {}, "DMC": {}}
    pool_hash = block["train_pool_hash"]
    for seed in SEEDS:
        hmc_selected, hmc_meta = build_hmc(pool, scores, view.train_pos, qths_idx, seed)
        dmc_selected, dmc_meta = build_dmc(pool, scores, view.train_pos, qths_selected, degree, seed)
        diagnostics["HMC"][str(seed)] = hmc_meta
        diagnostics["DMC"][str(seed)] = dmc_meta
        for method, selected in (("HMC", hmc_selected), ("DMC", dmc_selected)):
            rec = run_model("cora", view, f"MECH_{method}", seed, selected, pool, pool_hash,
                            valid_pos, valid_neg, valid_hash, hypergraph_mode="raw")
            records[method][str(seed)] = rec
            complete_methods = tuple(m for m in methods if len(records.get(m, {})) == len(SEEDS))
            partial_summary = summarize(
                {m: records[m] for m in complete_methods}, complete_methods,
            ) if complete_methods else None
            result["mechanism_controls"] = {"state": "RUNNING", "records": records,
                                             "diagnostics": diagnostics, "validation": partial_summary}
            save_results(result)
    summary = summarize(records, methods)
    means = {method: summary["methods"][method]["mean_mrr"] for method in methods}
    qths_wins_hmc = sum(records["QTHS25"][str(s)]["validation_metrics"]["mrr"] >
                        records["HMC"][str(s)]["validation_metrics"]["mrr"] for s in SEEDS)
    qths_wins_dmc = sum(records["QTHS25"][str(s)]["validation_metrics"]["mrr"] >
                        records["DMC"][str(s)]["validation_metrics"]["mrr"] for s in SEEDS)
    close_hmc = abs(means["QTHS25"] - means["HMC"]) <= 0.001
    close_dmc = abs(means["QTHS25"] - means["DMC"]) <= 0.001
    if means["QTHS25"] > means["HMC"] and means["QTHS25"] > means["DMC"]:
        classification = "JOINT_SELECTION_EFFECT"
    elif close_hmc and not close_dmc:
        classification = "HARDNESS_DOMINANT"
    elif close_dmc and not close_hmc:
        classification = "DIVERSITY_DOMINANT"
    else:
        classification = "INCONCLUSIVE"
    output = {
        "state": "COMPLETE", "validation": summary, "diagnostics": diagnostics,
        "mean_mrr": means,
        "QTHS25_beats_HMC_mean": bool(means["QTHS25"] > means["HMC"]),
        "QTHS25_beats_DMC_mean": bool(means["QTHS25"] > means["DMC"]),
        "QTHS25_wins_vs_HMC": int(qths_wins_hmc), "QTHS25_wins_vs_DMC": int(qths_wins_dmc),
        "classification_rule": "mean advantage over both => joint; within 0.001 of only HMC => hardness dominant; within 0.001 of only DMC => diversity dominant; ambiguous/both-close => inconclusive",
        "mechanism_class": classification,
        "test_evaluated": False,
    }
    result["mechanism_controls"] = output
    save_results(result)
    lines = ["# V7.1 mechanism controls", "",
             "Validation only. The Graph-hard, random-veto and QTHS25 rows reuse the locked Cora checkpoints; HMC and DMC are newly trained at fixed epoch 10.", "",
             "| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |", "|---|---:|---:|---:|---:|---:|"]
    for method in methods:
        row = summary["methods"][method]
        vals = [row["by_seed"][str(s)]["mrr"] for s in SEEDS]
        lines.append(f"| {method} | " + " | ".join(f"{x:.6f}" for x in vals) +
                     f" | {row['mean_mrr']:.6f} | {row['sample_std_mrr']:.6f} |")
    lines += ["", f"- Mechanism class: **{classification}**.",
              f"- QTHS25 beats HMC in {qths_wins_hmc}/3 seed comparisons; beats DMC in {qths_wins_dmc}/3.",
              "- Per-seed HMC hardness quantile matching and DMC diversity/hardness deviations are in results.json.", ""]
    (OUT / "04_MECHANISM_CONTROLS.md").write_text("\n".join(lines), encoding="utf-8")
    status("mechanism_controls_complete", None, mechanism_class=classification)
    return output


def adaptive_tail(pool: np.ndarray, scores: np.ndarray) -> tuple[np.ndarray, float, np.ndarray]:
    q25, q50, q75, q90 = np.quantile(scores, [0.25, 0.50, 0.75, 0.90], axis=1)
    tail = (q90 - q50) / ((q75 - q25) + 1e-8)
    threshold = float(np.median(tail))
    high_tail = tail >= threshold
    return tail.astype(np.float64), threshold, high_tail


def adaptive_selector(pool: np.ndarray, scores: np.ndarray, train_pos: np.ndarray,
                      high_mask: np.ndarray, salt: str, seed: int,
                      randomized: bool = False) -> tuple[np.ndarray, dict]:
    order = np.argsort(-scores, axis=1, kind="stable")[:, :2]
    selected_ids = order[:, 0].copy()
    groups = {"trim_15": np.flatnonzero(~high_mask), "trim_35": np.flatnonzero(high_mask)}
    rng = np.random.default_rng(780_000 + int(seed) * 10_000 + 1_000 * int(randomized))
    group_report = {}
    for label, rows in groups.items():
        alpha = 0.15 if label.endswith("15") else 0.35
        # The inherited QTHS mechanism is a two-candidate prepool. Trimming alpha of its
        # 2N candidate occurrences means 2*alpha*N rows switch from top-1 to runner-up.
        switch_count = min(len(rows), int(round(2.0 * alpha * len(rows))))
        if randomized:
            sequence = rng.permutation(rows)
        else:
            keys = []
            for row in rows:
                u, v = v61.canonical_edge(train_pos[row])
                key = hashlib.sha256(f"{u}:{v}:{salt}".encode("utf-8")).hexdigest()
                keys.append((key, int(row)))
            sequence = np.asarray([row for _, row in sorted(keys)], dtype=np.int64)
        switched = sequence[:switch_count]
        selected_ids[switched] = order[switched, 1]
        group_report[label] = {
            "positive_count": int(len(rows)), "nominal_trim_alpha": alpha,
            "runner_up_count": int(switch_count),
            "realized_candidate_occurrence_trim_fraction": float(switch_count / (2 * len(rows))) if len(rows) else 0.0,
            "selected_positive_row_hash": v61.array_hash(np.asarray(switched, dtype=np.int64)),
        }
    selected = pool[np.arange(len(pool)), selected_ids].copy()
    return selected, {
        "rule": "within each positive's frozen top-2 Graph-hard prepool, switch 2*alpha share of rows to rank-2",
        "low_trim_alpha": 0.15, "high_trim_alpha": 0.35,
        "high_group_positive_count": int(np.count_nonzero(high_mask)),
        "low_group_positive_count": int(np.count_nonzero(~high_mask)),
        "groups": group_report, "seed": int(seed), "selector_salt": salt,
        "randomized_within_groups": bool(randomized),
        "selected_negative_hash": v61.array_hash(selected),
    }


def prepare_aqths_selections(dataset: str, pool: np.ndarray, scores: np.ndarray,
                             train_pos: np.ndarray, degree: np.ndarray,
                             seed: int) -> tuple[dict, dict]:
    tail, threshold, aq_high = adaptive_tail(pool, scores)
    degree_sum = degree[train_pos[:, 0]] + degree[train_pos[:, 1]]
    degree_threshold = float(np.median(degree_sum))
    degree_high = degree_sum >= degree_threshold
    # Random-adaptive uses the same high/low class counts as AQTHS, but breaks the
    # link between tail shape and trim strength.
    rng = np.random.default_rng(790_000 + int(seed) * 10_000)
    high_rows = rng.permutation(len(train_pos))[:int(np.count_nonzero(aq_high))]
    random_high = np.zeros(len(train_pos), dtype=bool)
    random_high[high_rows] = True
    selections, metadata = {}, {}
    for name, mask, salt, randomized in (
        ("A2_RANDOM_ADAPTIVE", random_high, f"AQTHS_A2_{seed}", True),
        ("A3_DEGREE_ADAPTIVE", degree_high, "AQTHS_A3_DEGREE", False),
        ("A4_AQTHS", aq_high, "AQTHS_A4_TAIL", False),
    ):
        selections[name], metadata[name] = adaptive_selector(
            pool, scores, train_pos, mask, salt, seed, randomized=randomized,
        )
    metadata["train_only_tail_statistic"] = {
        "formula": "(Q90-Q50)/(Q75-Q25+1e-8)",
        "threshold_median_over_training_positive_pools": threshold,
        "training_pool_only": True, "validation_or_test_used": False,
        "tail_quantiles": {"q25_mean": float(np.mean(np.quantile(scores, .25, axis=1))),
                           "q50_mean": float(np.mean(np.quantile(scores, .50, axis=1))),
                           "q75_mean": float(np.mean(np.quantile(scores, .75, axis=1))),
                           "q90_mean": float(np.mean(np.quantile(scores, .90, axis=1)))},
        "tail_excess_mean": float(np.mean(tail)), "tail_excess_median": float(np.median(tail)),
        "tail_excess_min": float(np.min(tail)), "tail_excess_max": float(np.max(tail)),
        "aqths_high_group_count": int(np.count_nonzero(aq_high)),
        "degree_control_median_endpoint_degree_sum": degree_threshold,
        "degree_control_high_group_count": int(np.count_nonzero(degree_high)),
    }
    metadata["A2_random_assignment"] = {"seed": int(seed), "high_group_count_matches_AQTHS": bool(np.count_nonzero(random_high) == np.count_nonzero(aq_high))}
    return selections, {"tail_excess": tail, "threshold": threshold, "aq_high": aq_high,
                        "degree_high": degree_high, "random_high": random_high,
                        "metadata": metadata}


def run_aqths_cora(result: dict) -> dict:
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling

    full, view = init_dataset("cora")
    with np.load(V61 / "strict_train_candidates_and_selections.npz", allow_pickle=False) as z:
        archive = {key: z[key].copy() for key in z.files}
    pool, scores = archive["negative_candidates"], archive["score_graph"]
    valid_pos, valid_neg, valid_hash = make_eval_candidates(full, "valid")
    graph = view.train_graph()
    degree = np.asarray([graph.degree(node) for node in range(view.num_nodes)], dtype=np.int64)
    qths_idx, _ = v7.make_ids(pool, scores, view.train_pos, QTHS_ALPHA)
    graph_hard = pool[np.arange(len(pool)), np.argmax(scores, axis=1)].copy()
    records = {
        "A0_GRAPH_HARD": result["cora"]["validation"]["runs"]["C1_GRAPH_HARD"],
        "A1_QTHS25": result["cora"]["validation"]["runs"]["C3_QTHS25"],
        "A2_RANDOM_ADAPTIVE": {}, "A3_DEGREE_ADAPTIVE": {}, "A4_AQTHS": {},
    }
    diagnostics = {"selection_hashes": {}, "per_seed": {}}
    pool_hash = result["cora"]["train_pool_hash"]
    for seed in SEEDS:
        selections, details = prepare_aqths_selections(
            "cora", pool, scores, view.train_pos, degree, seed,
        )
        diagnostics["per_seed"][str(seed)] = details["metadata"]
        for method in ("A2_RANDOM_ADAPTIVE", "A3_DEGREE_ADAPTIVE", "A4_AQTHS"):
            selected = selections[method]
            diagnostics["selection_hashes"].setdefault(method, {})[str(seed)] = v61.array_hash(selected)
            rec = run_model("cora", view, method, seed, selected, pool, pool_hash,
                            valid_pos, valid_neg, valid_hash, hypergraph_mode="raw")
            records[method][str(seed)] = rec
            result["aqths"] = {"state": "RUNNING", "validation_runs": records,
                               "selection_diagnostics": diagnostics}
            save_results(result)
        # Persist training-only per-positive inputs/assignments; no held-out labels are included.
        assignment_dir = OUT / "A_AQTHS"
        assignment_dir.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            assignment_dir / f"cora_train_only_assignments_seed{seed}.npz",
            tail_excess=details["tail_excess"], high_tail=details["aq_high"],
            degree_high=details["degree_high"], random_high=details["random_high"],
            random_adaptive=selections["A2_RANDOM_ADAPTIVE"],
            degree_adaptive=selections["A3_DEGREE_ADAPTIVE"], aqths=selections["A4_AQTHS"],
        )
    methods = ("A0_GRAPH_HARD", "A1_QTHS25", "A2_RANDOM_ADAPTIVE", "A3_DEGREE_ADAPTIVE", "A4_AQTHS")
    summary = summarize(records, methods)
    qths = [records["A1_QTHS25"][str(s)]["validation_metrics"]["mrr"] for s in SEEDS]
    random_adaptive = [records["A2_RANDOM_ADAPTIVE"][str(s)]["validation_metrics"]["mrr"] for s in SEEDS]
    aqths = [records["A4_AQTHS"][str(s)]["validation_metrics"]["mrr"] for s in SEEDS]
    gain = float(np.mean(aqths) - np.mean(qths))
    relative = float(gain / np.mean(qths)) if np.mean(qths) else None
    wins_qths = int(sum(a > b for a, b in zip(aqths, qths)))
    wins_random = int(sum(a > b for a, b in zip(aqths, random_adaptive)))
    gain_gate = bool(gain >= 0.0015 or (relative is not None and relative >= 0.003))
    go = bool(np.mean(aqths) > np.mean(qths) and wins_qths >= 2 and
              np.mean(aqths) > np.mean(random_adaptive) and wins_random >= 2 and gain_gate)
    output = {
        "state": "VALIDATION_GO" if go else "AQTHS_REJECT",
        "validation": summary, "selection_diagnostics": diagnostics,
        "AQTHS_mean_gain_vs_QTHS25": gain, "AQTHS_relative_gain_vs_QTHS25": relative,
        "AQTHS_wins_vs_QTHS25": wins_qths, "AQTHS_wins_vs_random_adaptive": wins_random,
        "gain_gate_pass": gain_gate, "GO": go,
        "rule": "A4 mean > A1 and >=2/3 wins; A4 mean > A2 and >=2/3 wins; gain >=0.0015 absolute OR 0.3% relative",
        "test_evaluated": False,
    }
    previous_aqths = result.get("aqths", {})
    output["test"] = previous_aqths.get("test", output.get("test", {}))
    output["citeseer"] = previous_aqths.get("citeseer", output.get("citeseer", {}))
    result["aqths"] = output
    save_results(result)
    (OUT / "A_AQTHS" / "cora_validation.json").write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = ["# AQTHS Cora validation gate", "", "All trim thresholds and per-positive tail statistics use the training candidate pool only. The global high-tail threshold is the median over Cora training positives; no model or threshold was selected on validation.", "",
             "| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |", "|---|---:|---:|---:|---:|---:|"]
    for method, row in summary["methods"].items():
        values = [row["by_seed"][str(s)]["mrr"] for s in SEEDS]
        lines.append(f"| {method} | " + " | ".join(f"{x:.6f}" for x in values) +
                     f" | {row['mean_mrr']:.6f} | {row['sample_std_mrr']:.6f} |")
    lines += ["", f"- Gate: **{'GO' if go else 'REJECT'}**; mean gain={gain:+.6f} ({relative if relative is not None else 0:.3%}); wins vs QTHS25={wins_qths}/3, vs random adaptive={wins_random}/3.",
              "- A2 randomly assigns the same number of 15%/35% positives as AQTHS. A3 assigns them by train-graph endpoint-degree sum. A4 assigns them by train-pool hardness-tail excess.", ""]
    (OUT / "A_AQTHS" / "cora_validation.md").write_text("\n".join(lines), encoding="utf-8")
    return output


def run_aqths_cora_test(result: dict) -> dict:
    block = result["aqths"]
    if not block.get("GO"):
        return {"state": "NOT_RUN_VALIDATION_GATE_CLOSED", "test_evaluated": False}
    cora = result["cora"]
    with np.load(OUT / "EVALUATION" / "cora_test_candidates.npz", allow_pickle=False) as z:
        test_pos, test_neg = z["test_positive"].copy(), z["test_negative_candidates"].copy()
    test_hash = v61.array_hash(test_neg)
    if test_hash != cora["test"]["candidate_hash"]:
        raise RuntimeError("AQTHS test candidate cache is not the frozen Cora candidate array")
    full, view = init_dataset("cora")
    methods = ("A1_QTHS25", "A2_RANDOM_ADAPTIVE", "A4_AQTHS")
    records = {"A1_QTHS25": {}, "A2_RANDOM_ADAPTIVE": {}, "A4_AQTHS": {}}
    prior_test = block.get("test", {})
    for seed in SEEDS:
        locked = cora["test"]["by_method_seed"]["C3_QTHS25"][str(seed)]
        records["A1_QTHS25"][str(seed)] = locked
        for method in ("A2_RANDOM_ADAPTIVE", "A4_AQTHS"):
            prior_row = prior_test.get("summary", {}).get("methods", {}).get(method, {}).get("by_seed", {}).get(str(seed))
            if prior_test.get("candidate_hash") == test_hash and prior_row is not None:
                records[method][str(seed)] = prior_row
                continue
            rec = block["validation"]["runs"][method][str(seed)]
            metric = engine.eval_fixed_candidates(rec["checkpoint"], view, test_pos, test_neg)
            records[method][str(seed)] = {**metric, "checkpoint": rec["checkpoint"],
                                          "checkpoint_file_sha256": rec["checkpoint_file_sha256"],
                                          "candidate_hash": test_hash}
    summary = summarize(records, methods)
    qths = [records["A1_QTHS25"][str(s)]["mrr"] for s in SEEDS]
    aqths = [records["A4_AQTHS"][str(s)]["mrr"] for s in SEEDS]
    wins = int(sum(a > b for a, b in zip(aqths, qths)))
    confirmed = bool(np.mean(aqths) > np.mean(qths) and wins >= 2)
    output = {
        "state": "INNOVATION_2_CONFIRMED" if confirmed else "AQTHS_TEST_NOT_CONFIRMED",
        "summary": summary, "candidate_hash": test_hash,
        "AQTHS_test_mean_gain_vs_QTHS25": float(np.mean(aqths) - np.mean(qths)),
        "AQTHS_test_wins_vs_QTHS25": wins, "confirmed": confirmed,
        "test_candidates_reused_without_regeneration": True,
        "test_evaluated_once_per_new_checkpoint": True,
    }
    block["test"] = output
    block["state"] = output["state"]
    result["aqths"] = block
    save_results(result)
    write_json(OUT / "A_AQTHS" / "cora_test.json", output)
    lines = ["# AQTHS Cora test", "", "One-time test evaluation; the already frozen QTHS25 test rows are reused and the shared candidate hash is unchanged.", "",
             "| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |", "|---|---:|---:|---:|---:|---:|"]
    for method, row in summary["methods"].items():
        vals = [row["by_seed"][str(s)]["mrr"] for s in SEEDS]
        lines.append(f"| {method} | " + " | ".join(f"{x:.6f}" for x in vals) +
                     f" | {row['mean_mrr']:.6f} | {row['sample_std_mrr']:.6f} |")
    lines += ["", f"- Innovation 2 test confirmation: **{'YES' if confirmed else 'NO'}**; AQTHS beats QTHS25 in {wins}/3 seeds; mean delta={output['AQTHS_test_mean_gain_vs_QTHS25']:+.6f}.", ""]
    (OUT / "A_AQTHS" / "cora_test.md").write_text("\n".join(lines), encoding="utf-8")
    return output


def run_aqths_citeseer(result: dict) -> dict:
    if not result.get("aqths", {}).get("test", {}).get("confirmed"):
        return {"state": "NOT_RUN_AQTHS_TEST_NOT_CONFIRMED", "test_evaluated": False}
    full, view = init_dataset("citeseer")
    cite = result["citeseer"]
    with np.load(OUT / "TEACHERS" / "citeseer" / "graph_teacher_scores.npz", allow_pickle=False) as z:
        pool, scores = z["candidates"].copy(), z["scores"].copy()
    valid_pos, valid_neg, valid_hash = make_eval_candidates(full, "valid")
    qths_selected, _ = v7.make_ids(pool, scores, view.train_pos, QTHS_ALPHA)
    graph = view.train_graph()
    degree = np.asarray([graph.degree(node) for node in range(view.num_nodes)], dtype=np.int64)
    records = {"QTHS25": cite["validation"]["runs"]["C3_QTHS25"], "AQTHS": {}}
    metadata = {}
    for seed in SEEDS:
        selections, details = prepare_aqths_selections("citeseer", pool, scores, view.train_pos, degree, seed)
        selected = selections["A4_AQTHS"]
        metadata[str(seed)] = details["metadata"]
        rec = run_model("citeseer", view, "AQTHS_CROSSDATASET", seed, selected, pool,
                        cite["train_pool_hash"], valid_pos, valid_neg, valid_hash, hypergraph_mode="raw")
        records["AQTHS"][str(seed)] = rec
    valid_summary = summarize(records, ("QTHS25", "AQTHS"))
    with np.load(OUT / "EVALUATION" / "citeseer_test_candidates.npz", allow_pickle=False) as z:
        test_pos, test_neg = z["test_positive"].copy(), z["test_negative_candidates"].copy()
    test_hash = v61.array_hash(test_neg)
    if test_hash != cite["test_candidate_hash"]:
        raise RuntimeError("Citeseer AQTHS test candidate hash changed after the locked comparison")
    test_records = {"QTHS25": cite["test"]["by_method_seed"]["C3_QTHS25"], "AQTHS": {}}
    for seed in SEEDS:
        rec = records["AQTHS"][str(seed)]
        metric = engine.eval_fixed_candidates(rec["checkpoint"], view, test_pos, test_neg)
        test_records["AQTHS"][str(seed)] = {**metric, "checkpoint": rec["checkpoint"],
                                             "checkpoint_file_sha256": rec["checkpoint_file_sha256"],
                                             "candidate_hash": test_hash}
    test_summary = summarize(test_records, ("QTHS25", "AQTHS"))
    output = {"state": "COMPLETE", "validation": valid_summary, "test": test_summary,
              "test_candidate_hash": test_hash, "training_pool_median_recomputed_on_citeseer": True,
              "thresholds_used": {seed: metadata[seed]["train_only_tail_statistic"] for seed in metadata},
              "test_evaluated_once_per_AQTHS_checkpoint": True,
              "mean_test_gain": float(test_summary["methods"]["AQTHS"]["mean_mrr"] - test_summary["methods"]["QTHS25"]["mean_mrr"]),
              "test_wins": int(sum(test_records["AQTHS"][str(s)]["mrr"] > test_records["QTHS25"][str(s)]["mrr"] for s in SEEDS))}
    result["aqths"]["citeseer"] = output
    save_results(result)
    write_json(OUT / "A_AQTHS" / "citeseer_results.json", output)
    return output


def write_novelty_search() -> None:
    lines = [
        "# Focused novelty search: quantile and tail-adaptive negative sampling", "",
        "Search date: 2026-10-02. Scope: graph link prediction and adjacent hyperlink/hyperedge prediction; queries covered quantile hard-negative sampling, trimmed/extreme-tail negatives, per-positive adaptive hardness, semi-hard sampling, DMNS, MeBNS, HNS/DNS, and self-adversarial sampling. This is a targeted search, not an exhaustive priority review.", "",
        "## Findings", "",
        "No exact paper match was identified for (i) trimming a frozen graph-teacher-ranked top-two negative pool per positive and (ii) setting the trim level from that positive's training-pool tail-excess statistic using a two-level 15%/35% rule. This is not evidence of priority and does not support a first-claim.", "",
        "| Work | Relevant overlap | Distinction from QTHS/AQTHS |", "|---|---|---|",
        "| [MeBNS (Wang et al., 2023)](https://arxiv.org/abs/2312.04815) | Link-prediction negative selection and hard/easy sample migration; uses teacher/student and meta reweighting. | Learned/meta-learning framework; no fixed per-positive teacher-score quantile trim or tail-shape 15/35 rule. |",
        "| [DMNS (Nguyen & Fang, WWW 2024)](https://arxiv.org/abs/2403.17259) | Graph link prediction with controllable multi-level negative hardness. | Diffusion-based latent candidate generation and hardness levels, not trimming a fixed graph-teacher candidate pool by a per-positive quantile. |",
        "| [HeaRT (Li et al., NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/hash/0be50b4590f1c5fdf4c8feddd63c4f67-Abstract-Datasets_and_Benchmarks.html) | Positive-conditioned, heuristic hard negatives for link-prediction evaluation. | Evaluation benchmark construction, not train-time tail trimming. |",
        "| [ProGCL (Xia et al., ICML 2022)](https://proceedings.mlr.press/v162/xia22b.html) | Shows that the hardest graph contrastive negatives can be unreliable; estimates false-negative probability alongside similarity. | Node-level graph contrastive learning with reliability estimation, not supervised link-prediction candidate quantiles. |",
        "| [Adaptive Hardness Negative Sampling for Collaborative Filtering (2024)](https://arxiv.org/abs/2401.05191) | Adapts hardness to individual recommendation samples. | Collaborative filtering; adaptive hardness is related, but the searched description does not match graph-link-prediction teacher-pool tail quantile trimming. |",
        "| [Hard Negative Sampling in Hyperedge Prediction (Deng et al., 2025)](https://arxiv.org/abs/2503.08743) | Direct hard-negative work in higher-order prediction. | Synthesizes negatives in hyperedge embedding space; it rules out broad claims that hard-negative sampling itself is new. |",
        "| [Negative Sampling for Hyperlink Prediction in Networks (Patil et al., 2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7206280/) | Studies negative-sample hardness distributions for hyperlink prediction. | Structural sampling strategies; not teacher-ranked per-positive quantile trimming. |",
        "| [RotatE (Sun et al., ICLR 2019)](https://arxiv.org/abs/1902.10197) | Self-adversarial weighting emphasizes higher-scoring negatives. | Knowledge-graph embedding weighting, not tail trimming or adaptive per-positive candidate quantiles. |",
        "", "## Conservative novelty status", "",
        "`NO_EXACT_MATCH_IDENTIFIED_IN_FOCUSED_SEARCH`. The defensible claim, if experiments support it, is a narrow empirical contribution: a fixed graph-teacher top-two rank trim (QTHS) and a training-pool tail-shape-conditioned allocation of the trim between per-positive examples (AQTHS). Do not claim first, optimal, or universally novel. Database/citation searches and broader full-text screening remain necessary before submission.", "",
    ]
    (OUT / "05_NOVELTY_SEARCH.md").write_text("\n".join(lines), encoding="utf-8")


def write_locked_reproduction(result: dict) -> None:
    env = result.get("environment", {})
    cora = result.get("cora", {})
    lines = [
        "# Locked reproduction and environment", "",
        f"- Status: **{cora.get('locked_reproduction_status', 'PENDING')}**.",
        f"- Runtime: `{json.dumps(env, ensure_ascii=False)}`.",
        f"- Environment route: `{env.get('environment_route')}`; `ENVIRONMENT_REPRO_BLOCKED={env.get('environment_repro_blocked')}`. Existing `mei_env` was left unchanged. The new venv isolates PyTorch/CUDA wheels; other shared base packages are read-only site packages from Python 3.11.11.",
        "- The project environment file requests Python 3.10; this dedicated run retained the available Python 3.11.11 ABI and reports that mismatch rather than changing the active environment.",
        "- Locked rule: STRICT_TRAIN_ONLY; training-pool exclusions use train positives/message edges only; 20 fixed candidate rows per train positive; one sampled negative per positive per epoch; exactly 10 epochs; final epoch checkpoint; fixed Graph teacher, decoder, optimizer and hidden dimensions; no validation-best checkpoint and no test-guided changes.",
        f"- Cora split hash: `{cora.get('split_hash')}`; train positive hash: `{cora.get('train_positive_hash')}`; candidate-pool hash: `{cora.get('train_pool_hash')}`; validation candidate hash: `{cora.get('validation_candidate_hash')}`.",
        f"- Frozen teacher state hash: `{cora.get('teacher_state_hash')}`; cached teacher-score hash: `{cora.get('teacher_scores_hash')}`.",
        f"- Cora test candidate hash (opened once after validation freeze): `{cora.get('test', {}).get('candidate_hash', 'not opened')}`.",
        "- Per-seed validation/test MRR, means, sample standard deviations, paired deltas and checkpoint SHA256 values are in `results.json` and `01_CORA_FULL_RESULTS.md`.",
        "",
    ]
    (OUT / "00_LOCKED_REPRODUCTION.md").write_text("\n".join(lines), encoding="utf-8")


def write_final_report(result: dict) -> None:
    cora_status = result.get("cora", {}).get("locked_reproduction_status", "NOT_RUN")
    cite = result.get("citeseer", {}).get("transfer_assessment", {})
    pub = result.get("pubmed", {})
    mechanism = result.get("mechanism_controls", {}).get("mechanism_class", "NOT_RUN")
    aq = result.get("aqths", {})
    aq_confirmed = bool(aq.get("test", {}).get("confirmed", False))
    decision = "REPRODUCTION_FAILURE" if cora_status != "PASS" else (
        "QTHS_PLUS_AQTHS" if aq_confirmed else "QTHS_ONLY_PAPER_READY"
    )
    result["QTHS_LOCKED_REPRODUCTION"] = cora_status
    result["MECHANISM_CLASS"] = mechanism
    result["INNOVATION_1"] = "QTHS"
    result["INNOVATION_2_CONFIRMED"] = bool(aq_confirmed)
    result["NOVELTY_STATUS"] = "NO_EXACT_MATCH_IDENTIFIED_IN_FOCUSED_SEARCH"
    result["FINAL_DECISION"] = decision
    result["NEXT_EXPECTED_STEP"] = (
        "Benchmark expansion, ablations, runtime, paper writing" if cora_status == "PASS" else
        "Resolve the locked reproduction failure before continuing"
    )
    save_results(result)
    cora_test = result.get("cora", {}).get("test", {}).get("summary", {}).get("methods", {})
    lines = [
        "# V7.1 final report", "",
        f"- QTHS_LOCKED_REPRODUCTION: **{cora_status}**",
        f"- ENVIRONMENT_REPRO_BLOCKED: **{result.get('ENVIRONMENT_REPRO_BLOCKED', 'UNKNOWN')}**",
        f"- INNOVATION_1: **QTHS** (frozen rule; predefined alpha=0.25)",
        f"- INNOVATION_2: **AQTHS {'CONFIRMED' if aq_confirmed else ('REJECTED' if aq else 'NOT_RUN')}**",
        f"- MECHANISM_CLASS: **{mechanism}**",
        f"- NOVELTY_STATUS: **NO_EXACT_MATCH_IDENTIFIED_IN_FOCUSED_SEARCH** (not a priority claim)",
        f"- FINAL_DECISION: **{decision}**", "",
        "## Cora test", "",
    ]
    if cora_test:
        for method in ("C1_GRAPH_HARD", "C2_RANDOM_VETO", "C3_QTHS25"):
            if method not in cora_test:
                continue
            row = cora_test[method]
            lines.append(f"- {method}: {row['mean_mrr']:.6f} ± {row['sample_std_mrr']:.6f}; seeds=" +
                         ", ".join(f"{row['by_seed'][str(s)]['mrr']:.6f}" for s in SEEDS))
    lines += ["", "## Cross-dataset status", "",
              f"- Cora locked gate details: `{result.get('cora', {}).get('test', {}).get('locked_gate_details', {})}`.",
              f"- Citeseer: `{cite or 'NOT_RUN'}`.",
              f"- PubMed: `{pub.get('screen_status', pub.get('state', 'NOT_RUN'))}`; details in `03_PUBMED_SCREEN.md`.",
              f"- AQTHS Cora validation: `{aq.get('state', 'NOT_RUN')}`.",
              f"- AQTHS Cora test: `{aq.get('test', {}).get('state', 'NOT_RUN')}`.",
              f"- AQTHS Citeseer transfer: `{aq.get('citeseer', {}).get('state', 'NOT_RUN')}`.", "",
              f"NEXT_EXPECTED_STEP: {result['NEXT_EXPECTED_STEP']}", ""]
    (OUT / "FINAL_REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    env = ensure_expected_runtime()
    result = read_json(OUT / "results.json") if (OUT / "results.json").exists() else {}
    result["study"] = "QTHS V7.1: locked reproduction and adaptive trim"
    result["environment"] = env
    result["ENVIRONMENT_REPRO_BLOCKED"] = bool(env.get("environment_repro_blocked", False))
    result["source_code_sha256"] = file_hash(Path(__file__))
    if (OUT / "wheelhouse_sha256.json").exists():
        result["wheelhouse_manifest_sha256"] = file_hash(OUT / "wheelhouse_sha256.json")
    result["protocol"] = {
        "training_positive_exclusion": "STRICT_TRAIN_ONLY",
        "negative_count_per_positive": 1,
        "train_candidate_pool_size_per_positive": POOL_PER_POSITIVE,
        "fixed_epoch": EPOCHS, "checkpoint_rule": "FIXED_EPOCH_10",
        "qths_alpha": QTHS_ALPHA, "graph_teacher_frozen": True,
        "test_driven_tuning": False,
    }
    save_results(result)
    placeholders = {
        "02_CITESEER_FULL_RESULTS.md": "# Citeseer full results\n\nPending the Cora locked-reproduction gate.\n",
        "03_PUBMED_SCREEN.md": "# PubMed screen\n\nPending Cora and Citeseer gates.\n",
        "04_MECHANISM_CONTROLS.md": "# Mechanism controls\n\nPending the Cora locked-reproduction gate.\n",
    }
    for filename, content in placeholders.items():
        path = OUT / filename
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    aqths_readme = OUT / "A_AQTHS" / "README.md"
    if not aqths_readme.exists():
        aqths_readme.write_text("# AQTHS gated experiments\n\nTraining-pool-only assignments, validation gates and any authorized one-time test results are stored here.\n", encoding="utf-8")
    write_locked_reproduction(result)
    if "--preflight-only" in sys.argv:
        audit = preflight_audit()
        result["preflight"] = audit
        save_results(result)
        status("preflight_complete", None, preflight=audit["state"], test_evaluated=False)
        print(json.dumps(audit, indent=2, ensure_ascii=False), flush=True)
        return
    status("cora_locked_reproduction", "preflight", runtime=env)
    if not run_cora(result):
        result["aqths"] = {"state": "NOT_RUN_QTHS_REPRODUCTION_FAILURE", "test_evaluated": False}
        result["citeseer"] = {"state": "NOT_RUN_QTHS_REPRODUCTION_FAILURE"}
        result["pubmed"] = {"state": "NOT_RUN_QTHS_REPRODUCTION_FAILURE", "test_evaluated": False}
        write_novelty_search()
        write_locked_reproduction(result)
        write_final_report(result)
        status("complete", None, final_decision="REPRODUCTION_FAILURE",
               test_evaluated=bool(result.get("cora", {}).get("test_evaluated", False)))
        print("REPRODUCTION_FAILURE: Innovation 2 stopped by the preregistered gate", flush=True)
        return

    cite = run_citeseer(result)
    if not cite["transfer_assessment"]["fully_reverse"]:
        run_pubmed(result)
    else:
        result["pubmed"] = {"state": "SKIPPED_CITESEER_FULLY_REVERSE", "test_evaluated": False}
        (OUT / "03_PUBMED_SCREEN.md").write_text(
            "# PubMed screen\n\nSkipped under the preregistered rule because Citeseer validation and test were both fully reverse to Graph-hard.\n",
            encoding="utf-8",
        )
        save_results(result)
    run_mechanism_controls(result)
    aq = run_aqths_cora(result)
    if aq["GO"]:
        run_aqths_cora_test(result)
        if result.get("aqths", {}).get("test", {}).get("confirmed"):
            run_aqths_citeseer(result)
    else:
        result["aqths"]["test"] = {"state": "NOT_RUN_VALIDATION_GATE_CLOSED", "test_evaluated": False}
        result["aqths"]["citeseer"] = {"state": "NOT_RUN_AQTHS_TEST_NOT_CONFIRMED", "test_evaluated": False}
        save_results(result)
    write_novelty_search()
    write_locked_reproduction(result)
    write_final_report(result)
    decision = result["FINAL_DECISION"]
    status("complete", None, final_decision=decision,
           QTHS_LOCKED_REPRODUCTION=result["QTHS_LOCKED_REPRODUCTION"],
           INNOVATION_2_CONFIRMED=result["INNOVATION_2_CONFIRMED"],
           test_evaluated=bool(result.get("cora", {}).get("test_evaluated", False) or
                               result.get("citeseer", {}).get("test_evaluated", False) or
                               result.get("aqths", {}).get("test", {}).get("test_evaluated", False)))
    print(json.dumps({"state": "COMPLETE", "QTHS_LOCKED_REPRODUCTION": result["QTHS_LOCKED_REPRODUCTION"],
                      "CORA_TEST": result.get("cora", {}).get("test", {}).get("summary", {}).get("methods", {}),
                      "CITESEER": cite.get("transfer_assessment"), "PUBMED": result.get("pubmed", {}).get("screen_status", result.get("pubmed", {}).get("state")),
                      "MECHANISM_CLASS": result["MECHANISM_CLASS"],
                      "AQTHS": result.get("aqths", {}).get("state"),
                      "INNOVATION_2_CONFIRMED": result["INNOVATION_2_CONFIRMED"],
                      "FINAL_DECISION": decision}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        OUT.mkdir(parents=True, exist_ok=True)
        old = read_json(OUT / "status.json") if (OUT / "status.json").exists() else {}
        old.update({"state": "FAILED", "phase": old.get("phase", "unknown"),
                    "error": traceback.format_exc(),
                    "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        write_json(OUT / "status.json", old)
        raise
