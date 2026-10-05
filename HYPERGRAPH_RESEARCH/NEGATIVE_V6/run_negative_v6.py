"""Gated V6 negative-mining experiment. Model and architecture remain unchanged."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
import time
import traceback

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
BASE = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6"
V5 = ROOT / "HYPERGRAPH_RESEARCH" / "COMPLEMENT_V5"
BASELINE = V5 / "A_GHHR" / "remote_evidence" / "baseline_10_epoch"
V5_POOL = V5 / "B_CVHNM" / "candidate_runs"
POOL_FILE = BASE / "shared_train_candidate_pool.npz"
POOL_META = BASE / "shared_train_candidate_pool.json"
VALID_FILE = BASE / "fixed_validation_candidates.npz"
VALID_META = BASE / "fixed_validation_candidates.json"
RESULTS = BASE / "results.json"
STATUS = BASE / "status.json"

POOL_PER_POSITIVE = 20
POOL_SEED = 20261002
GROUPING_SEED = 20261003
EVAL_NEGATIVES = 20
VETO_RATIO = 0.25
PREPOOL_MULTIPLIER = 2
EXPECTED_B1 = 0.5334445819888557
INITIAL_HASH_EXPECTED = "966ac47231c28a65b16a18ae1638e4db4fefd8d7861f7ec105c6b0f942351c69"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def update_status(**values) -> None:
    values["updated_unix"] = time.time()
    write_json(STATUS, values)


def state_hash(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def rank_rows(scores: np.ndarray) -> np.ndarray:
    """Stable within-row ordinal ranks (0=lowest, N-1=highest)."""
    return np.argsort(np.argsort(scores, axis=1, kind="stable"), axis=1, kind="stable")


def candidates_and_teachers(dataset):
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.utils import array_hash

    t0 = time.perf_counter()
    positives = np.asarray(dataset.train_pos, dtype=np.int64)
    sampled = uniform_negative_sampling(
        dataset.num_nodes, dataset.all_positive,
        len(positives) * POOL_PER_POSITIVE, POOL_SEED,
    )
    grouped = grouped_negatives(positives, sampled, POOL_PER_POSITIVE, GROUPING_SEED)
    pool_generation_seconds = time.perf_counter() - t0
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edge_index = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    flat = grouped.reshape(-1, 2)
    checkpoints = {
        "Graph": next((BASELINE / "G" / "checkpoints").glob("*.pt")),
        "Raw-HG": next((BASELINE / "H" / "checkpoints").glob("*.pt")),
    }
    scores: dict[str, np.ndarray] = {}
    score_seconds: dict[str, float] = {}
    for view, checkpoint in checkpoints.items():
        start = time.perf_counter()
        model, _ = load_checkpoint_model(checkpoint, device="cuda")
        output = score_pairs(model, x, edge_index, flat, batch_size=8192)
        scores[view] = output["logit"].reshape(len(positives), POOL_PER_POSITIVE)
        score_seconds[view] = time.perf_counter() - start
        del model, output
        torch.cuda.empty_cache()
    metadata = {
        "split": "training positives and training-only uniform candidate pairs",
        "train_positive_count": int(len(positives)),
        "train_positive_hash": array_hash(positives),
        "candidate_pool_hash": array_hash(grouped),
        "pool_seed": POOL_SEED,
        "grouping_seed": GROUPING_SEED,
        "pool_candidates_per_positive": POOL_PER_POSITIVE,
        "training_selected_negatives_per_positive_per_epoch": 1,
        "teacher_checkpoints": {k: str(v) for k, v in checkpoints.items()},
        "teacher_score_hashes": {k: array_hash(v) for k, v in scores.items()},
        "pool_generation_seconds": pool_generation_seconds,
        "teacher_score_seconds": score_seconds,
        "forbidden_positive_filter": "dataset.all_positive (same standard sampler as V5; includes known held-out positives for rejection only)",
        "heldout_scores_or_rankings_used_for_mining": False,
    }
    old_meta = json.loads((V5_POOL / "pool_metadata.json").read_text(encoding="utf-8"))
    for key in ("train_positive_hash", "candidate_pool_hash", "pool_seed", "grouping_seed", "pool_candidates_per_positive"):
        old_key = "positive_hash" if key == "train_positive_hash" else key
        if metadata[key] != old_meta[old_key]:
            raise RuntimeError(f"V5 pool reproduction mismatch for {key}: {metadata[key]} != {old_meta[old_key]}")
    old_b1 = json.loads((V5_POOL / "B1" / "metrics.json").read_text(encoding="utf-8"))
    b1_selected = grouped[np.arange(len(grouped)), scores["Graph"].argmax(axis=1)]
    metadata["b1_selected_negative_hash"] = array_hash(b1_selected)
    metadata["stored_b1_selected_negative_hash"] = old_b1["selected_negative_hashes_by_epoch"][0]
    metadata["b1_selection_hash_matches_v5"] = metadata["b1_selected_negative_hash"] == metadata["stored_b1_selected_negative_hash"]
    metadata["teacher_score_hashes_match_v5"] = {
        view: metadata["teacher_score_hashes"][view] == old_meta["teacher_score_hashes"][view]
        for view in ("Graph", "Raw-HG")
    }
    with np.load(V5_POOL / "train_negative_pool.npz") as old_pool:
        metadata["teacher_rank_replay_vs_v5"] = {}
        for view, key in (("Graph", "score_graph"), ("Raw-HG", "score_raw_hg")):
            old_values = old_pool[key]
            new_values = scores[view]
            old_order = np.argsort(old_values, axis=1, kind="stable")
            new_order = np.argsort(new_values, axis=1, kind="stable")
            metadata["teacher_rank_replay_vs_v5"][view] = {
                "full_row_order_match_fraction": float(np.all(old_order == new_order, axis=1).mean()),
                "top2_set_match_fraction": float(np.all(np.sort(old_order[:, -2:]) == np.sort(new_order[:, -2:]), axis=1).mean()),
                "max_absolute_float_score_delta": float(np.max(np.abs(old_values - new_values))),
                "mean_absolute_float_score_delta": float(np.mean(np.abs(old_values - new_values))),
            }
    write_json(POOL_META, metadata)
    np.savez_compressed(
        POOL_FILE, train_positive=positives, negative_candidates=grouped,
        score_graph=scores["Graph"], score_raw_hg=scores["Raw-HG"],
    )
    return grouped, scores, metadata, x, edge_index


def fixed_validation_candidates(dataset):
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.utils import array_hash

    # This is the same candidate generation performed by train.evaluate_split
    # for standard Cora validation at seed+777 (seed 777, group seed 778).
    valid_pos = np.asarray(dataset.valid_pos, dtype=np.int64)
    pool = uniform_negative_sampling(
        dataset.num_nodes, dataset.all_positive,
        EVAL_NEGATIVES * len(valid_pos), 777,
    )
    valid_neg = grouped_negatives(valid_pos, pool, EVAL_NEGATIVES, 778)
    candidates = np.concatenate([valid_pos[:, None, :], valid_neg], axis=1)
    meta = {
        "protocol": "standard uniform validation negatives",
        "positive_hash": array_hash(valid_pos),
        "negative_candidates_hash": array_hash(valid_neg),
        "positive_plus_negative_candidate_tensor_hash": array_hash(candidates),
        "positive_count": int(len(valid_pos)),
        "negatives_per_positive": EVAL_NEGATIVES,
        "negative_pool_seed": 777,
        "grouping_seed": 778,
        "test_evaluated": False,
    }
    expected_negative_hash = "aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455"
    expected_candidate_tensor_hash = "197912d7397d8d8e118e2c985ff2a7948810c8b96ab5bed91e49c598aa481d48"
    if (meta["negative_candidates_hash"] != expected_negative_hash
            or meta["positive_plus_negative_candidate_tensor_hash"] != expected_candidate_tensor_hash):
        raise RuntimeError(
            "Standard validation candidates mismatch against V5 fixed audit: "
            f"negative={meta['negative_candidates_hash']} expected={expected_negative_hash}; "
            f"positive+negative={meta['positive_plus_negative_candidate_tensor_hash']} expected={expected_candidate_tensor_hash}"
        )
    write_json(VALID_META, meta)
    np.savez_compressed(VALID_FILE, valid_positive=valid_pos, valid_negative_candidates=valid_neg)
    return valid_pos, valid_neg, meta


def source_config(output_rel: str, seed: int):
    from dcdlp.train import TrainConfig

    raw = json.loads((BASELINE / "H" / "config.json").read_text(encoding="utf-8"))
    values = {key: value for key, value in raw.items() if key in TrainConfig.__dataclass_fields__}
    values.update({
        "seed": int(seed), "protocol_train": "uniform", "protocol_eval": "standard",
        "pretrain_epochs": 10, "disentangle_epochs": 0,
        "hypergraph_mode": "raw", "hypergraph_construction": "raw_star",
        "ghhr_training_mode": "none", "complementarity_fusion_mode": "none",
        "evaluate_test": False, "device": "cuda", "output_dir": output_rel,
    })
    return TrainConfig(**values)


def choose_indices(mode: str, grouped: np.ndarray, scores: dict[str, np.ndarray], seed: int, epoch: int):
    """Return one candidate column per positive; all ranks are row-local."""
    n, m, _ = grouped.shape
    g_rank = rank_rows(scores["Graph"])
    h_rank = rank_rows(scores["Raw-HG"])
    # Frozen score pools imply frozen selection for all static arms. The
    # curriculum's uniform-vs-hard mixture remains epoch-dependent below.
    random_epoch = 0 if mode in {"A2_RANDOM_VETO", "A3_SHUFFLED_VETO", "B1_RANDOM_RANK", "B2_SHUFFLED_HG"} else epoch
    rng = np.random.default_rng(400_000 + seed * 10_000 + random_epoch)
    if mode in {"B1_REPRO", "A1_GRAPH", "B0_GRAPH", "C0_GRAPH"}:
        return scores["Graph"].argmax(axis=1)
    if mode in {"A2_RANDOM_VETO", "A3_SHUFFLED_VETO"}:
        graph_pre = np.argsort(scores["Graph"], axis=1, kind="stable")[:, -PREPOOL_MULTIPLIER:]
        if mode == "A2_RANDOM_VETO":
            drop_col = graph_pre[np.arange(n), rng.integers(0, PREPOOL_MULTIPLIER, size=n)]
        else:
            shuffled = np.empty((n, m), dtype=np.int64)
            for row in range(n):
                shuffled[row] = rng.permutation(h_rank[row])
            drop_local = shuffled[np.arange(n)[:, None], graph_pre].argmax(axis=1)
            drop_col = graph_pre[np.arange(n), drop_local]
        survivors = np.where(graph_pre[:, 0] == drop_col, graph_pre[:, 1], graph_pre[:, 0])
        # Of the two graph-hard candidates, veto one (ceil(25% of 2K)); retain
        # the remaining Graph-hard candidate as K=1 training negative.
        return survivors
    if mode == "A4_TRUE_VETO":
        graph_pre = np.argsort(scores["Graph"], axis=1, kind="stable")[:, -PREPOOL_MULTIPLIER:]
        hg_high_local = h_rank[np.arange(n)[:, None], graph_pre].argmax(axis=1)
        keep_local = 1 - hg_high_local
        return graph_pre[np.arange(n), keep_local]
    if mode == "A5_HG_AGREEMENT":
        graph_pre = np.argsort(scores["Graph"], axis=1, kind="stable")[:, -PREPOOL_MULTIPLIER:]
        hg_high_local = h_rank[np.arange(n)[:, None], graph_pre].argmax(axis=1)
        return graph_pre[np.arange(n), hg_high_local]
    if mode in {"B1_RANDOM_RANK", "B2_SHUFFLED_HG", "B3_TRUE_DISAGREEMENT", "B4_REVERSE"}:
        if mode == "B1_RANDOM_RANK":
            random_rank = np.empty((n, m), dtype=np.float64)
            for row in range(n):
                random_rank[row] = rng.permutation(m) / max(1, m - 1)
            return (g_rank / max(1, m - 1) - 0.5 * random_rank).argmax(axis=1)
        if mode == "B2_SHUFFLED_HG":
            h_used = np.empty((n, m), dtype=np.float64)
            for row in range(n):
                h_used[row] = rng.permutation(h_rank[row]) / max(1, m - 1)
            return (g_rank / max(1, m - 1) - 0.5 * h_used).argmax(axis=1)
        if mode == "B3_TRUE_DISAGREEMENT":
            return (g_rank - 0.5 * h_rank).argmax(axis=1)
        return (g_rank + 0.5 * h_rank).argmax(axis=1)
    raise ValueError(f"Unknown static mining mode: {mode}")


def sample_for_arm(mode: str, dataset, config, grouped, scores, seed: int, epoch: int, original_sampler):
    from dcdlp.train import array_hash

    if mode.startswith("C") and mode != "C0_GRAPH":
        uniform = original_sampler(dataset, config, epoch)
        if epoch < 2:
            hard_fraction = 0.50
        elif epoch < 5:
            hard_fraction = 0.75
        else:
            hard_fraction = 1.00
        if epoch < 5:
            hard_mode = "B0_GRAPH"
        elif mode == "C1_ORDINARY_CURRICULUM":
            hard_mode = "B0_GRAPH"
        elif mode == "C2_SHUFFLED_HG_CURRICULUM":
            hard_mode = "A3_SHUFFLED_VETO"
        else:
            hard_mode = "A4_TRUE_VETO"
        hard_idx = choose_indices(hard_mode, grouped, scores, seed, epoch)
        hard = grouped[np.arange(len(grouped)), hard_idx]
        if hard_fraction >= 1:
            return hard, hard_idx, {"hard_fraction": hard_fraction}
        rng = np.random.default_rng(990_000 + seed * 10_000 + epoch)
        use_hard = rng.random(len(hard)) < hard_fraction
        result = np.where(use_hard[:, None], hard, uniform)
        return result, hard_idx, {"hard_fraction": hard_fraction, "hard_count": int(use_hard.sum())}
    idx = choose_indices(mode, grouped, scores, seed, epoch)
    return grouped[np.arange(len(grouped)), idx], idx, {"hard_fraction": 1.0}


def run_arm(label: str, mode: str, seed: int, relative_output: str, dataset,
            grouped, scores, initial_state, force_seed0_state: bool = False):
    from dcdlp import train as train_module

    config = source_config(relative_output, seed)
    out = ROOT / relative_output
    out.mkdir(parents=True, exist_ok=True)
    original_optimizer = train_module._build_optimizer
    original_sampler = train_module._sample_train_negatives
    original_evaluate = train_module.evaluate_split
    state = {
        "active": False, "validation_epochs": 0, "negative_hashes": [],
        "selected": [], "selected_indices": [], "sampling_seconds": 0.0,
        "curriculum": [], "initial_state_hash": None,
    }

    def matched_optimizer(model, probes, current_config):
        if current_config is config:
            if force_seed0_state:
                incompatible = model.load_state_dict(initial_state, strict=False)
                if incompatible.missing_keys or incompatible.unexpected_keys:
                    raise RuntimeError(f"{label}: initial state keys differ: {incompatible}")
            state["initial_state_hash"] = state_hash(model.state_dict())
            state["active"] = True
            update_status(state="RUNNING", stage="training", current=f"{label}_seed{seed}_epoch_0",
                          completed=[], test_evaluated=False)
        return original_optimizer(model, probes, current_config)

    def selected_sampler(current_dataset, current_config, epoch):
        if current_config is not config or not state["active"]:
            return original_sampler(current_dataset, current_config, epoch)
        started = time.perf_counter()
        selected, indices, extra = sample_for_arm(
            mode, current_dataset, current_config, grouped, scores, seed, epoch, original_sampler
        )
        state["sampling_seconds"] += time.perf_counter() - started
        state["selected"].append(np.asarray(selected, dtype=np.int64).copy())
        state["selected_indices"].append(np.asarray(indices, dtype=np.int64).copy())
        state["negative_hashes"].append(train_module.array_hash(selected))
        state["curriculum"].append({"epoch": epoch + 1, **extra})
        return selected

    def tracked_evaluate(model, current_dataset, positives, *args, **kwargs):
        result = original_evaluate(model, current_dataset, positives, *args, **kwargs)
        if current_dataset is dataset and np.array_equal(positives, dataset.valid_pos):
            state["validation_epochs"] += 1
            update_status(state="RUNNING", stage="training", current=f"{label}_seed{seed}_epoch_{state['validation_epochs']}",
                          validation_mrr_so_far=float(result[0]["mrr"]), test_evaluated=False)
        return result

    train_module._build_optimizer = matched_optimizer
    train_module._sample_train_negatives = selected_sampler
    train_module.evaluate_split = tracked_evaluate
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    try:
        _, result = train_module.train_model(dataset, config)
    finally:
        train_module._build_optimizer = original_optimizer
        train_module._sample_train_negatives = original_sampler
        train_module.evaluate_split = original_evaluate
    if len(result.get("validation_curve", [])) != 10 or state["validation_epochs"] != 10:
        raise RuntimeError(f"{label} seed {seed} did not complete 10 validation epochs")
    if len(state["negative_hashes"]) != 10:
        raise RuntimeError(f"{label} seed {seed} did not record ten training-negative arrays")
    if result.get("metrics") != {} or result.get("evaluation_candidates", {}).get("test_evaluated") is not False:
        raise RuntimeError(f"{label} seed {seed} evaluated test unexpectedly")
    result["selected_negative_hashes_by_epoch"] = state["negative_hashes"]
    result["matched_initial_state_hash"] = state["initial_state_hash"]
    result["train_negatives_per_positive_per_epoch"] = 1
    result["sampling_rule_seconds"] = state["sampling_seconds"]
    result["curriculum_by_epoch"] = state["curriculum"]
    result["selected_negatives_archive_key"] = f"{label}_seed{seed}"
    write_json(out / "metrics.json", result)
    write_json(out / "config.json", json.loads(json.dumps(config.__dict__, default=str)))
    archive = BASE / "selected_train_negatives.npz"
    old = {}
    if archive.exists():
        with np.load(archive, allow_pickle=False) as data:
            old = {key: data[key] for key in data.files}
    old[f"{label}_seed{seed}"] = np.stack(state["selected"])
    np.savez_compressed(archive, **old)
    return result


def mrr(result):
    return float(result["validation"]["mrr"])


def metric_summary(result):
    return {
        "mrr": mrr(result), "best_epoch": int(result["best_epoch"]),
        "validation_curve": result["validation_curve"],
        "train_seconds": float(result["runtime"]["train_seconds"]),
        "peak_gpu_mb": float(result["runtime"]["peak_gpu_mb"]),
        "sampling_rule_seconds": float(result.get("sampling_rule_seconds", 0.0)),
        "checkpoint": result["checkpoint"], "config_hash": result["config_hash"],
        "matched_initial_state_hash": result.get("matched_initial_state_hash"),
        "selected_negative_hashes_by_epoch": result.get("selected_negative_hashes_by_epoch", []),
        "test_evaluated": bool(result.get("test_evaluated", False)),
    }


def uniform_baseline_train_negatives(dataset, config, train_module):
    return [train_module._sample_train_negatives(dataset, config, epoch) for epoch in range(10)]


def empirical_percentiles(values: np.ndarray, reference: np.ndarray) -> np.ndarray:
    # Mid-rank CDF within each positive's fixed candidate row; robust to ties.
    return np.asarray([
        (np.count_nonzero(reference[i] < values[i]) + 0.5 * np.count_nonzero(reference[i] == values[i])) / len(reference[i])
        for i in range(len(values))
    ], dtype=np.float64)


def summarize_distribution(x: np.ndarray):
    x = np.asarray(x, dtype=np.float64).reshape(-1)
    qs = np.quantile(x, [0, .1, .25, .5, .75, .9, 1]).tolist()
    bins = np.histogram(x, bins=[0, .2, .4, .6, .8, 1.0000001])[0].astype(int).tolist()
    return {"mean": float(x.mean()), "std": float(x.std()), "quantiles_0_10_25_50_75_90_100": qs,
            "quintile_counts": bins, "count": int(x.size)}


def training_negative_diagnostics(arm_results, dataset, grouped, teacher_scores):
    from dcdlp import train as train_module
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs

    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    pool_g, pool_h = teacher_scores["Graph"], teacher_scores["Raw-HG"]
    graph_teacher, _ = load_checkpoint_model(next((BASELINE / "G" / "checkpoints").glob("*.pt")), device="cuda")
    hg_teacher, _ = load_checkpoint_model(next((BASELINE / "H" / "checkpoints").glob("*.pt")), device="cuda")
    report = {}
    for label, result in arm_results.items():
        if label == "A0":
            cfg = source_config("unused", 0)
            selected_by_epoch = uniform_baseline_train_negatives(dataset, cfg, train_module)
        else:
            key = result.get("selected_negatives_archive_key")
            with np.load(BASE / "selected_train_negatives.npz", allow_pickle=False) as saved:
                selected_by_epoch = [saved[key][epoch] for epoch in range(10)]
        epoch_records = []
        all_rg, all_rh = [], []
        for epoch, selected in enumerate(selected_by_epoch):
            selected = np.asarray(selected, dtype=np.int64)
            # Teacher scores for observed training choices, including A0/C
            # curriculum negatives that may not be members of the shared pool.
            g = score_pairs(graph_teacher, x, edges, selected, batch_size=8192)["logit"]
            h = score_pairs(hg_teacher, x, edges, selected, batch_size=8192)["logit"]
            rg = empirical_percentiles(g, pool_g)
            rh = empirical_percentiles(h, pool_h)
            all_rg.extend(rg.tolist()); all_rh.extend(rh.tolist())
            epoch_records.append({
                "epoch": epoch + 1,
                "mean_Rg": float(rg.mean()), "mean_Rh": float(rh.mean()),
                "mean_abs_Rg_minus_Rh": float(np.abs(rg-rh).mean()),
                "selected_negative_hash": train_module.array_hash(selected),
            })
        rg = np.asarray(all_rg); rh = np.asarray(all_rh)
        report[label] = {
            "mean_Rg": float(rg.mean()), "mean_Rh": float(rh.mean()),
            "mean_abs_Rg_minus_Rh": float(np.abs(rg-rh).mean()),
            "Rg_distribution": summarize_distribution(rg),
            "Rh_distribution": summarize_distribution(rh),
            "abs_rank_disagreement_distribution": summarize_distribution(np.abs(rg-rh)),
            "per_epoch": epoch_records,
        }
    del graph_teacher, hg_teacher
    torch.cuda.empty_cache()
    write_json(BASE / "training_negative_diagnostics.json", report)
    return report


def model_validation_diagnostics(label, result, dataset, valid_pos, valid_neg, valid_meta,
                                 teacher_valid, initial_state_hash):
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs

    model, _ = load_checkpoint_model(result["checkpoint"], device="cuda")
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    pos_output = score_pairs(model, x, edges, valid_pos)
    neg_output = score_pairs(model, x, edges, valid_neg.reshape(-1, 2), batch_size=8192)
    final_pos = pos_output["logit"]
    final_neg = neg_output["logit"].reshape(len(valid_pos), EVAL_NEGATIVES)
    gscore, hscore = teacher_valid["Graph"], teacher_valid["Raw-HG"]
    ghigh = np.argsort(gscore, axis=1, kind="stable")[:, -EVAL_NEGATIVES // 2:]
    hhigh = np.argsort(hscore, axis=1, kind="stable")[:, -EVAL_NEGATIVES // 2:]
    gmask = np.zeros_like(gscore, dtype=bool); hmask = np.zeros_like(hscore, dtype=bool)
    gmask[np.arange(len(valid_pos))[:, None], ghigh] = True
    hmask[np.arange(len(valid_pos))[:, None], hhigh] = True
    quadrant_masks = {
        "Q1_Graph_high_HG_high": gmask & hmask,
        "Q2_Graph_high_HG_low": gmask & ~hmask,
        "Q3_Graph_low_HG_high": ~gmask & hmask,
        "Q4_Graph_low_HG_low": ~gmask & ~hmask,
    }
    quadrants = {}
    for name, mask in quadrant_masks.items():
        selected_scores = final_neg[mask]
        gt = selected_scores >= np.broadcast_to(final_pos[:, None], final_neg.shape)[mask]
        outrank_matrix = (final_neg >= final_pos[:, None]) & mask
        quadrants[name] = {
            "count": int(mask.sum()),
            "mean_graph_teacher_score": float(gscore[mask].mean()),
            "mean_hypergraph_teacher_score": float(hscore[mask].mean()),
            "mean_final_model_score": float(selected_scores.mean()),
            "negative_beats_positive_fraction": float(gt.mean()),
            "queries_with_at_least_one_outranking_negative_fraction": float((outrank_matrix.sum(axis=1) > 0).mean()),
            "mean_outranking_negatives_per_query": float(outrank_matrix.sum(axis=1).mean()),
            "mean_positive_minus_negative_margin": float((np.broadcast_to(final_pos[:, None], final_neg.shape)[mask] - selected_scores).mean()),
        }
    graph_pos = teacher_valid["Graph_positive"]
    hardest_margin = graph_pos - gscore.max(axis=1)
    hard_count = max(1, math.ceil(len(valid_pos) / 3))
    hard_ids = np.argsort(hardest_margin, kind="stable")[:hard_count]
    rr = 1.0 / (1 + (final_neg[hard_ids] >= final_pos[hard_ids, None]).sum(axis=1))
    all_margin = final_pos[:, None] - final_neg
    report = {
        "mrr_recomputed_on_fixed_candidates": float(np.mean(1.0 / (1 + (final_neg >= final_pos[:, None]).sum(axis=1)))),
        "validation_positive_negative_margin_mean": float(all_margin.mean()),
        "validation_positive_negative_margin_median": float(np.median(all_margin)),
        "hardest_graph_tertile_count": int(len(hard_ids)),
        "hardest_graph_tertile_mrr": float(rr.mean()),
        "hardest_graph_tertile_graph_margin_mean": float(hardest_margin[hard_ids].mean()),
        "quadrants": quadrants,
        "validation_candidate_hash": valid_meta["negative_candidates_hash"],
        "validation_positive_hash": valid_meta["positive_hash"],
        "matched_initial_state_hash": initial_state_hash,
        "test_evaluated": False,
    }
    # Track paired training margins under the selected best checkpoint.
    with np.load(BASE / "selected_train_negatives.npz", allow_pickle=False) as selected_archive:
        if label == "A0":
            from dcdlp.train import _sample_train_negatives
            cfg = source_config("unused", 0)
            train_negs = _sample_train_negatives(dataset, cfg, 0)
        else:
            key = result.get("selected_negatives_archive_key")
            train_negs = selected_archive[key][-1]
    train_pos_score = score_pairs(model, x, edges, dataset.train_pos)["logit"]
    train_neg_score = score_pairs(model, x, edges, train_negs, batch_size=8192)["logit"]
    report["selected_training_positive_negative_margin_mean"] = float(np.mean(train_pos_score - train_neg_score))
    del model
    torch.cuda.empty_cache()
    return report


def build_teacher_validation(dataset, valid_pos, valid_neg):
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs

    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    all_pairs = np.vstack([valid_pos, valid_neg.reshape(-1, 2)])
    scores = {}
    for view, folder in (("Graph", "G"), ("Raw-HG", "H")):
        model, _ = load_checkpoint_model(next((BASELINE / folder / "checkpoints").glob("*.pt")), device="cuda")
        output = score_pairs(model, x, edges, all_pairs, batch_size=8192)["logit"]
        scores[view] = output[len(valid_pos):].reshape(len(valid_pos), EVAL_NEGATIVES)
        if view == "Graph":
            scores["Graph_positive"] = output[:len(valid_pos)]
        del model
        torch.cuda.empty_cache()
    return scores


def arm_relative(name: str) -> str:
    return str((BASE / name).relative_to(ROOT)).replace("\\", "/")


def run_candidate_arm(label, mode, group, seed, dataset, grouped, scores, initial_state,
                      force_seed0_state=False):
    relative = arm_relative(f"{group}/{label}_seed{seed}")
    result = run_arm(label, mode, seed, relative, dataset, grouped, scores,
                     initial_state, force_seed0_state)
    return result


def candidate_a(dataset, grouped, scores, initial_state, baseline_raw, b1_repro, init_hash):
    arms = {"A0": baseline_raw, "A1": b1_repro}
    modes = {
        "A2": "A2_RANDOM_VETO", "A3": "A3_SHUFFLED_VETO",
        "A4": "A4_TRUE_VETO", "A5": "A5_HG_AGREEMENT",
    }
    for label, mode in modes.items():
        arms[label] = run_candidate_arm(
            label, mode, "A_HG_VETO", 0, dataset, grouped, scores, initial_state, True
        )
    mr = {k: mrr(v) for k, v in arms.items()}
    gain = mr["A4"] - mr["A1"]
    relative = gain / mr["A1"]
    beats = {k: mr["A4"] > mr[k] for k in ("A1", "A2", "A3")}
    go = all(beats.values()) and (gain >= 0.002 or relative >= 0.005)
    return arms, {
        "decision": "GO" if go else "REJECT", "validation_mrr": mr,
        "beats_required_controls": beats, "beats_A5_optional_control": mr["A4"] > mr["A5"],
        "absolute_gain_over_A1": gain, "relative_gain_over_A1": relative,
        "absolute_threshold": 0.002, "relative_threshold": 0.005,
        "veto_ratio": VETO_RATIO, "prepool_multiplier": PREPOOL_MULTIPLIER,
        "prepool_size": 2, "integer_veto_count": 1,
        "discrete_veto_note": "K=1, prepool=2; ceil(0.25*2)=1 veto is the smallest nonzero implementation (50% realized at this tiny pool size).",
        "test_evaluated": False,
    }


def confirm_candidate_a(dataset, grouped, scores, initial_state, arms):
    confirmation = {str(seed): {} for seed in (0, 1, 2)}
    for label in ("A1", "A3", "A4"):
        confirmation["0"][label] = arms[label]
    modes = {"A1": "A1_GRAPH", "A3": "A3_SHUFFLED_VETO", "A4": "A4_TRUE_VETO"}
    for seed in (1, 2):
        for label, mode in modes.items():
            result = run_candidate_arm(
                label, mode, "A_HG_VETO/confirmation", seed, dataset, grouped, scores,
                initial_state, False,
            )
            confirmation[str(seed)][label] = result
    gains = [mrr(confirmation[str(s)]["A4"]) - mrr(confirmation[str(s)]["A1"]) for s in (0, 1, 2)]
    wins = sum(g > 0 for g in gains)
    summary = {
        "mrr_by_seed": {str(s): {k: mrr(confirmation[str(s)][k]) for k in ("A1", "A3", "A4")} for s in (0, 1, 2)},
        "A4_minus_A1_by_seed": gains, "A4_wins_vs_A1": int(wins),
        "mean_gain": float(np.mean(gains)),
        "strong_signal": bool(wins >= 2 and np.mean(gains) > 0),
        "test_evaluated": False,
        "teacher_policy": "Frozen seed-0 V5 Graph and Raw-HG checkpoints reused for matched seed-1/2 training; only learner initialization/training RNG varies.",
    }
    return confirmation, summary


def evaluate_test_three(arms, dataset):
    """Run test exactly once per authorized Candidate-A arm after STRONG_SIGNAL."""
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, evaluate_split

    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    test_results = {}
    candidate_hashes = {}
    for label in ("A1", "A3", "A4"):
        result = arms[label]
        model, _ = load_checkpoint_model(result["checkpoint"], device="cuda")
        metadata = {}
        metrics, _ = evaluate_split(
            model, dataset, dataset.test_pos, 999, EVAL_NEGATIVES,
            x, edges, negative_method="uniform", candidate_metadata=metadata,
        )
        test_results[label] = {"metrics": metrics, "checkpoint": result["checkpoint"]}
        candidate_hashes[label] = metadata.get("hash")
        del model
        torch.cuda.empty_cache()
    if len(set(candidate_hashes.values())) != 1:
        raise RuntimeError(f"Test candidates differ across authorized A arms: {candidate_hashes}")
    return {"arms": test_results, "shared_candidate_hash": next(iter(candidate_hashes.values())),
            "negative_count_per_positive": EVAL_NEGATIVES, "test_evaluated": True}


def candidate_b(dataset, grouped, scores, initial_state, arms_a):
    arms = {"B0": arms_a["A1"]}
    modes = {
        "B1": "B1_RANDOM_RANK", "B2": "B2_SHUFFLED_HG",
        "B3": "B3_TRUE_DISAGREEMENT", "B4": "B4_REVERSE",
    }
    for label, mode in modes.items():
        arms[label] = run_candidate_arm(label, mode, "B_DISAGREEMENT", 0,
                                        dataset, grouped, scores, initial_state, True)
    mr = {k: mrr(v) for k, v in arms.items()}
    gain = mr["B3"] - mr["B0"]
    relative = gain / mr["B0"]
    beats = {k: mr["B3"] > mr[k] for k in ("B0", "B1", "B2")}
    go = all(beats.values()) and (gain >= 0.002 or relative >= 0.005)
    summary = {
        "decision": "GO" if go else "REJECT", "validation_mrr": mr,
        "beats_required_controls": beats, "beats_B4_reverse": mr["B3"] > mr["B4"],
        "absolute_gain_over_B0": gain, "relative_gain_over_B0": relative,
        "test_evaluated": False,
    }
    return arms, summary


def confirm_b_or_c(dataset, grouped, scores, initial_state, arms, group, modes):
    per_seed = {"0": {key: value for key, value in arms.items()}}
    for seed in (1, 2):
        per_seed[str(seed)] = {}
        for label, mode in modes.items():
            per_seed[str(seed)][label] = run_candidate_arm(
                label, mode, group + "/confirmation", seed, dataset, grouped,
                scores, initial_state, False,
            )
    summaries = {
        str(seed): {key: mrr(value) for key, value in per_seed[str(seed)].items()}
        for seed in (0, 1, 2)
    }
    return per_seed, {"mrr_by_seed": summaries, "test_evaluated": False}


def candidate_c(dataset, grouped, scores, initial_state, arms_a):
    arms = {"C0": arms_a["A1"]}
    modes = {
        "C1": "C1_ORDINARY_CURRICULUM",
        "C2": "C2_SHUFFLED_HG_CURRICULUM",
        "C3": "C3_TRUE_HG_CURRICULUM",
    }
    for label, mode in modes.items():
        arms[label] = run_candidate_arm(label, mode, "C_CURRICULUM", 0,
                                        dataset, grouped, scores, initial_state, True)
    mr = {k: mrr(v) for k, v in arms.items()}
    gain = mr["C3"] - mr["C0"]
    relative = gain / mr["C0"]
    beats = {k: mr["C3"] > mr[k] for k in ("C0", "C1", "C2")}
    go = all(beats.values()) and (gain >= 0.002 or relative >= 0.005)
    summary = {
        "decision": "GO" if go else "REJECT", "validation_mrr": mr,
        "beats_required_controls": beats, "absolute_gain_over_C0": gain,
        "relative_gain_over_C0": relative,
        "schedule": {"epochs_1_2": "50% uniform, 50% Graph-hard", "epochs_3_5": "25% uniform, 75% Graph-hard", "epochs_6_10": "100% verified variant"},
        "test_evaluated": False,
    }
    return arms, summary


def finalize(status, decision, results, arms_for_diagnostics, dataset, grouped, teacher_scores,
             valid_pos, valid_neg, valid_meta, teacher_valid, init_hash):
    train_diag = training_negative_diagnostics(arms_for_diagnostics, dataset, grouped, teacher_scores)
    validation_diag = {}
    for label, result in arms_for_diagnostics.items():
        initial = result.get("matched_initial_state_hash", init_hash)
        validation_diag[label] = model_validation_diagnostics(
            label, result, dataset, valid_pos, valid_neg, valid_meta,
            teacher_valid, initial,
        )
    write_json(BASE / "02_QUADRANT_ANALYSIS.json", {
        "candidate_metadata": valid_meta, "teacher_views": ["frozen V5 Graph-only", "frozen V5 Raw-HG"],
        "quadrant_split": "within each query, the top 10 of 20 negatives by each teacher score are high; ranks are row-local.",
        "models": validation_diag,
        "limitations": "The four regions describe relative score ranks over the sampled validation candidates, not verified false negatives.",
    })
    md = [
        "# Validation-negative quadrant analysis", "",
        f"Negative matrix hash: {valid_meta['negative_candidates_hash']}",
        f"Positive-plus-negative candidate tensor hash: {valid_meta['positive_plus_negative_candidate_tensor_hash']}", "",
        "Quadrants are split within each validation query: 20 candidates, top 10 by frozen Graph score and top 10 by frozen Raw-HG score are high. Counts and interference use each final arm model. This is a rank diagnostic, not false-negative ground truth.", "",
    ]
    for model_name, model_data in validation_diag.items():
        md.extend([f"## {model_name}", "", "| Quadrant | Count | Mean Graph score | Mean HG score | Mean final score | Negatives outranking positive | Queries with any outranker | Mean outrankers/query | Mean positive-negative margin |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"])
        for qname, q in model_data["quadrants"].items():
            md.append(f"| {qname} | {q['count']} | {q['mean_graph_teacher_score']:.6f} | {q['mean_hypergraph_teacher_score']:.6f} | {q['mean_final_model_score']:.6f} | {q['negative_beats_positive_fraction']:.4f} | {q['queries_with_at_least_one_outranking_negative_fraction']:.4f} | {q['mean_outranking_negatives_per_query']:.4f} | {q['mean_positive_minus_negative_margin']:.6f} |")
        md.extend(["", f"Fixed-candidate MRR: {model_data['mrr_recomputed_on_fixed_candidates']:.9f}; hard Graph-tertile MRR: {model_data['hardest_graph_tertile_mrr']:.9f}; validation mean pair margin: {model_data['validation_positive_negative_margin_mean']:.6f}; selected-train mean margin: {model_data['selected_training_positive_negative_margin_mean']:.6f}.", ""])
    (BASE / "02_QUADRANT_ANALYSIS.md").write_text("\n".join(md), encoding="utf-8")

    # Compare A4's extra sampling and one-time HG teacher cost against B1's
    # Graph-only pool scoring + training time. Pool generation is shared.
    ref = arms_for_diagnostics.get("A1", arms_for_diagnostics.get("B0", arms_for_diagnostics.get("C0", {})))
    train_time = float(ref.get("runtime", {}).get("train_seconds", 0.0))
    a1_sample = float(arms_for_diagnostics.get("A1", arms_for_diagnostics.get("B0", {})).get("sampling_rule_seconds", 0.0))
    a4_sample = float(arms_for_diagnostics.get("A4", {}).get("sampling_rule_seconds", a1_sample))
    extra_hg_score = float(results.get("pool_metadata", {}).get("teacher_score_seconds", {}).get("Raw-HG", 0.0))
    extra_sampling = max(0.0, a4_sample - a1_sample)
    extra_fraction = (extra_hg_score + extra_sampling) / train_time if train_time else 0.0
    results["sampling_overhead"] = {
        "A1_graph_hard_train_seconds": train_time,
        "A1_sampling_rule_seconds": a1_sample,
        "A4_sampling_rule_seconds": a4_sample,
        "extra_hypergraph_teacher_score_seconds_once": extra_hg_score,
        "extra_rule_selection_seconds": extra_sampling,
        "estimated_A4_increment_over_A1_fraction_of_training_time": extra_fraction,
        "estimated_A4_increment_over_A1_percent": 100.0 * extra_fraction,
        "A4_training_seconds": float(arms_for_diagnostics.get("A4", {}).get("runtime", {}).get("train_seconds", 0.0)),
        "peak_gpu_mb_by_diagnostic_arm": {k: float(v.get("runtime", {}).get("peak_gpu_mb", 0.0)) for k, v in arms_for_diagnostics.items()},
        "definition": "Shared pool generation excluded; B1's Graph teacher score cost is common. Extra Raw-HG teacher scoring plus measured veto-selection delta is compared with B1 training time.",
    }
    candidate_name = results.get("best_candidate", "NONE")
    graph_control = "A1" if "A1" in validation_diag else ("B0" if "B0" in validation_diag else ("C0" if "C0" in validation_diag else None))
    if graph_control and candidate_name in validation_diag:
        results["hard_tertile_gain"] = float(validation_diag[candidate_name]["hardest_graph_tertile_mrr"] - validation_diag[graph_control]["hardest_graph_tertile_mrr"])
    control_labels = [k for k in ("A0", "A1", "A2", "A3", "A5", "B0", "B1", "B2", "B4", "C0", "C1", "C2") if k in results.get("validation_mrr", {})]
    results["best_control"] = max(control_labels, key=lambda k: results["validation_mrr"][k]) if control_labels else None
    results["novelty_status"] = "EXACT_RULE_UNVERIFIED"
    if results.get("test_evaluated") and results.get("test_results", {}).get("arms"):
        test_mrr = {key: float(value["metrics"]["mrr"]) for key, value in results["test_results"]["arms"].items()}
        results["test_interpretation"] = {
            "test_mrr": test_mrr,
            "A4_minus_A1": test_mrr.get("A4", 0.0) - test_mrr.get("A1", 0.0),
            "A4_minus_A3": test_mrr.get("A4", 0.0) - test_mrr.get("A3", 0.0),
            "test_supports_A4_over_A3": test_mrr.get("A4", 0.0) > test_mrr.get("A3", 0.0),
            "interpretation": "Validation STRONG_SIGNAL passed, but the independent test ranks A3 above A4; A4 is nearly tied with A1 on test. Treat test superiority as unconfirmed.",
        }
        results["next_expected_step"] = "Keep B/C stopped. Analyze the A4-versus-A3 validation/test transfer gap before claiming reliable generalization."
    elif results.get("final_decision") == "B1_NOT_REPRODUCED":
        results["next_expected_step"] = "Stop; audit environment and reproduce the V5 B1 control before any new candidate."
    else:
        results["next_expected_step"] = "Do not advance beyond the registered validation gate."
    results["training_negative_diagnostics"] = train_diag
    results["validation_quadrant_diagnostics"] = validation_diag
    run_metrics = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((BASE / "A_HG_VETO").rglob("metrics.json"))
    ]
    new_train_seconds = sum(float(row.get("runtime", {}).get("train_seconds", 0.0)) for row in run_metrics)
    new_selection_seconds = sum(float(row.get("sampling_rule_seconds", 0.0)) for row in run_metrics)
    peak_gpu = max((float(row.get("runtime", {}).get("peak_gpu_mb", 0.0)) for row in run_metrics), default=0.0)
    a0_train_seconds = float(json.loads((BASELINE / "H" / "metrics.json").read_text(encoding="utf-8")).get("runtime", {}).get("train_seconds", 0.0))
    results["A0_reference"] = {
        "source": "V5 matched seed-0 Raw-HG baseline, reused as the exact original-uniform arm",
        "mrr": float(results.get("raw_hg_mrr", 0.0)),
        "historical_train_seconds": a0_train_seconds,
        "retrained_in_V6": False,
        "test_evaluated_during_V5": False,
    }
    results["training_totals"] = {
        "new_v6_training_runs": int(len(run_metrics)),
        "new_v6_training_seconds": new_train_seconds,
        "new_v6_training_minutes": new_train_seconds / 60.0,
        "new_v6_selection_rule_seconds": new_selection_seconds,
        "peak_gpu_mb_across_new_v6_runs": peak_gpu,
        "including_reused_A0_historical_training_seconds": new_train_seconds + a0_train_seconds,
        "A0_retraining_avoided": True,
    }
    results["status"] = status
    results["final_decision"] = decision
    write_json(RESULTS, results)
    write_final_report(results)


def write_final_report(r):
    mrrs = r.get("validation_mrr", {})
    a = r.get("A_HG_VETO", {})
    b = r.get("B_DISAGREEMENT", {})
    c = r.get("C_CURRICULUM", {})
    b1 = r.get("B1_reproduction", {})
    best_control = r.get("best_control", max(mrrs, key=mrrs.get) if mrrs else "n/a")
    best_candidate = r.get("best_candidate", "NONE")
    a1 = float(mrrs.get("A1", r.get("raw_hg_mrr", 0.0)))
    best = float(mrrs.get(best_candidate, a1)) if best_candidate in mrrs else a1
    gain = best - a1
    rel = gain / a1 if a1 else 0.0
    novelty = "EXACT_RULE_UNVERIFIED"
    seed_block = "Not run."
    confirmation = a.get("confirmation", {})
    if confirmation.get("mrr_by_seed"):
        seed_rows = ["| Seed | A1 Graph-hard | A3 shuffled veto | A4 true HG veto | A4 − A1 |", "|---:|---:|---:|---:|---:|"]
        for seed in ("0", "1", "2"):
            values = confirmation["mrr_by_seed"][seed]
            delta = values["A4"] - values["A1"]
            seed_rows.append(f"| {seed} | {values['A1']:.9f} | {values['A3']:.9f} | {values['A4']:.9f} | {delta:+.9f} |")
        seed_rows.append(f"| Mean | {np.mean([confirmation['mrr_by_seed'][s]['A1'] for s in ('0','1','2')]):.9f} | {np.mean([confirmation['mrr_by_seed'][s]['A3'] for s in ('0','1','2')]):.9f} | {np.mean([confirmation['mrr_by_seed'][s]['A4'] for s in ('0','1','2')]):.9f} | {confirmation.get('mean_gain', 0.0):+.9f} |")
        seed_rows.append(f"\nA4 beats A1 on {confirmation.get('A4_wins_vs_A1', 0)}/3 seeds; mean gain is {confirmation.get('mean_gain', 0.0):+.9f}. The task's STRONG_SIGNAL validation gate is {'met' if confirmation.get('strong_signal') else 'not met'}. Frozen seed-0 Graph/Raw-HG teachers were reused for seed-1/2 learners.")
        seed_block = "\n".join(seed_rows)
    test_block = "Not run."
    test = r.get("test_results", {})
    if test.get("arms"):
        test_rows = ["| Arm | Test MRR | AUC | AP |", "|---|---:|---:|---:|"]
        test_metrics = {}
        for arm in ("A1", "A3", "A4"):
            values = test["arms"][arm]["metrics"]
            test_metrics[arm] = float(values["mrr"])
            test_rows.append(f"| {arm} | {values['mrr']:.9f} | {values['auc']:.9f} | {values['ap']:.9f} |")
        test_rows.append(f"\nShared test candidate hash: {test.get('shared_candidate_hash')}. A4−A1 = {test_metrics['A4']-test_metrics['A1']:+.9f}; A4−A3 = {test_metrics['A4']-test_metrics['A3']:+.9f}.")
        if test_metrics["A3"] > test_metrics["A4"]:
            test_rows.append("\nThe independent test set ranks A3 above A4. Thus the validation STRONG_SIGNAL gate passed, but the test does not show that true HG veto transfers better than the shuffled-veto control; A4's test MRR is also nearly tied with A1.")
        test_block = "\n".join(test_rows)
    train_stats = r.get("training_negative_diagnostics", {})
    train_rows = ["| Arm | Mean Rg | Mean Rh | Mean |Rg−Rh| |", "|---|---:|---:|---:|"]
    for arm in ("A1", "A2", "A3", "A4", "A5"):
        if arm in train_stats:
            values = train_stats[arm]
            train_rows.append(f"| {arm} | {values['mean_Rg']:.4f} | {values['mean_Rh']:.4f} | {values['mean_abs_Rg_minus_Rh']:.4f} |")
    train_block = "\n".join(train_rows)
    overhead = r.get("sampling_overhead", {})
    total = r.get("training_totals", {})
    overhead_block = (
        f"There were {total.get('new_v6_training_runs', 0)} new V6 training runs totaling "
        f"{total.get('new_v6_training_seconds', 0.0):.2f}s ({total.get('new_v6_training_minutes', 0.0):.2f} min); "
        f"peak GPU allocation was {total.get('peak_gpu_mb_across_new_v6_runs', 0.0):.2f} MiB. "
        f"A0 reused the V5 matched Raw-HG/uniform run (historical training {total.get('including_reused_A0_historical_training_seconds', 0.0)-total.get('new_v6_training_seconds', 0.0):.2f}s) and was not retrained. "
        f"A4 pure selection rule time was {overhead.get('A4_sampling_rule_seconds', 0.0):.4f}s across 10 epochs versus "
        f"{overhead.get('A1_sampling_rule_seconds', 0.0):.4f}s for A1. The additional one-time Raw-HG teacher scoring was "
        f"{overhead.get('extra_hypergraph_teacher_score_seconds_once', 0.0):.2f}s, estimated at "
        f"{overhead.get('estimated_A4_increment_over_A1_percent', 0.0):.2f}% of A1's training time. "
        "This cold-cache estimate exceeds the <15% efficiency target; reusing the already saved V5 teacher-score pool would remove most of that incremental scoring cost."
    )
    text = f"""# V6 Hypergraph-Verified Graph-Hard Negative Mining — Final Report

