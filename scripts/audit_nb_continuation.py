"""Stage-0/Stage-1 audit for a non-backtracking continuation profile."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from audit_role_transition import build_adjacency, pair_object, sample_train_negatives, scalar_matrix  # noqa: E402


def nb_profile(adj: list[set[int]], u: int, v: int) -> np.ndarray:
    """Summarize valid u-a-b-c-v continuations without immediate backtracks."""
    continuations = []
    nv = adj[v]
    for a in adj[u]:
        if a == v:
            continue
        for b in adj[a]:
            if b == u:
                continue
            count = 0
            for c in adj[b]:
                if c != a and c in nv:
                    count += 1
            if count:
                continuations.append(count)
    values = np.asarray(continuations, dtype=np.float64)
    if len(values) == 0:
        return np.zeros(8, dtype=np.float64)
    return np.asarray([
        float(values.sum()),
        float(len(values)),
        float(values.max()),
        float(np.sum(values == 1)),
        float(np.sum(values == 2)),
        float(np.sum(values == 3)),
        float(np.sum(values >= 4)),
        float(len(values) / values.sum()),
    ], dtype=np.float64)


def nb_matrix(adj, pairs):
    return np.asarray([nb_profile(adj, int(u), int(v)) for u, v in pairs], dtype=np.float64)


def proxy_matrix(scalar: np.ndarray) -> np.ndarray:
    cn, deg, l3, lp = scalar[:, 0], scalar[:, 3], scalar[:, 4], scalar[:, 5]
    return np.c_[
        np.log1p(np.maximum(l3, 0.0)), np.sqrt(np.maximum(l3, 0.0)),
        np.log1p(np.maximum(cn, 0.0)), np.sqrt(np.maximum(cn, 0.0)),
        deg, deg**2, np.log1p(np.maximum(lp, 0.0)), scalar[:, 1],
    ]


def stratified_shuffle(values, scalar, seed):
    rng = np.random.default_rng(seed)
    shuffled = values.copy()
    groups = defaultdict(list)
    for i, row in enumerate(scalar):
        groups[(round(float(row[0]), 3), round(float(row[4]), 3), round(float(row[3]), 3))].append(i)
    for indices in groups.values():
        if len(indices) > 1:
            shuffled[indices] = values[rng.permutation(np.asarray(indices, dtype=np.int64))]
    return shuffled


def scalar_features(adj, pairs):
    start = os.times().elapsed
    values = scalar_matrix([pair_object(adj, int(u), int(v)) for u, v in pairs])
    return values, float(os.times().elapsed - start)


def fit(train_x, train_y, valid_x, valid_y):
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, solver="liblinear"))
    model.fit(train_x, train_y)
    score = model.predict_proba(valid_x)[:, 1]
    return {"auc": float(roc_auc_score(valid_y, score)), "ap": float(average_precision_score(valid_y, score))}, score


def run_seed(path: Path, seed: int) -> dict:
    data = np.load(path, allow_pickle=False)
    n = int(data["num_nodes"])
    adj = build_adjacency(np.asarray(data["train_pos"], dtype=np.int64), n)
    train_pos = np.asarray(data["train_pos"], dtype=np.int64)
    train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), n, seed, len(train_pos))
    valid_pos = np.asarray(data["valid_pos"], dtype=np.int64)
    valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]
    test_pos = np.asarray(data["test_pos"], dtype=np.int64)
    test_neg = np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2)
    support = []
    for label, pairs in ((1, test_pos), (0, test_neg)):
        profile = nb_matrix(adj, pairs)
        support.append({"label": label, "total": int(len(pairs)), "nonzero": int(np.sum(profile[:, 0] > 0)), "multi_continuation": int(np.sum(profile[:, 1] > 1)), "high_continuation": int(np.sum(profile[:, 2] >= 3)), "mean_total": float(np.mean(profile[:, 0]))})
    train_pairs = np.concatenate([train_pos, train_neg], axis=0)
    valid_pairs = np.concatenate([valid_pos, valid_neg], axis=0)
    train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))]
    valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))]
    train_scalar, train_scalar_seconds = scalar_features(adj, train_pairs)
    valid_scalar, valid_scalar_seconds = scalar_features(adj, valid_pairs)
    train_nb, train_nb_seconds = nb_matrix(adj, train_pairs), 0.0
    valid_nb, valid_nb_seconds = nb_matrix(adj, valid_pairs), 0.0
    train_true = np.c_[train_scalar, train_nb]
    valid_true = np.c_[valid_scalar, valid_nb]
    train_shuffled = stratified_shuffle(train_nb, train_scalar, 91000 + seed)
    valid_shuffled = stratified_shuffle(valid_nb, valid_scalar, 92000 + seed)
    matrices = {
        "Base": (train_scalar, valid_scalar),
        "TrueNB": (train_true, valid_true),
        "ShuffledNB": (np.c_[train_scalar, train_shuffled], np.c_[valid_scalar, valid_shuffled]),
        "Proxy": (np.c_[train_scalar, proxy_matrix(train_scalar)], np.c_[valid_scalar, proxy_matrix(valid_scalar)]),
    }
    metrics, predictions = {}, {}
    for name, (train_x, valid_x) in matrices.items():
        metrics[name], predictions[name] = fit(train_x, train_y, valid_x, valid_y)
    l3 = valid_scalar[:, 4]
    regimes = []
    for label, lo, hi in (("L3=0", 0, 0), ("L3=1-3", 1, 3), ("L3>=4", 4, np.inf)):
        mask = (l3 >= lo) & (l3 <= hi)
        if int(mask.sum()) == 0 or len(np.unique(valid_y[mask])) < 2:
            continue
        true_auc = float(roc_auc_score(valid_y[mask], predictions["TrueNB"][mask]))
        base_auc = float(roc_auc_score(valid_y[mask], predictions["Base"][mask]))
        shuf_auc = float(roc_auc_score(valid_y[mask], predictions["ShuffledNB"][mask]))
        regimes.append({"regime": label, "n": int(mask.sum()), "true_minus_base_auc": true_auc - base_auc, "true_minus_shuffled_auc": true_auc - shuf_auc})
    return {"seed": seed, "support": support, "metrics": metrics, "delta_auc": {"true_minus_base": metrics["TrueNB"]["auc"] - metrics["Base"]["auc"], "true_minus_shuffled": metrics["TrueNB"]["auc"] - metrics["ShuffledNB"]["auc"], "true_minus_proxy": metrics["TrueNB"]["auc"] - metrics["Proxy"]["auc"]}, "regimes": regimes, "extract_seconds": {"scalar_train": train_scalar_seconds, "scalar_valid": valid_scalar_seconds, "nb_train": train_nb_seconds, "nb_valid": valid_nb_seconds}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()
    result = {"candidate": "R3-01 Non-Backtracking Continuation Profile", "runs": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if path.exists():
            result["runs"].append(run_seed(path, seed))
    result["aggregate"] = {}
    for name in ("Base", "TrueNB", "ShuffledNB", "Proxy"):
        rows = [row["metrics"][name] for row in result["runs"]]
        result["aggregate"][name] = {metric + "_mean": float(np.mean([row[metric] for row in rows])) for metric in ("auc", "ap")}
    result["delta_aggregate"] = {key: float(np.mean([row["delta_auc"][key] for row in result["runs"]])) for key in ("true_minus_base", "true_minus_shuffled", "true_minus_proxy")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"candidate": result["candidate"], "aggregate": result["aggregate"], "delta_aggregate": result["delta_aggregate"], "runs": result["runs"]}, indent=2))


if __name__ == "__main__":
    main()
