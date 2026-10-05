"""Ten protocol tests for the LPShift adapter.

Run this in the remote mei_env with the LPShift repository as the working
directory. The tests use no model weights and do not alter official files.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
import torch

from lpshift_adapter import LPShiftData, canonical_keys, sha256_array


EXPECTED = {
    "ogbl-collab_CN_2_1_0_seed1": {
        "train": "5db0173da159b5e79b4a641786b127644d64bb2593b273e11e76b29521e49a4a",
        "valid": "6c16deb8c6b39dd25f93b76798bcebd62704015c1e5729cd4102fc7371ca35c3",
        "test": "8f8c0805601d73ee91da361d1c6e695d4a3bc74602c46ffa2886f6004d98bf3a",
        "valid_neg": "24ee3173d984974fd9c9fef4cb133a0e04722b6f8f28415b4fd7c2dafbf0f51d",
        "test_neg": "10bd6bd21860ffd4a9b3c525205bfc6919be607e7b3534e1b8d135f575d313d4",
    },
    "ogbl-collab_CN_4_2_0_seed1": {
        "train": "9e876f00d0da73d7bb1229a9aee50ecf8ff9f1f3221eb932fbb9ec5f2c62c048",
        "valid": "f8ee3623440863545e162b38f4a6ff29cf35b8891ac49d81e8568e562895f42b",
        "test": "cd34f4b513f4d581e64afa405f9df384031d7b5de960153af7b65317fc992ed9",
        "valid_neg": "d3d53f225b54fa69a7f676a660949fdf607dfeaf85b0c92c90bbb18bd232940e",
        "test_neg": "7d8ea1cca3641da1c21fba8a1a6d81e901bfae6931a7b07c9850eea53949ea19",
    },
}


def run(adapter: LPShiftData) -> dict:
    message_keys = adapter.message_edge_keys()
    train_keys = canonical_keys(adapter.train_pos)
    valid_keys = canonical_keys(adapter.valid_pos)
    test_keys = canonical_keys(adapter.test_pos)
    checks = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"id": len(checks) + 1, "name": name, "passed": bool(passed), "detail": detail})

    check("node_and_feature_shape", adapter.num_nodes == 235868 and list(adapter.features.shape) == [235868, 128],
          str(adapter.features.shape))
    expected_message_shape = [2, 1733096] if adapter.dataset_name.endswith("2_1_0_seed1") else [2, 1597130]
    check("message_graph_preserved", list(adapter.message_edge_index.shape) == expected_message_shape,
          str(list(adapter.message_edge_index.shape)))
    raw_rows = [tuple(map(int, row)) for row in adapter.message_edge_index.detach().cpu().t().tolist()]
    expanded_rows = [tuple(map(int, row)) for row in LPShiftData.expand_dcdlp_edges(adapter.dcdlp_edge_index).detach().cpu().t().tolist()]
    check("direction_and_duplicate_semantics",
          Counter(raw_rows) == Counter(expanded_rows),
          f"raw_rows={len(raw_rows)}, expanded_rows={len(expanded_rows)}")
    check("dcdlp_edge_view_does_not_change_nodes",
          int(adapter.dcdlp_edge_index.max()) < adapter.num_nodes and int(adapter.dcdlp_edge_index.min()) >= 0,
          str(list(adapter.dcdlp_edge_index.shape)))
    check("train_positive_in_message_graph", train_keys <= message_keys,
          f"missing={len(train_keys - message_keys)}")
    check("heldout_positive_absent", not (valid_keys & message_keys) and not (test_keys & message_keys),
          f"valid_in_graph={len(valid_keys & message_keys)}, test_in_graph={len(test_keys & message_keys)}")

    target = adapter.train_pos[:1].to(torch.long)
    reverse = target.flip(1)
    masked = adapter.mask_target_edges(adapter.message_edge_index, torch.cat([target, reverse], dim=0))
    masked_keys = canonical_keys(masked.t())
    check("target_mask_removes_both_directions", tuple(sorted(map(int, target[0]))) not in masked_keys,
          f"remaining={tuple(sorted(map(int, target[0]))) in masked_keys}")

    context = next(iter(message_keys - {tuple(sorted(map(int, target[0]))) }))
    check("non_target_context_retained", context in masked_keys, str(context))

    split_order = {
        "train": torch.equal(adapter.train_pos, adapter.split["train"]["edge"]),
        "valid": torch.equal(adapter.valid_pos, adapter.split["valid"]["edge"]),
        "test": torch.equal(adapter.test_pos, adapter.split["test"]["edge"]),
    }
    check("positive_row_order", all(split_order.values()), json.dumps(split_order))
    check("positive_split_disjoint",
          not (train_keys & valid_keys or train_keys & test_keys or valid_keys & test_keys),
          json.dumps({"train_valid": len(train_keys & valid_keys),
                      "train_test": len(train_keys & test_keys),
                      "valid_test": len(valid_keys & test_keys)}))
    neg_order = {
        "valid": torch.equal(adapter.valid_neg, adapter.split["valid"]["edge_neg"]),
        "test": torch.equal(adapter.test_neg, adapter.split["test"]["edge_neg"]),
        "valid_shape": list(adapter.valid_neg.shape)[1:] == [250, 2],
        "test_shape": list(adapter.test_neg.shape)[1:] == [250, 2],
    }
    check("negative_group_and_order", all(neg_order.values()), json.dumps(neg_order))

    expected = EXPECTED.get(adapter.dataset_name)
    hash_values = {
        "train": sha256_array(adapter.train_pos),
        "valid": sha256_array(adapter.valid_pos),
        "test": sha256_array(adapter.test_pos),
        "valid_neg": sha256_array(adapter.valid_neg),
        "test_neg": sha256_array(adapter.test_neg),
    }
    check("official_hashes", expected is not None and hash_values == expected,
          json.dumps({"expected": expected, "actual": hash_values}, sort_keys=True))

    training_keys = set(adapter.training_view())
    check("training_view_has_no_heldout_labels", training_keys == {"message_edge_index", "train_pos"},
          json.dumps(sorted(training_keys)))

    summary = adapter.summary()
    return {
        "dataset": adapter.dataset_name,
        "passed": all(item["passed"] for item in checks),
        "checks": checks,
        "summary": summary,
        "message_edge_count_canonical": len(message_keys),
        "positive_overlap": {
            "train_valid": len(train_keys & valid_keys),
            "train_test": len(train_keys & test_keys),
            "valid_test": len(valid_keys & test_keys),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run(LPShiftData.load(args.repo, args.dataset))
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
