"""V8 QTHS paperization and backbone-generalization experiment.

This file reuses the frozen V7.1 split, candidate-pool, teacher-score and
training harness. It adds no sampler proposal: RANDOM_HARD50 and SH75 are
registered controls; QTHS25 remains the sole proposed rule.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import importlib
import json
import math
import multiprocessing as mp
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V8_PAPER"
V71 = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V7_1"
V61 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
V7 = ROOT / "HYPERGRAPH_RESEARCH" / "HARDNESS_V7"
sys.path[:0] = [str(ROOT / "src"), str(V71), str(V61), str(V7)]

import experiment_v71 as base  # noqa: E402
import run_negative_v6_1 as v61  # noqa: E402
import train_hardness_v7 as v7  # noqa: E402
engine = base.engine

SEEDS = (0, 1, 2)
EXTENDED_SEEDS = (3, 4)
METHODS = ("UNIFORM", "GRAPH_HARD", "QTHS25")
RANDOM_SEED_OFFSET = 810_000


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def task_key(task: dict) -> str:
    extra = f"_a{task['alpha']:.2f}" if task.get("alpha") is not None else ""
    return f"{task['stage']}_{task['dataset']}_{task['backbone']}_{task['method']}_s{task['seed']}{extra}".lower()


def state_path(task: dict) -> Path:
    return OUT / "state" / "jobs" / f"{task_key(task)}.json"


def update_status(**values) -> None:
    path = OUT / "status.json"
    old = read_json(path) if path.exists() else {}
    old.update(values)
    if values.get("state") != "FAILED":
        old.pop("traceback", None)
    old["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    write_json(path, old)


def worker_init() -> None:
    os.environ.setdefault("OMP_NUM_THREADS", "4")
    os.environ.setdefault("MKL_NUM_THREADS", "4")
    import torch
    torch.set_num_threads(4)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass


_NODE_ENCODER_PATCHED = False


def patch_gat_encoder() -> None:
    """Add one standard single-head GAT option inside this experiment only."""
    global _NODE_ENCODER_PATCHED
    if _NODE_ENCODER_PATCHED:
        return
    import torch
    from torch import nn
    from torch.nn import functional as F
    from torch_geometric.nn import GATConv
    model_module = importlib.import_module("dcdlp.models.dcdlp")
    original = model_module.NodeEncoder

    class V8NodeEncoder(original):
        def __init__(self, input_dim: int, hidden_dim: int = 128, num_layers: int = 2,
                     dropout: float = 0.3, backbone: str = "gcn") -> None:
            if backbone != "gat":
                super().__init__(input_dim, hidden_dim, num_layers, dropout, backbone)
                self._v8_is_gat = False
                return
            nn.Module.__init__(self)
            dims = [input_dim] + [hidden_dim] * num_layers
            self.layers = nn.ModuleList([
                GATConv(dims[i], dims[i + 1], heads=1, concat=False,
                        dropout=dropout, add_self_loops=True)
                for i in range(num_layers)
            ])
            self.norms = nn.ModuleList([nn.LayerNorm(hidden_dim) for _ in range(num_layers)])
            self.dropout = dropout
            self._v8_is_gat = True

        def forward(self, x, edge_index):
            if not self._v8_is_gat:
                return super().forward(x, edge_index)
            for layer, norm in zip(self.layers, self.norms):
                x = norm(layer(x, edge_index))
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
            return x

    model_module.NodeEncoder = V8NodeEncoder
    _NODE_ENCODER_PATCHED = True


def configure_backbone(backbone: str):
    if backbone == "gat":
        patch_gat_encoder()
    original_load = v61.load_json
    baseline_config = (v61.BASELINE / "H" / "config.json").resolve()

    def load_with_backbone(path):
        value = original_load(path)
        try:
            is_config = Path(path).resolve() == baseline_config
        except (TypeError, OSError):
            is_config = False
        if is_config:
            value["backbone"] = backbone
        return value

    v61.load_json = load_with_backbone
    return original_load


def dataset_context(name: str):
    full, view = base.init_dataset(name)
    if name == "cora":
        archive = np.load(V61 / "strict_train_candidates_and_selections.npz", allow_pickle=False)
        pool = archive["negative_candidates"].copy()
        scores = archive["score_graph"].copy()
        archived_pos = archive["train_positive"].copy()
        archive.close()
        meta = read_json(V61 / "strict_pool_metadata.json")
        pool_hash = meta["candidate_pool_hash"]
        if not np.array_equal(archived_pos, view.train_pos):
            raise RuntimeError("Cora frozen training positives differ from V6.1")
        frozen = read_json(V71 / "results.json")["cora"]
        if pool_hash != frozen["train_pool_hash"] or v61.array_hash(scores) != frozen["teacher_scores_hash"]:
            raise RuntimeError("Cora frozen candidate pool or graph-teacher score hash mismatch")
    else:
        pool, pool_hash = base.training_pool(view)
        teacher_dir = V71 / "TEACHERS" / name
        teacher_meta = read_json(teacher_dir / "graph_teacher.json")
        with np.load(teacher_dir / "graph_teacher_scores.npz", allow_pickle=False) as archive:
            cached_pool = archive["candidates"].copy()
            scores = archive["scores"].copy()
        if pool_hash != teacher_meta["train_pool_hash"] or not np.array_equal(pool, cached_pool):
            raise RuntimeError(f"{name} frozen teacher candidate pool mismatch")
        if v61.array_hash(scores) != teacher_meta["scores_hash"]:
            raise RuntimeError(f"{name} frozen graph-teacher score hash mismatch")
    if pool.shape != (len(view.train_pos), 20, 2) or scores.shape != pool.shape[:2]:
        raise RuntimeError(f"Unexpected {name} train pool or score shape: {pool.shape}, {scores.shape}")
    valid_pos, valid_neg, valid_hash = base.make_eval_candidates(full, "valid")
    return full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash


def selected_edges(task: dict, pool: np.ndarray, scores: np.ndarray, train_pos: np.ndarray):
    method, seed = task["method"], int(task["seed"])
    rows = np.arange(len(pool))
    if method == "UNIFORM":
        return None
    if method == "GRAPH_HARD":
        ids = np.argmax(scores, axis=1)
    elif method == "QTHS25":
        ids, _ = v7.make_ids(pool, scores, train_pos, 0.25, salt="QTHS25")
    elif method == "RANDOM_VETO":
        return base.random_veto(pool, scores, seed)
    elif method == "RANDOM_HARD50":
        order = np.argsort(-scores, axis=1, kind="stable")[:, :10]
        rng = np.random.default_rng(RANDOM_SEED_OFFSET + 10_000 * seed + 501)
        offsets = rng.integers(0, order.shape[1], size=len(pool))
        ids = order[rows, offsets]
    elif method == "SH75":
        order = np.argsort(-scores, axis=1, kind="stable")
        window = order[:, 10:15]
        rng = np.random.default_rng(RANDOM_SEED_OFFSET + 10_000 * seed + 755)
        offsets = rng.integers(0, window.shape[1], size=len(pool))
        ids = window[rows, offsets]
    elif method == "TRIM":
        alpha = float(task["alpha"])
        salt = "QTHS25" if math.isclose(alpha, 0.25) else f"QTHS_SENS_{alpha:.2f}"
        ids, _ = v7.make_ids(pool, scores, train_pos, alpha, salt=salt)
    else:
        raise ValueError(f"Unknown method {method}")
    return pool[rows, ids].copy()


def sampling_microbenchmark(pool: np.ndarray, selected: np.ndarray | None, seed: int) -> float:
    rows = np.arange(len(pool))
    rng = np.random.default_rng(RANDOM_SEED_OFFSET + seed)
    repeats = 60
    started = time.perf_counter()
    for _ in range(repeats):
        if selected is None:
            columns = rng.integers(0, pool.shape[1], size=len(pool))
            _ = pool[rows, columns]
        else:
            _ = selected.copy()
    return (time.perf_counter() - started) / repeats


def metric_for_checkpoint(checkpoint: str, view, positives: np.ndarray, negatives: np.ndarray):
    import torch
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.evaluation.ranking import ranking_metrics
    from dcdlp.train import edge_index_from_graph, score_pairs
    model, _ = load_checkpoint_model(checkpoint, device="cuda")
    params = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
    x = torch.as_tensor(view.features, dtype=torch.float32, device="cuda")
    edge_index = edge_index_from_graph(view.train_graph(), torch.device("cuda"))
    with torch.no_grad():
        pos = score_pairs(model, x, edge_index, positives, batch_size=8192)["logit"]
        neg = score_pairs(model, x, edge_index, negatives.reshape(-1, 2), batch_size=8192)["logit"]
    values = ranking_metrics(pos, neg.reshape(len(positives), negatives.shape[1]))
    result = {key: float(value) for key, value in values.items()}
    del model
    torch.cuda.empty_cache()
    return result, int(params)


def train_worker(task: dict) -> dict:
    worker_init()
    import torch
    original_load = configure_backbone(task["backbone"])
    started_total = time.perf_counter()
    try:
        name = task["dataset"]
        full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash = dataset_context(name)
        selection_start = time.perf_counter()
        selected = selected_edges(task, pool, scores, view.train_pos)
        selection_seconds = time.perf_counter() - selection_start
        per_epoch_sampling_seconds = sampling_microbenchmark(pool, selected, int(task["seed"]))
        engine.candidate_pool = pool
        engine.candidate_pool_hash = pool_hash
        engine.validation_candidate_hash = valid_hash
        suffix = f"_a{float(task['alpha']):.2f}" if task.get("alpha") is not None else ""
        run_method = task["method"] + suffix
        run_rel = Path("HYPERGRAPH_RESEARCH") / "QTHS_V8_PAPER" / "RUNS" / name.upper() / task["backbone"].upper() / run_method / f"seed{task['seed']}"
        if task["stage"] == "efficiency":
            run_rel = Path("HYPERGRAPH_RESEARCH") / "QTHS_V8_PAPER" / "RUNS" / "EFFICIENCY" / name.upper() / task["backbone"].upper() / run_method / f"seed{task['seed']}"
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
        rec = engine.train_one(
            view, run_method, int(task["seed"]), selected, run_rel.as_posix(),
            valid_pos, valid_neg, initialize_from_v6=False, dataset_name=name,
            hypergraph_mode="raw",
        )
        metrics, param_count = metric_for_checkpoint(rec["checkpoint"], view, valid_pos, valid_neg)
        if not math.isclose(metrics["mrr"], float(rec["epoch10_validation_mrr"]), rel_tol=0, abs_tol=1e-9):
            raise RuntimeError(f"Fixed validation recheck differs for {task_key(task)}")
        torch.cuda.synchronize()
        peak_mb = torch.cuda.max_memory_allocated() / (1024 * 1024)
        result = {
            "task": task, "task_key": task_key(task), "state": "COMPLETE",
            "train_record": rec, "validation_metrics": metrics,
            "trainable_parameters": param_count,
            "selection_preprocessing_seconds": selection_seconds,
            "per_epoch_sampling_seconds_microbench": per_epoch_sampling_seconds,
            "peak_gpu_memory_mb": float(peak_mb),
            "total_wall_seconds": time.perf_counter() - started_total,
            "train_pool_hash": pool_hash, "validation_candidate_hash": valid_hash,
            "qths_alpha": 0.25,
        }
        write_json(state_path(task), result)
        return result
    except Exception as exc:
        failed = {"task": task, "task_key": task_key(task), "state": "FAILED",
                  "error": repr(exc), "traceback": traceback.format_exc()}
        write_json(state_path(task), failed)
        raise
    finally:
        v61.load_json = original_load


def test_worker(task: dict) -> dict:
    worker_init()
    configure_backbone("gcn")
    full, view = base.init_dataset(task["dataset"])
    archive_path = OUT / "EVALUATION" / f"{task['dataset']}_test_candidates.npz"
    meta = read_json(OUT / "EVALUATION" / f"{task['dataset']}_test_candidates.json")
    with np.load(archive_path, allow_pickle=False) as archive:
        positives = archive["test_positive"].copy()
        negatives = archive["test_negative_candidates"].copy()
    if v61.array_hash(negatives) != meta["candidate_hash"]:
        raise RuntimeError(f"Test candidate hash mismatch for {task['dataset']}")
    train_stage = "pubmed" if task["dataset"] == "pubmed" and int(task["seed"]) < 3 else "five_seed"
    train_task = {**task, "stage": train_stage}
    job = read_json(state_path(train_task))
    rec = job["train_record"]
    metrics, params = metric_for_checkpoint(rec["checkpoint"], view, positives, negatives)
    result = {
        "task": task, "task_key": task_key(task), "state": "COMPLETE",
        "test_metrics": metrics, "checkpoint": rec["checkpoint"],
        "candidate_hash": meta["candidate_hash"], "trainable_parameters": params,
    }
    test_path = OUT / "state" / "tests" / f"{task_key(task)}.json"
    write_json(test_path, result)
    return result


def make_primary_tasks() -> list[dict]:
    tasks = []
    for method in ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"):
        for seed in SEEDS:
            tasks.append({"stage": "pubmed", "dataset": "pubmed", "backbone": "gcn",
                          "method": method, "seed": seed, "alpha": None})
    for backbone in ("sage", "gat"):
        for method in METHODS:
            for seed in SEEDS:
                tasks.append({"stage": "backbone", "dataset": "cora", "backbone": backbone,
                              "method": method, "seed": seed, "alpha": None})
    for method in ("RANDOM_HARD50", "SH75"):
        for seed in SEEDS:
            tasks.append({"stage": "control", "dataset": "cora", "backbone": "gcn",
                          "method": method, "seed": seed, "alpha": None})
    for alpha in (0.10, 0.40, 0.60):
        tasks.append({"stage": "sensitivity", "dataset": "cora", "backbone": "gcn",
                      "method": "TRIM", "seed": 0, "alpha": alpha})
    for method in METHODS:
        tasks.append({"stage": "efficiency", "dataset": "cora", "backbone": "gcn",
                      "method": method, "seed": 0, "alpha": None})
    return tasks


def run_tasks(tasks: list[dict], phase: str, max_workers: int) -> list[dict]:
    pending, done_records = [], []
    for task in tasks:
        path = state_path(task)
        if path.exists():
            previous = read_json(path)
            if previous.get("state") == "COMPLETE":
                done_records.append(previous)
                continue
        pending.append(task)
    completed_keys = [record["task_key"] for record in done_records]
    update_status(state="RUNNING", phase=phase, total=len(tasks), completed=len(done_records),
                  completed_tasks=completed_keys, failures=[], max_workers=max_workers)
    failures = []
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(max_workers, len(pending)),
                                    mp_context=mp.get_context("spawn"),
                                    initializer=worker_init) as pool:
            futures = {pool.submit(train_worker, task): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    record = future.result()
                    done_records.append(record)
                    completed_keys.append(record["task_key"])
                    active = [task_key(value) for future2, value in futures.items() if not future2.done()]
                    update_status(state="RUNNING", phase=phase, total=len(tasks),
                                  completed=len(done_records), completed_tasks=completed_keys,
                                  active_tasks=active, failures=failures)
                except Exception as exc:
                    failure = {"task": task, "error": repr(exc)}
                    failures.append(failure)
                    update_status(state="RUNNING", phase=phase, total=len(tasks),
                                  completed=len(done_records), completed_tasks=completed_keys,
                                  failures=failures)
    if failures:
        update_status(state="FAILED", phase=phase, failures=failures)
        raise RuntimeError(f"{len(failures)} V8 jobs failed; see status.json and state/jobs")
    return sorted(done_records, key=lambda value: value["task_key"])


def run_test_tasks(tasks: list[dict], phase: str, max_workers: int) -> list[dict]:
    pending, records = [], []
    for task in tasks:
        path = OUT / "state" / "tests" / f"{task_key(task)}.json"
        if path.exists() and read_json(path).get("state") == "COMPLETE":
            records.append(read_json(path))
        else:
            pending.append(task)
    failures = []
    update_status(state="RUNNING", phase=phase, total=len(tasks), completed=len(records), failures=[])
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(max_workers, len(pending)),
                                    mp_context=mp.get_context("spawn"),
                                    initializer=worker_init) as pool:
            futures = {pool.submit(test_worker, task): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    records.append(future.result())
                    update_status(state="RUNNING", phase=phase, total=len(tasks),
                                  completed=len(records), failures=failures)
                except Exception as exc:
                    failures.append({"task": task, "error": repr(exc)})
                    update_status(state="RUNNING", phase=phase, total=len(tasks),
                                  completed=len(records), failures=failures)
    if failures:
        update_status(state="FAILED", phase=phase, failures=failures)
        raise RuntimeError(f"{len(failures)} V8 test-evaluation jobs failed")
    return records


def ensure_test_candidates(dataset: str) -> dict:
    eval_dir = OUT / "EVALUATION"
    eval_dir.mkdir(parents=True, exist_ok=True)
    archive_path = eval_dir / f"{dataset}_test_candidates.npz"
    meta_path = eval_dir / f"{dataset}_test_candidates.json"
    if archive_path.exists() and meta_path.exists():
        return read_json(meta_path)
    if dataset == "cora":
        frozen_path = V71 / "EVALUATION" / "cora_test_candidates.npz"
        frozen_result = read_json(V71 / "results.json")["cora"]["test"]
        with np.load(frozen_path, allow_pickle=False) as archive:
            positives = archive["test_positive"].copy()
            negatives = archive["test_negative_candidates"].copy()
        digest = v61.array_hash(negatives)
        if digest != frozen_result["candidate_hash"]:
            raise RuntimeError("Frozen Cora test candidate cache failed V7.1 hash audit")
        np.savez_compressed(archive_path, test_positive=positives,
                            test_negative_candidates=negatives)
        meta = {"dataset": dataset, "candidate_hash": digest,
                "positive_hash": v61.array_hash(positives),
                "positive_count": int(len(positives)),
                "negative_count_per_positive": int(negatives.shape[1]),
                "created_after_validation_freeze": True,
                "reused_frozen_V7_1_test_candidates": True}
        write_json(meta_path, meta)
        return meta
    full, _ = base.init_dataset(dataset)
    positives, negatives, digest = base.make_eval_candidates(full, "test")
    np.savez_compressed(archive_path, test_positive=positives,
                        test_negative_candidates=negatives)
    meta = {"dataset": dataset, "candidate_hash": digest,
            "positive_hash": v61.array_hash(positives),
            "positive_count": int(len(positives)),
            "negative_count_per_positive": int(negatives.shape[1]),
            "created_after_validation_freeze": True,
            "test_evaluated_once_per_frozen_checkpoint": True}
    write_json(meta_path, meta)
    return meta


def aggregate(records: dict[str, dict], methods: tuple[str, ...], metric_name: str) -> dict:
    result = {}
    for method in methods:
        items = [records[method][str(seed)][metric_name] for seed in sorted(int(s) for s in records[method])]
        values = np.asarray(items, dtype=np.float64)
        result[method] = {"by_seed": items, "mean": float(values.mean()),
                          "sample_std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
                          "n": int(len(values))}
    return result


def bootstrap_mean_ci(values: list[float], n_boot: int = 100_000, seed: int = 20261002) -> list[float]:
    data = np.asarray(values, dtype=np.float64)
    rng = np.random.default_rng(seed)
    draws = rng.choice(data, size=(n_boot, len(data)), replace=True).mean(axis=1)
    return [float(np.quantile(draws, 0.025)), float(np.quantile(draws, 0.975))]


def rankdata(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    order = np.argsort(values, kind="stable")
    result = np.empty(len(values), dtype=np.float64)
    i = 0
    while i < len(values):
        j = i + 1
        while j < len(values) and values[order[j]] == values[order[i]]:
            j += 1
        result[order[i:j]] = (i + j - 1) / 2.0
        i = j
    return result


def spearman(x: list[float], y: list[float]) -> float:
    rx, ry = rankdata(np.asarray(x)), rankdata(np.asarray(y))
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def qths_selected_rank(pool: np.ndarray, scores: np.ndarray, selected: np.ndarray) -> np.ndarray:
    order = np.argsort(scores, axis=1, kind="stable")
    local = np.empty_like(order, dtype=np.float64)
    local[np.arange(len(pool))[:, None], order] = np.arange(pool.shape[1])[None, :] / max(1, pool.shape[1] - 1)
    selected = np.asarray(selected, dtype=np.int64)
    if selected.ndim == 3:
        repetitions = selected.shape[0]
        selected_rows = selected.reshape(-1, 2)
        query_rows = np.tile(np.arange(len(pool)), repetitions)
    elif selected.ndim == 2 and len(selected) == len(pool):
        selected_rows = selected
        query_rows = np.arange(len(pool))
    else:
        raise ValueError(f"Expected (N,2) or (R,N,2) selected edges, got {selected.shape}")
    ranks = np.empty(len(selected_rows), dtype=np.float64)
    for index, row in enumerate(query_rows):
        low = np.minimum(pool[row, :, 0], pool[row, :, 1])
        high = np.maximum(pool[row, :, 0], pool[row, :, 1])
        a, b = sorted((int(selected_rows[index, 0]), int(selected_rows[index, 1])))
        match = np.flatnonzero((low == a) & (high == b))
        if not len(match):
            raise RuntimeError(f"Selected negative not found in row {row}")
        ranks[index] = local[row, int(match[0])]
    return ranks


def summarize_ranks(ranks: np.ndarray) -> dict:
    return {"n": int(len(ranks)), "mean": float(np.mean(ranks)),
            "median": float(np.median(ranks)),
            "p75": float(np.quantile(ranks, 0.75)),
            "p90": float(np.quantile(ranks, 0.90)),
            "p95": float(np.quantile(ranks, 0.95)),
            "p99": float(np.quantile(ranks, 0.99)),
            "max": float(np.max(ranks)),
            "extreme_hard_fraction_ge_0_95": float(np.mean(ranks >= 0.95)),
            "extreme_hard_fraction_ge_0_99": float(np.mean(ranks >= 0.99))}


def sampled_edges_from_v71(method: str) -> np.ndarray:
    blocks = []
    for seed in SEEDS:
        path = V71 / "RUNS" / "CORA" / method / f"seed{seed}" / "negative_samples_by_epoch.npz"
        with np.load(path, allow_pickle=False) as archive:
            blocks.append(archive["negatives"].copy())
    return np.concatenate(blocks, axis=0)


def graph_structural_features(view, edge_pairs: np.ndarray) -> dict:
    from scipy.sparse import csr_matrix
    import torch
    from dcdlp.train import edge_index_from_graph
    graph = view.train_graph()
    edge_index = edge_index_from_graph(graph, torch.device("cpu")).numpy()
    n = int(view.num_nodes)
    adjacency = csr_matrix((np.ones(edge_index.shape[1], dtype=np.float64),
                            (edge_index[0], edge_index[1])), shape=(n, n))
    adjacency = adjacency.maximum(adjacency.T).tocsr()
    adjacency.setdiag(0)
    adjacency.eliminate_zeros()
    degree = np.diff(adjacency.indptr).astype(np.int64)
    edge_pairs = np.asarray(edge_pairs, dtype=np.int64).reshape(-1, 2)
    unique_pairs = np.unique(np.sort(edge_pairs, axis=1), axis=0)
    cn_values, aa_values, ra_values, buckets = [], [], [], {"2": 0, "3": 0, ">3_or_disconnected": 0}
    for u, v in unique_pairs:
        u, v = int(u), int(v)
        nu = adjacency.indices[adjacency.indptr[u]:adjacency.indptr[u + 1]]
        nv = adjacency.indices[adjacency.indptr[v]:adjacency.indptr[v + 1]]
        common = np.intersect1d(nu, nv, assume_unique=True)
        cn_values.append(float(len(common)))
        aa_values.append(float(np.sum(1.0 / np.log(np.maximum(degree[common], 2)))) if len(common) else 0.0)
        ra_values.append(float(np.sum(1.0 / np.maximum(degree[common], 1))) if len(common) else 0.0)
        if len(common):
            buckets["2"] += 1
        else:
            path3 = False
            nv_set = set(int(x) for x in nv)
            for mid in nu:
                nm = adjacency.indices[adjacency.indptr[int(mid)]:adjacency.indptr[int(mid) + 1]]
                if any(int(x) in nv_set for x in nm):
                    path3 = True
                    break
            buckets["3" if path3 else ">3_or_disconnected"] += 1
    endpoints = edge_pairs.reshape(-1)
    endpoint_deg = degree[endpoints]
    freq = np.bincount(endpoints, minlength=n)
    nonzero = freq[freq > 0]
    if len(nonzero) > 1:
        sorted_freq = np.sort(nonzero.astype(np.float64))
        k = len(sorted_freq)
        gini = float((2 * np.dot(np.arange(1, k + 1), sorted_freq) / (k * sorted_freq.sum())) - (k + 1) / k)
    else:
        gini = 0.0
    total = max(1, len(unique_pairs))
    return {
        "unique_selected_pair_count": int(len(unique_pairs)),
        "selected_pair_count_including_repeated_epochs": int(len(edge_pairs)),
        "unique_pair_fraction": float(len(unique_pairs) / max(1, len(edge_pairs))),
        "unique_endpoint_fraction": float(len(np.flatnonzero(freq)) / max(1, len(endpoints))),
        "endpoint_frequency_gini": gini,
        "endpoint_degree": {"mean": float(np.mean(endpoint_deg)), "median": float(np.median(endpoint_deg)),
                             "p75": float(np.quantile(endpoint_deg, .75)),
                             "p90": float(np.quantile(endpoint_deg, .90)),
                             "p95": float(np.quantile(endpoint_deg, .95)),
                             "max": int(np.max(endpoint_deg))},
        "common_neighbors": {"mean": float(np.mean(cn_values)), "p95": float(np.quantile(cn_values, .95)),
                             "fraction_nonzero": float(np.mean(np.asarray(cn_values) > 0))},
        "Adamic_Adar": {"mean": float(np.mean(aa_values)), "p95": float(np.quantile(aa_values, .95))},
        "Resource_Allocation": {"mean": float(np.mean(ra_values)), "p95": float(np.quantile(ra_values, .95))},
        "shortest_path_bucket_counts": buckets,
        "shortest_path_bucket_fractions": {key: float(value / total) for key, value in buckets.items()},
    }


def build_analysis(job_records: list[dict], test_records: list[dict], extras: dict) -> dict:
    v71_results = read_json(V71 / "results.json")
    cora = v71_results["cora"]
    citeseer = v71_results["citeseer"]
    pub_jobs = {item["task"]["method"]: {} for item in job_records if item["task"]["stage"] == "pubmed"}
    for item in job_records:
        task = item["task"]
        if task["stage"] == "pubmed":
            pub_jobs[task["method"]][str(task["seed"])] = item["validation_metrics"]
    pub_test = {}
    for item in test_records:
        task = item["task"]
        if task["dataset"] == "pubmed" and int(task["seed"]) in SEEDS:
            pub_test.setdefault(task["method"], {})[str(task["seed"])] = item["test_metrics"]
    pub_validation_summary = aggregate(pub_jobs, ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"), "mrr")
    pub_test_summary = aggregate(pub_test, ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"), "mrr")
    pub_deltas = [pub_test["QTHS25"][str(seed)]["mrr"] - pub_test["GRAPH_HARD"][str(seed)]["mrr"] for seed in SEEDS]
    pub_wins = sum(value > 0 for value in pub_deltas)
    pub_supported = bool(pub_test_summary["QTHS25"]["mean"] > pub_test_summary["GRAPH_HARD"]["mean"] and pub_wins >= 2)

    cite_deltas = list(citeseer["test"]["paired_mrr_deltas"]["C3_QTHS25_minus_C1_GRAPH_HARD_by_seed"])
    cite_ci = bootstrap_mean_ci(cite_deltas)
    cite_delta_mean = float(np.mean(cite_deltas))
    cite_class = "CITESEER_NEUTRAL" if cite_ci[0] <= 0 <= cite_ci[1] else (
        "CITESEER_SUPPORTED" if cite_ci[0] > 0 else "CITESEER_NEGATIVE")

    backbone_results = {}
    existing_methods = {"UNIFORM": "C0_UNIFORM", "GRAPH_HARD": "C1_GRAPH_HARD", "QTHS25": "C3_QTHS25"}
    v8_backbone_jobs = {}
    for item in job_records:
        task = item["task"]
        if task["stage"] == "backbone":
            v8_backbone_jobs.setdefault(task["backbone"], {}).setdefault(task["method"], {})[str(task["seed"])] = item
    for backbone in ("gcn", "sage", "gat"):
        methods_block = {}
        for method in METHODS:
            if backbone == "gcn":
                old = cora["validation"]["runs"][existing_methods[method]]
                vals = {str(seed): old[str(seed)]["validation_metrics"]["mrr"] for seed in SEEDS}
            else:
                vals = {seed: record["validation_metrics"]["mrr"]
                        for seed, record in v8_backbone_jobs[backbone][method].items()}
            vector = [float(vals[str(seed)]) for seed in SEEDS]
            methods_block[method] = {"by_seed": vector, "mean": float(np.mean(vector)),
                                     "sample_std": float(np.std(vector, ddof=1)), "n": 3}
        differences = [methods_block["QTHS25"]["by_seed"][i] - methods_block["GRAPH_HARD"]["by_seed"][i]
                       for i in range(3)]
        wins = int(sum(value > 0 for value in differences))
        backbone_results[backbone] = {
            "methods": methods_block,
            "QTHS25_minus_GRAPH_HARD_by_seed": differences,
            "paired_mean_delta": float(np.mean(differences)),
            "QTHS25_wins": wins,
            "positive_backbone_gate": bool(methods_block["QTHS25"]["mean"] > methods_block["GRAPH_HARD"]["mean"] and wins >= 2),
        }
    backbone_positive_count = sum(value["positive_backbone_gate"] for value in backbone_results.values())
    backbone_gate = backbone_positive_count >= 2

    controls = {item["task"]["method"]: {} for item in job_records if item["task"]["stage"] == "control"}
    for item in job_records:
        if item["task"]["stage"] == "control":
            controls[item["task"]["method"]][str(item["task"]["seed"])] = item["validation_metrics"]
    qths_cora = cora["validation"]["runs"]["C3_QTHS25"]
    qths_values = [qths_cora[str(seed)]["validation_metrics"]["mrr"] for seed in SEEDS]
    semihard_values = [controls["SH75"][str(seed)]["mrr"] for seed in SEEDS]
    semihard_deltas = [qths_values[i] - semihard_values[i] for i in range(3)]
    semihard_pass = bool(np.mean(qths_values) > np.mean(semihard_values))
    random_hard_values = [controls["RANDOM_HARD50"][str(seed)]["mrr"] for seed in SEEDS]

    sens = {}
    for alpha in (0.0, 0.10, 0.25, 0.40, 0.60):
        label = f"{alpha:.2f}"
        if alpha == 0:
            mrr = cora["validation"]["runs"]["C1_GRAPH_HARD"]["0"]["validation_metrics"]["mrr"]
        elif alpha == 0.25:
            mrr = qths_cora["0"]["validation_metrics"]["mrr"]
        else:
            job = next(item for item in job_records if item["task"]["stage"] == "sensitivity" and math.isclose(item["task"]["alpha"], alpha))
            mrr = job["validation_metrics"]["mrr"]
        sens[label] = {"alpha": alpha, "validation_mrr": float(mrr)}

    context = dataset_context("cora")
    full, view, pool, scores, pool_hash, _, _, _ = context
    sensitivity_ranks = {}
    for alpha in (0.0, 0.10, 0.25, 0.40, 0.60):
        if alpha == 0:
            chosen = pool[np.arange(len(pool)), np.argmax(scores, axis=1)]
        else:
            chosen_ids, _ = v7.make_ids(pool, scores, view.train_pos, alpha,
                                        salt="QTHS25" if alpha == 0.25 else f"QTHS_SENS_{alpha:.2f}")
            chosen = pool[np.arange(len(pool)), chosen_ids]
        ranks = qths_selected_rank(pool, scores, chosen)
        sensitivity_ranks[f"{alpha:.2f}"] = summarize_ranks(ranks)
        sens[f"{alpha:.2f}"].update({
            "effective_runner_up_fraction": float(np.mean(ranks < 1.0)),
            "mean_selected_Rg": float(np.mean(ranks)),
            "p95_selected_Rg": float(np.quantile(ranks, .95)),
            "extreme_hard_fraction": float(np.mean(ranks >= .95)),
        })
    alphas = [sens[f"{alpha:.2f}"]["alpha"] for alpha in (0, .1, .25, .4, .6)]
    mrrs = [sens[f"{alpha:.2f}"]["validation_mrr"] for alpha in (0, .1, .25, .4, .6)]
    mean_rgs = [sens[f"{alpha:.2f}"]["mean_selected_Rg"] for alpha in (0, .1, .25, .4, .6)]

    hardness = {}
    for method, v71_method in (("UNIFORM", "C0_UNIFORM"), ("GRAPH_HARD", "C1_GRAPH_HARD"),
                               ("RANDOM_VETO", "C2_RANDOM_VETO"), ("QTHS25", "C3_QTHS25")):
        edges = sampled_edges_from_v71(v71_method)
        ranks = qths_selected_rank(pool, scores, edges)
        hardness[method] = {"Rg": summarize_ranks(ranks),
                            "graph_structure": graph_structural_features(view, edges)}

    random_hard_summary = {"by_seed": random_hard_values, "mean": float(np.mean(random_hard_values)),
                           "sample_std": float(np.std(random_hard_values, ddof=1))}
    semihard_summary = {"by_seed": semihard_values, "mean": float(np.mean(semihard_values)),
                        "sample_std": float(np.std(semihard_values, ddof=1)),
                        "QTHS25_minus_SH75_by_seed": semihard_deltas,
                        "paired_mean_delta": float(np.mean(semihard_deltas)),
                        "QTHS25_wins": int(sum(value > 0 for value in semihard_deltas)),
                        "state": "QTHS25_ABOVE_SH75" if semihard_pass else "QTHS25_NOT_ABOVE_SH75"}

    eff_jobs = [item for item in job_records if item["task"]["stage"] == "efficiency"]
    eff = {item["task"]["method"]: {
        "train_seconds": item["train_record"]["train_seconds"],
        "wall_seconds": item["train_record"]["wall_seconds"],
        "selection_preprocessing_seconds": item["selection_preprocessing_seconds"],
        "per_epoch_sampling_seconds_microbench": item["per_epoch_sampling_seconds_microbench"],
        "peak_gpu_memory_mb": item["peak_gpu_memory_mb"],
        "trainable_parameters": item["trainable_parameters"],
        "checkpoint": item["train_record"]["checkpoint"],
    } for item in eff_jobs}
    params_match = eff["UNIFORM"]["trainable_parameters"] == eff["GRAPH_HARD"]["trainable_parameters"] == eff["QTHS25"]["trainable_parameters"]
    test_index = {(x["task"]["dataset"], x["task"]["method"], str(x["task"]["seed"])): x for x in test_records}
    pub_test_table = {method: {str(seed): test_index[("pubmed", method, str(seed))]["test_metrics"] for seed in SEEDS}
                      for method in ("GRAPH_HARD", "RANDOM_VETO", "QTHS25")}
    pub_deltas = [pub_test_table["QTHS25"][str(seed)]["mrr"] - pub_test_table["GRAPH_HARD"][str(seed)]["mrr"] for seed in SEEDS]
    result = {
        "protocol": {"method": "QTHS25", "trim_ratio": 0.25, "prepool_size": 2,
                     "protocol": "STRICT_TRAIN_ONLY", "checkpoint": "fixed epoch 10",
                     "seeds": list(SEEDS), "epochs": 10,
                     "backbones": ["gcn", "sage", "gat"],
                     "GAT": "PyG GATConv, one head, concat=False; experiment-local encoder option",
                     "control_random_hard50": "uniformly sample among teacher top 50% of the 20-item train candidate pool",
                     "control_SH75": "uniformly sample within teacher hardness rank window [50%,75%] of the 20-item pool",
                     "QTHS25_rule_note": "Frozen V7.1 implementation uses a per-positive top-2 prepool; alpha is the fraction of the 2N prepool candidate occurrences trimmed by a stable positive-key hash, with the hardest candidate replaced by rank-2 for selected positives. At alpha=0.25 this selects the runner-up for 50% of positives. Sensitivity ratios above 0.50 saturate at all positives because only N positive rows are available."},
        "pubmed": {"validation": pub_validation_summary,
                   "test": aggregate(pub_test_table, ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"), "mrr"),
                   "QTHS25_minus_GRAPH_HARD_test_by_seed": pub_deltas,
                   "QTHS25_minus_GRAPH_HARD_test_mean_delta": float(np.mean(pub_deltas)),
                   "QTHS25_wins_vs_GRAPH_HARD": int(sum(value > 0 for value in pub_deltas)),
                   "PUBMED_SUPPORTED": pub_supported,
                   "test_candidate_hash": read_json(OUT / "EVALUATION" / "pubmed_test_candidates.json")["candidate_hash"],
                   "test_evaluated_once_after_validation_freeze": True},
        "citeseer": {"test_by_seed_QTHS25_minus_GRAPH_HARD": cite_deltas,
                     "paired_mean_delta": cite_delta_mean, "bootstrap_ci95_percentile": cite_ci,
                     "bootstrap_replicates": 100_000, "bootstrap_seed": 20261002,
                     "classification": cite_class,
                     "interpretation": "CI crossing zero indicates noise-level/neutral under the pre-registered rule."},
        "backbone_generalization": {"by_backbone": backbone_results,
                                    "positive_backbone_count": int(backbone_positive_count),
                                    "BACKBONE_GENERALIZATION": "YES" if backbone_gate else "NO",
                                    "rule": "at least 2/3 backbones have QTHS25 mean above Graph-hard and at least 2/3 paired seed wins"},
        "random_hard_control": random_hard_summary,
        "semi_hard_control": semihard_summary,
        "trim_sensitivity": {"by_alpha": sens, "spearman_alpha_vs_validation_mrr": spearman(alphas, mrrs),
                             "spearman_mean_Rg_vs_validation_mrr": spearman(mean_rgs, mrrs),
                             "alpha_order": alphas, "validation_mrr_order": mrrs,
                             "mean_selected_Rg_order": mean_rgs,
                             "R_g_definition": "within each positive's 20-item frozen graph-teacher candidate pool, score percentile in [0,1], with 1 the hardest candidate"},
        "hardness_tail_characterization": {"R_g_definition": "within-positive teacher-score percentile among 20 candidates; 1 is hardest",
                                           "methods": hardness},
        "efficiency": {"Cora_GCN_seed0": eff, "parameter_counts_match_across_sampling_arms": bool(params_match),
                       "additional_trainable_parameters_for_QTHS": 0,
                       "teacher_scoring": extras.get("teacher_scoring", {}),
                       "resource_profile": extras.get("resource_profile", {})},
        "five_seed_gate": extras.get("five_seed_gate", {}),
        "cross_dataset_backbone_transfer": extras.get("cross_dataset_backbone_transfer", {}),
        "novelty_status": "EXACT_RULE_UNVERIFIED",
        "novelty_search_scope": "Focused search covered quantile/truncated graph link-prediction negatives, rank-window and semi-hard methods, dynamic/adversarial sampling, and adjacent hyperedge prediction; no exact-rule source was confirmed. No priority claim.",
        "source_code_sha256": sha256_file(Path(__file__)),
    }
    return result


def make_pubmed_report(result: dict) -> str:
    block = result["pubmed"]
    lines = ["# PubMed validation and test", "",
             "Frozen QTHS25; STRICT_TRAIN_ONLY; fixed epoch 10; Graph-hard, Random-veto and QTHS25 share the same split, candidate pool and evaluation candidates.", "",
             "## Validation MRR", "", "| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |", "|---|---:|---:|---:|---:|"]
    for method in ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"):
        row = block["validation"][method]
        vals = row["by_seed"]
        lines.append(f"| {method} | {vals[0]:.6f} | {vals[1]:.6f} | {vals[2]:.6f} | {row['mean']:.6f} ± {row['sample_std']:.6f} |")
    lines += ["", "## Test MRR", "", "| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |", "|---|---:|---:|---:|---:|"]
    for method in ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"):
        row = block["test"][method]
        vals = row["by_seed"]
        lines.append(f"| {method} | {vals[0]:.6f} | {vals[1]:.6f} | {vals[2]:.6f} | {row['mean']:.6f} ± {row['sample_std']:.6f} |")
    lines += ["", f"- QTHS25 − Graph-hard paired test deltas: {block['QTHS25_minus_GRAPH_HARD_test_by_seed']}",
              f"- QTHS25 mean test delta: {block['QTHS25_minus_GRAPH_HARD_test_mean_delta']:+.6f}; wins: {block['QTHS25_wins_vs_GRAPH_HARD']}/3.",
              f"- PUBMED_SUPPORTED: **{'YES' if block['PUBMED_SUPPORTED'] else 'NO'}** (requires mean test MRR above Graph-hard and at least 2/3 seed wins).",
              f"- Shared test candidate hash: {block['test_candidate_hash']}.", ""]
    return "\n".join(lines)


def write_reports(result: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "01_PUBMED.md").write_text(make_pubmed_report(result), encoding="utf-8")
    cora = read_json(V71 / "results.json")["cora"]
    cite = result["citeseer"]
    cite_class = cite["classification"]
    cite_ci = cite["bootstrap_ci95_percentile"]
    cite_delta_mean = cite["paired_mean_delta"]
    cite_lines = ["# Citeseer paired test statistics", "",
                  "The 3 existing seed pairs are reused without retraining or changing Citeseer parameters.", "",
                  "| Seed | QTHS25 − Graph-hard MRR |", "|---:|---:|"]
    cite_lines += [f"| {i} | {value:+.6f} |" for i, value in enumerate(cite["test_by_seed_QTHS25_minus_GRAPH_HARD"])]
    cite_lines += ["", f"- Paired mean delta: **{cite['paired_mean_delta']:+.6f}**.",
                   f"- 95% paired bootstrap percentile CI: **[{cite['bootstrap_ci95_percentile'][0]:+.6f}, {cite['bootstrap_ci95_percentile'][1]:+.6f}]** over 100,000 resamples of the three seed-level deltas.",
                   f"- Classification: **{cite['classification']}**.", ""]
    (OUT / "02_CITESEER_STATISTICS.md").write_text("\n".join(cite_lines), encoding="utf-8")

    bb = result["backbone_generalization"]
    lines = ["# Cora backbone generalization", "", "All runs use the same Cora split, frozen graph-teacher 20-candidate pool, raw-star hypergraph mode, decoder, optimizer settings, negative count, 10 epochs and seed list. The only model change is the graph encoder backbone. GCN rows reuse V7.1 checkpoints; SAGE and GAT are new V8 runs.", "",
             "| Backbone | Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD | QTHS−Graph-hard paired mean | Wins/3 |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for backbone, block in bb["by_backbone"].items():
        for method in METHODS:
            row = block["methods"][method]
            delta = block["paired_mean_delta"] if method == "QTHS25" else None
            wins = block["QTHS25_wins"] if method == "QTHS25" else None
            lines.append(f"| {backbone.upper()} | {method} | {row['by_seed'][0]:.6f} | {row['by_seed'][1]:.6f} | {row['by_seed'][2]:.6f} | {row['mean']:.6f} ± {row['sample_std']:.6f} | {'' if delta is None else f'{delta:+.6f}'} | {'' if wins is None else f'{wins}/3'} |")
    lines += ["", f"- Positive backbones passing both mean and paired-win gates: {bb['positive_backbone_count']}/3.",
              f"- BACKBONE_GENERALIZATION: **{bb['BACKBONE_GENERALIZATION']}**.", ""]
    (OUT / "03_BACKBONE_GENERALIZATION.md").write_text("\n".join(lines), encoding="utf-8")

    sens = result["trim_sensitivity"]
    sens_lines = ["# QTHS trim sensitivity", "",
                  "Cora seed 0 validation only. This is a sensitivity analysis, not a model-selection step; QTHS25 remains frozen as the main rule. Because the frozen V7.1 rule trims from a two-candidate prepool, alpha counts candidate occurrences (2N); effective replaced-positive fractions are capped at 100%.", "",
                  "| Nominal trim ratio | Effective runner-up fraction | Validation MRR | Mean selected Rg | p95 Rg | Extreme-hard fraction |", "|---:|---:|---:|---:|---:|---:|"]
    for alpha in (0, .1, .25, .4, .6):
        row = sens["by_alpha"][f"{alpha:.2f}"]
        sens_lines.append(f"| {alpha:.0%} | {row['effective_runner_up_fraction']:.3f} | {row['validation_mrr']:.6f} | {row['mean_selected_Rg']:.6f} | {row['p95_selected_Rg']:.6f} | {row['extreme_hard_fraction']:.4f} |")
    sens_lines += ["", f"- Spearman(alpha, validation MRR): {sens['spearman_alpha_vs_validation_mrr']:.4f}.",
                   f"- Spearman(mean selected Rg, validation MRR): {sens['spearman_mean_Rg_vs_validation_mrr']:.4f}.",
                   "- Correlations are descriptive associations over five settings, not causal estimates.", ""]
    (OUT / "04_TRIM_SENSITIVITY.md").write_text("\n".join(sens_lines), encoding="utf-8")

    semi = result["semi_hard_control"]
    semilines = ["# Matched semi-hard and random-hard controls", "",
                 "SH75 samples uniformly from each positive's graph-teacher hardness ranks [50%,75%] within the shared 20-item train pool. RANDOM_HARD50 samples uniformly from the top 50% of the same pool. All runs are Cora, GCN, STRICT_TRAIN_ONLY, fixed epoch 10, 3 seeds.", "",
                 "| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |", "|---|---:|---:|---:|---:|"]
    for method, values, summary in (("SH75", semi["by_seed"], semi),
                                    ("QTHS25", result["backbone_generalization"]["by_backbone"]["gcn"]["methods"]["QTHS25"]["by_seed"], result["backbone_generalization"]["by_backbone"]["gcn"]["methods"]["QTHS25"]),
                                    ("RANDOM_HARD50", result["random_hard_control"]["by_seed"], result["random_hard_control"])):
        semilines.append(f"| {method} | {values[0]:.6f} | {values[1]:.6f} | {values[2]:.6f} | {summary['mean']:.6f} ± {summary['sample_std']:.6f} |")
    semilines += ["", f"- QTHS25 − SH75 paired deltas: {semi['QTHS25_minus_SH75_by_seed']}.",
                  f"- Paired mean delta: {semi['paired_mean_delta']:+.6f}; QTHS25 wins {semi['QTHS25_wins']}/3.",
                  f"- Gate: **{semi['state']}**.", ""]
    (OUT / "05_SEMIHARD_CONTROL.md").write_text("\n".join(semilines), encoding="utf-8")

    eff = result["efficiency"]
    params_match = eff["parameter_counts_match_across_sampling_arms"]
    eff_lines = ["# Efficiency and parameter overhead", "", "Cora GCN seed 0; same fixed 10-epoch training budget. Wall time is a single measured run per method; it is descriptive and hardware-specific.", "",
                 "| Method | Train seconds | Wall seconds | Selection preprocessing s | Sampling microbenchmark s/epoch | Peak CUDA allocated MiB | Trainable parameters |", "|---|---:|---:|---:|---:|---:|---:|"]
    for method in ("UNIFORM", "GRAPH_HARD", "QTHS25"):
        row = eff["Cora_GCN_seed0"][method]
        eff_lines.append(f"| {method} | {row['train_seconds']:.3f} | {row['wall_seconds']:.3f} | {row['selection_preprocessing_seconds']:.6f} | {row['per_epoch_sampling_seconds_microbench']:.6f} | {row['peak_gpu_memory_mb']:.1f} | {row['trainable_parameters']} |")
    eff_lines += ["", f"- Additional trainable parameters for QTHS: **{eff['additional_trainable_parameters_for_QTHS']}**.",
                  f"- Parameter-count equality across sampling arms: **{eff['parameter_counts_match_across_sampling_arms']}**.",
                  f"- Frozen graph-teacher candidate scoring time: {eff['teacher_scoring']}.",
                  f"- Compute profile: {eff['resource_profile']}.", ""]
    (OUT / "06_EFFICIENCY.md").write_text("\n".join(eff_lines), encoding="utf-8")

    novelty_lines = ["# Focused novelty check", "",
                     "Search scope: quantile/truncated graph-link-prediction negatives; rank-window and semi-hard sampling; dynamic/adversarial sampling; adjacent hyperedge prediction. This focused check did not confirm an exact implementation of the frozen V7.1 QTHS rule. It is not an exhaustive priority review.", "",
                     "| Work | Relevant overlap | Distinction / status |", "|---|---|---|"]
    novelty_lines += [
        "| ProGCL (ICML 2022) | Hardest graph negatives can be unreliable in graph contrastive learning. | Reliability-aware graph contrastive setting, not this supervised LP fixed top-2 teacher-rank trim. |",
        "| DMNS (TheWebConf 2024) | Dynamic/difficulty-controlled negative generation for graph link prediction. | Diffusion-based generation and hardness levels; not the frozen 20-item teacher pool plus fixed top-2 trimming. |",
        "| MeBNS (2023 preprint) | Teacher/student adaptation and hard-negative handling for link prediction. | Meta-learning/reweighting formulation differs from the fixed QTHS25 rank rule. |",
        "| Hard Negative Sampling in Hyperedge Prediction (2025 preprint) | Direct hard-negative sampling in higher-order prediction. | Hyperedge prediction and synthesized candidates, rather than pairwise graph LP with QTHS. |",
        "| HeaRT (NeurIPS 2023) | Hard negatives for link-prediction evaluation. | Evaluation candidate benchmark, not train-time negative selection. |",
        "", "**NOVELTY_STATUS: EXACT_RULE_UNVERIFIED.** Do not claim QTHS is first; compare its exact top-2, per-positive, graph-teacher, stable-hash semantics against any closer paper during manuscript preparation."
    ]
    (OUT / "07_NOVELTY.md").write_text("\n".join(novelty_lines) + "\n", encoding="utf-8")

    matrix = ["# Paper evidence matrix", "",
              "| Claim | Required evidence | Current status | File | Ready? |", "|---|---|---|---|---|"]
    pub_status = "SUPPORTED" if result["pubmed"]["PUBMED_SUPPORTED"] else "NOT_SUPPORTED"
    matrix_rows = [
        ("QTHS > Graph-hard on Cora", "Frozen Cora test; paired seeds", "PASS" if cora["locked_reproduction_status"] == "PASS" else "FAIL", "01_CORA_FULL_RESULTS.md / V7.1", "YES"),
        ("QTHS generalizes to PubMed", "3-seed test mean and wins/3", pub_status, "01_PUBMED.md", "YES"),
        ("Citeseer behavior", "paired seed deltas and 95% bootstrap CI", f"{cite_class}: CI [{cite_ci[0]:+.4f},{cite_ci[1]:+.4f}]", "02_CITESEER_STATISTICS.md", "YES"),
        ("QTHS > random veto", "Cora frozen test paired comparison", "PASS" if cora["test"]["locked_gate_details"]["QTHS25_beats_random_veto_mean_or_ties"] else "FAIL", "01_CORA_FULL_RESULTS.md / V7.1", "YES"),
        ("QTHS > semi-hard", "Cora SH75, 3 seed paired validation", semi["state"], "05_SEMIHARD_CONTROL.md", "YES"),
        ("Backbone generalization", "3 encoders; 2/3 positive with 2/3 seed wins", bb["BACKBONE_GENERALIZATION"], "03_BACKBONE_GENERALIZATION.md", "YES"),
        ("Zero parameter overhead", "same backbone parameter-count audit", "PASS" if params_match else "FAIL", "06_EFFICIENCY.md", "YES"),
        ("Runtime overhead", "selection/scoring/training timing and GPU memory", "MEASURED", "06_EFFICIENCY.md", "YES"),
        ("Trim sensitivity", "Cora seed0 five ratios and association", "MEASURED", "04_TRIM_SENSITIVITY.md", "YES"),
        ("Novelty status", "focused primary-source overlap check", result["novelty_status"], "07_NOVELTY.md", "PARTIAL"),
    ]
    for row in matrix_rows:
        matrix.append("| " + " | ".join(str(value) for value in row) + " |")
    (OUT / "PAPER_EVIDENCE_MATRIX.md").write_text("\n".join(matrix) + "\n", encoding="utf-8")

    any_two = result["backbone_generalization"]["BACKBONE_GENERALIZATION"] == "YES"
    cite_acceptable = cite_class == "CITESEER_NEUTRAL" or (cite_class == "CITESEER_NEGATIVE" and abs(cite_delta_mean) <= 0.01)
    paperize = bool(cora["locked_reproduction_status"] == "PASS" and pub_status == "SUPPORTED" and cite_acceptable and any_two)
    if paperize:
        decision = "PAPERIZE_QTHS"
    elif not result["pubmed"]["PUBMED_SUPPORTED"] and not any_two:
        decision = "QTHS_GENERALIZATION_TOO_WEAK"
    else:
        decision = "QTHS_NEEDS_MORE_BENCHMARKS"
    result["PAPER_EVIDENCE_READY"] = "YES" if paperize else "PARTIAL"
    result["FINAL_DECISION"] = decision
    result["NEXT_EXPECTED_STEP"] = "paper outline, tables, figures, related work, and writing" if paperize else "targeted additional benchmark work based on the failed gates"
    final = ["# V8 final report", "", f"- STATUS: **COMPLETE**",
             f"- QTHS: **QTHS25 frozen; alpha=0.25**",
             f"- CORA: V7.1 locked reproduction **{cora['locked_reproduction_status']}**; test QTHS25 mean {cora['test']['summary']['methods']['C3_QTHS25']['mean_mrr']:.6f} vs Graph-hard {cora['test']['summary']['methods']['C1_GRAPH_HARD']['mean_mrr']:.6f}.",
             f"- CITESEER: **{cite_class}**, paired mean delta {cite_delta_mean:+.6f}, 95% bootstrap CI [{cite_ci[0]:+.6f}, {cite_ci[1]:+.6f}].",
             f"- PUBMED: **{'SUPPORTED' if result['pubmed']['PUBMED_SUPPORTED'] else 'NOT_SUPPORTED'}**, test paired mean delta {result['pubmed']['QTHS25_minus_GRAPH_HARD_test_mean_delta']:+.6f}, wins {result['pubmed']['QTHS25_wins_vs_GRAPH_HARD']}/3.",
             f"- BACKBONE_GENERALIZATION: **{bb['BACKBONE_GENERALIZATION']}** ({bb['positive_backbone_count']}/3 pass).",
             f"- SEMI_HARD_CONTROL: **{semi['state']}**, delta {semi['paired_mean_delta']:+.6f}, wins {semi['QTHS25_wins']}/3.",
             f"- TRIM_SENSITIVITY: Spearman(alpha, MRR)={sens['spearman_alpha_vs_validation_mrr']:.4f}; Spearman(mean Rg, MRR)={sens['spearman_mean_Rg_vs_validation_mrr']:.4f}.",
             f"- EFFICIENCY: QTHS additional trainable parameters **0**; sampling, scoring, wall time and GPU memory recorded.",
             f"- NOVELTY_STATUS: **{result['novelty_status']}**.",
             f"- PAPER_EVIDENCE_READY: **{result['PAPER_EVIDENCE_READY']}**.",
             f"- FINAL_DECISION: **{decision}**.", f"- NEXT_EXPECTED_STEP: {result['NEXT_EXPECTED_STEP']}", ""]
    (OUT / "FINAL_REPORT.md").write_text("\n".join(final), encoding="utf-8")
    write_json(OUT / "results.json", result)


def preflight() -> dict:
    info = base.ensure_expected_runtime()
    v71_results = read_json(V71 / "results.json")
    if v71_results.get("QTHS_LOCKED_REPRODUCTION") != "PASS":
        raise RuntimeError("Frozen V7.1 QTHS reproduction is not PASS")
    worker_init()
    patch_gat_encoder()
    import torch
    from dcdlp.models.dcdlp import NodeEncoder
    encoder = NodeEncoder(8, hidden_dim=16, num_layers=2, dropout=0.0, backbone="gat").cuda()
    x = torch.randn(6, 8, device="cuda")
    edge_index = torch.tensor([[0, 1, 2, 3, 4], [1, 2, 3, 4, 0]], dtype=torch.long, device="cuda")
    with torch.no_grad():
        output = encoder(x, edge_index)
    if tuple(output.shape) != (6, 16) or not torch.isfinite(output).all():
        raise RuntimeError("Experiment-local GAT encoder smoke test failed")
    meta = read_json(V61 / "strict_pool_metadata.json")
    if not (V61 / "strict_train_candidates_and_selections.npz").exists():
        raise RuntimeError("Frozen Cora train-only pool missing")
    data_audit = {}
    for name in ("cora", "citeseer", "pubmed"):
        _, view, pool, scores, pool_hash, _, _, valid_hash = dataset_context(name)
        data_audit[name] = {"train_pool_hash": pool_hash,
                            "candidate_shape": list(pool.shape),
                            "teacher_scores_shape": list(scores.shape),
                            "validation_candidate_hash": valid_hash,
                            "train_positive_count": int(len(view.train_pos))}
    info.update({"V7_1_reproduction": "PASS", "Cora_pool_hash": meta["candidate_pool_hash"],
                 "GAT_smoke": "PASS", "data_audit": data_audit,
                 "cpu_count": os.cpu_count(), "max_workers": int(os.getenv("QTHS_V8_WORKERS", "6"))})
    write_json(OUT / "preflight.json", info)
    return info


def measure_teacher_scoring() -> dict:
    import torch
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs
    full, view, pool, cached, _, _, _, _ = dataset_context("cora")
    metadata = read_json(V61 / "strict_pool_metadata.json")
    checkpoint = Path(metadata["teacher_records"]["Graph"]["checkpoint"])
    if not checkpoint.exists():
        relocated = V61 / "TEACHERS" / "Graph" / "checkpoints" / checkpoint.name
        if not relocated.exists():
            raise FileNotFoundError(
                f"Teacher checkpoint unavailable at persisted path {checkpoint} or relocated path {relocated}"
            )
        checkpoint = relocated
    model, _ = load_checkpoint_model(checkpoint, device="cuda")
    x = torch.as_tensor(view.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(view.train_graph(), torch.device("cuda"))
    torch.cuda.synchronize()
    start = time.perf_counter()
    with torch.no_grad():
        result = score_pairs(model, x, edges, pool.reshape(-1, 2), batch_size=8192)["logit"]
    torch.cuda.synchronize()
    seconds = time.perf_counter() - start
    if hasattr(result, "detach"):
        scores = result.detach().cpu().numpy().reshape(pool.shape[:2])
    else:
        scores = np.asarray(result).reshape(pool.shape[:2])
    cached_array = np.asarray(cached)
    digest = v61.array_hash(scores)
    cached_hash = v61.array_hash(cached_array)
    absolute_diff = np.abs(scores.astype(np.float64) - cached_array.astype(np.float64))
    allclose = bool(np.allclose(scores, cached_array, rtol=1e-5, atol=1e-6))
    del model
    torch.cuda.empty_cache()
    return {"dataset": "Cora", "candidate_pairs": int(pool.shape[0] * pool.shape[1]),
            "wall_seconds": float(seconds), "score_hash_matches_frozen_cache": digest == cached_hash,
            "score_allclose_to_frozen_cache": allclose,
            "allclose_rtol": 1e-5, "allclose_atol": 1e-6,
            "max_abs_difference": float(absolute_diff.max()),
            "mean_abs_difference": float(absolute_diff.mean()),
            "scores_hash": digest, "cached_scores_hash": cached_hash}


def make_extended_tasks(pubmed_supported: bool) -> list[dict]:
    tasks = []
    for method in ("GRAPH_HARD", "QTHS25"):
        for seed in EXTENDED_SEEDS:
            tasks.append({"stage": "five_seed", "dataset": "cora", "backbone": "gcn",
                          "method": method, "seed": seed, "alpha": None})
            if pubmed_supported:
                tasks.append({"stage": "five_seed", "dataset": "pubmed", "backbone": "gcn",
                              "method": method, "seed": seed, "alpha": None})
    return tasks


def preexisting_test_metric(dataset: str, method: str, seed: int) -> dict:
    results = read_json(V71 / "results.json")
    key = {"GRAPH_HARD": "C1_GRAPH_HARD", "QTHS25": "C3_QTHS25"}[method]
    return results["cora"]["test"]["by_method_seed"][key][str(seed)]


def five_seed_summary(ext_records: list[dict], ext_tests: list[dict], main_pubmed_tests: list[dict], pubmed_supported: bool) -> dict:
    tests = {(item["task"]["dataset"], item["task"]["method"], int(item["task"]["seed"])): item for item in ext_tests}
    main_tests = {(item["task"]["dataset"], item["task"]["method"], int(item["task"]["seed"])): item for item in main_pubmed_tests}
    result = {}
    datasets = ["cora"] + (["pubmed"] if pubmed_supported else [])
    for dataset in datasets:
        by_method = {}
        for method in ("GRAPH_HARD", "QTHS25"):
            vals = []
            for seed in range(5):
                if seed < 3:
                    if dataset == "cora":
                        old = preexisting_test_metric(dataset, method, seed)
                        vals.append(float(old["mrr"]))
                    else:
                        vals.append(float(main_tests[(dataset, method, seed)]["test_metrics"]["mrr"]))
                else:
                    vals.append(float(tests[(dataset, method, seed)]["test_metrics"]["mrr"]))
            by_method[method] = {"by_seed": vals, "mean": float(np.mean(vals)),
                                 "sample_std": float(np.std(vals, ddof=1))}
        deltas = [by_method["QTHS25"]["by_seed"][i] - by_method["GRAPH_HARD"]["by_seed"][i] for i in range(5)]
        result[dataset] = {"test": by_method, "QTHS25_minus_GRAPH_HARD_by_seed": deltas,
                           "paired_mean_delta": float(np.mean(deltas)),
                           "QTHS25_wins": int(sum(value > 0 for value in deltas))}
    return result


def transfer_summary(records: list[dict]) -> dict:
    data = {item["task"]["method"]: item["validation_metrics"]["mrr"] for item in records
            if item["task"]["stage"] == "transfer"}
    return {"dataset": "citeseer", "backbone": "sage", "seed": 0,
            "GRAPH_HARD": data["GRAPH_HARD"], "QTHS25": data["QTHS25"],
            "paired_delta": float(data["QTHS25"] - data["GRAPH_HARD"]),
            "purpose": "single-seed backbone transfer check beyond Cora; validation only"}


def run_all(max_workers: int) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    info = preflight()
    update_status(state="RUNNING", phase="preflight_passed", error=None,
                  experiment="V8 QTHS Paperization & Backbone Generalization",
                  resource_profile={"gpu": info.get("gpu"), "cpu_count": os.cpu_count(), "workers": max_workers})
    primary_tasks = make_primary_tasks()
    primary_records = run_tasks(primary_tasks, "primary_validation", max_workers)
    update_status(state="RUNNING", phase="pubmed_validation_frozen", validation_tasks_complete=len(primary_tasks))
    pub_jobs = [x for x in primary_records if x["task"]["stage"] == "pubmed"]
    pub_val = {method: {} for method in ("GRAPH_HARD", "RANDOM_VETO", "QTHS25")}
    for item in pub_jobs:
        pub_val[item["task"]["method"]][str(item["task"]["seed"])] = {"mrr": item["validation_metrics"]["mrr"]}
    pub_val_summary = aggregate(pub_val, ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"), "mrr")
    test_meta = ensure_test_candidates("pubmed")
    pub_test_tasks = [{"stage": "test", "dataset": "pubmed", "backbone": "gcn",
                       "method": method, "seed": seed, "alpha": None}
                      for method in ("GRAPH_HARD", "RANDOM_VETO", "QTHS25") for seed in SEEDS]
    pub_test_records = run_test_tasks(pub_test_tasks, "pubmed_test_evaluation", max_workers)
    pub_test_vals = {method: {} for method in ("GRAPH_HARD", "RANDOM_VETO", "QTHS25")}
    for item in pub_test_records:
        task = item["task"]
        pub_test_vals[task["method"]][str(task["seed"])] = {"mrr": item["test_metrics"]["mrr"]}
    pub_test_summary = aggregate(pub_test_vals, ("GRAPH_HARD", "RANDOM_VETO", "QTHS25"), "mrr")
    pub_deltas = [pub_test_vals["QTHS25"][str(seed)]["mrr"] - pub_test_vals["GRAPH_HARD"][str(seed)]["mrr"] for seed in SEEDS]
    pub_supported = bool(pub_test_summary["QTHS25"]["mean"] > pub_test_summary["GRAPH_HARD"]["mean"] and sum(value > 0 for value in pub_deltas) >= 2)
    write_json(OUT / "state" / "pubmed_gate.json", {"validation": pub_val_summary, "test": pub_test_summary,
               "test_deltas": pub_deltas, "supported": pub_supported, "candidate_hash": test_meta["candidate_hash"]})

    transfer_tasks = [{"stage": "transfer", "dataset": "citeseer", "backbone": "sage",
                       "method": method, "seed": 0, "alpha": None} for method in ("GRAPH_HARD", "QTHS25")]
    transfer_records = run_tasks(transfer_tasks, "citeseer_sage_transfer", max_workers)

    extended_tasks = make_extended_tasks(pub_supported)
    extended_records = run_tasks(extended_tasks, "five_seed_extension", max_workers)
    ensure_test_candidates("cora")
    five_test_tasks = [{"stage": "test", "dataset": task["dataset"], "backbone": "gcn",
                        "method": task["method"], "seed": task["seed"], "alpha": None}
                       for task in extended_tasks]
    five_tests = run_test_tasks(five_test_tasks, "five_seed_test_evaluation", max_workers) if five_test_tasks else []

    cite = read_json(V71 / "results.json")["citeseer"]
    cite_deltas = list(cite["test"]["paired_mrr_deltas"]["C3_QTHS25_minus_C1_GRAPH_HARD_by_seed"])
    cite_ci = bootstrap_mean_ci(cite_deltas)
    cite_class = "CITESEER_NEUTRAL" if cite_ci[0] <= 0 <= cite_ci[1] else ("CITESEER_SUPPORTED" if cite_ci[0] > 0 else "CITESEER_NEGATIVE")
    transfer = transfer_summary(transfer_records)
    five_seed = five_seed_summary(extended_records, five_tests, pub_test_records, pub_supported)
    teacher_scoring = measure_teacher_scoring()
    result = build_analysis(primary_records + transfer_records + extended_records,
                            pub_test_records + five_tests,
                            {"teacher_scoring": teacher_scoring,
                             "resource_profile": {"gpu": info["gpu"], "cuda_build": info["torch_cuda_build"],
                                                  "cpu_count": os.cpu_count(), "max_workers": max_workers},
                             "five_seed_gate": five_seed,
                             "cross_dataset_backbone_transfer": transfer})
    # Carry the precomputed CI used for the classification to keep the value stable.
    result["citeseer"]["bootstrap_ci95_percentile"] = cite_ci
    result["citeseer"]["classification"] = cite_class
    write_reports(result)
    update_status(state="COMPLETE", phase="complete", current=None, error=None,
                  final_decision=result["FINAL_DECISION"], pubmed_supported=pub_supported,
                  backbone_generalization=result["backbone_generalization"]["BACKBONE_GENERALIZATION"],
                  test_evaluated=True, source_code_sha256=result["source_code_sha256"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--pilot", action="store_true", help="run one scheduled Cora GAT/QTHS25 seed-0 job as a pipeline smoke test")
    parser.add_argument("--workers", type=int, default=int(os.getenv("QTHS_V8_WORKERS", "6")))
    args = parser.parse_args()
    if args.workers < 1 or args.workers > 8:
        raise SystemExit("workers must be between 1 and 8 for the single V100")
    if args.preflight_only:
        print(json.dumps(preflight(), indent=2, ensure_ascii=False))
    elif args.pilot:
        preflight()
        task = {"stage": "backbone", "dataset": "cora", "backbone": "gat",
                "method": "QTHS25", "seed": 0, "alpha": None}
        print(json.dumps(train_worker(task), indent=2, ensure_ascii=False))
    else:
        run_all(args.workers)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        try:
            update_status(state="FAILED", phase="failed", current=None,
                          error=repr(exc), traceback=traceback.format_exc())
        except Exception:
            pass
        raise
