"""V6.1 strict train-only hypergraph-verified false-negative experiment.

The training phase operates on a train-only view. Validation and test identities
are loaded only in later, separate evaluation phases after all training choices
and checkpoints have been frozen.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
import time
import traceback
from pathlib import Path
from typing import Iterable

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
OUT = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
V6 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6"
V5 = ROOT / "HYPERGRAPH_RESEARCH" / "COMPLEMENT_V5"
BASELINE = V5 / "A_GHHR" / "remote_evidence" / "baseline_10_epoch"
SEEDS = (0, 1, 2)
METHODS = ("A1", "A3", "A4")
POOL_PER_POSITIVE = 20
POOL_SEED = 20261002
GROUPING_SEED = 20261003
EVAL_NEGATIVES = 20
VETO_RATIO = 0.25
PREPOOL_MULTIPLIER = 2
BOOTSTRAPS = 5000
INITIAL_HASH_EXPECTED = "966ac47231c28a65b16a18ae1638e4db4fefd8d7861f7ec105c6b0f942351c69"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    temporary.replace(path)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def array_hash(array: object) -> str:
    value = np.ascontiguousarray(np.asarray(array))
    digest = hashlib.sha256()
    digest.update(str(value.dtype).encode("ascii"))
    digest.update(json.dumps(value.shape).encode("ascii"))
    digest.update(value.tobytes())
    return digest.hexdigest()


def canonical_edge(edge: Iterable[int]) -> tuple[int, int]:
    u, v = map(int, edge)
    return (u, v) if u <= v else (v, u)


def filter_eligible_candidates(
    candidates: np.ndarray, forbidden: set[tuple[int, int]], num_nodes: int,
) -> np.ndarray:
    """Apply only train-derived pair, node-range, and self-loop constraints."""
    kept = [
        canonical_edge(pair) for pair in np.asarray(candidates, dtype=np.int64).reshape(-1, 2)
        if 0 <= int(pair[0]) < num_nodes
        and 0 <= int(pair[1]) < num_nodes
        and int(pair[0]) != int(pair[1])
        and canonical_edge(pair) not in forbidden
    ]
    return np.asarray(kept, dtype=np.int64).reshape(-1, 2)


def strict_eligibility_unit_test() -> dict:
    """A future edge is passed only to the test harness, never to the filter."""
    train_forbidden = {(0, 1), (1, 2)}
    heldout_identity_for_test_harness_only = (3, 4)
    ordinary_unknown = (4, 5)
    candidates = np.asarray([
        heldout_identity_for_test_harness_only, ordinary_unknown, (0, 1), (6, 6),
    ], dtype=np.int64)
    observed = filter_eligible_candidates(candidates, train_forbidden, 8)
    observed_set = {canonical_edge(edge) for edge in observed}
    assert canonical_edge(heldout_identity_for_test_harness_only) in observed_set
    assert canonical_edge(ordinary_unknown) in observed_set
    assert canonical_edge((0, 1)) not in observed_set
    assert canonical_edge((6, 6)) not in observed_set
    return {
        "status": "PASS",
        "future_edge_and_ordinary_unknown_use_same_train_only_predicate": True,
        "future_edge_identity_is_not_an_input_to_filter": True,
        "train_positive_and_self_loop_rejected": True,
    }


def run_preflight() -> None:
    import torch

    from dcdlp.data.loaders import load_dataset
    from dcdlp.utils import array_hash as project_array_hash

    if not torch.cuda.is_available() or "V100" not in torch.cuda.get_device_name(0):
        raise RuntimeError("V6.1 requires the registered CUDA V100 server")
    scipy_available = True
    try:
        import scipy  # noqa: F401
    except ImportError:
        scipy_available = False
    loaded = load_dataset("cora", ROOT / "data", "standard", 0)
    view = TrainOnlyView(loaded)
    del loaded
    rows, forbidden = make_train_forbidden(view)
    test = strict_eligibility_unit_test()
    initial_state = torch.load(BASELINE / "raw_initial_state.pt", map_location="cpu", weights_only=True)
    digest = hashlib.sha256()
    for key in sorted(initial_state):
        value = initial_state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(value.numpy().tobytes())
    init_hash = digest.hexdigest()
    if init_hash != INITIAL_HASH_EXPECTED:
        raise RuntimeError(f"Frozen initial-state hash mismatch: {init_hash}")
    from dcdlp.models.dcdlp import DCDLP
    from dcdlp.train import ablation_profile

    raw_config = load_json(BASELINE / "H" / "config.json")
    profile = ablation_profile("A5")
    compatibility = {}
    for hg_mode in ("disabled", "raw"):
        model = DCDLP(
            view.features.shape[1], raw_config["hidden_dim"], raw_config["branch_dim"],
            raw_config["num_layers"], raw_config["dropout"], raw_config["backbone"],
            use_interaction=profile["interaction"], active_branches=profile["active"],
            decoder_mode=profile["decoder"], cn_feature_mode=raw_config["cn_feature_mode"],
            interaction_mode=raw_config["interaction_mode"], cn_input_schema=raw_config["cn_input_schema"],
            hypergraph_mode=hg_mode, hypergraph_construction=raw_config["hypergraph_construction"],
        )
        incompatible = model.load_state_dict(initial_state, strict=False)
        bad_missing = [key for key in incompatible.missing_keys if not key.startswith("hypergraph.")]
        bad_unexpected = [key for key in incompatible.unexpected_keys if not key.startswith("hypergraph.")]
        if bad_missing or bad_unexpected:
            raise RuntimeError(f"V6 initial-state compatibility failed for {hg_mode}: {incompatible}")
        compatibility[hg_mode] = {
            "allowed_missing_hypergraph_keys": list(incompatible.missing_keys),
            "allowed_unexpected_hypergraph_keys": list(incompatible.unexpected_keys),
        }
        del model
    filtered_paths = []
    for method in METHODS:
        for seed in SEEDS:
            path = (V6 / "A_HG_VETO" / f"{method}_seed0" / "metrics.json") if seed == 0 else (V6 / "A_HG_VETO" / "confirmation" / f"{method}_seed{seed}" / "metrics.json")
            value = load_json(path)
            if value.get("seed") != seed or value.get("validation", {}).get("mrr") is None:
                raise RuntimeError(f"Invalid exact V6 filtered result: {path}")
            filtered_paths.append(str(path))
    with np.load(V6 / "fixed_validation_candidates.npz", allow_pickle=False) as candidates:
        valid_neg = candidates["valid_negative_candidates"]
    valid_hash = project_array_hash(valid_neg)
    expected_valid = load_json(V6 / "fixed_validation_candidates.json")["negative_candidates_hash"]
    if valid_hash != expected_valid:
        raise RuntimeError("V6 fixed validation candidate cache failed hash audit")
    report = {
        "status": "PASS",
        "gpu": torch.cuda.get_device_name(0),
        "torch": torch.__version__,
        "scipy_available": scipy_available,
        "cora_train_positive_count": len(view.train_pos),
        "num_nodes": view.num_nodes,
        "train_only_forbidden_edge_count": len(forbidden),
        "train_only_forbidden_hash": project_array_hash(rows),
        "initial_state_hash": init_hash,
        "matched_initial_state_compatibility": compatibility,
        "fixed_validation_candidate_hash": valid_hash,
        "filtered_runs_present": len(filtered_paths),
        "heldout_eligibility_unit_test": test,
    }
    write_json(OUT / "preflight.json", report)
    print(json.dumps(report, ensure_ascii=False), flush=True)


class TrainOnlyView:
    """Whitelisted training data plus empty placeholders for legacy train API."""

    def __init__(self, source):
        self.name = str(source.name)
        self.num_nodes = int(source.num_nodes)
        self.features = np.asarray(source.features).copy()
        self.train_pos = np.asarray(source.train_pos, dtype=np.int64).copy()
        self._empty = np.empty((0, 2), dtype=np.int64)
        self.placeholder_reads = {"valid_pos": 0, "test_pos": 0}

    @property
    def valid_pos(self):
        self.placeholder_reads["valid_pos"] += 1
        return self._empty

    @property
    def test_pos(self):
        self.placeholder_reads["test_pos"] += 1
        return self._empty

    @property
    def valid_neg(self):
        return None

    @property
    def test_neg(self):
        return None

    @property
    def all_positive(self):
        raise AssertionError("STRICT_TRAIN_ONLY must never access all_positive")

    def train_graph(self):
        import networkx as nx

        graph = nx.Graph()
        graph.add_nodes_from(range(self.num_nodes))
        graph.add_edges_from(map(tuple, self.train_pos.tolist()))
        return graph


def make_train_forbidden(view: TrainOnlyView) -> tuple[np.ndarray, set[tuple[int, int]]]:
    graph_edges = np.asarray(list(view.train_graph().edges()), dtype=np.int64).reshape(-1, 2)
    pieces = [view.train_pos, graph_edges]
    joined = np.sort(np.vstack(pieces), axis=1)
    unique = np.unique(joined, axis=0)
    forbidden = {tuple(map(int, pair)) for pair in unique.tolist()}
    return unique, forbidden


def run_train_only_phase() -> None:
    import torch

    from dcdlp.data.loaders import load_dataset
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp import train as train_module
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import TrainConfig, edge_index_from_graph, score_pairs

    OUT.mkdir(parents=True, exist_ok=True)
    status = {"state": "RUNNING", "phase": "train_only", "completed": [], "test_evaluated": False}
    write_json(OUT / "status.json", status)
    test_audit = strict_eligibility_unit_test()

    started = time.perf_counter()
    loaded = load_dataset("cora", ROOT / "data", "standard", 0)
    view = TrainOnlyView(loaded)
    del loaded
    train_forbidden_rows, train_forbidden = make_train_forbidden(view)
    if any(u == v for u, v in train_forbidden):
        raise RuntimeError("self-loop unexpectedly present in train forbidden set")
    split_hash = hashlib.sha256(
        (array_hash(view.train_pos) + array_hash(view.features) + str(view.num_nodes)).encode("ascii")
    ).hexdigest()

    pool_started = time.perf_counter()
    ungrouped_pool = uniform_negative_sampling(
        view.num_nodes, train_forbidden_rows, len(view.train_pos) * POOL_PER_POSITIVE, POOL_SEED,
    )
    grouped = grouped_negatives(view.train_pos, ungrouped_pool, POOL_PER_POSITIVE, GROUPING_SEED)
    pool_seconds = time.perf_counter() - pool_started
    if len(grouped) != len(view.train_pos) or grouped.shape[1:] != (POOL_PER_POSITIVE, 2):
        raise RuntimeError(f"Unexpected strict pool shape: {grouped.shape}")
    for row in grouped.reshape(-1, 2):
        if canonical_edge(row) in train_forbidden:
            raise RuntimeError("strict candidate pool contains a train/message edge")
    pool_hash = array_hash(grouped)

    initial_state_path = BASELINE / "raw_initial_state.pt"
    initial_state = torch.load(initial_state_path, map_location="cpu", weights_only=True)
    from dcdlp.utils import stable_hash

    def state_hash(state: dict) -> str:
        digest = hashlib.sha256()
        for key in sorted(state):
            value = state[key].detach().cpu().contiguous()
            digest.update(key.encode("utf-8"))
            digest.update(str(value.dtype).encode("ascii"))
            digest.update(value.numpy().tobytes())
        return digest.hexdigest()

    init_hash = state_hash(initial_state)
    if init_hash != INITIAL_HASH_EXPECTED:
        raise RuntimeError(f"Frozen V6 initial state mismatch: {init_hash}")

    old_sampler = train_module._sample_train_negatives
    old_eval = train_module.evaluate_split
    old_residualizer = train_module.fit_training_cn_residualizer
    old_optimizer = train_module._build_optimizer

    def make_config(seed: int, output_dir: str, hypergraph_mode: str):
        raw = load_json(BASELINE / "H" / "config.json")
        values = {key: value for key, value in raw.items() if key in TrainConfig.__dataclass_fields__}
        values.update({
            "seed": int(seed), "protocol_train": "uniform", "protocol_eval": "standard",
            "pretrain_epochs": 10, "disentangle_epochs": 0, "hypergraph_mode": hypergraph_mode,
            "hypergraph_construction": "raw_star", "ghhr_training_mode": "none",
            "complementarity_fusion_mode": "none", "evaluate_test": False,
            "device": "cuda", "output_dir": output_dir, "prediction_subdir": "raw",
        })
        return TrainConfig(**values)

    train_clock: dict[str, float] = {}

    def run_isolated_training(label: str, mode: str, seed: int, output_rel: str,
                              selected: np.ndarray | None = None, initialize_from_v6: bool = False):
        config = make_config(seed, output_rel, mode)
        validation_counter = {"n": 0}
        epoch_negatives: list[np.ndarray] = []

        def sampler(current_dataset, current_config, epoch):
            if current_dataset is not view or current_config is not config:
                raise RuntimeError("strict sampler was called outside the train-only view")
            if selected is not None:
                negative = np.asarray(selected, dtype=np.int64).copy()
            else:
                negative = uniform_negative_sampling(
                    view.num_nodes, train_forbidden_rows, len(view.train_pos),
                    int(seed) * 10_000 + int(epoch),
                )
            if len(negative) != len(view.train_pos):
                raise RuntimeError("strict epoch sampler returned an unexpected count")
            if any(canonical_edge(pair) in train_forbidden for pair in negative):
                raise RuntimeError("strict sampler emitted a train/message edge")
            epoch_negatives.append(negative.copy())
            return negative

        def no_heldout_evaluation(*_args, **_kwargs):
            # Monotone sentinel forces train_model's legacy best-state holder to
            # retain epoch 10 without reading validation labels or candidates.
            validation_counter["n"] += 1
            return {"mrr": float(validation_counter["n"])}, []

        def no_cn_residualizer(_dataset, _config):
            return None, {
                "residualizer_type": "NOT_USED", "fit_split": "train_only",
                "uses_valid_or_test": False, "used_as_model_input": False,
            }

        def matched_optimizer(model, probes, current_config):
            if current_config is config and initialize_from_v6:
                incompat = model.load_state_dict(initial_state, strict=False)
                bad_missing = [key for key in incompat.missing_keys if not key.startswith("hypergraph.")]
                bad_unexpected = [key for key in incompat.unexpected_keys if not key.startswith("hypergraph.")]
                if bad_missing or bad_unexpected:
                    raise RuntimeError(f"Matched V6 initial state mismatch: {incompat}")
            return old_optimizer(model, probes, current_config)

        train_module._sample_train_negatives = sampler
        train_module.evaluate_split = no_heldout_evaluation
        train_module.fit_training_cn_residualizer = no_cn_residualizer
        train_module._build_optimizer = matched_optimizer
        run_started = time.perf_counter()
        try:
            model, result = train_module.train_model(view, config)
        finally:
            train_module._sample_train_negatives = old_sampler
            train_module.evaluate_split = old_eval
            train_module.fit_training_cn_residualizer = old_residualizer
            train_module._build_optimizer = old_optimizer
        if validation_counter["n"] != 10 or len(epoch_negatives) != 10:
            raise RuntimeError(f"{label} seed {seed} did not complete 10 fixed epochs")

        # Remove the synthetic checkpoint-holder signal from the persisted audit.
        result["validation"] = {"checkpoint_rule": "fixed_final_epoch_10", "heldout_evaluation_used": False}
        result["validation_curve"] = []
        result["best_epoch"] = 9
        result["checkpoint_selection_audit"] = {
            "rule": "fixed_final_epoch_10",
            "validation_or_test_metrics_used": False,
            "legacy_train_api_placeholder_reads": dict(view.placeholder_reads),
            "heldout_identity_values_exposed": 0,
        }
        result["data_integrity"] = {
            "train_positive_hash": array_hash(view.train_pos),
            "train_only_split_hash": split_hash,
            "valid_positive_hash": "NOT_ACCESSED",
            "test_positive_hash": "NOT_ACCESSED",
            "candidate_hash": pool_hash,
        }
        result["strict_train_negative_hashes_by_epoch"] = [array_hash(x) for x in epoch_negatives]
        result["runtime"]["train_seconds"] = float(result["runtime"]["train_seconds"])
        result_path = Path(result["result_file"])
        write_json(result_path, result)
        train_clock[label] = float(result["runtime"]["train_seconds"])
        del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return result

    try:
        teacher_dir = OUT / "TEACHERS"
        teacher_records = {}
        for view_name, hg_mode in (("Graph", "disabled"), ("Raw-HG", "raw")):
            status.update({"current": f"teacher_{view_name}", "completed": []})
            write_json(OUT / "status.json", status)
            rel = str((teacher_dir / view_name).relative_to(ROOT)).replace("\\", "/")
            res = run_isolated_training(
                f"teacher_{view_name}", hg_mode, 0, rel, selected=None, initialize_from_v6=True,
            )
            model, _ = load_checkpoint_model(Path(res["checkpoint"]), device="cuda")
            teacher_records[view_name] = {
                "checkpoint": str(res["checkpoint"]),
                "checkpoint_hash": state_hash(model.state_dict()),
                "train_seconds": float(res["runtime"]["train_seconds"]),
                "selection_rule": "fixed_final_epoch_10; no validation/test checkpoint selection",
            }
            del model
            torch.cuda.empty_cache()

        x = torch.as_tensor(view.features, dtype=torch.float32, device="cuda")
        edge_index = edge_index_from_graph(view.train_graph(), torch.device("cuda"))
        flat = grouped.reshape(-1, 2)
        scores: dict[str, np.ndarray] = {}
        scoring_seconds = {}
        cache_meta = {}
        cache_dir = OUT / "score_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        for view_name in ("Graph", "Raw-HG"):
            cache_key = stable_hash({
                "train_split_hash": split_hash, "seed": 0,
                "checkpoint_hash": teacher_records[view_name]["checkpoint_hash"],
                "candidate_pool_hash": pool_hash, "teacher": view_name,
            })
            cache_npz = cache_dir / f"{view_name}_{cache_key}.npz"
            cache_json = cache_dir / f"{view_name}_{cache_key}.json"
            if cache_npz.exists() and cache_json.exists():
                meta = load_json(cache_json)
                if meta.get("cache_key") != cache_key:
                    raise RuntimeError("detached teacher-score cache key mismatch")
                with np.load(cache_npz, allow_pickle=False) as saved:
                    values = saved["scores"]
                scoring_seconds[view_name] = 0.0
                meta["cache_hit"] = True
            else:
                model, _ = load_checkpoint_model(teacher_records[view_name]["checkpoint"], device="cuda")
                score_started = time.perf_counter()
                with torch.no_grad():
                    output = score_pairs(model, x, edge_index, flat, batch_size=8192)
                    values = np.asarray(output["logit"]).reshape(
                        len(view.train_pos), POOL_PER_POSITIVE
                    ).astype(np.float32, copy=False)
                scoring_seconds[view_name] = time.perf_counter() - score_started
                np.savez_compressed(cache_npz, scores=values)
                meta = {
                    "cache_key": cache_key, "train_split_hash": split_hash, "seed": 0,
                    "checkpoint_hash": teacher_records[view_name]["checkpoint_hash"],
                    "candidate_pool_hash": pool_hash, "teacher": view_name,
                    "detached": True, "score_hash": array_hash(values),
                    "forward_seconds": scoring_seconds[view_name], "cache_hit": False,
                }
                write_json(cache_json, meta)
                del model, output
                torch.cuda.empty_cache()
            if values.shape != (len(view.train_pos), POOL_PER_POSITIVE):
                raise RuntimeError(f"bad cached score shape {view_name}: {values.shape}")
            scores[view_name] = values
            cache_meta[view_name] = meta

        selection_started = time.perf_counter()
        graph_pre = np.argsort(scores["Graph"], axis=1, kind="stable")[:, -PREPOOL_MULTIPLIER:]
        hg_rank = np.argsort(np.argsort(scores["Raw-HG"], axis=1, kind="stable"), axis=1, kind="stable")
        graph_hard_idx = scores["Graph"].argmax(axis=1)
        true_hg_high_local = hg_rank[np.arange(len(grouped))[:, None], graph_pre].argmax(axis=1)
        true_veto_idx = graph_pre[np.arange(len(grouped)), true_hg_high_local]
        a4_idx = graph_pre[np.arange(len(grouped)), 1 - true_hg_high_local]
        selected_by_seed = {}
        selection_seconds = {"A1": 0.0, "A3": 0.0, "A4": 0.0}
        for seed in SEEDS:
            rng_shuf = np.random.default_rng(400_000 + seed * 10_000)
            shuffled_idx = np.empty(len(grouped), dtype=np.int64)
            for row in range(len(grouped)):
                shuffled_ranks = rng_shuf.permutation(hg_rank[row])
                local = int(np.argmax(shuffled_ranks[graph_pre[row]]))
                shuffled_idx[row] = graph_pre[row, 1 - local]
            selected_by_seed[f"S_A1_seed{seed}"] = grouped[np.arange(len(grouped)), graph_hard_idx]
            selected_by_seed[f"S_A3_seed{seed}"] = grouped[np.arange(len(grouped)), shuffled_idx]
            selected_by_seed[f"S_A4_seed{seed}"] = grouped[np.arange(len(grouped)), a4_idx]
        # Recompute veto indices directly, avoiding pair-identity ambiguity if rows overlap.
        veto_indices_by_seed = {"true": np.asarray(true_veto_idx, dtype=np.int64)}
        for seed in SEEDS:
            rng = np.random.default_rng(400_000 + seed * 10_000)
            veto_cols = np.empty(len(grouped), dtype=np.int64)
            for row in range(len(grouped)):
                shuffled_ranks = rng.permutation(hg_rank[row])
                veto_cols[row] = graph_pre[row, int(np.argmax(shuffled_ranks[graph_pre[row]]))]
            veto_indices_by_seed[f"shuffled_{seed}"] = veto_cols
            rng_random = np.random.default_rng(400_000 + seed * 10_000)
            drop_local = rng_random.integers(0, PREPOOL_MULTIPLIER, size=len(grouped))
            veto_indices_by_seed[f"random_{seed}"] = graph_pre[np.arange(len(grouped)), drop_local]
        selection_seconds_total = time.perf_counter() - selection_started

        archive = {
            "train_positive": view.train_pos,
            "negative_candidates": grouped,
            "score_graph": scores["Graph"],
            "score_raw_hg": scores["Raw-HG"],
            "graph_prepool_indices": graph_pre,
            "graph_hard_indices": graph_hard_idx,
            "true_veto_indices": true_veto_idx,
            "a4_indices": a4_idx,
        }
        for seed in SEEDS:
            for key in (f"S_A1_seed{seed}", f"S_A3_seed{seed}", f"S_A4_seed{seed}"):
                archive[key] = selected_by_seed[key]
            archive[f"veto_shuffled_seed{seed}"] = veto_indices_by_seed[f"shuffled_{seed}"]
            archive[f"veto_random_seed{seed}"] = veto_indices_by_seed[f"random_{seed}"]
        np.savez_compressed(OUT / "strict_train_candidates_and_selections.npz", **archive)

        pool_meta = {
            "protocol": "STRICT_TRAIN_ONLY",
            "candidate_pool_hash": pool_hash,
            "train_positive_hash": array_hash(view.train_pos),
            "train_only_split_hash": split_hash,
            "num_nodes": view.num_nodes,
            "train_positive_count": len(view.train_pos),
            "candidate_count": int(grouped.size // 2),
            "candidate_count_per_positive": POOL_PER_POSITIVE,
            "pool_seed": POOL_SEED,
            "grouping_seed": GROUPING_SEED,
            "forbidden_sources": ["training positives", "training/message graph observed edges", "self-loops", "out-of-range pairs"],
            "forbidden_edge_count": len(train_forbidden),
            "forbidden_edge_hash": array_hash(train_forbidden_rows),
            "heldout_positive_identities_read_by_miner": False,
            "all_positive_access_attempts": 0,
            "eligibility_unit_test": test_audit,
            "teacher_records": teacher_records,
            "score_cache": cache_meta,
            "pool_generation_seconds": pool_seconds,
            "teacher_scoring_seconds": scoring_seconds,
            "selection_seconds_total": selection_seconds_total,
            "prepool_multiplier": PREPOOL_MULTIPLIER,
            "veto_ratio_nominal": VETO_RATIO,
            "realized_veto_count_per_positive": 1,
            "realized_veto_fraction_of_prepool": 0.5,
            "selection_rule": "V6 frozen A1/A3/A4 rank rules; no parameter tuning",
            "training_phase_wall_seconds": time.perf_counter() - started,
        }
        write_json(OUT / "strict_pool_metadata.json", pool_meta)

        # Cache V6 filtered arm metrics as a sensitivity control; no re-training.
        filtered = {}
        for method in METHODS:
            filtered[method] = {}
            for seed in SEEDS:
                if seed == 0:
                    metric_path = V6 / "A_HG_VETO" / f"{method}_seed0" / "metrics.json"
                else:
                    metric_path = V6 / "A_HG_VETO" / "confirmation" / f"{method}_seed{seed}" / "metrics.json"
                metrics = load_json(metric_path)
                filtered[method][str(seed)] = {
                    "validation_mrr": float(metrics["validation"]["mrr"]),
                    "best_epoch": int(metrics["best_epoch"]),
                    "checkpoint": metrics["checkpoint"],
                    "source": "reused exact V6 FILTERED_ALL_POSITIVE run",
                }

        training_runs = {}
        for seed in SEEDS:
            for method in METHODS:
                key = f"S_{method}_seed{seed}"
                selected = selected_by_seed[key]
                rel = str((OUT / "STRICT" / key).relative_to(ROOT)).replace("\\", "/")
                status.update({"current": key, "completed": list(training_runs)})
                write_json(OUT / "status.json", status)
                result = run_isolated_training(
                    key, "raw", seed, rel, selected=selected,
                    initialize_from_v6=(seed == 0),
                )
                training_runs[key] = {
                    "checkpoint": result["checkpoint"],
                    "result_file": result["result_file"],
                    "train_seconds": float(result["runtime"]["train_seconds"]),
                    "selected_negative_hash": array_hash(selected),
                    "selected_negative_count": int(len(selected)),
                    "epochs": 10,
                    "checkpoint_rule": "fixed_final_epoch_10",
                    "test_evaluated": False,
                }
                status["completed"].append(key)
                status["current"] = key
                write_json(OUT / "status.json", status)

        state = {
            "state": "STRICT_TRAINING_COMPLETE",
            "strict_protocol": "STRICT_TRAIN_ONLY",
            "training_runs": training_runs,
            "filtered_v6_reuse": filtered,
            "teacher_records": teacher_records,
            "pool_hash": pool_hash,
            "split_hash_train_only": split_hash,
            "test_evaluated": False,
        }
        write_json(OUT / "training_state.json", state)
        status.update({"state": "STRICT_TRAINING_COMPLETE", "phase": "await_validation", "current": None})
        write_json(OUT / "status.json", status)
    except Exception:
        status.update({"state": "FAILED", "phase": "train_only", "error": traceback.format_exc()})
        write_json(OUT / "status.json", status)
        raise


def load_train_view_for_eval():
    from dcdlp.data.loaders import load_dataset

    full = load_dataset("cora", ROOT / "data", "standard", 0)
    view = TrainOnlyView(full)
    del full
    return view


def score_fixed_candidates(checkpoint: str, view: TrainOnlyView, positives: np.ndarray,
                           negatives: np.ndarray, device: str = "cuda") -> dict:
    import torch

    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.evaluation.ranking import ranking_metrics

    model, _ = load_checkpoint_model(checkpoint, device=device)
    x = torch.as_tensor(view.features, dtype=torch.float32, device=device)
    edges = edge_index_from_graph(view.train_graph(), torch.device(device))
    with torch.no_grad():
        pos_score = score_pairs(model, x, edges, positives, batch_size=8192)["logit"]
        neg_score = score_pairs(model, x, edges, negatives.reshape(-1, 2), batch_size=8192)["logit"]
    metrics = ranking_metrics(pos_score, neg_score.reshape(len(positives), negatives.shape[1]))
    del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return metrics


def run_validation_phase() -> None:
    state = load_json(OUT / "training_state.json")
    if state.get("state") != "STRICT_TRAINING_COMPLETE":
        raise RuntimeError("Validation phase requires all strict training runs to finish")
    status = load_json(OUT / "status.json")
    status.update({"state": "RUNNING", "phase": "validation_only", "current": "S_A1_A3_A4_all_seeds"})
    write_json(OUT / "status.json", status)
    try:
        view = load_train_view_for_eval()
        with np.load(V6 / "fixed_validation_candidates.npz", allow_pickle=False) as candidate_file:
            valid_pos = candidate_file["valid_positive"].copy()
            valid_neg = candidate_file["valid_negative_candidates"].copy()
        if valid_neg.shape != (len(valid_pos), EVAL_NEGATIVES, 2):
            raise RuntimeError(f"Unexpected fixed validation candidates shape: {valid_neg.shape}")
        from dcdlp.utils import array_hash as project_array_hash

        valid_hash = project_array_hash(valid_neg)
        expected = load_json(V6 / "fixed_validation_candidates.json")["negative_candidates_hash"]
        if valid_hash != expected:
            raise RuntimeError("Fixed validation candidate hash differs from the V6 audit")
        validation = {}
        for seed in SEEDS:
            for method in METHODS:
                key = f"S_{method}_seed{seed}"
                metrics = score_fixed_candidates(
                    state["training_runs"][key]["checkpoint"], view, valid_pos, valid_neg,
                )
                validation.setdefault(method, {})[str(seed)] = {
                    "mrr": float(metrics["mrr"]),
                    "hits10": float(metrics["hits10"]),
                    "mean_positive_rank": float(metrics["mean_positive_rank"]),
                    "checkpoint_rule": "fixed_final_epoch_10",
                    "candidate_hash": valid_hash,
                }
        means = {method: float(np.mean([validation[method][str(seed)]["mrr"] for seed in SEEDS])) for method in METHODS}
        stds = {method: float(np.std([validation[method][str(seed)]["mrr"] for seed in SEEDS], ddof=1)) for method in METHODS}
        deltas = {
            "A4_minus_A1_by_seed": [validation["A4"][str(s)]["mrr"] - validation["A1"][str(s)]["mrr"] for s in SEEDS],
            "A4_minus_A3_by_seed": [validation["A4"][str(s)]["mrr"] - validation["A3"][str(s)]["mrr"] for s in SEEDS],
        }
        wins_a1 = sum(value > 0 for value in deltas["A4_minus_A1_by_seed"])
        wins_a3 = sum(value > 0 for value in deltas["A4_minus_A3_by_seed"])
        gate = bool(
            wins_a1 >= 2 and wins_a3 >= 2
            and np.mean(deltas["A4_minus_A1_by_seed"]) > 0
            and np.mean(deltas["A4_minus_A3_by_seed"]) > 0
        )
        filtered = state["filtered_v6_reuse"]
        filtered_means = {
            method: float(np.mean([filtered[method][str(seed)]["validation_mrr"] for seed in SEEDS]))
            for method in METHODS
        }
        filtered_stds = {
            method: float(np.std([filtered[method][str(seed)]["validation_mrr"] for seed in SEEDS], ddof=1))
            for method in METHODS
        }
        result = {
            "validation_status": "COMPLETE",
            "validation_candidate_hash": valid_hash,
            "validation_positive_count": len(valid_pos),
            "negatives_per_positive": EVAL_NEGATIVES,
            "strict": {"by_method_seed": validation, "mean_mrr": means, "sample_sd_mrr": stds, "deltas": deltas,
                       "A4_wins_vs_A1": wins_a1, "A4_wins_vs_A3": wins_a3,
                       "strict_mechanism_validation_gate": gate},
            "filtered_all_positive_reused_v6": {"by_method_seed": filtered, "mean_mrr": filtered_means,
                                                "sample_sd_mrr": filtered_stds,
                                                "checkpoint_selection": "V6 validation-best epoch"},
            "test_evaluated": False,
            "test_labels_or_candidates_loaded": False,
        }
        write_json(OUT / "validation_results.json", result)
        state.update({"state": "VALIDATION_COMPLETE", "validation": result})
        write_json(OUT / "training_state.json", state)
        status.update({"state": "VALIDATION_COMPLETE", "phase": "await_authorized_test", "current": None,
                       "test_evaluated": False})
        write_json(OUT / "status.json", status)
    except Exception:
        status.update({"state": "FAILED", "phase": "validation_only", "error": traceback.format_exc()})
        write_json(OUT / "status.json", status)
        raise


def fisher_exact_two_sided(a: int, n1: int, b: int, n2: int) -> dict:
    try:
        from scipy.stats import fisher_exact

        odds, p_value = fisher_exact([[a, n1 - a], [b, n2 - b]], alternative="two-sided")
        odds_out = float(odds)
        if not math.isfinite(odds_out):
            odds_out = "infinity" if odds_out > 0 else "undefined"
        return {"odds_ratio": odds_out, "p_value": float(p_value), "method": "scipy.stats.fisher_exact"}
    except ImportError:
        # Probability-ordering definition of the two-sided Fisher exact test.
        total_success = a + b
        total_n = n1 + n2
        lower = max(0, total_success - n2)
        upper = min(n1, total_success)

        def log_choose(n: int, k: int) -> float:
            return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)

        def log_prob(x: int) -> float:
            return log_choose(n1, x) + log_choose(n2, total_success - x) - log_choose(total_n, total_success)

        observed_logp = log_prob(a)
        probabilities = [math.exp(log_prob(x)) for x in range(lower, upper + 1) if log_prob(x) <= observed_logp + 1e-12]
        odds = ((a + 0.5) * (n2 - b + 0.5)) / ((n1 - a + 0.5) * (b + 0.5))
        return {"odds_ratio": float(odds), "p_value": min(1.0, float(sum(probabilities))), "method": "local probability-ordered exact implementation"}


def paired_bootstrap(true_y: np.ndarray, control_y: np.ndarray, seed: int,
                     iterations: int = BOOTSTRAPS) -> dict:
    true_y = np.asarray(true_y, dtype=float).reshape(-1)
    control_y = np.asarray(control_y, dtype=float).reshape(-1)
    if true_y.shape != control_y.shape:
        raise ValueError("paired bootstrap arrays must have same length")
    n = len(true_y)
    point_true, point_control = float(true_y.mean()), float(control_y.mean())

    def odds(rate):
        return (rate + 0.5 / n) / (1.0 - rate + 0.5 / n)

    point_or = odds(point_true) / odds(point_control)
    rng = np.random.default_rng(seed)
    differences = np.empty(iterations, dtype=float)
    ratios = np.empty(iterations, dtype=float)
    ors = np.empty(iterations, dtype=float)
    for index in range(iterations):
        ids = rng.integers(0, n, size=n)
        tr, ct = float(true_y[ids].mean()), float(control_y[ids].mean())
        differences[index] = tr - ct
        ratios[index] = tr / ct if ct > 0 else (math.inf if tr > 0 else 1.0)
        ors[index] = odds(tr) / odds(ct)
    def quantile(array):
        ordered = np.sort(np.asarray(array, dtype=float))
        output = []
        for probability in (0.025, 0.975):
            # Nearest-rank percentile avoids NaN interpolation between finite
            # ratios and +infinity when a bootstrap control has zero positives.
            position = min(len(ordered) - 1, int(math.ceil(probability * (len(ordered) - 1))))
            value = ordered[position]
            number = float(value)
            output.append(number if math.isfinite(number) else ("infinity" if number > 0 else "undefined"))
        return output
    return {
        "true_rate": point_true, "control_rate": point_control,
        "rate_difference": point_true - point_control,
        "rate_difference_95pct_bootstrap_ci": quantile(differences),
        "rate_ratio": point_true / point_control if point_control > 0 else (None if point_true == 0 else "infinity"),
        "rate_ratio_95pct_bootstrap_ci": quantile(ratios),
        "odds_ratio_haldane_corrected": float(point_or),
        "odds_ratio_95pct_bootstrap_ci": quantile(ors),
        "bootstrap_unit": "training-positive query row",
        "bootstrap_iterations": iterations,
    }


def rate_and_interval(positive: np.ndarray, iterations: int, seed: int) -> dict:
    positive = np.asarray(positive, dtype=float)
    n = len(positive)
    rng = np.random.default_rng(seed)
    values = np.empty(iterations, dtype=float)
    for index in range(iterations):
        rows = rng.integers(0, n, size=n)
        values[index] = positive[rows].mean()
    return {"count": int(positive.sum()), "denominator": int(n), "rate": float(positive.mean()),
            "rate_95pct_bootstrap_ci": [float(np.quantile(values, .025)), float(np.quantile(values, .975))]}


def pair_level_rate(pairs: np.ndarray, future_set: set[tuple[int, int]]) -> dict:
    unique = sorted({canonical_edge(pair) for pair in np.asarray(pairs).reshape(-1, 2)})
    hits = sum(pair in future_set for pair in unique)
    return {"future_positive_unique_pairs": int(hits), "unique_pairs": len(unique),
            "rate": float(hits / len(unique)) if unique else 0.0}


def run_test_and_posthoc_phase() -> None:
    import torch

    from dcdlp.data.loaders import load_dataset
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, evaluate_split
    from dcdlp.utils import array_hash as project_array_hash

    state = load_json(OUT / "training_state.json")
    validation = load_json(OUT / "validation_results.json")
    if state.get("state") != "VALIDATION_COMPLETE" or validation.get("validation_status") != "COMPLETE":
        raise RuntimeError("Test is gated until all strict validation analyses finish")
    status = load_json(OUT / "status.json")
    if status.get("test_evaluated"):
        raise RuntimeError("Test phase already ran; refusing a second test look")
    status.update({"state": "RUNNING", "phase": "authorized_test_and_posthoc", "current": "S_A1_A3_A4_all_seeds"})
    write_json(OUT / "status.json", status)
    try:
        dataset = load_dataset("cora", ROOT / "data", "standard", 0)
        x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
        edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
        test_seed = 999
        test_pool = uniform_negative_sampling(
            dataset.num_nodes, dataset.all_positive, EVAL_NEGATIVES * len(dataset.test_pos), test_seed,
        )
        test_neg = grouped_negatives(dataset.test_pos, test_pool, EVAL_NEGATIVES, test_seed + 1)
        test_candidate_tensor = np.concatenate([dataset.test_pos[:, None, :], test_neg], axis=1)
        test_candidate_hash = project_array_hash(test_neg)
        expected_v6_candidate_hash = load_json(V6 / "results.json")["test_results"]["shared_candidate_hash"]
        if test_candidate_hash != expected_v6_candidate_hash:
            raise RuntimeError(
                "Fixed test candidate hash differs from V6 seed-0 protocol: "
                f"{test_candidate_hash} != {expected_v6_candidate_hash}"
            )

        # Test is evaluated once, using the same test negatives for every method/seed.
        test_metrics = {}
        candidate_hashes = {}
        for seed in SEEDS:
            for method in METHODS:
                key = f"S_{method}_seed{seed}"
                model, _ = load_checkpoint_model(state["training_runs"][key]["checkpoint"], device="cuda")
                metadata = {}
                metrics, _ = evaluate_split(
                    model, dataset, dataset.test_pos, test_seed, EVAL_NEGATIVES,
                    x, edges, negative_method="uniform", candidate_metadata=metadata,
                )
                if metadata.get("hash") != test_candidate_hash:
                    raise RuntimeError("model-specific test candidate hash unexpectedly differs")
                test_metrics.setdefault(method, {})[str(seed)] = {
                    "mrr": float(metrics["mrr"]),
                    "hits10": float(metrics["hits10"]),
                    "mean_positive_rank": float(metrics["mean_positive_rank"]),
                    "candidate_hash": metadata["hash"],
                    "checkpoint": state["training_runs"][key]["checkpoint"],
                }
                candidate_hashes[key] = metadata["hash"]
                del model
                torch.cuda.empty_cache()
        test_means = {method: float(np.mean([test_metrics[method][str(seed)]["mrr"] for seed in SEEDS])) for method in METHODS}
        test_stds = {method: float(np.std([test_metrics[method][str(seed)]["mrr"] for seed in SEEDS], ddof=1)) for method in METHODS}
        test_deltas = {
            "A4_minus_A1_by_seed": [test_metrics["A4"][str(s)]["mrr"] - test_metrics["A1"][str(s)]["mrr"] for s in SEEDS],
            "A4_minus_A3_by_seed": [test_metrics["A4"][str(s)]["mrr"] - test_metrics["A3"][str(s)]["mrr"] for s in SEEDS],
        }
        performance = bool(
            sum(v > 0 for v in test_deltas["A4_minus_A1_by_seed"]) >= 2
            and sum(v > 0 for v in test_deltas["A4_minus_A3_by_seed"]) >= 2
            and test_means["A4"] > test_means["A1"]
            and test_means["A4"] > test_means["A3"]
        )
        test_result = {
            "test_status": "COMPLETE", "test_evaluated_once": True,
            "test_positive_count": len(dataset.test_pos), "negatives_per_positive": EVAL_NEGATIVES,
            "test_negative_pool_seed": test_seed, "grouping_seed": test_seed + 1,
            "test_candidate_hash": test_candidate_hash,
            "candidate_hash_matches_v6_seed0": test_candidate_hash == expected_v6_candidate_hash,
            "by_method_seed": test_metrics, "mean_mrr": test_means, "sample_sd_mrr": test_stds,
            "deltas": test_deltas, "performance_supported": performance,
            "A4_wins_vs_A1": sum(v > 0 for v in test_deltas["A4_minus_A1_by_seed"]),
            "A4_wins_vs_A3": sum(v > 0 for v in test_deltas["A4_minus_A3_by_seed"]),
            "filtered_v6_test_reuse": load_json(V6 / "results.json")["test_results"],
        }
        write_json(OUT / "test_results.json", test_result)

        # Post-hoc only: the held-out identity set is first consumed here, after
        # every sampler, teacher, checkpoint, validation decision, and test score is frozen.
        future_set = {canonical_edge(x) for x in np.vstack([dataset.valid_pos, dataset.test_pos]).tolist()}
        with np.load(OUT / "strict_train_candidates_and_selections.npz", allow_pickle=False) as archive:
            grouped = archive["negative_candidates"].copy()
            graph_pre = archive["graph_prepool_indices"].copy()
            raw_hg_scores = archive["score_raw_hg"].copy()
            true_veto_idx = archive["true_veto_indices"].copy()
            pool_hash = array_hash(grouped)
            per_seed = {}
            for seed in SEEDS:
                shuffled_idx = archive[f"veto_shuffled_seed{seed}"].copy()
                random_idx = archive[f"veto_random_seed{seed}"].copy()
                true_pairs = grouped[np.arange(len(grouped)), true_veto_idx]
                shuffled_pairs = grouped[np.arange(len(grouped)), shuffled_idx]
                random_pairs = grouped[np.arange(len(grouped)), random_idx]
                pre_pairs = grouped[np.arange(len(grouped))[:, None], graph_pre]
                true_y = np.asarray([canonical_edge(pair) in future_set for pair in true_pairs], dtype=np.int8)
                shuffled_y = np.asarray([canonical_edge(pair) in future_set for pair in shuffled_pairs], dtype=np.int8)
                random_y = np.asarray([canonical_edge(pair) in future_set for pair in random_pairs], dtype=np.int8)
                pre_y = np.asarray([[canonical_edge(pair) in future_set for pair in row] for row in pre_pairs], dtype=np.int8)
                q1_y = np.asarray([canonical_edge(pair) in future_set for pair in true_pairs], dtype=np.int8)
                q2_idx = graph_pre[np.arange(len(grouped)), 1 - np.argmax(
                    np.take_along_axis(raw_hg_scores, graph_pre, axis=1), axis=1
                )]
                q2_pairs = grouped[np.arange(len(grouped)), q2_idx]
                q2_y = np.asarray([canonical_edge(pair) in future_set for pair in q2_pairs], dtype=np.int8)
                per_seed[str(seed)] = {
                    "true_veto_occurrence_rate": rate_and_interval(true_y, BOOTSTRAPS, 71_000 + seed),
                    "shuffled_veto_occurrence_rate": rate_and_interval(shuffled_y, BOOTSTRAPS, 72_000 + seed),
                    "random_veto_occurrence_rate": rate_and_interval(random_y, BOOTSTRAPS, 73_000 + seed),
                    "graph_hard_prepool_occurrence_rate": rate_and_interval(pre_y.reshape(-1), BOOTSTRAPS, 74_000 + seed),
                    "true_veto_unique_pair_rate": pair_level_rate(true_pairs, future_set),
                    "shuffled_veto_unique_pair_rate": pair_level_rate(shuffled_pairs, future_set),
                    "random_veto_unique_pair_rate": pair_level_rate(random_pairs, future_set),
                    "graph_hard_prepool_unique_pair_rate": pair_level_rate(pre_pairs.reshape(-1, 2), future_set),
                    "true_vs_shuffled": paired_bootstrap(true_y, shuffled_y, 75_000 + seed),
                    "true_vs_random": paired_bootstrap(true_y, random_y, 76_000 + seed),
                    "true_vs_shuffled_fisher": fisher_exact_two_sided(int(true_y.sum()), len(true_y), int(shuffled_y.sum()), len(shuffled_y)),
                    "true_vs_random_fisher": fisher_exact_two_sided(int(true_y.sum()), len(true_y), int(random_y.sum()), len(random_y)),
                    "prepool_future_positive_occurrences": int(pre_y.sum()),
                    "true_veto_pairs": true_pairs,
                    "shuffled_veto_pairs": shuffled_pairs,
                    "random_veto_pairs": random_pairs,
                    "graph_hard_prepool_pairs": pre_pairs.reshape(-1, 2),
                    "q1_y": q1_y, "q2_y": q2_y,
                }

            # The true veto decision is deterministic for the shared pool and teacher.
            primary = per_seed["0"]
            true_y = np.asarray([canonical_edge(pair) in future_set for pair in grouped[np.arange(len(grouped)), true_veto_idx]], dtype=np.int8)
            shuffled_matrix = np.vstack([
                np.asarray([canonical_edge(pair) in future_set for pair in grouped[np.arange(len(grouped)), archive[f"veto_shuffled_seed{s}"]]], dtype=np.float64)
                for s in SEEDS
            ])
            random_matrix = np.vstack([
                np.asarray([canonical_edge(pair) in future_set for pair in grouped[np.arange(len(grouped)), archive[f"veto_random_seed{s}"]]], dtype=np.float64)
                for s in SEEDS
            ])
            avg_shuffled_y = shuffled_matrix.mean(axis=0)
            avg_random_y = random_matrix.mean(axis=0)
            pre_pairs = grouped[np.arange(len(grouped))[:, None], graph_pre]
            pre_y = np.asarray([[canonical_edge(pair) in future_set for pair in row] for row in pre_pairs], dtype=np.float64)
            q1_y = true_y.astype(float)
            hg_pre_scores = np.take_along_axis(raw_hg_scores, graph_pre, axis=1)
            q2_idx = graph_pre[np.arange(len(grouped)), 1 - np.argmax(hg_pre_scores, axis=1)]
            q2_y = np.asarray([canonical_edge(pair) in future_set for pair in grouped[np.arange(len(grouped)), q2_idx]], dtype=float)
            q1q2 = paired_bootstrap(q1_y, q2_y, 77_001)
            true_vs_shuffle_aggregate = paired_bootstrap(true_y.astype(float), avg_shuffled_y, 77_002)
            true_vs_random_aggregate = paired_bootstrap(true_y.astype(float), avg_random_y, 77_003)

            # Empirical HG percentile over Graph-hard prepool occurrences, not over held-out labels.
            reference = hg_pre_scores.reshape(-1)
            sorted_reference = np.sort(reference)
            percentile = np.searchsorted(sorted_reference, reference, side="right") / max(1, len(sorted_reference))
            bucket = np.minimum((percentile * 5).astype(int), 4)
            future_pre = pre_y.reshape(-1).astype(np.int8)
            bucket_rows = []
            bucket_rates = []
            labels = ("0-20%", "20-40%", "40-60%", "60-80%", "80-100%")
            for index, name in enumerate(labels):
                mask = bucket == index
                values = future_pre[mask]
                summary = rate_and_interval(values, BOOTSTRAPS, 78_000 + index)
                summary["hg_percentile_bucket"] = name
                bucket_rows.append(summary)
                bucket_rates.append(summary["rate"])

            # Primary point estimates use one veto per train-positive row.
            true_rate = float(true_y.mean())
            pre_rate = float(pre_y.mean())
            enrichment_vs_prepool = true_rate / pre_rate if pre_rate > 0 else None
            pre_ratio_boot = np.empty(BOOTSTRAPS)
            rng_pre = np.random.default_rng(79_000)
            for index in range(BOOTSTRAPS):
                ids = rng_pre.integers(0, len(grouped), size=len(grouped))
                tr = float(true_y[ids].mean())
                pr = float(pre_y[ids].mean())
                pre_ratio_boot[index] = tr / pr if pr > 0 else (math.inf if tr > 0 else 1.0)

            # Filtered V6 pool was drawn against all_positive, so held-out positives are ineligible by design.
            with np.load(V6 / "shared_train_candidate_pool.npz", allow_pickle=False) as filtered_archive:
                filtered_grouped = filtered_archive["negative_candidates"].copy()
            filtered_hits = sum(canonical_edge(pair) in future_set for pair in filtered_grouped.reshape(-1, 2))
            if filtered_hits != 0:
                raise RuntimeError("FILTERED_ALL_POSITIVE pool unexpectedly contains a heldout positive")

            # V6 A3 diagnostic: diversity and selected hardness on the held-out-blind pool.
            test_a3_best = test_result["mean_mrr"]["A3"] >= max(test_result["mean_mrr"]["A1"], test_result["mean_mrr"]["A4"])
            diversity = {}
            if test_a3_best:
                graph = dataset.train_graph()
                degree = np.asarray([graph.degree(i) for i in range(dataset.num_nodes)], dtype=float)
                for seed in SEEDS:
                    diversity[str(seed)] = {}
                    selected_sets = {}
                    for method in METHODS:
                        pairs = archive[f"S_{method}_seed{seed}"].copy()
                        idx = {"A1": archive["graph_hard_indices"], "A3": None, "A4": archive["a4_indices"]}[method]
                        if method == "A3":
                            # Identify the selected candidate in each row from pair identity.
                            rows = []
                            for row, pair in enumerate(pairs):
                                hits = np.flatnonzero(np.all(grouped[row] == pair, axis=1))
                                if not len(hits):
                                    raise RuntimeError("selected A3 pair absent from its candidate row")
                                rows.append(int(hits[0]))
                            idx = np.asarray(rows, dtype=np.int64)
                        scores_g = scores_from_archive = archive["score_graph"]
                        selected_score = scores_g[np.arange(len(pairs)), idx]
                        endpoints = pairs.reshape(-1)
                        selected_sets[method] = {canonical_edge(pair) for pair in pairs}
                        diversity[str(seed)][method] = {
                            "unique_endpoint_ratio": float(len(np.unique(endpoints)) / max(1, len(endpoints))),
                            "unique_selected_pair_ratio": float(len(selected_sets[method]) / len(pairs)),
                            "endpoint_degree_mean": float(degree[endpoints].mean()),
                            "endpoint_degree_std": float(degree[endpoints].std()),
                            "endpoint_degree_p90": float(np.quantile(degree[endpoints], .9)),
                            "graph_hardness_mean": float(selected_score.mean()),
                            "graph_hardness_std": float(selected_score.std()),
                            "selected_pairs": pairs,
                        }
                    overlaps = {}
                    for left, right in (("A1", "A3"), ("A1", "A4"), ("A3", "A4")):
                        union = selected_sets[left] | selected_sets[right]
                        overlaps[f"{left}_vs_{right}_jaccard"] = len(selected_sets[left] & selected_sets[right]) / len(union) if union else 0.0
                    diversity[str(seed)]["pair_overlap"] = overlaps

            def nearest_rank_ci(values):
                ordered = np.sort(np.asarray(values, dtype=float))
                result = []
                for probability in (.025, .975):
                    position = min(len(ordered) - 1, int(math.ceil(probability * (len(ordered) - 1))))
                    item = float(ordered[position])
                    result.append(item if math.isfinite(item) else ("infinity" if item > 0 else "undefined"))
                return result

            enrichment = {
                "future_positive_definition": "undirected pair occurs in valid_pos OR test_pos; labels accessed only after all training and validation decisions were frozen",
                "strict_pool_hash": pool_hash,
                "future_positive_unique_identity_count": len(future_set),
                "per_seed": {
                    seed: {key: value for key, value in entry.items() if not key.endswith("_pairs") and key not in {"q1_y", "q2_y"}}
                    for seed, entry in per_seed.items()
                },
                "aggregate_control_rates_are_query_row_averages_across_three_control_seeds": True,
                "true_veto_rate": rate_and_interval(true_y, BOOTSTRAPS, 80_001),
                "shuffled_veto_rate_mean_across_seeds": rate_and_interval(avg_shuffled_y, BOOTSTRAPS, 80_002),
                "random_veto_rate_mean_across_seeds": rate_and_interval(avg_random_y, BOOTSTRAPS, 80_003),
                "graph_hard_prepool_rate": rate_and_interval(pre_y.reshape(-1), BOOTSTRAPS, 80_004),
                "true_veto_enrichment_vs_prepool": {
                    "ratio": enrichment_vs_prepool,
                    "bootstrap_ci_95": nearest_rank_ci(pre_ratio_boot),
                    "prepool_rate": pre_rate,
                    "true_veto_rate": true_rate,
                },
                "true_vs_shuffled_aggregate": true_vs_shuffle_aggregate,
                "true_vs_random_aggregate": true_vs_random_aggregate,
                "true_vs_shuffled_fisher_seed0": primary["true_vs_shuffled_fisher"],
                "true_vs_random_fisher_seed0": primary["true_vs_random_fisher"],
                "Q1_graph_hard_HG_high_vs_Q2_graph_hard_HG_low": {
                    "Q1_rate": float(q1_y.mean()), "Q2_rate": float(q2_y.mean()),
                    "risk_ratio": float(q1_y.mean() / q2_y.mean()) if q2_y.mean() > 0 else (None if q1_y.mean() == 0 else "infinity"),
                    "odds_ratio_and_paired_bootstrap": q1q2,
                    "absolute_rate_difference": float(q1_y.mean() - q2_y.mean()),
                    "Q1_future_positive_count": int(q1_y.sum()), "Q2_future_positive_count": int(q2_y.sum()),
                },
                "hg_percentile_buckets": bucket_rows,
                "hg_percentile_monotonicity": {
                    "rates": bucket_rates,
                    "nondecreasing": bool(all(bucket_rates[i] <= bucket_rates[i + 1] for i in range(len(bucket_rates) - 1))),
                    "spearman_rho": None,
                },
                "filtered_all_positive_control": {
                    "candidate_occurrences": int(filtered_grouped.size // 2),
                    "future_positive_occurrences": int(filtered_hits),
                    "future_positive_rate": 0.0,
                    "interpretation": "structurally forced to zero by the all_positive rejection filter; not evidence against or for the verifier",
                },
                "diversity_diagnostic_if_A3_test_best": diversity if test_a3_best else None,
                "a3_test_best": test_a3_best,
            }
            write_json(OUT / "enrichment_results.json", enrichment)

            csv_path = OUT / "HG_PERCENTILE_VS_FUTURE_POSITIVE.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["hg_percentile_bucket", "future_positive_count", "candidate_occurrence_count", "future_positive_rate", "ci95_low", "ci95_high"])
                writer.writeheader()
                for row in bucket_rows:
                    writer.writerow({
                        "hg_percentile_bucket": row["hg_percentile_bucket"],
                        "future_positive_count": row["count"],
                        "candidate_occurrence_count": row["denominator"],
                        "future_positive_rate": row["rate"],
                        "ci95_low": row["rate_95pct_bootstrap_ci"][0],
                        "ci95_high": row["rate_95pct_bootstrap_ci"][1],
                    })

        test_result["diversity_analysis_if_a3_test_best"] = enrichment["diversity_diagnostic_if_A3_test_best"]
        write_json(OUT / "test_results.json", test_result)
        state.update({"state": "POSTHOC_COMPLETE", "test_results": test_result,
                      "enrichment_results": enrichment, "test_evaluated": True})
        write_json(OUT / "training_state.json", state)
        status.update({"state": "POSTHOC_COMPLETE", "phase": "reporting", "current": None,
                       "test_evaluated": True})
        write_json(OUT / "status.json", status)
    except Exception:
        status.update({"state": "FAILED", "phase": "authorized_test_and_posthoc", "error": traceback.format_exc()})
        write_json(OUT / "status.json", status)
        raise


def metric_summary(by_seed: dict) -> tuple[float, float]:
    values = np.asarray(list(by_seed.values()), dtype=float)
    return float(values.mean()), float(values.std(ddof=1))


def render_reports() -> None:
    state = load_json(OUT / "training_state.json")
    validation = load_json(OUT / "validation_results.json")
    test = load_json(OUT / "test_results.json")
    enrich = load_json(OUT / "enrichment_results.json")
    pool = load_json(OUT / "strict_pool_metadata.json")
    q1q2_boot = enrich["Q1_graph_hard_HG_high_vs_Q2_graph_hard_HG_low"]["odds_ratio_and_paired_bootstrap"]
    q1q2_ratio_ci = q1q2_boot.get("rate_ratio_95pct_bootstrap_ci", [])
    if len(q1q2_ratio_ci) == 2 and q1q2_ratio_ci[1] == "undefined" and q1q2_boot.get("control_rate", 0) < q1q2_boot.get("true_rate", 0):
        # The historical linear quantile interpolated a finite value with +inf.
        # The nearest-rank bootstrap interval is unbounded above in this case.
        q1q2_ratio_ci[1] = "infinity"
        q1q2_boot["rate_ratio_95pct_bootstrap_ci"] = q1q2_ratio_ci
        q1q2_boot["ci_note"] = "upper endpoint is unbounded because bootstrap samples include zero Q2 future positives"
        write_json(OUT / "enrichment_results.json", enrich)
    strict = validation["strict"]
    filtered = validation["filtered_all_positive_reused_v6"]
    strict_signal = strict["strict_mechanism_validation_gate"]
    fisher_shuffled_p = enrich["true_vs_shuffled_fisher_seed0"]["p_value"]
    fisher_random_p = enrich["true_vs_random_fisher_seed0"]["p_value"]
    mechanism_supported = bool(
        enrich["true_vs_shuffled_aggregate"]["rate_difference_95pct_bootstrap_ci"][0] > 0
        and enrich["true_vs_random_aggregate"]["rate_difference_95pct_bootstrap_ci"][0] > 0
        and enrich["true_veto_enrichment_vs_prepool"]["ratio"] is not None
        and enrich["true_veto_enrichment_vs_prepool"]["ratio"] > 1.0
        and fisher_shuffled_p < 0.05
        and fisher_random_p < 0.05
    )
    performance_supported = bool(test["performance_supported"])
    if performance_supported and mechanism_supported:
        decision = "PERFORMANCE_AND_MECHANISM"
    elif mechanism_supported and not performance_supported:
        delta = strict["mean_mrr"]["A4"] - strict["mean_mrr"]["A1"]
        decision = "MECHANISM_FOUND_BUT_OPTIMIZATION_WEAK" if delta < 0.002 else "MECHANISM_ONLY"
    else:
        decision = "NO_MECHANISM"
    final = {
        "status": "COMPLETE",
        "strict_protocol": "PASS",
        "filtered_results": {"mean_mrr": filtered["mean_mrr"], "sample_sd_mrr": filtered["sample_sd_mrr"],
                             "by_method_seed": filtered["by_method_seed"],
                             "source": "exact V6 FILTERED_ALL_POSITIVE runs; no retraining"},
        "strict_results": {"mean_mrr": strict["mean_mrr"], "sample_sd_mrr": strict["sample_sd_mrr"],
                           "by_method_seed": strict["by_method_seed"]},
        "test_results": {"mean_mrr": test["mean_mrr"], "sample_sd_mrr": test["sample_sd_mrr"],
                         "by_method_seed": test["by_method_seed"]},
        "true_veto_future_positive_rate": enrich["true_veto_rate"],
        "shuffled_veto_future_positive_rate": enrich["shuffled_veto_rate_mean_across_seeds"],
        "random_veto_future_positive_rate": enrich["random_veto_rate_mean_across_seeds"],
        "graph_hard_prepool_future_positive_rate": enrich["graph_hard_prepool_rate"],
        "true_veto_enrichment_vs_prepool": enrich["true_veto_enrichment_vs_prepool"],
        "odds_ratio_true_vs_shuffled": enrich["true_vs_shuffled_aggregate"]["odds_ratio_haldane_corrected"],
        "odds_ratio_true_vs_random": enrich["true_vs_random_aggregate"]["odds_ratio_haldane_corrected"],
        "hg_percentile_monotonicity": enrich["hg_percentile_monotonicity"],
        "strict_mechanism_signal": "YES" if strict_signal else "NO",
        "mechanism_supported": "YES" if mechanism_supported else "NO",
        "performance_supported": "YES" if performance_supported else "NO",
        "efficiency": {
            "pool_generation_seconds": pool["pool_generation_seconds"],
            "teacher_training_seconds": {k: v["train_seconds"] for k, v in pool["teacher_records"].items()},
            "teacher_scoring_seconds": pool["teacher_scoring_seconds"],
            "selection_seconds_total": pool["selection_seconds_total"],
            "amortized_selection_seconds_per_epoch": pool["selection_seconds_total"] / 10,
            "cached_score_forward_repeats": 0,
            "cached_a4_selection_overhead_target_under_5pct": pool["selection_seconds_total"] < 0.05 * max(1e-9, float(np.mean([r["train_seconds"] for r in state["training_runs"].values()]))),
        },
        "final_decision": decision,
        "novelty_status": "EXACT_RULE_UNVERIFIED",
        "mechanism_decision_basis": {
            "rule": "require enrichment above prepool, positive paired row-bootstrap CIs against both controls, and Fisher exact p<0.05 against both controls",
            "true_vs_shuffled_fisher_p_seed0": fisher_shuffled_p,
            "true_vs_random_fisher_p_seed0": fisher_random_p,
            "true_vs_shuffled_paired_ci": enrich["true_vs_shuffled_aggregate"]["rate_difference_95pct_bootstrap_ci"],
            "true_vs_random_paired_ci": enrich["true_vs_random_aggregate"]["rate_difference_95pct_bootstrap_ci"],
        },
        "next_expected_step": (
            "If mechanism is supported but A4 does not beat both test controls, investigate diversity-preserving purification in a separate sprint."
            if mechanism_supported and not performance_supported
            else "Stop the false-negative mechanism claim; retain any test performance result separately and require a pre-registered, adequately powered independent mechanism replication before a new method design. Do not tune from this test set."
            if performance_supported and not mechanism_supported
            else "Treat this strict protocol result as the gate for any follow-up; do not tune from this test set."
        ),
    }
    write_json(OUT / "results.json", final)

    def fmt(mean, std):
        return f"{mean:.6f} ± {std:.6f}"

    lines = [
        "# V6.1 Protocol Audit",
        "",
        "## Strict boundary",
        "",
        "- Candidate-pool forbidden set was formed only from canonicalized training positives and the training/message graph edges; self-loops and out-of-range pairs were rejected by the same eligibility predicate.",
        "- The miner and teachers received a train-only view. Accessing `all_positive` raises; actual validation/test identities were not exposed to candidate sampling, teacher fitting/scoring, or strict training.",
        "- The compatibility training loop saw empty validation/test placeholders only. Validation selection was replaced by the precommitted fixed-final-epoch-10 rule; no validation or test score selected a checkpoint.",
        "- The held-out-positive eligibility unit test passed: a synthetic future-positive identity and an ordinary unknown pair both pass the exact same train-only candidate predicate.",
        "- Validation used the previously audited V6 fixed candidate tensor; test scoring ran once only after all strict validation results and gates were frozen.",
        "- Test labels were first consumed in the post-hoc stage after training and validation decisions were frozen.",
        "",
        "## Frozen settings",
        "",
        f"Cora standard; {pool['candidate_count_per_positive']} candidate pairs per training positive; A1/A3/A4; nominal veto={VETO_RATIO}; graph prepool multiplier={PREPOOL_MULTIPLIER} (2 candidates, 1 removed); 10 epochs; seeds 0/1/2.",
        "",
        f"Train positives: {pool['train_positive_count']}; candidate pool hash: `{pool['candidate_pool_hash']}`; train-only split hash: `{pool['train_only_split_hash']}`.",
        "",
        "## Filtered sensitivity control",
        "",
        "Reused the exact V6 FILTERED_ALL_POSITIVE runs. Their validation-best checkpoint rule differs from strict V6.1's fixed epoch-10 rule, so this is protocol sensitivity context rather than a fully matched retraining comparison.",
        "",
        "## Novelty status",
        "",
        "`EXACT_RULE_UNVERIFIED`.",
        "",
    ]
    (OUT / "00_PROTOCOL_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# V6.1 Strict Results", "", "Validation uses the unchanged V6 fixed candidate tensor. Values are MRR mean ± sample SD over seeds 0/1/2.", "",
             "| Protocol | A1 Graph-hard | A3 shuffled veto | A4 true HG veto |", "|---|---:|---:|---:|"]
    lines.append("| STRICT_TRAIN_ONLY | " + " | ".join(fmt(strict["mean_mrr"][m], strict["sample_sd_mrr"][m]) for m in METHODS) + " |")
    lines.append("| FILTERED_ALL_POSITIVE (reused V6) | " + " | ".join(fmt(filtered["mean_mrr"][m], filtered["sample_sd_mrr"][m]) for m in METHODS) + " |")
    lines += ["", "## Per-seed strict validation MRR", "", "| Seed | A1 | A3 | A4 | A4−A1 | A4−A3 |", "|---:|---:|---:|---:|---:|---:|"]
    for seed in SEEDS:
        vals = {m: strict["by_method_seed"][m][str(seed)]["mrr"] for m in METHODS}
        lines.append(f"| {seed} | {vals['A1']:.6f} | {vals['A3']:.6f} | {vals['A4']:.6f} | {vals['A4']-vals['A1']:+.6f} | {vals['A4']-vals['A3']:+.6f} |")
    lines += ["", f"STRICT_MECHANISM_SIGNAL validation gate: **{'YES' if strict_signal else 'NO'}** ({strict['A4_wins_vs_A1']}/3 A4 wins vs A1; {strict['A4_wins_vs_A3']}/3 vs A3; both mean deltas must be positive).", "", "Strict checkpoints use the fixed final epoch because validation-based checkpoint selection is disallowed in STRICT_TRAIN_ONLY.", ""]
    (OUT / "01_STRICT_RESULTS.md").write_text("\n".join(lines), encoding="utf-8")

    e = enrich
    lines = ["# V6.1 False-Negative Enrichment", "", "Future-positive labels were joined only after all training, candidate selection, validation gating, and test scoring completed. Rates below count candidate occurrences; unique-pair rates are also present in `enrichment_results.json`.", "",
             f"- True HG veto: {e['true_veto_rate']['count']}/{e['true_veto_rate']['denominator']} = {e['true_veto_rate']['rate']:.8f} (95% row-bootstrap CI {e['true_veto_rate']['rate_95pct_bootstrap_ci']}).",
             f"- Shuffled veto, averaged across three seed-specific shuffles: {e['shuffled_veto_rate_mean_across_seeds']['rate']:.8f}.",
             f"- Random veto, averaged across three seed-specific draws: {e['random_veto_rate_mean_across_seeds']['rate']:.8f}.",
             f"- Graph-hard prepool: {e['graph_hard_prepool_rate']['rate']:.8f}.",
             f"- True veto / prepool enrichment: {e['true_veto_enrichment_vs_prepool']['ratio']} (95% row-bootstrap CI {e['true_veto_enrichment_vs_prepool']['bootstrap_ci_95']}).",
             f"- True vs shuffled paired rate difference: {e['true_vs_shuffled_aggregate']['rate_difference']:.8f}, 95% CI {e['true_vs_shuffled_aggregate']['rate_difference_95pct_bootstrap_ci']}; OR={e['true_vs_shuffled_aggregate']['odds_ratio_haldane_corrected']:.4g}, CI {e['true_vs_shuffled_aggregate']['odds_ratio_95pct_bootstrap_ci']}; seed-0 Fisher p={e['true_vs_shuffled_fisher_seed0']['p_value']:.6g}.",
             f"- True vs random paired rate difference: {e['true_vs_random_aggregate']['rate_difference']:.8f}, 95% CI {e['true_vs_random_aggregate']['rate_difference_95pct_bootstrap_ci']}; OR={e['true_vs_random_aggregate']['odds_ratio_haldane_corrected']:.4g}, CI {e['true_vs_random_aggregate']['odds_ratio_95pct_bootstrap_ci']}; seed-0 Fisher p={e['true_vs_random_fisher_seed0']['p_value']:.6g}.",
             "- Mechanism support requires both paired bootstrap comparisons to exclude zero and both seed-0 Fisher tests to have p<0.05. Fisher tests are non-significant here, so the higher point estimates are not treated as confirmed enrichment.",
             f"- Q1 (Graph-hard/HG-high) vs Q2 (Graph-hard/HG-low): rates {e['Q1_graph_hard_HG_high_vs_Q2_graph_hard_HG_low']['Q1_rate']:.8f} vs {e['Q1_graph_hard_HG_high_vs_Q2_graph_hard_HG_low']['Q2_rate']:.8f}; RR={e['Q1_graph_hard_HG_high_vs_Q2_graph_hard_HG_low']['risk_ratio']}; absolute difference={e['Q1_graph_hard_HG_high_vs_Q2_graph_hard_HG_low']['absolute_rate_difference']:.8f}.",
             f"- HG percentile monotonicity: {e['hg_percentile_monotonicity']['nondecreasing']}; bucket rates={e['hg_percentile_monotonicity']['rates']}.",
             f"- FILTERED_ALL_POSITIVE future-positive pool occurrences: {e['filtered_all_positive_control']['future_positive_occurrences']}/{e['filtered_all_positive_control']['candidate_occurrences']} (structurally forced to zero).",
             "", "See `HG_PERCENTILE_VS_FUTURE_POSITIVE.csv` for publication-ready bucket counts and intervals.", ""]
    (OUT / "02_FALSE_NEGATIVE_ENRICHMENT.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# V6.1 Test Confirmation", "", "Test was evaluated once after the complete strict validation table and validation gate were frozen. All methods and seeds use the same V6 seed-0 test candidate tensor.", "",
             "| Seed | A1 | A3 | A4 | A4−A1 | A4−A3 |", "|---:|---:|---:|---:|---:|---:|"]
    for seed in SEEDS:
        vals = {m: test["by_method_seed"][m][str(seed)]["mrr"] for m in METHODS}
        lines.append(f"| {seed} | {vals['A1']:.6f} | {vals['A3']:.6f} | {vals['A4']:.6f} | {vals['A4']-vals['A1']:+.6f} | {vals['A4']-vals['A3']:+.6f} |")
    lines += ["", "Test mean ± sample SD: " + "; ".join(f"{m} {fmt(test['mean_mrr'][m], test['sample_sd_mrr'][m])}" for m in METHODS) + ".", "",
              f"PERFORMANCE_SUPPORTED: **{'YES' if performance_supported else 'NO'}** ({test['A4_wins_vs_A1']}/3 wins over A1 and {test['A4_wins_vs_A3']}/3 over A3; A4 must have the highest mean).", "",
              f"Candidate hash: `{test['test_candidate_hash']}`; matches V6 seed-0 test candidates: {test['candidate_hash_matches_v6_seed0']}.", "",
              f"Test shows A3 is strongest on mean: {test['mean_mrr']['A3'] >= max(test['mean_mrr']['A1'], test['mean_mrr']['A4'])}.", ""]
    (OUT / "03_TEST_CONFIRMATION.md").write_text("\n".join(lines), encoding="utf-8")

    eff = final["efficiency"]
    lines = ["# V6.1 Efficiency", "", f"- Strict pool generation cold-start: {pool['pool_generation_seconds']:.4f}s.",
             f"- Train-only teacher fitting: Graph {pool['teacher_records']['Graph']['train_seconds']:.3f}s; Raw-HG {pool['teacher_records']['Raw-HG']['train_seconds']:.3f}s. These are one-time cold-start costs, not per-epoch selection overhead.",
             f"- Detached teacher score forward: Graph {pool['teacher_scoring_seconds']['Graph']:.4f}s; Raw-HG {pool['teacher_scoring_seconds']['Raw-HG']:.4f}s (cached score reuse avoids repeated forward passes).",
             f"- Cached rank/veto selection: total {pool['selection_seconds_total']:.4f}s; amortized across 10 epochs {pool['selection_seconds_total']/10:.6f}s/epoch.",
             f"- Cached score forward repeats for same teacher/pool: 0.",
             f"- A4 selection-only overhead relative to mean strict learner training time: {eff['cached_a4_selection_overhead_target_under_5pct']} under 5% target.", ""]
    (OUT / "04_EFFICIENCY.md").write_text("\n".join(lines), encoding="utf-8")

    lines = ["# V6.1 Final Report", "", f"STATUS: {final['status']}", f"STRICT_PROTOCOL: {final['strict_protocol']}", "",
             "FILTERED_RESULTS:"]
    for method in METHODS:
        lines.append(f"- {method}: {fmt(filtered['mean_mrr'][method], filtered['sample_sd_mrr'][method])}")
    lines += ["", "STRICT_RESULTS:"]
    for method in METHODS:
        lines.append(f"- {method}: {fmt(strict['mean_mrr'][method], strict['sample_sd_mrr'][method])}")
    lines += ["", "VALIDATION_MEAN_STD:"]
    for method in METHODS:
        lines.append(f"- {method}: {fmt(strict['mean_mrr'][method], strict['sample_sd_mrr'][method])}")
    lines += ["", "TEST_MEAN_STD:"]
    for method in METHODS:
        lines.append(f"- {method}: {fmt(test['mean_mrr'][method], test['sample_sd_mrr'][method])}")
    lines += ["", f"TRUE_VETO_FUTURE_POSITIVE_RATE: {e['true_veto_rate']['rate']:.8f}",
              f"SHUFFLED_VETO_FUTURE_POSITIVE_RATE: {e['shuffled_veto_rate_mean_across_seeds']['rate']:.8f}",
              f"RANDOM_VETO_FUTURE_POSITIVE_RATE: {e['random_veto_rate_mean_across_seeds']['rate']:.8f}",
              f"ENRICHMENT_RATIO: {e['true_veto_enrichment_vs_prepool']['ratio']}",
              f"ODDS_RATIO: true-vs-shuffled {e['true_vs_shuffled_aggregate']['odds_ratio_haldane_corrected']:.6g}; true-vs-random {e['true_vs_random_aggregate']['odds_ratio_haldane_corrected']:.6g}",
              f"HG_PERCENTILE_MONOTONICITY: {e['hg_percentile_monotonicity']['nondecreasing']}",
              f"STRICT_MECHANISM_SIGNAL: {'YES' if strict_signal else 'NO'}",
              f"MECHANISM_SUPPORTED: {'YES' if mechanism_supported else 'NO'}",
              f"PERFORMANCE_SUPPORTED: {'YES' if performance_supported else 'NO'}",
              f"EFFICIENCY: cached selection {pool['selection_seconds_total']:.4f}s total / {pool['selection_seconds_total']/10:.6f}s per epoch; cold teacher scoring Graph {pool['teacher_scoring_seconds']['Graph']:.4f}s, Raw-HG {pool['teacher_scoring_seconds']['Raw-HG']:.4f}s.",
              f"FINAL_DECISION: {decision}", "", f"NEXT_EXPECTED_STEP: {final['next_expected_step']}", "",
              ("A4 meets the predeclared test performance gate, but the requested false-negative mechanism is not statistically confirmed; report these as separate findings." if performance_supported and not mechanism_supported else ""), "",
              "Interpretation is restricted to the measured Cora standard split and frozen V6 rule. Novelty status remains EXACT_RULE_UNVERIFIED.", ""]
    (OUT / "FINAL_REPORT.md").write_text("\n".join(lines), encoding="utf-8")

    status = load_json(OUT / "status.json")
    status.update({"state": "COMPLETE", "phase": "complete", "current": None,
                   "test_evaluated": True, "final_decision": decision})
    write_json(OUT / "status.json", status)


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"preflight", "train", "validate", "test", "report"}:
        raise SystemExit("usage: run_negative_v6_1.py {preflight|train|validate|test|report}")
    phase = sys.argv[1]
    if phase == "preflight":
        run_preflight()
    elif phase == "train":
        run_train_only_phase()
    elif phase == "validate":
        run_validation_phase()
    elif phase == "test":
        run_test_and_posthoc_phase()
    else:
        render_reports()


if __name__ == "__main__":
    main()
