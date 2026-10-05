from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from dcdlp.models.dcdlp import DCDLP
from candidate_models import CrossDepthPairTensor, PairConditionedDynamicTransport


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", choices=["V2-001_PCDT", "V2-002_CDPT"], default="V2-001_PCDT")
    args = parser.parse_args()
    torch.manual_seed(0)
    num_nodes, input_dim, hidden_dim, branch_dim = 31, 7, 16, 8
    edges = torch.tensor([
        [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    ], dtype=torch.long)
    x = torch.randn(num_nodes, input_dim)
    pairs = torch.tensor([[0, 6], [2, 8], [10, 16], [20, 21]], dtype=torch.long)
    common = dict(
        hidden_dim=hidden_dim,
        branch_dim=branch_dim,
        num_layers=2,
        dropout=0.0,
        backbone="gcn",
        use_interaction=True,
        active_branches=("degree", "cn", "residual"),
        decoder_mode="additive",
        interaction_mode="unrestricted",
    )
    parent = DCDLP(input_dim, **common)
    candidate_class = PairConditionedDynamicTransport if args.candidate == "V2-001_PCDT" else CrossDepthPairTensor
    candidate_kwargs = {"transport_rank": 4} if args.candidate == "V2-001_PCDT" else {}
    candidate = candidate_class(input_dim, **common, **candidate_kwargs)
    shared = {key: value for key, value in candidate.state_dict().items() if key in parent.state_dict()}
    parent.load_state_dict(shared, strict=False)
    candidate.eval()
    parent.eval()
    if hasattr(candidate, "transport_scale"):
        candidate.transport_scale.data.zero_()
    else:
        candidate.depth_scale.data.zero_()
    cand = candidate(x, edges, pairs)
    par = parent(x, edges, pairs)
    max_parent_equivalence_error = float((cand["logit"] - par["logit"]).abs().max())
    if hasattr(candidate, "transport_scale"):
        candidate.transport_scale.data.fill_(0.1)
    else:
        candidate.depth_scale.data.fill_(0.1)
    out = candidate(x, edges, pairs)
    out["logit"].sum().backward()
    nonzero_transport_grads = sum(
        int(parameter.grad is not None and torch.isfinite(parameter.grad).all() and parameter.grad.abs().sum() > 0)
        for name, parameter in candidate.named_parameters()
        if name.startswith(("pair_token", "operator_generator", "neighbor_projection", "rank_projection", "endpoint_update", "transport_score", "transport_scale", "depth_pair_encoder", "depth_operator", "depth_scale"))
    )
    result = {
        "parent_parameters": sum(value.numel() for value in parent.parameters()),
        "candidate": args.candidate,
        "candidate_parameters": sum(value.numel() for value in candidate.parameters()),
        "parameter_delta": sum(value.numel() for value in candidate.parameters()) - sum(value.numel() for value in parent.parameters()),
        "max_parent_equivalence_error_when_scale_zero": max_parent_equivalence_error,
        "exchange_error": float((candidate(x, edges, pairs)["logit"] - candidate(x, edges, pairs.flip(1))["logit"]).abs().max()),
        "finite_output": bool(torch.isfinite(out["logit"]).all()),
        "nonzero_transport_gradient_parameter_tensors": nonzero_transport_grads,
        "status": "PASS" if max_parent_equivalence_error < 1e-6 and torch.isfinite(out["logit"]).all() and nonzero_transport_grads > 0 else "FAIL",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