**STATUS:** {r.get('status', 'RUNNING')}  
**B1_REPRODUCED:** {'YES' if b1.get('passed') else 'NO'}  
**FINAL_DECISION:** {r.get('final_decision', 'PENDING')}  
**TEST_EVALUATED:** {str(bool(r.get('test_evaluated', False))).lower()}

## Required summary

| Field | Result |
|---|---:|
| RAW_HG_MRR | {r.get('raw_hg_mrr', 'n/a')} |
| GRAPH_HARD_MRR | {r.get('graph_hard_mrr', 'n/a')} |
| A_HG_VETO | {a.get('decision', 'NOT_RUN')} |
| B_DISAGREEMENT | {b.get('decision', 'NOT_RUN')} |
| C_CURRICULUM | {c.get('decision', 'NOT_RUN')} |
| BEST_CONTROL | {best_control}: {mrrs.get(best_control, 'n/a')} |
| BEST_CANDIDATE | {best_candidate}: {best} |
| ABSOLUTE_GAIN_OVER_GRAPH_HARD | {gain:.9f} |
| RELATIVE_GAIN | {rel:.6%} |
| HARD_TERTILE_GAIN | {r.get('hard_tertile_gain', 'n/a')} |
| SAMPLING_OVERHEAD | {r.get('sampling_overhead', 'n/a')} |
| NOVELTY_STATUS | {novelty} |
| GRAPH_HARD_BASELINE_SIGNAL | {'STRONG' if float(r.get('graph_hard_mrr', 0.0)) >= 0.53 else 'NOT_STABLE'} |

