"""Prepare exact V8 trim-sensitivity CSV and configs for plot_figure.py."""
from __future__ import annotations

import csv
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
FIG = OUT / "figures"
RESULTS = json.loads((OUT / "results.json").read_text(encoding="utf-8"))
rows = []
for key in ("0.00", "0.10", "0.25", "0.40", "0.60"):
    item = RESULTS["trim_sensitivity"]["by_alpha"][key]
    rows.append({
        "trim_ratio_percent": round(float(item["alpha"]) * 100, 1),
        "effective_runner_up_fraction": float(item["effective_runner_up_fraction"]),
        "validation_mrr": float(item["validation_mrr"]),
        "mean_selected_Rg": float(item["mean_selected_Rg"]),
        "p95_selected_Rg": float(item["p95_selected_Rg"]),
        "extreme_hard_fraction": float(item["extreme_hard_fraction"]),
    })

source_dir = FIG / "source_data"
source_dir.mkdir(parents=True, exist_ok=True)
csv_path = source_dir / "trim_sensitivity_input.csv"
with csv_path.open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

config_dir = OUT / "figure_configs"
config_dir.mkdir(parents=True, exist_ok=True)
shared = {
    "kind": "line", "input": "../figures/source_data/trim_sensitivity_input.csv",
    "x": "trim_ratio_percent", "figsize": [3.5, 2.6],
    "font_size": 8, "label_size": 8, "tick_size": 7, "legend_size": 7,
    "xlim": [0, 60], "grid": True,
}
configs = [
    {
        **shared, "figure_id": "trim_vs_mrr", "y": "validation_mrr",
        "xlabel": "Nominal QTHS trim ratio (%)",
        "ylabel": "Cora validation MRR (seed 0)", "ylim": [0, 1],
        "caption": "Cora validation MRR at fixed epoch 10 for seed 0 across the registered trim ratios. The main method remains QTHS25; these five observations are a descriptive sensitivity analysis and are not used to select a new rule. No error bars are shown because only one seed is plotted. The nominal alpha is the fraction of candidate-occurrence slots in the frozen two-candidate prepool; values above 50% saturate at replacing all positive rows.",
    },
    {
        **shared, "figure_id": "trim_vs_hardness", "y": "mean_selected_Rg",
        "xlabel": "Nominal QTHS trim ratio (%)",
        "ylabel": "Mean selected graph-teacher hardness Rg", "ylim": [0, 1],
        "caption": "Mean selected negative hardness Rg on Cora for seed 0 across the registered trim ratios. Rg is the within-positive percentile of the frozen graph-teacher score among 20 training candidates, with 1 denoting the hardest candidate. This is a descriptive selection statistic, not a causal measure. No error bars are shown because only one seed is plotted; QTHS25 remains the frozen main rule.",
    },
]
for config in configs:
    (config_dir / f"{config['figure_id']}.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"rows": rows, "csv": str(csv_path), "configs": [c["figure_id"] for c in configs]}, indent=2))
