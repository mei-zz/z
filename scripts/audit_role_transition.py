"""Stage-0/Stage-1 audit for a pair-conditioned role-transition object.

The candidate object is a symmetric histogram over the degree-shell roles of
the two internal nodes on length-3 u-a-b-v paths.  The total path count is
already controlled separately by L3; the hypothesis is that the joint role
transition pattern contains information beyond that scalar and beyond the
existing CN/AA/RA/degree/L3/CH2-L3/CH3-L3 controls.

No GNN, attention, gate, extra loss, or test-label tuning is used here.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


ROLE_DIM = 4
ROLE_FEATURE_DIM = ROLE_DIM * (ROLE_DIM + 1) // 2
ROLE_PAIRS = [(i, j) for i in range(ROLE_DIM) for j in range(i, ROLE_DIM)]


def build_adjacency(edges: np.ndarray, n: int) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for x, y in np.asarray(edges, dtype=np.int64):
        x, y = int(x), int(y)
        if x != y:
            adj[x].add(y)
            adj[y].add(x)
    return adj


def role_bucket(degree: int) -> int:
    if degree <= 2:
        return 0
    if degree <= 4:
        return 1
    if degree <= 8:
        return 2
    return 3


def pair_object(adj: list[set[int]], u: int, v: int) -> dict[str, object]:
    """Compute scalar controls plus the symmetric role-transition histogram."""
    nu, nv = adj[u], adj[v]
    common = (nu & nv) - {u, v}
    degree_product = len(nu) * len(nv)
    role = np.zeros(ROLE_FEATURE_DIM, dtype=np.float64)
    l3 = 0
    ch2 = 0.0
    ch3 = 0.0
    local_community = nu | nv | {u, v}

    # Iterating from the smaller endpoint neighborhood keeps the extraction
    # cost bounded on the sparse Cora graph.
    if len(nu) <= len(nv):
        first, second = nu, nv
        flipped = False
    else:
        first, second = nv, nu
        flipped = True
    second_lookup = second
    for a in first:
        for b in adj[a]:
            if b not in second_lookup or a == v or b == u or a == b:
                continue
            l3 += 1
            left, right = (b, a) if flipped else (a, b)
            bi = role_bucket(len(adj[left]))
            bj = role_bucket(len(adj[right]))
            key = (min(bi, bj), max(bi, bj))
            role[ROLE_PAIRS.index(key)] += 1.0

            a_internal = len(adj[a] & local_community)
            a_external = len(adj[a] - local_community)
            b_internal = len(adj[b] & local_community)
            b_external = len(adj[b] - local_community)
            ch2 += math.sqrt((1 + a_internal) * (1 + b_internal)) / math.sqrt(
                (1 + a_external) * (1 + b_external)
            )
            ch3 += 1.0 / math.sqrt((1 + a_external) * (1 + b_external))

    aa = sum(1.0 / math.log1p(len(adj[x])) for x in common)
    ra = sum(1.0 / max(1, len(adj[x])) for x in common)
    return {
        "cn": float(len(common)),
        "aa": float(aa),
        "ra": float(ra),
        "degree_product": float(degree_product),
        "l3": float(l3),
        "local_path": float(len(common) + 0.01 * l3),
        "ch2_l3": float(ch2),
        "ch3_l3": float(ch3),
        "role": role,
    }


def sample_train_negatives(all_positive: np.ndarray, n: int, seed: int, count: int) -> np.ndarray:
    known = {tuple(sorted((int(x), int(y)))) for x, y in all_positive}
    rng = np.random.default_rng(10000 + seed)
    negatives: list[tuple[int, int]] = []
    while len(negatives) < count:
        u, v = int(rng.integers(n)), int(rng.integers(n))
        if u == v:
            continue
        pair = tuple(sorted((u, v)))
        if pair not in known:
            known.add(pair)
            negatives.append(pair)
    return np.asarray(negatives, dtype=np.int64)


def scalar_matrix(features: list[dict[str, object]]) -> np.ndarray:
    return np.asarray(
        [
            [
                float(item["cn"]),
                float(item["aa"]),
                float(item["ra"]),
                math.log1p(float(item["degree_product"])),
                float(item["l3"]),
                float(item["local_path"]),
                float(item["ch2_l3"]),
                float(item["ch3_l3"]),
            ]
            for item in features
        ],
        dtype=np.float64,
    )


def role_matrix(features: list[dict[str, object]]) -> np.ndarray:
    return np.asarray([np.asarray(item["role"], dtype=np.float64) for item in features])


def fit_predictions(train_x: np.ndarray, train_y: np.ndarray, valid_x: np.ndarray, valid_y: np.ndarray):
    model = make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=800, solver="liblinear")
    )
    model.fit(train_x, train_y)
    probabilities = model.predict_proba(valid_x)[:, 1]
    metrics = {
        "auc": float(roc_auc_score(valid_y, probabilities)),
        "ap": float(average_precision_score(valid_y, probabilities)),
    }
    return metrics, probabilities


def stratified_shuffle(values: np.ndarray, scalar: np.ndarray, seed: int) -> np.ndarray:
    """Shuffle only the candidate object within label-independent controls."""
    rng = np.random.default_rng(seed)
    shuffled = values.copy()
    strata: dict[tuple[float, ...], list[int]] = defaultdict(list)
    for index, row in enumerate(scalar):
        # Rounded continuous controls avoid singleton strata while preserving
        # the marginal scale of CN/L3/degree regimes.
        key = (
            float(round(row[0], 3)),
            float(round(row[4], 3)),
            float(round(row[3], 3)),
        )
        strata[key].append(index)
    for indices in strata.values():
        if len(indices) > 1:
            source = np.asarray(indices, dtype=np.int64)
            shuffled[indices] = values[rng.permutation(source)]
    return shuffled


def compute_features(adj, pairs: np.ndarray) -> tuple[list[dict[str, object]], float]:
    start = os.times().elapsed
    features = [pair_object(adj, int(u), int(v)) for u, v in pairs]
    return features, float(os.times().elapsed - start)


def support_for_seed(path: Path, adj: list[set[int]], seed: int) -> dict:
    data = np.load(path, allow_pickle=False)
    positives = np.asarray(data["test_pos"], dtype=np.int64)
    negatives = np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2)
    rows = []
    for label, pairs in ((1, positives), (0, negatives)):
        feats, seconds = compute_features(adj, pairs)
        role = role_matrix(feats)
        row = {
            "seed": seed,
            "label": label,
            "total": int(len(pairs)),
            "role_nonzero": int(np.sum(np.sum(role, axis=1) > 0)),
            "role_ge2": int(np.sum(np.sum(role, axis=1) >= 2)),
            "role_ge5": int(np.sum(np.sum(role, axis=1) >= 5)),
            "unique_role_states": int(np.sum(np.count_nonzero(role, axis=1) > 1)),
            "mean_role_paths": float(np.mean(np.sum(role, axis=1))),
            "max_role_paths": int(np.max(np.sum(role, axis=1))) if len(role) else 0,
            "extract_seconds": seconds,
        }
        rows.append(row)
    return {"seed": seed, "rows": rows}


def probe_for_seed(path: Path, adj: list[set[int]], seed: int) -> dict:
    data = np.load(path, allow_pickle=False)
    n = int(data["num_nodes"])
    train_pos = np.asarray(data["train_pos"], dtype=np.int64)
    train_neg = sample_train_negatives(np.asarray(data["all_positive"], dtype=np.int64), n, seed, len(train_pos))
    valid_pos = np.asarray(data["valid_pos"], dtype=np.int64)
    valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]
    train_pairs = np.concatenate([train_pos, train_neg], axis=0)
    valid_pairs = np.concatenate([valid_pos, valid_neg], axis=0)
    train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))]
    valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))]

    train_features, train_seconds = compute_features(adj, train_pairs)
    valid_features, valid_seconds = compute_features(adj, valid_pairs)
    train_scalar = scalar_matrix(train_features)
    valid_scalar = scalar_matrix(valid_features)
    train_role = role_matrix(train_features)
    valid_role = role_matrix(valid_features)
    train_shuffled = stratified_shuffle(train_role, train_scalar, 20000 + seed)
    valid_shuffled = stratified_shuffle(valid_role, valid_scalar, 30000 + seed)

    matrices = {
        "Base": (train_scalar[:, :4], valid_scalar[:, :4]),
        "BasePlusL3": (train_scalar[:, :6], valid_scalar[:, :6]),
        "DangerousControls": (train_scalar, valid_scalar),
        "TrueRole": (np.c_[train_scalar, train_role], np.c_[valid_scalar, valid_role]),
        "ShuffledRole": (np.c_[train_scalar, train_shuffled], np.c_[valid_scalar, valid_shuffled]),
    }
    metrics = {}
    probabilities = {}
    for name, (train_x, valid_x) in matrices.items():
        metrics[name], probabilities[name] = fit_predictions(train_x, train_y, valid_x, valid_y)

    valid_l3 = valid_scalar[:, 4]
    regime_bins = [("L3=0", 0, 0), ("L3=1", 1, 1), ("L3=2-3", 2, 3), ("L3=4-7", 4, 7), ("L3>=8", 8, np.inf)]
    regime_metrics = []
    for regime, lower, upper in regime_bins:
        mask = (valid_l3 >= lower) & (valid_l3 <= upper)
        if int(mask.sum()) == 0 or len(np.unique(valid_y[mask])) < 2:
            regime_metrics.append({"regime": regime, "n": int(mask.sum()), "true_auc": None, "control_auc": None, "shuffled_auc": None, "true_minus_control_auc": None, "true_minus_shuffled_auc": None})
            continue
        true_auc = float(roc_auc_score(valid_y[mask], probabilities["TrueRole"][mask]))
        control_auc = float(roc_auc_score(valid_y[mask], probabilities["DangerousControls"][mask]))
        shuffled_auc = float(roc_auc_score(valid_y[mask], probabilities["ShuffledRole"][mask]))
        regime_metrics.append({
            "regime": regime,
            "n": int(mask.sum()),
            "true_auc": true_auc,
            "control_auc": control_auc,
            "shuffled_auc": shuffled_auc,
            "true_minus_control_auc": true_auc - control_auc,
            "true_minus_shuffled_auc": true_auc - shuffled_auc,
        })
    return {
        "dataset": "cora_heart",
        "seed": seed,
        "train_pairs": int(len(train_pairs)),
        "valid_pairs": int(len(valid_pairs)),
        "train_positive": int(len(train_pos)),
        "valid_positive": int(len(valid_pos)),
        "metrics": metrics,
        "candidate_minus_controls_auc": float(metrics["TrueRole"]["auc"] - metrics["DangerousControls"]["auc"]),
        "candidate_minus_shuffled_auc": float(metrics["TrueRole"]["auc"] - metrics["ShuffledRole"]["auc"]),
        "candidate_minus_controls_ap": float(metrics["TrueRole"]["ap"] - metrics["DangerousControls"]["ap"]),
        "candidate_minus_shuffled_ap": float(metrics["TrueRole"]["ap"] - metrics["ShuffledRole"]["ap"]),
        "regime_metrics": regime_metrics,
        "train_extract_seconds": train_seconds,
        "valid_extract_seconds": valid_seconds,
        "role_dim": int(train_role.shape[1]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()

    result = {"candidate": "R1-07 Neighbor-Role Transition Matrix", "support": [], "probes": [], "seed_detail": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if not path.exists():
            continue
        data = np.load(path, allow_pickle=False)
        n = int(data["num_nodes"])
        adj = build_adjacency(np.asarray(data["train_pos"], dtype=np.int64), n)
        support = support_for_seed(path, adj, seed)
        result["support"].extend(support["rows"])
        result["probes"].append(probe_for_seed(path, adj, seed))
        result["seed_detail"].append({
            "seed": seed,
            "nodes": n,
            "train_pos": int(len(data["train_pos"])),
            "valid_pos": int(len(data["valid_pos"])),
            "test_pos": int(len(data["test_pos"])),
        })

    result["support_aggregate"] = {}
    for label in (1, 0):
        rows = [row for row in result["support"] if row["label"] == label]
        total = sum(row["total"] for row in rows)
        result["support_aggregate"][str(label)] = {
            "total": total,
            "role_nonzero": sum(row["role_nonzero"] for row in rows),
            "role_ge2": sum(row["role_ge2"] for row in rows),
            "role_ge5": sum(row["role_ge5"] for row in rows),
            "unique_role_states": sum(row["unique_role_states"] for row in rows),
            "mean_role_paths": float(sum(row["mean_role_paths"] * row["total"] for row in rows) / total) if total else None,
        }

    result["probe_aggregate"] = {}
    for name in ("Base", "BasePlusL3", "DangerousControls", "TrueRole", "ShuffledRole"):
        rows = [row["metrics"][name] for row in result["probes"]]
        result["probe_aggregate"][name] = {
            "auc_mean": float(np.mean([row["auc"] for row in rows])),
            "auc_std": float(np.std([row["auc"] for row in rows], ddof=1)) if len(rows) > 1 else 0.0,
            "ap_mean": float(np.mean([row["ap"] for row in rows])),
            "ap_std": float(np.std([row["ap"] for row in rows], ddof=1)) if len(rows) > 1 else 0.0,
        }
    result["delta_aggregate"] = {
        key: float(np.mean([row[key] for row in result["probes"]]))
        for key in (
            "candidate_minus_controls_auc",
            "candidate_minus_shuffled_auc",
            "candidate_minus_controls_ap",
            "candidate_minus_shuffled_ap",
        )
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "candidate": result["candidate"],
        "support_aggregate": result["support_aggregate"],
        "probe_aggregate": result["probe_aggregate"],
        "delta_aggregate": result["delta_aggregate"],
        "seeds": result["seed_detail"],
    }, indent=2))


if __name__ == "__main__":
    main()
