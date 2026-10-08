from __future__ import annotations

import hashlib
import json
import math
import os
import resource
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve()
OUT = HERE.parents[1]
ROOT = Path(os.environ.get("NHMC_RUNTIME_ROOT", HERE.parents[4] / "HMC_V15" / "runtime")).resolve()
V71 = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V7_1"
V61 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
sys.path[:0] = [str(ROOT / "src"), str(V71), str(V61),
                str(ROOT / "HYPERGRAPH_RESEARCH" / "CODNS_V6_2"),
                str(ROOT / "HYPERGRAPH_RESEARCH" / "HARDNESS_V7")]

import experiment_v71 as base  # noqa: E402
import run_negative_v6_1 as v61  # noqa: E402

FOLDS_SEED = 20261003
MATCH_SEED = 20261016
SHUFFLE_SEED = 20261017
AUDIT_SEED = 20261018
POOL_PER_POSITIVE = 20
MATCH_PER_POSITIVE = 3
TOKEN_DTYPE = np.dtype([
    ("pair", "<i4"), ("stratum", "<u2"), ("size", "<f4", (3,)), ("overlap", "<f4", (3,)),
], align=False)
_CTX: dict | None = None
_OFFSETS: np.ndarray | None = None
_TOKEN_PATH: str | None = None
_NS_PATH: str | None = None
_PAIR_ARRAY: np.ndarray | None = None
_TARGET_ARRAY: np.ndarray | None = None


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


def array_hash(array: np.ndarray) -> str:
    return v61.array_hash(np.asarray(array))


def canonical_pairs(pairs: np.ndarray) -> np.ndarray:
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    return np.sort(pairs, axis=1)


def build_adjacency(n: int, edges: np.ndarray) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in canonical_pairs(edges):
        u, v = int(u), int(v)
        if u == v:
            raise ValueError("self-loop in train-positive graph")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def build_structure(adj: list[set[int]]) -> dict:
    """Build raw-star hyperedges and their train-only 2-section counts."""
    n = len(adj)
    degree = np.fromiter((len(x) for x in adj), dtype=np.int64, count=n)
    row_parts, col_parts = [], []
    member_masks = [0] * n
    incident = [set() for _ in range(n)]
    for center, neighbors in enumerate(adj):
        d = len(neighbors)
        if not d:
            continue
        members = np.fromiter([center, *sorted(neighbors)], dtype=np.int64, count=d + 1)
        row_parts.append(members)
        col_parts.append(np.full(d + 1, center, dtype=np.int64))
        mask = 1 << center
        for node in neighbors:
            mask |= 1 << node
            incident[node].add(center)
        incident[center].add(center)
        member_masks[center] = mask
    if row_parts:
        rows = np.concatenate(row_parts)
        cols = np.concatenate(col_parts)
    else:
        rows = cols = np.empty(0, dtype=np.int64)
    incidence = sp.csr_matrix(
        (np.ones(len(rows), dtype=np.int32), (rows, cols)), shape=(n, n), dtype=np.int32,
    )
    incidence.sum_duplicates()
    co = (incidence @ incidence.T).tocsr()
    co.sum_duplicates()
    co.sort_indices()
    q = np.asarray(incidence @ degree, dtype=np.int64).reshape(-1)
    return {
        "n": n, "adj": adj, "degree": degree, "q": q, "co": co,
        "incident": incident, "member_masks": member_masks,
    }


def _pair_projection(ctx: dict, u: int, v: int, target_mask: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float, float, int]:
    if u == v:
        raise ValueError("candidate pair endpoints must differ")
    adj, degree, q, co = ctx["adj"], ctx["degree"], ctx["q"], ctx["co"]
    if target_mask and v not in adj[u]:
        raise ValueError("target mask requested for a pair absent from train graph")
    lo, hi = co.indptr[u], co.indptr[u + 1]
    li, lv = co.indices[lo:hi], co.data[lo:hi]
    lo, hi = co.indptr[v], co.indptr[v + 1]
    ri, rv = co.indices[lo:hi], co.data[lo:hi]
    shared, il, ir = np.intersect1d(li, ri, assume_unique=True, return_indices=True)
    keep = (shared != u) & (shared != v)
    shared, il, ir = shared[keep], il[keep], ir[keep]
    mu = lv[il].astype(np.int64, copy=True)
    mv = rv[ir].astype(np.int64, copy=True)
    if target_mask and len(shared):
        mu -= np.fromiter((int(w in adj[v]) for w in shared), dtype=np.int64, count=len(shared))
        mv -= np.fromiter((int(w in adj[u]) for w in shared), dtype=np.int64, count=len(shared))
    valid = (mu > 0) & (mv > 0)
    shared, mu, mv = shared[valid], mu[valid], mv[valid]
    c = len(shared)
    product = mu * mv
    token_count = int(product.sum()) if c else 0
    max_product = int(product.max()) if c else 0
    ms = float(np.sum(np.log1p(mu) * np.log1p(mv))) if c else 0.0
    qu, qv = int(q[u]), int(q[v])
    qw = q[shared].astype(np.float64, copy=True)
    if target_mask:
        # e_v no longer contains u and e_u loses one neighbor; apply the
        # corresponding symmetric update to q(v).
        qu -= 1 + int(degree[v])
        qv -= 1 + int(degree[u])
        if c:
            qw -= np.fromiter((int(w in adj[u]) + int(w in adj[v]) for w in shared), dtype=np.float64, count=c)
    denom = math.sqrt(max(qu, 1) * max(qv, 1)) * (1.0 + np.maximum(qw, 0.0))
    hra = float(np.sum(1.0 / denom)) if c else 0.0
    return shared, mu, mv, hra, ms, float(max_product), token_count


