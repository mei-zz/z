from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
import traceback
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
ROOT = Path(os.environ.get("HMC_RUNTIME_ROOT", HERE.parents[3])).resolve()
OUT = HERE.parents[1]
V71 = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V7_1"
V61 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
V7 = ROOT / "HYPERGRAPH_RESEARCH" / "HARDNESS_V7"
V62 = ROOT / "HYPERGRAPH_RESEARCH" / "CODNS_V6_2"
V8 = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V8_PAPER"
sys.path[:0] = [str(ROOT / "src"), str(V71), str(V61), str(V7), str(V62), str(V8)]

import experiment_v71 as base
import run_negative_v6_1 as v61
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

EXPECTED_SPLIT = "c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a"
EXPECTED_POOL = "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba"
MATCH_SEED = 20261003
SHUFFLE_SEED = 150015


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def adjacency(n: int, edges: np.ndarray) -> list[set[int]]:
    adj = [set() for _ in range(n)]
    for u, v in np.asarray(edges, dtype=np.int64).reshape(-1, 2):
        u, v = int(u), int(v)
        if u == v:
            raise ValueError("self-loop in training graph")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def incidence_counts(adj: list[set[int]]) -> tuple[list[dict[int, int]], np.ndarray, np.ndarray]:
    """Raw-star co-incidence counts and q(x)=sum_e(|e|-1)."""
    n = len(adj)
    deg = np.fromiter((len(x) for x in adj), dtype=np.int64, count=n)
    counts: list[dict[int, int]] = [dict() for _ in range(n)]
    strength = np.zeros(n, dtype=np.int64)
    for center, neighbors in enumerate(adj):
        d = len(neighbors)
        if not d:
            continue
        members = [center, *sorted(neighbors)]
        for node in members:
            strength[node] += d
        for u in members:
            row = counts[u]
            for w in members:
                row[w] = row.get(w, 0) + 1
    return counts, deg, strength


def corrected_row(row: dict[int, int], decrement_nodes: set[int], endpoints: set[int]) -> dict[int, int]:
    result = {}
    for w, count in row.items():
        if w in endpoints:
            continue
        count -= int(w in decrement_nodes)
        if count > 0:
            result[w] = count
    return result


def pair_stats(u: int, v: int, adj, counts, deg, strength, target_positive: bool) -> dict:
    u, v = canonical(int(u), int(v))
    endpoints = {u, v}
    if target_positive:
        if v not in adj[u]:
            raise ValueError("target mask requested for a non-edge")
        row_u = corrected_row(counts[u], adj[v], endpoints)
        row_v = corrected_row(counts[v], adj[u], endpoints)
        qu = int(strength[u] - 1 - deg[v])
        qv = int(strength[v] - 1 - deg[u])
    else:
        row_u = corrected_row(counts[u], set(), endpoints)
        row_v = corrected_row(counts[v], set(), endpoints)
        qu, qv = int(strength[u]), int(strength[v])

    shared = sorted(set(row_u).intersection(row_v))
    mu = np.fromiter((row_u[w] for w in shared), dtype=np.int64, count=len(shared))
    mv = np.fromiter((row_v[w] for w in shared), dtype=np.int64, count=len(shared))
    if target_positive:
        qw = np.fromiter(
            (int(strength[w] - int(w in adj[u]) - int(w in adj[v])) for w in shared),
            dtype=np.float64, count=len(shared),
        )
    else:
        qw = np.fromiter((strength[w] for w in shared), dtype=np.float64, count=len(shared))

    c = len(shared)
    product = mu * mv
    m = int(product.sum()) if c else 0
    e = m - c
    max_product = int(product.max()) if c else 0
    std_product = float(np.std(np.log1p(product.astype(np.float64)))) if c else 0.0
    ms = float(np.sum(np.log1p(mu) * np.log1p(mv))) if c else 0.0
    denominator = math.sqrt(max(qu, 1) * max(qv, 1)) * (1.0 + qw)
    hra = float(np.sum(1.0 / denominator)) if c else 0.0

    rng = np.random.default_rng((SHUFFLE_SEED + u * 1000003 + v * 9176) & 0xFFFFFFFF)
    perm = rng.permutation(c)
    shuffled_product = mu * (mv[perm] if c else mv)
    original_joint = sorted(zip(mu.tolist(), mv.tolist()))
    shuffled_joint = sorted(zip(mu.tolist(), (mv[perm] if c else mv).tolist()))
    return {
        "u": u, "v": v, "supports": shared, "mu": mu, "mv": mv, "C": c,
        "M": m, "E": e, "MAX": max_product, "STD": std_product, "MS": ms, "HRA": hra,
        "graph_cn": len(adj[u].intersection(adj[v])),
        "shuffle_C": c,
        "shuffle_M": int(shuffled_product.sum()) if c else 0,
        "shuffle_E": int(shuffled_product.sum() - c) if c else 0,
        "shuffle_MAX": int(shuffled_product.max()) if c else 0,
        "shuffle_STD": float(np.std(np.log1p(shuffled_product.astype(np.float64)))) if c else 0.0,
        "informative_shuffle": bool(original_joint != shuffled_joint),
    }


