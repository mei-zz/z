"""Run the frozen one-seed LCHR screen on an offline server."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "runs" / "lchr_stage1"
DATA = ROOT / "data"
MODES = {
    "B0": "disabled", "B1": "raw", "B2": "random_topk",
    "B3": "global_router", "B4": "lchr",
}


def run(label: str, dataset: str, mode: str) -> dict:
    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    args = [sys.executable, "-m", "dcdlp.cli", "train", "--dataset", dataset,
            "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
            "--seed", "0", "--ablation", "A5", "--pretrain-epochs", "1",
            "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
            "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
            "--device", "cuda", "--output-dir", str(out), "--hypergraph-mode", mode,
            f"negatives_per_positive_eval={10 if dataset == 'smoke' else 20}"]
    (out / "config.json").write_text(json.dumps({"argv": args, "topk": 8}, indent=2))
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    start = time.time()
    with (out / "stdout.log").open("w") as stdout, (out / "stderr.log").open("w") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"{label} failed with exit code {proc.returncode}; see {out / 'stderr.log'}")
    result = json.loads((out / "stdout.log").read_text())
    result["wall_seconds"] = time.time() - start
    (out / "metrics.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    (RUNS / "status.json").write_text(json.dumps({"state": "smoke", "started": time.time()}))
    run("smoke_B4", "smoke", "lchr")
    results = {}
    for label, mode in MODES.items():
        (RUNS / "status.json").write_text(json.dumps({"state": "running", "current": label,
                                                       "completed": list(results), "updated": time.time()}))
        results[label] = run(label, "cora", mode)
        (RUNS / "results.json").write_text(json.dumps(results, indent=2))
    v = {key: float(value["validation"]["mrr"]) for key, value in results.items()}
    gain = v["B4"] - v["B3"]
    decision = "GO" if all(v["B4"] > v[key] for key in ("B1", "B2", "B3")) and (
        gain >= 0.003 or gain / max(v["B3"], 1e-12) >= 0.02
    ) else "REJECT" if v["B4"] <= v["B3"] or v["B4"] <= v["B2"] else "BORDERLINE"
    (RUNS / "status.json").write_text(json.dumps({"state": "complete", "decision": decision,
                                                   "validation_mrr": v, "updated": time.time()}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        RUNS.mkdir(parents=True, exist_ok=True)
        (RUNS / "status.json").write_text(json.dumps({"state": "failed", "error": str(exc),
                                                       "updated": time.time()}, indent=2))
        raise
