"""Compute train/validation/test structural and feature distributions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import scipy.sparse as ssp
import torch

from lpshift_adapter import LPShiftData


def summarize(values: np.ndarray) -> dict:
    values = np.asarray(values, dtype=np.float64)
    return {
        "count": int(values.size),
        "mean": float(values.mean()) if values.size else None,
        "std": float(values.std()) if values.size else None,
        "q01": float(np.quantile(values, 0.01)) if values.size else None,
        "q10": float(np.quantile(values, 0.10)) if values.size else None,
        "q25": float(np.quantile(values, 0.25)) if values.size else None,
        "q50": float(np.quantile(values, 0.50)) if values.size else None,
        "q75": float(np.quantile(values, 0.75)) if values.size else None,
        "q90": float(np.quantile(values, 0.90)) if values.size else None,
        "q99": float(np.quantile(values, 0.99)) if values.size else None,
        "zero_fraction": float(np.mean(values == 0)) if values.size else None,
    }


def pair_values(adj, features, pairs, batch_size=100000):
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    degree = np.asarray(adj.sum(axis=1)).reshape(-1)
    aa_adj = adj.multiply(np.where(degree > 1, 1.0 / np.log(np.maximum(degree, 2)), 0.0)).tocsr()
    ra_adj = adj.multiply(np.where(degree > 0, 1.0 / degree, 0.0)).tocsr()
    feat_norm = np.linalg.norm(features, axis=1)
    output = {name: [] for name in ("degree_u", "degree_v", "degree_min", "degree_max", "degree_product", "cn", "aa", "ra", "feature_cosine")}
    for start in range(0, len(pairs), batch_size):
        rows = pairs[start:start + batch_size]
        u, v = rows[:, 0], rows[:, 1]
        common = adj[u].multiply(adj[v])
        output["degree_u"].append(degree[u])
        output["degree_v"].append(degree[v])
        output["degree_min"].append(np.minimum(degree[u], degree[v]))
        output["degree_max"].append(np.maximum(degree[u], degree[v]))
        output["degree_product"].append(degree[u] * degree[v])
        output["cn"].append(np.asarray(common.sum(axis=1)).reshape(-1))
        output["aa"].append(np.asarray(adj[u].multiply(aa_adj[v]).sum(axis=1)).reshape(-1))
        output["ra"].append(np.asarray(adj[u].multiply(ra_adj[v]).sum(axis=1)).reshape(-1))
        dot = np.sum(features[u] * features[v], axis=1)
        denom = feat_norm[u] * feat_norm[v]
        output["feature_cosine"].append(np.divide(dot, denom, out=np.zeros_like(dot, dtype=np.float32), where=denom > 0))
    return {name: summarize(np.concatenate(values)) for name, values in output.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--train-seeds", nargs="+", type=int, default=[1, 2, 3])
    args = parser.parse_args()
    adapter = LPShiftData.load(args.repo, args.dataset)
    edge = adapter.message_edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
    adj = ssp.csr_matrix((np.ones(edge.shape[1], dtype=np.float32), (edge[0], edge[1])), shape=(adapter.num_nodes, adapter.num_nodes))
    adj.sum_duplicates()
    adj.data[:] = 1.0
    features = adapter.features.detach().cpu().numpy().astype(np.float32, copy=False)
    result = {"dataset": args.dataset, "data_hashes": adapter.summary(), "groups": {}}
    result["groups"]["train_pos"] = pair_values(adj, features, adapter.train_pos.detach().cpu().numpy())
    result["groups"]["valid_pos"] = pair_values(adj, features, adapter.valid_pos.detach().cpu().numpy())
    result["groups"]["valid_neg"] = pair_values(adj, features, adapter.valid_neg.detach().cpu().numpy())
    result["groups"]["test_pos"] = pair_values(adj, features, adapter.test_pos.detach().cpu().numpy())
    result["groups"]["test_neg"] = pair_values(adj, features, adapter.test_neg.detach().cpu().numpy())
    for seed in args.train_seeds:
        # Reproduce the V8 DCDLP training-negative protocol without using any
        # held-out labels.  The sampler itself is run in the remote runner;
        # this audit records only the resulting distribution summary.
        from dcdlp.data.negative_sampling import uniform_negative_sampling
        forbidden = np.asarray(sorted(adapter.message_edge_keys()), dtype=np.int64)
        negative = uniform_negative_sampling(adapter.num_nodes, forbidden, len(adapter.train_pos), seed * 10000)
        result["groups"][f"train_neg_seed{seed}"] = pair_values(adj, features, negative)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