def full_rebuild_pair(u: int, v: int, adj: list[set[int]]) -> dict:
    rebuilt_adj = [set(x) for x in adj]
    rebuilt_adj[u].remove(v)
    rebuilt_adj[v].remove(u)
    counts, deg, strength = incidence_counts(rebuilt_adj)
    return pair_stats(u, v, rebuilt_adj, counts, deg, strength, False)


def fast_support_count(u: int, v: int, adj, counts, masked: bool) -> int:
    u, v = canonical(u, v)
    if not masked:
        return sum(1 for w in counts[u] if w not in (u, v) and w in counts[v])
    if v not in adj[u]:
        raise ValueError("target mask requested for non-edge")
    total = 0
    for w in counts[u]:
        if w in (u, v) or w not in counts[v]:
            continue
        if counts[u][w] - int(w in adj[v]) > 0 and counts[v][w] - int(w in adj[u]) > 0:
            total += 1
    return total


def degree_bins(deg: np.ndarray) -> np.ndarray:
    return np.searchsorted(np.quantile(deg, [0.2, 0.4, 0.6, 0.8]), deg, side="right")


def bin_pair(u: int, v: int, bins: np.ndarray) -> tuple[int, int]:
    return tuple(sorted((int(bins[u]), int(bins[v]))))


def match_negatives(positives, pool, adj, counts, deg, strength):
    bins = degree_bins(deg)
    chosen = []
    quality = Counter()
    tie = np.random.default_rng(MATCH_SEED).random(pool.shape[:2])
    for i, (pu, pv) in enumerate(positives):
        pu, pv = map(int, (pu, pv))
        pos = pair_stats(pu, pv, adj, counts, deg, strength, True)
        pbin = bin_pair(pu, pv, bins)
        opts = []
        for j, pair in enumerate(pool[i]):
            u, v = canonical(int(pair[0]), int(pair[1]))
            c = fast_support_count(u, v, adj, counts, False)
            cn = len(adj[u].intersection(adj[v]))
            c_gap, cn_gap = abs(c - pos["C"]), abs(cn - pos["graph_cn"])
            nbin = bin_pair(u, v, bins)
            bin_gap = abs(nbin[0] - pbin[0]) + abs(nbin[1] - pbin[1])
            exact_bin = bin_gap == 0
            exact_support, exact_cn = c_gap == 0, cn_gap == 0
            opts.append((
                int(not exact_bin), int(not (exact_support or exact_cn)), bin_gap,
                min(c_gap, cn_gap), c_gap + cn_gap, float(tie[i, j]),
                u, v, exact_bin, exact_support, exact_cn,
            ))
        opts.sort()
        for rank, item in enumerate(opts[:3]):
            _, _, _, _, _, _, u, v, exact_bin, exact_c, exact_cn = item
            if canonical(u, v) == canonical(pu, pv):
                raise ValueError("matched negative equals its positive")
            chosen.append((i, u, v))
            quality["selected_negatives"] += 1
            quality["degree_bin_exact"] += int(exact_bin)
            quality["support_count_exact"] += int(exact_c)
            quality["graph_cn_exact"] += int(exact_cn)
            quality["degree_and_support_or_cn_exact"] += int(exact_bin and (exact_c or exact_cn))
            quality[f"selection_rank_{rank+1}"] += 1
    quality["positive_count"] = len(positives)
    quality["positives_with_matches"] = len({i for i, _, _ in chosen})
    quality["max_negatives_per_positive"] = 3
    return chosen, dict(quality)


