"""Run the 2×4×3 HL-GNN-PDG V0 matrix sequentially on one GPU."""

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--data-root", default="~/dataset")
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--eval-batch-size", type=int, default=2048)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out_root = root / "results" / "hlgnn_pdg_v0"
    script = root / "Planetoid" / "run_pdg_experiment.py"
    plan = []
    for dataset in ("cora", "citeseer"):
        mlp_layers = 3 if dataset == "cora" else 2
        for variant in ("B0", "B1", "B2", "B3"):
            for seed in (0, 1, 2):
                output = out_root / dataset / variant / f"seed{seed}.json"
                log = out_root / "logs" / f"{dataset}_{variant}_seed{seed}.log"
                plan.append((dataset, variant, seed, mlp_layers, output, log))
    for index, (dataset, variant, seed, mlp_layers, output, log) in enumerate(plan, 1):
        if output.exists() and not args.force:
            print(f"[{index}/{len(plan)}] SKIP {output}", flush=True)
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        log.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable, str(script), "--dataset", dataset, "--variant", variant,
            "--seed", str(seed), "--device", str(args.device), "--data-root", args.data_root,
            "--epochs", str(args.epochs), "--hidden-channels", "8192",
            "--mlp-num-layers", str(mlp_layers), "--dropout", "0.5",
            "--batch-size", str(args.batch_size), "--eval-batch-size", str(args.eval_batch_size),
            "--lr", "0.001", "--K", "20", "--alpha", "0.2", "--init", "RWR",
            "--output", str(output),
        ]
        print(f"[{index}/{len(plan)}] RUN {dataset} {variant} seed={seed}", flush=True)
        with log.open("w", encoding="utf-8") as handle:
            proc = subprocess.run(cmd, cwd=root, stdout=handle, stderr=subprocess.STDOUT)
        if proc.returncode != 0:
            raise SystemExit(f"run failed ({proc.returncode}): {dataset} {variant} seed={seed}; see {log}")
        print(f"[{index}/{len(plan)}] DONE {output}", flush=True)


if __name__ == "__main__":
    main()
