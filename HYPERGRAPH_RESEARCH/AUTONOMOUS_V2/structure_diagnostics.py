from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import pearsonr, spearmanr

from dcdlp.data.loaders import load_dataset


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results" / "regime_gradient_audit_v1" / "data"
OUT = ROOT / "HYPERGRAPH_RESEARCH" / "AUTONOMOUS_V2"


def describe(values):
    a = np.asarray(values, dtype=float)
    return {
        "count": int(a.size),
        "mean": float(a.mean()) if a.size else 0.0,
        "std": float(a.std()) if a.size else 0.0,
        "min": float(a.min()) if a.size else 0.0,
        "p25": float(np.quantile(a, 0.25)) if a.size else 0.0,
        "median": float(np.median(a)) if a.size else 0.0,
        "p75": float(np.quantile(a, 0.75)) if a.size else 0.0,
        "p90": float(np.quantile(a, 0.90)) if a.size else 0.0,
        "max": float(a.max()) if a.size else 0.0,
    }


def correlation(left, right):
    if len(left) < 3 or np.std(left) == 0 or np.std(right) == 0:
        return {"pearson": None, "spearman": None}
    return {
        "pearson": float(pearsonr(left, right).statistic),
        "spearman": float(spearmanr(left, right).statistic),
    }


def main():
    dataset = load_dataset("cora", DATA, "standard", 0)
    graph = dataset.train_graph()
    nodes = list(range(dataset.num_nodes))
    members = []
    centers = []
    for center in nodes:
        leaves = sorted(graph.neighbors(center))
        if leaves:
            centers.append(center)
            members.append(set([center, *leaves]))
    incident = [[] for _ in nodes]
    for eid, edge in enumerate(members):
        for node in edge:
            incident[node].append(eid)

    sizes, center_degrees, internal_density, off_center_density = [], [], [], []
    triangles, redundancies, leaf_degrees = [], [], []
    for center, edge in zip(centers, members):
        leaves = edge - {center}
        size, leaf_count = len(edge), len(leaves)
        leaf_degree = graph.degree(center)
        sizes.append(size)
        center_degrees.append(leaf_degree)
        leaf_degrees.append(leaf_count)
        all_possible = size * (size - 1) / 2
        internal_edges = graph.subgraph(edge).number_of_edges()
        internal_density.append(internal_edges / all_possible if all_possible else 0.0)
        possible_leaf_pairs = leaf_count * (leaf_count - 1) / 2
        leaf_edges = graph.subgraph(leaves).number_of_edges()
        off_center_density.append(leaf_edges / possible_leaf_pairs if possible_leaf_pairs else 0.0)
        triangles.append(int(leaf_edges))

        nearby = set()
        for node in edge:
            nearby.update(incident[node])
        nearby.discard(len(redundancies))
        overlaps = []
        for other_id in nearby:
            other = members[other_id]
            union = len(edge | other)
            overlaps.append(len(edge & other) / union if union else 0.0)
        overlaps.sort(reverse=True)
        redundancies.append(float(np.mean(overlaps[:3])) if overlaps else 0.0)

    hyperdegree = np.asarray([len(incident[node]) for node in nodes], dtype=float)
    arrays = {
        "size": np.asarray(sizes, dtype=float),
        "center_degree": np.asarray(center_degrees, dtype=float),
        "internal_pairwise_density": np.asarray(internal_density),
        "off_center_density": np.asarray(off_center_density),
        "triangle_count_among_leaves": np.asarray(triangles, dtype=float),
        "shared_node_top3_jaccard_mean": np.asarray(redundancies),
    }
    result = {
        "protocol": "Cora standard train/message graph seed 0",
        "message_graph_nodes": graph.number_of_nodes(),
        "message_graph_edges": graph.number_of_edges(),
        "star_hyperedges": len(members),
        "hyperedge_stats": {key: describe(value) for key, value in arrays.items()},
        "node_hyperdegree": describe(hyperdegree),
        "correlations_with_size": {
            key: correlation(arrays["size"], value)
            for key, value in arrays.items()
            if key != "size"
        },
        "off_center_density_vs_redundancy": correlation(
            arrays["off_center_density"], arrays["shared_node_top3_jaccard_mean"]
        ),
        "leakage_note": "Star hyperedges and all diagnostics are derived only from train_pos via GraphDataset.train_graph().",
    }
    (OUT / "structure_diagnostics.json").write_text(
        json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
