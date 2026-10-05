"""Check the sparse cached decoder against the unmodified DCDLP forward."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as ssp
import torch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcdlp.models.dcdlp import DCDLP
from lpshift_adapter import LPShiftData
from run_lpshift_dcdlp import (
    degrees_after_mask,
    decode,
    masked_adjacency,
    target_mask_keys,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--pairs", type=int, default=512)
    args = parser.parse_args()

    device = torch.device(args.device)
    adapter = LPShiftData.load(args.repo, args.dataset)
    x = adapter.features.to(device=device, dtype=torch.float32)
    edge_index = adapter.dcdlp_edge_index.to(device=device, dtype=torch.long)
    pairs = adapter.train_pos[:args.pairs].to(device=device, dtype=torch.long)
    base_neighbors = adapter.message_neighbors()
    message_keys = adapter.message_edge_keys()
    removed = target_mask_keys(pairs, message_keys)
    edge_cpu = adapter.message_edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
    base_adj = ssp.csr_matrix((np.ones(edge_cpu.shape[1], dtype=np.float32),
                               (edge_cpu[0], edge_cpu[1])), shape=(adapter.num_nodes, adapter.num_nodes))
    base_adj.sum_duplicates()
    base_adj.data[:] = 1.0
    masked_edge = adapter.mask_target_edges(edge_index, pairs)
    model = DCDLP(
        x.shape[1], hidden_dim=64, branch_dim=32, num_layers=2, dropout=0.1,
        backbone="gcn", use_interaction=True,
        active_branches=("degree", "cn", "residual"), decoder_mode="additive",
        cn_feature_mode="raw", cn_regressor=None,
        interaction_mode="unrestricted", cn_input_schema="selective_v1",
    ).to(device)
    model.eval()
    with torch.no_grad():
        old = model(x, masked_edge, pairs, remove_target_edges=False)
        h = model.node_encoder(x, masked_edge)
        degrees = degrees_after_mask(base_neighbors, removed, device)
        new = decode(model, h, pairs, base_neighbors, degrees,
                     masked_adjacency(base_adj, removed), removed)
    names = ["logit", "score_degree", "score_cn", "score_residual", "score_interaction", "cn_raw"]
    errors = {}
    for name in names:
        lhs = old[name].detach().cpu().float()
        rhs = new[name].detach().cpu().float()
        errors[name] = {"max_abs": float((lhs - rhs).abs().max()),
                        "mean_abs": float((lhs - rhs).abs().mean())}
    result = {"dataset": args.dataset, "pairs": args.pairs, "passed": all(v["max_abs"] < 1e-5 for v in errors.values()), "errors": errors}
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
