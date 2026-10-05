from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import torch
from ogb.linkproppred import PygLinkPropPredDataset

from synth_dataset import SynthDataset


def digest(array) -> str:
    value = np.asarray(array)
    return hashlib.sha256(np.ascontiguousarray(value).tobytes()).hexdigest()


def canonical_set(edges) -> set[tuple[int, int]]:
    rows = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    return {(min(int(u), int(v)), max(int(u), int(v))) for u, v in rows}


def audit(dataset_name: str, ogb_root: str) -> dict:
    dataset = SynthDataset(dataset_name=dataset_name)
    data = dataset.get()
    split = dataset.get_edge_split()
    train = np.asarray(split["train"]["edge"], dtype=np.int64)
    valid = np.asarray(split["valid"]["edge"], dtype=np.int64)
    test = np.asarray(split["test"]["edge"], dtype=np.int64)
    valid_neg = np.asarray(split["valid"]["edge_neg"], dtype=np.int64)
    test_neg = np.asarray(split["test"]["edge_neg"], dtype=np.int64)

    train_set = canonical_set(train)
    valid_set = canonical_set(valid)
    test_set = canonical_set(test)
    graph_set = canonical_set(data.edge_index.detach().cpu().numpy().T)
    ogb = PygLinkPropPredDataset(name="ogbl-collab", root=ogb_root)
    original_set = canonical_set(ogb[0].edge_index.detach().cpu().numpy().T)

    def negative_audit(negative, positive_set):
        rows = negative.reshape(-1, 2)
        canonical = [(min(int(u), int(v)), max(int(u), int(v))) for u, v in rows]
        return {
            "shape": list(negative.shape),
            "sha256": digest(negative),
            "self_loops": int(sum(u == v for u, v in canonical)),
            "duplicate_rows": int(len(canonical) - len(set(canonical))),
            "in_training_graph": int(sum(pair in graph_set for pair in canonical)),
            "in_original_ogb_positive_graph": int(sum(pair in original_set for pair in canonical)),
            "in_target_split_positive": int(sum(pair in positive_set for pair in canonical)),
        }

    output = {
        "dataset_name": dataset_name,
        "node_count": int(data.num_nodes),
        "feature_shape": list(data.x.shape),
        "training_graph_edge_index_shape": list(data.edge_index.shape),
        "positive_shapes": {"train": list(train.shape), "valid": list(valid.shape), "test": list(test.shape)},
        "positive_hashes": {"train": digest(train), "valid": digest(valid), "test": digest(test)},
        "negative": {
            "valid": negative_audit(valid_neg, valid_set),
            "test": negative_audit(test_neg, test_set),
        },
        "positive_overlap": {
            "train_valid": len(train_set & valid_set),
            "train_test": len(train_set & test_set),
            "valid_test": len(valid_set & test_set),
            "train_in_graph": len(train_set & graph_set),
            "valid_in_graph": len(valid_set & graph_set),
            "test_in_graph": len(test_set & graph_set),
        },
        "original_ogb": {
            "node_count": int(ogb[0].num_nodes),
            "edge_index_shape": list(ogb[0].edge_index.shape),
            "positive_edge_count": len(original_set),
            "edge_index_sha256": digest(ogb[0].edge_index.detach().cpu().numpy()),
        },
    }
    return output


if __name__ == "__main__":
    result = audit("ogbl-collab_CN_2_1_0_seed1", "dataset")
    Path("/home/ubuntu/AFDR_V7/raw/lpshift_dataset_audit.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
