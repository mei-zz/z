"""Sequential ARPM falsification; test scoring is gated on validation GO."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "structural_v3" / "C_ARPM"
DATA = ROOT / "data"
ARMS = {
    "C0": "raw",
    "C1": "pmhe_pair",
    "C2": "arpm_mean",
    "C3": "arpm_pair",
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
        "pair_moment_domain": "star members excluding the currently selected anchor",
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
    if f0["C3"] < f0["C0"] - 0.005:
        write_status(state="complete", candidate="C_ARPM", decision="REJECT_F0",
                     validation_mrr={"F0": f0}, completed=list(results["F0"]))
        return

    for label, mode in ARMS.items():
        write_status(state="running", stage="F1", current=label,
                     completed=list(results["F1"]), f0_mrr=f0)
        results["F1"][label] = run(label, mode, 5)
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    f1 = {name: float(row["validation"]["mrr"])
          for name, row in results["F1"].items()}

    write_status(state="running", stage="F1", current="C4", completed=list(results["F1"]),
                 f1_mrr=f1)
    results["F1"]["C4"] = run("C4", "arpm_anchor_shuffled", 5)
    c4_mrr = float(results["F1"]["C4"]["validation"]["mrr"])
    (RUNS / "results.json").write_text(json.dumps(results, indent=2))

    gain = f1["C3"] - f1["C0"]
    effect = gain >= 0.003 or gain / max(f1["C0"], 1e-12) >= 0.02
    base_go = all(f1["C3"] > f1[name] for name in ("C0", "C1", "C2")) and effect
    # The shuffled-anchor arm is a diagnostic preference; the registered GO
    # threshold is defined by the three primary controls and the effect size.
    anchor_shuffle_pass = f1["C3"] > c4_mrr
    go = base_go
    controls = [name for name in ("C1", "C2", "C4") if name in results["F1"]]
    control = max(controls, key=lambda name: float(results["F1"][name]["validation"]["mrr"]))
    test_results = None
    if go:
        test_results = {
            "C0": evaluate_test("C0", results["F1"]["C0"]["checkpoint"]),
            control: evaluate_test(control, results["F1"][control]["checkpoint"]),
            "C3": evaluate_test("C3", results["F1"]["C3"]["checkpoint"]),
        }
        results["test_once"] = test_results
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))

    branch_count = int(results["F1"]["C3"].get("structural_branch_parameter_count", 0))
    raw_count = int(results["F1"]["C0"].get("trainable_parameter_count", 0))
    write_status(state="complete", candidate="C_ARPM",
                 decision="GO" if go else "REJECT", winner="C3" if go else None,
                 matched_control=control, validation_mrr={"F0": f0, "F1": f1},
                 absolute_gain=gain, relative_gain=gain / max(f1["C0"], 1e-12),
                 c4_validation_mrr=c4_mrr, anchor_shuffle_pass=anchor_shuffle_pass,
                 base_go=base_go, structural_branch_parameter_count=branch_count,
                 raw_trainable_parameter_count=raw_count, test_results=test_results,
                 completed=list(results["F1"]))
    (RUNS / "results.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", error=str(exc))
        raise
