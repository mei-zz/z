"""Stage-0/Stage-1 audit for exclusive-neighborhood internal cohesion."""

from __future__ import annotations

import argparse
import json
import math
import os
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_adjacency(edges, n):
    adj = [set() for _ in range(n)]
    for x, y in np.asarray(edges, dtype=np.int64):
        x, y = int(x), int(y)
        if x != y: adj[x].add(y); adj[y].add(x)
    return adj


def side_cohesion(adj, nodes):
    nodes = list(nodes); node_set = set(nodes); internal_degrees = np.asarray([len(adj[x] & node_set) for x in nodes], dtype=np.float64)
    edges = float(internal_degrees.sum() / 2.0); possible = len(nodes) * max(0, len(nodes) - 1) / 2.0
    return edges, edges / max(1.0, possible), float(internal_degrees.mean() if len(nodes) else 0), float(internal_degrees.std() if len(nodes) else 0)


def pair_object(adj, u, v):
    left, right = adj[u] - adj[v] - {v}, adj[v] - adj[u] - {u}; le, ld, lm, ls = side_cohesion(adj, left); re, rd, rm, rs = side_cohesion(adj, right)
    profile = np.asarray([le, re, ld, rd, abs(ld - rd), lm + rm, abs(lm - rm), ls + rs], dtype=np.float64)
    common = (adj[u] & adj[v]) - {u, v}; l3 = 0; first, second = (adj[u], adj[v]) if len(adj[u]) <= len(adj[v]) else (adj[v], adj[u])
    for a in first: l3 += sum(1 for b in adj[a] if b in second and a != v and b != u and a != b)
    aa = sum(1.0 / math.log1p(len(adj[x])) for x in common); ra = sum(1.0 / max(1, len(adj[x])) for x in common)
    return {"cn": float(len(common)), "aa": float(aa), "ra": float(ra), "degree_product": float(len(adj[u]) * len(adj[v])), "l3": float(l3), "local_path": float(len(common) + 0.01 * l3), "cohesion": profile}


def sample_train_negatives(all_positive, n, seed, count):
    known = {tuple(sorted((int(x), int(y)))) for x, y in all_positive}; rng = np.random.default_rng(10000 + seed); negatives = []
    while len(negatives) < count:
        u, v = int(rng.integers(n)), int(rng.integers(n))
        if u == v: continue
        pair = tuple(sorted((u, v)))
        if pair not in known: known.add(pair); negatives.append(pair)
    return np.asarray(negatives, dtype=np.int64)


def scalar_matrix(values): return np.asarray([[float(x["cn"]), float(x["aa"]), float(x["ra"]), math.log1p(float(x["degree_product"])), float(x["l3"]), float(x["local_path"])] for x in values], dtype=np.float64)
def object_matrix(values): return np.asarray([np.asarray(x["cohesion"], dtype=np.float64) for x in values])
def compute(adj, pairs):
    start = os.times().elapsed; values = [pair_object(adj, int(u), int(v)) for u, v in pairs]; return values, float(os.times().elapsed - start)
