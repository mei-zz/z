from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np


METRICS = ("mrr", "hits10", "hits20", "hits50", "hits100")
T975_DF4 = 2.7764451051977987


def read_results(roots: list[Path]) -> list[dict]:
    records = []
    for root in roots:
        for path in sorted(root.rglob("*.json")):
            if path.name.endswith("manifest.json"):
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            if "model_id" in payload and "metrics" in payload:
                payload["_path"] = str(path)
                records.append(payload)
    return records


def summary(values: list[float]) -> dict:
    array = np.asarray(values, dtype=float)
    mean = float(np.mean(array))
    std = float(np.std(array, ddof=1)) if len(array) > 1 else 0.0
    result = {"n": int(len(array)), "mean": mean, "std": std,
              "min": float(np.min(array)), "max": float(np.max(array))}
    if len(array) == 5:
        half = T975_DF4 * std / math.sqrt(5)
        result["approx_95pct_t_interval"] = [mean - half, mean + half]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    records = read_results([Path(root) for root in args.roots])
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        grouped[(record["dataset"], record["model_id"])].append(record)

    output = {"records": len(records), "groups": {}}
    for (dataset, model_id), items in sorted(grouped.items()):
        items.sort(key=lambda item: int(item["seed"]))
        group = {"seeds": [int(item["seed"]) for item in items],
                 "source_paths": [item["_path"] for item in items],
                 "metrics": {}}
        for split in ("validation_best", "test_report"):
            group["metrics"][split] = {
                metric: summary([item["metrics"][split][metric] for item in items])
                for metric in METRICS
            }
        group["parameters"] = {
            "total": sorted({item["parameter_count"]["total"] for item in items}),
            "trainable": sorted({item["parameter_count"]["trainable"] for item in items}),
        }
        group["runtime_seconds"] = summary([float(item["runtime_seconds"]) for item in items])
        peak_values = [item.get("peak_gpu_memory_mb") for item in items
                       if item.get("peak_gpu_memory_mb") is not None]
        group["peak_gpu_memory_mb"] = summary([float(value) for value in peak_values]) if peak_values else None
        output["groups"][f"{dataset}/{model_id}"] = group

    for dataset in sorted({record["dataset"] for record in records}):
        baseline = {
            int(item["seed"]): item for item in grouped.get((dataset, "B0_Parent"), [])
        }
        for model_id in sorted({record["model_id"] for record in records if record["dataset"] == dataset}):
            if model_id == "B0_Parent":
                continue
            items = grouped[(dataset, model_id)]
            paired = []
            for item in items:
                base = baseline.get(int(item["seed"]))
                if base is None:
                    continue
                row = {"seed": int(item["seed"])}
                for split in ("validation_best", "test_report"):
                    row[split] = {
                        metric: float(item["metrics"][split][metric] - base["metrics"][split][metric])
                        for metric in METRICS
                    }
                paired.append(row)
            output.setdefault("paired_deltas_vs_B0", {})[f"{dataset}/{model_id}"] = {
                "rows": paired,
                "improved_count": {
                    split: {metric: sum(row[split][metric] > 0 for row in paired)
                            for metric in METRICS}
                    for split in ("validation_best", "test_report")
                },
                "summary": {
                    split: {metric: summary([row[split][metric] for row in paired])
                            for metric in METRICS}
                    for split in ("validation_best", "test_report")
                    if paired
                },
            }

    Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({"records": len(records), "groups": len(grouped), "output": args.output}, indent=2))


if __name__ == "__main__":
    main()
