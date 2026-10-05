"""Minimal locked ranking screen for R1-03."""

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
from audit_disjoint_path_profile import build_adjacency, compute, object_matrix, sample_train_negatives, scalar_matrix, shuffle  # noqa: E402


class PairDecoder(nn.Module):
    def __init__(self, width):
        super().__init__(); self.net = nn.Sequential(nn.Linear(width, 32), nn.ReLU(), nn.Linear(32, 1))
    def forward(self, x): return self.net(x).squeeze(-1)


def proxy_matrix(scalar):
    cn, deg, l3, local_path = scalar[:, 0], scalar[:, 3], scalar[:, 4], scalar[:, 5]
    return np.c_[np.log1p(np.maximum(l3, 0)), np.sqrt(np.maximum(l3, 0)), np.log1p(np.maximum(cn, 0)), np.sqrt(np.maximum(cn, 0)), deg, deg ** 2, np.log1p(np.maximum(local_path, 0)), np.sin(np.minimum(l3, 20)), np.cos(np.minimum(l3, 20))]


def standardize(train_x, *others):
    mean, std = train_x.mean(axis=0), train_x.std(axis=0); std[std < 1e-8] = 1.0
    return ((train_x - mean) / std, *[((x - mean) / std) for x in others])


def metrics(pos, neg):
    labels = np.r_[np.ones(len(pos)), np.zeros(neg.size)]; scores = np.r_[pos, neg.reshape(-1)]; ranks = 1 + np.sum(neg > pos[:, None], axis=1)
    return {"auc": float(roc_auc_score(labels, scores)), "ap": float(average_precision_score(labels, scores)), "mrr": float(np.mean(1.0 / ranks)), "hits@10": float(np.mean(ranks <= 10)), "hits@50": float(np.mean(ranks <= 50)), "hits@100": float(np.mean(ranks <= 100))}


