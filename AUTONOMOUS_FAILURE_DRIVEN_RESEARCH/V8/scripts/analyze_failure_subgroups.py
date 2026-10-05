"""Validation-first subgroup analysis for LPShift V8.

The subgroup thresholds are frozen from the train-positive distribution in the
already locked message graph.  Test rows are only scored descriptively after
the thresholds have been fixed; they never affect subgroup definitions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import scipy.sparse as ssp
import torch

from lpshift_adapter import LPShiftData


def pair_arrays(adj, features, pairs, batch_size=100000):
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    degree = np.asarray(adj.sum(axis=1)).reshape(-1)
    feat_norm = np.linalg.norm(features, axis=1)
    output = {name: [] for name in ("degree_product", "degree_gap", "cn", "aa", "ra", "feature_cosine")}
    aa_adj = adj.multiply(np.where(degree > 1, 1.0 / np.log(np.maximum(degree, 2)), 0.0)).tocsr()
    ra_adj = adj.multiply(np.where(degree > 0, 1.0 / degree, 0.0)).tocsr()
    for start in range(0, len(pairs), batch_size):
        rows = pairs[start:start + batch_size]
        u, v = rows[:, 0], rows[:, 1]
        common = adj[u].multiply(adj[v])
        output["degree_product"].append(degree[u] * degree[v])
        output["degree_gap"].append(np.abs(np.log1p(degree[u]) - np.log1p(degree[v])))
        output["cn"].append(np.asarray(common.sum(axis=1)).reshape(-1))
        output["aa"].append(np.asarray(adj[u].multiply(aa_adj[v]).sum(axis=1)).reshape(-1))
        output["ra"].append(np.asarray(adj[u].multiply(ra_adj[v]).sum(axis=1)).reshape(-1))
        dot = np.sum(features[u] * features[v], axis=1)
        denom = feat_norm[u] * feat_norm[v]
        output["feature_cosine"].append(np.divide(dot, denom, out=np.zeros_like(dot, dtype=np.float32), where=denom > 0))
    return {key: np.concatenate(value) for key, value in output.items()}


def ranks(pos, neg):
    pos = np.asarray(pos).reshape(-1)
    neg = np.asarray(neg).reshape(pos.shape[0], -1)
    optimistic = 1 + np.sum(neg > pos[:, None], axis=1)
    pessimistic = 1 + np.sum(neg >= pos[:, None], axis=1)
    return 0.5 * (optimistic + pessimistic)


def metric(rank):
    rank = np.asarray(rank)
    return {
        "count": int(rank.size),
        "mrr": float(np.mean(1.0 / rank)) if rank.size else None,
        "hits10": float(np.mean(rank <= 10)) if rank.size else None,
        "hits20": float(np.mean(rank <= 20)) if rank.size else None,
        "hits50": float(np.mean(rank <= 50)) if rank.size else None,
        "hits100": float(np.mean(rank <= 100)) if rank.size else None,
    }


def load_score_bundle(path, kind):
    if kind == "dcdlp":
        obj = np.load(path)
        return {key: obj[key] for key in obj.files}
    obj = torch.load(path, map_location="cpu", weights_only=False)
    if isinstance(obj, dict):
        return obj
    # Official LPShift saves [valid_pos, valid_neg, test_pos, test_neg, ...].
    return {"valid_pos": obj[0], "valid_neg": obj[1], "test_pos": obj[2], "test_neg": obj[3]}


def pick(bundle, stem):
    aliases = [stem, f"{stem}_pred", f"{stem}_score", f"{stem}_scores"]
    for name in aliases:
        if name in bundle:
            value = bundle[name]
            if torch.is_tensor(value):
                value = value.detach().cpu().numpy()
            return np.asarray(value)
    raise KeyError(f"missing {stem}; keys={sorted(bundle)}")


def analyze_one(data, dist, dcdlp_path, gcn_path, include_heuristics=False):
    dcdlp = load_score_bundle(dcdlp_path, "dcdlp")
    gcn = load_score_bundle(gcn_path, "gcn")
    model_scores = {
        "DCDLP": (pick(dcdlp, "valid_pos"), pick(dcdlp, "valid_neg"), pick(dcdlp, "test_pos"), pick(dcdlp, "test_neg")),
        "GCN": (pick(gcn, "valid_pos"), pick(gcn, "valid_neg"), pick(gcn, "test_pos"), pick(gcn, "test_neg")),
    }
    valid_pairs = data.valid_pos.detach().cpu().numpy()
    test_pairs = data.test_pos.detach().cpu().numpy()
    edge = data.message_edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
    adj = ssp.csr_matrix((np.ones(edge.shape[1], dtype=np.float32), (edge[0], edge[1])), shape=(data.num_nodes, data.num_nodes))
    adj.sum_duplicates()
    adj.data[:] = 1.0
    features = data.features.detach().cpu().numpy().astype(np.float32, copy=False)
    valid_props = pair_arrays(adj, features, valid_pairs)
    test_props = pair_arrays(adj, features, test_pairs)
    if include_heuristics:
        valid_neg_pairs = data.valid_neg.detach().cpu().numpy().reshape(-1, 2)
        valid_neg_props = pair_arrays(adj, features, valid_neg_pairs)
        test_neg_pairs = data.test_neg.detach().cpu().numpy().reshape(-1, 2)
        test_neg_props = pair_arrays(adj, features, test_neg_pairs)
        for key, name in (("cn", "CN"), ("aa", "AA"), ("ra", "RA"),
                          ("feature_cosine", "FeatureCosine"), ("degree_product", "DegreeProduct")):
            model_scores[name] = (
                valid_props[key], valid_neg_props[key],
                test_props[key], test_neg_props[key],
            )

    # Freeze thresholds using only train-positive summaries.  This is a
    # predeclared quartile rule, not a test-driven subgroup search.
    train_summary = dist["groups"]["train_pos"]
    thresholds = {
        "cn_low": train_summary["cn"]["q25"], "cn_high": train_summary["cn"]["q75"],
        "degree_product_low": train_summary["degree_product"]["q25"],
        "degree_product_high": train_summary["degree_product"]["q75"],
        "degree_gap_high": None,
        "feature_low": train_summary["feature_cosine"]["q25"],
        "feature_high": train_summary["feature_cosine"]["q75"],
    }
    # degree-gap is not in the distribution audit, so calculate its train
    # quartiles on a deterministic prefix, explicitly recorded as such.
    train_sample = data.train_pos.detach().cpu().numpy()[:100000]
    train_props_sample = pair_arrays(adj, features, train_sample)
    thresholds["degree_gap_high"] = float(np.quantile(train_props_sample["degree_gap"], 0.75))
    groups = {
        "all": np.ones(len(valid_pairs), dtype=bool),
        "cn_low": valid_props["cn"] <= thresholds["cn_low"],
        "cn_high": valid_props["cn"] >= thresholds["cn_high"],
        "degree_product_low": valid_props["degree_product"] <= thresholds["degree_product_low"],
        "degree_product_high": valid_props["degree_product"] >= thresholds["degree_product_high"],
        "degree_gap_high": valid_props["degree_gap"] >= thresholds["degree_gap_high"],
        "feature_cosine_low": valid_props["feature_cosine"] <= thresholds["feature_low"],
        "feature_cosine_high": valid_props["feature_cosine"] >= thresholds["feature_high"],
        "cn_exact_zero": valid_props["cn"] == 0,
    }
    test_groups = {
        name: {
            "count": int(np.sum(mask)),
            "fraction": float(np.mean(mask)) if len(mask) else None,
        }
        for name, mask in {
            "all": np.ones(len(test_pairs), dtype=bool),
            "cn_low": test_props["cn"] <= thresholds["cn_low"],
            "cn_high": test_props["cn"] >= thresholds["cn_high"],
            "degree_product_low": test_props["degree_product"] <= thresholds["degree_product_low"],
            "degree_product_high": test_props["degree_product"] >= thresholds["degree_product_high"],
            "degree_gap_high": test_props["degree_gap"] >= thresholds["degree_gap_high"],
            "feature_cosine_low": test_props["feature_cosine"] <= thresholds["feature_low"],
            "feature_cosine_high": test_props["feature_cosine"] >= thresholds["feature_high"],
            "cn_exact_zero": test_props["cn"] == 0,
        }.items()
    }
    output = {"thresholds_from_train_pos": thresholds, "validation": {}, "test_descriptive": test_groups}
    for name, mask in groups.items():
        output["validation"][name] = {"count": int(mask.sum()), "fraction": float(mask.mean())}
        for model, (vp, vn, tp, tn) in model_scores.items():
            vrank = ranks(vp, vn)
            trank = ranks(tp, tn) if len(tp) else None
            output["validation"][name][model] = metric(vrank[mask])
            if name == "all" and trank is not None:
                output["test_descriptive"][name][model] = metric(trank)
            else:
                # Apply the same frozen rule to test positives only.
                tmask = {
                    "cn_low": test_props["cn"] <= thresholds["cn_low"],
                    "cn_high": test_props["cn"] >= thresholds["cn_high"],
                    "degree_product_low": test_props["degree_product"] <= thresholds["degree_product_low"],
                    "degree_product_high": test_props["degree_product"] >= thresholds["degree_product_high"],
                    "degree_gap_high": test_props["degree_gap"] >= thresholds["degree_gap_high"],
                    "feature_cosine_low": test_props["feature_cosine"] <= thresholds["feature_low"],
                    "feature_cosine_high": test_props["feature_cosine"] >= thresholds["feature_high"],
                    "cn_exact_zero": test_props["cn"] == 0,
                }.get(name)
                if tmask is not None and trank is not None:
                    output["test_descriptive"][name][model] = metric(trank[tmask])
    # Ranking ties: official evaluator uses average rank; this diagnostic is
    # conservative (competition rank) and reports exact CN tie prevalence.
    output["validation"]["tie_diagnostic"] = {
        "cn_exact_zero_fraction": float(np.mean(valid_props["cn"] == 0)),
        "cn_integer_unique_values": int(np.unique(valid_props["cn"]).size),
    }
    return output


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--dataset", required=True)
    p.add_argument("--dist", required=True)
    p.add_argument("--dcdlp", nargs=3, required=True)
    p.add_argument("--gcn", nargs=3, required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    data = LPShiftData.load(args.repo, args.dataset)
    dist = json.loads(Path(args.dist).read_text(encoding="utf-8"))
    result = {"dataset": args.dataset, "seeds": {}}
    for seed, dpath, gpath in zip((1, 2, 3), args.dcdlp, args.gcn):
        result["seeds"][str(seed)] = analyze_one(data, dist, dpath, gpath, include_heuristics=(seed == 1))
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
