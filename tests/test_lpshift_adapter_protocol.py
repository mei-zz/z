from __future__ import annotations

from collections import Counter
from pathlib import Path
from types import SimpleNamespace
import sys

import torch


SCRIPT_DIR = Path(__file__).resolve().parents[1] / "AUTONOMOUS_FAILURE_DRIVEN_RESEARCH" / "V8" / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
from lpshift_adapter import LPShiftData  # noqa: E402


def _adapter() -> LPShiftData:
    # Synthetic protocol fixture: two context pairs, one with duplicate
    # directed rows, plus a held-out positive that must not enter the graph.
    raw_message = torch.tensor(
        [[0, 0, 1, 1, 2, 3], [1, 1, 0, 0, 3, 2]], dtype=torch.long
    )
    split = {
        "train": {"edge": torch.tensor([[0, 1], [2, 3]], dtype=torch.long)},
        "valid": {
            "edge": torch.tensor([[0, 2]], dtype=torch.long),
            "edge_neg": torch.tensor([[[0, 3], [1, 3]]], dtype=torch.long),
        },
        "test": {
            "edge": torch.tensor([[1, 3]], dtype=torch.long),
            "edge_neg": torch.tensor([[[0, 2], [0, 3]]], dtype=torch.long),
        },
    }
    data = SimpleNamespace(num_nodes=4, x=torch.arange(8, dtype=torch.float32).reshape(4, 2), edge_index=raw_message)
    return LPShiftData("synthetic", Path("."), data, split)


def test_raw_message_graph_and_dcdlp_view_preserve_direction_and_multiplicity():
    adapter = _adapter()
    expanded = LPShiftData.expand_dcdlp_edges(adapter.dcdlp_edge_index)
    assert Counter(map(tuple, expanded.t().tolist())) == Counter(map(tuple, adapter.message_edge_index.t().tolist()))
    assert torch.equal(adapter.features, adapter.data.x)
    assert adapter.num_nodes == 4


def test_target_mask_removes_both_directions_but_keeps_other_context():
    adapter = _adapter()
    target = torch.tensor([[0, 1]], dtype=torch.long)
    masked = adapter.mask_target_edges(adapter.dcdlp_edge_index, target)
    expanded = LPShiftData.expand_dcdlp_edges(masked)
    rows = Counter(map(tuple, expanded.t().tolist()))
    assert rows[(0, 1)] == 0
    assert rows[(1, 0)] == 0
    assert rows[(2, 3)] == 1
    assert rows[(3, 2)] == 1


def test_official_split_rows_and_grouped_candidates_are_not_reordered():
    adapter = _adapter()
    assert torch.equal(adapter.valid_pos, adapter.split["valid"]["edge"])
    assert torch.equal(adapter.test_pos, adapter.split["test"]["edge"])
    assert adapter.valid_neg.shape == (1, 2, 2)
    assert adapter.test_neg.shape == (1, 2, 2)
    assert set(adapter.training_view()) == {"message_edge_index", "train_pos"}
