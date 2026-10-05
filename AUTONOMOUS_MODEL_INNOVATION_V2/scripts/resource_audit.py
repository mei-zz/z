from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcdlp.data.loaders import load_dataset
from dcdlp.train import edge_index_from_graph
from dcdlp.models.dcdlp import DCDLP
from candidate_models import CrossDepthPairTensor, PairConditionedDynamicTransport


def measure(model, x, edges, pairs, device):
    model.eval()
    with torch.no_grad():
        for _ in range(2):
            model(x, edges, pairs)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
            torch.cuda.reset_peak_memory_stats(device)
        start = time.perf_counter()
        for _ in range(3):
            model(x, edges, pairs)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
            peak = torch.cuda.max_memory_allocated(device) / 2**20
        else:
            peak = 0.0
    return {"mean_forward_seconds": (time.perf_counter() - start) / 3.0, "peak_gpu_mb": peak}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--batch-size", type=int, default=8192)
    parser.add_argument("--candidate", choices=["V2-001_PCDT", "V2-002_CDPT"], default="V2-001_PCDT")
    args = parser.parse_args()
    device = torch.device(args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    dataset = load_dataset("cora", Path(args.data_root), protocol="heart", seed=0)
    graph = dataset.train_graph()
    edges = edge_index_from_graph(graph, device)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device=device)
    flat = np.asarray(dataset.test_neg).reshape(-1, 2)
    pairs = torch.as_tensor(flat[:args.batch_size], dtype=torch.long, device=device)
    common = dict(
        hidden_dim=64,
        branch_dim=32,
        num_layers=2,
        dropout=0.0,
        backbone="gcn",
        use_interaction=True,
        active_branches=("degree", "cn", "residual"),
        decoder_mode="additive",
        interaction_mode="unrestricted",
    )
    parent = DCDLP(x.shape[1], **common).to(device)
    candidate_class = PairConditionedDynamicTransport if args.candidate == "V2-001_PCDT" else CrossDepthPairTensor
    candidate_kwargs = {"transport_rank": 8} if args.candidate == "V2-001_PCDT" else {}
    candidate = candidate_class(x.shape[1], **common, **candidate_kwargs).to(device)
    parent_result = measure(parent, x, edges, pairs, device)
    candidate_result = measure(candidate, x, edges, pairs, device)
    result = {
        "dataset": "cora_heart_seed0",
        "num_nodes": int(dataset.num_nodes),
        "train_edges": int(len(dataset.train_pos)),
        "max_train_degree": int(max(dict(graph.degree()).values())),
        "batch_size": int(len(pairs)),
        "device": str(device),
        "candidate": args.candidate,
        "parent_parameters": int(sum(value.numel() for value in parent.parameters())),
        "candidate_parameters": int(sum(value.numel() for value in candidate.parameters())),
        "parameter_ratio": float(sum(value.numel() for value in candidate.parameters()) / sum(value.numel() for value in parent.parameters())),
        "parent": parent_result,
        "candidate_runtime": candidate_result,
        "forward_time_ratio": float(candidate_result["mean_forward_seconds"] / parent_result["mean_forward_seconds"]),
        "peak_memory_delta_mb": float(candidate_result["peak_gpu_mb"] - parent_result["peak_gpu_mb"]),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
