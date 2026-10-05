"""Stage-0/Stage-1 audit for CECG versus L3 and graphlet controls.

This script deliberately contains no GNN, trainable attention, gate, expert,
or message-passing implementation. It reads the repository's leakage-safe
processed npz files and writes structural support plus logistic probes.
"""
import argparse
import hashlib
import json
import math
import os
from collections import Counter, defaultdict
from itertools import combinations, permutations
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_adjacency(edges: np.ndarray, n: int):
    adj = [set() for _ in range(n)]
    for x, y in np.asarray(edges, dtype=np.int64):
        x, y = int(x), int(y)
        if x != y:
            adj[x].add(y)
            adj[y].add(x)
    return adj


def graphlet_keys():
    edge_positions = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    def canonical(mask: int) -> int:
        variants = []
        for perm in permutations(range(4)):
            bits = 0
            for bit, (i, j) in enumerate(edge_positions):
                a, b = sorted((perm[i], perm[j]))
                if mask & (1 << edge_positions.index((a, b))):
                    bits |= 1 << bit
            variants.append(bits)
        return min(variants)

    return sorted({canonical(mask) for mask in range(64)}), canonical


GRAPHLET_KEYS, CANONICAL_GRAPHLET = graphlet_keys()
GRAPHLET_MASK_TO_KEY = {
    mask: CANONICAL_GRAPHLET(mask) for mask in range(64)
}


def graphlet_proxy(adj, u: int, v: int):
    edge_positions = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    local_nodes = (adj[u] | adj[v]) - {u, v}
    counts: Counter[int] = Counter()
    for x, y in combinations(sorted(local_nodes), 2):
        nodes = [u, v, x, y]
        mask = 0
        for bit, (i, j) in enumerate(edge_positions):
            if nodes[j] in adj[nodes[i]]:
                mask |= 1 << bit
        counts[GRAPHLET_MASK_TO_KEY[mask]] += 1
    return [float(counts[key]) for key in GRAPHLET_KEYS]


def stable_bucket(value: str, buckets: int = 16) -> int:
    return int(hashlib.md5(value.encode("utf-8")).hexdigest()[:8], 16) % buckets


def pair_features(adj, u: int, v: int, descriptors: bool = False):
    nu, nv = adj[u], adj[v]
    common = nu & nv
    a_side = nu - nv - {v}
    b_side = nv - nu - {u}

    witnesses = []
    if len(a_side) <= len(b_side):
        for a in a_side:
            for b in adj[a]:
                if b in b_side:
                    witnesses.append((a, b))
    else:
        for b in b_side:
            for a in adj[b]:
                if a in a_side:
                    witnesses.append((a, b))
    witnesses.sort()

    # For a non-edge, this is the ordinary (A^3)uv length-3 walk/path count.
    full_l3 = 0
    for a in nu:
        for b in adj[a]:
            if v in adj[b]:
                full_l3 += 1

    local_community = nu | nv | {u, v}
    ch2 = 0.0
    ch3 = 0.0
    for a, b in witnesses:
        a_internal = len(adj[a] & local_community)
        a_external = len(adj[a] - local_community)
        b_internal = len(adj[b] & local_community)
        b_external = len(adj[b] - local_community)
        ch2 += math.sqrt((1 + a_internal) * (1 + b_internal)) / math.sqrt(
            (1 + a_external) * (1 + b_external)
        )
        ch3 += 1.0 / math.sqrt((1 + a_external) * (1 + b_external))

    result = {
        "cn": float(len(common)),
        "aa": float(sum(1.0 / math.log1p(len(adj[x])) for x in common)),
        "ra": float(sum(1.0 / max(1, len(adj[x])) for x in common)),
        "degree_product": float(len(nu) * len(nv)),
        "l3": float(full_l3),
        "l3_exclusive": float(len(witnesses)),
        "local_path": float(len(common) + 0.01 * full_l3),
        "ch2_l3": float(ch2),
        "ch3_l3": float(ch3),
    }
    if not descriptors:
        return result

    # Path-interaction graph: one node per exclusive L3 witness. Edges are
    # typed A/B in the conceptual object; descriptors below use their union.
    witness_count = len(witnesses)
    union_parent = list(range(witness_count))
    interaction_adj = [set() for _ in range(witness_count)]

    def find(index: int) -> int:
        while union_parent[index] != index:
            union_parent[index] = union_parent[union_parent[index]]
            index = union_parent[index]
        return index

    def union(left: int, right: int) -> None:
        left, right = find(left), find(right)
        if left != right:
            union_parent[right] = left

    by_a = defaultdict(list)
    by_b = defaultdict(list)
    for index, (a, b) in enumerate(witnesses):
        by_a[a].append(index)
        by_b[b].append(index)

    for groups in (by_a.values(), by_b.values()):
        for indices in groups:
            for left, right in combinations(indices, 2):
                union(left, right)
                interaction_adj[left].add(right)
                interaction_adj[right].add(left)

    components = Counter(find(index) for index in range(witness_count))
    degrees = [len(neighbors) for neighbors in interaction_adj]
    a_sharing = Counter(min(8, len(indices)) for indices in by_a.values())
    b_sharing = Counter(min(8, len(indices)) for indices in by_b.values())

    # Fixed two-round WL histogram. The raw L3 counts are intentionally not
    # included in the returned CECG vector; they remain P1 controls.
    colors = ["0"] * witness_count
    wl_histogram = [0] * 16
    for _ in range(2):
        next_colors = []
        for index in range(witness_count):
            signature = colors[index] + "|" + ",".join(
                sorted(colors[neighbor] for neighbor in interaction_adj[index])
            )
            next_colors.append(str(stable_bucket(signature)))
        colors = next_colors
        for color in colors:
            wl_histogram[int(color)] += 1

    # No l3/l3_exclusive scalar is returned here: P1 already owns L3 and P4
    # must prove incremental topology beyond that count.
    cecg = [
        float(len(by_a)),
        float(len(by_b)),
        float(len(components)),
        float(max(components.values()) / witness_count if witness_count else 0.0),
        float(np.mean(degrees) if degrees else 0.0),
        float(max(degrees) if degrees else 0),
    ]
    cecg += [float(a_sharing[k]) for k in range(1, 9)]
    cecg += [float(b_sharing[k]) for k in range(1, 9)]
    cecg += [float(value) for value in wl_histogram]
    result["cecg"] = cecg
    return result


