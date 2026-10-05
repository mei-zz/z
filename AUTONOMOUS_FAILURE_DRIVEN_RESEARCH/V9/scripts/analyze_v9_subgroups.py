"""Validation-first subgroup metrics for V9 attribution controls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import scipy.sparse as ssp
import torch

from lpshift_adapter import LPShiftData


def props(adj, features, pairs, batch_size=100000):
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    degree = np.asarray(adj.sum(axis=1)).reshape(-1)
    norm = np.linalg.norm(features, axis=1)
    out = {k: [] for k in ("degree_product", "degree_gap", "cn", "feature_cosine")}
    for start in range(0, len(pairs), batch_size):
        rows = pairs[start:start + batch_size]
        u, v = rows[:, 0], rows[:, 1]
        common = adj[u].multiply(adj[v])
        out["degree_product"].append(degree[u] * degree[v])
        out["degree_gap"].append(np.abs(np.log1p(degree[u]) - np.log1p(degree[v])))
        out["cn"].append(np.asarray(common.sum(axis=1)).reshape(-1))
        dot = np.sum(features[u] * features[v], axis=1)
        denom = norm[u] * norm[v]
        out["feature_cosine"].append(np.divide(dot, denom, out=np.zeros_like(dot, dtype=np.float32), where=denom > 0))
    return {k: np.concatenate(v) for k, v in out.items()}


def ranks(pos, neg):
    pos = np.asarray(pos).reshape(-1)
    neg = np.asarray(neg).reshape(len(pos), -1)
    optimistic = 1 + np.sum(neg > pos[:, None], axis=1)
    pessimistic = 1 + np.sum(neg >= pos[:, None], axis=1)
    return 0.5 * (optimistic + pessimistic)


def metric(rank):
    rank = np.asarray(rank)
    return {"count": int(len(rank)), "mrr": float(np.mean(1.0 / rank)),
            "hits10": float(np.mean(rank <= 10)), "hits20": float(np.mean(rank <= 20)),
            "hits50": float(np.mean(rank <= 50)), "hits100": float(np.mean(rank <= 100))}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--dataset", required=True)
    p.add_argument("--dist", required=True)
    p.add_argument("--results", nargs=3, required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    data = LPShiftData.load(args.repo, args.dataset)
    edge = data.message_edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
    adj = ssp.csr_matrix((np.ones(edge.shape[1], dtype=np.float32), (edge[0], edge[1])), shape=(data.num_nodes, data.num_nodes))
    adj.sum_duplicates(); adj.data[:] = 1.0
    features = data.features.detach().cpu().numpy().astype(np.float32, copy=False)
    valid_pos = data.valid_pos.detach().cpu().numpy()
    valid_neg = data.valid_neg.detach().cpu().numpy()
    test_pos = data.test_pos.detach().cpu().numpy()
    test_neg = data.test_neg.detach().cpu().numpy()
    valid_props = props(adj, features, valid_pos)
    test_props = props(adj, features, test_pos)
    dist = json.loads(Path(args.dist).read_text(encoding="utf-8"))
    train = dist["groups"]["train_pos"]
    train_sample = data.train_pos.detach().cpu().numpy()[:100000]
    train_gap = props(adj, features, train_sample)["degree_gap"]
    thresholds = {
        "cn_low": train["cn"]["q25"], "cn_high": train["cn"]["q75"],
        "degree_product_low": train["degree_product"]["q25"],
        "degree_product_high": train["degree_product"]["q75"],
        "degree_gap_high": float(np.quantile(train_gap, 0.75)),
        "feature_low": train["feature_cosine"]["q25"],
        "feature_high": train["feature_cosine"]["q75"],
    }
    group_valid = {
        "all": np.ones(len(valid_pos), dtype=bool),
        "cn_zero": valid_props["cn"] == 0,
        "cn_low": valid_props["cn"] <= thresholds["cn_low"],
        "cn_high": valid_props["cn"] >= thresholds["cn_high"],
        "degree_product_low": valid_props["degree_product"] <= thresholds["degree_product_low"],
        "degree_product_high": valid_props["degree_product"] >= thresholds["degree_product_high"],
        "degree_gap_high": valid_props["degree_gap"] >= thresholds["degree_gap_high"],
        "feature_cosine_low": valid_props["feature_cosine"] <= thresholds["feature_low"],
        "feature_cosine_high": valid_props["feature_cosine"] >= thresholds["feature_high"],
    }
    group_test = {
        "all": np.ones(len(test_pos), dtype=bool),
        "cn_zero": test_props["cn"] == 0,
        "cn_low": test_props["cn"] <= thresholds["cn_low"],
        "cn_high": test_props["cn"] >= thresholds["cn_high"],
        "degree_product_low": test_props["degree_product"] <= thresholds["degree_product_low"],
        "degree_product_high": test_props["degree_product"] >= thresholds["degree_product_high"],
        "degree_gap_high": test_props["degree_gap"] >= thresholds["degree_gap_high"],
        "feature_cosine_low": test_props["feature_cosine"] <= thresholds["feature_low"],
        "feature_cosine_high": test_props["feature_cosine"] >= thresholds["feature_high"],
    }
    output = {"dataset": args.dataset, "thresholds_from_train_pos": thresholds, "seeds": {}}
    for seed, result_path in zip((1, 2, 3), args.results):
        result = json.loads(Path(result_path).read_text(encoding="utf-8"))
        seed_out = {"validation": {}, "test_descriptive": {}}
        for model_name, info in result["models"].items():
            bundle = np.load(info["prediction_file"])
            vp, vn = bundle["valid_pos"], bundle["valid_neg"]
            tp, tn = bundle["test_pos"], bundle["test_neg"]
            vrank = ranks(vp, vn); trank = ranks(tp, tn)
            seed_out["validation"][model_name] = {}
            seed_out["test_descriptive"][model_name] = {}
            for group, mask in group_valid.items():
                seed_out["validation"][model_name][group] = metric(vrank[mask])
            for group, mask in group_test.items():
                seed_out["test_descriptive"][model_name][group] = metric(trank[mask])
        output["seeds"][str(seed)] = seed_out
    Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
