from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


MODEL_IDS = ["A_EarlyEarly", "B_LateLate", "C_CDPT", "D_ConcatMLP", "E_FixedRandom"]
METRICS = ["mrr", "hits10", "hits20", "hits50", "hits100"]
T95_DF4 = 2.7764451051977987


def mean(values):
    return sum(values) / len(values) if values else None


def sd(values):
    if len(values) < 2:
        return 0.0 if values else None
    mu = mean(values)
    return math.sqrt(sum((value - mu) ** 2 for value in values) / (len(values) - 1))


def summary(values):
    mu = mean(values)
    sigma = sd(values)
    half = T95_DF4 * sigma / math.sqrt(len(values)) if values else None
    return {
        "values": values,
        "mean": mu,
        "sd": sigma,
        "t95_interval": [mu - half, mu + half] if values else None,
        "wins_positive": sum(value > 0 for value in values),
        "ties": sum(value == 0 for value in values),
        "wins_negative": sum(value < 0 for value in values),
    }


def load_runs(root: Path):
    runs = {}
    for seed_dir in sorted(root.glob("seed*")):
        if not seed_dir.is_dir():
            continue
        for model_id in MODEL_IDS:
            # V4 uses the same JSON schema for Cora and CiteSeer, but the
            # filename prefix follows the dataset name.  Match the seed/model
            # suffix instead of hard-coding Cora.
            paths = sorted(seed_dir.glob(f"*_{seed_dir.name}_{model_id}.json"))
            if paths:
                item = json.loads(paths[0].read_text(encoding="utf-8"))
                runs[(int(item["seed"]), model_id)] = item
    return runs


def metric(item, split, name):
    return float(item["metrics"][split][name])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    runs = load_runs(Path(args.root))
    seeds = sorted({seed for seed, _ in runs})
    result = {"root": args.root, "seeds": seeds, "models": {}, "paired": {}}
    for model_id in MODEL_IDS:
        model_runs = [runs[(seed, model_id)] for seed in seeds if (seed, model_id) in runs]
        result["models"][model_id] = {
            "seeds": [int(item["seed"]) for item in model_runs],
            "validation": {name: summary([metric(item, "validation_best", name) for item in model_runs]) for name in METRICS},
            "test": {name: summary([metric(item, "test_report", name) for item in model_runs]) for name in METRICS},
            "parameter_counts": [item["parameter_count"] for item in model_runs],
            "runtime_seconds": [item["runtime_seconds"] for item in model_runs],
            "peak_gpu_memory_mb": [item["peak_gpu_memory_mb"] for item in model_runs],
            "score_path": [item["score_path"] for item in model_runs],
        }
    for other in ["A_EarlyEarly", "B_LateLate", "D_ConcatMLP", "E_FixedRandom"]:
        paired = {"against": other, "seeds": seeds, "validation": {}, "test": {}}
        for split, key in [("validation_best", "validation"), ("test_report", "test")]:
            for name in METRICS:
                values = [
                    metric(runs[(seed, "C_CDPT")], split, name) - metric(runs[(seed, other)], split, name)
                    for seed in seeds if (seed, "C_CDPT") in runs and (seed, other) in runs
                ]
                paired[key][name] = summary(values)
        result["paired"][other] = paired
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
