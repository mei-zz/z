"""Sequential, validation-only ECNH screen and registered confirmations."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "HYPERGRAPH_RESEARCH" / "CONSTRUCTION_V4" / "B_ECNH" / "remote_evidence"
DATA = ROOT / "data"
ARMS = {
    "B0": "raw_star",
    "B1": "ecnh_random",
    "B2": "ecnh_union",
    "B3": "ecnh_true",
}


def write_status(**fields) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    fields["updated"] = time.time()
    (RUNS / "status.json").write_text(json.dumps(fields, indent=2), encoding="utf-8")


def run(label: str, construction: str, epochs: int, stage: str, seed: int = 0) -> dict:
    out = RUNS / stage / (f"seed{seed}" if stage == "seed_confirmation" else "") / label
    out.mkdir(parents=True, exist_ok=True)
    args = [
        sys.executable, "-m", "dcdlp.cli", "train", "--dataset", "cora",
        "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
        "--seed", str(seed), "--ablation", "A5", "--pretrain-epochs", str(epochs),
        "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
        "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
        "--device", "cuda", "--output-dir", str(out), "--hypergraph-mode", "raw",
        "--hypergraph-construction", construction,
        "evaluate_test=false", "negatives_per_positive_eval=20",
    ]
    config = {
        "argv": args, "test_evaluated": False, "stage": stage, "epochs": epochs,
        "arm": label, "hypergraph_mode": "raw", "hypergraph_construction": construction,
        "dataset": "cora", "protocol": "standard", "seed": seed,
        "ablation": "A5", "split_hash_expected": "4ad9a114f501" if seed == 0 else None,
        "common_neighbor_cap": 16,
    }
    (out / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    started = time.time()
    with (out / "stdout.log").open("w", encoding="utf-8") as stdout, \
            (out / "stderr.log").open("w", encoding="utf-8") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"{label}/{stage} failed ({proc.returncode}); inspect {out / 'stderr.log'}")
    result = json.loads((out / "stdout.log").read_text(encoding="utf-8"))
    result["wall_seconds"] = time.time() - started
    result["stage"] = stage
    result["arm"] = label
    result["hypergraph_construction"] = construction
    result["seed"] = seed
    result["test_evaluated"] = False
    (out / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def best_mrr(results: dict[str, dict]) -> dict[str, float]:
    return {label: float(row["validation"]["mrr"]) for label, row in results.items()}


def evaluate_test(label: str, result: dict) -> dict:
    out = RUNS / "post_go_test" / label
    out.mkdir(parents=True, exist_ok=True)
    args = [sys.executable, "-m", "dcdlp.cli", "evaluate", "--dataset", "cora",
            "--data-root", str(DATA), "--checkpoint", result["checkpoint"],
            "--protocols", "standard", "--output-dir", str(out)]
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    with (out / "stdout.log").open("w", encoding="utf-8") as stdout, \
            (out / "stderr.log").open("w", encoding="utf-8") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"post-GO test evaluation failed for {label}")
    value = json.loads((out / "stdout.log").read_text(encoding="utf-8"))
    (out / "test_evaluation.json").write_text(json.dumps(value, indent=2), encoding="utf-8")
    return value


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[str, dict]] = {"screen_5_epoch": {}, "confirm_10_epoch": {}}
    write_status(state="running", candidate="B_ECNH", stage="screen_5_epoch", current=None,
                 completed=[], test_evaluated=False)
    for label, construction in ARMS.items():
        write_status(state="running", candidate="B_ECNH", stage="screen_5_epoch", current=label,
                     completed=list(results["screen_5_epoch"]), test_evaluated=False)
        results["screen_5_epoch"][label] = run(label, construction, 5, "screen_5_epoch")
        (RUNS / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    screen = best_mrr(results["screen_5_epoch"])
    potential = (screen["B3"] > screen["B0"] + 0.001
                 and screen["B3"] > screen["B1"] and screen["B3"] > screen["B2"])
    best_control = max(("B1", "B2"), key=lambda label: screen[label])
    if potential:
        for label in ("B0", best_control, "B3"):
            write_status(state="running", candidate="B_ECNH", stage="confirm_10_epoch", current=label,
                         completed=list(results["confirm_10_epoch"]), screen_mrr=screen,
                         test_evaluated=False)
            results["confirm_10_epoch"][label] = run(label, ARMS[label], 10, "confirm_10_epoch")
            (RUNS / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        confirm = best_mrr(results["confirm_10_epoch"])
        gain = confirm["B3"] - confirm["B0"]
        relative = gain / max(confirm["B0"], 1e-12)
        threshold_met = gain >= 0.003 or relative >= 0.01
        decision = "GO" if (confirm["B3"] > confirm["B0"]
                            and confirm["B3"] > confirm[best_control]
                            and threshold_met) else "REJECT"
        winner = "B3" if decision == "GO" else None
        reason = "10_epoch_GO" if decision == "GO" else "10_epoch_threshold_or_control_failed"
    else:
        gain = screen["B3"] - screen["B0"]
        relative = gain / max(screen["B0"], 1e-12)
        decision, winner = "REJECT", None
        if screen["B3"] <= screen["B0"]:
            reason = "B3_not_above_raw"
        elif gain < 0.001:
            reason = "B3_gain_below_0.001"
        else:
            reason = "B3_did_not_beat_both_controls_or_screen_rule"

    final_decision = decision
    seed_summary = None
    test_results = None
    if decision == "GO":
        seed_results: dict[str, dict[str, dict]] = {}
        for seed in (0, 1, 2):
            seed_results[str(seed)] = {}
            for label in ("B0", best_control, "B3"):
                write_status(state="running", candidate="B_ECNH", stage="seed_confirmation",
                             current=f"seed{seed}/{label}", completed=list(seed_results),
                             single_seed_decision="GO", test_evaluated=False)
                seed_results[str(seed)][label] = run(
                    label, ARMS[label], 10, "seed_confirmation", seed=seed
                )
        seed_mrr = {seed: best_mrr(rows) for seed, rows in seed_results.items()}
        seed_gains = [seed_mrr[seed]["B3"] - seed_mrr[seed]["B0"] for seed in seed_mrr]
        wins = sum(gain_value > 0 for gain_value in seed_gains)
        mean_gain = sum(seed_gains) / len(seed_gains)
        final_decision = "STRONG_SIGNAL" if wins >= 2 and mean_gain > 0 else "INCONCLUSIVE"
        seed_summary = {
            "validation_mrr": seed_mrr, "winner_minus_raw": seed_gains,
            "winner_beats_raw_count": wins, "mean_gain": mean_gain,
            "decision": final_decision,
        }
        test_results = {
            label: evaluate_test(label, seed_results["0"][label])
            for label in ("B0", best_control, "B3")
        }
        (RUNS / "seed_confirmation.json").write_text(json.dumps(seed_summary, indent=2), encoding="utf-8")
        (RUNS / "post_go_test.json").write_text(json.dumps(test_results, indent=2), encoding="utf-8")

    (RUNS / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    write_status(
        state="complete", candidate="B_ECNH", decision=decision, final_decision=final_decision,
        winner=winner, reason=reason, best_control=best_control,
        validation_mrr={
            "screen_5_epoch": screen,
            "confirm_10_epoch": best_mrr(results["confirm_10_epoch"])
            if results["confirm_10_epoch"] else None,
        },
        absolute_gain=gain, relative_gain=relative, seed_confirmation=seed_summary,
        test_results=test_results, test_evaluated=(test_results is not None),
        stop_after_go=(decision == "GO"),
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", candidate="B_ECNH", error=str(exc), test_evaluated=False)
        raise
