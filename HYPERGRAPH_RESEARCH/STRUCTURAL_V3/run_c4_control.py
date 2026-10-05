"""Run the registered 5-epoch shuffled-anchor ARPM diagnostic control."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "runs" / "structural_v3" / "C_ARPM" / "F1" / "C4"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    args = [
        sys.executable, "-m", "dcdlp.cli", "train", "--dataset", "cora",
        "--data-root", str(DATA), "--protocol", "standard", "--protocol-train", "uniform",
        "--seed", "0", "--ablation", "A5", "--pretrain-epochs", "5",
        "--disentangle-epochs", "0", "--hidden-dim", "16", "--branch-dim", "8",
        "--num-layers", "2", "--dropout", "0", "--batch-size", "4096",
        "--device", "cuda", "--output-dir", str(OUT), "--hypergraph-mode",
        "arpm_anchor_shuffled", "evaluate_test=false", "negatives_per_positive_eval=20",
    ]
    (OUT / "config.json").write_text(json.dumps({
        "argv": args, "evaluate_test": False, "stage": "F1",
        "epochs": 5, "mode": "arpm_anchor_shuffled",
        "registered_diagnostic": "C4; run after C3 failed to lead primary controls",
    }, indent=2))
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUNBUFFERED": "1"}
    started = time.time()
    with (OUT / "stdout.log").open("w", encoding="utf-8") as stdout, \
            (OUT / "stderr.log").open("w", encoding="utf-8") as stderr:
        proc = subprocess.run(args, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
    if proc.returncode:
        raise RuntimeError("C4 training failed; inspect stderr.log")
    result = json.loads((OUT / "stdout.log").read_text(encoding="utf-8"))
    result["wall_seconds"] = time.time() - started
    result["stage"] = "F1"
    result["mode"] = "arpm_anchor_shuffled"
    (OUT / "metrics.json").write_text(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
