from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "runs" / "autonomous_v2" / "A_SSHC" / "A4_revision1"
DATA = ROOT / "data"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    args = [sys.executable, "-m", "dcdlp.cli", "train", "--dataset", "cora",
            "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
            "--seed", "0", "--ablation", "A5", "--pretrain-epochs", "1",
            "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
            "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
            "--device", "cuda", "--output-dir", str(OUT), "--hypergraph-mode", "sshc",
            "evaluate_test=false", "negatives_per_positive_eval=20"]
    (OUT / "config.json").write_text(json.dumps({"argv": args, "alpha_logit_init": -3.0,
                                                  "evaluate_test": False}, indent=2))
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    start = time.time()
    with (OUT / "stdout.log").open("w") as stdout, (OUT / "stderr.log").open("w") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError(f"A4 revision failed ({proc.returncode}); see {OUT / 'stderr.log'}")
    result = json.loads((OUT / "stdout.log").read_text())
    result["wall_seconds"] = time.time() - start
    result["targeted_revision"] = "one alpha initialization change: logit -5 to -3"
    (OUT / "metrics.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({"validation_mrr": result["validation"]["mrr"],
                      "alpha_logit_init": -3.0,
                      "alpha_learned": float(__import__("torch").sigmoid(
                          __import__("torch").load(result["checkpoint"], map_location="cpu",
                                                     weights_only=False)["model"]["hypergraph.calibration_logit"]
                      )),
                      "test_evaluated": False}, indent=2))


if __name__ == "__main__":
    main()
