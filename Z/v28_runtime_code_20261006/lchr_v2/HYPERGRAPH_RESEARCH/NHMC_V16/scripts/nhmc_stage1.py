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
import torch
from torch import nn

HERE = Path(__file__).resolve()
OUT = HERE.parents[1]
ROOT = Path(os.environ.get("NHMC_RUNTIME_ROOT", HERE.parents[4] / "HMC_V15" / "runtime")).resolve()
V71 = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V7_1"
V61 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
V7 = ROOT / "HYPERGRAPH_RESEARCH" / "HARDNESS_V7"
sys.path[:0] = [str(ROOT / "src"), str(V71), str(V61), str(V7),
                str(ROOT / "HYPERGRAPH_RESEARCH" / "CODNS_V6_2")]

import experiment_v71 as base  # noqa: E402
import run_negative_v6_1 as v61  # noqa: E402
import train_hardness_v7 as v7  # noqa: E402
import run_codns_v6_2 as engine  # noqa: E402
import nhmc_stage0 as stage0  # noqa: E402

EPOCHS = 5
VALID_SEED = 72200
VALID_NEGATIVES = 20
NATIVE_ENCODER_DIM = 8
ARMS = ("B0_BASELINE", "B1_HRA", "B2_NATIVE_SCALAR", "C1_NHMC_SIZE",
        "C2_NHMC_SHUFFLE", "H1_NHMC_REAL")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pair_key(pair: tuple[int, int] | np.ndarray, n: int) -> int:
    u, v = sorted(map(int, pair))
    return u * n + v


def make_validation_candidates(view, positives: np.ndarray) -> tuple[np.ndarray, dict]:
    """Validation candidates draw only against train-derived forbidden pairs."""
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling

    forbidden_rows, forbidden = v61.make_train_forbidden(view)
    pool_count = max(VALID_NEGATIVES * len(positives), VALID_NEGATIVES)
    pool = uniform_negative_sampling(view.num_nodes, forbidden_rows, pool_count, VALID_SEED)
    negatives = grouped_negatives(positives, pool, VALID_NEGATIVES, VALID_SEED + 1)
    # A query's own target cannot also be one of its negative candidates. This
    # evaluation-only check does not inspect any other held-out identity.
    collisions = 0
    reserve = None
    reserve_cursor = 0
    for row, positive in enumerate(positives):
        target = tuple(sorted(map(int, positive)))
        for col, negative in enumerate(negatives[row]):
            if tuple(sorted(map(int, negative))) != target:
                continue
            collisions += 1
            if reserve is None:
                reserve = uniform_negative_sampling(
                    view.num_nodes, forbidden_rows, max(100, VALID_NEGATIVES * len(positives)), VALID_SEED + 2,
                )
            while reserve_cursor < len(reserve):
                candidate = reserve[reserve_cursor]
                reserve_cursor += 1
                if tuple(sorted(map(int, candidate))) != target:
                    negatives[row, col] = candidate
                    break
            else:
                raise RuntimeError("could not replace a validation self-positive from the train-only reserve pool")
    if any(v61.canonical_edge(pair) in forbidden for pair in negatives.reshape(-1, 2)):
        raise RuntimeError("validation negative candidate overlaps a train/message edge")
    return negatives, {
        "source": "uniform candidates filtered only by train/message edges",
        "seed": VALID_SEED, "grouping_seed": VALID_SEED + 1,
        "negative_count_per_positive": VALID_NEGATIVES,
        "shape": list(negatives.shape), "self_positive_collisions_replaced": collisions,
        "train_forbidden_count": len(forbidden_rows),
        "heldout_test_identities_used": False,
    }


def _load_stage0_cache(dataset: str, n_nodes: int) -> dict | None:
    archive_path = OUT / "diagnostics" / f"stage0_{dataset}_features.npz"
    token_path = OUT / "diagnostics" / f"stage0_{dataset}_native_tokens.npy"
    if not (archive_path.exists() and token_path.exists()):
        return None
    with np.load(archive_path, allow_pickle=False) as archive:
        data = {key: archive[key].copy() for key in archive.files}
    tokens = np.load(token_path, mmap_mode="r")
    offsets = np.asarray(data["pair_token_offsets"], dtype=np.int64)
    mapping = {}
    for row, pair in enumerate(data["pairs"]):
        mapping[pair_key(pair, n_nodes)] = row
    return {"data": data, "tokens": tokens, "offsets": offsets, "mapping": mapping}


def _pair_tokens(ctx: dict, pair: np.ndarray, target: bool) -> tuple[np.ndarray, float, float, int]:
    u, v = map(int, pair)
    projection = stage0._pair_projection(ctx, u, v, target)
    shared, _, _, hra, _, _, expected = projection
    rows = []
    native_scalar = 0.0
    for sizes, overlap, stratum, contribution in stage0._iter_native_tokens(ctx, u, v, target):
        rows.append((0, stratum, sizes, overlap))
        native_scalar += contribution
    records = np.asarray(rows, dtype=stage0.TOKEN_DTYPE)
    if len(records) != expected:
        raise RuntimeError(f"token count mismatch for pair {(u, v)}: {len(records)} != {expected}")
    return records, float(hra), float(native_scalar), int(len(shared))


