"""Stage-0/Stage-1 audit for a fixed community-boundary profile."""

from __future__ import annotations

import argparse
import json
import math
import os
from collections import defaultdict
from pathlib import Path

import networkx as nx
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


def community_labels(adj):
    graph = nx.Graph(); graph.add_nodes_from(range(len(adj)))
    graph.add_edges_from((u, v) for u, ns in enumerate(adj) for v in ns if u < v)
    communities = list(nx.community.asyn_lpa_communities(graph, weight=None, seed=20260916))
    labels = np.full(len(adj), -1, dtype=np.int64); sizes = {}
    for index, nodes in enumerate(communities):
        for node in nodes: labels[node] = index
        sizes[index] = len(nodes)
    return labels, sizes


def pair_object(adj, labels, sizes, u, v):
    cu, cv = int(labels[u]), int(labels[v]); nu, nv = adj[u], adj[v]
    u_in = sum(1 for x in nu if labels[x] == cu); v_in = sum(1 for x in nv if labels[x] == cv); u_out, v_out = len(nu) - u_in, len(nv) - v_in
    union_communities = len({int(labels[x]) for x in (nu | nv)})
    profile = np.asarray([float(cu == cv), float(u_in), float(v_in), float(u_out), float(v_out), float(u_out / max(1, len(nu))), float(v_out / max(1, len(nv))), float(abs(sizes.get(cu, 0) - sizes.get(cv, 0))), float(union_communities)], dtype=np.float64)
    common = (nu & nv) - {u, v}; l3 = 0; first, second = (nu, nv) if len(nu) <= len(nv) else (nv, nu)
    for a in first: l3 += sum(1 for b in adj[a] if b in second and a != v and b != u and a != b)
    aa = sum(1.0 / math.log1p(len(adj[x])) for x in common); ra = sum(1.0 / max(1, len(adj[x])) for x in common)
    return {"cn": float(len(common)), "aa": float(aa), "ra": float(ra), "degree_product": float(len(nu) * len(nv)), "l3": float(l3), "local_path": float(len(common) + 0.01 * l3), "community": profile}


def sample_train_negatives(all_positive, n, seed, count):
    known = {tuple(sorted((int(x), int(y)))) for x, y in all_positive}; rng = np.random.default_rng(10000 + seed); negatives = []
    while len(negatives) < count:
        u, v = int(rng.integers(n)), int(rng.integers(n))
        if u == v: continue
        pair = tuple(sorted((u, v)))
        if pair not in known: known.add(pair); negatives.append(pair)
    return np.asarray(negatives, dtype=np.int64)


def scalar_matrix(values): return np.asarray([[float(x["cn"]), float(x["aa"]), float(x["ra"]), math.log1p(float(x["degree_product"])), float(x["l3"]), float(x["local_path"])] for x in values], dtype=np.float64)
def object_matrix(values): return np.asarray([np.asarray(x["community"], dtype=np.float64) for x in values])
def compute(adj, labels, sizes, pairs):
    start = os.times().elapsed; values = [pair_object(adj, labels, sizes, int(u), int(v)) for u, v in pairs]; return values, float(os.times().elapsed - start)
