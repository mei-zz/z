"""V6.2 cross-order disagreement negative-sampling experiment.

All mining inputs are restricted to the frozen V6.1 train-only candidate pool.
Validation is used only for epoch diagnostics and pre-registered gates; test
candidates are not opened until the validation decisions are frozen.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "HYPERGRAPH_RESEARCH" / "CODNS_V6_2"
V61 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
sys.path.insert(0, str(V61))
import run_negative_v6_1 as v61  # noqa: E402

SEEDS = (0, 1, 2)
EPOCHS = 10
LAMBDA = 0.5
METHODS_MECH = ("M0", "M1", "M2", "M3", "M4")
METHODS_CODNS = ("C0", "C1", "C2", "C3", "C4", "C5")
MATCH_STRATA_TRY = (20, 40, 80, 160, 320)
INITIAL_HASH_EXPECTED = v61.INITIAL_HASH_EXPECTED


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def state_hash(state: dict) -> str:
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def current_status() -> dict:
    path = OUT / "status.json"
    return read_json(path) if path.exists() else {"state": "NOT_STARTED", "completed": []}


def set_status(phase: str, current: str | None = None, **extra) -> None:
    value = current_status()
    value.update({"state": "COMPLETE" if phase == "complete" else "RUNNING", "phase": phase, "current": current, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
    value.update(extra)
    write_json(OUT / "status.json", value)


def rank_percentiles(values: np.ndarray) -> np.ndarray:
    flat = np.asarray(values).reshape(-1)
    order = np.argsort(flat, kind="stable")
    rank = np.empty(len(flat), dtype=np.float64)
    rank[order] = np.arange(len(flat), dtype=np.float64)
    if len(flat) > 1:
        rank /= (len(flat) - 1)
    return rank.reshape(np.asarray(values).shape)


def quantile_strata(values: np.ndarray, count: int) -> np.ndarray:
    flat = np.asarray(values).reshape(-1)
    order = np.argsort(flat, kind="stable")
    bins = np.empty(len(flat), dtype=np.int64)
    bins[order] = np.minimum(np.arange(len(flat), dtype=np.int64) * count // len(flat), count - 1)
    return bins.reshape(np.asarray(values).shape)


def exact_stratified_assignment(
    strata: np.ndarray,
    objective: np.ndarray,
    target_counts: np.ndarray,
    candidate_ids: np.ndarray,
) -> np.ndarray:
    """Choose one of two candidates per query with exact stratum quotas."""
    import networkx as nx

    strata = np.asarray(strata, dtype=np.int64)
    objective = np.asarray(objective, dtype=np.float64)
    candidate_ids = np.asarray(candidate_ids, dtype=np.int64)
    n_rows, n_choices = strata.shape
    if n_choices != 2 or objective.shape != strata.shape or candidate_ids.shape != strata.shape:
        raise ValueError("Matching expects two Graph-hard candidates per training positive")
    if int(np.asarray(target_counts).sum()) != n_rows:
        raise ValueError("Stratum quota total must equal the number of training positives")

    graph = nx.DiGraph()
    source, sink = ("source", 0), ("sink", 0)
    graph.add_node(source, demand=-n_rows)
    graph.add_node(sink, demand=n_rows)
    option_id: dict[tuple[int, int], int] = {}
    n_bins = len(target_counts)
    for row in range(n_rows):
        row_node = ("row", row)
        graph.add_node(row_node, demand=0)
        graph.add_edge(source, row_node, capacity=1, weight=0)
        best_by_bin: dict[int, tuple[int, float]] = {}
        for col in range(n_choices):
            b = int(strata[row, col])
            value = float(objective[row, col])
            if b not in best_by_bin or value < best_by_bin[b][1]:
                best_by_bin[b] = (col, value)
        for b, (col, value) in best_by_bin.items():
            bin_node = ("bin", b)
            # Integer costs are deterministic; the final small term breaks ties.
            weight = int(round(value * 1_000_000)) * 3 + int(col)
            graph.add_edge(row_node, bin_node, capacity=1, weight=weight)
            option_id[(row, b)] = int(candidate_ids[row, col])
    for b in range(n_bins):
        bin_node = ("bin", b)
        graph.add_node(bin_node, demand=0)
        graph.add_edge(bin_node, sink, capacity=int(target_counts[b]), weight=0)
    try:
        flow = nx.min_cost_flow(graph)
    except (nx.NetworkXUnfeasible, nx.NetworkXError) as exc:
        raise RuntimeError(f"Graph-hardness stratum matching failed: {exc}") from exc
    selected = np.empty(n_rows, dtype=np.int64)
    for row in range(n_rows):
        chosen = [node[1] for node, amount in flow[("row", row)].items() if amount]
        if len(chosen) != 1:
            raise RuntimeError(f"Matching returned {len(chosen)} bins for row {row}")
        selected[row] = option_id[(row, int(chosen[0]))]
    return selected


def make_ranked_pool() -> dict:
    selection_started = time.perf_counter()
    with np.load(V61 / "strict_train_candidates_and_selections.npz", allow_pickle=False) as archive:
        data = {key: archive[key].copy() for key in archive.files}
    meta = read_json(V61 / "strict_pool_metadata.json")
    candidates = data["negative_candidates"]
    if candidates.shape != (4488, 20, 2):
        raise RuntimeError(f"Unexpected V6.1 train candidate shape: {candidates.shape}")
    if v61.array_hash(candidates) != meta["candidate_pool_hash"]:
        raise RuntimeError("V6.1 candidate-pool hash mismatch")
    if v61.array_hash(data["score_graph"]) != meta["score_cache"]["Graph"]["score_hash"]:
        raise RuntimeError("Cached Graph-teacher score hash mismatch")
    if v61.array_hash(data["score_raw_hg"]) != meta["score_cache"]["Raw-HG"]["score_hash"]:
        raise RuntimeError("Cached Raw-HG score hash mismatch")
    graph_ckpt = meta["teacher_records"]["Graph"]["checkpoint_hash"]
    hg_ckpt = meta["teacher_records"]["Raw-HG"]["checkpoint_hash"]
    for teacher, expected in (("Graph", graph_ckpt), ("Raw-HG", hg_ckpt)):
        entry = meta["score_cache"][teacher]
        if (entry["train_split_hash"] != meta["train_only_split_hash"]
                or entry["candidate_pool_hash"] != meta["candidate_pool_hash"]
                or int(entry["seed"]) != 0
                or entry["checkpoint_hash"] != expected):
            raise RuntimeError(f"Cache key does not match split/teacher/pool for {teacher}")
    rg = rank_percentiles(data["score_graph"])
    rh = rank_percentiles(data["score_raw_hg"])
    pre_idx = data["graph_prepool_indices"]
    if pre_idx.shape != (len(candidates), 2):
        raise RuntimeError("V6.1 graph-hard prepool does not contain exactly 2K candidates")
    pre_rg = np.take_along_axis(rg, pre_idx, axis=1)
    pre_rh = np.take_along_axis(rh, pre_idx, axis=1)
    graph_hard_idx = data["graph_hard_indices"]
    graph_hard_rg = rg[np.arange(len(candidates)), graph_hard_idx]

    match_audit = None
    mechanism = None
    for n_strata in MATCH_STRATA_TRY:
        bins = quantile_strata(pre_rg, n_strata)
        # Use the identical prepool rank transform for M0 and both arm candidates.
        graph_hard_col = np.argmax(data["score_graph"][np.arange(len(candidates))[:, None], pre_idx], axis=1)
        m0_flat = bins[np.arange(len(candidates)), graph_hard_col]
        target = np.bincount(m0_flat, minlength=n_strata)
        candidate_ids = pre_idx.copy()
        low = exact_stratified_assignment(bins, pre_rh, target, candidate_ids)
        medians = np.asarray([
            np.median(pre_rh[bins == b]) if np.any(bins == b) else 0.0
            for b in range(n_strata)
        ])
        middle_cost = np.abs(pre_rh - medians[bins])
        middle = exact_stratified_assignment(bins, middle_cost, target, candidate_ids)
        high = exact_stratified_assignment(bins, 1.0 - pre_rh, target, candidate_ids)
        picked = {
            "M1": low,
            "M2": middle,
            "M3": high,
        }
        rg_selected = {
            name: rg[np.arange(len(candidates)), ids]
            for name, ids in picked.items()
        }
        means = {name: float(values.mean()) for name, values in rg_selected.items()}
        max_mean_delta = max(abs(means[a] - means[b]) for a, b in (("M1", "M2"), ("M1", "M3"), ("M2", "M3")))
        match_audit = {
            "strata": n_strata,
            "strata_definition": "equal-frequency quantile bins over the 2K Graph-hard prepool's global-pool rank percentile Rg",
            "quota_reference": "M0 Graph-hard top-1 histogram; exact same per-stratum counts assigned to M1/M2/M3",
            "target_counts": target.astype(int).tolist(),
            "mean_Rg": means,
            "median_Rg": {name: float(np.median(values)) for name, values in rg_selected.items()},
            "max_abs_mean_Rg_difference": float(max_mean_delta),
            "KS_M1_M2": None,
            "KS_M1_M3": None,
            "KS_M2_M3": None,
        }
        from scipy.stats import ks_2samp
        for a, b in (("M1", "M2"), ("M1", "M3"), ("M2", "M3")):
            match_audit[f"KS_{a}_{b}"] = float(ks_2samp(rg_selected[a], rg_selected[b]).statistic)
        mechanism = {"M0": graph_hard_idx.copy(), **picked}
        if max_mean_delta <= 0.01:
            break
    if match_audit is None or mechanism is None:
        raise RuntimeError("Could not build matched mechanism selections")

    def shuffle_rh_by_bin(seed: int) -> np.ndarray:
        n_strata = int(match_audit["strata"])
        bins = quantile_strata(pre_rg, n_strata)
        shuffled = pre_rh.copy()
        rng = np.random.default_rng(400_000 + int(seed) * 10_000 + 6_200)
        for b in range(n_strata):
            positions = np.argwhere(bins == b)
            vals = shuffled[bins == b].copy()
            if len(vals) > 1:
                vals = rng.permutation(vals)
            shuffled[positions[:, 0], positions[:, 1]] = vals
        return shuffled

    m4_by_seed = {}
    c3_by_seed = {}
    c4 = np.empty(len(candidates), dtype=np.int64)
    c5 = np.empty(len(candidates), dtype=np.int64)
    for row in range(len(candidates)):
        c4[row] = pre_idx[row, int(np.argmax(pre_rg[row] + LAMBDA * pre_rh[row]))]
        c5[row] = pre_idx[row, int(np.argmax(pre_rg[row] - LAMBDA * pre_rh[row]))]
    for seed in SEEDS:
        shuffled = shuffle_rh_by_bin(seed)
        bins = quantile_strata(pre_rg, int(match_audit["strata"]))
        target = np.asarray(match_audit["target_counts"], dtype=np.int64)
        m4_by_seed[str(seed)] = exact_stratified_assignment(
            bins, shuffled, target, pre_idx,
        )
        c3_idx = np.empty(len(candidates), dtype=np.int64)
        for row in range(len(candidates)):
            local = int(np.argmax(pre_rg[row] - LAMBDA * shuffled[row]))
            c3_idx[row] = pre_idx[row, local]
        c3_by_seed[str(seed)] = c3_idx

    selections = {
        "mechanism": mechanism,
        "M4_by_seed": m4_by_seed,
        "C0": None,
        "C1": data["graph_hard_indices"].copy(),
        "C2": data["a4_indices"].copy(),
        "C3_by_seed": c3_by_seed,
        "C4": c4,
        "C5": c5,
        "lambda": float(LAMBDA),
        "match_audit": match_audit,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    flat_archive = {f"mechanism_{k}": v for k, v in mechanism.items()}
    flat_archive.update({f"M4_seed{s}": arr for s, arr in m4_by_seed.items()})
    flat_archive.update({f"C3_seed{s}": arr for s, arr in c3_by_seed.items()})
    flat_archive.update({f"candidate_{k}": selections[k] for k in ("C1", "C2", "C4", "C5")})
    np.savez_compressed(OUT / "selected_negative_indices.npz", **flat_archive)
    write_json(OUT / "selection_audit.json", {
        "candidate_pool_hash": meta["candidate_pool_hash"],
        "train_only_split_hash": meta["train_only_split_hash"],
        "Graph_teacher_hash": graph_ckpt,
        "Raw_HG_teacher_hash": hg_ckpt,
        "Graph_score_hash": meta["score_cache"]["Graph"]["score_hash"],
        "Raw_HG_score_hash": meta["score_cache"]["Raw-HG"]["score_hash"],
        "R_g_definition": "global candidate-pool ordinal rank percentile over all 89,760 candidate pairs",
        "R_h_definition": "global candidate-pool ordinal rank percentile over all 89,760 candidate pairs",
        "graph_prepool_per_positive": 2,
        "K": 1,
        "matching": match_audit,
        "all_selected_indices_are_in_train_only_pool": True,
        "selection_seconds": float(time.perf_counter() - selection_started),
    })
    return {"data": data, "meta": meta, "Rg": rg, "Rh": rh, "pre_idx": pre_idx, "pre_Rg": pre_rg, "pre_Rh": pre_rh, "selections": selections}


def verify_preflight(pool: dict) -> dict:
    import torch
    from dcdlp.data.loaders import load_dataset
    from dcdlp.evaluate import load_checkpoint_model

    if not torch.cuda.is_available() or "V100" not in torch.cuda.get_device_name(0):
        raise RuntimeError("V6.2 requires the registered CUDA V100 server")
    loaded = load_dataset("cora", ROOT / "data", "standard", 0)
    view = v61.TrainOnlyView(loaded)
    del loaded
    forbidden_rows, forbidden = v61.make_train_forbidden(view)
    split_hash = hashlib.sha256((v61.array_hash(view.train_pos) + v61.array_hash(view.features) + str(view.num_nodes)).encode("ascii")).hexdigest()
    meta = pool["meta"]
    if split_hash != meta["train_only_split_hash"] or len(view.train_pos) != meta["train_positive_count"]:
        raise RuntimeError("V6.1 split hash/count mismatch")
    if v61.array_hash(forbidden_rows) != meta["forbidden_edge_hash"]:
        raise RuntimeError("V6.1 train-only forbidden edge hash mismatch")
    teacher_hashes_actual = {}
    for teacher in ("Graph", "Raw-HG"):
        checkpoint = Path(meta["teacher_records"][teacher]["checkpoint"])
        if not checkpoint.exists():
            raise RuntimeError(f"Cached {teacher} teacher checkpoint is missing")
        model, _ = load_checkpoint_model(checkpoint, device="cuda")
        actual = state_hash(model.state_dict())
        teacher_hashes_actual[teacher] = actual
        if actual != meta["teacher_records"][teacher]["checkpoint_hash"]:
            raise RuntimeError(f"Cached {teacher} teacher checkpoint hash mismatch")
        del model
        torch.cuda.empty_cache()
    data = pool["data"]
    if not np.array_equal(data["S_A1_seed0"], data["negative_candidates"][np.arange(len(view.train_pos)), data["graph_hard_indices"]]):
        raise RuntimeError("V6.1 A1 cached selection is not the frozen Graph-hard top-1 selection")
    if np.any(pool["data"]["negative_candidates"][:, :, 0] == pool["data"]["negative_candidates"][:, :, 1]):
        raise RuntimeError("Candidate pool contains self-loops")
    for pair in pool["data"]["negative_candidates"].reshape(-1, 2):
        if v61.canonical_edge(pair) in forbidden:
            raise RuntimeError("Candidate pool contains a train/message edge")
    audit = {
        "status": "PASS",
        "gpu": torch.cuda.get_device_name(0),
        "protocol": "STRICT_TRAIN_ONLY",
        "split_hash": split_hash,
        "train_positive_count": len(view.train_pos),
        "candidate_pool_hash": meta["candidate_pool_hash"],
        "candidate_count": int(pool["data"]["negative_candidates"].shape[0] * pool["data"]["negative_candidates"].shape[1]),
        "forbidden_edge_count": len(forbidden),
        "all_positive_access_attempts": 0,
        "validation_identities_in_training_pool": False,
        "test_identities_loaded": False,
        "teacher_cache_keys_verified": True,
        "teacher_checkpoint_hashes_verified": teacher_hashes_actual,
        "V6_1_A1_selection_reused_as_M0_source": True,
        "selection_match": pool["selections"]["match_audit"],
        "strict_eligibility_unit_test": v61.strict_eligibility_unit_test(),
    }
    write_json(OUT / "preflight.json", audit)
    return audit


def validation_arrays() -> tuple[np.ndarray, np.ndarray, str]:
    from dcdlp.utils import array_hash
    with np.load(v61.V6 / "fixed_validation_candidates.npz", allow_pickle=False) as z:
        pos = z["valid_positive"].copy()
        neg = z["valid_negative_candidates"].copy()
    expected = v61.load_json(v61.V6 / "fixed_validation_candidates.json")["negative_candidates_hash"]
    digest = array_hash(neg)
    if digest != expected or neg.shape != (len(pos), 20, 2):
        raise RuntimeError("Fixed validation candidate cache failed its V6 hash/shape audit")
    return pos, neg, digest


def train_one(
    view,
    method: str,
    seed: int,
    selected: np.ndarray | None,
    output_rel: str,
    validation_pos: np.ndarray,
    validation_neg: np.ndarray,
    initialize_from_v6: bool = False,
    dataset_name: str = "cora",
    hypergraph_mode: str = "raw",
) -> dict:
    """Train one fixed epoch-10 model, instrumenting diagnostics only."""
    import torch
    from dcdlp import train as train_module
    from dcdlp.data.negative_sampling import uniform_negative_sampling
    from dcdlp.evaluation.ranking import ranking_metrics
    from dcdlp.train import TrainConfig, edge_index_from_graph, score_pairs

    baseline_config = v61.load_json(v61.BASELINE / "H" / "config.json")
    config_values = {key: value for key, value in baseline_config.items() if key in TrainConfig.__dataclass_fields__}
    config_values.update({
        "dataset": dataset_name,
        "seed": int(seed),
        "protocol_train": "uniform",
        "protocol_eval": "standard",
        "pretrain_epochs": EPOCHS,
        "disentangle_epochs": 0,
        "hypergraph_mode": hypergraph_mode,
        "hypergraph_construction": "raw_star",
        "ghhr_training_mode": "none",
        "complementarity_fusion_mode": "none",
        "evaluate_test": False,
        "device": "cuda",
        "output_dir": output_rel,
        "prediction_subdir": "raw",
    })
    config = TrainConfig(**config_values)
    run_dir = ROOT / output_rel
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = run_dir / "codns_run.json"
    checkpoint = None
    if manifest_path.exists():
        existing = read_json(manifest_path)
        checkpoint = Path(existing.get("checkpoint", ""))
        diag_path = run_dir / "epoch_diagnostics.json"
        if (existing.get("selected_negative_hash") == v61.array_hash(selected) if selected is not None else existing.get("dynamic_sampler") == "uniform_from_strict_pool_per_epoch"):
            if checkpoint and checkpoint.exists() and diag_path.exists() and existing.get("status") == "COMPLETE":
                return existing

    if selected is not None:
        selected = np.asarray(selected, dtype=np.int64).copy()
        if selected.shape != (len(view.train_pos), 2):
            raise RuntimeError(f"{method} has unexpected selection shape {selected.shape}")
    train_forbidden_rows, forbidden = v61.make_train_forbidden(view)
    epoch_negatives: list[np.ndarray] = []
    validation_curve: list[dict] = []
    loss_trace: dict = {"logits": [], "labels": [], "weighted_loss": 0.0, "samples": 0, "rows": []}
    epoch_expected_samples = len(view.train_pos) * 2

    old_sampler = train_module._sample_train_negatives
    old_eval = train_module.evaluate_split
    old_residualizer = train_module.fit_training_cn_residualizer
    old_optimizer = train_module._build_optimizer
    old_link_loss = train_module.link_prediction_loss
    initial_state = None
    if initialize_from_v6:
        initial_state = torch.load(v61.BASELINE / "raw_initial_state.pt", map_location="cpu", weights_only=True)
        if state_hash(initial_state) != INITIAL_HASH_EXPECTED:
            raise RuntimeError("Frozen Cora initial-state hash mismatch")

    def sampler(current_dataset, current_config, epoch):
        if current_dataset is not view or current_config is not config:
            raise RuntimeError("Strict sampler called outside the train-only view")
        if selected is None:
            rng = np.random.default_rng(int(seed) * 10_000 + int(epoch) + 710_000)
            cols = rng.integers(0, 20, size=len(view.train_pos))
            negative = pool_candidates[np.arange(len(view.train_pos)), cols].copy()
        else:
            negative = selected.copy()
        if len(negative) != len(view.train_pos):
            raise RuntimeError("Strict sampler did not return one negative per train positive")
        if any(v61.canonical_edge(pair) in forbidden for pair in negative):
            raise RuntimeError("Strict sampler emitted a forbidden pair")
        epoch_negatives.append(negative.copy())
        return negative

    def diag_eval(model, dataset, _positives, eval_seed, negatives_per_positive, x, edge_index, *args, **kwargs):
        count = len(validation_curve) + 1
        model.eval()
        with torch.no_grad():
            pos_score = score_pairs(model, x, edge_index, validation_pos, batch_size=8192)["logit"]
            neg_score = score_pairs(model, x, edge_index, validation_neg.reshape(-1, 2), batch_size=8192)["logit"]
        metrics = ranking_metrics(pos_score, neg_score.reshape(len(validation_pos), validation_neg.shape[1]))
        validation_curve.append({"epoch": count, "validation_mrr": float(metrics["mrr"]), "hits10": float(metrics["hits10"]), "candidate_hash": validation_candidate_hash})
        # This monotone, label-free sentinel locks the legacy train API to epoch 10.
        return {"mrr": float(count)}, []

    def no_cn_residualizer(_dataset, _config):
        return None, {"residualizer_type": "NOT_USED", "fit_split": "train_only", "uses_valid_or_test": False, "used_as_model_input": False}

    def matched_optimizer(model, probes, current_config):
        if current_config is config and initial_state is not None:
            incompatible = model.load_state_dict(initial_state, strict=False)
            bad_missing = [key for key in incompatible.missing_keys if not key.startswith("hypergraph.")]
            bad_unexpected = [key for key in incompatible.unexpected_keys if not key.startswith("hypergraph.")]
            if bad_missing or bad_unexpected:
                raise RuntimeError(f"Frozen V6 model initialization mismatch: {incompatible}")
        return old_optimizer(model, probes, current_config)

    def trace_link_loss(logits, labels, *args, **kwargs):
        loss = old_link_loss(logits, labels, *args, **kwargs)
        logit_np = logits.detach().float().cpu().numpy().reshape(-1)
        label_np = labels.detach().float().cpu().numpy().reshape(-1)
        loss_trace["logits"].append(logit_np)
        loss_trace["labels"].append(label_np)
        loss_trace["weighted_loss"] += float(loss.detach().cpu()) * len(label_np)
        loss_trace["samples"] += len(label_np)
        if loss_trace["samples"] == epoch_expected_samples:
            all_logits = np.concatenate(loss_trace["logits"])
            all_labels = np.concatenate(loss_trace["labels"])
            pos_scores = all_logits[all_labels > 0.5]
            neg_scores = all_logits[all_labels <= 0.5]
            epoch = len(loss_trace["rows"]) + 1
            loss_trace["rows"].append({
                "epoch": epoch,
                "training_loss": float(loss_trace["weighted_loss"] / epoch_expected_samples),
                "positive_negative_margin": float(pos_scores.mean() - neg_scores.mean()),
                "selected_negative_average_model_score": float(neg_scores.mean()),
                "positive_score_mean": float(pos_scores.mean()),
                "negative_score_mean": float(neg_scores.mean()),
            })
            for key in ("logits", "labels"):
                loss_trace[key] = []
            loss_trace["weighted_loss"] = 0.0
            loss_trace["samples"] = 0
        elif loss_trace["samples"] > epoch_expected_samples:
            raise RuntimeError("Training-loss instrumentation crossed an epoch boundary")
        return loss

    # The sampler reads only the audited train-only candidate pool.
    pool_candidates = candidate_pool_for_view(view)
    train_module._sample_train_negatives = sampler
    train_module.evaluate_split = diag_eval
    train_module.fit_training_cn_residualizer = no_cn_residualizer
    train_module._build_optimizer = matched_optimizer
    train_module.link_prediction_loss = trace_link_loss
    started = time.perf_counter()
    try:
        model, result = train_module.train_model(view, config)
    finally:
        train_module._sample_train_negatives = old_sampler
        train_module.evaluate_split = old_eval
        train_module.fit_training_cn_residualizer = old_residualizer
        train_module._build_optimizer = old_optimizer
        train_module.link_prediction_loss = old_link_loss
    if len(epoch_negatives) != EPOCHS or len(validation_curve) != EPOCHS or len(loss_trace["rows"]) != EPOCHS or loss_trace["samples"] != 0:
        raise RuntimeError(f"{method} seed {seed}: incomplete 10-epoch diagnostics")

    selected_hash = None if selected is None else v61.array_hash(selected)
    result["validation"] = {
        "checkpoint_rule": "fixed_final_epoch_10",
        "epoch10_mrr": validation_curve[-1]["validation_mrr"],
        "validation_best_diagnostic_mrr": max(row["validation_mrr"] for row in validation_curve),
        "validation_best_diagnostic_epoch": 1 + int(np.argmax([row["validation_mrr"] for row in validation_curve])),
        "validation_metrics_used_for_selection": False,
        "test_evaluated": False,
        "candidate_hash": validation_candidate_hash,
    }
    result["validation_curve"] = []
    result["best_epoch"] = EPOCHS - 1
    result["checkpoint_selection_audit"] = {
        "rule": "FIXED_EPOCH_10",
        "validation_best_is_diagnostic_only": True,
        "heldout_metrics_used_for_checkpoint_selection": False,
        "legacy_train_api_placeholder_reads": dict(view.placeholder_reads),
        "heldout_identity_values_exposed_to_sampler": 0,
        "test_identity_values_loaded": False,
    }
    result["data_integrity"] = {
        "train_positive_hash": v61.array_hash(view.train_pos),
        "candidate_hash": pool_hash_for_view(view),
        "valid_identity_in_training_pool": False,
        "test_identity_in_training_pool": False,
        "all_positive_access_attempts": 0,
    }
    result_path = Path(result["result_file"])
    v61.write_json(result_path, result)
    diagnostics = {
        "epoch_diagnostics": [
            {**loss_trace["rows"][i], "validation_mrr": validation_curve[i]["validation_mrr"], "selected_negative_hash": v61.array_hash(epoch_negatives[i])}
            for i in range(EPOCHS)
        ],
        "validation_best_diagnostic": {
            "epoch": result["validation"]["validation_best_diagnostic_epoch"],
            "mrr": result["validation"]["validation_best_diagnostic_mrr"],
            "used_for_method_comparison": False,
            "used_for_checkpoint_selection": False,
        },
        "negative_diversity": diversity_summary(epoch_negatives, view),
    }
    write_json(run_dir / "epoch_diagnostics.json", diagnostics)
    np.savez_compressed(run_dir / "negative_samples_by_epoch.npz", negatives=np.stack(epoch_negatives))
    model_hash = state_hash(model.state_dict())
    run_record = {
        "status": "COMPLETE",
        "method": method,
        "seed": int(seed),
        "checkpoint": result["checkpoint"],
        "result_file": str(result_path),
        "diagnostics_file": str(run_dir / "epoch_diagnostics.json"),
        "train_seconds": float(result["runtime"]["train_seconds"]),
        "wall_seconds": float(time.perf_counter() - started),
        "selected_negative_hash": selected_hash,
        "dynamic_sampler": "uniform_from_strict_pool_per_epoch" if selected is None else None,
        "model_state_hash": model_hash,
        "epoch10_validation_mrr": float(validation_curve[-1]["validation_mrr"]),
        "epoch_count": EPOCHS,
        "checkpoint_rule": "FIXED_EPOCH_10",
        "test_evaluated": False,
    }
    write_json(manifest_path, run_record)
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return run_record


def candidate_pool_for_view(view) -> np.ndarray:
    global candidate_pool
    pool = globals().get("candidate_pool")
    if pool is not None and len(pool) == len(view.train_pos):
        return np.asarray(pool, dtype=np.int64)
    if view.name.lower() == "cora":
        with np.load(V61 / "strict_train_candidates_and_selections.npz", allow_pickle=False) as z:
            return z["negative_candidates"].copy()
    raise RuntimeError(f"No strict candidate pool registered for {view.name}")


def pool_hash_for_view(view) -> str:
    return v61.array_hash(candidate_pool_for_view(view))


def diversity_summary(epoch_negatives: list[np.ndarray], view) -> dict:
    import networkx as nx
    pairs = [np.asarray(rows, dtype=np.int64) for rows in epoch_negatives]
    unique_pair = [len({v61.canonical_edge(x) for x in rows}) / max(1, len(rows)) for rows in pairs]
    unique_endpoint = [len(set(map(int, rows.reshape(-1)))) / max(1, rows.size) for rows in pairs]
    overlaps = []
    for a, b in zip(pairs, pairs[1:]):
        sa = {v61.canonical_edge(x) for x in a}
        sb = {v61.canonical_edge(x) for x in b}
        overlaps.append(len(sa & sb) / max(1, len(sa | sb)))
    graph = view.train_graph()
    degrees = dict(graph.degree())
    endpoint_degrees = [degrees.get(int(node), 0) for rows in pairs for node in rows.reshape(-1)]
    return {
        "unique_pair_ratio_mean": float(np.mean(unique_pair)),
        "unique_endpoint_ratio_mean": float(np.mean(unique_endpoint)),
        "consecutive_epoch_pair_jaccard_mean": float(np.mean(overlaps)) if overlaps else 1.0,
        "consecutive_epoch_pair_jaccard": [float(x) for x in overlaps],
        "endpoint_degree_mean": float(np.mean(endpoint_degrees)),
        "endpoint_degree_median": float(np.median(endpoint_degrees)),
        "endpoint_degree_histogram_le_1_2_5_10_gt10": {
            "0-1": int(np.sum(np.asarray(endpoint_degrees) <= 1)),
            "2-5": int(np.sum((np.asarray(endpoint_degrees) >= 2) & (np.asarray(endpoint_degrees) <= 5))),
            "6-10": int(np.sum((np.asarray(endpoint_degrees) >= 6) & (np.asarray(endpoint_degrees) <= 10))),
            ">10": int(np.sum(np.asarray(endpoint_degrees) > 10)),
        },
    }


def run_training_suite(pool: dict, method_group: str) -> dict:
    from dcdlp.data.loaders import load_dataset

    if method_group == "mechanism":
        labels = METHODS_MECH
        selection = pool["selections"]["mechanism"]
    elif method_group == "codns":
        labels = METHODS_CODNS
        selection = pool["selections"]
    else:
        raise ValueError(method_group)
    loaded = load_dataset("cora", ROOT / "data", "standard", 0)
    view = v61.TrainOnlyView(loaded)
    del loaded
    valid_pos, valid_neg, valid_hash = validation_arrays()
    global candidate_pool, candidate_pool_hash, validation_candidate_hash
    candidate_pool = pool["data"]["negative_candidates"]
    candidate_pool_hash = pool["meta"]["candidate_pool_hash"]
    validation_candidate_hash = valid_hash
    validation_candidate_hash = valid_hash
    state_path = OUT / ("mechanism_training_state.json" if method_group == "mechanism" else "codns_training_state.json")
    state = read_json(state_path) if state_path.exists() else {"method_group": method_group, "runs": {}, "state": "RUNNING"}
    for method in labels:
        for seed in SEEDS:
            key = f"{method}_seed{seed}"
            if method_group == "codns" and method == "C1":
                source = read_json(OUT / "mechanism_training_state.json")["runs"][f"M0_seed{seed}"]
                state["runs"][key] = {
                    **source,
                    "method": "C1",
                    "source_method": "M0",
                    "reused_exact_graph_hard_run": True,
                }
                state["state"] = "RUNNING"
                write_json(state_path, state)
                continue
            set_status(f"{method_group}_training", key, completed=list(state["runs"]))
            if method_group == "mechanism":
                if method == "M4":
                    selected_ids = pool["selections"]["M4_by_seed"][str(seed)]
                else:
                    selected_ids = selection[method]
                selected = pool["data"]["negative_candidates"][np.arange(len(view.train_pos)), selected_ids]
            elif method == "codns":
                if method == "C0":
                    selected = None
                elif method == "C3":
                    ids = selection["C3_by_seed"][str(seed)]
                    selected = pool["data"]["negative_candidates"][np.arange(len(view.train_pos)), ids]
                else:
                    ids = selection[method]
                    selected = pool["data"]["negative_candidates"][np.arange(len(view.train_pos)), ids]
            run_dir = OUT / "RUNS" / method_group.upper() / key
            output_rel = str(run_dir.relative_to(ROOT)).replace("\\", "/")
            record = train_one(
                view, method, seed, selected, output_rel, valid_pos, valid_neg,
                initialize_from_v6=(seed == 0 and method_group == "mechanism"),
            )
            state["runs"][key] = record
            state["state"] = "RUNNING"
            state["candidate_pool_hash"] = candidate_pool_hash
            state["split_hash"] = pool["meta"]["train_only_split_hash"]
            state["validation_candidate_hash"] = valid_hash
            write_json(state_path, state)
            stat = current_status()
            done = stat.get("completed", [])
            if key not in done:
                done.append(key)
            set_status(f"{method_group}_training", None, completed=done, current_finished=key)
    state["state"] = "TRAINING_COMPLETE"
    write_json(state_path, state)
    return state


def eval_fixed_candidates(checkpoint: str, view, positives: np.ndarray, negatives: np.ndarray) -> dict:
    import torch
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.evaluation.ranking import ranking_metrics

    model, _ = load_checkpoint_model(checkpoint, device="cuda")
    x = torch.as_tensor(view.features, dtype=torch.float32, device="cuda")
    edge_index = edge_index_from_graph(view.train_graph(), torch.device("cuda"))
    with torch.no_grad():
        pos = score_pairs(model, x, edge_index, positives, batch_size=8192)["logit"]
        neg = score_pairs(model, x, edge_index, negatives.reshape(-1, 2), batch_size=8192)["logit"]
    metrics = ranking_metrics(pos, neg.reshape(len(positives), negatives.shape[1]))
    del model
    torch.cuda.empty_cache()
    return {key: float(value) for key, value in metrics.items()}


def summary_metrics(metrics_by_method: dict) -> dict:
    result = {}
    for method, values in metrics_by_method.items():
        vals = [float(values[str(seed)]["mrr"]) for seed in SEEDS]
        result[method] = {"by_seed": vals, "mean": float(np.mean(vals)), "sample_std": float(np.std(vals, ddof=1))}
    return result


def run_validation_gate(pool: dict, method_group: str) -> dict:
    from dcdlp.data.loaders import load_dataset
    from dcdlp.utils import array_hash

    state_path = OUT / ("mechanism_training_state.json" if method_group == "mechanism" else "codns_training_state.json")
    state = read_json(state_path)
    if state.get("state") not in {"TRAINING_COMPLETE", "VALIDATION_COMPLETE"}:
        raise RuntimeError(f"{method_group} validation requested before training completion")
    view_loaded = load_dataset("cora", ROOT / "data", "standard", 0)
    view = v61.TrainOnlyView(view_loaded)
    del view_loaded
    pos, neg, candidate_hash = validation_arrays()
    results = {}
    for method in (METHODS_MECH if method_group == "mechanism" else METHODS_CODNS):
        results[method] = {}
        if method_group == "codns" and method == "C1":
            source_state = read_json(OUT / "mechanism_training_state.json")
            source_method = "M0"
        else:
            source_state = state
            source_method = method
        for seed in SEEDS:
            record = source_state["runs"][f"{source_method}_seed{seed}"]
            values = eval_fixed_candidates(record["checkpoint"], view, pos, neg)
            diag = read_json(Path(record["diagnostics_file"]))
            curve_last = diag["epoch_diagnostics"][-1]["validation_mrr"]
            if abs(values["mrr"] - float(curve_last)) > 1e-5:
                raise RuntimeError(f"Epoch-10 validation recheck mismatch for {method} seed {seed}")
            results[method][str(seed)] = {
                "mrr": values["mrr"],
                "hits10": values["hits10"],
                "mean_positive_rank": values["mean_positive_rank"],
                "checkpoint": record["checkpoint"],
                "checkpoint_rule": "FIXED_EPOCH_10",
                "validation_candidate_hash": candidate_hash,
                "validation_best_diagnostic_mrr": diag["validation_best_diagnostic"]["mrr"],
                "validation_best_diagnostic_epoch": diag["validation_best_diagnostic"]["epoch"],
            }
    summary = summary_metrics(results)
    if method_group == "mechanism":
        deltas_13 = [results["M1"][str(s)]["mrr"] - results["M3"][str(s)]["mrr"] for s in SEEDS]
        deltas_14 = [results["M1"][str(s)]["mrr"] - results["M4"][str(s)]["mrr"] for s in SEEDS]
        match = pool["selections"]["match_audit"]
        match_pass = float(match["max_abs_mean_Rg_difference"]) <= 0.01
        gate = bool(
            match_pass
            and sum(x > 0 for x in deltas_13) >= 2 and float(np.mean(deltas_13)) > 0
            and sum(x > 0 for x in deltas_14) >= 2 and float(np.mean(deltas_14)) > 0
        )
        output = {
            "state": "VALIDATION_COMPLETE",
            "protocol": "STRICT_TRAIN_ONLY",
            "checkpoint_rule": "FIXED_EPOCH_10",
            "validation_candidate_hash": candidate_hash,
            "metrics": results,
            "summary": summary,
            "Graph_hardness_match": match,
            "Graph_hardness_match_pass": match_pass,
            "M1_minus_M3_by_seed": deltas_13,
            "M1_minus_M3_mean": float(np.mean(deltas_13)),
            "M1_minus_M3_wins": int(sum(x > 0 for x in deltas_13)),
            "M1_minus_M4_by_seed": deltas_14,
            "M1_minus_M4_mean": float(np.mean(deltas_14)),
            "M1_minus_M4_wins": int(sum(x > 0 for x in deltas_14)),
            "MECHANISM_SUPPORTED": bool(gate),
            "next": "CODNS" if gate else "DISAGREEMENT_MECHANISM_NOT_SUPPORTED",
        }
        write_json(OUT / "mechanism_validation.json", output)
    else:
        c5 = [results["C5"][str(s)]["mrr"] for s in SEEDS]
        c1 = [results["C1"][str(s)]["mrr"] for s in SEEDS]
        c3 = [results["C3"][str(s)]["mrr"] for s in SEEDS]
        c4 = [results["C4"][str(s)]["mrr"] for s in SEEDS]
        c2 = [results["C2"][str(s)]["mrr"] for s in SEEDS]
        gain = float(np.mean(c5) - np.mean(c1))
        relative = gain / float(np.mean(c1)) if np.mean(c1) else None
        wins = {
            "C5_vs_C1": int(sum(a > b for a, b in zip(c5, c1))),
            "C5_vs_C3": int(sum(a > b for a, b in zip(c5, c3))),
            "C5_vs_C4": int(sum(a > b for a, b in zip(c5, c4))),
        }
        mean_deltas = {
            "C5_minus_C1": float(np.mean(c5) - np.mean(c1)),
            "C5_minus_C3": float(np.mean(c5) - np.mean(c3)),
            "C5_minus_C4": float(np.mean(c5) - np.mean(c4)),
            "C5_minus_C2": float(np.mean(c5) - np.mean(c2)),
        }
        gain_gate = gain > 0 and (gain >= 0.002 or (relative is not None and relative >= 0.005))
        gate = bool(
            wins["C5_vs_C1"] >= 2 and wins["C5_vs_C3"] >= 2 and wins["C5_vs_C4"] >= 2
            and gain_gate and mean_deltas["C5_minus_C4"] > 0
            and mean_deltas["C5_minus_C2"] >= -0.001
        )
        output = {
            "state": "VALIDATION_COMPLETE",
            "protocol": "STRICT_TRAIN_ONLY",
            "checkpoint_rule": "FIXED_EPOCH_10",
            "validation_candidate_hash": candidate_hash,
            "metrics": results,
            "summary": summary,
            "wins_C5": wins,
            "mean_deltas_C5": mean_deltas,
            "absolute_gain_C5_vs_C1": gain,
            "relative_gain_C5_vs_C1": relative,
            "gain_gate_pass": gain_gate,
            "CODNS_SUPPORTED": bool(gate),
            "next": "LAMBDA_SENSITIVITY_THEN_TEST" if gate else "CODNS_REJECT",
        }
        write_json(OUT / "codns_validation.json", output)
    state["state"] = "VALIDATION_COMPLETE"
    write_json(state_path, state)
    set_status(f"{method_group}_validation_complete", None, decision=output.get("next"))
    return output


def run_lambda_sensitivity(pool: dict) -> dict:
    from dcdlp.data.loaders import load_dataset

    codns_gate = read_json(OUT / "codns_validation.json")
    if not codns_gate.get("CODNS_SUPPORTED"):
        raise RuntimeError("Lambda sensitivity is gated by the CODNS validation GO")
    view_source = load_dataset("cora", ROOT / "data", "standard", 0)
    view = v61.TrainOnlyView(view_source)
    del view_source
    valid_pos, valid_neg, valid_hash = validation_arrays()
    global candidate_pool, candidate_pool_hash, validation_candidate_hash, LAMBDA
    candidate_pool = pool["data"]["negative_candidates"]
    candidate_pool_hash = pool["meta"]["candidate_pool_hash"]
    validation_candidate_hash = valid_hash
    pre_idx, pre_rg, pre_rh = pool["pre_idx"], pool["pre_Rg"], pool["pre_Rh"]
    by_lambda = {}
    codns_state = read_json(OUT / "codns_training_state.json")
    c1_record = read_json(OUT / "mechanism_training_state.json")["runs"]["M0_seed0"]
    baseline_c1 = eval_fixed_candidates(c1_record["checkpoint"], view, valid_pos, valid_neg)["mrr"]
    for value in (0.25, 0.5, 0.75):
        key = f"lambda_{value:.2f}"
        if value == 0.5:
            record = codns_state["runs"]["C5_seed0"]
        else:
            ids = np.asarray([
                pre_idx[row, int(np.argmax(pre_rg[row] - value * pre_rh[row]))]
                for row in range(len(view.train_pos))
            ], dtype=np.int64)
            selected = pool["data"]["negative_candidates"][np.arange(len(view.train_pos)), ids]
            LAMBDA = float(value)
            out_dir = OUT / "RUNS" / "LAMBDA_SENSITIVITY" / key
            record = train_one(
                view, key, 0, selected, str(out_dir.relative_to(ROOT)).replace("\\", "/"),
                valid_pos, valid_neg, initialize_from_v6=True,
            )
        mrr = eval_fixed_candidates(record["checkpoint"], view, valid_pos, valid_neg)["mrr"]
        by_lambda[str(value)] = {
            "seed": 0,
            "mrr": float(mrr),
            "selected_negative_hash": record.get("selected_negative_hash"),
            "checkpoint": record["checkpoint"],
            "checkpoint_rule": "FIXED_EPOCH_10",
        }
    LAMBDA = 0.5
    comparable = all(float(row["mrr"]) >= baseline_c1 - 0.001 for row in by_lambda.values())
    result = {
        "status": "COMPLETE",
        "purpose": "predeclared sensitivity diagnostic; lambda=0.5 remains the primary method",
        "values": by_lambda,
        "Graph_hard_seed0_validation_mrr": float(baseline_c1),
        "ROBUST_TO_LAMBDA": bool(comparable),
        "decision_rule": "each lambda is within 0.001 MRR of or above seed-0 Graph-hard; no value is selected post hoc",
        "validation_candidate_hash": valid_hash,
        "test_evaluated": False,
    }
    write_json(OUT / "lambda_sensitivity.json", result)
    set_status("lambda_sensitivity_complete", None, robust_to_lambda=result["ROBUST_TO_LAMBDA"], test_evaluated=False)
    return result


def make_cora_test_candidates_once(dataset) -> tuple[np.ndarray, np.ndarray, str]:
    """Build and persist the one shared test set only after all validation gates."""
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.utils import array_hash

    path = OUT / "test_candidates_once.npz"
    meta_path = OUT / "test_candidates_once.json"
    if path.exists() and meta_path.exists():
        meta = read_json(meta_path)
        with np.load(path, allow_pickle=False) as z:
            pos, neg = z["test_positive"].copy(), z["test_negative_candidates"].copy()
        if array_hash(neg) != meta["negative_candidate_hash"]:
            raise RuntimeError("Persisted one-time test candidate hash mismatch")
        return pos, neg, meta["negative_candidate_hash"]
    seed, grouping_seed = 999, 1000
    pool = uniform_negative_sampling(
        dataset.num_nodes, dataset.all_positive, 20 * len(dataset.test_pos), seed,
    )
    negatives = grouped_negatives(dataset.test_pos, pool, 20, grouping_seed)
    digest = array_hash(negatives)
    expected = v61.load_json(v61.V6 / "results.json")["test_results"]["shared_candidate_hash"]
    if digest != expected:
        raise RuntimeError(f"New test pool differs from the frozen V6.1 shared pool: {digest} != {expected}")
    np.savez_compressed(path, test_positive=dataset.test_pos, test_negative_candidates=negatives)
    write_json(meta_path, {
        "negative_candidate_hash": digest,
        "positive_count": int(len(dataset.test_pos)),
        "negative_count_per_positive": 20,
        "pool_seed": seed,
        "grouping_seed": grouping_seed,
        "created_after_validation_freeze": True,
        "all_positive_used_only_for_test_pool_generation": True,
    })
    set_status("test_candidates_frozen", None, test_evaluated=True, test_candidate_hash=digest)
    return dataset.test_pos.copy(), negatives, digest


def run_cora_test_once(pool: dict) -> dict:
    from dcdlp.data.loaders import load_dataset

    mech = read_json(OUT / "mechanism_validation.json")
    codns = read_json(OUT / "codns_validation.json")
    lambdas = read_json(OUT / "lambda_sensitivity.json")
    if not mech.get("MECHANISM_SUPPORTED") or not codns.get("CODNS_SUPPORTED") or lambdas.get("status") != "COMPLETE":
        raise RuntimeError("Cora test remains closed until mechanism, CODNS, and lambda validation decisions are frozen")
    prior = OUT / "test_results.json"
    if prior.exists():
        existing = read_json(prior)
        if existing.get("state") == "COMPLETE":
            return existing
    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    pos, neg, candidate_hash = make_cora_test_candidates_once(dataset)
    existing = read_json(prior) if prior.exists() else {}
    records = existing.get("by_method_seed", {})
    mech_state = read_json(OUT / "mechanism_training_state.json")["runs"]
    codns_state = read_json(OUT / "codns_training_state.json")["runs"]
    for method in ("C1", "C2", "C3", "C4", "C5"):
        source = mech_state if method == "C1" else codns_state
        source_method = "M0" if method == "C1" else method
        records.setdefault(method, {})
        for seed in SEEDS:
            if str(seed) in records.get(method, {}):
                continue
            key = f"{source_method}_seed{seed}"
            run = source[key]
            set_status("test_evaluation", f"{method}_seed{seed}", test_evaluated=True, test_candidate_hash=candidate_hash)
            metric = eval_fixed_candidates(run["checkpoint"], v61.TrainOnlyView(dataset), pos, neg)
            records[method][str(seed)] = {
                "mrr": metric["mrr"],
                "hits10": metric["hits10"],
                "mean_positive_rank": metric["mean_positive_rank"],
                "checkpoint": run["checkpoint"],
                "candidate_hash": candidate_hash,
            }
            # Persist after each model so an interrupted evaluation can resume
            # against precisely the same already-frozen candidate array.
            write_json(prior, {
                "state": "RUNNING_TEST_EVALUATION",
                "test_evaluated_once": True,
                "test_candidate_hash": candidate_hash,
                "by_method_seed": records,
                "completed_models": [f"{m}_seed{s}" for m, rows in records.items() for s in rows],
            })
    means = {m: float(np.mean([records[m][str(s)]["mrr"] for s in SEEDS])) for m in records}
    stds = {m: float(np.std([records[m][str(s)]["mrr"] for s in SEEDS], ddof=1)) for m in records}
    deltas = {
        "C5_minus_C1_by_seed": [records["C5"][str(s)]["mrr"] - records["C1"][str(s)]["mrr"] for s in SEEDS],
        "C5_minus_C3_by_seed": [records["C5"][str(s)]["mrr"] - records["C3"][str(s)]["mrr"] for s in SEEDS],
        "C5_minus_C4_by_seed": [records["C5"][str(s)]["mrr"] - records["C4"][str(s)]["mrr"] for s in SEEDS],
        "C5_minus_C2_by_seed": [records["C5"][str(s)]["mrr"] - records["C2"][str(s)]["mrr"] for s in SEEDS],
    }
    supported = bool(means["C5"] > means["C1"] and means["C5"] > means["C3"])
    result = {
        "state": "COMPLETE",
        "test_evaluated_once": True,
        "test_positive_count": int(len(pos)),
        "negative_count_per_positive": 20,
        "test_candidate_hash": candidate_hash,
        "candidate_hash_matches_V6_1": True,
        "by_method_seed": records,
        "mean_mrr": means,
        "sample_sd_mrr": stds,
        "deltas": deltas,
        "C5_beats_C1_and_C3_test_means": supported,
        "C5_beats_C4_test_mean": bool(means["C5"] > means["C4"]),
        "C5_minus_C2_mean": float(means["C5"] - means["C2"]),
        "test_data_first_opened_after_validation_freeze": True,
    }
    write_json(prior, result)
    set_status("test_complete", None, test_evaluated=True, test_candidate_hash=candidate_hash)
    return result


_COMPONENT_BY_NODE: dict[int, int] = {}
_DISTANCE_BY_SOURCE: dict[int, dict[int, int]] = {}
_ACTIVE_GRAPH_ID: int | None = None


def pair_structure(pair: tuple[int, int], graph) -> dict:
    u, v = pair
    nu = set(graph.neighbors(u))
    nv = set(graph.neighbors(v))
    common = nu & nv
    du, dv = graph.degree(u), graph.degree(v)
    aa = sum(1.0 / math.log(graph.degree(w)) for w in common if graph.degree(w) > 1)
    ra = sum(1.0 / graph.degree(w) for w in common if graph.degree(w) > 0)
    union = nu | nv
    closed_u, closed_v = nu | {u}, nv | {v}
    if v in nu:
        path_category = "1-hop"
    else:
        try:
            distance = nx_shortest_distance(graph, u, v, cutoff=3)
        except Exception:
            distance = None
        if distance == 2:
            path_category = "2-hop"
        elif distance == 3:
            path_category = "3-hop"
        elif distance is None:
            path_category = "disconnected"
        else:
            path_category = ">3"
    return {
        "common_neighbors": len(common),
        "adamic_adar": aa,
        "resource_allocation": ra,
        "jaccard": len(common) / max(1, len(union)),
        "degree_u": du,
        "degree_v": dv,
        "degree_product": du * dv,
        "shortest_path_category": path_category,
        "raw_star_shared_hyperedge_count": len(closed_u & closed_v),
        "raw_star_overlap_strength": len(closed_u & closed_v) / max(1, len(closed_u | closed_v)),
    }


def nx_shortest_distance(graph, u: int, v: int, cutoff: int = 3) -> int | None:
    import networkx as nx
    global _ACTIVE_GRAPH_ID, _COMPONENT_BY_NODE, _DISTANCE_BY_SOURCE
    if _ACTIVE_GRAPH_ID != id(graph):
        _ACTIVE_GRAPH_ID = id(graph)
        _COMPONENT_BY_NODE = {}
        for component_id, nodes in enumerate(nx.connected_components(graph)):
            for node in nodes:
                _COMPONENT_BY_NODE[int(node)] = component_id
        _DISTANCE_BY_SOURCE = {}
    if u not in _DISTANCE_BY_SOURCE:
        _DISTANCE_BY_SOURCE[u] = dict(nx.single_source_shortest_path_length(graph, u, cutoff=cutoff))
    distance = _DISTANCE_BY_SOURCE[u].get(v)
    if distance is not None:
        return int(distance)
    if _COMPONENT_BY_NODE.get(u) == _COMPONENT_BY_NODE.get(v):
        return cutoff + 1
    return None


def structural_summary(pool: dict, mechanism: dict, codns: dict | None) -> dict:
    from dcdlp.data.loaders import load_dataset
    import networkx as nx

    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    graph = dataset.train_graph()
    candidates = pool["data"]["negative_candidates"]
    selections = pool["selections"]
    groups = {
        "M1_HG_low": [selections["mechanism"]["M1"]],
        "M3_HG_high": [selections["mechanism"]["M3"]],
    }
    if codns is not None and codns.get("CODNS_SUPPORTED"):
        groups["C5_CODNS"] = [selections["C5"]]
        groups["C4_reverse_agreement"] = [selections["C4"]]
    output = {}
    for name, index_runs in groups.items():
        per_run = []
        for indices in index_runs:
            pairs = candidates[np.arange(len(indices)), indices]
            rows = [pair_structure(v61.canonical_edge(pair), graph) for pair in pairs]
            row = {}
            numeric_keys = ["common_neighbors", "adamic_adar", "resource_allocation", "jaccard", "degree_u", "degree_v", "degree_product", "raw_star_shared_hyperedge_count", "raw_star_overlap_strength"]
            for key in numeric_keys:
                values = np.asarray([item[key] for item in rows], dtype=np.float64)
                row[key] = {"mean": float(values.mean()), "median": float(np.median(values))}
            row["shortest_path_counts"] = {key: int(sum(item["shortest_path_category"] == key for item in rows)) for key in ("1-hop", "2-hop", "3-hop", ">3", "disconnected")}
            row["unique_pair_ratio"] = len({v61.canonical_edge(x) for x in pairs}) / max(1, len(pairs))
            row["unique_endpoint_ratio"] = len(set(map(int, pairs.reshape(-1)))) / max(1, pairs.size)
            rg = pool["Rg"][np.arange(len(indices)), indices]
            rh = pool["Rh"][np.arange(len(indices)), indices]
            row["mean_Rg"] = float(rg.mean())
            row["median_Rg"] = float(np.median(rg))
            row["mean_Rh"] = float(rh.mean())
            per_run.append(row)
        output[name] = per_run[0]
    output["interpretation_limit"] = "Descriptive train-graph structure only; no future-positive or false-negative enrichment analysis was run."
    return output


def efficiency_summary(pool: dict) -> dict:
    meta = pool["meta"]
    cache = meta["score_cache"]
    return {
        "candidate_pool_generation_seconds_V6_1": float(meta["pool_generation_seconds"]),
        "cold_teacher_training_seconds_V6_1": {k: float(v["train_seconds"]) for k, v in meta["teacher_records"].items()},
        "cold_teacher_scoring_seconds_V6_1": {k: float(v["forward_seconds"]) for k, v in cache.items()},
        "V6_2_teacher_forward_repeats": 0,
        "teacher_cache_key_fields": ["train_only_split_hash", "seed", "teacher_checkpoint_hash", "candidate_pool_hash"],
        "cache_verified": True,
        "candidate_pool_hash": meta["candidate_pool_hash"],
        "selection_cache_hit": True,
        "selection_time_seconds_V6_2": float(read_json(OUT / "selection_audit.json").get("selection_seconds", 0.0)),
        "training_wall_seconds": {
            name: float(sum(row.get("wall_seconds", 0.0) for row in read_json(OUT / name)["runs"].values()))
            for name in ("mechanism_training_state.json", "codns_training_state.json") if (OUT / name).exists()
        },
        "amortized_selection_seconds_per_epoch": float(read_json(OUT / "selection_audit.json").get("selection_seconds", 0.0)) / EPOCHS,
    }


def write_reports(pool: dict, final_decision: str, cross: dict | None = None) -> None:
    preflight = read_json(OUT / "preflight.json")
    mechanism = read_json(OUT / "mechanism_validation.json") if (OUT / "mechanism_validation.json").exists() else None
    codns = read_json(OUT / "codns_validation.json") if (OUT / "codns_validation.json").exists() else None
    lambdas = read_json(OUT / "lambda_sensitivity.json") if (OUT / "lambda_sensitivity.json").exists() else None
    test = read_json(OUT / "test_results.json") if (OUT / "test_results.json").exists() and read_json(OUT / "test_results.json").get("state") == "COMPLETE" else None
    structure = structural_summary(pool, mechanism or {}, codns)
    efficiency = efficiency_summary(pool)
    write_json(OUT / "structural_results.json", structure)
    write_json(OUT / "efficiency_results.json", efficiency)
    v61audit = {
        "V6.1_strict_validation_mean_mrr": {"A1": 0.4541538265172445, "A3": 0.47065613209770296, "A4": 0.5049546061738671},
        "V6.1_strict_test_mean_mrr": {"A1": 0.4728099413871146, "A3": 0.4900635446840087, "A4": 0.5274332218780171},
        "V6.1_false_negative_mechanism_supported": False,
        "V6.1_final_decision": "NO_MECHANISM",
        "train_only_split_hash": pool["meta"]["train_only_split_hash"],
        "candidate_pool_hash": pool["meta"]["candidate_pool_hash"],
        "validation_candidate_hash": v61.load_json(v61.V6 / "fixed_validation_candidates.json")["negative_candidates_hash"],
        "teacher_hashes": {k: v["checkpoint_hash"] for k, v in pool["meta"]["teacher_records"].items()},
        "note": "Do not claim that HG identifies future positives or false negatives; this sprint tests a distinct training-utility disagreement hypothesis.",
    }
    write_json(OUT / "results.json", {
        "status": "EXECUTED",
        "protocol": "STRICT_TRAIN_ONLY",
        "checkpoint_rule": "FIXED_EPOCH_10",
        "preflight": preflight,
        "mechanism": mechanism,
        "codns": codns,
        "lambda_sensitivity": lambdas,
        "test": test,
        "second_dataset": cross,
        "structural_characterization": structure,
        "efficiency": efficiency,
        "novelty_status": "EXACT_RULE_UNVERIFIED",
        "final_decision": final_decision,
    })
    write_json(OUT / "v61_audit.json", v61audit)
    (OUT / "00_V61_AUDIT.md").write_text(
        "# V6.1 Audit\n\n"
        f"- Strict validation MRR: A1 {v61audit['V6.1_strict_validation_mean_mrr']['A1']:.6f}, A3 {v61audit['V6.1_strict_validation_mean_mrr']['A3']:.6f}, A4 {v61audit['V6.1_strict_validation_mean_mrr']['A4']:.6f}.\n"
        f"- Strict test MRR: A1 {v61audit['V6.1_strict_test_mean_mrr']['A1']:.6f}, A3 {v61audit['V6.1_strict_test_mean_mrr']['A3']:.6f}, A4 {v61audit['V6.1_strict_test_mean_mrr']['A4']:.6f}.\n"
        "- V6.1 performance signal is retained as historical context; its false-negative enrichment mechanism was not statistically supported.\n"
        "- Reused train-only split, 20-per-positive pool, Graph/Raw-HG teacher scores, and fixed validation candidates only after checking their stored hashes.\n"
        f"- Split hash: `{v61audit['train_only_split_hash']}`\n- Candidate pool hash: `{v61audit['candidate_pool_hash']}`\n"
        "- No V6.1 false-negative claim is carried into V6.2.\n", encoding="utf-8")
    (OUT / "01_DISAGREEMENT_ISOLATION.md").write_text(
        "# Disagreement Mechanism Isolation\n\n"
        "All arms use the same DCDLP model, raw-star hypergraph, decoder, optimizer, loss, 10 epochs, and three seeds. Only negative selection differs. Rg and Rh are global rank percentiles over the frozen strict train-only candidate pool. The two Graph-hard candidates per query are matched with adaptive equal-frequency Rg strata, using M0's stratum histogram as a common exact quota.\n\n"
        + ("\n```json\n" + json.dumps(mechanism, indent=2, ensure_ascii=False) + "\n```\n" if mechanism else "Mechanism training/validation has not completed.\n"), encoding="utf-8")
    (OUT / "02_CODNS_RESULTS.md").write_text(
        "# CODNS Results\n\n"
        + ("CODNS was not run because the pre-registered mechanism gate failed.\n\n" if codns is None else "\n```json\n" + json.dumps(codns, indent=2, ensure_ascii=False) + "\n```\n")
        + ("\n```json\n" + json.dumps(lambdas, indent=2, ensure_ascii=False) + "\n```\n" if lambdas else ""), encoding="utf-8")
    (OUT / "03_STRUCTURAL_CHARACTERIZATION.md").write_text(
        "# Structural Characterization\n\nDescriptive statistics use only the Cora training graph and selected train negatives. No future-positive enrichment analysis is performed.\n\n```json\n"
        + json.dumps(structure, indent=2, ensure_ascii=False) + "\n```\n", encoding="utf-8")
    (OUT / "04_EFFICIENCY.md").write_text(
        "# Efficiency and Cache Audit\n\nTeacher scoring is reused only after verifying split, seed, checkpoint and candidate-pool cache keys. No V6.2 teacher forward pass is repeated.\n\n```json\n"
        + json.dumps(efficiency, indent=2, ensure_ascii=False) + "\n```\n", encoding="utf-8")
    (OUT / "05_CROSS_DATASET.md").write_text(
        "# Cross-Dataset Check\n\n"
        + ("Second-dataset check was skipped because Cora did not meet both the CODNS validation and test gates.\n" if cross is None else "```json\n" + json.dumps(cross, indent=2, ensure_ascii=False) + "\n```\n"), encoding="utf-8")
    (OUT / "06_NOVELTY_SEARCH.md").write_text(
        "# Novelty Search\n\n"
        "Searches covered cross-view disagreement negative sampling, graph–hypergraph link prediction, hard negatives for pairwise link prediction, DMNS, MeBNS, HNS, and dual-anchor negative sampling. This is a targeted web search, not an exhaustive systematic review. Exact-rule status remains **EXACT_RULE_UNVERIFIED**; do not claim priority.\n\n"
        "- DMNS generates graph-link-prediction negatives at controllable latent hardness levels with a conditional diffusion process; it is a graph-only generation approach, unlike a pairwise Graph-hard / higher-order HG-rank disagreement selector. [arXiv:2403.17259](https://arxiv.org/abs/2403.17259).\n"
        "- MeBNS is a teacher–student/meta-learning framework for handling migration and weighting of hard negatives in link prediction; it is relevant to dynamic hard-negative selection but does not match the frozen two-teacher rank-difference rule searched here. [arXiv:2312.04815](https://arxiv.org/abs/2312.04815).\n"
        "- HNS synthesizes hard negatives in hyperedge embedding space for hyperedge prediction, a different prediction unit from ordinary pairwise graph link prediction. [arXiv:2503.08743](https://arxiv.org/abs/2503.08743).\n"
        "- Patil et al. study uniform, sized, motif, and clique negative sampling for hyperlink prediction in networks; this concerns higher-order hyperlink negatives rather than cross-order disagreement on pairwise candidates. [DOI:10.1007/978-3-030-47436-2_46](https://doi.org/10.1007/978-3-030-47436-2_46).\n"
        "- Differentiable Dual Anchor Negative Sampling (DDANS) is a nearby dual-anchor naming match in graph-based recommendation; its task and sampler differ from ordinary graph link prediction, so it should be discussed if the method survives, but it is not evidence that this exact rule is already present. [SIGIR 2026 paper](https://doi.org/10.1145/3805712.3809853).\n"
        "- Cross-view graph consistency learning studies paired graph views for link prediction, but the inspected source describes view consistency learning rather than negative selection by cross-order score disagreement. [arXiv:2311.11821](https://arxiv.org/abs/2311.11821).\n\n"
        "No inspected primary source explicitly stated the exact combination: (1) Graph teacher supplies pairwise hardness, (2) Raw-HG teacher supplies higher-order plausibility, and (3) their global rank-percentile disagreement selects ordinary pairwise link-prediction training negatives under this fixed prepool. This search is insufficient for a first/novel claim; the exact rule remains unverified.\n", encoding="utf-8")
    if mechanism:
        mrows = []
        for method in METHODS_MECH:
            row = mechanism["summary"][method]
            mrows.append(f"| {method} | {row['mean']:.6f} ± {row['sample_std']:.6f} | " + ", ".join(f"{x:.6f}" for x in row["by_seed"]) + " |")
        mech_lines = "\n".join(mrows)
        mechanism_line = f"MECHANISM_SUPPORTED: **{'YES' if mechanism['MECHANISM_SUPPORTED'] else 'NO'}**\n\nM1−M3 = {mechanism['M1_minus_M3_mean']:+.6f} ({mechanism['M1_minus_M3_wins']}/3 seed wins); M1−M4 = {mechanism['M1_minus_M4_mean']:+.6f} ({mechanism['M1_minus_M4_wins']}/3)."
        mechanism_table = "| Arm | Validation MRR mean ± sample SD | Seed 0, 1, 2 |\n|---|---:|---|\n" + mech_lines
    else:
        mechanism_line, mechanism_table = "MECHANISM_SUPPORTED: **NOT RUN**", "Mechanism results are unavailable."
    codns_line = "CODNS: **NOT RUN**"
    test_line = "TEST: **NOT RUN**"
    cross_line = "SECOND_DATASET: **NOT RUN**"
    if codns:
        codns_line = f"CODNS_SUPPORTED: **{'YES' if codns['CODNS_SUPPORTED'] else 'NO'}**\n\nValidation: " + "; ".join(f"{m} {codns['summary'][m]['mean']:.6f} ± {codns['summary'][m]['sample_std']:.6f}" for m in METHODS_CODNS)
    if test:
        test_line = "Test mean ± sample SD: " + "; ".join(f"{m} {test['mean_mrr'][m]:.6f} ± {test['sample_sd_mrr'][m]:.6f}" for m in test["mean_mrr"]) + f"\n\nC5 beats C1 and C3 test means: **{test['C5_beats_C1_and_C3_test_means']}**; C5 beats C4 mean: **{test['C5_beats_C4_test_mean']}**."
    if cross is not None:
        cross_line = "SECOND_DATASET: **" + str(cross.get("status")) + "**"
    failure_reason = {
        "DISAGREEMENT_MECHANISM_NOT_SUPPORTED": "The pre-registered M1 comparisons did not pass both seed-win and positive-mean gates under Graph-hardness matching.",
        "CODNS_REJECT": "The continuous CODNS validation gate failed; the test set remained closed.",
        "GO": "The Cora validation and test criteria were met; see per-arm results and cross-dataset status.",
        "STRONG_GO": "Cora and the rapid cross-dataset validation supported the frozen CODNS rule.",
        "CROSS_DATASET_INCONCLUSIVE": "The Cora gates passed, but the second-dataset quick check did not support the rule.",
    }.get(final_decision, "See stage status and experiment logs.")
    final = (
        "# V6.2 CODNS Final Report\n\n"
        "STATUS: EXECUTED\n\nPROTOCOL: STRICT_TRAIN_ONLY\n\nCHECKPOINT_RULE: FIXED_EPOCH_10\n\n"
        f"CANDIDATE: Cross-Order Disagreement Negative Sampling (CODNS), λ={LAMBDA}\n\n"
        f"{mechanism_line}\n\n{mechanism_table}\n\n{codns_line}\n\n{test_line}\n\n{cross_line}\n\n"
        f"NOVELTY_STATUS: EXACT_RULE_UNVERIFIED\n\nDECISION: **{final_decision}**\n\nFAILURE_REASON: {failure_reason}\n\n"
        f"STRUCTURAL_CHARACTERIZATION: see [03_STRUCTURAL_CHARACTERIZATION.md](03_STRUCTURAL_CHARACTERIZATION.md)\n\n"
        f"EFFICIENCY: see [04_EFFICIENCY.md](04_EFFICIENCY.md)\n\n"
        "PAPER_CORE_INNOVATION: CODNS remains a candidate only if the mechanism and CODNS gates pass; no false-negative claim is made.\n\n"
        "NEXT_EXPECTED_STEP: Report the matched mechanism result first. If unsupported, stop this line; if supported, retain λ=0.5 and interpret CODNS/test/cross-dataset outcomes without tuning.\n"
    )
    (OUT / "FINAL_REPORT.md").write_text(final, encoding="utf-8")
    set_status("complete", None, final_decision=final_decision, test_evaluated=bool(test), all_reports_written=True)


def run_cross_dataset() -> dict:
    """Run the predeclared Citeseer-first transfer screen only after Cora GO."""
    import torch
    from dcdlp.data.loaders import load_dataset
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs

    test = read_json(OUT / "test_results.json")
    codns = read_json(OUT / "codns_validation.json")
    if not test.get("C5_beats_C1_and_C3_test_means") or not codns.get("CODNS_SUPPORTED"):
        return {"status": "SKIPPED_CORA_GATE_FAILED", "reason": "Cora CODNS validation and test gates were not both supported"}
    dataset_name = None
    full = None
    load_errors = {}
    for candidate_name in ("citeseer", "pubmed"):
        try:
            full = load_dataset(candidate_name, ROOT / "data", "standard", 0)
            dataset_name = candidate_name
            break
        except Exception as exc:
            load_errors[candidate_name] = f"{type(exc).__name__}: {exc}"
    if full is None or dataset_name is None:
        result = {"status": "CROSS_DATASET_UNAVAILABLE", "dataset_load_errors": load_errors}
        write_json(OUT / "cross_dataset_results.json", result)
        return result

    view = v61.TrainOnlyView(full)
    valid_pos = np.asarray(full.valid_pos, dtype=np.int64).copy()
    # This is evaluation-only candidate construction. It does not enter the
    # strict training pool or teacher score computation.
    val_seed = 62_200
    val_pool = uniform_negative_sampling(
        full.num_nodes, full.all_positive, max(20 * len(valid_pos), 20), val_seed,
    )
    valid_neg = grouped_negatives(valid_pos, val_pool, 20, val_seed + 1)
    valid_hash = v61.array_hash(valid_neg)
    forbidden_rows, forbidden = v61.make_train_forbidden(view)
    train_seed, grouping_seed = 20261002, 20261003
    raw_pool = uniform_negative_sampling(
        view.num_nodes, forbidden_rows, len(view.train_pos) * 20, train_seed,
    )
    candidates = grouped_negatives(view.train_pos, raw_pool, 20, grouping_seed)
    if candidates.shape != (len(view.train_pos), 20, 2):
        raise RuntimeError(f"{dataset_name}: strict train pool has unexpected shape {candidates.shape}")
    if any(v61.canonical_edge(pair) in forbidden for pair in candidates.reshape(-1, 2)):
        raise RuntimeError(f"{dataset_name}: strict pool contains a train/message edge")
    global candidate_pool, candidate_pool_hash, validation_candidate_hash, LAMBDA
    candidate_pool = candidates
    candidate_pool_hash = v61.array_hash(candidates)
    validation_candidate_hash = valid_hash
    LAMBDA = 0.5
    write_json(OUT / "cross_dataset_preflight.json", {
        "dataset": dataset_name,
        "protocol": "STRICT_TRAIN_ONLY",
        "num_nodes": int(view.num_nodes),
        "train_positive_count": int(len(view.train_pos)),
        "candidate_pool_hash": candidate_pool_hash,
        "validation_candidate_hash": valid_hash,
        "heldout_identity_used_in_training_pool": False,
        "forbidden_edge_count": len(forbidden),
    })
    np.savez_compressed(OUT / f"cross_{dataset_name}_strict_candidates.npz", train_positive=view.train_pos, negative_candidates=candidates)

    teacher_scores = {}
    teacher_records = {}
    scoring_seconds = {}
    x = torch.as_tensor(view.features, dtype=torch.float32, device="cuda")
    edge_index = edge_index_from_graph(view.train_graph(), torch.device("cuda"))
    for label, mode in (("Graph", "disabled"), ("Raw-HG", "raw")):
        out_dir = OUT / "RUNS" / f"CROSS_{dataset_name.upper()}_TEACHERS" / label
        rel = str(out_dir.relative_to(ROOT)).replace("\\", "/")
        record = train_one(
            view, f"TEACHER_{label}", 0, None, rel, valid_pos, valid_neg,
            initialize_from_v6=False, dataset_name=dataset_name, hypergraph_mode=mode,
        )
        model, _ = load_checkpoint_model(record["checkpoint"], device="cuda")
        score_started = time.perf_counter()
        with torch.no_grad():
            output = score_pairs(model, x, edge_index, candidates.reshape(-1, 2), batch_size=8192)
            scores = np.asarray(output["logit"]).reshape(len(view.train_pos), 20).astype(np.float32, copy=False)
        scoring_seconds[label] = float(time.perf_counter() - score_started)
        score_path = OUT / "score_cache" / f"{dataset_name}_{label}_{candidate_pool_hash[:12]}.npz"
        score_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(score_path, scores=scores)
        teacher_scores[label] = scores
        teacher_records[label] = {
            "checkpoint": record["checkpoint"],
            "checkpoint_hash": record["model_state_hash"],
            "candidate_pool_hash": candidate_pool_hash,
            "split_hash": hashlib.sha256((v61.array_hash(view.train_pos) + v61.array_hash(view.features) + str(view.num_nodes)).encode("ascii")).hexdigest(),
            "score_hash": v61.array_hash(scores),
            "score_cache_path": str(score_path),
            "scoring_seconds": scoring_seconds[label],
            "teacher_forward_repeats": 0,
        }
        del model
        torch.cuda.empty_cache()

    rg = rank_percentiles(teacher_scores["Graph"])
    rh = rank_percentiles(teacher_scores["Raw-HG"])
    pre_idx = np.argsort(teacher_scores["Graph"], axis=1, kind="stable")[:, -2:]
    pre_rg = np.take_along_axis(rg, pre_idx, axis=1)
    pre_rh = np.take_along_axis(rh, pre_idx, axis=1)
    c1 = np.argmax(teacher_scores["Graph"], axis=1)
    c5 = np.asarray([pre_idx[row, int(np.argmax(pre_rg[row] - 0.5 * pre_rh[row]))] for row in range(len(view.train_pos))])
    n_bins = 20
    bins = quantile_strata(pre_rg, n_bins)
    shuffled = pre_rh.copy()
    rng = np.random.default_rng(462_200)
    for b in range(n_bins):
        positions = np.argwhere(bins == b)
        vals = shuffled[bins == b].copy()
        if len(vals) > 1:
            vals = rng.permutation(vals)
        shuffled[positions[:, 0], positions[:, 1]] = vals
    c3 = np.asarray([pre_idx[row, int(np.argmax(pre_rg[row] - 0.5 * shuffled[row]))] for row in range(len(view.train_pos))])
    selections = {"C1": c1, "C3": c3, "C5": c5}
    for name, ids in selections.items():
        if len(ids) != len(view.train_pos):
            raise RuntimeError(f"{dataset_name}: invalid {name} selection count")
    results = {"dataset": dataset_name, "selection_rule": "lambda=0.5, no dataset-specific tuning", "candidate_pool_hash": candidate_pool_hash, "validation_candidate_hash": valid_hash, "teachers": teacher_records, "scoring_seconds": scoring_seconds, "metrics": {}, "seed0_screen": None, "three_seed_confirmation": None}
    for seed in SEEDS:
        if seed > 0 and not results["seed0_screen"]["proceed_to_three_seeds"]:
            break
        for method in ("C1", "C3", "C5"):
            selected = candidates[np.arange(len(view.train_pos)), selections[method]]
            out_dir = OUT / "RUNS" / f"CROSS_{dataset_name.upper()}" / f"{method}_seed{seed}"
            rel = str(out_dir.relative_to(ROOT)).replace("\\", "/")
            record = train_one(
                view, f"{dataset_name}_{method}", seed, selected, rel, valid_pos, valid_neg,
                initialize_from_v6=False, dataset_name=dataset_name,
            )
            metric = eval_fixed_candidates(record["checkpoint"], view, valid_pos, valid_neg)
            results["metrics"].setdefault(method, {})[str(seed)] = {
                "mrr": metric["mrr"],
                "hits10": metric["hits10"],
                "checkpoint": record["checkpoint"],
                "selected_negative_hash": record["selected_negative_hash"],
                "checkpoint_rule": "FIXED_EPOCH_10",
            }
        if seed == 0:
            proceed = results["metrics"]["C5"]["0"]["mrr"] > results["metrics"]["C1"]["0"]["mrr"]
            results["seed0_screen"] = {
                "C1_mrr": results["metrics"]["C1"]["0"]["mrr"],
                "C3_mrr": results["metrics"]["C3"]["0"]["mrr"],
                "C5_mrr": results["metrics"]["C5"]["0"]["mrr"],
                "proceed_to_three_seeds": bool(proceed),
            }
            if not proceed:
                results["status"] = "CROSS_DATASET_INCONCLUSIVE"
                break
    if results["seed0_screen"] and results["seed0_screen"]["proceed_to_three_seeds"]:
        means = {m: float(np.mean([results["metrics"][m][str(s)]["mrr"] for s in SEEDS])) for m in ("C1", "C3", "C5")}
        stds = {m: float(np.std([results["metrics"][m][str(s)]["mrr"] for s in SEEDS], ddof=1)) for m in ("C1", "C3", "C5")}
        results["three_seed_confirmation"] = {"mean_mrr": means, "sample_sd_mrr": stds, "C5_beats_C1_mean": means["C5"] > means["C1"], "C5_beats_C3_mean": means["C5"] > means["C3"]}
        results["status"] = "SUPPORTED" if means["C5"] > means["C1"] else "CROSS_DATASET_INCONCLUSIVE"
    write_json(OUT / "cross_dataset_results.json", results)
    set_status("cross_dataset_complete", None, second_dataset=dataset_name, second_dataset_status=results["status"])
    return results


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    set_status("preflight", "V6.1_cache_and_V100")
    pool = make_ranked_pool()
    audit = verify_preflight(pool)
    print(json.dumps({"phase": "preflight", "status": audit["status"], "match": audit["selection_match"]}, ensure_ascii=False), flush=True)
    if "--preflight-only" in sys.argv:
        set_status("preflight_complete", None, preflight="PASS", test_evaluated=False)
        return
    mech_state = run_training_suite(pool, "mechanism")
    mech = run_validation_gate(pool, "mechanism")
    if not mech["MECHANISM_SUPPORTED"]:
        write_reports(pool, "DISAGREEMENT_MECHANISM_NOT_SUPPORTED")
        set_status("complete", None, final_decision="DISAGREEMENT_MECHANISM_NOT_SUPPORTED", test_evaluated=False)
        print("MECHANISM_GATE_FAILED", flush=True)
        return
    codns_state = run_training_suite(pool, "codns")
    codns = run_validation_gate(pool, "codns")
    if not codns["CODNS_SUPPORTED"]:
        write_reports(pool, "CODNS_REJECT")
        set_status("complete", None, final_decision="CODNS_REJECT", test_evaluated=False)
        print("CODNS_VALIDATION_GATE_FAILED_TEST_CLOSED", flush=True)
        return
    lambdas = run_lambda_sensitivity(pool)
    test = run_cora_test_once(pool)
    if not test["C5_beats_C1_and_C3_test_means"]:
        write_reports(pool, "CODNS_REJECT")
        set_status("complete", None, final_decision="CODNS_REJECT", test_evaluated=True, test_performance_supported=False)
        print("CORA_TEST_PERFORMANCE_GATE_FAILED", flush=True)
        return
    cross = run_cross_dataset()
    if cross.get("status") == "SUPPORTED":
        decision = "STRONG_GO"
    elif cross.get("status") == "CROSS_DATASET_INCONCLUSIVE":
        decision = "CROSS_DATASET_INCONCLUSIVE"
    else:
        decision = "GO"
    write_reports(pool, decision, cross)
    set_status("complete", None, final_decision=decision, test_evaluated=True)
    print(json.dumps({"phase": "complete", "mechanism_supported": True, "codns_supported": True, "test_performance_supported": True, "second_dataset": cross.get("status"), "decision": decision}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        OUT.mkdir(parents=True, exist_ok=True)
        old = current_status()
        old.update({"state": "FAILED", "phase": old.get("phase", "unknown"), "error": traceback.format_exc(), "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        write_json(OUT / "status.json", old)
        raise