def _resume_pair_cache(dataset: str, cache_dir: Path, expected_keys: np.ndarray,
                       expected_target_mask: np.ndarray) -> tuple[dict, dict] | None:
    """Reuse an intact cache from a run that stopped only at the zero-init audit."""
    status_path = OUT / "diagnostics" / f"stage1_{dataset}_status.json"
    if not status_path.exists():
        return None
    status = v61.load_json(status_path)
    error = str(status.get("error", ""))
    if status.get("state") != "FAILED" or "NHMC zero-init equivalence failed" not in error:
        return None

    archive_path = cache_dir / f"{dataset}_pair_features.npz"
    raw_path = cache_dir / f"{dataset}_native_tokens.npy"
    shuffle_path = cache_dir / f"{dataset}_shuffle_overlap.npy"
    meta_path = cache_dir / f"{dataset}_cache.json"
    if not all(path.is_file() for path in (archive_path, raw_path, shuffle_path, meta_path)):
        return None
    meta = v61.load_json(meta_path)
    if (sha256_file(archive_path) != meta.get("pair_feature_archive_sha256")
            or sha256_file(raw_path) != meta.get("raw_tokens_sha256")
            or sha256_file(shuffle_path) != meta.get("shuffle_overlap_sha256")):
        return None
    with np.load(archive_path, allow_pickle=False) as archive:
        cache = {key: archive[key].copy() for key in archive.files}
    if not np.array_equal(cache.get("keys"), expected_keys):
        return None
    offsets = np.asarray(cache.get("offsets"), dtype=np.int64)
    token_count = int(meta.get("token_count", -1))
    pair_count = int(meta.get("pair_count_unique", -1))
    if (pair_count != len(expected_keys) or len(offsets) != pair_count + 1
            or len(offsets) == 0 or int(offsets[0]) != 0
            or int(offsets[-1]) != token_count or np.any(offsets[1:] < offsets[:-1])
            or cache["tokens_real"].shape != (token_count, 6)
            or cache["tokens_shuffle"].shape != (token_count, 6)
            or cache["hra"].shape != (pair_count,)
            or cache["ns"].shape != (pair_count,)
            or cache["support"].shape != (pair_count,)):
        return None

    meta = dict(meta)
    meta["resume_reused_after_zero_init_audit_failure"] = True
    meta["resume_audit"] = {
        "prior_failure_phase": "zero_init_equivalence_preflight_after_both_feature_caches_completed",
        "expected_pair_keys_hash": v61.array_hash(expected_keys),
        "expected_target_mask_hash": v61.array_hash(expected_target_mask.astype(np.uint8)),
        "pair_keys_match": True,
        "cache_file_hashes_match": True,
        "cache_generated_by_current_frozen_pair_cache_builder": True,
        "test_evaluated": False,
    }
    return {
        "keys": cache["keys"], "offsets": offsets,
        "tokens_real": cache["tokens_real"], "tokens_shuffle": cache["tokens_shuffle"],
        "hra": cache["hra"], "ns": cache["ns"], "support": cache["support"],
        "pair_count": pair_count, "token_count": token_count,
    }, meta


def build_pair_cache(dataset: str, ctx: dict, pairs: np.ndarray, targets: np.ndarray,
                     cache_dir: Path, reuse_stage0: bool) -> tuple[dict, dict]:
    """Build/reuse exact raw tokens, then make a separate within-split shuffle."""
    n_nodes = int(ctx["n"])
    canonical = stage0.canonical_pairs(pairs)
    if len(targets) != len(canonical):
        raise ValueError("target-mask vector does not align with candidate pairs")
    target_by_key: dict[int, bool] = {}
    for pair, target in zip(canonical, targets):
        key = pair_key(pair, n_nodes)
        target_by_key[key] = bool(target_by_key.get(key, False) or target)
    unique_pairs = np.unique(canonical, axis=0)
    keys = np.asarray([pair_key(pair, n_nodes) for pair in unique_pairs], dtype=np.int64)
    expected_target_mask = np.asarray([target_by_key[int(key)] for key in keys], dtype=np.uint8)
    resumed = _resume_pair_cache(dataset, cache_dir, keys, expected_target_mask)
    if resumed is not None:
        return resumed
    stage0_cache = _load_stage0_cache(dataset, n_nodes) if reuse_stage0 else None
    cached_map = stage0_cache["mapping"] if stage0_cache else {}
    records_parts: list[np.ndarray] = []
    counts = np.zeros(len(unique_pairs), dtype=np.int64)
    hra_values = np.zeros(len(unique_pairs), dtype=np.float32)
    ns_values = np.zeros(len(unique_pairs), dtype=np.float32)
    support_values = np.zeros(len(unique_pairs), dtype=np.int32)
    reused, freshly_built = 0, 0
    for row, pair in enumerate(unique_pairs):
        key = int(keys[row])
        target = bool(target_by_key.get(key, False))
        cached_row = cached_map.get(key)
        if cached_row is not None:
            old_target = bool(stage0_cache["data"]["target_mask"][cached_row])
            if old_target == target:
                lo, hi = map(int, stage0_cache["offsets"][cached_row:cached_row + 2])
                records = np.asarray(stage0_cache["tokens"][lo:hi]).copy()
                records["pair"] = row
                hra_values[row] = float(stage0_cache["data"]["Z1"][cached_row, 0])
                ns_values[row] = float(stage0_cache["data"]["NS"][cached_row, 0])
                support_values[row] = int(round(math.expm1(float(stage0_cache["data"]["Z2"][cached_row, 0]))))
                reused += 1
            else:
                records, hra, ns, support = _pair_tokens(ctx, pair, target)
                records["pair"] = row
                hra_values[row], ns_values[row], support_values[row] = hra, ns, support
                freshly_built += 1
        else:
            records, hra, ns, support = _pair_tokens(ctx, pair, target)
            records["pair"] = row
            hra_values[row], ns_values[row], support_values[row] = hra, ns, support
            freshly_built += 1
        counts[row] = len(records)
        records_parts.append(records)
    offsets = np.r_[0, np.cumsum(counts, dtype=np.int64)]
    records_all = np.concatenate(records_parts) if records_parts else np.empty(0, dtype=stage0.TOKEN_DTYPE)
    if len(records_all) != int(offsets[-1]):
        raise RuntimeError("pair cache offsets disagree with raw token records")
    cache_dir.mkdir(parents=True, exist_ok=True)
    raw_path = cache_dir / f"{dataset}_native_tokens.npy"
    np.save(raw_path, records_all, allow_pickle=False)
    shuffle_path = cache_dir / f"{dataset}_shuffle_overlap.npy"
    seed_offset = {"cora": 1, "pubmed": 2, "citeseer": 3}[dataset]
    shuffle_seed = stage0.SHUFFLE_SEED + seed_offset + (100_000 if "valid" in cache_dir.name else 0)
    shuffle_meta = stage0._shuffle_tokens(raw_path, shuffle_path, offsets, shuffle_seed)
    records_disk = np.load(raw_path, mmap_mode="r")
    shuffled_overlap = np.load(shuffle_path, mmap_mode="r")
    real = np.column_stack((records_disk["size"], records_disk["overlap"])).astype(np.float32, copy=False)
    shuffle = np.column_stack((records_disk["size"], shuffled_overlap)).astype(np.float32, copy=False)
    meta = {
        "pair_count_unique": int(len(unique_pairs)), "token_count": int(len(records_all)),
        "stage0_raw_pair_cache_reused": int(reused), "fresh_pairs_computed": int(freshly_built),
        "raw_tokens_sha256": sha256_file(raw_path),
        "shuffle_overlap_sha256": sha256_file(shuffle_path),
        "shuffle": shuffle_meta, "shuffle_seed": int(shuffle_seed),
    }
    cache = {"keys": keys, "offsets": offsets, "tokens_real": real, "tokens_shuffle": shuffle,
             "hra": hra_values, "ns": ns_values, "support": support_values,
             "pair_count": len(unique_pairs), "token_count": len(records_all)}
    np.savez_compressed(
        cache_dir / f"{dataset}_pair_features.npz", keys=keys, offsets=offsets,
        tokens_real=real, tokens_shuffle=shuffle, hra=hra_values, ns=ns_values,
        support=support_values,
    )
    meta["pair_feature_archive_sha256"] = sha256_file(cache_dir / f"{dataset}_pair_features.npz")
    write_json(cache_dir / f"{dataset}_cache.json", meta)
    return cache, meta