def _metric_chunk(job: tuple[np.ndarray, bool]) -> np.ndarray:
    pairs, target_mask = job
    if _CTX is None:
        raise RuntimeError("worker structure context was not inherited")
    rows = np.empty((len(pairs), 5), dtype=np.float64)
    for i, (u, v) in enumerate(pairs):
        shared, mu, mv, hra, ms, maxp, count = _pair_projection(_CTX, int(u), int(v), target_mask)
        rows[i] = (len(shared), hra, ms, maxp, count)
    return rows


def map_pair_metrics(ctx: dict, pairs: np.ndarray, target_mask: bool, workers: int) -> np.ndarray:
    global _CTX
    _CTX = ctx
    pairs = canonical_pairs(pairs)
    chunks = [(pairs[i:i + 4096], target_mask) for i in range(0, len(pairs), 4096)]
    if workers <= 1 or len(chunks) <= 1:
        return np.concatenate([_metric_chunk(item) for item in chunks], axis=0) if chunks else np.empty((0, 5))
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("fork")) as pool:
        result = list(pool.map(_metric_chunk, chunks, chunksize=1))
    return np.concatenate(result, axis=0) if result else np.empty((0, 5))


def _pair_degree_bin(u: int, v: int, bins: np.ndarray) -> tuple[int, int]:
    return tuple(sorted((int(bins[u]), int(bins[v]))))


def match_negatives(train_pos: np.ndarray, pool: np.ndarray, pos_metrics: np.ndarray,
                    pool_metrics: np.ndarray, degree: np.ndarray, dataset: str) -> tuple[list[tuple[int, int, int]], dict]:
    bins = np.searchsorted(np.quantile(degree, [0.2, 0.4, 0.6, 0.8]), degree, side="right")
    hra_cuts = np.quantile(pool_metrics[:, 1], [0.2, 0.4, 0.6, 0.8])
    hra_bin = np.searchsorted(hra_cuts, pool_metrics[:, :, 1], side="right")
    tie_seed = MATCH_SEED + {"cora": 1, "pubmed": 2, "citeseer": 3}[dataset]
    tie = np.random.default_rng(tie_seed).random(pool.shape[:2])
    selected: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int]] = set()
    quality = {
        "candidate_pool_per_positive": int(pool.shape[1]), "selected_negative_count": 0,
        "positives_with_matches": 0, "degree_bin_pair_exact": 0,
        "support_count_exact": 0, "hra_bin_exact": 0,
        "degree_support_hra_all_exact": 0, "selection_rank_1": 0,
        "selection_rank_2": 0, "selection_rank_3": 0,
    }
    for i, (pu, pv) in enumerate(train_pos):
        pdegree = _pair_degree_bin(int(pu), int(pv), bins)
        pc = int(round(pos_metrics[i, 0]))
        phb = int(np.searchsorted(hra_cuts, pos_metrics[i, 1], side="right"))
        candidates = []
        for j, (u, v) in enumerate(pool[i]):
            u, v = int(u), int(v)
            c_gap = abs(pc - int(round(pool_metrics[i, j, 0])))
            hb_gap = abs(phb - int(hra_bin[i, j]))
            h_gap = abs(float(pos_metrics[i, 1]) - float(pool_metrics[i, j, 1]))
            dbin = _pair_degree_bin(u, v, bins)
            dbin_gap = abs(dbin[0] - pdegree[0]) + abs(dbin[1] - pdegree[1])
            candidates.append(((dbin_gap, c_gap, hb_gap, h_gap, float(tie[i, j]), u, v), j, dbin_gap, c_gap, hb_gap))
        candidates.sort(key=lambda row: row[0])
        rank = 0
        for _, j, dbin_gap, c_gap, hb_gap in candidates:
            u, v = map(int, pool[i, j])
            pair = (min(u, v), max(u, v))
            if pair in seen:
                continue
            seen.add(pair)
            selected.append((i, pair[0], pair[1]))
            rank += 1
            quality["selected_negative_count"] += 1
            quality["degree_bin_pair_exact"] += int(dbin_gap == 0)
            quality["support_count_exact"] += int(c_gap == 0)
            quality["hra_bin_exact"] += int(hb_gap == 0)
            quality["degree_support_hra_all_exact"] += int(dbin_gap == 0 and c_gap == 0 and hb_gap == 0)
            quality[f"selection_rank_{rank}"] += 1
            if rank == MATCH_PER_POSITIVE:
                break
    quality["positives_with_matches"] = len({i for i, _, _ in selected})
    quality["matched_per_positive_histogram"] = {
        str(k): sum(1 for i in range(len(train_pos)) if sum(1 for g, _, _ in selected if g == i) == k)
        for k in range(MATCH_PER_POSITIVE + 1)
    }
    return selected, quality