def sample_train_negatives(all_positive: np.ndarray, n: int, seed: int, count: int):
    known = {tuple(sorted((int(x), int(y)))) for x, y in all_positive}
    rng = np.random.default_rng(10000 + seed)
    negatives = []
    while len(negatives) < count:
        u, v = int(rng.integers(n)), int(rng.integers(n))
        if u == v:
            continue
        pair = tuple(sorted((u, v)))
        if pair not in known:
            known.add(pair)
            negatives.append(pair)
    return np.asarray(negatives, dtype=np.int64)


def base_matrix(features: list) -> np.ndarray:
    return np.asarray(
        [
            [
                item["cn"],
                item["aa"],
                item["ra"],
                math.log1p(item["degree_product"]),
            ]
            for item in features
        ],
        dtype=np.float64,
    )


def p1_matrix(features: list) -> np.ndarray:
    return np.c_[
        base_matrix(features),
        np.asarray(
            [[item["l3"], item["local_path"]] for item in features], dtype=np.float64
        ),
    ]


def p2_matrix(features: list) -> np.ndarray:
    return np.c_[
        p1_matrix(features),
        np.asarray(
            [[item["ch2_l3"], item["ch3_l3"]] for item in features], dtype=np.float64
        ),
    ]


def fit_predictions(
    train_x: np.ndarray,
    train_y: np.ndarray,
    valid_x: np.ndarray,
    valid_y: np.ndarray,
):
    model = make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=500, solver="liblinear")
    )
    model.fit(train_x, train_y)
    probabilities = model.predict_proba(valid_x)[:, 1]
    return {
        "auc": float(roc_auc_score(valid_y, probabilities)),
        "ap": float(average_precision_score(valid_y, probabilities)),
    }, probabilities


def support_rows(npz_path: Path, adj, seed: int):
    data = np.load(npz_path, allow_pickle=True)
    positives = np.asarray(data["test_pos"], dtype=np.int64)
    negatives = np.asarray(data["test_neg"], dtype=np.int64).reshape(-1, 2)
    rows = []
    for label, pairs in ((1, positives), (0, negatives)):
        values = np.asarray(
            [pair_features(adj, int(u), int(v))["l3_exclusive"] for u, v in pairs],
            dtype=np.float64,
        )
        rows.append(
            {
                "dataset": "cora",
                "seed": seed,
                "label": label,
                "total": int(len(values)),
                "l3_gt0": int(np.sum(values > 0)),
                "l3_ge2": int(np.sum(values >= 2)),
                "l3_ge5": int(np.sum(values >= 5)),
                "mean_l3_exclusive": float(np.mean(values)),
            }
        )
    return rows


