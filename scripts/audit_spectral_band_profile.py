"""Stage-0/Stage-1 audit for a fixed Laplacian spectral band profile."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_adjacency(edges: np.ndarray, n: int) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for x, y in np.asarray(edges, dtype=np.int64):
        x, y = int(x), int(y)
        if x != y:
            adj[x].add(y); adj[y].add(x)
    return adj


def spectral_basis(adj: list[set[int]], k: int = 32):
    n = len(adj); rows, cols = [], []
    for u, neighbors in enumerate(adj):
        for v in neighbors: rows.append(u); cols.append(v)
    matrix = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    degree = np.asarray(matrix.sum(axis=1)).ravel(); inv_sqrt = 1.0 / np.sqrt(np.maximum(degree, 1.0))
    laplacian = sp.eye(n, format="csr") - sp.diags(inv_sqrt) @ matrix @ sp.diags(inv_sqrt)
    values, vectors = eigsh(laplacian, k=min(k + 1, n - 2), which="SM")
    order = np.argsort(values); values, vectors = values[order], vectors[:, order]
    keep = np.where(values > 1e-7)[0][:k]
    return values[keep], vectors[:, keep]


def pair_features(adj, u, v):
    common = (adj[u] & adj[v]) - {u, v}; l3 = 0
    first, second = (adj[u], adj[v]) if len(adj[u]) <= len(adj[v]) else (adj[v], adj[u])
    for a in first: l3 += sum(1 for b in adj[a] if b in second and a != v and b != u and a != b)
    aa = sum(1.0 / math.log1p(len(adj[x])) for x in common); ra = sum(1.0 / max(1, len(adj[x])) for x in common)
    return np.asarray([len(common), aa, ra, math.log1p(len(adj[u]) * len(adj[v])), l3, len(common) + 0.01 * l3], dtype=np.float64)


def spectral_matrix(basis, values, pairs):
    vectors = basis[np.asarray(pairs, dtype=np.int64)]
    diff = (vectors[:, 0, :] - vectors[:, 1, :]) ** 2
    bands = [slice(0, 4), slice(4, 8), slice(8, 16), slice(16, 32)]
    raw = np.column_stack([diff[:, band].sum(axis=1) for band in bands])
    weighted = np.column_stack([(diff[:, band] / (values[band] + 0.05)).sum(axis=1) for band in bands])
    return np.c_[raw, weighted]


def sample_train_negatives(all_positive, n, seed, count):
    known = {tuple(sorted((int(x), int(y)))) for x, y in all_positive}; rng = np.random.default_rng(10000 + seed); negatives = []
    while len(negatives) < count:
        u, v = int(rng.integers(n)), int(rng.integers(n))
        if u == v: continue
        pair = tuple(sorted((u, v)))
        if pair not in known: known.add(pair); negatives.append(pair)
    return np.asarray(negatives, dtype=np.int64)


def scalar_matrix(adj, pairs):
    return np.asarray([pair_features(adj, int(u), int(v)) for u, v in pairs], dtype=np.float64)


def fit(train_x, train_y, valid_x, valid_y):
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, solver="liblinear")); model.fit(train_x, train_y); score = model.predict_proba(valid_x)[:, 1]
    return {"auc": float(roc_auc_score(valid_y, score)), "ap": float(average_precision_score(valid_y, score))}


def shuffle(values, scalar, seed):
    rng = np.random.default_rng(seed); out = values.copy(); strata = defaultdict(list)
    for i, row in enumerate(scalar): strata[(float(round(row[0], 3)), float(round(row[4], 3)), float(round(row[3], 3)))].append(i)
    for indices in strata.values():
        if len(indices) > 1: out[indices] = values[rng.permutation(np.asarray(indices, dtype=np.int64))]
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--data-root", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4]); args = parser.parse_args(); result = {"candidate": "R4-08 Fixed Laplacian Spectral Band Profile", "support": [], "probes": []}
    for seed in args.seeds:
        data = np.load(args.data_root / f"cora_heart_seed{seed}.npz", allow_pickle=False); adj = build_adjacency(np.asarray(data["train_pos"], dtype=np.int64), int(data["num_nodes"])); values, basis = spectral_basis(adj)
        pos = np.asarray(data["test_pos"], dtype=np.int64); neg = np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2); pos_obj, neg_obj = spectral_matrix(basis, values, pos), spectral_matrix(basis, values, neg)
        result["support"].append({"seed": seed, "positive_nonzero": int(np.sum(pos_obj.sum(axis=1) > 0)), "negative_nonzero": int(np.sum(neg_obj.sum(axis=1) > 0)), "positive_mean_norm": float(np.mean(pos_obj[:, :4].sum(axis=1))), "negative_mean_norm": float(np.mean(neg_obj[:, :4].sum(axis=1)))})
        train_pos = np.asarray(data["train_pos"], dtype=np.int64); train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), int(data["num_nodes"]), seed, len(train_pos)); valid_pos = np.asarray(data["valid_pos"], dtype=np.int64); valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]; train_pairs = np.concatenate([train_pos, train_neg]); valid_pairs = np.concatenate([valid_pos, valid_neg]); train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))]; valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))]
        train_scalar, valid_scalar = scalar_matrix(adj, train_pairs), scalar_matrix(adj, valid_pairs); train_obj, valid_obj = spectral_matrix(basis, values, train_pairs), spectral_matrix(basis, values, valid_pairs); train_shuf, valid_shuf = shuffle(train_obj, train_scalar, 20000 + seed), shuffle(valid_obj, valid_scalar, 30000 + seed)
        matrices = {"Base": (train_scalar[:, :4], valid_scalar[:, :4]), "DangerousControls": (train_scalar, valid_scalar), "TrueSpectral": (np.c_[train_scalar, train_obj], np.c_[valid_scalar, valid_obj]), "ShuffledSpectral": (np.c_[train_scalar, train_shuf], np.c_[valid_scalar, valid_shuf])}
        metrics = {name: fit(x, train_y, y, valid_y) for name, (x, y) in matrices.items()}
        proxy_train = np.c_[np.log1p(np.maximum(train_scalar[:, 4], 0)), np.sqrt(np.maximum(train_scalar[:, 4], 0)), np.log1p(np.maximum(train_scalar[:, 0], 0)), np.sqrt(np.maximum(train_scalar[:, 0], 0)), train_scalar[:, 3], train_scalar[:, 3] ** 2, np.log1p(np.maximum(train_scalar[:, 5], 0)), np.sin(np.minimum(train_scalar[:, 4], 20)), np.cos(np.minimum(train_scalar[:, 4], 20))]; proxy_valid = np.c_[np.log1p(np.maximum(valid_scalar[:, 4], 0)), np.sqrt(np.maximum(valid_scalar[:, 4], 0)), np.log1p(np.maximum(valid_scalar[:, 0], 0)), np.sqrt(np.maximum(valid_scalar[:, 0], 0)), valid_scalar[:, 3], valid_scalar[:, 3] ** 2, np.log1p(np.maximum(valid_scalar[:, 5], 0)), np.sin(np.minimum(valid_scalar[:, 4], 20)), np.cos(np.minimum(valid_scalar[:, 4], 20))]
        metrics["Proxy"] = fit(np.c_[train_scalar, proxy_train], train_y, np.c_[valid_scalar, proxy_valid], valid_y)
        result["probes"].append({"seed": seed, "metrics": metrics, "candidate_minus_controls_auc": metrics["TrueSpectral"]["auc"] - metrics["DangerousControls"]["auc"], "candidate_minus_shuffled_auc": metrics["TrueSpectral"]["auc"] - metrics["ShuffledSpectral"]["auc"], "candidate_minus_proxy_auc": metrics["TrueSpectral"]["auc"] - metrics["Proxy"]["auc"], "candidate_minus_controls_ap": metrics["TrueSpectral"]["ap"] - metrics["DangerousControls"]["ap"], "candidate_minus_shuffled_ap": metrics["TrueSpectral"]["ap"] - metrics["ShuffledSpectral"]["ap"], "candidate_minus_proxy_ap": metrics["TrueSpectral"]["ap"] - metrics["Proxy"]["ap"]})
    result["probe_aggregate"] = {}
    for name in ("Base", "DangerousControls", "TrueSpectral", "ShuffledSpectral", "Proxy"):
        rows = [x["metrics"][name] for x in result["probes"]]; result["probe_aggregate"][name] = {"auc_mean": float(np.mean([x["auc"] for x in rows])), "auc_std": float(np.std([x["auc"] for x in rows], ddof=1)), "ap_mean": float(np.mean([x["ap"] for x in rows])), "ap_std": float(np.std([x["ap"] for x in rows], ddof=1))}
    result["delta_aggregate"] = {key: float(np.mean([x[key] for x in result["probes"]])) for key in ("candidate_minus_controls_auc", "candidate_minus_shuffled_auc", "candidate_minus_proxy_auc", "candidate_minus_controls_ap", "candidate_minus_shuffled_ap", "candidate_minus_proxy_ap")}; args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"candidate": result["candidate"], "support_aggregate": result["support"], "probe_aggregate": result["probe_aggregate"], "delta_aggregate": result["delta_aggregate"]}, indent=2))


if __name__ == "__main__": main()
