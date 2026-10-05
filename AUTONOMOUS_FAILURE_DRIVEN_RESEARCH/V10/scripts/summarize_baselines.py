from __future__ import print_function

import glob
import json
import os
import re
import statistics


ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "raw", "formal")


def summary(values):
    keys = ["mrr", "hits@10", "hits@20", "hits@30", "hits@50", "auc"]
    return {k: {"mean": statistics.mean([v[k] for v in values]),
                "sd": statistics.stdev([v[k] for v in values]) if len(values) > 1 else 0.0,
                "values": [v[k] for v in values]} for k in keys}


def main():
    rows = []
    for path in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(path)
        match = re.search(r"induc_sp_augment_(cora|citeseer)-sage-sum-hits@20-20-500-(none|duplicated)-", name)
        if not match:
            continue
        dataset, augmentation = match.groups()
        lines = [line for line in open(path, encoding="utf-8") if line.startswith("Overall,")]
        line = lines[-1]
        metrics = {key: float(value) for key, value in re.findall(
            r"(hits@10|hits@20|hits@30|hits@50|mrr|auc): ([0-9.]+)", line)}
        rows.append({"dataset": dataset, "augmentation": augmentation,
                     "metrics": metrics, "source": path})

    aggregate = {}
    for dataset in ["cora", "citeseer"]:
        aggregate[dataset] = {}
        for augmentation in ["none", "duplicated"]:
            values = [row["metrics"] for row in rows
                      if row["dataset"] == dataset and row["augmentation"] == augmentation]
            aggregate[dataset][augmentation] = summary(values)

    validation = {}
    for path in glob.glob(os.path.join(ROOT, "*.log")):
        name = os.path.basename(path)
        match = re.match(r"(cora|citeseer)_(none|duplicated)_seed([123])\.log", name)
        if not match:
            continue
        dataset, augmentation, seed = match.groups()
        values = []
        for line in open(path, encoding="utf-8", errors="ignore"):
            value = line.strip()
            if re.fullmatch(r"0\.\d+(?:[eE][-+]?\d+)?", value):
                values.append(float(value))
        validation.setdefault(dataset, {}).setdefault(augmentation, {})[seed] = {
            "best_validation_hits20": max(values),
            "epochs_logged": len(values),
        }

    output = {"aggregate_test": aggregate, "validation_trace": validation,
              "selection_metric": "validation_hits@20", "test_used_for_selection": False}
    out_path = os.path.join(os.path.dirname(ROOT), "baseline_summary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, sort_keys=True)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
