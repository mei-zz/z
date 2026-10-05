"""Audit fixed feature/topology proxies on the NodeDup inductive split.

This is an analysis script only. It adds no trainable model or GNN module.
It loads the official cached split, scores the official positive/negative
candidate groups, and applies the repository's average-rank convention.
"""
from __future__ import print_function

import argparse
import json
import math
import os
import random
import sys

import numpy as np
import torch


def cosine_score(x, u, v):
    a = x[u].float()
    b = x[v].float()
    den = torch.linalg.vector_norm(a) * torch.linalg.vector_norm(b)
    if float(den) == 0.0:
        return 0.0
    return float(torch.dot(a, b) / den)


def graph_stats(edge_index, n):
    adj = [set() for _ in range(n)]
    for u, v in edge_index.t().tolist():
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    deg = np.asarray([len(a) for a in adj], dtype=np.float64)
    return adj, deg


def pair_topology(adj, deg, u, v):
    common = adj[u].intersection(adj[v])
    cn = float(len(common))
    ra = sum(1.0 / max(deg[w], 1.0) for w in common)
    return cn, ra


def rank_metrics(pos, neg):
    pos = torch.as_tensor(pos, dtype=torch.float64).view(-1, 1)
    neg = torch.as_tensor(neg, dtype=torch.float64).view(1, -1)
    optimistic = (neg > pos).sum(dim=1).double()
    pessimistic = (neg >= pos).sum(dim=1).double()
    rank = 0.5 * (optimistic + pessimistic) + 1.0
    return {
        "mrr": float((1.0 / rank).mean()),
        "hits10": float((rank <= 10).double().mean()),
        "hits20": float((rank <= 20).double().mean()),
        "hits50": float((rank <= 50).double().mean()),
        "n_positive": int(pos.numel()),
    }


def evaluate(split, graph, x, degree_bucket):
    adj, deg = graph_stats(graph, x.size(0))
    accum = {}
    total = {k: 0.0 for k in ["mrr", "hits10", "hits20", "hits50"]}
    total_n = 0
    for node, record in split["new"].items():
        pos_e = record["positive"]
        neg_e = record["negative"]
        methods = {"feature_cosine": [[], []], "cn": [[], []], "ra": [[], []]}
        for group, edges in [(0, pos_e), (1, neg_e)]:
            for u, v in edges.t().tolist():
                methods["feature_cosine"][group].append(cosine_score(x, u, v))
                cn, ra = pair_topology(adj, deg, u, v)
                methods["cn"][group].append(cn)
                methods["ra"][group].append(ra)
        bucket = degree_bucket.get(str(node), 0)
        bucket = "0" if bucket == 0 else ("1-2" if bucket <= 2 else ">2")
        for name, (p, n) in methods.items():
            met = rank_metrics(p, n)
            if name not in accum:
                accum[name] = {"overall": {k: 0.0 for k in total}, "buckets": {}}
            if bucket not in accum[name]["buckets"]:
                accum[name]["buckets"][bucket] = {k: 0.0 for k in total}
                accum[name]["buckets"][bucket]["n_positive"] = 0
            for key in total:
                accum[name]["overall"][key] += met[key] * met["n_positive"]
                accum[name]["buckets"][bucket][key] += met[key] * met["n_positive"]
            accum[name]["overall"]["n_positive"] = accum[name]["overall"].get("n_positive", 0) + met["n_positive"]
            accum[name]["buckets"][bucket]["n_positive"] += met["n_positive"]
            total_n += met["n_positive"] if name == "feature_cosine" else 0
    for name in accum:
        n = float(accum[name]["overall"]["n_positive"])
        for key in total:
            accum[name]["overall"][key] /= n
        for bucket in accum[name]["buckets"]:
            bn = float(accum[name]["buckets"][bucket]["n_positive"])
            for key in total:
                accum[name]["buckets"][bucket][key] /= bn
    return accum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    os.chdir(args.repo)
    if args.repo not in sys.path:
        sys.path.insert(0, args.repo)

    # The cache is trusted local data produced by the official repository.
    old_load = torch.load
    torch.load = lambda *a, **k: old_load(*a, weights_only=False, **k)
    from utils import get_dataset

    path = os.path.join(args.data_dir, args.dataset + "-1.0-1.0-1.0-1.0-500neg-induc.pkl")
    cached = torch.load(path, map_location="cpu")
    training_data, inference_data, split_edge = cached
    dataset = get_dataset(args.data_dir, args.dataset)
    x = dataset[0].x.cpu()
    degree_path = os.path.join(args.data_dir, args.dataset + "-1.0-1.0-1.0-1.0-500neg-induc_dict.json")
    with open(degree_path, "r") as f:
        degree_bucket = json.load(f)
    result = {
        "dataset": args.dataset,
        "split_cache": os.path.abspath(path),
        "feature_shape": list(x.shape),
        "training_nodes": int(training_data.x.size(0)),
        "inference_nodes": int(inference_data.x.size(0)),
        "validation": evaluate(split_edge["valid"], training_data.edge_index.cpu(), x, degree_bucket),
        "test": evaluate(split_edge["test"], inference_data.edge_index.cpu(), x, degree_bucket),
        "protocol": {
            "negative_samples": 500,
            "split_seed": 234,
            "test_used_for_selection": False,
            "score_tie_rule": "official average rank",
        },
    }
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