class PairFeatureStore:
    def __init__(self, cache: dict, n_nodes: int, device: torch.device):
        self.n_nodes = int(n_nodes)
        self.keys = torch.as_tensor(cache["keys"], dtype=torch.long, device=device)
        self.offsets = torch.as_tensor(cache["offsets"], dtype=torch.long, device=device)
        self.real = torch.as_tensor(cache["tokens_real"], dtype=torch.float32, device=device)
        self.shuffled = torch.as_tensor(cache["tokens_shuffle"], dtype=torch.float32, device=device)
        self.hra = torch.as_tensor(cache["hra"], dtype=torch.float32, device=device)
        self.ns = torch.as_tensor(cache["ns"], dtype=torch.float32, device=device)
        self.support = torch.as_tensor(cache["support"], dtype=torch.float32, device=device)

    def lookup(self, pairs: torch.Tensor) -> torch.Tensor:
        low = torch.minimum(pairs[:, 0], pairs[:, 1])
        high = torch.maximum(pairs[:, 0], pairs[:, 1])
        wanted = low * self.n_nodes + high
        rows = torch.searchsorted(self.keys, wanted)
        if torch.any(rows >= len(self.keys)):
            raise KeyError("NHMC pair missing from the frozen train/validation feature cache")
        if torch.any(self.keys[rows] != wanted):
            raise KeyError("NHMC pair missing from the frozen train/validation feature cache")
        return rows


def _pool_nhmc(tokens: torch.Tensor, offsets: torch.Tensor, rows: torch.Tensor,
               encoder: nn.Module) -> tuple[torch.Tensor, torch.Tensor]:
    counts = offsets[rows + 1] - offsets[rows]
    batch = len(rows)
    total = int(counts.sum().item())
    if total == 0:
        zero = tokens.new_zeros((batch, NATIVE_ENCODER_DIM))
        return zero, zero
    segment = torch.repeat_interleave(torch.arange(batch, device=rows.device), counts)
    prefix = torch.cumsum(counts, dim=0) - counts
    prefix_rep = torch.repeat_interleave(prefix, counts)
    starts_rep = torch.repeat_interleave(offsets[rows], counts)
    token_ids = starts_rep + (torch.arange(total, device=rows.device) - prefix_rep)
    encoded = torch.relu(encoder(tokens[token_ids]))
    mean = encoded.new_zeros((batch, NATIVE_ENCODER_DIM))
    mean.index_add_(0, segment, encoded)
    mean = mean / counts.clamp_min(1).to(encoded.dtype).unsqueeze(1)
    maximum = encoded.new_full((batch, NATIVE_ENCODER_DIM), -torch.inf)
    maximum.scatter_reduce_(0, segment[:, None].expand(-1, NATIVE_ENCODER_DIM), encoded,
                            reduce="amax", include_self=True)
    maximum = torch.where(counts[:, None] > 0, maximum, torch.zeros_like(maximum))
    return mean, maximum


