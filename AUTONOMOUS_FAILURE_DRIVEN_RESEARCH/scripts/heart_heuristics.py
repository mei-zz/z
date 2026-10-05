from __future__ import annotations

import argparse
import json
from pathlib import Path

import networkx as nx
import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

from dcdlp.data.loaders import load_dataset
from dcdlp.data.negative_sampling import uniform_negative_sampling
from dcdlp.data.pair_statistics import ConditionalCNRegressor, assign_quadrants, pair_features
from dcdlp.evaluation.ranking import ranking_metrics


def score_pairs(graph: nx.Graph, pairs: np.ndarray, features: np.ndarray) -> dict[str, np.ndarray]:
    stats = pair_features(graph, pairs, features)
    return {
        "cn": stats["cn"].astype(float),
        "aa": stats["aa"].astype(float),
        "ra": stats["ra"].astype(float),
        "jaccard": stats["jaccard"].astype(float),
        "degree_product": stats["degree_product"].astype(float),
        "feature_similarity": np.nan_to_num(stats["feature_similarity"].astype(float), nan=0.0),
    }


def evaluate(name: str, positive: np.ndarray, negatives: np.ndarray, pos_scores: np.ndarray, neg_scores: np.ndarray) -> dict:
    out = ranking_metrics(pos_scores, neg_scores)
    labels = np.concatenate([np.ones(len(pos_scores)), np.zeros(neg_scores.size)])
    scores = np.concatenate([pos_scores, neg_scores.reshape(-1)])
    out["auc"] = float(roc_auc_score(labels, scores))
    out["ap"] = float(average_precision_score(labels, scores))
    out["positive_count"] = int(len(positive))
    out["negative_count"] = int(negatives.size)
    return out


def grouped_mrr(pos_scores: np.ndarray, neg_scores: np.ndarray, groups: np.ndarray) -> dict[str, float]:
    reciprocal = 1.0 / (1.0 + (neg_scores > pos_scores[:, None]).sum(axis=1))
    return {
        group: float(reciprocal[groups == group].mean())
        for group in ("HH", "HL", "LH", "LL")
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dataset", default="cora")
    parser.add_argument("--protocol", default="heart")
    args = parser.parse_args()

    dataset = load_dataset(args.dataset, args.data_root, args.protocol, 0)
    graph = dataset.train_graph()
    train_neg = uniform_negative_sampling(
        dataset.num_nodes, dataset.all_positive, len(dataset.train_pos), seed=0
    )
    train_stats = pair_features(graph, np.vstack([dataset.train_pos, train_neg]), dataset.features)
    regressor = ConditionalCNRegressor(seed=0, symmetric=True).fit(train_stats)
    train_degree_threshold = float(np.median(train_stats["degree_score"]))
    results = {
        "dataset": args.dataset,
        "protocol": args.protocol,
        "train_edge_count": int(len(dataset.train_pos)),
        "valid_edge_count": int(len(dataset.valid_pos)),
        "test_edge_count": int(len(dataset.test_pos)),
        "methods": {},
    }
    for method in ("cn", "aa", "ra", "jaccard", "degree_product", "feature_similarity"):
        results["methods"][method] = {}
        for split, positives, negatives in (
            ("valid", dataset.valid_pos, dataset.valid_neg),
            ("test", dataset.test_pos, dataset.test_neg),
        ):
            target_stats = pair_features(graph, positives, dataset.features)
            _, residual = regressor.residual(target_stats)
            groups = assign_quadrants(target_stats["degree_score"], residual, train_degree_threshold)
            pos = score_pairs(graph, positives, dataset.features)[method]
            flat_neg = np.asarray(negatives).reshape(-1, 2)
            neg = score_pairs(graph, flat_neg, dataset.features)[method].reshape(len(positives), -1)
            metrics = evaluate(method, positives, negatives, pos, neg)
            metrics["groups_mrr"] = grouped_mrr(pos, neg, groups)
            metrics["group_counts"] = {
                group: int((groups == group).sum()) for group in ("HH", "HL", "LH", "LL")
            }
            results["methods"][method][split] = metrics
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
