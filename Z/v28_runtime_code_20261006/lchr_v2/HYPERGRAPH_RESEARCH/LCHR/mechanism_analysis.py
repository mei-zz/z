from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import torch

from dcdlp.data.loaders import load_dataset
from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
from dcdlp.evaluate import load_checkpoint_model
from dcdlp.train import edge_index_from_graph, score_pairs


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "lchr_stage1"
DATA = ROOT / "data"


def checkpoint_for(label: str) -> Path:
    return next((RUNS / label / "checkpoints").glob("*.pt"))


def main() -> None:
    dataset = load_dataset("cora", DATA, "standard", 0)
    graph = dataset.train_graph()
    edge_index = edge_index_from_graph(graph, torch.device("cuda"))
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    nneg, seed = 20, 777
    count = max(nneg * len(dataset.valid_pos), nneg)
    neg_pool = uniform_negative_sampling(dataset.num_nodes, dataset.all_positive, count, seed)
    negatives = grouped_negatives(dataset.valid_pos, neg_pool, nneg, seed + 1)
    flat = negatives.reshape(-1, 2)

    entropy, pools, tops, routes = [], [], [], []
    model, _ = load_checkpoint_model(checkpoint_for("B4"), "cuda")
    candidates = np.vstack([dataset.valid_pos, flat])
    with torch.no_grad():
        for start in range(0, len(candidates), 1024):
            pairs = torch.as_tensor(candidates[start:start + 1024], dtype=torch.long, device="cuda")
            model(x, edge_index, pairs, remove_target_edges=True)
            diag = model.link_router.last_diagnostics
            entropy.extend(diag["entropy"])
            pools.extend(diag["pool_sizes"])
            tops.extend(diag["top1"])
            routes.extend(diag.get("weights", []))
    positive_entropy = np.asarray(entropy[:len(dataset.valid_pos)])
    order = np.argsort(positive_entropy)
    groups = np.array_split(order, 3)
    group_results = {}
    for label in ("B1", "B3", "B4"):
        current, _ = load_checkpoint_model(checkpoint_for(label), "cuda")
        pos = score_pairs(current, x, edge_index, dataset.valid_pos)["logit"]
        neg = score_pairs(current, x, edge_index, flat, batch_size=4096)["logit"].reshape(len(dataset.valid_pos), nneg)
        group_results[label] = []
        for idx in groups:
            rr = 1.0 / (1 + (neg[idx] > pos[idx, None]).sum(axis=1))
            group_results[label].append({"n": int(len(idx)), "mrr": float(rr.mean())})
    # Sparse cosine similarity on exact hyperedge member sets.
    sparse = []
    for row in routes[:len(dataset.valid_pos)]:
        sparse.append({tuple(members): weight for members, weight in row})
    sims = []
    for i in range(len(sparse)):
        for j in range(i):
            keys = sparse[i].keys() | sparse[j].keys()
            dot = sum(sparse[i].get(k, 0.0) * sparse[j].get(k, 0.0) for k in keys)
            ni = sum(v * v for v in sparse[i].values()) ** 0.5
            nj = sum(v * v for v in sparse[j].values()) ** 0.5
            sims.append(dot / (ni * nj) if ni and nj else 0.0)
    result = {
        "validation_entropy_bins": group_results,
        "candidate_count_including_negatives": len(candidates),
        "average_pool_size": float(np.mean(pools)),
        "empty_pool_fraction": float(np.mean(np.asarray(pools) == 0)),
        "average_entropy": float(np.mean(entropy)),
        "average_top1_weight": float(np.mean(tops)),
        "positive_entropy_cut_points": [float(np.quantile(positive_entropy, q)) for q in (1 / 3, 2 / 3)],
        "mean_pairwise_router_cosine_similarity_positive_candidates": float(np.mean(sims)),
        "router_similarity_pair_count": len(sims),
        "seed": 0,
        "validation_negative_seed": seed,
    }
    (RUNS / "mechanism_analysis.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