def fit(train_x, train_y, valid_x, valid_y):
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, solver="liblinear")); model.fit(train_x, train_y); score = model.predict_proba(valid_x)[:, 1]; return {"auc": float(roc_auc_score(valid_y, score)), "ap": float(average_precision_score(valid_y, score))}
def shuffle(values, scalar, seed):
    rng = np.random.default_rng(seed); out = values.copy(); strata = defaultdict(list)
    for i, row in enumerate(scalar): strata[(float(round(row[0], 3)), float(round(row[4], 3)), float(round(row[3], 3)))].append(i)
    for indices in strata.values():
        if len(indices) > 1: out[indices] = values[rng.permutation(np.asarray(indices, dtype=np.int64))]
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--data-root", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4]); args = parser.parse_args(); result = {"candidate": "R4-12 Exclusive-Neighborhood Cohesion Profile", "support": [], "probes": []}
    for seed in args.seeds:
        data = np.load(args.data_root / f"cora_heart_seed{seed}.npz", allow_pickle=False); adj = build_adjacency(np.asarray(data["train_pos"], dtype=np.int64), int(data["num_nodes"]))
        for label, pairs in ((1, np.asarray(data["test_pos"], dtype=np.int64)), (0, np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2))):
            values, seconds = compute(adj, pairs); obj = object_matrix(values); result["support"].append({"seed": seed, "label": label, "total": int(len(pairs)), "nonzero": int(np.sum(obj[:, :2].sum(axis=1) > 0)), "mean_internal_edges": float(np.mean(obj[:, 0] + obj[:, 1])), "extract_seconds": seconds})
        train_pos = np.asarray(data["train_pos"], dtype=np.int64); train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), int(data["num_nodes"]), seed, len(train_pos)); valid_pos = np.asarray(data["valid_pos"], dtype=np.int64); valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]; train_pairs = np.concatenate([train_pos, train_neg]); valid_pairs = np.concatenate([valid_pos, valid_neg]); train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))]; valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))]
        train_values, _ = compute(adj, train_pairs); valid_values, _ = compute(adj, valid_pairs); train_scalar, valid_scalar = scalar_matrix(train_values), scalar_matrix(valid_values); train_obj, valid_obj = object_matrix(train_values), object_matrix(valid_values); train_shuf, valid_shuf = shuffle(train_obj, train_scalar, 20000 + seed), shuffle(valid_obj, valid_scalar, 30000 + seed); matrices = {"Base": (train_scalar[:, :4], valid_scalar[:, :4]), "DangerousControls": (train_scalar, valid_scalar), "TrueCohesion": (np.c_[train_scalar, train_obj], np.c_[valid_scalar, valid_obj]), "ShuffledCohesion": (np.c_[train_scalar, train_shuf], np.c_[valid_scalar, valid_shuf])}; metrics = {name: fit(x, train_y, y, valid_y) for name, (x, y) in matrices.items()}
        proxy_train = np.c_[np.log1p(np.maximum(train_scalar[:, 4], 0)), np.sqrt(np.maximum(train_scalar[:, 4], 0)), np.log1p(np.maximum(train_scalar[:, 0], 0)), np.sqrt(np.maximum(train_scalar[:, 0], 0)), train_scalar[:, 3], train_scalar[:, 3] ** 2, np.log1p(np.maximum(train_scalar[:, 5], 0)), np.sin(np.minimum(train_scalar[:, 4], 20)), np.cos(np.minimum(train_scalar[:, 4], 20))]; proxy_valid = np.c_[np.log1p(np.maximum(valid_scalar[:, 4], 0)), np.sqrt(np.maximum(valid_scalar[:, 4], 0)), np.log1p(np.maximum(valid_scalar[:, 0], 0)), np.sqrt(np.maximum(valid_scalar[:, 0], 0)), valid_scalar[:, 3], valid_scalar[:, 3] ** 2, np.log1p(np.maximum(valid_scalar[:, 5], 0)), np.sin(np.minimum(valid_scalar[:, 4], 20)), np.cos(np.minimum(valid_scalar[:, 4], 20))]; metrics["Proxy"] = fit(np.c_[train_scalar, proxy_train], train_y, np.c_[valid_scalar, proxy_valid], valid_y)
        result["probes"].append({"seed": seed, "metrics": metrics, "candidate_minus_controls_auc": metrics["TrueCohesion"]["auc"] - metrics["DangerousControls"]["auc"], "candidate_minus_shuffled_auc": metrics["TrueCohesion"]["auc"] - metrics["ShuffledCohesion"]["auc"], "candidate_minus_proxy_auc": metrics["TrueCohesion"]["auc"] - metrics["Proxy"]["auc"], "candidate_minus_controls_ap": metrics["TrueCohesion"]["ap"] - metrics["DangerousControls"]["ap"], "candidate_minus_shuffled_ap": metrics["TrueCohesion"]["ap"] - metrics["ShuffledCohesion"]["ap"], "candidate_minus_proxy_ap": metrics["TrueCohesion"]["ap"] - metrics["Proxy"]["ap"]})
    result["support_aggregate"] = {}
    for label in (1, 0):
        rows = [x for x in result["support"] if x["label"] == label]; total = sum(x["total"] for x in rows); result["support_aggregate"][str(label)] = {"total": total, "nonzero": sum(x["nonzero"] for x in rows), "mean_internal_edges": sum(x["mean_internal_edges"] * x["total"] for x in rows) / total}
    result["probe_aggregate"] = {}
    for name in ("Base", "DangerousControls", "TrueCohesion", "ShuffledCohesion", "Proxy"):
        rows = [x["metrics"][name] for x in result["probes"]]; result["probe_aggregate"][name] = {"auc_mean": float(np.mean([x["auc"] for x in rows])), "auc_std": float(np.std([x["auc"] for x in rows], ddof=1)), "ap_mean": float(np.mean([x["ap"] for x in rows])), "ap_std": float(np.std([x["ap"] for x in rows], ddof=1))}
    result["delta_aggregate"] = {key: float(np.mean([x[key] for x in result["probes"]])) for key in ("candidate_minus_controls_auc", "candidate_minus_shuffled_auc", "candidate_minus_proxy_auc", "candidate_minus_controls_ap", "candidate_minus_shuffled_ap", "candidate_minus_proxy_ap")}; args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"candidate": result["candidate"], "support_aggregate": result["support_aggregate"], "probe_aggregate": result["probe_aggregate"], "delta_aggregate": result["delta_aggregate"]}, indent=2))


if __name__ == "__main__": main()
