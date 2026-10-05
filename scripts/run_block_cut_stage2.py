"""Minimal parent integration screening for the block-cut route object."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import average_precision_score, roc_auc_score
from torch import nn

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from audit_block_cut_route import (  # noqa: E402
    build_route_index,
    compute_features,
    proxy_matrix,
    route_features,
    stratified_shuffle,
)
from audit_role_transition import build_adjacency, sample_train_negatives, scalar_matrix  # noqa: E402


class PairDecoder(nn.Module):
    def __init__(self, input_dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(nn.Linear(input_dim, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, x):
        return self.net(x).squeeze(-1)


def standardize(train_x, *others):
    mean, std = train_x.mean(axis=0), train_x.std(axis=0)
    std[std < 1e-8] = 1.0
    return ((train_x - mean) / std, *[((x - mean) / std) for x in others])


def classification(pos, neg):
    labels = np.r_[np.ones(len(pos)), np.zeros(neg.size)]
    scores = np.r_[pos, neg.reshape(-1)]
    return {"auc": float(roc_auc_score(labels, scores)), "ap": float(average_precision_score(labels, scores))}


def ranking(pos, neg):
    ranks = 1 + np.sum(neg > pos[:, None], axis=1)
    return {"hits@10": float(np.mean(ranks <= 10)), "hits@50": float(np.mean(ranks <= 50)), "hits@100": float(np.mean(ranks <= 100)), "mrr": float(np.mean(1.0 / ranks))}


def train_variant(train_x, train_y, valid_x, valid_y, test_pos_x, test_neg_x, seed, epochs):
    torch.manual_seed(7100 + seed)
    np.random.seed(8100 + seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    test_neg_flat = test_neg_x.reshape(-1, test_neg_x.shape[-1])
    train_x, valid_x, test_pos_x, test_neg_flat = standardize(train_x, valid_x, test_pos_x, test_neg_flat)
    train_tensor = torch.as_tensor(train_x, dtype=torch.float32, device=device)
    valid_tensor = torch.as_tensor(valid_x, dtype=torch.float32, device=device)
    train_y_tensor = torch.as_tensor(train_y, dtype=torch.float32, device=device)
    pos_tensor = torch.as_tensor(test_pos_x, dtype=torch.float32, device=device)
    neg_tensor = torch.as_tensor(test_neg_flat, dtype=torch.float32, device=device)
    model = PairDecoder(train_x.shape[1]).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
    loss_fn = nn.BCEWithLogitsLoss()
    best_auc, best_state, best_epoch = -float("inf"), None, 0
    start = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = loss_fn(model(train_tensor), train_y_tensor)
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            valid_score = model(valid_tensor).cpu().numpy()
        current_auc = float(roc_auc_score(valid_y, valid_score))
        if current_auc > best_auc:
            best_auc, best_epoch = current_auc, epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pos = model(pos_tensor).cpu().numpy()
        neg = model(neg_tensor).cpu().numpy().reshape(-1, 500)
    metrics = classification(pos, neg)
    metrics.update(ranking(pos, neg))
    return {"metrics": metrics, "best_valid_auc": best_auc, "best_epoch": best_epoch, "train_seconds": float(time.perf_counter() - start), "device": str(device), "parameter_count": int(sum(p.numel() for p in model.parameters()))}


def build_features(path: Path, seed: int):
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
    test_neg = np.asarray(data["test_neg"], dtype=np.int64)
    train_pairs = np.concatenate([train_pos, train_neg], axis=0)
    valid_pairs = np.concatenate([valid_pos, valid_neg], axis=0)
    train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))].astype(np.float32)
    valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))].astype(np.float32)
    train_scalar, train_seconds = compute_features(adj, train_pairs)
    valid_scalar, valid_seconds = compute_features(adj, valid_pairs)
    pos_scalar, pos_seconds = compute_features(adj, test_pos)
    neg_scalar, neg_seconds = compute_features(adj, test_neg.reshape(-1, 2))
    train_route, valid_route = route_features(route, train_pairs), route_features(route, valid_pairs)
    pos_route, neg_route = route_features(route, test_pos), route_features(route, test_neg.reshape(-1, 2))
    train_shuf = stratified_shuffle(train_route, train_scalar, 82000 + seed)
    valid_shuf = stratified_shuffle(valid_route, valid_scalar, 83000 + seed)
    pos_shuf = stratified_shuffle(pos_route, pos_scalar, 84000 + seed)
    neg_shuf = stratified_shuffle(neg_route, neg_scalar, 85000 + seed)
    matrices = {
        "Parent": (train_scalar, valid_scalar, pos_scalar, neg_scalar),
        "TrueRoute": (np.c_[train_scalar, train_route], np.c_[valid_scalar, valid_route], np.c_[pos_scalar, pos_route], np.c_[neg_scalar, neg_route]),
        "ShuffledRoute": (np.c_[train_scalar, train_shuf], np.c_[valid_scalar, valid_shuf], np.c_[pos_scalar, pos_shuf], np.c_[neg_scalar, neg_shuf]),
        "Proxy": (np.c_[train_scalar, proxy_matrix(train_scalar)], np.c_[valid_scalar, proxy_matrix(valid_scalar)], np.c_[pos_scalar, proxy_matrix(pos_scalar)], np.c_[neg_scalar, proxy_matrix(neg_scalar)]),
    }
    return {"train_y": train_y, "valid_y": valid_y, "matrices": matrices, "extraction_seconds": {"train": train_seconds, "valid": valid_seconds, "test_pos": pos_seconds, "test_neg": neg_seconds}, "counts": {"train_pos": len(train_pos), "train_neg": len(train_neg), "valid_pos": len(valid_pos), "test_pos": len(test_pos), "test_neg_per_pos": int(test_neg.shape[1])}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--epochs", type=int, default=80)
    args = parser.parse_args()
    result = {"candidate": "R2-01 Block-Cut Route Profile", "epochs": args.epochs, "runs": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if not path.exists():
            continue
        features = build_features(path, seed)
        for variant, (train_x, valid_x, pos_x, neg_x) in features["matrices"].items():
            out = train_variant(train_x, features["train_y"], valid_x, features["valid_y"], pos_x, neg_x, seed, args.epochs)
            result["runs"].append({"seed": seed, "variant": variant, "counts": features["counts"], "extraction_seconds": features["extraction_seconds"], **out})
            print(json.dumps({"seed": seed, "variant": variant, **out}, indent=2), flush=True)
    result["aggregate"] = {}
    for variant in ("Parent", "TrueRoute", "ShuffledRoute", "Proxy"):
        rows = [r for r in result["runs"] if r["variant"] == variant]
        result["aggregate"][variant] = {metric + "_mean": float(np.mean([r["metrics"].get(metric, r.get(metric)) for r in rows])) for metric in ("auc", "ap", "mrr", "hits@10", "hits@50", "hits@100", "best_valid_auc")}
        result["aggregate"][variant].update({metric + "_std": float(np.std([r["metrics"][metric] for r in rows], ddof=1)) for metric in ("auc", "ap", "mrr", "hits@10", "hits@50", "hits@100")})
    by_key = {(r["seed"], r["variant"]): r for r in result["runs"]}
    result["aggregate_deltas"] = {}
    for variant in ("TrueRoute", "ShuffledRoute", "Proxy"):
        pairs = [(by_key[(s, variant)], by_key[(s, "Parent")]) for s in args.seeds if (s, variant) in by_key and (s, "Parent") in by_key]
        result["aggregate_deltas"][variant] = {metric: float(np.mean([a["metrics"][metric] - b["metrics"][metric] for a, b in pairs])) for metric in ("auc", "ap", "mrr", "hits@10", "hits@50", "hits@100")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"aggregate": result["aggregate"], "aggregate_deltas": result["aggregate_deltas"]}, indent=2))


if __name__ == "__main__":
    main()
