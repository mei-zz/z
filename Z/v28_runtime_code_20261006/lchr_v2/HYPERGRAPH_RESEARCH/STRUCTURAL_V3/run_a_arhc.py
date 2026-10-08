"""Sequential, validation-only ARHC falsification on the offline V100 host."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "structural_v3" / "A_ARHC"
DATA = ROOT / "data"
ARMS = {
    "A0": "raw",
    "A1": "arhc_symmetric",
    "A2": "arhc_role",
    "A3": "arhc_full",
}


def run(label: str, mode: str, epochs: int) -> dict:
    out = RUNS / f"F{0 if epochs == 1 else 1}" / label
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
        "argv": args, "evaluate_test": False, "stage": f"F{0 if epochs == 1 else 1}",
        "epochs": epochs, "mode": mode,
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
    result["stage"] = f"F{0 if epochs == 1 else 1}"
    result["mode"] = mode
    (out / "metrics.json").write_text(json.dumps(result, indent=2))
    return result


def write_status(**fields) -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    fields["updated"] = time.time()
    (RUNS / "status.json").write_text(json.dumps(fields, indent=2))


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    all_results: dict[str, dict] = {"F0": {}, "F1": {}}
    write_status(state="running", stage="F0", current=None, completed=[])
    for label, mode in ARMS.items():
        write_status(state="running", stage="F0", current=label,
                     completed=list(all_results["F0"]))
        all_results["F0"][label] = run(label, mode, 1)
        (RUNS / "results.json").write_text(json.dumps(all_results, indent=2))
    f0 = {name: float(row["validation"]["mrr"])
          for name, row in all_results["F0"].items()}
    if f0["A3"] < f0["A0"] - 0.005:
        write_status(state="complete", candidate="A_ARHC", decision="REJECT_F0",
                     validation_mrr={"F0": f0}, completed=list(all_results["F0"]))
        return

    for label, mode in ARMS.items():
        write_status(state="running", stage="F1", current=label,
                     completed=list(all_results["F1"]), f0_mrr=f0)
        all_results["F1"][label] = run(label, mode, 5)
        (RUNS / "results.json").write_text(json.dumps(all_results, indent=2))
    f1 = {name: float(row["validation"]["mrr"])
          for name, row in all_results["F1"].items()}

    a4_mrr = None
    if f1["A3"] > max(f1["A0"], f1["A1"], f1["A2"]):
        write_status(state="running", stage="F1", current="A4", completed=list(all_results["F1"]),
                     f1_mrr=f1)
        a4 = run("A4", "arhc_anchor_shuffled", 5)
        all_results["F1"]["A4"] = a4
        a4_mrr = float(a4["validation"]["mrr"])
        (RUNS / "results.json").write_text(json.dumps(all_results, indent=2))

    full_gain = f1["A3"] - f1["A0"]
    full_effect = full_gain >= 0.003 or full_gain / max(f1["A0"], 1e-12) >= 0.02
    full_go = (f1["A3"] > f1["A0"] and f1["A3"] > f1["A1"] and full_effect
               and (a4_mrr is None or f1["A3"] > a4_mrr))
    role_gain = f1["A2"] - f1["A0"]
    role_effect = role_gain >= 0.003 or role_gain / max(f1["A0"], 1e-12) >= 0.02
    role_go = (f1["A2"] > f1["A0"] and f1["A2"] > f1["A1"]
               and f1["A3"] <= f1["A2"] and role_effect)
    winner = "A3" if full_go else ("A2" if role_go else None)
    write_status(state="complete", candidate="A_ARHC",
                 decision="GO" if winner else "REJECT", winner=winner,
                 validation_mrr={"F0": f0, "F1": f1},
                 absolute_gain=(full_gain if winner == "A3" else role_gain) if winner else None,
                 relative_gain=((full_gain if winner == "A3" else role_gain)
                                / max(f1["A0"], 1e-12)) if winner else None,
                 completed=list(all_results["F1"]))
    (RUNS / "results.json").write_text(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", error=str(exc))
        raise