def cv_metrics(X, y, groups):
    splitter = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=20261003)
    auc, ap, sizes = [], [], []
    for train, test in splitter.split(X, y, groups):
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(C=1.0, solver="lbfgs", max_iter=2000, random_state=0),
        )
        model.fit(X[train], y[train])
        score = model.predict_proba(X[test])[:, 1]
        auc.append(float(roc_auc_score(y[test], score)))
        ap.append(float(average_precision_score(y[test], score)))
        sizes.append(int(len(test)))
    return {
        "roc_auc_by_fold": auc, "roc_auc_mean": float(np.mean(auc)),
        "roc_auc_sample_std": float(np.std(auc, ddof=1)),
        "pr_auc_by_fold": ap, "pr_auc_mean": float(np.mean(ap)),
        "pr_auc_sample_std": float(np.std(ap, ddof=1)), "fold_sizes": sizes,
    }


def token_audit(records, labels):
    output = {}
    for label, name in ((1, "train_positive"), (0, "matched_legal_negative")):
        selected = [r for r, y in zip(records, labels) if y == label]
        nonempty = [r for r in selected if len(r["mu"])]
        mu = np.concatenate([r["mu"] for r in nonempty]) if nonempty else np.zeros(0, dtype=np.int64)
        mv = np.concatenate([r["mv"] for r in nonempty]) if nonempty else np.zeros(0, dtype=np.int64)
        prod = mu * mv
        c = np.asarray([r["C"] for r in selected], dtype=np.float64)
        es = np.asarray([r["E"] for r in selected], dtype=np.float64)
        output[name] = {
            "pair_count": len(selected), "mean_support_count": float(np.mean(c)),
            "median_support_count": float(np.median(c)),
            "empty_support_pair_fraction": float(np.mean(c == 0)),
            "support_token_count": int(len(mu)),
            "p_mu_mv_eq_1_1": float(np.mean((mu == 1) & (mv == 1))) if len(mu) else None,
            "p_max_multiplicity_at_least_2": float(np.mean(np.maximum(mu, mv) >= 2)) if len(mu) else None,
            "p_min_multiplicity_at_least_2": float(np.mean(np.minimum(mu, mv) >= 2)) if len(mu) else None,
            "mean_multiplicity_product": float(np.mean(prod)) if len(prod) else None,
            "mean_extra_multiplicity_E": float(np.mean(es)),
            "median_extra_multiplicity_E": float(np.median(es)),
            "max_multiplicity_product": int(np.max(prod)) if len(prod) else 0,
        }
    return output