def make_model_class(arm: str, train_store: PairFeatureStore, valid_store: PairFeatureStore):
    from dcdlp.models.dcdlp import DCDLP as BaseDCDLP

    class NHMCWrappedDCDLP(BaseDCDLP):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._nhmc_enabled = arm != "B0_BASELINE"
            if arm in {"B1_HRA", "B2_NATIVE_SCALAR"}:
                with torch.random.fork_rng(devices=[]):
                    self.nhmc_scalar_residual = nn.Linear(1, 1)
                    nn.init.zeros_(self.nhmc_scalar_residual.weight)
                    nn.init.zeros_(self.nhmc_scalar_residual.bias)
            elif arm in {"C1_NHMC_SIZE", "C2_NHMC_SHUFFLE", "H1_NHMC_REAL"}:
                with torch.random.fork_rng(devices=[]):
                    self.nhmc_encoder = nn.Linear(6, NATIVE_ENCODER_DIM)
                    self.nhmc_residual = nn.Linear(2 * NATIVE_ENCODER_DIM + 2, 1)
                    nn.init.zeros_(self.nhmc_residual.weight)
                    nn.init.zeros_(self.nhmc_residual.bias)

        def forward(self, x, edge_index, pairs, remove_target_edges=True,
                    support_edge_index=None):
            output = super().forward(x, edge_index, pairs,
                                     remove_target_edges=remove_target_edges,
                                     support_edge_index=support_edge_index)
            if not self._nhmc_enabled:
                return output
            store = train_store if self.training else valid_store
            rows = store.lookup(pairs)
            if arm in {"B1_HRA", "B2_NATIVE_SCALAR"}:
                scalar = store.hra[rows] if arm == "B1_HRA" else store.ns[rows]
                delta = self.nhmc_scalar_residual(scalar.unsqueeze(-1)).squeeze(-1)
            else:
                if arm == "C2_NHMC_SHUFFLE":
                    tokens = store.shuffled
                else:
                    tokens = store.real
                if arm == "C1_NHMC_SIZE":
                    tokens = torch.cat((tokens[:, :3], torch.zeros_like(tokens[:, 3:])), dim=1)
                mean, maximum = _pool_nhmc(tokens, store.offsets, rows, self.nhmc_encoder)
                count = (store.offsets[rows + 1] - store.offsets[rows]).to(mean.dtype)
                support = store.support[rows]
                summary = torch.cat((mean, maximum, torch.log1p(count).unsqueeze(1),
                                     torch.log1p(support).unsqueeze(1)), dim=1)
                delta = self.nhmc_residual(summary).squeeze(-1)
            output["logit"] = output["logit"] + delta
            output["nhmc_delta"] = delta
            return output

    return NHMCWrappedDCDLP


def make_config(dataset: str, output_dir: Path, epochs: int):
    from dcdlp.train import TrainConfig

    baseline_config = v61.load_json(v61.BASELINE / "H" / "config.json")
    values = {key: value for key, value in baseline_config.items()
              if key in TrainConfig.__dataclass_fields__}
    values.update({
        "dataset": dataset.lower(), "seed": 0, "protocol_train": "uniform",
        "protocol_eval": "standard", "pretrain_epochs": int(epochs), "disentangle_epochs": 0,
        "hypergraph_mode": "raw", "hypergraph_construction": "raw_star",
        "ghhr_training_mode": "none", "complementarity_fusion_mode": "none",
        "evaluate_test": False, "device": "cuda", "output_dir": str(output_dir),
        "prediction_subdir": "raw",
    })
    return TrainConfig(**values)


def train_graph_teacher(dataset: str, view, pool: np.ndarray, cache_dir: Path) -> tuple[np.ndarray, dict]:
    """Train the existing train-only Graph teacher needed by frozen QTHS25."""
    from dcdlp import train as train_module
    from dcdlp.train import TrainConfig, edge_index_from_graph, score_pairs

    config = make_config(dataset, OUT / "experiments" / dataset / "graph_teacher", 10)
    config.hypergraph_mode = "disabled"
    train_forbidden_rows, forbidden = v61.make_train_forbidden(view)
    old_sampler, old_eval = train_module._sample_train_negatives, train_module.evaluate_split
    old_residualizer = train_module.fit_training_cn_residualizer
    eval_count = {"n": 0}

    def sampler(current_dataset, current_config, epoch):
        if current_dataset is not view or current_config is not config:
            raise RuntimeError("Graph-teacher sampler escaped the train-only view")
        rng = np.random.default_rng(int(current_config.seed) * 10_000 + int(epoch) + 710_000)
        columns = rng.integers(0, pool.shape[1], size=len(view.train_pos))
        negative = pool[np.arange(len(view.train_pos)), columns].copy()
        if any(v61.canonical_edge(pair) in forbidden for pair in negative):
            raise RuntimeError("Graph-teacher emitted a train-forbidden negative")
        return negative

    def diagnostic_eval(*args, **kwargs):
        eval_count["n"] += 1
        return {"mrr": float(eval_count["n"])}, []

    def no_residualizer(_dataset, _config):
        return None, {"fit_split": "train_only", "uses_valid_or_test": False}

    train_module._sample_train_negatives = sampler
    train_module.evaluate_split = diagnostic_eval
    train_module.fit_training_cn_residualizer = no_residualizer
    started = time.perf_counter()
    try:
        model, result = train_module.train_model(view, config)
    finally:
        train_module._sample_train_negatives = old_sampler
        train_module.evaluate_split = old_eval
        train_module.fit_training_cn_residualizer = old_residualizer
    device = torch.device("cuda")
    x = torch.as_tensor(view.features, dtype=torch.float32, device=device)
    edge_index = edge_index_from_graph(view.train_graph(), device)
    model.eval()
    with torch.no_grad():
        scores = score_pairs(model, x, edge_index, pool.reshape(-1, 2), batch_size=8192)["logit"]
    scores = np.asarray(scores, dtype=np.float32).reshape(len(pool), pool.shape[1])
    record = {
        "state": "COMPLETE", "dataset": dataset, "seed": 0, "epochs": 10,
        "hypergraph_mode": "disabled", "training_pool_hash": v61.array_hash(pool),
        "graph_teacher_score_hash": v61.array_hash(scores),
        "checkpoint": result.get("checkpoint"),
        "train_seconds": result.get("runtime", {}).get("train_seconds"),
        "wall_seconds": float(time.perf_counter() - started),
        "valid_or_test_labels_used_for_training_or_selection": False,
        "test_evaluated": False,
    }
    cache_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache_dir / f"{dataset}_graph_teacher_scores.npz", scores=scores)
    write_json(cache_dir / f"{dataset}_graph_teacher.json", record)
    del model
    torch.cuda.empty_cache()
    return scores, record


