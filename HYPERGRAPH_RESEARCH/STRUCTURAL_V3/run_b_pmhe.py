"""Sequential PMHE falsification; test scoring is gated on validation GO."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "structural_v3" / "B_PMHE"
DATA = ROOT / "data"
ARMS = {
    "B0": "raw",
    "B1": "pmhe_mean",
    "B2": "pmhe_second",
    "B3": "pmhe_pair",
}


def run(label: str, mode: str, epochs: int) -> dict:
    stage = f"F{0 if epochs == 1 else 1}"
    out = RUNS / stage / label
    out.mkdir(parents=True, exist_ok=True)
    args = [
        sys.executable, "-m", "dcdlp.cli", "train", "--dataset", "cora",
        "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
        "--seed", "0", "--ablation", "A5", "--pretrain-epochs", str(epochs),
        "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
        "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
        "--device", "cuda", "--output-dir", str(out), "--hypergraph-mode", mode,
        "evaluate_test=false", "negatives_per_positive_eval=20",
    ]
    (out / "config.json").write_text(json.dumps({
        "argv": args, "evaluate_test": False, "stage": stage,
        "epochs": epochs, "mode": mode,
        "moment_definition": "mean unordered Hadamard product over all incidence nodes in the star",
    }, indent=2))
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    started = time.time()
    with (out / "stdout.log").open("w", encoding="utf-8") as stdout, \
            (out / "stderr.log").open("w", encoding="utf-8") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"{label} failed ({proc.returncode}); inspect {out / 'stderr.log'}")
    result = json.loads((out / "stdout.log").read_text(encoding="utf-8"))
    result["wall_seconds"] = time.time() - started
    result["stage"] = stage
    result["mode"] = mode
    (out / "metrics.json").write_text(json.dumps(result, indent=2))
    return result


def evaluate_test(label: str, checkpoint: str) -> dict:
    out = RUNS / "test_once" / label
    out.mkdir(parents=True, exist_ok=True)
    args = [
        sys.executable, "-m", "dcdlp.cli", "evaluate", "--dataset", "cora",
        "--data-root", str(DATA), "--protocol", "standard", "--seed", "0",
        "--protocols", "standard", "--checkpoint", checkpoint,
        "--output-dir", str(out),
    ]
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    with (out / "stdout.log").open("w", encoding="utf-8") as stdout, \
            (out / "stderr.log").open("w", encoding="utf-8") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"test evaluation {label} failed; inspect {out / 'stderr.log'}")
    return json.loads((out / "evaluation.json").read_text(encoding="utf-8"))


def write_status(**fields) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    fields["updated"] = time.time()
    (RUNS / "status.json").write_text(json.dumps(fields, indent=2))


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict] = {"F0": {}, "F1": {}}
    write_status(state="running", stage="F0", current=None, completed=[])
    for label, mode in ARMS.items():
        write_status(state="running", stage="F0", current=label,
                     completed=list(results["F0"]))
        results["F0"][label] = run(label, mode, 1)
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    f0 = {name: float(row["validation"]["mrr"])
          for name, row in results["F0"].items()}
    if f0["B3"] < f0["B0"] - 0.005:
        write_status(state="complete", candidate="B_PMHE", decision="REJECT_F0",
                     validation_mrr={"F0": f0}, completed=list(results["F0"]))
        return

    for label, mode in ARMS.items():
        write_status(state="running", stage="F1", current=label,
                     completed=list(results["F1"]), f0_mrr=f0)
        results["F1"][label] = run(label, mode, 5)
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    f1 = {name: float(row["validation"]["mrr"])
          for name, row in results["F1"].items()}
    gain = f1["B3"] - f1["B0"]
    effect = gain >= 0.003 or gain / max(f1["B0"], 1e-12) >= 0.02
    go = all(f1["B3"] > f1[name] for name in ("B0", "B1", "B2")) and effect
    if go:
        control = max(("B1", "B2"), key=lambda name: f1[name])
        write_status(state="running", stage="test_once", current="B0",
                     validation_mrr=f1, winner="B3", matched_control=control)
        test_results = {
            "B0": evaluate_test("B0", results["F1"]["B0"]["checkpoint"]),
            control: evaluate_test(control, results["F1"][control]["checkpoint"]),
            "B3": evaluate_test("B3", results["F1"]["B3"]["checkpoint"]),
        }
        results["test_once"] = test_results
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    else:
        control = max(("B1", "B2"), key=lambda name: f1[name])
        test_results = None
    branch_count = int(results["F1"]["B3"].get("structural_branch_parameter_count", 0))
    raw_count = int(results["F1"]["B0"].get("trainable_parameter_count", 0))
    write_status(state="complete", candidate="B_PMHE",
                 decision="GO" if go else "REJECT", winner="B3" if go else None,
                 matched_control=control, validation_mrr={"F0": f0, "F1": f1},
                 absolute_gain=gain, relative_gain=gain / max(f1["B0"], 1e-12),
                 structural_branch_parameter_count=branch_count,
                 raw_trainable_parameter_count=raw_count, test_results=test_results,
                 completed=list(results["F1"]))
    (RUNS / "results.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", error=str(exc))
        raise
