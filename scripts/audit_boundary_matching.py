r"""Stage-0/Stage-1 audit for a boundary matching/cover profile.

For a candidate pair (u,v), form the bipartite graph induced by the two
exclusive one-hop neighborhoods A=N(u)\N(v) and B=N(v)\N(u).  The candidate
object is the maximum matching/deficiency profile of this boundary graph,
not the raw number of cross-boundary edges used by CECG.
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


MATCH_DIM = 8


def build_adjacency(edges: np.ndarray, n: int) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for x, y in np.asarray(edges, dtype=np.int64):
        x, y = int(x), int(y)
        if x != y:
            adj[x].add(y)
            adj[y].add(x)
    return adj


def maximum_boundary_matching(adj: list[set[int]], left: list[int], right: set[int]) -> int:
    """Exact augmenting-path matching on the small local boundary graph."""
    left_to_right = {a: [b for b in adj[a] if b in right] for a in left}
    matched_right: dict[int, int] = {}

    def augment(a: int, seen: set[int]) -> bool:
        for b in left_to_right[a]:
            if b in seen:
                continue
            seen.add(b)
            if b not in matched_right or augment(matched_right[b], seen):
                matched_right[b] = a
                return True
        return False

    size = 0
    for a in left:
        if augment(a, set()):
            size += 1
    return size


def pair_object(adj: list[set[int]], u: int, v: int) -> dict[str, object]:
    nu, nv = adj[u], adj[v]
    left = sorted(nu - nv - {v})
    right = nv - nu - {u}
    left_size, right_size = len(left), len(right)
    matching = maximum_boundary_matching(adj, left, right)
    min_side = min(left_size, right_size)
    profile = np.asarray(
        [
            float(matching),
            float(left_size - matching),
            float(right_size - matching),
            float(matching / max(1, min_side)),
            float(matching == min_side and min_side > 0),
            float(left_size),
            float(right_size),
            float(abs(left_size - right_size)),
        ],
        dtype=np.float64,
    )
    common = (nu & nv) - {u, v}
    l3 = 0
    if len(nu) <= len(nv):
        first, second = nu, nv
    else:
        first, second = nv, nu
    for a in first:
        l3 += sum(1 for b in adj[a] if b in second and a != v and b != u and a != b)
    aa = sum(1.0 / math.log1p(len(adj[x])) for x in common)
    ra = sum(1.0 / max(1, len(adj[x])) for x in common)
    return {
        "cn": float(len(common)),
        "aa": float(aa),
        "ra": float(ra),
        "degree_product": float(len(nu) * len(nv)),
        "l3": float(l3),
        "local_path": float(len(common) + 0.01 * l3),
        "matching": profile,
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
            ]
            for item in features
        ],
        dtype=np.float64,
    )


def matching_matrix(features: list[dict[str, object]]) -> np.ndarray:
    return np.asarray([np.asarray(item["matching"], dtype=np.float64) for item in features])


def fit_predictions(train_x: np.ndarray, train_y: np.ndarray, valid_x: np.ndarray, valid_y: np.ndarray):
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, solver="liblinear"))
    model.fit(train_x, train_y)
    probabilities = model.predict_proba(valid_x)[:, 1]
    return {
        "auc": float(roc_auc_score(valid_y, probabilities)),
        "ap": float(average_precision_score(valid_y, probabilities)),
    }


def stratified_shuffle(values: np.ndarray, scalar: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    shuffled = values.copy()
    strata: dict[tuple[float, ...], list[int]] = defaultdict(list)
    for index, row in enumerate(scalar):
        key = (float(round(row[0], 3)), float(round(row[4], 3)), float(round(row[3], 3)))
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
    rows = []
    for label, pairs in ((1, np.asarray(data["test_pos"], dtype=np.int64)), (0, np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2))):
        feats, seconds = compute_features(adj, pairs)
        match = matching_matrix(feats)
        rows.append({
            "seed": seed,
            "label": label,
            "total": int(len(pairs)),
            "matching_nonzero": int(np.sum(match[:, 0] > 0)),
            "matching_ge2": int(np.sum(match[:, 0] >= 2)),
            "perfect_boundary": int(np.sum(match[:, 4] > 0)),
            "mean_matching": float(np.mean(match[:, 0])),
            "mean_left_deficiency": float(np.mean(match[:, 1])),
            "mean_right_deficiency": float(np.mean(match[:, 2])),
            "extract_seconds": seconds,
        })
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
    train_scalar, valid_scalar = scalar_matrix(train_features), scalar_matrix(valid_features)
    train_match, valid_match = matching_matrix(train_features), matching_matrix(valid_features)
    train_shuffled = stratified_shuffle(train_match, train_scalar, 20000 + seed)
    valid_shuffled = stratified_shuffle(valid_match, valid_scalar, 30000 + seed)
    matrices = {
        "Base": (train_scalar[:, :4], valid_scalar[:, :4]),
        "DangerousControls": (train_scalar, valid_scalar),
        "TrueMatch": (np.c_[train_scalar, train_match], np.c_[valid_scalar, valid_match]),
        "ShuffledMatch": (np.c_[train_scalar, train_shuffled], np.c_[valid_scalar, valid_shuffled]),
    }
    metrics = {name: fit_predictions(x, train_y, y, valid_y) for name, (x, y) in matrices.items()}
    proxy_train = np.c_[np.log1p(np.maximum(train_scalar[:, 4], 0)), np.sqrt(np.maximum(train_scalar[:, 4], 0)), np.log1p(np.maximum(train_scalar[:, 0], 0)), np.sqrt(np.maximum(train_scalar[:, 0], 0)), train_scalar[:, 3], train_scalar[:, 3] ** 2, np.log1p(np.maximum(train_scalar[:, 5], 0)), np.sin(np.minimum(train_scalar[:, 4], 20)), np.cos(np.minimum(train_scalar[:, 4], 20))]
    proxy_valid = np.c_[np.log1p(np.maximum(valid_scalar[:, 4], 0)), np.sqrt(np.maximum(valid_scalar[:, 4], 0)), np.log1p(np.maximum(valid_scalar[:, 0], 0)), np.sqrt(np.maximum(valid_scalar[:, 0], 0)), valid_scalar[:, 3], valid_scalar[:, 3] ** 2, np.log1p(np.maximum(valid_scalar[:, 5], 0)), np.sin(np.minimum(valid_scalar[:, 4], 20)), np.cos(np.minimum(valid_scalar[:, 4], 20))]
    metrics["Proxy"] = fit_predictions(np.c_[train_scalar, proxy_train], train_y, np.c_[valid_scalar, proxy_valid], valid_y)
    return {
        "dataset": "cora_heart",
        "seed": seed,
        "metrics": metrics,
        "candidate_minus_controls_auc": float(metrics["TrueMatch"]["auc"] - metrics["DangerousControls"]["auc"]),
        "candidate_minus_shuffled_auc": float(metrics["TrueMatch"]["auc"] - metrics["ShuffledMatch"]["auc"]),
        "candidate_minus_proxy_auc": float(metrics["TrueMatch"]["auc"] - metrics["Proxy"]["auc"]),
        "candidate_minus_controls_ap": float(metrics["TrueMatch"]["ap"] - metrics["DangerousControls"]["ap"]),
        "candidate_minus_shuffled_ap": float(metrics["TrueMatch"]["ap"] - metrics["ShuffledMatch"]["ap"]),
        "candidate_minus_proxy_ap": float(metrics["TrueMatch"]["ap"] - metrics["Proxy"]["ap"]),
        "train_extract_seconds": train_seconds,
        "valid_extract_seconds": valid_seconds,
        "match_dim": MATCH_DIM,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()
    result = {"candidate": "R4-01 Boundary Matching/Cover Profile", "support": [], "probes": [], "seed_detail": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if not path.exists():
            continue
        data = np.load(path, allow_pickle=False)
        adj = build_adjacency(np.asarray(data["train_pos"], dtype=np.int64), int(data["num_nodes"]))
        result["support"].extend(support_for_seed(path, adj, seed)["rows"])
        result["probes"].append(probe_for_seed(path, adj, seed))
        result["seed_detail"].append({"seed": seed, "nodes": int(data["num_nodes"]), "train_pos": int(len(data["train_pos"])), "valid_pos": int(len(data["valid_pos"])), "test_pos": int(len(data["test_pos"]))})
    result["support_aggregate"] = {}
    for label in (1, 0):
        rows = [row for row in result["support"] if row["label"] == label]
        total = sum(row["total"] for row in rows)
        result["support_aggregate"][str(label)] = {
            "total": total,
            "matching_nonzero": sum(row["matching_nonzero"] for row in rows),
            "matching_ge2": sum(row["matching_ge2"] for row in rows),
            "perfect_boundary": sum(row["perfect_boundary"] for row in rows),
            "mean_matching": float(sum(row["mean_matching"] * row["total"] for row in rows) / total) if total else None,
        }
    result["probe_aggregate"] = {}
    for name in ("Base", "DangerousControls", "TrueMatch", "ShuffledMatch", "Proxy"):
        rows = [row["metrics"][name] for row in result["probes"]]
        result["probe_aggregate"][name] = {"auc_mean": float(np.mean([row["auc"] for row in rows])), "auc_std": float(np.std([row["auc"] for row in rows], ddof=1)) if len(rows) > 1 else 0.0, "ap_mean": float(np.mean([row["ap"] for row in rows])), "ap_std": float(np.std([row["ap"] for row in rows], ddof=1)) if len(rows) > 1 else 0.0}
    result["delta_aggregate"] = {key: float(np.mean([row[key] for row in result["probes"]])) for key in ("candidate_minus_controls_auc", "candidate_minus_shuffled_auc", "candidate_minus_proxy_auc", "candidate_minus_controls_ap", "candidate_minus_shuffled_ap", "candidate_minus_proxy_ap")}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"candidate": result["candidate"], "support_aggregate": result["support_aggregate"], "probe_aggregate": result["probe_aggregate"], "delta_aggregate": result["delta_aggregate"], "seeds": result["seed_detail"]}, indent=2))


if __name__ == "__main__":
    main()
