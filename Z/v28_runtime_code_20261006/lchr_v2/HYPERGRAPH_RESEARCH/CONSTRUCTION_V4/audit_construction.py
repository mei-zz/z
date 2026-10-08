"""Recompute raw and ECPH construction statistics on the registered Cora split."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch

from dcdlp.data.loaders import load_dataset
from dcdlp.models.hypergraph import construction_statistics
from dcdlp.models.node_encoder import mask_pair_edges
from dcdlp.train import edge_index_from_graph


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "HYPERGRAPH_RESEARCH" / "CONSTRUCTION_V4" / "construction_audit.json"


def main() -> None:
    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    graph = dataset.train_graph()
    edge_index = edge_index_from_graph(graph, torch.device("cpu"))
    constructions = (
        "raw_star", "ecph_random", "ecph_degree", "ecph_true",
        "ecnh_random", "ecnh_union", "ecnh_true",
        "owh_random", "owh_closed", "owh_open",
    )
    stats = {
        name: construction_statistics(edge_index, dataset.num_nodes, name)
        for name in constructions
    }
    target = torch.as_tensor(dataset.train_pos[:1], dtype=torch.long)
    masked = mask_pair_edges(edge_index, target)
    target_key = tuple(sorted(map(int, target[0].tolist())))
    remaining = {tuple(sorted(map(int, pair))) for pair in masked.t().tolist()}
    result = {
        "dataset": dataset.name,
        "protocol": "standard",
        "seed": 0,
        "nodes": int(dataset.num_nodes),
        "undirected_train_edges": int(graph.number_of_edges()),
        "train_positive_count": int(len(dataset.train_pos)),
        "validation_positive_count": int(len(dataset.valid_pos)),
        "test_positive_count": int(len(dataset.test_pos)),
        "construction_stats": stats,
        "density_check": {
            "true_component_internal_density": stats["ecph_true"]["mean_internal_density_in_group_members"],
            "random_control_internal_density": stats["ecph_random"]["mean_internal_density_in_group_members"],
            "true_exceeds_random": (
                stats["ecph_true"]["mean_internal_density_in_group_members"]
                > stats["ecph_random"]["mean_internal_density_in_group_members"]
            ),
        },
        "target_mask_check": {
            "target_pair": target_key,
            "removed_from_builder_input": target_key not in remaining,
            "builder_input_undirected_edge_count": int(len(remaining)),
        },
        "test_evaluated": False,
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