def _size_bin(size: int) -> int:
    if size <= 2:
        return 0
    if size == 3:
        return 1
    if size == 4:
        return 2
    if size <= 8:
        return 3
    if size <= 16:
        return 4
    if size <= 32:
        return 5
    return 6


def _mult_bin(value: int) -> int:
    if value <= 1:
        return 0
    if value == 2:
        return 1
    if value <= 4:
        return 2
    if value <= 8:
        return 3
    if value <= 16:
        return 4
    if value <= 32:
        return 5
    return 6


def _iter_native_tokens(ctx: dict, u: int, v: int, target_mask: bool):
    shared, mu, mv, _, _, _, expected = _pair_projection(ctx, u, v, target_mask)
    incident, masks, degree = ctx["incident"], ctx["member_masks"], ctx["degree"]
    anchor_bits_base = (1 << u) | (1 << v)
    emitted = 0
    for w, m_u, m_v in zip(shared.tolist(), mu.tolist(), mv.tolist()):
        centers_u = incident[u].intersection(incident[w])
        centers_v = incident[v].intersection(incident[w])
        if target_mask:
            centers_u.discard(v)  # e_v loses u when (u,v) is removed
            centers_v.discard(u)  # e_u loses v when (u,v) is removed
        if len(centers_u) != m_u or len(centers_v) != m_v:
            raise RuntimeError(f"incidence identity/count mismatch for pair {(u, v)}, support {w}: {(len(centers_u), len(centers_v))} != {(m_u, m_v)}")
        anchors = anchor_bits_base | (1 << w)
        u_mb, v_mb = _mult_bin(m_u), _mult_bin(m_v)
        for e_center in sorted(centers_u):
            size_e = int(degree[e_center]) + 1 - int(target_mask and e_center in (u, v))
            if size_e <= 1:
                continue
            a = masks[e_center] & ~anchors
            a_size = a.bit_count()
            s_e = math.log1p(size_e)
            for f_center in sorted(centers_v):
                size_f = int(degree[f_center]) + 1 - int(target_mask and f_center in (u, v))
                if size_f <= 1:
                    continue
                b = masks[f_center] & ~anchors
                b_size = b.bit_count()
                overlap = (a & b).bit_count()
                union = (a | b).bit_count()
                s_f = math.log1p(size_f)
                size_desc = (s_e + s_f, abs(s_e - s_f), s_e * s_f)
                overlap_desc = (math.log1p(overlap), overlap / max(1, union),
                                overlap / max(1, min(a_size, b_size)))
                sb0, sb1 = sorted((_size_bin(size_e), _size_bin(size_f)))
                mb0, mb1 = sorted((u_mb, v_mb))
                stratum = (((sb0 * 7 + sb1) * 7 + mb0) * 7 + mb1)
                denom = math.sqrt(max(1, (size_e - 2) * (size_f - 2)))
                ns_contribution = math.log1p(overlap) / denom
                emitted += 1
                yield size_desc, overlap_desc, stratum, ns_contribution
    if emitted != expected:
        raise RuntimeError(f"native token count mismatch for {(u, v)}: emitted {emitted}, expected {expected}")
def _collect_native_rows(ctx: dict, u: int, v: int, target_mask: bool) -> np.ndarray:
    rows = []
    for sizes, overlap, _, _ in _iter_native_tokens(ctx, u, v, target_mask):
        rows.append((*sizes, *overlap))
    return np.asarray(rows, dtype=np.float64).reshape(-1, 6)


def _pair_context_fresh(adj: list[set[int]], n: int) -> dict:
    return build_structure(adj)