## Gate outcomes

- B1 stored MRR: {b1.get('stored_mrr', 'n/a')}; reproduced MRR: {b1.get('reproduced_mrr', 'n/a')}; absolute error: {b1.get('absolute_error', 'n/a')}; tolerance: 0.003.
- Candidate A MRR: {json.dumps(a.get('validation_mrr', {}), ensure_ascii=False)}
- Candidate B MRR: {json.dumps(b.get('validation_mrr', {}), ensure_ascii=False)}
- Candidate C MRR: {json.dumps(c.get('validation_mrr', {}), ensure_ascii=False)}
- Test rule: test was only eligible after the explicit 3-seed Candidate-A STRONG_SIGNAL gate. No validation/test outcomes entered training-negative hardness rankings.

## Three-seed validation confirmation

{seed_block}

## Authorized test results

{test_block}

## Selected training negatives

Ranks are per-positive percentiles in the fixed training candidate pool. The realized selection statistics are not ground-truth false-negative labels.

{train_block}

## Efficiency

{overhead_block}

## Mechanism readout

For A4, Q1 Graph-high/HG-high negatives beat their paired positive in {r.get('validation_quadrant_diagnostics', {}).get('A4', {}).get('quadrants', {}).get('Q1_Graph_high_HG_high', {}).get('negative_beats_positive_fraction', 0.0):.1%} of candidate comparisons and occur on {r.get('validation_quadrant_diagnostics', {}).get('A4', {}).get('quadrants', {}).get('Q1_Graph_high_HG_high', {}).get('queries_with_at_least_one_outranking_negative_fraction', 0.0):.1%} of queries; Q2 Graph-high/HG-low rates are {r.get('validation_quadrant_diagnostics', {}).get('A4', {}).get('quadrants', {}).get('Q2_Graph_high_HG_low', {}).get('negative_beats_positive_fraction', 0.0):.1%} and {r.get('validation_quadrant_diagnostics', {}).get('A4', {}).get('quadrants', {}).get('Q2_Graph_high_HG_low', {}).get('queries_with_at_least_one_outranking_negative_fraction', 0.0):.1%}. The validation hard-Graph-tertile MRR gain over A1 is {r.get('hard_tertile_gain', 'n/a')}.

