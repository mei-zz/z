"""Reanalyse saved V11 trajectories without training or reading test metrics."""
import glob
import hashlib
import json
import os
from collections import defaultdict
from statistics import mean, pstdev


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.path.join(ROOT, "..", "V11", "raw", "formal_repaired")
OUTPUT = os.path.join(ROOT, "raw", "v11_m2_selection.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def choose(history, fn):
    # Equivalent to V11's earliest-epoch tie break.
    return max(history, key=lambda row: (fn(row), -row["epoch"]))


def main():
    rows = []
    for path in sorted(glob.glob(os.path.join(INPUT, "*.json"))):
        with open(path, encoding="utf-8") as f:
            obj = json.load(f)
        name = os.path.basename(path)
        dataset = "CiteSeer" if name.startswith("citeseer") else "Cora"
        model = "NodeDup" if "duplicated" in name else "GraphSAGE"
        history = obj["history"]
        a = choose(history, lambda x: x["old_old"]["hits@20"])
        b = choose(history, lambda x: x["old_old"]["mrr"])
        c = choose(history, lambda x: x["combined"]["hits@20"])
        d = choose(history, lambda x: x["combined"]["mrr"])
        m2 = choose(history, lambda x: 0.5 * x["old_old"]["mrr"] + 0.5 * x["new"]["mrr"])
        row = {
            "source_file": os.path.relpath(path, ROOT),
            "source_sha256": sha256(path),
            "dataset": dataset,
            "model": model,
            "seed": obj["seed"],
            "epochs_available": len(history),
            "A_epoch": a["epoch"],
            "B_epoch": b["epoch"],
            "C_epoch": c["epoch"],
            "D_epoch": d["epoch"],
            "M2_epoch": m2["epoch"],
            "M2_equals_D": m2["epoch"] == d["epoch"],
            "M2_equals_B": m2["epoch"] == b["epoch"],
            "M2_selection_score": 0.5 * m2["old_old"]["mrr"] + 0.5 * m2["new"]["mrr"],
            "D_selection_score": 0.5 * d["old_old"]["mrr"] + 0.5 * d["new"]["mrr"],
            "M2_validation": {
                "old_old_mrr": m2["old_old"]["mrr"],
                "new_mrr": m2["new"]["mrr"],
                "combined_mrr": m2["combined"]["mrr"],
                "old_old_hits20": m2["old_old"]["hits@20"],
                "new_hits20": m2["new"]["hits@20"],
                "combined_hits20": m2["combined"]["hits@20"],
            },
            "M2_test_evaluated": False,
            "M2_test_reason": "V11 did not save M2-selected checkpoints or prediction tensors; V11 test was previously viewed and is not independent evidence.",
        }
        rows.append(row)

    grouped = defaultdict(list)
    for row in rows:
        grouped[f"{row['dataset']}::{row['model']}"] .append(row)
    summary = {}
    for key, group in sorted(grouped.items()):
        epochs = [x["M2_epoch"] for x in group]
        summary[key] = {
            "n": len(group),
            "M2_epochs": epochs,
            "mean_M2_epoch": mean(epochs),
            "sd_M2_epoch_population": pstdev(epochs),
            "M2_equals_D_count": sum(x["M2_equals_D"] for x in group),
            "M2_equals_B_count": sum(x["M2_equals_B"] for x in group),
        }

    output = {
        "analysis": "V12 pre-registered M2 reanalysis of V11 saved validation histories",
        "input_directory": os.path.relpath(INPUT, ROOT),
        "formula": "J_M2=0.5*MRR_old_old+0.5*MRR_new",
        "tie_break": "earliest epoch",
        "uses_test_for_selection": False,
        "n_runs": len(rows),
        "rows": rows,
        "summary": summary,
    }
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(json.dumps({"output": OUTPUT, "n_runs": len(rows), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
