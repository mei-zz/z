"""Aggregate completed HL-GNN-PDG V0 runs and emit the screening report."""

import json
import math
from pathlib import Path
from statistics import mean, stdev


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results" / "hlgnn_pdg_v0"


def load_results():
    records = []
    for path in sorted(RESULTS.glob("cora/*/seed*.json")) + sorted(RESULTS.glob("citeseer/*/seed*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            record["_path"] = str(path)
            records.append(record)
        except Exception as exc:
            print(f"WARN unreadable {path}: {exc}")
    return records


def pct(record, key):
    return 100.0 * record["best_metrics"][key]


def fmt(values):
    if not values:
        return "NA"
    return f"{mean(values):.2f} ± {stdev(values) if len(values) > 1 else 0.0:.2f}"


def diagnostics_summary(records):
    depths = []
    gate_delta = []
    gate_std = []
    subgroup_ranges = []
    for record in records:
        diag = record.get("diagnostics") or {}
        if "expected_depth" in diag:
            depths.append(diag["expected_depth"])
            gate_delta.append(diag.get("mean_abs_w_minus_t", 0.0))
            gate_std.append(diag.get("pairwise_std_w_mean", 0.0))
            values = [
                item["depth_mean"]
                for item in (diag.get("subgroups") or {}).values()
                if item.get("depth_mean") is not None
            ]
            if values:
                subgroup_ranges.append(max(values) - min(values))
    return {
        "depth_mean": mean([x["mean"] for x in depths]) if depths else None,
        "depth_std": mean([x["std"] for x in depths]) if depths else None,
        "gate_delta_mean": mean(gate_delta) if gate_delta else None,
        "gate_pairwise_std_mean": mean(gate_std) if gate_std else None,
        "subgroup_depth_range_mean": mean(subgroup_ranges) if subgroup_ranges else None,
    }


def main():
    records = load_results()
    expected = {(d, v, s) for d in ("cora", "citeseer") for v in ("B0", "B1", "B2", "B3") for s in (0, 1, 2)}
    present = {(r["dataset"], r["variant"], r["seed"]) for r in records}
    missing = sorted(expected - present)
    if missing:
        raise SystemExit(f"incomplete matrix; missing {missing}")
    by_key = {(r["dataset"], r["variant"], r["seed"]): r for r in records}

    table_lines = [
        "| Dataset | Seed | Parent | Profile | PDG | Shuffled | ΔPDG |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for dataset in ("cora", "citeseer"):
        for seed in (0, 1, 2):
            parent = pct(by_key[(dataset, "B0", seed)], "Hits@100_test")
            profile = pct(by_key[(dataset, "B1", seed)], "Hits@100_test")
            pdg = pct(by_key[(dataset, "B2", seed)], "Hits@100_test")
            shuffled = pct(by_key[(dataset, "B3", seed)], "Hits@100_test")
            table_lines.append(f"| {dataset} | {seed} | {parent:.2f} | {profile:.2f} | {pdg:.2f} | {shuffled:.2f} | {pdg-parent:+.2f} |")

    summary_lines = []
    for dataset in ("cora", "citeseer"):
        summary_lines.append(f"### {dataset}")
        for variant, label in (("B0", "Parent"), ("B1", "Profile Direct"), ("B2", "PDG"), ("B3", "Shuffled PDG")):
            vals100 = [pct(by_key[(dataset, variant, seed)], "Hits@100_test") for seed in (0, 1, 2)]
            vals10 = [pct(by_key[(dataset, variant, seed)], "Hits@10_test") for seed in (0, 1, 2)]
            vals50 = [pct(by_key[(dataset, variant, seed)], "Hits@50_test") for seed in (0, 1, 2)]
            summary_lines.append(f"- {label}: Hits@10 {fmt(vals10)}; Hits@50 {fmt(vals50)}; Hits@100 {fmt(vals100)}")

    deltas = []
    dataset_mean_delta = {}
    shuffled_deltas = {}
    profile_deltas = {}
    for dataset in ("cora", "citeseer"):
        d = []
        s = []
        p = []
        for seed in (0, 1, 2):
            pdg = pct(by_key[(dataset, "B2", seed)], "Hits@100_test")
            parent = pct(by_key[(dataset, "B0", seed)], "Hits@100_test")
            shuffled = pct(by_key[(dataset, "B3", seed)], "Hits@100_test")
            profile = pct(by_key[(dataset, "B1", seed)], "Hits@100_test")
            d.append(pdg - parent); s.append(pdg - shuffled); p.append(pdg - profile)
            deltas.append(pdg > parent)
        dataset_mean_delta[dataset] = mean(d)
        shuffled_deltas[dataset] = mean(s)
        profile_deltas[dataset] = mean(p)

    pdg_records = [by_key[(d, "B2", s)] for d in ("cora", "citeseer") for s in (0, 1, 2)]
    b0_records = [by_key[(d, "B0", s)] for d in ("cora", "citeseer") for s in (0, 1, 2)]
    runtime_overhead = []
    memory_overhead = []
    for d in ("cora", "citeseer"):
        for s in (0, 1, 2):
            parent = by_key[(d, "B0", s)]
            pdg = by_key[(d, "B2", s)]
            if parent["mean_epoch_runtime_sec"] > 0:
                runtime_overhead.append(pdg["mean_epoch_runtime_sec"] / parent["mean_epoch_runtime_sec"] - 1.0)
            pm = parent.get("peak_gpu_memory_allocated_mb", 0.0)
            dm = pdg.get("peak_gpu_memory_allocated_mb", 0.0)
            if pm > 0:
                memory_overhead.append(dm / pm - 1.0)
    diag = diagnostics_summary(pdg_records)
    five_of_six = sum(deltas) >= 5
    positive_means = all(value > 0 for value in dataset_mean_delta.values())
    shuffled_beaten = all(value > 0 for value in shuffled_deltas.values())
    profile_not_explain = any(value > 0 for value in profile_deltas.values())
    gate_active = (diag["gate_delta_mean"] or 0.0) > 1e-3 and (diag["gate_pairwise_std_mean"] or 0.0) > 1e-3
    range_active = (diag["subgroup_depth_range_mean"] or 0.0) > 0.05
    overhead_ok = (mean(runtime_overhead) if runtime_overhead else math.inf) < 0.25 and (mean(memory_overhead) if memory_overhead else math.inf) < 0.25
    stop_trigger = (not positive_means) or (not shuffled_beaten) or (not profile_not_explain) or (not gate_active)
    if five_of_six and positive_means and shuffled_beaten and profile_not_explain and gate_active and range_active and overhead_ok:
        verdict = "STRONG GO"
    elif (not stop_trigger) and sum(deltas) >= 4 and shuffled_beaten and profile_not_explain and gate_active and overhead_ok:
        verdict = "GO"
    elif stop_trigger or not records:
        verdict = "STOP"
    else:
        verdict = "WEAK"

    report = [
        "# HL-GNN-PDG V0 screening report",
        "",
        f"Final verdict: **{verdict}**",
        "",
        "## 1. Source audit",
        "",
        "See `HLGNN_PDG_SOURCE_AUDIT.md`. The official parent uses a global `(K+1,)` `self.temp`, streams hop states into one global hidden representation, and feeds the endpoint product to the original LinkPredictor.",
        "",
        "## 2. Parent mathematical reconstruction",
        "",
        "`X^(0)=Linear(X)`; `X^(k+1)=normalized_train_adjacency @ X^(k)`; `H=sum_k t_k X^(k)`. PDG keeps the same propagation and uses `w_k(u,v)=t_k+c*tanh(a)*tanh(G(profile_uv))`.",
        "",
        "## 3. Seed and negative-sampling audit",
        "",
        "The official split is generated with seed 234 before resetting the requested seed. Each variant×seed is a separate process. Training batch permutations use an independent deterministic generator, and random negative edges use a dedicated CPU generator shared by all four variants for the same dataset×seed.",
        "",
        "## 4. Parent reproduction and initial equivalence",
        "",
        "B0 is the unmodified parent model and original LinkPredictor. B1 appends the four profiles to the endpoint product. B2 is PDG; B3 has the same gate and parameterization with within-pool profile shuffling.",
        "",
        "| Dataset | Seed | B2 max abs init logit diff |",
        "| --- | ---: | ---: |",
    ]
    for d in ("cora", "citeseer"):
        for s in (0, 1, 2):
            diff = by_key[(d, "B2", s)].get("initial_equivalence_max_abs_logit_diff")
            report.append(f"| {d} | {s} | {diff:.3e} |" if diff is not None else f"| {d} | {s} | NA |")
    report += ["", "## 5. Seed-level metrics", "", *table_lines, "", "## 6. Mean ± std", "", *summary_lines, "", "## 7. Expected-depth and gate diagnostics", "", f"- Mean expected depth across PDG runs: {diag['depth_mean']:.4f}", f"- Mean expected-depth within-run std: {diag['depth_std']:.4f}", f"- Mean `mean|w-t|`: {diag['gate_delta_mean']:.6f}", f"- Mean pairwise hop-weight std: {diag['gate_pairwise_std_mean']:.6f}", f"- Mean subgroup depth range: {diag['subgroup_depth_range_mean']:.4f}", "", "The per-run JSON files contain depth quantiles, CN=0/1/>=2 groups, train-only degree thresholds, train-only feature-similarity thresholds, and subgroup depth statistics.", "", "## 8. Parameters, runtime, and GPU memory", "", "| Dataset | Variant | Params (mean) | Epoch sec (mean) | Peak allocated MB (mean) |", "| --- | --- | ---: | ---: | ---: |"]
    for d in ("cora", "citeseer"):
        for v in ("B0", "B1", "B2", "B3"):
            rs = [by_key[(d, v, s)] for s in (0, 1, 2)]
            report.append(f"| {d} | {v} | {mean([r['trainable_parameters'] for r in rs]):.0f} | {mean([r['mean_epoch_runtime_sec'] for r in rs]):.3f} | {mean([r.get('peak_gpu_memory_allocated_mb', 0.0) for r in rs]):.1f} |")
    report += ["", f"Mean PDG-vs-Parent epoch-runtime overhead: {mean(runtime_overhead):.2%}", f"Mean PDG-vs-Parent peak-allocated-memory overhead: {mean(memory_overhead):.2%}", "", "## 9. Interpretation", "", f"PDG > Parent on {sum(deltas)}/6 paired seeds. Dataset mean ΔPDG (percentage points): " + "; ".join(f"{d} {dataset_mean_delta[d]:+.2f}" for d in dataset_mean_delta) + ". PDG-vs-Shuffled means: " + "; ".join(f"{d} {shuffled_deltas[d]:+.2f}" for d in shuffled_deltas) + ". PDG-vs-Profile means: " + "; ".join(f"{d} {profile_deltas[d]:+.2f}" for d in profile_deltas) + ".", "", "## 10. Final verdict", "", f"**{verdict}**", ""]
    detail_lines = [
        "", "## 11. Gate-collapse diagnostics", "",
        "| Dataset | Seed | mean|w-t| | mean pairwise std(w) | depth mean | depth std |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    subgroup_names = [
        "CN=0", "CN=1", "CN>=2", "degree_low", "degree_medium", "degree_high",
        "similarity_low", "similarity_medium", "similarity_high",
    ]
    subgroup_lines = [
        "| Dataset | Seed | Group | Count | E[D_uv] | SD[D_uv] | mean|w-t| |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for d in ("cora", "citeseer"):
        for s in (0, 1, 2):
            diag_run = by_key[(d, "B2", s)].get("diagnostics") or {}
            depth_run = diag_run.get("expected_depth") or {}
            detail_lines.append(
                f"| {d} | {s} | {diag_run.get('mean_abs_w_minus_t', 0.0):.3e} | "
                f"{diag_run.get('pairwise_std_w_mean', 0.0):.3e} | "
                f"{depth_run.get('mean', 0.0):.4f} | {depth_run.get('std', 0.0):.3e} |"
            )
            for group in subgroup_names:
                item = (diag_run.get("subgroups") or {}).get(group, {})
                depth_mean = item.get("depth_mean")
                depth_std = item.get("depth_std")
                delta_mean = item.get("delta_mean")
                subgroup_lines.append(
                    f"| {d} | {s} | {group} | {item.get('count', 0)} | "
                    f"{'NA' if depth_mean is None else format(depth_mean, '.4f')} | "
                    f"{'NA' if depth_std is None else format(depth_std, '.4f')} | "
                    f"{'NA' if delta_mean is None else format(delta_mean, '.3e')} |"
                )
    report.extend(detail_lines)
    report += ["", "## 12. CN subgroup", "", *[line for line in subgroup_lines if "| CN" in line or line.startswith("| Dataset") or line.startswith("| ---")]]
    report += ["", "## 13. Degree subgroup", "", *[line for line in subgroup_lines if "| degree_" in line or line.startswith("| Dataset") or line.startswith("| ---")]]
    report += ["", "## 14. Feature-similarity subgroup", "", *[line for line in subgroup_lines if "| similarity_" in line or line.startswith("| Dataset") or line.startswith("| ---")]]
    report += ["", "## 15. Interpretation note", "", "The measured gate deltas and subgroup depth ranges above are the mechanism check. A near-zero value indicates that the zero-initialized residual gate stayed at the parent profile during training.", "", "## 16. Final verdict", "", f"**{verdict}**", ""]
    (ROOT / "HLGNN_PDG_V0_SCREENING_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    (RESULTS / "paired_table.md").write_text("\n".join(table_lines) + "\n", encoding="utf-8")
    (RESULTS / "summary.json").write_text(json.dumps({"verdict": verdict, "dataset_mean_delta": dataset_mean_delta, "pdg_vs_shuffled_mean": shuffled_deltas, "pdg_vs_profile_mean": profile_deltas, "pdg_parent_improvement_count": sum(deltas), "runtime_overhead_mean": mean(runtime_overhead), "memory_overhead_mean": mean(memory_overhead), "diagnostics": diag}, indent=2), encoding="utf-8")
    print(f"Wrote {ROOT / 'HLGNN_PDG_V0_SCREENING_REPORT.md'}")
    print(f"VERDICT={verdict}")


if __name__ == "__main__":
    main()