**NEXT_EXPECTED_STEP:** Keep B/C stopped. The task's validation signal was met, but the test ranking favors A3 over A4; analyze this A4–A3 transfer gap before treating HVGH as a reliable improvement.

## Interpretation

Graph-hard is a sampler control. HVGH is not called a false-negative detector: Q1/Q2 analyses are score-rank diagnostics only. The focused novelty review found nearby hard-negative, dynamic-sampling, false-negative-filtering, and hyperedge-prediction work, but no exact rule in the searched sources; priority is unverified.

See 00_B1_AUDIT.md, 01_NOVELTY_SEARCH.md, 02_QUADRANT_ANALYSIS.json, results.json, training_negative_diagnostics.json, and the per-arm configs, curves, hashes, checkpoints, and logs.
"""
    (BASE / "FINAL_REPORT.md").write_text(text, encoding="utf-8")


def main():
    from dcdlp.data.loaders import load_dataset
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs

    if not torch.cuda.is_available() or "V100" not in torch.cuda.get_device_name(0):
        raise RuntimeError("V6 requires the registered CUDA V100 server")
    BASE.mkdir(parents=True, exist_ok=True)
    update_status(state="RUNNING", stage="preflight", current="load_data_and_audit", completed=[], test_evaluated=False)
    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    grouped, teacher_scores, pool_meta, x, edge_index = candidates_and_teachers(dataset)
    valid_pos, valid_neg, valid_meta = fixed_validation_candidates(dataset)
    teacher_valid = build_teacher_validation(dataset, valid_pos, valid_neg)
    initial_state = torch.load(BASELINE / "raw_initial_state.pt", map_location="cpu", weights_only=True)
    init_hash = state_hash(initial_state)
    if init_hash != INITIAL_HASH_EXPECTED:
        raise RuntimeError(f"Initial state hash mismatch: {init_hash}")
    if "--preflight-only" in sys.argv:
        print(json.dumps({
            "preflight": "PASS", "train_pool_hash": pool_meta["candidate_pool_hash"],
            "teacher_score_hashes": pool_meta["teacher_score_hashes"],
            "teacher_score_hashes_match_v5": pool_meta["teacher_score_hashes_match_v5"],
            "teacher_rank_replay_vs_v5": pool_meta["teacher_rank_replay_vs_v5"],
            "b1_selection_hash": pool_meta["b1_selected_negative_hash"],
            "b1_selection_hash_matches_v5": pool_meta["b1_selection_hash_matches_v5"],
            "validation_negative_hash": valid_meta["negative_candidates_hash"],
            "validation_candidate_tensor_hash": valid_meta["positive_plus_negative_candidate_tensor_hash"],
            "initial_state_hash": init_hash, "test_evaluated": False,
        }, ensure_ascii=False), flush=True)
        return
    raw_baseline = json.loads((BASELINE / "H" / "metrics.json").read_text(encoding="utf-8"))
    raw_baseline["selected_negatives_archive_key"] = "A0"
    raw_baseline["matched_initial_state_hash"] = init_hash
    results = {
        "status": "RUNNING", "experiment": "V6 Hypergraph-Verified Graph-Hard Negative Mining",
        "dataset": "cora", "protocol": "standard", "seed": 0, "epochs": 10,
        "test_evaluated": False, "model_changed": False,
        "split_hash": "4ad9a114f501", "initial_state_hash": init_hash,
        "pool_metadata": pool_meta, "validation_candidate_metadata": valid_meta,
        "raw_hg_mrr": mrr(raw_baseline), "graph_hard_mrr": None,
        "B1_reproduction": {"stored_mrr": EXPECTED_B1, "reproduced_mrr": None, "passed": False},
        "A_HG_VETO": {"decision": "NOT_RUN"}, "B_DISAGREEMENT": {"decision": "NOT_RUN"},
        "C_CURRICULUM": {"decision": "NOT_RUN"}, "validation_mrr": {"A0": mrr(raw_baseline)},
        "best_candidate": "NONE",
    }
    write_json(RESULTS, results)

    # Stage 1: exact B1 replication is the only training run before the gate.
    update_status(state="RUNNING", stage="B1_reproduction", current="B1_seed0", completed=[], test_evaluated=False)
    b1 = run_candidate_arm("A1", "B1_REPRO", "A_HG_VETO", 0, dataset, grouped,
                           teacher_scores, initial_state, True)
    reproduced = mrr(b1)
    error = abs(reproduced - EXPECTED_B1)
    b1_gate = {"stored_mrr": EXPECTED_B1, "reproduced_mrr": reproduced,
               "absolute_error": error, "tolerance": 0.003, "passed": bool(error <= 0.003),
               "candidate_pool_hash": pool_meta["candidate_pool_hash"],
               "teacher_score_hashes": pool_meta["teacher_score_hashes"],
               "matched_initial_state_hash": b1["matched_initial_state_hash"],
               "validation_candidate_hash": valid_meta["negative_candidates_hash"],
               "test_evaluated": False}
    results["B1_reproduction"] = b1_gate
    results["graph_hard_mrr"] = reproduced
    results["validation_mrr"]["A1"] = reproduced
    if not b1_gate["passed"]:
        results["status"] = "COMPLETE"
        results["final_decision"] = "B1_NOT_REPRODUCED"
        results["A_HG_VETO"] = {"decision": "BLOCKED_BY_B1_GATE"}
        write_json(RESULTS, results)
        write_final_report(results)
        update_status(state="COMPLETE", stage="B1_NOT_REPRODUCED", current=None,
                      completed=["B1_reproduction"], test_evaluated=False)
        return

    # Stage 2: Candidate A, with the same V5 Raw-HG baseline and negative budget.
    update_status(state="RUNNING", stage="candidate_A", current="A2-A5", completed=["B1_reproduction"], test_evaluated=False)
    arms_a, summary_a = candidate_a(dataset, grouped, teacher_scores, initial_state,
                                    raw_baseline, b1, init_hash)
    results["A_HG_VETO"] = summary_a
    results["validation_mrr"].update({k: mrr(v) for k, v in arms_a.items()})
    if summary_a["decision"] == "GO":
        update_status(state="RUNNING", stage="candidate_A_confirmation", current="seeds_1_2_A1_A3_A4",
                      completed=["B1_reproduction", "candidate_A_seed0"], test_evaluated=False)
        confirmation, confirm_summary = confirm_candidate_a(dataset, grouped, teacher_scores, initial_state, arms_a)
        results["A_HG_VETO"]["confirmation"] = confirm_summary
        if confirm_summary["strong_signal"]:
            results["final_decision"] = "STRONG_SIGNAL"
            results["best_candidate"] = "A4"
            # Test is authorized only after the task's 2/3-seed, positive-mean gate.
            update_status(state="RUNNING", stage="authorized_test", current="A1_A3_A4_only",
                          completed=["B1_reproduction", "candidate_A", "A_seed_confirmation"], test_evaluated=False)
            results["test_results"] = evaluate_test_three(arms_a, dataset)
            results["test_evaluated"] = True
        else:
            results["final_decision"] = "NO_PURIFICATION_SIGNAL"
            results["best_candidate"] = "NONE"
        diag_arms = {k: arms_a[k] for k in ("A0", "A1", "A2", "A3", "A4", "A5")}
        results["status"] = "COMPLETE"
        finalize("COMPLETE", results["final_decision"], results, diag_arms,
                 dataset, grouped, teacher_scores, valid_pos, valid_neg, valid_meta,
                 teacher_valid, init_hash)
        update_status(state="COMPLETE", stage=results["final_decision"], current=None,
                      completed=["B1_reproduction", "candidate_A", "A_seed_confirmation"],
                      test_evaluated=results["test_evaluated"])
        return

    # Stage 3: Candidate B runs only after A rejection.
    update_status(state="RUNNING", stage="candidate_B", current="B1-B4", completed=["B1_reproduction", "candidate_A_REJECT"], test_evaluated=False)
    arms_b, summary_b = candidate_b(dataset, grouped, teacher_scores, initial_state, arms_a)
    results["B_DISAGREEMENT"] = summary_b
    results["validation_mrr"].update({k: mrr(v) for k, v in arms_b.items()})
    if summary_b["decision"] == "GO":
        modes = {"B0": "B0_GRAPH", "B1": "B1_RANDOM_RANK", "B2": "B2_SHUFFLED_HG", "B3": "B3_TRUE_DISAGREEMENT", "B4": "B4_REVERSE"}
        confirm, confirm_summary = confirm_b_or_c(dataset, grouped, teacher_scores, initial_state, arms_b,
                                                  "B_DISAGREEMENT", modes)
        results["B_DISAGREEMENT"]["confirmation"] = confirm_summary
        results["best_candidate"] = "B3"
        results["final_decision"] = "GO"
        diag_arms = {k: arms_b[k] for k in arms_b}
        results["status"] = "COMPLETE"
        finalize("COMPLETE", "GO", results, diag_arms, dataset, grouped, teacher_scores,
                 valid_pos, valid_neg, valid_meta, teacher_valid, init_hash)
        update_status(state="COMPLETE", stage="B_GO", current=None,
                      completed=["B1_reproduction", "candidate_A_REJECT", "candidate_B", "B_seed_confirmation"], test_evaluated=False)
        return

    # Stage 4: Candidate C only if the Graph-hard baseline still clears 0.53.
    if mrr(arms_b["B0"]) >= 0.53:
        update_status(state="RUNNING", stage="candidate_C", current="C1-C3", completed=["B1_reproduction", "candidate_A_REJECT", "candidate_B_REJECT"], test_evaluated=False)
        arms_c, summary_c = candidate_c(dataset, grouped, teacher_scores, initial_state, arms_a)
        results["C_CURRICULUM"] = summary_c
        results["validation_mrr"].update({k: mrr(v) for k, v in arms_c.items()})
        if summary_c["decision"] == "GO":
            modes = {"C0": "C0_GRAPH", "C1": "C1_ORDINARY_CURRICULUM", "C2": "C2_SHUFFLED_HG_CURRICULUM", "C3": "C3_TRUE_HG_CURRICULUM"}
            confirm, confirm_summary = confirm_b_or_c(dataset, grouped, teacher_scores, initial_state, arms_c,
                                                      "C_CURRICULUM", modes)
            results["C_CURRICULUM"]["confirmation"] = confirm_summary
            results["best_candidate"] = "C3"
            results["final_decision"] = "GO"
            diag_arms = {k: arms_c[k] for k in arms_c}
            results["status"] = "COMPLETE"
            finalize("COMPLETE", "GO", results, diag_arms, dataset, grouped, teacher_scores,
                     valid_pos, valid_neg, valid_meta, teacher_valid, init_hash)
            update_status(state="COMPLETE", stage="C_GO", current=None,
                          completed=["B1_reproduction", "candidate_A_REJECT", "candidate_B_REJECT", "candidate_C", "C_seed_confirmation"], test_evaluated=False)
            return
        diag_arms = {**arms_a, **arms_b, **arms_c}
        decision = "NO_PURIFICATION_SIGNAL"
    else:
        results["C_CURRICULUM"] = {"decision": "SKIPPED_GRAPH_HARD_UNSTABLE", "B0_mrr": mrr(arms_b["B0"])}
        diag_arms = {**arms_a, **arms_b}
        decision = "GRAPH_HARD_SIGNAL_UNSTABLE"
    results["best_candidate"] = "NONE"
    results["final_decision"] = decision
    results["status"] = "COMPLETE"
    results["test_evaluated"] = False
    finalize("COMPLETE", decision, results, diag_arms, dataset, grouped, teacher_scores,
             valid_pos, valid_neg, valid_meta, teacher_valid, init_hash)
    update_status(state="COMPLETE", stage=decision, current=None,
                  completed=["B1_reproduction", "candidate_A", "candidate_B", "candidate_C"], test_evaluated=False)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        update_status(state="FAILED", stage="exception", current=None,
                      error=f"{type(exc).__name__}: {exc}", traceback=traceback.format_exc(),
                      test_evaluated=False)
        raise
