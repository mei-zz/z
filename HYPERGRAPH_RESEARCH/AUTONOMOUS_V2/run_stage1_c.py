"""Sequential Candidate C seed-0 falsification on the offline V100 host."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time
from statistics import mean, pstdev


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "autonomous_v2" / "C_HSA"
DATA = ROOT / "data"
ARMS = {
    "C0": ("raw", 0.0),
    "C1": ("hsa", 0.0),
    "C2_lambda005": ("hsa_shuffled", 0.05),
    "C2_lambda01": ("hsa_shuffled", 0.1),
    "C3_lambda005": ("hsa", 0.05),
    "C3_lambda01": ("hsa", 0.1),
}


def run(label: str, dataset: str, mode: str, lambda_aux: float) -> dict:
    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    args = [
        sys.executable, "-m", "dcdlp.cli", "train", "--dataset", dataset,
        "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
        "--seed", "0", "--ablation", "A5", "--pretrain-epochs", "1",
        "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
        "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
        "--device", "cuda", "--output-dir", str(out), "--hypergraph-mode", mode,
        f"lambda_aux={lambda_aux}", "evaluate_test=false",
        f"negatives_per_positive_eval={10 if dataset == 'smoke' else 20}",
    ]
    (out / "config.json").write_text(json.dumps({
        "argv": args, "lambda_aux": lambda_aux,
        "leaf_pairs_per_class_per_hyperedge": 4,
        "evaluate_test": False,
    }, indent=2))
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    start = time.time()
    with (out / "stdout.log").open("w") as stdout, (out / "stderr.log").open("w") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"{label} failed ({proc.returncode}); see {out / 'stderr.log'}")
    result = json.loads((out / "stdout.log").read_text())
    result["wall_seconds"] = time.time() - start
    (out / "metrics.json").write_text(json.dumps(result, indent=2))
    return result


def run_confirmation(seed: int, label: str, mode: str, lambda_aux: float) -> dict:
    out = RUNS / "confirmation" / f"seed{seed}" / label
    out.mkdir(parents=True, exist_ok=True)
    args = [
        sys.executable, "-m", "dcdlp.cli", "train", "--dataset", "cora",
        "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
        "--seed", str(seed), "--ablation", "A5", "--pretrain-epochs", "1",
        "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
        "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
        "--device", "cuda", "--output-dir", str(out), "--hypergraph-mode", mode,
        f"lambda_aux={lambda_aux}", "evaluate_test=false", "negatives_per_positive_eval=20",
    ]
    (out / "config.json").write_text(json.dumps({"argv": args, "lambda_aux": lambda_aux,
                                                  "evaluate_test": False}, indent=2))
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    with (out / "stdout.log").open("w") as stdout, (out / "stderr.log").open("w") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"confirmation {label}, seed {seed} failed; see {out / 'stderr.log'}")
    result = json.loads((out / "stdout.log").read_text())
    (out / "metrics.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / "status.json").write_text(json.dumps({"state": "smoke", "started": time.time()}))
    run("smoke_C3", "smoke", "hsa", 0.05)
    results = {}
    for label, (mode, coefficient) in ARMS.items():
        (RUNS / "status.json").write_text(json.dumps({
            "state": "running", "current": label, "completed": list(results), "updated": time.time()
        }))
        results[label] = run(label, "cora", mode, coefficient)
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    mrr = {key: float(row["validation"]["mrr"]) for key, row in results.items()}
    best_true = max(mrr["C3_lambda005"], mrr["C3_lambda01"])
    control = max(mrr["C0"], mrr["C1"], mrr["C2_lambda005"], mrr["C2_lambda01"])
    gain = best_true - mrr["C0"]
    go = best_true > control and (gain >= 0.003 or gain / max(mrr["C0"], 1e-12) >= 0.02)
    best_label = "C3_lambda005" if mrr["C3_lambda005"] >= mrr["C3_lambda01"] else "C3_lambda01"
    stage1_status = {
        "state": "complete", "candidate": "C_HSA",
        "decision": "GO" if go else "REJECT",
        "best_true_arm": best_label,
        "validation_mrr": mrr, "updated": time.time()
    }
    (RUNS / "status.json").write_text(json.dumps(stage1_status, indent=2))
    if go:
        sys.path.insert(0, str(ROOT / "src"))
        from dcdlp.evaluate import evaluate_checkpoint

        coefficient = ARMS[best_label][1]
        control_label = "C2_lambda005" if coefficient == 0.05 else "C2_lambda01"
        confirmation = {
            "seeds": [0, 1, 2],
            "validation_mrr": {
                "C0_raw": [mrr["C0"]],
                "matched_shuffled": [mrr[control_label]],
                "C3_hsa": [mrr[best_label]],
            },
        }
        for seed in (1, 2):
            raw = run_confirmation(seed, "C0_raw", "raw", 0.0)
            shuffled = run_confirmation(seed, "matched_shuffled", "hsa_shuffled", coefficient)
            candidate = run_confirmation(seed, "C3_hsa", "hsa", coefficient)
            confirmation["validation_mrr"]["C0_raw"].append(float(raw["validation"]["mrr"]))
            confirmation["validation_mrr"]["matched_shuffled"].append(float(shuffled["validation"]["mrr"]))
            confirmation["validation_mrr"]["C3_hsa"].append(float(candidate["validation"]["mrr"]))
        deltas = [c - r for c, r in zip(confirmation["validation_mrr"]["C3_hsa"],
                                       confirmation["validation_mrr"]["C0_raw"])]
        confirmation["paired_delta_candidate_minus_raw"] = deltas
        confirmation["mean_delta"] = mean(deltas)
        confirmation["std_delta_population"] = pstdev(deltas)
        strong = sum(delta > 0 for delta in deltas) >= 2 and mean(deltas) > 0
        confirmation["status"] = "STRONG_SIGNAL" if strong else "INCONCLUSIVE"
        test_results = {"protocol": "standard", "selected_after_validation": True}
        for seed_index, seed in enumerate((0, 1, 2)):
            selected_paths = {
                "C0_raw": (RUNS / "C0" / "metrics.json") if seed == 0 else (
                    RUNS / "confirmation" / f"seed{seed}" / "C0_raw" / "metrics.json"
                ),
                "matched_shuffled": (
                    RUNS / control_label / "metrics.json" if seed == 0 else
                    RUNS / "confirmation" / f"seed{seed}" / "matched_shuffled" / "metrics.json"
                ),
                "C3_hsa": (
                    RUNS / best_label / "metrics.json" if seed == 0 else
                    RUNS / "confirmation" / f"seed{seed}" / "C3_hsa" / "metrics.json"
                ),
            }
            test_results[str(seed)] = {}
            for arm, metrics_path in selected_paths.items():
                trained = json.loads(metrics_path.read_text())
                test_output = evaluate_checkpoint(
                    Path(trained["checkpoint"]), DATA, ["standard"],
                    RUNS / "test_evaluation" / f"seed{seed}" / arm,
                )
                test_results[str(seed)][arm] = test_output["standard"]
        confirmation["test_results"] = test_results
        (RUNS / "confirmation.json").write_text(json.dumps(confirmation, indent=2))
        stage1_status["stage2_status"] = confirmation["status"]
        stage1_status["state"] = "complete"
        (RUNS / "status.json").write_text(json.dumps(stage1_status, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        RUNS.mkdir(parents=True, exist_ok=True)
        (RUNS / "status.json").write_text(json.dumps({
            "state": "failed", "error": str(exc), "updated": time.time()
        }, indent=2))
        raise