def audit_target_mask(ctx: dict, train_pos: np.ndarray, dataset: str) -> dict:
    rng = np.random.default_rng(AUDIT_SEED + {"cora": 1, "pubmed": 2, "citeseer": 3}[dataset])
    count = min(100, len(train_pos))
    ids = rng.choice(len(train_pos), size=count, replace=False)
    max_abs = 0.0
    max_tokens = 0
    for sample_id in ids:
        u, v = map(int, train_pos[int(sample_id)])
        local_stats = _pair_projection(ctx, u, v, True)
        masked_adj = [set(row) for row in ctx["adj"]]
        masked_adj[u].remove(v)
        masked_adj[v].remove(u)
        full = _pair_context_fresh(masked_adj, ctx["n"])
        full_stats = _pair_projection(full, u, v, False)
        for a, b in zip(local_stats[:3], full_stats[:3]):
            if not np.array_equal(a, b):
                raise RuntimeError(f"target-mask projection mismatch on {dataset} pair {(u, v)}")
        if any(abs(float(a) - float(b)) > 1e-6 for a, b in zip(local_stats[3:6], full_stats[3:6])) or local_stats[6] != full_stats[6]:
            raise RuntimeError(f"target-mask scalar mismatch on {dataset} pair {(u, v)}")
        local_rows = _collect_native_rows(ctx, u, v, True)
        full_rows = _collect_native_rows(full, u, v, False)
        reverse_rows = _collect_native_rows(ctx, v, u, True)
        max_tokens = max(max_tokens, len(local_rows), len(full_rows))
        if local_rows.shape != full_rows.shape or local_rows.shape != reverse_rows.shape:
            raise RuntimeError(f"target-mask or endpoint-symmetry token-count mismatch on {dataset} pair {(u, v)}")
        order = lambda rows: rows[np.lexsort(tuple(rows[:, k] for k in range(5, -1, -1)))] if len(rows) else rows
        local_sorted, full_sorted, reverse_sorted = map(order, (local_rows, full_rows, reverse_rows))
        for other in (full_sorted, reverse_sorted):
            diff = np.abs(local_sorted - other)
            current = float(diff.max()) if diff.size else 0.0
            max_abs = max(max_abs, current)
            if current > 1e-6:
                raise RuntimeError(f"target-mask or endpoint-symmetry descriptor mismatch on {dataset} pair {(u, v)}: {current}")
        del full
    return {"pairs_checked": int(count), "full_rebuild_equal": True,
            "endpoint_symmetry_equal": True, "max_abs_token_difference": max_abs,
            "largest_sample_token_count": max_tokens, "tolerance": 1e-6}


def _stats(values: np.ndarray) -> dict:
    values = np.asarray(values, dtype=np.int64)
    if not len(values):
        return {"count": 0, "total": 0, "mean": 0.0, "median": 0.0,
                "p90": 0.0, "p95": 0.0, "p99": 0.0, "max": 0}
    return {"count": int(len(values)), "total": int(values.sum()),
            "mean": float(np.mean(values)), "median": float(np.median(values)),
            "p90": float(np.quantile(values, 0.90)), "p95": float(np.quantile(values, 0.95)),
            "p99": float(np.quantile(values, 0.99)), "max": int(values.max())}


def _summary_block(values: np.ndarray, percentiles: tuple[float, ...]) -> list[float]:
    if not len(values):
        return [0.0] * (values.shape[1] * (4 + len(percentiles)))
    return np.concatenate((values.mean(axis=0), values.std(axis=0), values.max(axis=0),
                           *[np.percentile(values, p, axis=0) for p in percentiles])).astype(np.float64).tolist()


def cv_metrics(x: np.ndarray, y: np.ndarray, groups: np.ndarray) -> dict:
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=FOLDS_SEED)
    auc, ap, sizes = [], [], []
    for train, test in splitter.split(x, y, groups):
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=0),
        )
        model.fit(x[train], y[train])
        score = model.predict_proba(x[test])[:, 1]
        auc.append(float(roc_auc_score(y[test], score)))
        ap.append(float(average_precision_score(y[test], score)))
        sizes.append(int(len(test)))
    return {"roc_auc_by_fold": auc, "roc_auc_mean": float(np.mean(auc)),
            "roc_auc_sample_std": float(np.std(auc, ddof=1)),
            "pr_auc_by_fold": ap, "pr_auc_mean": float(np.mean(ap)),
            "pr_auc_sample_std": float(np.std(ap, ddof=1)), "fold_sizes": sizes}


