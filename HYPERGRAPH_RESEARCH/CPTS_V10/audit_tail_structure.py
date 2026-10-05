"""Train-only CPTS BIC tail-structure audit. No training/test data access."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HR = ROOT / "HYPERGRAPH_RESEARCH"
OUT = HR / "CPTS_V10"
M = 20
EPS = np.finfo(np.float64).tiny


def arr_hash(x: np.ndarray) -> str:
    x = np.ascontiguousarray(x)
    h = hashlib.sha256()
    h.update(str(x.dtype).encode("ascii"))
    h.update(json.dumps(x.shape).encode("ascii"))
    h.update(x.tobytes())
    return h.hexdigest()


def sse(a: np.ndarray, b: np.ndarray) -> float:
    n = len(a)
    if n == 0:
        return 0.0
    return float(np.square(a - a.mean()).sum())


def local_cpts(scores: np.ndarray):
    # Each row is ascending hardness; ties retain original candidate order.
    order = np.argsort(scores, axis=1, kind="stable")
    x = np.take_along_axis(scores.astype(np.float64), order, axis=1)
    n, m = x.shape
    sum1 = x.sum(axis=1)
    ss1 = np.square(x).sum(axis=1) - sum1 * sum1 / m
    bic1 = m * np.log(np.maximum(ss1 / m, EPS)) + 2 * np.log(m)
    # One shared residual variance; H1 parameters are two means, variance, and
    # the discrete breakpoint location (4 parameters in total).
    prefix = np.concatenate([np.zeros((n, 1)), np.cumsum(x, axis=1)], axis=1)
    prefix2 = np.concatenate([np.zeros((n, 1)), np.cumsum(x * x, axis=1)], axis=1)
    bs = np.arange(2, m - 1)  # b = 2,...,M-2; lower segment has b items.
    lo_sse = prefix2[:, bs] - prefix[:, bs] ** 2 / bs[None, :]
    hi_n = m - bs
    hi_sse = (prefix2[:, m:m+1] - prefix2[:, bs]) - (
        (prefix[:, m:m+1] - prefix[:, bs]) ** 2 / hi_n[None, :]
    )
    total_sse = np.maximum(lo_sse + hi_sse, 0.0)
    bic2 = m * np.log(np.maximum(total_sse / m, EPS)) + 4 * np.log(m)
    best_col = np.argmin(bic2, axis=1)
    best_b = bs[best_col]
    best_bic2 = bic2[np.arange(n), best_col]
    present = best_bic2 < bic1
    tail = np.where(present, m - best_b, 0).astype(np.int64)
    selected_asc = np.where(present, best_b - 1, m - 1).astype(np.int64)
    selected_idx = order[np.arange(n), selected_asc]
    return order, x, tail, best_b, bic1, best_bic2, selected_idx


def canonical(pairs: np.ndarray) -> np.ndarray:
    p = np.asarray(pairs, dtype=np.int64).copy()
    p.sort(axis=-1)
    return p


def selected_from_run(path: Path) -> np.ndarray:
    with np.load(path, allow_pickle=False) as z:
        a = z["negatives"]
    return a[0].copy() if a.ndim == 3 else a.copy()


def candidate_indices(pool: np.ndarray, selected: np.ndarray) -> np.ndarray:
    match = np.all(canonical(pool) == canonical(selected)[:, None, :], axis=2)
    if not np.all(match.sum(axis=1) == 1):
        raise RuntimeError("Cached selector edges did not map uniquely into the frozen pool")
    return np.argmax(match, axis=1)


def rank_summary(scores: np.ndarray, indices: np.ndarray) -> dict:
    order = np.argsort(scores, axis=1, kind="stable")
    ranks = np.empty(len(scores), dtype=np.int64)
    chosen_scores = scores[np.arange(len(scores)), indices]
    for row in range(len(scores)):
        ranks[row] = int(np.flatnonzero(order[row] == indices[row])[0])
    asc_pos = ranks.copy()
    ranks = M - ranks  # 1 is hardest, M is easiest.
    has_easier = asc_pos > 0
    next_idx = order[np.arange(len(scores)), np.maximum(asc_pos - 1, 0)]
    next_easier = scores[np.arange(len(scores)), next_idx]
    gap_next = np.where(has_easier, chosen_scores - next_easier, np.nan)
    return {
        "selected_rank_from_hardest_mean": float(ranks.mean()),
        "selected_rank_from_hardest_median": float(np.median(ranks)),
        "selected_rank_from_hardest_counts_1_to_20": np.bincount(ranks, minlength=M+1)[1:].tolist(),
        "selected_teacher_score_mean": float(chosen_scores.mean()),
        "score_percentile_mean_0_to_100": float(np.mean(100 * (M - ranks) / (M - 1))),
        "gap_to_hardest_score_mean": float(np.mean(scores.max(axis=1) - chosen_scores)),
        "gap_to_next_easier_mean": float(np.nanmean(gap_next)) if np.any(np.isfinite(gap_next)) else None,
    }


def summarize(name: str, candidates: np.ndarray, scores: np.ndarray, pool_hash: str, scores_hash: str):
    assert candidates.shape == (len(scores), M, 2), (name, candidates.shape, scores.shape)
    assert scores.shape[1] == M
    assert arr_hash(scores) == scores_hash, f"{name}: score hash mismatch"
    order, x, tail, boundary, bic1, bic2, cpts_idx = local_cpts(scores)
    n = len(scores)
    counts = np.bincount(tail, minlength=M + 1)
    freq = counts / n
    modal = int(np.argmax(counts))
    fixed_collapse = float(freq[modal]) > 0.80
    adaptive = (not fixed_collapse) and int(np.sum(freq > 0.10)) >= 3
    cpts = candidates[np.arange(n), cpts_idx]
    hard_idx = np.argmax(scores, axis=1)
    hard = candidates[np.arange(n), hard_idx]
    # Training-only pooled change point on Cora is also used by Global-CPTS.
    global_result = None
    if name == "cora":
        flat = np.sort(scores.astype(np.float64).reshape(-1), kind="stable")
        nn = len(flat)
        s1 = float(np.square(flat - flat.mean()).sum())
        bicg1 = nn * np.log(max(s1 / nn, EPS)) + 2 * np.log(nn)
        cs = np.concatenate([[0.0], np.cumsum(flat)])
        cs2 = np.concatenate([[0.0], np.cumsum(flat * flat)])
        bscan = np.arange(2, nn - 1, dtype=np.int64)
        s2 = (cs2[-1] - cs2[bscan]) + cs2[bscan] - cs[bscan] ** 2 / bscan - (cs[-1] - cs[bscan]) ** 2 / (nn - bscan)
        bg = bscan[int(np.argmin(s2))]
        bicg2 = nn * np.log(max(max(float(s2.min()), 0.0) / nn, EPS)) + 4 * np.log(nn)
        cp_score = float((flat[bg - 1] + flat[bg]) / 2)
        global_removed = scores > cp_score
        global_count = global_removed.sum(axis=1)
        global_idx = np.argmax(np.where(~global_removed, scores, -np.inf), axis=1)
        fallback = global_count == M
        global_idx[fallback] = np.argmin(scores[fallback], axis=1)
        qbar = float(tail.mean() / M)
        fixed_removed_n = int(np.floor(tail.mean() + 0.5))
        fixed_idx = order[:, M - 1 - fixed_removed_n]
        global_result = {
            "pooled_bic1": float(bicg1), "pooled_bic2": float(bicg2),
            "pooled_change_point_lower_count": int(bg), "global_score_boundary": cp_score,
            "global_removed_count_mean": float(global_count.mean()),
            "global_selected_candidate_rank_from_hardest_distribution": np.bincount(M - np.argsort(np.argsort(scores, axis=1, kind="stable"), axis=1, kind="stable")[np.arange(n), global_idx], minlength=M+1).tolist(),
            "matched_q_mean_tail_fraction_qbar": qbar,
            "matched_q_fixed_removed_count": fixed_removed_n,
            "matched_q_selected_rank_from_hardest": fixed_removed_n + 1,
            "global_selected_indices": global_idx,
            "matched_q_selected_indices": fixed_idx,
        }
    ranks_hardest = M - cpts_idx
    selected_scores = scores[np.arange(n), cpts_idx]
    raw_hard = scores.max(axis=1)
    report = {
        "dataset": name,
        "candidate_pool_hash": pool_hash,
        "teacher_score_hash": scores_hash,
        "positive_count": n,
        "candidate_count_per_positive": M,
        "cpts_selection_index_hash": arr_hash(cpts_idx),
        "local_tail_present_rate": float(np.mean(tail > 0)),
        "tail_size_counts_0_to_20": counts.tolist(),
        "tail_size_fraction_0_to_20": freq.tolist(),
        "tail_size_mean": float(tail.mean()),
        "tail_size_median": float(np.median(tail)),
        "tail_size_p90": float(np.quantile(tail, .9)),
        "tail_size_buckets_over_10pct": int(np.sum(freq > .10)),
        "modal_tail_size": modal,
        "modal_tail_size_fraction": float(freq[modal]),
        "adaptive_structure_confirmed": bool(adaptive),
        "fixed_quantile_collapse": bool(fixed_collapse),
        "boundary_rank_b_counts_2_to_18": np.bincount(np.where(tail > 0, boundary, 0), minlength=M).tolist(),
        "selected_rank_from_hardest_counts_1_to_20": np.bincount(ranks_hardest, minlength=M+1)[1:].tolist(),
        "selected_teacher_score_mean": float(selected_scores.mean()),
        "selected_teacher_score_sample_std": float(np.std(selected_scores, ddof=1)),
        "graph_hard_score_mean": float(raw_hard.mean()),
        "score_gap_to_hardest_mean": float(np.mean(raw_hard - selected_scores)),
        "cpts_selected_indices": cpts_idx,
        "cpts_selected_edges": cpts,
        "graph_hard_indices": hard_idx,
        "graph_hard_edges": hard,
        "tail_counts": tail,
        "boundary_b": boundary,
        "sorted_scores": x,
        "sorted_indices": order,
        "global_control": global_result,
        "bic1": bic1,
        "bic2": bic2,
    }
    return report


def public(r):
    return {k: v for k, v in r.items() if not isinstance(v, np.ndarray)}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with np.load(HR / "NEGATIVE_V6_1/strict_train_candidates_and_selections.npz", allow_pickle=False) as z:
        c, s = z["negative_candidates"].copy(), z["score_graph"].copy()
    cm = json.loads((HR / "NEGATIVE_V6_1/strict_pool_metadata.json").read_text())
    datasets = {"cora": (c, s, cm["candidate_pool_hash"], cm["score_cache"]["Graph"]["score_hash"])}
    for name in ("pubmed", "citeseer"):
        td = HR / f"QTHS_V7_1/TEACHERS/{name}"
        with np.load(td / "graph_teacher_scores.npz", allow_pickle=False) as z:
            cc, ss = z["candidates"].copy(), z["scores"].copy()
        meta = json.loads((td / "graph_teacher.json").read_text())
        datasets[name] = (cc, ss, meta["train_pool_hash"], meta["scores_hash"])

    reports = {name: summarize(name, *items) for name, items in datasets.items()}
    # Actual selection overlap on Cora uses cached V8/7.1 selected training edges.
    cr = reports["cora"]
    pool = datasets["cora"][0]
    overlap = {}
    base_v7 = HR / "QTHS_V7_1/RUNS/CORA"
    base_v8 = HR / "QTHS_V8_PAPER/RUNS/CORA/GCN"
    for seed in (0, 1, 2):
        q = selected_from_run(base_v7 / f"C3_QTHS25/seed{seed}/negative_samples_by_epoch.npz")
        sh = selected_from_run(base_v8 / f"SH75/seed{seed}/negative_samples_by_epoch.npz")
        cp, qq, ss = canonical(cr["cpts_selected_edges"]), canonical(q), canonical(sh)
        overlap[str(seed)] = {
            "cpts_equals_graph_hard_fraction": float(np.mean(np.all(cp == canonical(cr["graph_hard_edges"]), axis=1))),
            "cpts_equals_qths25_fraction": float(np.mean(np.all(cp == qq, axis=1))),
            "cpts_equals_sh75_fraction": float(np.mean(np.all(cp == ss, axis=1))),
        }
    cpts_stats = rank_summary(datasets["cora"][1], cr["cpts_selected_indices"])
    graph_stats = rank_summary(datasets["cora"][1], cr["graph_hard_indices"])
    selection_stats = {"CPTS": cpts_stats, "GRAPH_HARD": graph_stats}
    q_indices, sh_indices = [], []
    for seed in (0, 1, 2):
        q = selected_from_run(base_v7 / f"C3_QTHS25/seed{seed}/negative_samples_by_epoch.npz")
        sh = selected_from_run(base_v8 / f"SH75/seed{seed}/negative_samples_by_epoch.npz")
        q_indices.append(candidate_indices(pool, q))
        sh_indices.append(candidate_indices(pool, sh))
    selection_stats["QTHS25_by_seed"] = {str(i): rank_summary(datasets["cora"][1], ids) for i,ids in enumerate(q_indices)}
    selection_stats["SH75_by_seed"] = {str(i): rank_summary(datasets["cora"][1], ids) for i,ids in enumerate(sh_indices)}
    sizes = cr["tail_counts"]
    # Deterministic illustrative rows: median positive tail size, smallest
    # positive tail, largest tail, and a no-tail row (first row within class).
    rep = {}
    classes = {
        "median_tail": int(np.median(sizes)),
        "small_positive_tail": int(np.min(sizes[sizes > 0])) if np.any(sizes > 0) else None,
        "large_tail": int(np.max(sizes)),
        "no_tail": 0,
    }
    for label, t in classes.items():
        if t is None or not np.any(sizes == t):
            rep[label] = None
            continue
        ids = np.flatnonzero(sizes == t)
        row = int(ids[len(ids)//2])
        rep[label] = {
            "row": row, "tail_size": int(t),
            "sorted_scores_ascending": reports["cora"]["sorted_scores"][row].tolist(),
            "sorted_candidate_indices": reports["cora"]["sorted_indices"][row].tolist(),
            "boundary_b": int(reports["cora"]["boundary_b"][row]),
            "cpts_selected_candidate_index": int(reports["cora"]["cpts_selected_indices"][row]),
        }
    out = {
        "protocol": "STRICT_TRAIN_ONLY",
        "method": "CPTS",
        "m": M,
        "bic_definition": {
            "bic1": "M*ln(SSE1/M) + 2*ln(M); Gaussian mean and shared variance",
            "bic2": "M*ln(SSE2/M) + 4*ln(M); two segment means, shared variance, and discrete breakpoint",
            "split_range": "b=2,...,M-2 inclusive; two contiguous segments; minimize SSE2(b)",
            "tail_rule": "if min BIC2 < BIC1, remove upper tail h_(b+1)...h_(M) and select h_(b); else select h_(M)",
            "zero_variance_handling": "variance likelihood uses float64 tiny floor",
        },
        "datasets": {n: public(r) for n, r in reports.items()},
        "cora_selection_overlap_cached": overlap,
        "cora_selection_rank_statistics": selection_stats,
        "cora_representative_rows_deterministic": rep,
        "training_started": False,
        "test_accessed": False,
    }
    # Drop bulky row-wise arrays from JSON; retain exact audit summaries.
    for d in out["datasets"].values():
        d.pop("global_control", None)  # emitted below without row-level indices
    g = reports["cora"]["global_control"]
    random_match = {}
    for seed in (0, 1, 2):
        rng = np.random.default_rng(20261002 + seed)
        chosen = np.empty(len(sizes), dtype=np.int64)
        row_ids = np.arange(len(sizes))
        c_order = reports["cora"]["sorted_indices"]
        for row, removed_n in enumerate(sizes):
            removed = rng.choice(M, size=int(removed_n), replace=False) if removed_n else np.empty(0, dtype=np.int64)
            keep = np.ones(M, dtype=bool)
            keep[removed] = False
            chosen[row] = int(np.argmax(np.where(keep, datasets["cora"][1][row], -np.inf)))
        random_match[str(seed)] = chosen
    selection_stats["GLOBAL_CPTS"] = rank_summary(datasets["cora"][1], g["global_selected_indices"])
    selection_stats["MATCHED_Q"] = rank_summary(datasets["cora"][1], g["matched_q_selected_indices"])
    selection_stats["RANDOM_MATCHED_by_seed"] = {
        seed: rank_summary(datasets["cora"][1], ids) for seed, ids in random_match.items()
    }
    np.savez_compressed(
        OUT / "cora_selector_indices.npz",
        cpts=cr["cpts_selected_indices"],
        global_cpts=g["global_selected_indices"],
        matched_q=g["matched_q_selected_indices"],
        random_matched_s0=random_match["0"],
        random_matched_s1=random_match["1"],
        random_matched_s2=random_match["2"],
    )
    out["global_cpts_control"] = {k: v for k, v in g.items() if not isinstance(v, np.ndarray)}
    out["matched_q_control"] = {
        "qbar": g["matched_q_mean_tail_fraction_qbar"],
        "fixed_removed_count": g["matched_q_fixed_removed_count"],
        "selected_rank_from_hardest": g["matched_q_selected_rank_from_hardest"],
    }
    (OUT / "tail_audit.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "results.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({n: {k: r[k] for k in ("local_tail_present_rate", "tail_size_counts_0_to_20", "tail_size_mean", "tail_size_median", "tail_size_p90", "modal_tail_size_fraction", "adaptive_structure_confirmed", "fixed_quantile_collapse")} for n,r in reports.items()}, indent=2))
    print("CORA_SELECTION_OVERLAP", json.dumps(overlap, indent=2))
    print("GLOBAL_CPTS", json.dumps(out["global_cpts_control"], indent=2))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figdir = OUT / "figures"
    figdir.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    bins = np.arange(-0.5, M + 1.5, 1)
    ax.hist(sizes, bins=bins, weights=np.ones_like(sizes, dtype=float)/len(sizes), color="#336699", edgecolor="white")
    ax.set(xlabel="Detected tail size per positive (0 = no tail)", ylabel="Fraction of positives", title="Cora training-only CPTS tail-size distribution")
    fig.tight_layout(); fig.savefig(figdir / "tail_size_distribution.png", dpi=180); plt.close(fig)
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), sharex=True)
    cscore, cedge = datasets["cora"][1], datasets["cora"][0]
    for ax, (label, item) in zip(axes.ravel(), rep.items()):
        if item is None:
            ax.set_visible(False); continue
        row = item["row"]
        y = reports["cora"]["sorted_scores"][row]
        ax.plot(np.arange(1, M+1), y, marker="o", ms=3, lw=1, color="#336699")
        b = item["boundary_b"]
        if item["tail_size"] > 0:
            ax.axvline(b + .5, color="#cc3311", ls="--", label="CPTS boundary")
        else:
            ax.axvline(M + .5, color="#cc3311", ls="--", label="no detected tail")
        ax.axvline(M, color="#228833", ls=":", label="Graph-hard")
        ax.set_title(f"{label}: row {row}, tail={item['tail_size']}")
        ax.set_ylabel("Graph-teacher score")
    axes[-1,0].set_xlabel("Candidate hardness rank (ascending)")
    axes[-1,1].set_xlabel("Candidate hardness rank (ascending)")
    handles, labels = axes[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2)
    fig.tight_layout(rect=(0,0,1,.94)); fig.savefig(figdir / "representative_score_profiles.png", dpi=180); plt.close(fig)

    # Compact markdown summary for the user and gate decision.
    lines = ["# Tail structure audit", "", "All calculations use frozen, train-only graph-teacher scores. No validation/test arrays enter CPTS selection or BIC fitting.", "", "## BIC rule", "", out["bic_definition"]["bic1"], "", out["bic_definition"]["bic2"], "", out["bic_definition"]["tail_rule"], "", "## Dataset summaries", "", "| Dataset | Positives | Tail present | Mean tail | Median | p90 | Modal tail share | 3 sizes >10% | >80% same size | Adaptive gate |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for n,r in reports.items():
        lines.append(f"| {n} | {len(r['tail_counts'])} | {r['local_tail_present_rate']:.4f} | {r['tail_size_mean']:.4f} | {r['tail_size_median']:.1f} | {r['tail_size_p90']:.1f} | {r['modal_tail_size_fraction']:.4f} | {r['tail_size_buckets_over_10pct']} | {r['fixed_quantile_collapse']} | {r['adaptive_structure_confirmed']} |")
    lines += ["", "## Cora tail-size counts", "", "| Tail size | Count | Fraction |", "|---:|---:|---:|"]
    for t,(count,frac) in enumerate(zip(reports["cora"]["tail_size_counts_0_to_20"],reports["cora"]["tail_size_fraction_0_to_20"])):
        lines.append(f"| {t} | {count} | {frac:.6f} |")
    lines += ["", "## Cora cached selection overlap", "", "| Seed | CPTS = Graph-hard | CPTS = QTHS25 | CPTS = SH75 |", "|---:|---:|---:|---:|"]
    for seed,v in overlap.items():
        lines.append(f"| {seed} | {v['cpts_equals_graph_hard_fraction']:.4f} | {v['cpts_equals_qths25_fraction']:.4f} | {v['cpts_equals_sh75_fraction']:.4f} |")
    lines += ["", "## Cora selected hardness", "", "Rank 1 is hardest; rank 20 is easiest. Percentile is 100 at the hardest candidate and 0 at the easiest.", "", "| Selector | Mean rank | Median rank | Mean teacher score | Mean score percentile | Mean gap to hardest |", "|---|---:|---:|---:|---:|---:|"]
    for key in ("CPTS", "GRAPH_HARD"):
        q = selection_stats[key]
        lines.append(f"| {key} | {q['selected_rank_from_hardest_mean']:.3f} | {q['selected_rank_from_hardest_median']:.1f} | {q['selected_teacher_score_mean']:.6f} | {q['score_percentile_mean_0_to_100']:.2f} | {q['gap_to_hardest_score_mean']:.6f} |")
    for key in ("QTHS25_by_seed", "SH75_by_seed"):
        vals = [selection_stats[key][str(i)] for i in range(3)]
        lines.append(f"| {key.replace('_by_seed','')} | {np.mean([v['selected_rank_from_hardest_mean'] for v in vals]):.3f} | {np.median([v['selected_rank_from_hardest_median'] for v in vals]):.1f} | {np.mean([v['selected_teacher_score_mean'] for v in vals]):.6f} | {np.mean([v['score_percentile_mean_0_to_100'] for v in vals]):.2f} | {np.mean([v['gap_to_hardest_score_mean'] for v in vals]):.6f} |")
    lines += ["", "## Gate", "", f"Cora fixed-quantile collapse: **{reports['cora']['fixed_quantile_collapse']}**. Adaptive structure confirmed: **{reports['cora']['adaptive_structure_confirmed']}**.", "Training remains disabled until this gate is evaluated. See `figures/tail_size_distribution.png` and `figures/representative_score_profiles.png`.", ""]
    (OUT / "02_TAIL_STRUCTURE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
