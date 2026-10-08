"""Sequential Candidate A seed-0 falsification on the offline V100 host."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "autonomous_v2" / "A_SSHC"
DATA = ROOT / "data"
ARMS = {
    "A0": "disabled",
    "A1": "raw",
    "A2": "size_calibration",
    "A3": "shuffled_cohesion",
    "A4": "sshc",
}


def run(label: str, dataset: str, mode: str) -> dict:
    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    args = [
        sys.executable, "-m", "dcdlp.cli", "train", "--dataset", dataset,
        "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
        "--seed", "0", "--ablation", "A5", "--pretrain-epochs", "1",
        "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
        "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
        "--device", "cuda", "--output-dir", str(out), "--hypergraph-mode", mode,
        "evaluate_test=false", f"negatives_per_positive_eval={10 if dataset == 'smoke' else 20}",
    ]
    (out / "config.json").write_text(json.dumps({"argv": args, "evaluate_test": False}, indent=2))
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


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / "status.json").write_text(json.dumps({"state": "smoke", "started": time.time()}))
    run("smoke_A4", "smoke", "sshc")
    results = {}
    for label, mode in ARMS.items():
        (RUNS / "status.json").write_text(json.dumps({
            "state": "running", "current": label, "completed": list(results), "updated": time.time()
        }))
        results[label] = run(label, "cora", mode)
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    mrr = {key: float(row["validation"]["mrr"]) for key, row in results.items()}
    gain = mrr["A4"] - mrr["A1"]
    go = all(mrr["A4"] > mrr[key] for key in ("A1", "A2", "A3")) and (
        gain >= 0.003 or gain / max(mrr["A1"], 1e-12) >= 0.02
    )
    decision = "GO" if go else (
        "REJECT"
        if any(mrr["A4"] <= mrr[key] for key in ("A1", "A2", "A3"))
        else "BORDERLINE"
    )
    (RUNS / "status.json").write_text(json.dumps({
        "state": "complete", "candidate": "A_SSHC", "decision": decision,
        "validation_mrr": mrr, "updated": time.time()
    }, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        RUNS.mkdir(parents=True, exist_ok=True)
        (RUNS / "status.json").write_text(json.dumps({
            "state": "failed", "error": str(exc), "updated": time.time()
        }, indent=2))
        raise
