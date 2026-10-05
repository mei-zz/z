"""Stage-0/Stage-1 audit for a block-cut-tree route object.

The graph is decomposed using training positives only.  A candidate pair is
represented by its route through the block-cut forest: shared biconnected
block evidence, articulation incidence, route length, and a compact route
profile.  These are structural relations that are not supplied as CN/L3
counts or node embeddings.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import networkx as nx
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from audit_role_transition import build_adjacency, pair_object, sample_train_negatives, scalar_matrix  # noqa: E402


def build_route_index(edges: np.ndarray, n: int) -> dict:
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from((int(u), int(v)) for u, v in np.asarray(edges, dtype=np.int64))
    blocks = [set(block) for block in nx.biconnected_components(graph)]
    articulation = set(nx.articulation_points(graph))
    block_count = len(blocks)
    tree = nx.Graph()
    block_node = {index: n + index for index in range(block_count)}
    cut_node = {node: n + block_count + node for node in articulation}
    for index, block in enumerate(blocks):
        bnode = block_node[index]
        tree.add_node(bnode, kind="block", size=len(block))
        for node in block:
            if node in articulation:
                cnode = cut_node[node]
                tree.add_node(cnode, kind="cut", original=node)
                tree.add_edge(bnode, cnode)
    anchors = [None] * n
    membership = [[] for _ in range(n)]
    for index, block in enumerate(blocks):
        for node in block:
            membership[node].append(index)
    for node in range(n):
        if node in articulation:
            anchors[node] = cut_node[node]
        elif membership[node]:
            anchors[node] = block_node[membership[node][0]]
        else:
            isolated = n + block_count + n + node
            tree.add_node(isolated, kind="isolated", original=node)
            anchors[node] = isolated
    tree_components = list(nx.connected_components(tree))
    distance = np.full((n, n), -1, dtype=np.int32)
    for source in range(n):
        lengths = nx.single_source_shortest_path_length(tree, anchors[source])
        for target in range(n):
            value = lengths.get(anchors[target])
            if value is not None:
                distance[source, target] = int(value)
    block_sizes = np.asarray([len(block) for block in blocks], dtype=np.float64)
    return {
        "distance": distance,
        "membership": membership,
        "block_sizes": block_sizes,
        "articulation": articulation,
        "blocks": blocks,
        "tree_nodes": int(tree.number_of_nodes()),
        "tree_edges": int(tree.number_of_edges()),
        "tree_components": len(tree_components),
    }


def route_features(index: dict, pairs: np.ndarray) -> np.ndarray:
    distance = index["distance"]
    membership = index["membership"]
    block_sizes = index["block_sizes"]
    articulation = index["articulation"]
    rows = []
    for raw_u, raw_v in np.asarray(pairs, dtype=np.int64):
        u, v = int(raw_u), int(raw_v)
        memberships_u = membership[u]
        memberships_v = membership[v]
        shared = set(memberships_u).intersection(memberships_v)
        shared_size = max((block_sizes[b] for b in shared), default=0.0)
        route_distance = float(distance[u, v])
        reachable = float(route_distance >= 0)
        route_hops = route_distance / 2.0 if reachable else -1.0
        rows.append([
            reachable,
            float(bool(shared)),
            math.log1p(shared_size),
            route_distance,
            route_hops,
            float(u in articulation),
            float(v in articulation),
            float(len(memberships_u) + len(memberships_v)),
            float(abs(len(memberships_u) - len(memberships_v))),
        ])
    return np.asarray(rows, dtype=np.float64)


def proxy_matrix(scalar: np.ndarray) -> np.ndarray:
    cn, deg, l3, lp = scalar[:, 0], scalar[:, 3], scalar[:, 4], scalar[:, 5]
    return np.c_[
        np.log1p(np.maximum(cn, 0.0)),
        np.log1p(np.maximum(l3, 0.0)),
        deg,
        np.log1p(np.maximum(lp, 0.0)),
        scalar[:, 1], scalar[:, 2], scalar[:, 6], scalar[:, 7],
        np.sin(np.minimum(l3, 20.0)),
    ]


def stratified_shuffle(values: np.ndarray, scalar: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    shuffled = values.copy()
    strata: dict[tuple[float, ...], list[int]] = defaultdict(list)
    for i, row in enumerate(scalar):
        strata[(round(float(row[0]), 3), round(float(row[4]), 3), round(float(row[3]), 3))].append(i)
    for indices in strata.values():
        if len(indices) > 1:
            shuffled[indices] = values[rng.permutation(np.asarray(indices, dtype=np.int64))]
    return shuffled


def fit_predictions(train_x, train_y, valid_x, valid_y):
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, solver="liblinear"))
    model.fit(train_x, train_y)
    pred = model.predict_proba(valid_x)[:, 1]
    return {"auc": float(roc_auc_score(valid_y, pred)), "ap": float(average_precision_score(valid_y, pred))}, pred


def compute_features(adj, pairs):
    start = os.times().elapsed
    features = [pair_object(adj, int(u), int(v)) for u, v in pairs]
    return scalar_matrix(features), float(os.times().elapsed - start)


def probe_seed(path: Path, seed: int) -> dict:
    data = np.load(path, allow_pickle=False)
    n = int(data["num_nodes"])
    train_edges = np.asarray(data["train_pos"], dtype=np.int64)
    adj = build_adjacency(train_edges, n)
    route = build_route_index(train_edges, n)
    train_pos = train_edges
    train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), n, seed, len(train_pos))
    valid_pos = np.asarray(data["valid_pos"], dtype=np.int64)
    valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]
    test_pos = np.asarray(data["test_pos"], dtype=np.int64)
    test_neg = np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2)
    support_rows = []
    for label, pairs in ((1, test_pos), (0, test_neg)):
        values = route_features(route, pairs)
        support_rows.append({
            "label": label,
            "total": int(len(pairs)),
            "reachable": int(np.sum(values[:, 0] > 0)),
            "shared_block": int(np.sum(values[:, 1] > 0)),
            "articulation_incident": int(np.sum((values[:, 5] + values[:, 6]) > 0)),
            "route_ge2": int(np.sum(values[:, 4] >= 2)),
            "route_ge4": int(np.sum(values[:, 4] >= 4)),
            "mean_route_hops": float(np.mean(values[:, 4])),
        })
    train_pairs = np.concatenate([train_pos, train_neg], axis=0)
    valid_pairs = np.concatenate([valid_pos, valid_neg], axis=0)
    train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))]
    valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))]
    train_scalar, train_seconds = compute_features(adj, train_pairs)
    valid_scalar, valid_seconds = compute_features(adj, valid_pairs)
    train_route = route_features(route, train_pairs)
    valid_route = route_features(route, valid_pairs)
    valid_shuffled = stratified_shuffle(valid_route, valid_scalar, 90000 + seed)
    matrices = {
        "Base": (train_scalar, valid_scalar),
        "TrueRoute": (np.c_[train_scalar, train_route], np.c_[valid_scalar, valid_route]),
        "ShuffledRoute": (np.c_[train_scalar, stratified_shuffle(train_route, train_scalar, 80000 + seed)], np.c_[valid_scalar, valid_shuffled]),
        "Proxy": (np.c_[train_scalar, proxy_matrix(train_scalar)], np.c_[valid_scalar, proxy_matrix(valid_scalar)]),
    }
    metrics, probabilities = {}, {}
    for name, (train_x, valid_x) in matrices.items():
        metrics[name], probabilities[name] = fit_predictions(train_x, train_y, valid_x, valid_y)
    valid_hops = valid_route[:, 4]
    regimes = []
    for label, lower, upper in (("route<2", -1, 1.999), ("route=2-3", 2, 3.999), ("route>=4", 4, np.inf)):
        mask = (valid_hops >= lower) & (valid_hops <= upper)
        if int(mask.sum()) == 0 or len(np.unique(valid_y[mask])) < 2:
            continue
        true_auc = float(roc_auc_score(valid_y[mask], probabilities["TrueRoute"][mask]))
        base_auc = float(roc_auc_score(valid_y[mask], probabilities["Base"][mask]))
        shuf_auc = float(roc_auc_score(valid_y[mask], probabilities["ShuffledRoute"][mask]))
        regimes.append({"regime": label, "n": int(mask.sum()), "true_minus_base_auc": true_auc - base_auc, "true_minus_shuffled_auc": true_auc - shuf_auc})
    return {
        "seed": seed,
        "support": support_rows,
        "metrics": metrics,
        "delta_auc": {"true_minus_base": metrics["TrueRoute"]["auc"] - metrics["Base"]["auc"], "true_minus_shuffled": metrics["TrueRoute"]["auc"] - metrics["ShuffledRoute"]["auc"], "true_minus_proxy": metrics["TrueRoute"]["auc"] - metrics["Proxy"]["auc"]},
        "regimes": regimes,
        "route_graph": {"blocks": len(route["blocks"]), "articulation_points": len(route["articulation"]), "tree_nodes": route["tree_nodes"], "tree_edges": route["tree_edges"], "tree_components": route["tree_components"]},
        "extract_seconds": {"train": train_seconds, "valid": valid_seconds},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()
    result = {"candidate": "R2-01 Block-Cut Route Profile", "runs": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if path.exists():
            result["runs"].append(probe_seed(path, seed))
    result["aggregate"] = {}
    for name in ("Base", "TrueRoute", "ShuffledRoute", "Proxy"):
        rows = [row["metrics"][name] for row in result["runs"]]
        result["aggregate"][name] = {metric + "_mean": float(np.mean([item[metric] for item in rows])) for metric in ("auc", "ap")}
    result["delta_aggregate"] = {key: float(np.mean([row["delta_auc"][key] for row in result["runs"]])) for key in ("true_minus_base", "true_minus_shuffled", "true_minus_proxy")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"candidate": result["candidate"], "aggregate": result["aggregate"], "delta_aggregate": result["delta_aggregate"], "runs": result["runs"]}, indent=2))


if __name__ == "__main__":
    main()