def _fixed_train_pool(dataset: str, view) -> tuple[np.ndarray, str, np.ndarray, dict]:
    pool, pool_hash = base.training_pool(view)
    if dataset == "cora":
        archive_path = V61 / "strict_train_candidates_and_selections.npz"
        with np.load(archive_path, allow_pickle=False) as archive:
            frozen_pool = archive["negative_candidates"].copy()
            frozen_train = archive["train_positive"].copy()
            scores = archive["score_graph"].copy()
        meta = v61.load_json(V61 / "strict_pool_metadata.json")
        if pool_hash != meta["candidate_pool_hash"] or not np.array_equal(pool, frozen_pool):
            raise RuntimeError("Cora Stage 1 pool differs from the frozen V7.1/QTHS25 pool")
        if not np.array_equal(stage0.canonical_pairs(view.train_pos), stage0.canonical_pairs(frozen_train)):
            raise RuntimeError("Cora Stage 1 train split differs from the frozen QTHS25 split")
        return pool, pool_hash, scores, {"source": "frozen_V6_1_graph_teacher_cache",
                                        "score_hash": v61.array_hash(scores),
                                        "pool_hash": pool_hash}
    teacher_dir = OUT / "diagnostics" / "stage1" / dataset
    score_path = teacher_dir / f"{dataset}_graph_teacher_scores.npz"
    teacher_path = teacher_dir / f"{dataset}_graph_teacher.json"
    if score_path.exists() and teacher_path.exists():
        cached_meta = v61.load_json(teacher_path)
        with np.load(score_path, allow_pickle=False) as archive:
            cached_scores = archive["scores"].copy()
        if (cached_meta.get("state") == "COMPLETE"
                and cached_meta.get("training_pool_hash") == pool_hash
                and cached_scores.shape == pool.shape[:2]
                and cached_meta.get("graph_teacher_score_hash") == v61.array_hash(cached_scores)):
            cached_meta["cache_reused"] = True
            return pool, pool_hash, cached_scores, cached_meta
    scores, teacher_meta = train_graph_teacher(dataset, view, pool, teacher_dir)
    teacher_meta["cache_reused"] = False
    return pool, pool_hash, scores, teacher_meta


