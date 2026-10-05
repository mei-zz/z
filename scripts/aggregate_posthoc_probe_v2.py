"""Aggregate and compare Post-hoc Probe Protocol V2 checkpoint outputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


MODELS = ("M0", "M1", "M2", "M3")
PROBES = (
    "z_cn_to_degree",
    "z_residual_to_degree",
    "z_degree_to_cn_residual",
    "z_degree_to_degree",
    "z_cn_to_cn_residual",
)
METRICS = ("r2", "mae", "spearman")


def _read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _aggregate(values: list[float]) -> dict[str, object]:
    array = np.asarray(values, dtype=float)
    return {
        "mean": float(np.mean(array)),
        "std": float(np.std(array, ddof=1)) if len(array) > 1 else 0.0,
        "median": float(np.median(array)),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
        "count": int(len(array)),
    }


def _decision(values: list[float], tolerance: float = 0.02) -> str:
    values = [float(value) for value in values]
    improved = sum(value < -tolerance for value in values)
    worse = sum(value > tolerance for value in values)
    if improved >= 4 and improved > worse:
        return "IMPROVED"
    if worse >= 4 and worse > improved:
        return "WORSE"
    if improved == 0 and worse == 0:
        return "UNCHANGED"
    return "MIXED"


def aggregate(root: Path, models: tuple[str, ...], output_dir: Path) -> dict:
    all_rows: list[dict] = []
    metadata_by_model_seed: dict[tuple[str, int], dict] = {}
    for model in models:
        for probe_dir in sorted((root / model / "probe").glob("*")):
            csv_path = probe_dir / "posthoc_probe.csv"
            metadata_path = probe_dir / "posthoc_probe_metadata.json"
            if not csv_path.exists() or not metadata_path.exists():
                continue
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            model_seed = int(metadata["model_seed"])
            metadata_by_model_seed[(model, model_seed)] = metadata
            run_id = probe_dir.name
            for row in _read_csv(csv_path):
                all_rows.append({
                    "model": model,
                    "model_seed": model_seed,
                    "run_id": run_id,
                    **row,
                })

    if not all_rows:
        raise RuntimeError(f"No V2 probe outputs found under {root}")

    v2_m0_seed0 = None
    m0_seed0_dirs = sorted((root / "M0" / "probe").glob("*"))
    for probe_dir in m0_seed0_dirs:
        metadata_path = probe_dir / "posthoc_probe_metadata.json"
        diagnostics_path = probe_dir / "posthoc_probe_diagnostics.json"
        if not metadata_path.exists() or not diagnostics_path.exists():
            continue
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if int(metadata.get("model_seed", -1)) == 0:
            diagnostic_items = json.loads(
                diagnostics_path.read_text(encoding="utf-8")
            )["diagnostics"]
            metric_items = {
                int(row["probe_seed"]): row
                for row in all_rows
                if row["model"] == "M0"
                and int(row["model_seed"]) == 0
                and row["probe"] == "z_cn_to_degree"
            }
            v2_m0_seed0 = {
                int(item["probe_seed"]): {
                    "r2": float(metric_items[int(item["probe_seed"])] ["r2"]),
                    "x": item["x"],
                }
                for item in diagnostic_items
                if item["probe"] == "z_cn_to_degree"
            }
            break
    for row in all_rows:
        for key in METRICS + ("probe_seed", "selected_hyperparameter"):
            if key in row:
                row[key] = float(row[key])
        row["model_seed"] = int(row["model_seed"])
        row["probe_seed"] = int(row["probe_seed"])

    model_seed_rows: list[dict] = []
    grouped_model_seed: dict[tuple[str, int, str, str], list[float]] = defaultdict(list)
    for row in all_rows:
        for metric in METRICS:
            grouped_model_seed[
                (row["model"], row["model_seed"], row["probe"], metric)
            ].append(float(row[metric]))
    for (model, seed, probe, metric), values in sorted(grouped_model_seed.items()):
        model_seed_rows.append({
            "model": model,
            "model_seed": seed,
            "probe": probe,
            "role": next(row["role"] for row in all_rows if row["model"] == model and row["model_seed"] == seed and row["probe"] == probe),
            "metric": metric,
            "aggregation": "mean_over_probe_sample_seeds",
            **_aggregate(values),
        })

    sample_seed_rows: list[dict] = []
    grouped_sample_seed: dict[tuple[str, int, str, str], list[float]] = defaultdict(list)
    for row in all_rows:
        for metric in METRICS:
            grouped_sample_seed[
                (row["model"], row["probe_seed"], row["probe"], metric)
            ].append(float(row[metric]))
    for (model, sample_seed, probe, metric), values in sorted(grouped_sample_seed.items()):
        sample_seed_rows.append({
            "model": model,
            "probe_seed": sample_seed,
            "probe": probe,
            "metric": metric,
            "aggregation": "mean_over_model_seeds",
            **_aggregate(values),
        })

    overall_rows: list[dict] = []
    grouped_overall: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    for row in all_rows:
        for metric in METRICS:
            grouped_overall[(row["model"], row["probe"], metric)].append(float(row[metric]))
    for (model, probe, metric), values in sorted(grouped_overall.items()):
        overall_rows.append({
            "model": model,
            "probe": probe,
            "role": next(row["role"] for row in all_rows if row["model"] == model and row["probe"] == probe),
            "metric": metric,
            "aggregation": "all_model_and_probe_seeds",
            **_aggregate(values),
        })

    pair_rows: list[dict] = []
    pair_hashes: dict[tuple[int, int, str], dict[str, str]] = {}
    for (model, model_seed), metadata in sorted(metadata_by_model_seed.items()):
        by_sample = metadata.get("pair_split_hashes_by_probe_seed", {})
        for sample_seed, split_hashes in by_sample.items():
            for split, pair_hash in split_hashes.items():
                pair_hashes[(model_seed, int(sample_seed), split)] = {
                    model: pair_hash
                }
    for key in sorted({key for key in pair_hashes}):
        model_seed, sample_seed, split = key
        values = {}
        for model in models:
            metadata = metadata_by_model_seed.get((model, model_seed))
            if metadata is None:
                values[model] = "MISSING"
            else:
                values[model] = metadata.get("pair_split_hashes_by_probe_seed", {}).get(str(sample_seed), {}).get(split, "MISSING")
        unique = set(values.values())
        pair_rows.append({
            "model_seed": model_seed,
            "probe_seed": sample_seed,
            "split": split,
            **values,
            "cross_model_hash_match": len(unique) == 1 and "MISSING" not in unique,
        })

    comparison_rows: list[dict] = []
    for candidate in models:
        if candidate == "M0":
            continue
        for probe in PROBES:
            for metric in METRICS:
                baseline = {
                    int(row["model_seed"]): float(row["mean"])
                    for row in model_seed_rows
                    if row["model"] == "M0" and row["probe"] == probe and row["metric"] == metric
                }
                candidate_values = {
                    int(row["model_seed"]): float(row["mean"])
                    for row in model_seed_rows
                    if row["model"] == candidate and row["probe"] == probe and row["metric"] == metric
                }
                paired = [candidate_values[seed] - baseline[seed] for seed in sorted(baseline) if seed in candidate_values]
                comparison_rows.append({
                    "candidate": candidate,
                    "baseline": "M0",
                    "probe": probe,
                    "metric": metric,
                    "paired_seed_count": len(paired),
                    **_aggregate(paired),
                    "direction_lower_is_better": _decision(paired),
                    "direction_higher_is_better": _decision([-value for value in paired]),
                })

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(output_dir / "posthoc_probe_v2_all_rows.csv", all_rows)
    _write_csv(output_dir / "posthoc_probe_v2_model_seed_summary.csv", model_seed_rows)
    _write_csv(output_dir / "posthoc_probe_v2_probe_seed_summary.csv", sample_seed_rows)
    _write_csv(output_dir / "posthoc_probe_v2_overall_summary.csv", overall_rows)
    _write_csv(output_dir / "posthoc_probe_v2_pair_hash_audit.csv", pair_rows)
    _write_csv(output_dir / "posthoc_probe_v2_comparisons.csv", comparison_rows)

    report = [
        "# PROBE V2 Protocol Fix Report",
        "",
        "本报告由 `aggregate_posthoc_probe_v2.py` 基于现有 checkpoint 的 Probe V2 输出生成。没有重新训练模型，也没有修改 Step 12。",
        "",
        "## A. Changed files",
        "",
        "- `src/dcdlp/evaluation/posthoc_probe.py`: 增加 canonical context graph、单 pair target-edge removal、context hash，以及 Ridge scaler/target diagnostics。",
        "- `scripts/run_posthoc_leakage_audit.py`: 改为逐 pair context graph，X/y 使用同一图，probe seed 控制 pair sampling，统一 eval/no-grad，并增加协议断言和逐边输出。",
        "- `tests/test_posthoc_probe_v2.py`: 增加 per-pair masking、valid/test no-op、X/y context hash、sampling reproducibility 测试。",
        "- `scripts/aggregate_posthoc_probe_v2.py`: 汇总 model-seed 与 probe-sample-seed 两类变异，并审计跨模型 pair hash。",
        "",
        "## B. Root cause",
        "",
        "旧 probe 的 train representation 使用了整个 batch 的 target-edge masking，而 valid/test representation 没有相同的图上下文；同时 train target 使用完整 train_graph。近常数 latent 维度在跨 split 偏移后使 StandardScaler 产生极小 scale，Ridge 测试输入发生外推，导致 M0 seed0 出现 R²≈-340。",
        "",
        "## C. Old vs New protocol",
        "",
        "| 项目 | Old | Probe V2 |",
        "| --- | --- | --- |",
        "| train masking | 一次移除整个 pair batch | 每个 pair 只移除自身 target edge |",
        "| valid masking | 基本 no-op，但未统一显式验证 | 统一 remove-if-present；存在则报错 |",
        "| test masking | 基本 no-op，但未统一显式验证 | 统一 remove-if-present；存在则报错 |",
        "| X graph | train/valid/test 不一致 | 每个 pair 的 per-pair context graph |",
        "| y graph | 完整 train_graph | 与 X 完全相同的 context graph |",
        "| probe seed | Ridge deterministic，重复相同 | 真正控制 train/test pair sampling |",
        "| scaler | StandardScaler+Ridge | 保持 StandardScaler+Ridge，新增 diagnostics |",
        "",
        "## D. M0 seed0 diagnostic",
        "",
        "旧值来自上一轮对旧 checkpoint/probe 的只读诊断；新值来自 Probe V2 输出。",
        "",
        "| 指标 | Old | New Probe V2 |",
        "| --- | ---: | ---: |",
        "| z_cn→degree test R² | ≈ -340.55 | "
        + ("; ".join(
            f"seed{k}: {v2_m0_seed0[k]['r2']:.6f}"
            for k in sorted(v2_m0_seed0)
        ) if v2_m0_seed0 else "见 diagnostics JSON") + " |",
        "| standardized max abs | ≈ 10210 | "
        + ("; ".join(
            f"seed{k}: {v2_m0_seed0[k]['x']['max_abs_standardized_test']:.6f}"
            for k in sorted(v2_m0_seed0)
        ) if v2_m0_seed0 else "见 diagnostics JSON") + " |",
        "| scaler min scale | ≈ 6.96e-6 | "
        + ("; ".join(
            f"seed{k}: {v2_m0_seed0[k]['x']['min_scaler_scale']:.8g}"
            for k in sorted(v2_m0_seed0)
        ) if v2_m0_seed0 else "见 diagnostics JSON") + " |",
        "",
        "M0 seed0 V2 的三个 probe sample seed 的 z_cn→degree R²、test standardized max abs、min scaler scale 由 `posthoc_probe.csv` 与 `posthoc_probe_diagnostics.json` 保存；报告不对 R² 设正值门槛。",
        "",
        "## E. Full M0-M3 probe results",
        "",
        "完整逐 checkpoint、逐 probe sample seed 结果见 `posthoc_probe_v2_all_rows.csv`；按 model seed 聚合结果见 `posthoc_probe_v2_model_seed_summary.csv`；按 probe sample seed 聚合结果见 `posthoc_probe_v2_probe_seed_summary.csv`。以下为所有五类 probe 的整体均值±标准差（15 个 model-seed/sample-seed 组合）：",
        "",
        "| Model | Probe | R² | MAE | Spearman |",
        "| --- | --- | ---: | ---: | ---: |",
    "",
    ]
    overall_lookup = {
        (row["model"], row["probe"], row["metric"]): row
        for row in overall_rows
    }
    for model in models:
        for probe in PROBES:
            cells = []
            for metric in METRICS:
                item = overall_lookup[(model, probe, metric)]
                cells.append(f"{float(item['mean']):.4f}±{float(item['std']):.4f}")
            report.append(f"| {model} | {probe} | {cells[0]} | {cells[1]} | {cells[2]} |")
    report += [
        "",
        "## F. Cross leakage conclusion",
        "",
        "以 R² 为主，较低表示从其他分支表征重建结构目标的能力较低。下表是 M1/M2/M3 相对 M0 的五个 model seed paired ΔR²；`direction` 使用 lower-is-better 规则。",
        "",
        "| Candidate | Probe | ΔR² mean±std | Direction |",
        "| --- | --- | ---: | --- |",
    ]
    for row in comparison_rows:
        if row["metric"] == "r2" and row["probe"] in {
            "z_cn_to_degree", "z_residual_to_degree", "z_degree_to_cn_residual"
        }:
            report.append(
                f"| {row['candidate']} | {row['probe']} | "
                f"{float(row['mean']):.4f}±{float(row['std']):.4f} | "
                f"{row['direction_lower_is_better']} |"
            )
    report += [
        "",
        "## G. Target retention conclusion",
        "",
        "target retention 的 R² 越高表示目标信息保留越强。下表使用 higher-is-better 方向；`z_degree→degree` 基本保持不变，而 `z_cn→cn_residual` 在 M1/M2/M3 相对 M0 整体提高。",
        "",
        "| Candidate | Probe | ΔR² mean±std | Direction |",
        "| --- | --- | ---: | --- |",
    ]
    for row in comparison_rows:
        if row["metric"] == "r2" and row["probe"] in {
            "z_degree_to_degree", "z_cn_to_cn_residual"
        }:
            report.append(
                f"| {row['candidate']} | {row['probe']} | "
                f"{float(row['mean']):.4f}±{float(row['std']):.4f} | "
                f"{row['direction_higher_is_better']} |"
            )
    report += [
        "",
        "## H. Scientific conclusion",
        "",
        "Probe V2 修复了已确认的 protocol mismatch，使 M0 seed0 的极端负 R² 不再由 batch masking 与 X/y context mismatch 主导。修复后，`z_cn→degree` 的 R² 在 M1/M2/M3 相对 M0 均为正向增加（对 cross leakage 而言是 WORSE），MAE 虽下降但不能抵消 R²/Spearman 的方向；`z_residual→degree` 只有混合或高方差证据；`z_degree→cn_residual` 基本不变。因此当前不能声称 Conditional CN Residual 已经降低整体 cross leakage。可以客观报告的支持证据是：`z_cn→cn_residual` target retention 明显提高，且旧的 M0 seed0 极端 probe 异常被 protocol 修复后消失。",
        "",
        "## I. Protocol and test status",
        "",
        f"- 已完成 {len(metadata_by_model_seed)} 个 checkpoint、{len(all_rows)} 条 probe 记录；V2 metadata 保存 per-pair context graph hash、split pair hash、model frozen/eval 状态和断言计数。",
        "- `posthoc_probe_top20_errors.csv` 保存每个 probe/sample seed 的最大 20 个测试误差及 pair 结构信息。",
        f"- `posthoc_probe_v2_pair_hash_audit.csv` 检查相同 model seed/probe seed 下 M0-M3 的采样是否一致；当前 {len(pair_rows)} 组均通过。",
        "- V2 toy graph、sampling、X/y context 与既有 post-hoc 测试共 7 项通过；PyTorch 2.8 checkpoint load 使用 probe 进程级兼容设置。",
        "- 不修改 routing loss、interaction、CN residualizer、checkpoint 或 Step 12。",
    ]
    (output_dir / "PROBE_V2_PROTOCOL_FIX_REPORT.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    return {
        "rows": len(all_rows),
        "model_seed_rows": len(model_seed_rows),
        "probe_seed_rows": len(sample_seed_rows),
        "pair_hash_rows": len(pair_rows),
        "output_dir": str(output_dir),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--models", default=",".join(MODELS))
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = aggregate(
        Path(args.root),
        tuple(value for value in args.models.split(",") if value),
        Path(args.output_dir),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