def probe_for_seed(npz_path: Path, adj, seed: int):
    data = np.load(npz_path, allow_pickle=True)
    n = int(data["num_nodes"])
    train_pos = np.asarray(data["train_pos"], dtype=np.int64)
    train_neg = sample_train_negatives(
        np.asarray(data["all_positive"], dtype=np.int64), n, seed, len(train_pos)
    )
    valid_pos = np.asarray(data["valid_pos"], dtype=np.int64)
    valid_neg = np.asarray(data["valid_neg"], dtype=np.int64)[:, 0, :]
    train_pairs = np.concatenate([train_pos, train_neg], axis=0)
    valid_pairs = np.concatenate([valid_pos, valid_neg], axis=0)
    train_y = np.r_[np.ones(len(train_pos)), np.zeros(len(train_neg))]
    valid_y = np.r_[np.ones(len(valid_pos)), np.zeros(len(valid_neg))]

    train_start = os.times().elapsed
    train_features = [
        pair_features(adj, int(u), int(v), descriptors=True) for u, v in train_pairs
    ]
    train_seconds = os.times().elapsed - train_start
    valid_start = os.times().elapsed
    valid_features = [
        pair_features(adj, int(u), int(v), descriptors=True) for u, v in valid_pairs
    ]
    valid_seconds = os.times().elapsed - valid_start

    train_graphlets = np.asarray(
        [graphlet_proxy(adj, int(u), int(v)) for u, v in train_pairs], dtype=np.float64
    )
    valid_graphlets = np.asarray(
        [graphlet_proxy(adj, int(u), int(v)) for u, v in valid_pairs], dtype=np.float64
    )
    train_base, valid_base = base_matrix(train_features), base_matrix(valid_features)
    train_p1, valid_p1 = p1_matrix(train_features), p1_matrix(valid_features)
    train_p2, valid_p2 = p2_matrix(train_features), p2_matrix(valid_features)
    train_p3 = np.c_[train_p2, train_graphlets]
    valid_p3 = np.c_[valid_p2, valid_graphlets]
    train_p4 = np.c_[train_p3, np.asarray([f["cecg"] for f in train_features])]
    valid_p4 = np.c_[valid_p3, np.asarray([f["cecg"] for f in valid_features])]

    metrics = {}
    probabilities = {}
    matrices = {
        "P0": (train_base, valid_base),
        "P1": (train_p1, valid_p1),
        "P2": (train_p2, valid_p2),
        "P3": (train_p3, valid_p3),
        "P4": (train_p4, valid_p4),
    }
    for name, (train_x, valid_x) in matrices.items():
        metrics[name], probabilities[name] = fit_predictions(
            train_x, train_y, valid_x, valid_y
        )

    l3_values = np.asarray([f["l3"] for f in valid_features])
    bins = [("0", 0, 0), ("1", 1, 1), ("2-3", 2, 3), ("4-7", 4, 7), (">=8", 8, np.inf)]
    matched = []
    for name, lower, upper in bins:
        mask = (l3_values >= lower) & (l3_values <= upper)
        if int(mask.sum()) == 0 or len(np.unique(valid_y[mask])) < 2:
            matched.append({"bin": name, "n": int(mask.sum()), "p3_auc": None, "p4_auc": None, "delta_auc": None})
            continue
        p3_auc = float(roc_auc_score(valid_y[mask], probabilities["P3"][mask]))
        p4_auc = float(roc_auc_score(valid_y[mask], probabilities["P4"][mask]))
        matched.append({"bin": name, "n": int(mask.sum()), "p3_auc": p3_auc, "p4_auc": p4_auc, "delta_auc": p4_auc - p3_auc})

    return {
        "dataset": "cora",
        "seed": seed,
        "train_pairs": int(len(train_pairs)),
        "valid_pairs": int(len(valid_pairs)),
        "metrics": metrics,
        "matched_l3": matched,
        "train_seconds": float(train_seconds),
        "valid_seconds": float(valid_seconds),
        "cecg_dim": int(train_p4.shape[1] - train_p3.shape[1]),
        "graphlet_dim": int(train_graphlets.shape[1]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    args = parser.parse_args()

    result: dict = {"support": [], "probes": [], "seed_detail": []}
    for seed in args.seeds:
        path = args.data_root / f"cora_heart_seed{seed}.npz"
        if not path.exists():
            continue
        data = np.load(path, allow_pickle=True)
        n = int(data["num_nodes"])
        adj = build_adjacency(data["train_pos"], n)
        result["support"].extend(support_rows(path, adj, seed))
        result["probes"].append(probe_for_seed(path, adj, seed))
        result["seed_detail"].append(
            {
                "seed": seed,
                "nodes": n,
                "train_pos": int(len(data["train_pos"])),
                "valid_pos": int(len(data["valid_pos"])),
                "test_pos": int(len(data["test_pos"])),
            }
        )

    aggregate_support = []
    for label in (1, 0):
        rows = [row for row in result["support"] if row["label"] == label]
        total = sum(row["total"] for row in rows)
        aggregate_support.append(
            {
                "dataset": "cora",
                "label": label,
                "total": total,
                "l3_gt0": sum(row["l3_gt0"] for row in rows),
                "l3_ge2": sum(row["l3_ge2"] for row in rows),
                "l3_ge5": sum(row["l3_ge5"] for row in rows),
                "mean_l3_exclusive": sum(
                    row["mean_l3_exclusive"] * row["total"] for row in rows
                )
                / total
                if total
                else None,
            }
        )
    result["support_aggregate"] = aggregate_support

    result["probe_aggregate"] = {}
    for name in ("P0", "P1", "P2", "P3", "P4"):
        rows = [row["metrics"][name] for row in result["probes"]]
        result["probe_aggregate"][name] = {
            "auc_mean": float(np.mean([row["auc"] for row in rows])),
            "auc_std": float(np.std([row["auc"] for row in rows], ddof=1)),
            "ap_mean": float(np.mean([row["ap"] for row in rows])),
            "ap_std": float(np.std([row["ap"] for row in rows], ddof=1)),
        }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({
        "support_aggregate": result["support_aggregate"],
        "probe_aggregate": result["probe_aggregate"],
        "seeds": result["seed_detail"],
    }, indent=2))


if __name__ == "__main__":
    main()