def _check_zero_initialization(view, valid_pos: np.ndarray, config) -> dict:
    from dcdlp import train as train_module
    from dcdlp.train import ablation_profile, edge_index_from_graph
    from dcdlp.models.dcdlp import DCDLP

    profile = ablation_profile(config.ablation)
    kwargs = dict(
        input_dim=view.features.shape[1], hidden_dim=config.hidden_dim,
        branch_dim=config.branch_dim, num_layers=config.num_layers,
        dropout=config.dropout, backbone=config.backbone,
        use_interaction=profile["interaction"], active_branches=profile["active"],
        decoder_mode=profile["decoder"], cn_feature_mode=config.cn_feature_mode,
        cn_regressor=None, interaction_mode=config.interaction_mode,
        cn_input_schema=config.cn_input_schema, hypergraph_mode=config.hypergraph_mode,
        hypergraph_construction=config.hypergraph_construction,
        ghhr_enabled=False, complementarity_fusion_mode="none",
        fusion_gate_hidden_dim=config.fusion_gate_hidden_dim,
        fusion_margin_graph_threshold=config.fusion_margin_graph_threshold,
        fusion_margin_hypergraph_threshold=config.fusion_margin_hypergraph_threshold,
    )
    def instantiate(cls):
        return cls(kwargs["input_dim"], kwargs["hidden_dim"], kwargs["branch_dim"],
                   kwargs["num_layers"], kwargs["dropout"], kwargs["backbone"],
                   use_interaction=kwargs["use_interaction"], active_branches=kwargs["active_branches"],
                   decoder_mode=kwargs["decoder_mode"], cn_feature_mode=kwargs["cn_feature_mode"],
                   cn_regressor=kwargs["cn_regressor"], interaction_mode=kwargs["interaction_mode"],
                   cn_input_schema=kwargs["cn_input_schema"], hypergraph_mode=kwargs["hypergraph_mode"],
                   hypergraph_construction=kwargs["hypergraph_construction"], ghhr_enabled=False,
                   complementarity_fusion_mode="none", fusion_gate_hidden_dim=kwargs["fusion_gate_hidden_dim"],
                   fusion_margin_graph_threshold=kwargs["fusion_margin_graph_threshold"],
                    fusion_margin_hypergraph_threshold=kwargs["fusion_margin_hypergraph_threshold"]).to("cuda")

    # Stores are assigned by the caller before this function's forward probe.
    train_store, valid_store = _check_zero_initialization.train_store, _check_zero_initialization.valid_store
    custom_class = make_model_class("H1_NHMC_REAL", train_store, valid_store)
    torch.manual_seed(0)
    torch.cuda.manual_seed_all(0)
    base_model = instantiate(DCDLP).eval()
    torch.manual_seed(0)
    torch.cuda.manual_seed_all(0)
    augmented_model = instantiate(custom_class).eval()
    base_state = base_model.state_dict()
    custom_state = augmented_model.state_dict()
    backbone_equal = all(torch.equal(base_state[k], custom_state[k]) for k in base_state)
    x = torch.as_tensor(view.features, dtype=torch.float32, device="cuda")
    edge_index = edge_index_from_graph(view.train_graph(), torch.device("cuda"))
    pair = torch.as_tensor(valid_pos[:1], dtype=torch.long, device="cuda")
    with torch.no_grad():
        plain = base_model(x, edge_index, pair, remove_target_edges=True)["logit"]
        wrapped_output = augmented_model(x, edge_index, pair, remove_target_edges=True)
        wrapped = wrapped_output["logit"]
    error = float(torch.max(torch.abs(plain - wrapped)).detach().cpu())
    residual_parameters = list(augmented_model.nhmc_residual.parameters())
    residual_is_zero = all(torch.count_nonzero(parameter).item() == 0
                           for parameter in residual_parameters)
    residual_output_max_abs = float(torch.max(torch.abs(
        wrapped_output["nhmc_delta"])).detach().cpu())
    del base_model, augmented_model
    torch.cuda.empty_cache()
    tolerance = 2e-7
    if not backbone_equal or not residual_is_zero or error > tolerance or residual_output_max_abs != 0.0:
        raise RuntimeError(
            f"NHMC zero-init equivalence failed: base_equal={backbone_equal}, "
            f"residual_is_zero={residual_is_zero}, residual_output={residual_output_max_abs}, "
            f"error={error}, tolerance={tolerance}"
        )
    return {"base_initialization_identical": backbone_equal,
            "initial_logit_max_abs_difference": error,
            "zero_initialized_residual": residual_is_zero,
            "initial_residual_output_max_abs": residual_output_max_abs,
            "max_abs_tolerance": tolerance}


def _run_arm(dataset: str, arm: str, view, pool: np.ndarray, pool_hash: str,
             selected: np.ndarray, valid_pos: np.ndarray, valid_neg: np.ndarray,
             valid_hash: str, train_store: PairFeatureStore,
             valid_store: PairFeatureStore) -> dict:
    from dcdlp import train as train_module
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.evaluation.ranking import ranking_metrics
    from dcdlp.models.dcdlp import DCDLP as BaseDCDLP

    old_epochs = engine.EPOCHS
    old_out = engine.OUT
    old_class = train_module.DCDLP
    old_train_model = train_module.train_model
    capture: list[torch.nn.Module] = []
    engine.EPOCHS = EPOCHS
    engine.OUT = OUT / "experiments" / f"stage1_{dataset}" / "runner_state"
    torch.cuda.reset_peak_memory_stats()
    model_class = BaseDCDLP if arm == "B0_BASELINE" else make_model_class(arm, train_store, valid_store)
    train_module.DCDLP = model_class

    def capture_model(*args, **kwargs):
        model, result = old_train_model(*args, **kwargs)
        capture.append(model)
        return model, result

    train_module.train_model = capture_model
    arm_dir = OUT / "experiments" / f"stage1_{dataset}" / "arms" / arm
    try:
        run_record = engine.train_one(
            view, f"NHMC_{arm}", 0, selected, str(arm_dir), valid_pos, valid_neg,
            initialize_from_v6=False, dataset_name=dataset, hypergraph_mode="raw",
        )
    finally:
        train_module.train_model = old_train_model
        train_module.DCDLP = old_class
        engine.EPOCHS = old_epochs
        engine.OUT = old_out
    if len(capture) != 1:
        raise RuntimeError(f"{arm} did not return exactly one in-memory model")
    model = capture[0]
    device = torch.device("cuda")
    x = torch.as_tensor(view.features, dtype=torch.float32, device=device)
    edge_index = edge_index_from_graph(view.train_graph(), device)
    model.eval()
    with torch.no_grad():
        positive = score_pairs(model, x, edge_index, valid_pos, batch_size=8192)["logit"]
        negative = score_pairs(model, x, edge_index, valid_neg.reshape(-1, 2), batch_size=8192)["logit"]
    metrics = ranking_metrics(positive, negative.reshape(len(valid_pos), valid_neg.shape[1]))
    trainable_parameters = sum(
        int(parameter.numel()) for parameter in model.parameters() if parameter.requires_grad
    )
    added_parameters = 0
    if arm in {"B1_HRA", "B2_NATIVE_SCALAR"}:
        added_parameters = sum(p.numel() for p in model.nhmc_scalar_residual.parameters())
    elif arm in {"C1_NHMC_SIZE", "C2_NHMC_SHUFFLE", "H1_NHMC_REAL"}:
        added_parameters = sum(p.numel() for p in model.nhmc_encoder.parameters()) + sum(
            p.numel() for p in model.nhmc_residual.parameters())
    record = {
        "state": "COMPLETE", "dataset": dataset, "arm": arm, "seed": 0,
        "epochs": EPOCHS, "validation_only": True, "test_evaluated": False,
        "train_pool_hash": pool_hash, "selected_negative_hash": v61.array_hash(selected),
        "validation_candidate_hash": valid_hash,
        "validation_metrics": {k: float(v) for k, v in metrics.items()
                               if isinstance(v, (int, float, np.floating, np.integer))},
        "validation_curve_epoch_mrr": [row["validation_mrr"] for row in run_record.get("validation_curve", [])],
        "train_seconds": run_record.get("train_seconds"), "wall_seconds": run_record.get("wall_seconds"),
        "peak_gpu_mb": run_record.get("runtime", {}).get("peak_gpu_mb"),
        "trainable_parameters": int(trainable_parameters),
        "added_nhmc_parameters": int(added_parameters),
        "checkpoint": run_record.get("checkpoint"),
        "checkpoint_sha256": run_record.get("checkpoint_file_sha256"),
        "model_state_hash": run_record.get("model_state_hash"),
        "sampler": "same fixed QTHS25 one-negative-per-train-positive across all arms",
    }
    write_json(OUT / "experiments" / f"stage1_{dataset}" / f"{arm}.json", record)
    del capture[:]
    del model
    torch.cuda.empty_cache()
    return record