def run():
    started = time.perf_counter()
    status_path = OUT / "status.json"
    write_json(status_path, {
        "state": "RUNNING", "phase": "stage0", "current": "load_train_only_cora",
        "gpu_training_started": False, "test_evaluated": False,
    })

    full, view = base.init_dataset("cora")
    del full
    positives = np.asarray(view.train_pos, dtype=np.int64).reshape(-1, 2)
    split_hash = base.split_hash(view)
    if split_hash != EXPECTED_SPLIT:
        raise RuntimeError(f"frozen train split mismatch: {split_hash}")
    pool_path = V61 / "strict_train_candidates_and_selections.npz"
    with np.load(pool_path, allow_pickle=False) as archive:
        pool = np.asarray(archive["negative_candidates"], dtype=np.int64).copy()
        archived_positive = np.asarray(archive["train_positive"], dtype=np.int64).copy()
    if not np.array_equal(archived_positive, positives):
        raise RuntimeError("V6.1 train-positive order mismatch")
    pool_hash = v61.array_hash(pool)
    if pool_hash != EXPECTED_POOL:
        raise RuntimeError(f"frozen train-pool mismatch: {pool_hash}")
    if pool.shape != (len(positives), 20, 2):
        raise RuntimeError(f"unexpected train-only pool shape: {pool.shape}")
    meta = v61.load_json(V61 / "strict_pool_metadata.json")
    if meta.get("heldout_positive_identities_read_by_miner") is not False:
        raise RuntimeError("train-pool audit does not certify train-only candidate generation")

    n = int(view.num_nodes)
    adj = adjacency(n, positives)
    counts, deg, strength = incidence_counts(adj)
    eq_rng = np.random.default_rng(150515)
    sample_ids = eq_rng.choice(len(positives), size=min(100, len(positives)), replace=False)
    changed = 0
    for i in sample_ids:
        u, v = map(int, positives[i])
        local = pair_stats(u, v, adj, counts, deg, strength, True)
        rebuilt = full_rebuild_pair(u, v, adj)
        keys = ("supports", "C", "M", "E", "MAX", "MS", "HRA", "graph_cn")
        if any(local[k] != rebuilt[k] for k in keys):
            raise RuntimeError(f"local/full target-mask mismatch at {u},{v}")
        if sorted(zip(local["mu"].tolist(), local["mv"].tolist())) != sorted(zip(rebuilt["mu"].tolist(), rebuilt["mv"].tolist())):
            raise RuntimeError(f"multiplicity mismatch at {u},{v}")
        reverse = pair_stats(v, u, adj, counts, deg, strength, True)
        if local["C"] != reverse["C"] or local["MS"] != reverse["MS"] or sorted(zip(local["mu"], local["mv"])) != sorted(zip(reverse["mu"], reverse["mv"])):
            raise RuntimeError(f"endpoint symmetry failure at {u},{v}")
        changed += 1

    chosen, quality = match_negatives(positives, pool, adj, counts, deg, strength)
    records, labels, groups = [], [], []
    seen_pairs = set()
    shuffle_changed = 0
    for i, (u, v) in enumerate(positives):
        row = pair_stats(int(u), int(v), adj, counts, deg, strength, True)
        records.append(row); labels.append(1); groups.append(i)
        seen_pairs.add(canonical(int(u), int(v)))
        shuffle_changed += int(row["informative_shuffle"])
    for i, u, v in chosen:
        pair = canonical(u, v)
        if pair in seen_pairs:
            raise RuntimeError("duplicate pair across Stage-0 examples; refusing CV leakage")
        seen_pairs.add(pair)
        row = pair_stats(u, v, adj, counts, deg, strength, False)
        records.append(row); labels.append(0); groups.append(i)
        shuffle_changed += int(row["informative_shuffle"])

    y = np.asarray(labels, dtype=np.int64)
    groups = np.asarray(groups, dtype=np.int64)
    column = lambda key: np.asarray([r[key] for r in records], dtype=np.float64)
    C, M, E, MAX = (column(k) for k in ("C", "M", "E", "MAX"))
    z0 = np.log1p(C)[:, None]
    z1 = column("MS")[:, None]
    z2 = column("HRA")[:, None]
    z3 = np.column_stack([np.log1p(C), np.log1p(M), np.log1p(E), np.log1p(MAX), column("STD")])
    z4 = np.column_stack([
        np.log1p(column("shuffle_C")), np.log1p(column("shuffle_M")),
        np.log1p(column("shuffle_E")), np.log1p(column("shuffle_MAX")),
        column("shuffle_STD"),
    ])
    cv = {
        "Z0_CN_or_support_count": cv_metrics(z0, y, groups),
        "Z1_multiplicity_scalar_MS": cv_metrics(z1, y, groups),
        "Z2_HRA_like": cv_metrics(z2, y, groups),
        "Z3_real_joint_multiplicity": cv_metrics(z3, y, groups),
        "Z4_cross_side_shuffled": cv_metrics(z4, y, groups),
    }
    auc0 = cv["Z0_CN_or_support_count"]["roc_auc_mean"]
    auc1 = cv["Z1_multiplicity_scalar_MS"]["roc_auc_mean"]
    auc2 = cv["Z2_HRA_like"]["roc_auc_mean"]
    auc3 = cv["Z3_real_joint_multiplicity"]["roc_auc_mean"]
    auc4 = cv["Z4_cross_side_shuffled"]["roc_auc_mean"]
    informative = shuffle_changed / max(1, len(records))
    token = token_audit(records, y)
    pos_e = token["train_positive"]["median_extra_multiplicity_E"]
    neg_e = token["matched_legal_negative"]["median_extra_multiplicity_E"]
    power = informative >= 0.20
    gates = {
        "real_auc_gt_cn_plus_0_015": bool(auc3 > auc0 + 0.015),
        "real_auc_gt_shuffle_plus_0_010": bool(auc3 > auc4 + 0.010),
        "real_auc_at_least_both_scalar_controls": bool(auc3 >= max(auc1, auc2)),
        "positive_median_E_gt_matched_negative_median_E": bool(pos_e > neg_e),
        "informative_shuffle_fraction_at_least_0_20": bool(power),
    }
    if auc3 <= max(auc1, auc2):
        decision = "SCALAR_SUFFICIENT"
        interpretation = (
            "A scalar MS or HRA-like control beats the real joint feature set; "
            "the HMC set encoder fails the scalar-residual gate. "
            + ("LOW_SHUFFLE_POWER; real≈shuffle is not interpreted directly."
               if not power else "")
        )
    elif not power:
        decision = "NO_HMC_STRUCTURE_SIGNAL"
        interpretation = "LOW_SHUFFLE_POWER; real≈shuffle is not interpreted as direct mechanism failure, and the registered Stage-0 gate does not pass."
    elif all(gates.values()):
        decision = "ZERO_GPU_GO"
        interpretation = "Real joint multiplicity passes every corrected Stage-0 gate."
    else:
        decision = "NO_HMC_STRUCTURE_SIGNAL"
        interpretation = "At least one registered Stage-0 signal gate failed; HMC stops without tuning."

    feature_path = OUT / "diagnostics" / "stage0_train_features.npz"
    np.savez_compressed(
        feature_path, labels=y, groups=groups, Z0=z0, Z1=z1, Z2=z2, Z3=z3, Z4=z4,
    )
    source_hashes = {
        "experiment_v71.py": sha256_file(V71 / "experiment_v71.py"),
        "run_negative_v6_1.py": sha256_file(V61 / "run_negative_v6_1.py"),
        "dcdlp_hypergraph.py": sha256_file(ROOT / "src" / "dcdlp" / "models" / "hypergraph.py"),
        "hmc_zero_gpu_audit.py": sha256_file(HERE),
        "train_positive_hash": v61.array_hash(positives),
        "train_pool_hash": pool_hash,
    }
    result = {
        "state": "COMPLETE", "stage": "zero_gpu_signal_audit", "dataset": "cora",
        "strict_train_only": True, "split_hash": split_hash,
        "train_positive_count": len(positives), "train_pool_shape": list(pool.shape),
        "matched_negative_count": int(np.sum(y == 0)), "matching_quality": quality,
        "negative_matching": "up to three per train positive; degree-bin pair prioritized; exact support count or graph-CN preferred",
        "target_mask": {
            "method": "pair-specific local subtraction",
            "oracle": "full raw_star rebuild after deleting target edge",
            "equivalence_pairs": changed, "all_equivalence_passed": True,
            "endpoint_symmetry_passed": True,
        },
        "cv": cv, "token_distribution": token,
        "informative_shuffle_fraction": informative,
        "shuffle_power": "ADEQUATE" if power else "LOW_SHUFFLE_POWER",
        "gates": gates, "interpretation": interpretation, "decision": decision,
        "feature_cache": str(feature_path), "source_hashes": source_hashes,
        "validation_positive_identity_used": False, "test_positive_identity_used": False,
        "gpu_training_started": False, "test_evaluated": False,
        "runtime_seconds": float(time.perf_counter() - started),
        "cpu_count": os.cpu_count(), "gpu_compute_used": False,
    }
    write_json(OUT / "diagnostics" / "zero_gpu_results.json", result)
    result_path = OUT / "results.json"
    aggregate = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}
    aggregate.update({
        "state": "STAGE0_COMPLETE", "phase": "zero_gpu_complete",
        "candidate": "HMC", "test_evaluated": False, "gpu_training_started": False,
        "stage0": result, "final_decision": None if decision == "ZERO_GPU_GO" else decision,
    })
    write_json(result_path, aggregate)

    report = [
        "# Stage 0 — Zero-GPU Signal Audit", "",
        f"Decision: {decision}",
        f"Matched legal negatives: {int(np.sum(y == 0))}; positives with matches: {quality['positives_with_matches']}.",
        f"Informative shuffle fraction: {informative:.6f} ({result['shuffle_power']}).",
        f"Median E: positives {pos_e:.6f}; matched negatives {neg_e:.6f}.", "",
        "| Feature set | ROC-AUC mean ± sample SD | PR-AUC mean ± sample SD |",
        "|---|---:|---:|",
    ]
    for key, label in [
        ("Z0_CN_or_support_count", "Z0 support count"),
        ("Z1_multiplicity_scalar_MS", "Z1 MS scalar"),
        ("Z2_HRA_like", "Z2 HRA-like"),
        ("Z3_real_joint_multiplicity", "Z3 real joint"),
        ("Z4_cross_side_shuffled", "Z4 shuffled"),
    ]:
        row = cv[key]
        report.append(f"| {label} | {row['roc_auc_mean']:.6f} ± {row['roc_auc_sample_std']:.6f} | {row['pr_auc_mean']:.6f} ± {row['pr_auc_sample_std']:.6f} |")
    report += ["", "## Gate checks", ""]
    report += [f"- {name}: {'PASS' if passed else 'FAIL'}" for name, passed in gates.items()]
    report += [
        "", f"Interpretation: {interpretation}",
        "", "Local subtraction matched full target-masked raw_star rebuild on 100 sampled training positives. Endpoint symmetry passed. Validation/test identities were not used; test is sealed. No GPU training ran in Stage 0.",
    ]
    (OUT / "02_ZERO_GPU_SIGNAL_AUDIT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    final = (
        "# V15 Final Report\n\n"
        "STATUS: STAGE0_COMPLETE\n"
        "DIRECTION: HMC\n"
        "OLD_DIRECTION: V14 stopped; V13 preserved.\n"
        f"ZERO_GPU_SIGNAL: {decision}\n"
        "CORA_STAGE1: NOT_RUN\nCORA_STAGE2: NOT_RUN\nCORA_3SEED: NOT_RUN\n"
        "CORA_TEST: SEALED\nPUBMED_QUICK: NOT_RUN\n"
        "MECHANISM_CONTROLS: Stage-0 scalar and shuffle controls complete.\n"
        "NOVELTY: pending focused primary-source check.\n"
        f"DECISION: {decision}\n"
        "NEXT_EXPECTED_STEP: GPU Stage 1 only if the corrected gate passes.\n"
    )
    (OUT / "FINAL_REPORT.md").write_text(final, encoding="utf-8")
    write_json(OUT / "status.json", {
        "state": "COMPLETE" if decision != "ZERO_GPU_GO" else "RUNNING",
        "phase": "stage0_complete" if decision != "ZERO_GPU_GO" else "await_gpu_stage1",
        "decision": decision, "gpu_training_started": False, "test_evaluated": False,
        "runtime_seconds": result["runtime_seconds"],
    })
    return result


if __name__ == "__main__":
    try:
        r = run()
        print(json.dumps({
            "decision": r["decision"], "runtime_seconds": r["runtime_seconds"],
            "shuffle_power": r["shuffle_power"],
            "auc": {k: v["roc_auc_mean"] for k, v in r["cv"].items()},
        }, indent=2))
    except Exception:
        failure = {
            "state": "FAILED", "phase": "stage0", "gpu_training_started": False,
            "test_evaluated": False, "traceback": traceback.format_exc(),
        }
        write_json(OUT / "status.json", failure)
        write_json(OUT / "diagnostics" / "zero_gpu_failure.json", failure)
        raise