def _aggregate_pair_features(token_path: Path, shuffle_path: Path, offsets: np.ndarray,
                              pair_count: int, z2: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    records = np.load(token_path, mmap_mode="r")
    shuffled = np.load(shuffle_path, mmap_mode="r")
    z3, z4, informative = [], [], np.zeros(pair_count, dtype=bool)
    log3 = np.float32(math.log1p(2))
    for i in range(pair_count):
        lo, hi = int(offsets[i]), int(offsets[i + 1])
        if hi == lo:
            size_block = [0.0] * 12
            overlap_block = [0.0] * 15
            frac = [0.0, 0.0]
            shuf_block = [0.0] * 15
            shuf_frac = [0.0, 0.0]
        else:
            size = records["size"][lo:hi].astype(np.float64)
            real = records["overlap"][lo:hi].astype(np.float64)
            shuf = np.asarray(shuffled[lo:hi], dtype=np.float64)
            size_block = _summary_block(size, (75.0,))
            overlap_block = _summary_block(real, (75.0, 90.0))
            shuf_block = _summary_block(shuf, (75.0, 90.0))
            frac = [float(np.mean(real[:, 0] > 0.0)), float(np.mean(real[:, 0] >= float(log3)))]
            shuf_frac = [float(np.mean(shuf[:, 0] > 0.0)), float(np.mean(shuf[:, 0] >= float(log3)))]
            informative[i] = bool(np.any(np.any(records["overlap"][lo:hi] != shuffled[lo:hi], axis=1)))
        log_token_count = math.log1p(int(offsets[i + 1] - offsets[i]))
        z3.append(np.concatenate((z2[i], np.asarray(size_block + [log_token_count], dtype=np.float64))))
        z4.append(np.concatenate((z3[-1], np.asarray(overlap_block + frac, dtype=np.float64))))
        z4[-1] = (z4[-1], np.concatenate((z3[-1], np.asarray(shuf_block + shuf_frac, dtype=np.float64))))
    z3_array = np.stack(z3)
    z4_real = np.stack([row[0] for row in z4])
    z5 = np.stack([row[1] for row in z4])
    return z3_array, z4_real, np.column_stack((z5, informative.astype(np.float64)))


def _shuffle_tokens(token_path: Path, shuffle_path: Path, pair_offsets: np.ndarray,
                    seed: int) -> dict:
    records = np.load(token_path, mmap_mode="r")
    total = len(records)
    shuffled = np.lib.format.open_memmap(shuffle_path, mode="w+", dtype=np.float32, shape=(total, 3))
    if total:
        order = np.argsort(records["stratum"], kind="stable")
        strata = records["stratum"][order]
        starts = np.r_[0, np.flatnonzero(strata[1:] != strata[:-1]) + 1, total]
        rng = np.random.default_rng(seed)
        singleton_tokens = 0
        stratum_count = len(starts) - 1
        for a, b in zip(starts[:-1], starts[1:]):
            ids = order[a:b]
            if len(ids) <= 1:
                singleton_tokens += len(ids)
                shuffled[ids] = records["overlap"][ids]
            else:
                source = ids.copy()
                rng.shuffle(source)
                shuffled[ids] = records["overlap"][source]
        shuffled.flush()
    else:
        singleton_tokens, stratum_count = 0, 0
        shuffled.flush()
    del shuffled
    records = np.load(token_path, mmap_mode="r")
    sh = np.load(shuffle_path, mmap_mode="r")
    changed_pairs = 0
    for i in range(len(pair_offsets) - 1):
        lo, hi = int(pair_offsets[i]), int(pair_offsets[i + 1])
        if hi > lo and np.any(np.any(records["overlap"][lo:hi] != sh[lo:hi], axis=1)):
            changed_pairs += 1
    pair_total = len(pair_offsets) - 1
    return {"seed": seed, "stratum_count": int(stratum_count),
            "singleton_token_fraction": float(singleton_tokens / max(1, total)),
            "informative_pair_count": int(changed_pairs),
            "candidate_pair_count": int(pair_total),
            "informative_shuffle_fraction": float(changed_pairs / max(1, pair_total)),
            "shuffle_power": "LOW_NATIVE_SHUFFLE_POWER" if changed_pairs / max(1, pair_total) < 0.30 else "ADEQUATE"}


def _native_chunk_task(bounds: tuple[int, int]) -> tuple[int, int]:
    if _CTX is None or _OFFSETS is None or _TOKEN_PATH is None or _NS_PATH is None:
        raise RuntimeError("native-token worker globals missing")
    token_map = np.load(_TOKEN_PATH, mmap_mode="r+")
    ns_map = np.load(_NS_PATH, mmap_mode="r+")
    start, end = bounds
    for pair_id in range(start, end):
        u, v = map(int, _PAIR_ARRAY[pair_id])
        target = bool(_TARGET_ARRAY[pair_id])
        cursor = int(_OFFSETS[pair_id])
        stop = int(_OFFSETS[pair_id + 1])
        buffer = []
        ns_total = 0.0
        for size_desc, overlap_desc, stratum, ns_contribution in _iter_native_tokens(_CTX, u, v, target):
            buffer.append((pair_id, stratum, size_desc, overlap_desc))
            ns_total += ns_contribution
            if len(buffer) >= 8192:
                chunk = np.asarray(buffer, dtype=TOKEN_DTYPE)
                token_map[cursor:cursor + len(chunk)] = chunk
                cursor += len(chunk)
                buffer.clear()
        if buffer:
            chunk = np.asarray(buffer, dtype=TOKEN_DTYPE)
            token_map[cursor:cursor + len(chunk)] = chunk
            cursor += len(chunk)
        if cursor != stop:
            raise RuntimeError(f"native token offset mismatch for pair {pair_id}: {cursor-int(_OFFSETS[pair_id])} != {stop-int(_OFFSETS[pair_id])}")
        ns_map[pair_id] = ns_total
    token_map.flush()
    ns_map.flush()
    del token_map, ns_map
    return start, end


def _token_counts_summary(values: np.ndarray, labels: np.ndarray) -> dict:
    return {"all": _stats(values), "positive": _stats(values[labels == 1]),
            "matched_negative": _stats(values[labels == 0]),
            "largest_token_pair_index": int(np.argmax(values)) if len(values) else None}


def _dataset_name(name: str) -> str:
    name = name.lower()
    if name not in {"cora", "pubmed", "citeseer"}:
        raise ValueError(f"unsupported dataset {name}")
    return name


def run_dataset(dataset: str, workers: int) -> dict:
    global _CTX, _OFFSETS, _TOKEN_PATH, _NS_PATH, _PAIR_ARRAY, _TARGET_ARRAY
    dataset = _dataset_name(dataset)
    started_wall, started_cpu = time.perf_counter(), os.times()
    diag = OUT / "diagnostics"
    diag.mkdir(parents=True, exist_ok=True)
    status_path = diag / f"stage0_{dataset}_status.json"
    result_path = diag / f"stage0_{dataset}.json"
    status = {"state": "RUNNING", "dataset": dataset, "phase": "loading_train_only_split",
              "gpu_compute_used": False, "test_evaluated": False}
    write_json(status_path, status)
    timings: dict[str, float] = {}
    try:
        import torch

        if hasattr(torch, "set_num_threads"):
            torch.set_num_threads(1)
            torch.set_num_interop_threads(1)
        t0 = time.perf_counter()
        full, view = base.init_dataset(dataset)
        split_hash = base.split_hash(view)
        train_pos = canonical_pairs(np.asarray(view.train_pos, dtype=np.int64))
        n_nodes = int(view.num_nodes)
        feature_hash = array_hash(np.asarray(view.features))
        del full
        if view.placeholder_reads != {"valid_pos": 0, "test_pos": 0}:
            raise RuntimeError(f"held-out identity placeholder access detected: {view.placeholder_reads}")
        pool, pool_hash = base.training_pool(view)
        if pool.shape != (len(train_pos), POOL_PER_POSITIVE, 2):
            raise RuntimeError(f"unexpected frozen training-pool shape: {pool.shape}")
        if view.placeholder_reads != {"valid_pos": 0, "test_pos": 0}:
            raise RuntimeError(f"held-out identity placeholder access detected during pool generation: {view.placeholder_reads}")
        timings["load_and_train_pool_seconds"] = time.perf_counter() - t0
        status.update({"phase": "building_train_only_raw_star", "train_positive_count": len(train_pos),
                       "pool_shape": list(pool.shape), "split_hash": split_hash})
        write_json(status_path, status)

        t0 = time.perf_counter()
        adj = build_adjacency(n_nodes, train_pos)
        ctx = build_structure(adj)
        _CTX = ctx
        degree = ctx["degree"]
        timings["raw_star_projection_seconds"] = time.perf_counter() - t0

        t0 = time.perf_counter()
        pos_metrics = map_pair_metrics(ctx, train_pos, True, workers)
        pool_flat = canonical_pairs(pool.reshape(-1, 2))
        unique_pool, inverse = np.unique(pool_flat, axis=0, return_inverse=True)
        unique_metrics = map_pair_metrics(ctx, unique_pool, False, workers)
        pool_metrics = unique_metrics[inverse].reshape(len(train_pos), POOL_PER_POSITIVE, 5)
        selected, match_quality = match_negatives(train_pos, pool, pos_metrics, pool_metrics, degree, dataset)
        if not selected:
            raise RuntimeError("matched-negative selection returned no legal negatives")
        pos_set = {tuple(map(int, row)) for row in train_pos.tolist()}
        if any((u, v) in pos_set for _, u, v in selected):
            raise RuntimeError("matched negative overlaps a train positive")
        # Re-index selected candidates directly by their canonical pair for a
        # deterministic exact match to the 20-entry generated pool.
        selected_metric_rows = []
        for group, u, v in selected:
            want = (u, v)
            found = None
            for j, pair in enumerate(pool[group]):
                a, b = map(int, pair)
                if (min(a, b), max(a, b)) == want:
                    found = pool_metrics[group, j]
                    break
            if found is None:
                raise RuntimeError(f"matched pair missing from its train-only candidate row: {(group, u, v)}")
            selected_metric_rows.append(found)
        chosen_metrics = np.asarray(selected_metric_rows, dtype=np.float64)
        pairs = np.vstack((train_pos, np.asarray([(u, v) for _, u, v in selected], dtype=np.int64)))
        labels = np.r_[np.ones(len(train_pos), dtype=np.int64), np.zeros(len(selected), dtype=np.int64)]
        groups = np.r_[np.arange(len(train_pos), dtype=np.int64), np.asarray([i for i, _, _ in selected], dtype=np.int64)]
        targets = np.r_[np.ones(len(train_pos), dtype=bool), np.zeros(len(selected), dtype=bool)]
        pair_metrics = np.vstack((pos_metrics, chosen_metrics))
        pair_token_counts = np.rint(pair_metrics[:, 4]).astype(np.int64)
        if int(pair_token_counts.sum()) < 0:
            raise RuntimeError("invalid negative native-token count")
        timings["candidate_scoring_and_matching_seconds"] = time.perf_counter() - t0
        status.update({"phase": "target_mask_equivalence_and_token_preflight",
                       "matched_negative_count": len(selected), "token_count_total": int(pair_token_counts.sum())})
        write_json(status_path, status)

        t0 = time.perf_counter()
        target_audit = audit_target_mask(ctx, train_pos, dataset)
        timings["target_mask_audit_seconds"] = time.perf_counter() - t0
        token_summary = _token_counts_summary(pair_token_counts, labels)
        total_tokens = int(pair_token_counts.sum())
        estimated_bytes = total_tokens * TOKEN_DTYPE.itemsize + total_tokens * 3 * np.dtype(np.float32).itemsize
        disk_free = int(__import__("shutil").disk_usage(OUT).free)
        token_summary.update({"per_pair_cache_record_bytes": TOKEN_DTYPE.itemsize,
                              "estimated_raw_and_shuffle_cache_bytes": estimated_bytes,
                              "available_disk_bytes_at_preflight": disk_free,
                              "token_explosion_review_required": bool(token_summary["all"]["max"] >= 1_000_000 or estimated_bytes >= 10 * 1024**3)})
        if estimated_bytes > int(disk_free * 0.8):
            result = {"state": "TOKEN_EXPLOSION_REQUIRES_PROTOCOL", "dataset": dataset,
                      "token_count_distribution": token_summary, "target_mask_audit": target_audit,
                      "gpu_compute_used": False, "test_evaluated": False,
                      "failure_reason": "full native-token cache would exceed 80% of available disk; no truncation applied"}
            write_json(result_path, result)
            status.update({"state": "COMPLETE", "phase": "stopped_token_explosion", "decision": result["state"]})
            write_json(status_path, status)
            return result

        offsets = np.r_[0, np.cumsum(pair_token_counts, dtype=np.int64)]
        token_path = diag / f"stage0_{dataset}_native_tokens.npy"
        shuffle_path = diag / f"stage0_{dataset}_shuffle_overlap.npy"
        ns_path = diag / f"stage0_{dataset}_native_scalar.npy"
        if total_tokens:
            np.lib.format.open_memmap(token_path, mode="w+", dtype=TOKEN_DTYPE, shape=(total_tokens,)).flush()
        else:
            np.save(token_path, np.empty(0, dtype=TOKEN_DTYPE), allow_pickle=False)
        np.lib.format.open_memmap(ns_path, mode="w+", dtype=np.float64, shape=(len(pairs),)).flush()
        _PAIR_ARRAY, _TARGET_ARRAY = pairs, targets
        _OFFSETS, _TOKEN_PATH, _NS_PATH = offsets, str(token_path), str(ns_path)
        t0 = time.perf_counter()
        if workers <= 1 or len(pairs) <= 1:
            _native_chunk_task((0, len(pairs)))
        else:
            chunks = [(i, min(len(pairs), i + 128)) for i in range(0, len(pairs), 128)]
            with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("fork")) as process_pool:
                list(process_pool.map(_native_chunk_task, chunks, chunksize=1))
        timings["native_token_cache_seconds"] = time.perf_counter() - t0

        t0 = time.perf_counter()
        shuffle_meta = _shuffle_tokens(token_path, shuffle_path, offsets,
                                       SHUFFLE_SEED + {"cora": 1, "pubmed": 2, "citeseer": 3}[dataset])
        timings["shuffle_seconds"] = time.perf_counter() - t0

        z0 = np.log1p(pair_metrics[:, 0:1])
        z1 = pair_metrics[:, 1:2]
        z2 = np.column_stack((np.log1p(pair_metrics[:, 0]), pair_metrics[:, 1],
                              pair_metrics[:, 2], np.log1p(pair_metrics[:, 3])))
        t0 = time.perf_counter()
        z3, z4, z5_plus_info = _aggregate_pair_features(token_path, shuffle_path, offsets, len(pairs), z2)
        z5 = z5_plus_info[:, :-1]
        informative = z5_plus_info[:, -1].astype(bool)
        ns = np.asarray(np.load(ns_path, mmap_mode="r"), dtype=np.float64).reshape(-1, 1)
        timings["pair_feature_aggregation_seconds"] = time.perf_counter() - t0
        t0 = time.perf_counter()
        cv = {
            "Z0_CN": cv_metrics(z0, labels, groups),
            "Z1_HRA": cv_metrics(z1, labels, groups),
            "Z2_PROJECTION": cv_metrics(z2, labels, groups),
            "Z3_NATIVE_SIZE": cv_metrics(z3, labels, groups),
            "Z4_NATIVE_REAL": cv_metrics(z4, labels, groups),
            "Z5_NATIVE_SHUFFLE": cv_metrics(z5, labels, groups),
            "NATIVE_SCALAR_NS": cv_metrics(ns, labels, groups),
        }
        timings["classifier_cv_seconds"] = time.perf_counter() - t0
        auc = {key: val["roc_auc_mean"] for key, val in cv.items()}
        d_native = auc["Z4_NATIVE_REAL"] - auc["Z2_PROJECTION"]
        d_content = auc["Z4_NATIVE_REAL"] - auc["Z3_NATIVE_SIZE"]
        d_semantic = auc["Z4_NATIVE_REAL"] - auc["Z5_NATIVE_SHUFFLE"]
        power = shuffle_meta["informative_shuffle_fraction"] >= 0.30
        native_signal = (d_native >= 0.010 and d_content >= 0.005 and
                         (d_semantic >= 0.010 if power else d_semantic > 0.0))
        if not power:
            shuffle_meta["shuffle_power"] = "LOW_NATIVE_SHUFFLE_POWER"
        dataset_decision = "NATIVE_SIGNAL" if native_signal else "NO_NATIVE_STRUCTURE_SIGNAL"
        native_scalar_sufficient = bool(auc["NATIVE_SCALAR_NS"] >= auc["Z4_NATIVE_REAL"])
        selected_hash = array_hash(np.asarray([(g, u, v) for g, u, v in selected], dtype=np.int64))
        cache_path = diag / f"stage0_{dataset}_features.npz"
        np.savez_compressed(cache_path, pairs=pairs, labels=labels, groups=groups,
                            target_mask=targets, token_counts=pair_token_counts,
                            pair_token_offsets=offsets, Z0=z0, Z1=z1, Z2=z2,
                            Z3=z3, Z4=z4, Z5=z5, NS=ns)
        cache_hashes = {
            "pair_feature_archive_sha256": sha256_file(cache_path),
            "native_token_cache_sha256": sha256_file(token_path),
            "shuffle_overlap_cache_sha256": sha256_file(shuffle_path),
            "native_scalar_cache_sha256": sha256_file(ns_path),
        }
        child = os.times()
        cpu_start = getattr(run_dataset, "_cpu_start", None)
        timings["dataset_wall_seconds"] = time.perf_counter() - started_wall
        result = {
            "state": "COMPLETE", "dataset": dataset, "decision": dataset_decision,
            "native_signal": bool(native_signal), "native_scalar_sufficient_on_dataset": native_scalar_sufficient,
            "strict_train_only": True, "test_evaluated": False, "gpu_compute_used": False,
            "num_nodes": n_nodes, "train_positive_count": int(len(train_pos)),
            "split_hash": split_hash, "train_feature_hash": feature_hash,
            "train_positive_hash": array_hash(train_pos), "training_pool_hash": pool_hash,
            "training_pool_shape": list(pool.shape), "unique_pool_pair_count": int(len(unique_pool)),
            "matched_negative_count": int(len(selected)), "matched_negative_hash": selected_hash,
            "matching": match_quality, "target_mask_audit": target_audit,
            "token_count_distribution": token_summary, "shuffle": shuffle_meta,
            "cv": cv, "auc": auc,
            "deltas": {"native_minus_projection": d_native, "real_minus_size": d_content,
                       "real_minus_shuffle": d_semantic,
                       "native_minus_projection_gate": d_native >= 0.010,
                       "real_minus_size_gate": d_content >= 0.005,
                       "real_minus_shuffle_gate": d_semantic >= (0.010 if power else 0.0) if power else d_semantic > 0.0},
            "decision_rule": {"native_signal": "Delta_native>=0.010 and Delta_content>=0.005 and Delta_semantic>=0.010 when shuffle power>=30%, otherwise Delta_semantic>0; weak shuffle is annotated, not treated as a strong mechanism rejection",
                              "native_scalar_sufficient_on_dataset": "AUC(NS)>=AUC(Z4); final sufficiency requires Cora and at least one extra dataset"},
            "cache_paths": {"features": str(cache_path), "native_tokens": str(token_path),
                            "shuffle_overlap": str(shuffle_path), "native_scalar": str(ns_path)},
            "cache_hashes": cache_hashes,
            "source_hashes": {"experiment_v71.py": sha256_file(V71 / "experiment_v71.py"),
                              "run_negative_v6_1.py": sha256_file(V61 / "run_negative_v6_1.py"),
                              "loaders.py": sha256_file(ROOT / "src" / "dcdlp" / "data" / "loaders.py"),
                              "native_stage0_script.py": sha256_file(HERE)},
            "heldout_positive_placeholder_reads": dict(view.placeholder_reads),
            "timings_seconds": timings,
            "cpu_time_seconds": {"user_child": float(child.children_user), "system_child": float(child.children_system)},
        }
        write_json(result_path, result)
        status.update({"state": "COMPLETE", "phase": "stage0_complete", "decision": dataset_decision,
                       "native_signal": bool(native_signal), "native_scalar_sufficient_on_dataset": native_scalar_sufficient,
                       "runtime_seconds": timings["dataset_wall_seconds"]})
        write_json(status_path, status)
        return result
    except Exception as exc:
        failure = {"state": "FAILED", "dataset": dataset, "error": repr(exc),
                   "traceback": traceback.format_exc(), "gpu_compute_used": False,
                   "test_evaluated": False, "timings_seconds": timings}
        write_json(result_path, failure)
        status.update({"state": "FAILED", "phase": "failed", "error": repr(exc)})
        write_json(status_path, status)
        raise


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: nhmc_stage0.py {cora|pubmed|citeseer} [workers]")
    dataset = _dataset_name(sys.argv[1])
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.environ.get("NHMC_WORKERS", "12"))
    workers = max(1, workers)
    result = run_dataset(dataset, workers)
    print(json.dumps({"dataset": dataset, "state": result.get("state"),
                      "decision": result.get("decision"), "native_signal": result.get("native_signal"),
                      "native_scalar_sufficient_on_dataset": result.get("native_scalar_sufficient_on_dataset"),
                      "wall_seconds": result.get("timings_seconds", {}).get("dataset_wall_seconds"),
                      "token_total": result.get("token_count_distribution", {}).get("all", {}).get("total")},
                     indent=2), flush=True)


if __name__ == "__main__":
    main()