def run_stage1(dataset: str) -> dict:
    dataset = dataset.lower()
    if dataset not in {"cora", "pubmed", "citeseer"}:
        raise ValueError(dataset)
    import torch_geometric
    from dcdlp.train import edge_index_from_graph

    t_start = time.perf_counter()
    full, view = base.init_dataset(dataset)
    train_pos = stage0.canonical_pairs(np.asarray(view.train_pos, dtype=np.int64))
    pool, pool_hash, graph_scores, teacher_meta = _fixed_train_pool(dataset, view)
    if graph_scores.shape != pool.shape[:2]:
        raise RuntimeError(f"QTHS25 Graph-score shape mismatch: {graph_scores.shape} != {pool.shape[:2]}")
    qths_ids, qths_meta = v7.make_ids(pool, graph_scores, train_pos, .25)
    selected = pool[np.arange(len(pool)), qths_ids].copy()
    forbidden_rows, forbidden = v61.make_train_forbidden(view)
    if any(v61.canonical_edge(pair) in forbidden for pair in selected):
        raise RuntimeError("QTHS25 selected a train/message-positive pair")
    valid_pos = stage0.canonical_pairs(np.asarray(full.valid_pos, dtype=np.int64))
    valid_neg, valid_sampling = make_validation_candidates(view, valid_pos)
    valid_hash = v61.array_hash(valid_neg)
    engine.candidate_pool = pool
    engine.candidate_pool_hash = pool_hash
    engine.validation_candidate_hash = valid_hash
    del full
    if (type(view).__name__ != "TrainOnlyView"
            or getattr(view, "_empty", np.empty((1, 2))).shape != (0, 2)):
        raise RuntimeError("legacy training API placeholders are not empty train-only sentinels")
    status_path = OUT / "diagnostics" / f"stage1_{dataset}_status.json"
    write_json(status_path, {"state": "RUNNING", "phase": "building_train_only_pair_cache",
                             "dataset": dataset, "test_evaluated": False,
                             "gpu": torch.cuda.get_device_name(0),
                             "train_pool_hash": pool_hash})
    ctx = stage0.build_structure(stage0.build_adjacency(int(view.num_nodes), train_pos))
    train_pairs = np.vstack((train_pos, selected))
    train_targets = np.r_[np.ones(len(train_pos), dtype=bool), np.zeros(len(selected), dtype=bool)]
    valid_pairs = np.vstack((valid_pos, valid_neg.reshape(-1, 2)))
    valid_targets = np.zeros(len(valid_pairs), dtype=bool)
    root_cache = OUT / "experiments" / f"stage1_{dataset}" / "cache"
    train_cache_np, train_cache_meta = build_pair_cache(
        dataset, ctx, train_pairs, train_targets, root_cache / "train", reuse_stage0=True,
    )
    valid_cache_np, valid_cache_meta = build_pair_cache(
        dataset, ctx, valid_pairs, valid_targets, root_cache / "valid", reuse_stage0=False,
    )
    device = torch.device("cuda")
    train_store = PairFeatureStore(train_cache_np, view.num_nodes, device)
    valid_store = PairFeatureStore(valid_cache_np, view.num_nodes, device)
    config = make_config(dataset, OUT / "experiments" / f"stage1_{dataset}" / "zero_init_probe", EPOCHS)
    _check_zero_initialization.train_store = train_store
    _check_zero_initialization.valid_store = valid_store
    zero_init = _check_zero_initialization(view, valid_pos, config)
    status = {
        "state": "RUNNING", "phase": "training_six_frozen_arms", "dataset": dataset,
        "test_evaluated": False, "gpu": torch.cuda.get_device_name(0),
        "train_pool_hash": pool_hash, "selected_negative_hash": v61.array_hash(selected),
        "validation_candidate_hash": valid_hash, "qths25": qths_meta,
        "graph_teacher": teacher_meta, "validation_candidate_sampling": valid_sampling,
        "train_cache": train_cache_meta, "validation_cache": valid_cache_meta,
        "zero_init_audit": zero_init,
    }
    write_json(status_path, status)
    config_baseline = make_config(dataset, OUT / "experiments" / f"stage1_{dataset}" / "arms" / "B0_BASELINE", EPOCHS)
    records = {}
    for arm in ARMS:
        current = dict(status)
        current["current_arm"] = arm
        write_json(status_path, current)
        records[arm] = _run_arm(
            dataset, arm, view, pool, pool_hash, selected, valid_pos, valid_neg,
            valid_hash, train_store, valid_store,
        )
        current["completed_arms"] = list(records)
        write_json(status_path, current)
    baseline_params = int(records["B0_BASELINE"]["trainable_parameters"])
    if baseline_params <= 0:
        raise RuntimeError(f"invalid frozen-baseline trainable parameter count: {baseline_params}")
    parameter_budget = {
        arm: {"added": row["added_nhmc_parameters"],
              "fraction_of_baseline": row["added_nhmc_parameters"] / max(1, baseline_params)}
        for arm, row in records.items() if arm != "B0_BASELINE"
    }
    if any(value["fraction_of_baseline"] > .02 for value in parameter_budget.values()):
        decision = "PARAMETER_BUDGET_VIOLATION"
    else:
        mrr = {arm: float(row["validation_metrics"]["mrr"]) for arm, row in records.items()}
        delta = {arm: mrr["H1_NHMC_REAL"] - value for arm, value in mrr.items()
                 if arm != "H1_NHMC_REAL"}
        shuffle_power = train_cache_meta["shuffle"]["informative_shuffle_fraction"]
        shuffle_adequate = shuffle_power >= .30
        passed = (
            delta["B0_BASELINE"] >= .003
            and delta["B1_HRA"] >= .002
            and delta["B2_NATIVE_SCALAR"] >= .002
            and delta["C1_NHMC_SIZE"] >= .002
            and (delta["C2_NHMC_SHUFFLE"] >= .002 if shuffle_adequate
                 else delta["C2_NHMC_SHUFFLE"] > 0.0)
        )
        decision = "NHMC_STAGE1_GO" if passed else "NHMC_STAGE1_REJECT"
    result = {
        "state": "COMPLETE", "dataset": dataset, "decision": decision,
        "stage0_decision_is_diagnostic_only": True,
        "validation_only": True, "test_evaluated": False,
        "arms": records, "mrr": {arm: row["validation_metrics"]["mrr"] for arm, row in records.items()},
        "deltas_h1_minus_controls": delta if "delta" in locals() else None,
        "stage1_gate": {"passed": decision == "NHMC_STAGE1_GO",
                         "thresholds": {"H1-B0": .003, "H1-B1": .002,
                                        "H1-B2": .002, "H1-C1": .002,
                                        "H1-C2": .002 if train_cache_meta["shuffle"]["informative_shuffle_fraction"] >= .30 else ">0"},
                         "shuffle_power_train": train_cache_meta["shuffle"]["informative_shuffle_fraction"],
                         "shuffle_power_validation": valid_cache_meta["shuffle"]["informative_shuffle_fraction"]},
        "parameter_budget": {"baseline_trainable_parameters": baseline_params,
                             "per_arm": parameter_budget,
                             "max_allowed_fraction": .02},
        "train_pool_hash": pool_hash, "qths25_selected_negative_hash": v61.array_hash(selected),
        "validation_candidate_hash": valid_hash, "qths25": qths_meta,
        "graph_teacher": teacher_meta, "validation_candidate_sampling": valid_sampling,
        "train_cache": train_cache_meta, "validation_cache": valid_cache_meta,
        "zero_init_audit": zero_init,
        "strict_train_only": True,
        "heldout_positive_placeholder_reads": dict(view.placeholder_reads),
        "legacy_train_api_empty_placeholders": {
            "view_type": type(view).__name__,
            "empty_placeholder_shape": list(getattr(view, "_empty", np.empty((1, 2))).shape),
            "placeholder_values_exposed": False,
            "all_positive_accessed": False,
            "test_evaluated": False,
        },
        "wall_seconds": float(time.perf_counter() - t_start),
        "source_hashes": {"stage1_script": sha256_file(HERE),
                          "stage0_script": sha256_file(stage0.HERE),
                          "experiment_v71": sha256_file(V71 / "experiment_v71.py"),
                          "run_negative_v6_1": sha256_file(V61 / "run_negative_v6_1.py")},
    }
    result_path = OUT / "experiments" / f"stage1_{dataset}" / "results.json"
    write_json(result_path, result)
    status.update({"state": "COMPLETE", "phase": "stage1_complete", "decision": decision,
                   "completed_arms": list(records), "test_evaluated": False})
    write_json(status_path, status)
    if (type(view).__name__ != "TrainOnlyView"
            or getattr(view, "_empty", np.empty((1, 2))).shape != (0, 2)):
        raise RuntimeError("legacy training API placeholders are not empty train-only sentinels")
    return result


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: nhmc_stage1.py {cora|pubmed|citeseer}")
    dataset = sys.argv[1].lower()
    try:
        result = run_stage1(dataset)
    except Exception as exc:
        path = OUT / "diagnostics" / f"stage1_{dataset}_status.json"
        write_json(path, {"state": "FAILED", "dataset": dataset,
                          "phase": "failed", "error": repr(exc),
                          "traceback": traceback.format_exc(), "test_evaluated": False})
        raise
    print(json.dumps({"dataset": dataset, "decision": result["decision"],
                      "mrr": result["mrr"], "wall_seconds": result["wall_seconds"],
                      "test_evaluated": False}, indent=2), flush=True)


if __name__ == "__main__":
    main()
