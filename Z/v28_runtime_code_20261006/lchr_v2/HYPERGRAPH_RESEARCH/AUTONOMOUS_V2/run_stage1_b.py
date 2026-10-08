"""Sequential Candidate B seed-0 falsification on the offline V100 host."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "autonomous_v2" / "B_RAHC"
DATA = ROOT / "data"
ARMS = {
    "B1": "raw",
    "B2": "size_calibration",
    "B3": "shuffled_redundancy",
    "B4": "redundancy_calibration",
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
    (out / "config.json").write_text(json.dumps({"argv": args, "top_m": 3,
                                                  "evaluate_test": False}, indent=2))
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
    run("smoke_B4", "smoke", "redundancy_calibration")
    results = {}
    for label, mode in ARMS.items():
        (RUNS / "status.json").write_text(json.dumps({
            "state": "running", "current": label, "completed": list(results), "updated": time.time()
        }))
        results[label] = run(label, "cora", mode)
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    mrr = {key: float(row["validation"]["mrr"]) for key, row in results.items()}
    gain = mrr["B4"] - mrr["B1"]
    go = all(mrr["B4"] > mrr[key] for key in ("B1", "B2", "B3")) and (
        gain >= 0.003 or gain / max(mrr["B1"], 1e-12) >= 0.02
    )
    decision = "GO" if go else "REJECT" if any(
        mrr["B4"] <= mrr[key] for key in ("B1", "B2", "B3")
    ) else "BORDERLINE"
    (RUNS / "status.json").write_text(json.dumps({
        "state": "complete", "candidate": "B_RAHC", "decision": decision,
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