def fit(train_x, train_y, valid_x, valid_y):
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, solver="liblinear")); model.fit(train_x, train_y); score = model.predict_proba(valid_x)[:, 1]; return {"auc": float(roc_auc_score(valid_y, score)), "ap": float(average_precision_score(valid_y, score))}
def shuffle(values, scalar, seed):
    rng = np.random.default_rng(seed); out = values.copy(); strata = defaultdict(list)
    for i, row in enumerate(scalar): strata[(float(round(row[0], 3)), float(round(row[4], 3)), float(round(row[3], 3)))].append(i)
    for indices in strata.values():
        if len(indices) > 1: out[indices] = values[rng.permutation(np.asarray(indices, dtype=np.int64))]
    return out


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--data-root", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4]); args = parser.parse_args(); result = {"candidate": "R4-13 Multi-Scale Community Boundary Profile", "support": [], "probes": []}
    for seed in args.seeds:
        data = np.load(args.data_root / f"cora_heart_seed{seed}.npz", allow_pickle=False); adj = build_adjacency(np.asarray(data["train_pos"], dtype=np.int64), int(data["num_nodes"])); labels, sizes = community_labels(adj)
        for label, pairs in ((1, np.asarray(data["test_pos"], dtype=np.int64)), (0, np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2))):
            values, seconds = compute(adj, labels, sizes, pairs); obj = object_matrix(values); result["support"].append({"seed": seed, "label": label, "total": int(len(pairs)), "same_community": int(np.sum(obj[:, 0] > 0)), "nonzero": int(np.sum(obj[:, 1:].sum(axis=1) > 0)), "extract_seconds": seconds})
        train_pos = np.asarray(data["train_pos"], dtype=np.int64); train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), int(data["num_nodes"]), seed, len(train_pos)); valid_pos = np.asarray(data["valid_pos"], dtype=np.int64); valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]; train_pairs = np.concatenate([train_pos, train_neg]); valid_pairs = np.concatenate([valid_pos, valid_neg]); train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))]; valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))]
        train_values, _ = compute(adj, labels, sizes, train_pairs); valid_values, _ = compute(adj, labels, sizes, valid_pairs); train_scalar, valid_scalar = scalar_matrix(train_values), scalar_matrix(valid_values); train_obj, valid_obj = object_matrix(train_values), object_matrix(valid_values); train_shuf, valid_shuf = shuffle(train_obj, train_scalar, 20000 + seed), shuffle(valid_obj, valid_scalar, 30000 + seed); matrices = {"Base": (train_scalar[:, :4], valid_scalar[:, :4]), "DangerousControls": (train_scalar, valid_scalar), "TrueCommunity": (np.c_[train_scalar, train_obj], np.c_[valid_scalar, valid_obj]), "ShuffledCommunity": (np.c_[train_scalar, train_shuf], np.c_[valid_scalar, valid_shuf])}; metrics = {name: fit(x, train_y, y, valid_y) for name, (x, y) in matrices.items()}
        proxy_train = np.c_[np.log1p(np.maximum(train_scalar[:, 4], 0)), np.sqrt(np.maximum(train_scalar[:, 4], 0)), np.log1p(np.maximum(train_scalar[:, 0], 0)), np.sqrt(np.maximum(train_scalar[:, 0], 0)), train_scalar[:, 3], train_scalar[:, 3] ** 2, np.log1p(np.maximum(train_scalar[:, 5], 0)), np.sin(np.minimum(train_scalar[:, 4], 20)), np.cos(np.minimum(train_scalar[:, 4], 20))]; proxy_valid = np.c_[np.log1p(np.maximum(valid_scalar[:, 4], 0)), np.sqrt(np.maximum(valid_scalar[:, 4], 0)), np.log1p(np.maximum(valid_scalar[:, 0], 0)), np.sqrt(np.maximum(valid_scalar[:, 0], 0)), valid_scalar[:, 3], valid_scalar[:, 3] ** 2, np.log1p(np.maximum(valid_scalar[:, 5], 0)), np.sin(np.minimum(valid_scalar[:, 4], 20)), np.cos(np.minimum(valid_scalar[:, 4], 20))]; metrics["Proxy"] = fit(np.c_[train_scalar, proxy_train], train_y, np.c_[valid_scalar, proxy_valid], valid_y)
        result["probes"].append({"seed": seed, "metrics": metrics, "candidate_minus_controls_auc": metrics["TrueCommunity"]["auc"] - metrics["DangerousControls"]["auc"], "candidate_minus_shuffled_auc": metrics["TrueCommunity"]["auc"] - metrics["ShuffledCommunity"]["auc"], "candidate_minus_proxy_auc": metrics["TrueCommunity"]["auc"] - metrics["Proxy"]["auc"], "candidate_minus_controls_ap": metrics["TrueCommunity"]["ap"] - metrics["DangerousControls"]["ap"], "candidate_minus_shuffled_ap": metrics["TrueCommunity"]["ap"] - metrics["ShuffledCommunity"]["ap"], "candidate_minus_proxy_ap": metrics["TrueCommunity"]["ap"] - metrics["Proxy"]["ap"]})
    result["support_aggregate"] = {}
    for label in (1, 0):
        rows = [x for x in result["support"] if x["label"] == label]; total = sum(x["total"] for x in rows); result["support_aggregate"][str(label)] = {"total": total, "same_community": sum(x["same_community"] for x in rows), "nonzero": sum(x["nonzero"] for x in rows)}
    result["probe_aggregate"] = {}
    for name in ("Base", "DangerousControls", "TrueCommunity", "ShuffledCommunity", "Proxy"):
        rows = [x["metrics"][name] for x in result["probes"]]; result["probe_aggregate"][name] = {"auc_mean": float(np.mean([x["auc"] for x in rows])), "auc_std": float(np.std([x["auc"] for x in rows], ddof=1)), "ap_mean": float(np.mean([x["ap"] for x in rows])), "ap_std": float(np.std([x["ap"] for x in rows], ddof=1))}
    result["delta_aggregate"] = {key: float(np.mean([x[key] for x in result["probes"]])) for key in ("candidate_minus_controls_auc", "candidate_minus_shuffled_auc", "candidate_minus_proxy_auc", "candidate_minus_controls_ap", "candidate_minus_shuffled_ap", "candidate_minus_proxy_ap")}; args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"candidate": result["candidate"], "support_aggregate": result["support_aggregate"], "probe_aggregate": result["probe_aggregate"], "delta_aggregate": result["delta_aggregate"]}, indent=2))


if __name__ == "__main__": main()
