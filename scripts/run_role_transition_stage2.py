"""Minimal real-benchmark screening for R1-07.

The parent is a deterministic scalar structural pair decoder. TrueRole adds
exactly one new input object: the 10-dimensional role-transition histogram.
ShuffledRole and Proxy are same-width controls using the same pair lists and
training protocol.
"""

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
from audit_role_transition import (  # noqa: E402
    build_adjacency,
    compute_features,
    role_matrix,
    sample_train_negatives,
    scalar_matrix,
    stratified_shuffle,
)


class PairDecoder(nn.Module):
    def __init__(self, input_dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(nn.Linear(input_dim, 32), nn.ReLU(), nn.Linear(32, 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)


def proxy_matrix(scalar: np.ndarray) -> np.ndarray:
    """Parameter-matched features made only from already-known scalars."""
    cn, deg_log, l3, local_path = scalar[:, 0], scalar[:, 3], scalar[:, 4], scalar[:, 5]
    return np.c_[
        np.log1p(np.maximum(l3, 0.0)),
        np.sqrt(np.maximum(l3, 0.0)),
        np.log1p(np.maximum(cn, 0.0)),
        np.sqrt(np.maximum(cn, 0.0)),
        deg_log,
        deg_log**2,
        np.log1p(np.maximum(l3 * (1.0 + cn), 0.0)),
        np.log1p(np.maximum(local_path, 0.0)),
        np.sin(np.minimum(l3, 20.0)),
        np.cos(np.minimum(l3, 20.0)),
    ]


def standardize(train_x: np.ndarray, *others: np.ndarray):
    mean, std = train_x.mean(axis=0), train_x.std(axis=0)
    std[std < 1e-8] = 1.0
    return ((train_x - mean) / std, *[((x - mean) / std) for x in others])


def ranking_metrics(pos_scores: np.ndarray, neg_scores: np.ndarray) -> dict[str, float]:
    ranks = 1 + np.sum(neg_scores > pos_scores[:, None], axis=1)
    return {
        "hits@10": float(np.mean(ranks <= 10)),
        "hits@50": float(np.mean(ranks <= 50)),
        "hits@100": float(np.mean(ranks <= 100)),
        "mrr": float(np.mean(1.0 / ranks)),
    }


def classify_metrics(pos_scores: np.ndarray, neg_scores: np.ndarray) -> dict[str, float]:
    labels = np.r_[np.ones(len(pos_scores)), np.zeros(neg_scores.size)]
    scores = np.r_[pos_scores, neg_scores.reshape(-1)]
    return {"auc": float(roc_auc_score(labels, scores)), "ap": float(average_precision_score(labels, scores))}


def train_variant(train_x, train_y, valid_x, valid_y, test_pos_x, test_neg_x, seed: int, epochs: int) -> dict:
    torch.manual_seed(7000 + seed)
    np.random.seed(8000 + seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    test_neg_flat = test_neg_x.reshape(-1, test_neg_x.shape[-1])
    train_x, valid_x, test_pos_x, test_neg_flat = standardize(train_x, valid_x, test_pos_x, test_neg_flat)
    train_tensor = torch.as_tensor(train_x, dtype=torch.float32, device=device)
    train_label = torch.as_tensor(train_y, dtype=torch.float32, device=device)
    valid_tensor = torch.as_tensor(valid_x, dtype=torch.float32, device=device)
    pos_test_tensor = torch.as_tensor(test_pos_x, dtype=torch.float32, device=device)
    neg_test_tensor = torch.as_tensor(test_neg_flat, dtype=torch.float32, device=device)
    model = PairDecoder(train_x.shape[1]).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
    loss_fn = nn.BCEWithLogitsLoss()
    best_valid_auc, best_epoch, best_state = -float("inf"), 0, None
    start = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        loss = loss_fn(model(train_tensor), train_label)
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            valid_scores = model(valid_tensor).detach().cpu().numpy()
        valid_auc = float(roc_auc_score(valid_y, valid_scores))
        if valid_auc > best_valid_auc:
            best_valid_auc, best_epoch = valid_auc, epoch
            best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        pos_scores = model(pos_test_tensor).detach().cpu().numpy()
        neg_scores = model(neg_test_tensor).detach().cpu().numpy().reshape(-1, 500)
    metrics = classify_metrics(pos_scores, neg_scores)
    metrics.update(ranking_metrics(pos_scores, neg_scores))
    return {
        "metrics": metrics,
        "best_valid_auc": best_valid_auc,
        "best_epoch": best_epoch,
        "train_seconds": float(time.perf_counter() - start),
        "device": str(device),
        "parameter_count": int(sum(p.numel() for p in model.parameters())),
    }


def build_split_features(path: Path, seed: int) -> dict:
    data = np.load(path, allow_pickle=False)
    adj = build_adjacency(np.asarray(data["train_pos"], dtype=np.int64), int(data["num_nodes"]))
    train_pos = np.asarray(data["train_pos"], dtype=np.int64)
    train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), int(data["num_nodes"]), seed, len(train_pos))
    valid_pos = np.asarray(data["valid_pos"], dtype=np.int64)
    valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]
    test_pos = np.asarray(data["test_pos"], dtype=np.int64)
    test_neg = np.asarray(data["test_neg"], dtype=np.int64)
    train_pairs = np.concatenate([train_pos, train_neg], axis=0)
    valid_pairs = np.concatenate([valid_pos, valid_neg], axis=0)
    train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))].astype(np.float32)
    valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))].astype(np.float32)
    train_features, train_seconds = compute_features(adj, train_pairs)
    valid_features, valid_seconds = compute_features(adj, valid_pairs)
    test_pos_features, test_seconds = compute_features(adj, test_pos)
    test_neg_flat = test_neg.reshape(-1, 2)
    test_neg_features, test_neg_seconds = compute_features(adj, test_neg_flat)
    scalar_train, scalar_valid = scalar_matrix(train_features), scalar_matrix(valid_features)
    scalar_test_pos, scalar_test_neg = scalar_matrix(test_pos_features), scalar_matrix(test_neg_features)
    role_train, role_valid = role_matrix(train_features), role_matrix(valid_features)
    role_test_pos, role_test_neg = role_matrix(test_pos_features), role_matrix(test_neg_features)
    train_shuffled = stratified_shuffle(role_train, scalar_train, 20000 + seed)
    valid_shuffled = stratified_shuffle(role_valid, scalar_valid, 30000 + seed)
    test_pos_shuffled = stratified_shuffle(role_test_pos, scalar_test_pos, 50000 + seed)
    test_shuffled = stratified_shuffle(role_test_neg, scalar_test_neg, 40000 + seed)
    return {
        "train_y": train_y,
        "valid_y": valid_y,
        "matrices": {
            "Parent": (scalar_train, scalar_valid, scalar_test_pos, scalar_test_neg),
            "TrueRole": (np.c_[scalar_train, role_train], np.c_[scalar_valid, role_valid], np.c_[scalar_test_pos, role_test_pos], np.c_[scalar_test_neg, role_test_neg]),
            "ShuffledRole": (np.c_[scalar_train, train_shuffled], np.c_[scalar_valid, valid_shuffled], np.c_[scalar_test_pos, test_pos_shuffled], np.c_[scalar_test_neg, test_shuffled]),
            "Proxy": (np.c_[scalar_train, proxy_matrix(scalar_train)], np.c_[scalar_valid, proxy_matrix(scalar_valid)], np.c_[scalar_test_pos, proxy_matrix(scalar_test_pos)], np.c_[scalar_test_neg, proxy_matrix(scalar_test_neg)]),
        },
        "extraction_seconds": {"train": train_seconds, "valid": valid_seconds, "test_pos": test_seconds, "test_neg": test_neg_seconds},
        "counts": {"train_pos": int(len(train_pos)), "train_neg": int(len(train_neg)), "valid_pos": int(len(valid_pos)), "valid_neg": int(len(valid_neg)), "test_pos": int(len(test_pos)), "test_neg_per_pos": int(test_neg.shape[1])},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--epochs", type=int, default=80)
    args = parser.parse_args()
    result = {"candidate": "R1-07 Neighbor-Role Transition Matrix", "epochs": args.epochs, "runs": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if not path.exists():
            continue
        split = build_split_features(path, seed)
        for variant, (train_x, valid_x, test_pos_x, test_neg_x) in split["matrices"].items():
            outcome = train_variant(train_x, split["train_y"], valid_x, split["valid_y"], test_pos_x, test_neg_x, seed, args.epochs)
            result["runs"].append({"dataset": "cora_heart", "seed": seed, "variant": variant, "counts": split["counts"], "extraction_seconds": split["extraction_seconds"], **outcome})
            print(json.dumps({"seed": seed, "variant": variant, **outcome}, indent=2), flush=True)
    result["aggregate"] = {}
    for variant in ("Parent", "TrueRole", "ShuffledRole", "Proxy"):
        rows = [row for row in result["runs"] if row["variant"] == variant]
        result["aggregate"][variant] = {}
        for metric in ("auc", "ap", "mrr", "hits@10", "hits@50", "hits@100", "best_valid_auc"):
            values = [row["metrics"].get(metric, row.get(metric)) for row in rows]
            result["aggregate"][variant][metric + "_mean"] = float(np.mean(values)) if values else None
            result["aggregate"][variant][metric + "_std"] = float(np.std(values, ddof=1)) if len(values) > 1 else (0.0 if values else None)
    by_key = {(row["seed"], row["variant"]): row for row in result["runs"]}
    result["aggregate_deltas"] = {}
    for variant in ("TrueRole", "ShuffledRole", "Proxy"):
        pairs = [(by_key[(seed, variant)], by_key[(seed, "Parent")]) for seed in args.seeds if (seed, variant) in by_key and (seed, "Parent") in by_key]
        result["aggregate_deltas"][variant] = {metric: float(np.mean([a["metrics"][metric] - b["metrics"][metric] for a, b in pairs])) if pairs else None for metric in ("auc", "ap", "mrr", "hits@10", "hits@50", "hits@100")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"aggregate": result["aggregate"], "aggregate_deltas": result["aggregate_deltas"]}, indent=2))


if __name__ == "__main__":
    main()