def train_variant(train_x, train_y, valid_x, valid_y, pos_x, neg_x, seed, epochs):
    torch.manual_seed(7600 + seed); np.random.seed(8600 + seed); device = torch.device("cuda" if torch.cuda.is_available() else "cpu"); flat_neg = neg_x.reshape(-1, neg_x.shape[-1]); train_x, valid_x, pos_x, flat_neg = standardize(train_x, valid_x, pos_x, flat_neg)
    train_tensor, valid_tensor, pos_tensor, neg_tensor = [torch.as_tensor(x, dtype=torch.float32, device=device) for x in (train_x, valid_x, pos_x, flat_neg)]; y = torch.as_tensor(train_y, dtype=torch.float32, device=device); model = PairDecoder(train_x.shape[1]).to(device); optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4); loss_fn = nn.BCEWithLogitsLoss(); best_auc, best_epoch, best_state = -float("inf"), 0, None; start = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train(); optimizer.zero_grad(set_to_none=True); loss = loss_fn(model(train_tensor), y); loss.backward(); optimizer.step(); model.eval()
        with torch.no_grad(): current_auc = float(roc_auc_score(valid_y, model(valid_tensor).cpu().numpy()))
        if current_auc > best_auc: best_auc, best_epoch = current_auc, epoch; best_state = {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    if best_state is not None: model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad(): pos = model(pos_tensor).cpu().numpy(); neg = model(neg_tensor).cpu().numpy().reshape(-1, 500)
    return {"metrics": metrics(pos, neg), "best_valid_auc": best_auc, "best_epoch": best_epoch, "train_seconds": float(time.perf_counter() - start), "device": str(device), "parameter_count": int(sum(p.numel() for p in model.parameters()))}


def build(path, seed):
    data = np.load(path, allow_pickle=False); n = int(data["num_nodes"]); train_pos = np.asarray(data["train_pos"], dtype=np.int64); adj = build_adjacency(train_pos, n); train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), n, seed, len(train_pos)); valid_pos = np.asarray(data["valid_pos"], dtype=np.int64); valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]; test_pos = np.asarray(data["test_pos"], dtype=np.int64); test_neg = np.asarray(data["test_neg"], dtype=np.int64); train_pairs = np.concatenate([train_pos, train_neg]); valid_pairs = np.concatenate([valid_pos, valid_neg]); train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))].astype(np.float32); valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))].astype(np.float32)
    train_values = compute(adj, train_pairs)[0]; valid_values = compute(adj, valid_pairs)[0]; pos_values = compute(adj, test_pos)[0]; neg_values = compute(adj, test_neg.reshape(-1, 2))[0]; train_scalar, valid_scalar = scalar_matrix(train_values), scalar_matrix(valid_values); pos_scalar, neg_scalar = scalar_matrix(pos_values), scalar_matrix(neg_values); train_obj, valid_obj = object_matrix(train_values), object_matrix(valid_values); pos_obj, neg_obj = object_matrix(pos_values), object_matrix(neg_values); train_shuf, valid_shuf = shuffle(train_obj, train_scalar, 93000 + seed), shuffle(valid_obj, valid_scalar, 94000 + seed); pos_shuf, neg_shuf = shuffle(pos_obj, pos_scalar, 95000 + seed), shuffle(neg_obj, neg_scalar, 96000 + seed)
    return train_y, valid_y, {"Parent": (train_scalar, valid_scalar, pos_scalar, neg_scalar), "TrueDisjoint": (np.c_[train_scalar, train_obj], np.c_[valid_scalar, valid_obj], np.c_[pos_scalar, pos_obj], np.c_[neg_scalar, neg_obj]), "ShuffledDisjoint": (np.c_[train_scalar, train_shuf], np.c_[valid_scalar, valid_shuf], np.c_[pos_scalar, pos_shuf], np.c_[neg_scalar, neg_shuf]), "Proxy": (np.c_[train_scalar, proxy_matrix(train_scalar)], np.c_[valid_scalar, proxy_matrix(valid_scalar)], np.c_[pos_scalar, proxy_matrix(pos_scalar)], np.c_[neg_scalar, proxy_matrix(neg_scalar)])}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--data-root", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2]); parser.add_argument("--epochs", type=int, default=80); args = parser.parse_args(); result = {"candidate": "R1-03 Internally Vertex-Disjoint Path Profile", "epochs": args.epochs, "runs": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if not path.exists(): continue
        train_y, valid_y, matrices = build(path, seed)
        for variant, (train_x, valid_x, pos_x, neg_x) in matrices.items():
            outcome = train_variant(train_x, train_y, valid_x, valid_y, pos_x, neg_x, seed, args.epochs); result["runs"].append({"seed": seed, "variant": variant, **outcome}); print(json.dumps({"seed": seed, "variant": variant, **outcome}, indent=2), flush=True)
    result["aggregate"] = {}
    for variant in ("Parent", "TrueDisjoint", "ShuffledDisjoint", "Proxy"):
        rows = [r for r in result["runs"] if r["variant"] == variant]; result["aggregate"][variant] = {m + "_mean": float(np.mean([r["metrics"][m] for r in rows])) for m in ("auc", "ap", "mrr", "hits@10", "hits@50", "hits@100")}
    by_key = {(r["seed"], r["variant"]): r for r in result["runs"]}; result["aggregate_deltas"] = {}
    for variant in ("TrueDisjoint", "ShuffledDisjoint", "Proxy"):
        pairs = [(by_key[(s, variant)], by_key[(s, "Parent")]) for s in args.seeds if (s, variant) in by_key and (s, "Parent") in by_key]; result["aggregate_deltas"][variant] = {m: float(np.mean([a["metrics"][m] - b["metrics"][m] for a, b in pairs])) for m in ("auc", "ap", "mrr", "hits@10", "hits@50", "hits@100")}
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"aggregate": result["aggregate"], "aggregate_deltas": result["aggregate_deltas"]}, indent=2))


if __name__ == "__main__": main()
