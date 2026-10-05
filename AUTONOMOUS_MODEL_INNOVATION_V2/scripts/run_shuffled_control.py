from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcdlp.data.loaders import load_dataset
from dcdlp.train import edge_index_from_graph, fit_training_cn_residualizer
from dcdlp.utils import seed_everything
from run_candidate import build_models, model_config, train_one


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--candidate", choices=["V2-001_PCDT", "V2-002_CDPT"], default="V2-002_CDPT")
    args = parser.parse_args()
    seed_everything(args.seed)
    device = torch.device(args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    dataset = load_dataset("cora", Path(args.data_root), protocol="heart", seed=args.seed)
    edge_index = edge_index_from_graph(dataset.train_graph(), device)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device=device)
    config = model_config(args.seed, args.epochs, str(Path(args.output).parent))
    regressor, metadata = fit_training_cn_residualizer(dataset, config)
    _, model = build_models(x.shape[1], config, device, args.candidate)
    metrics, seconds = train_one(
        model, dataset, config, edge_index, x, regressor, device,
        shuffle_training=True,
    )
    result = {
        "candidate": args.candidate,
        "control": "trained_shuffled_structural_path",
        "seed": args.seed,
        "epochs": args.epochs,
        "metrics": metrics,
        "runtime_seconds": seconds,
        "parameter_count": sum(value.numel() for value in model.parameters()),
        "cn_regressor_metadata": metadata,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
