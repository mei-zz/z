from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from dcdlp.data.loaders import load_dataset
from dcdlp.evaluate import load_checkpoint_model
from dcdlp.train import edge_index_from_graph, evaluate_split


# These checkpoints are produced by the trusted local project.  PyTorch 2.6+
# changed torch.load's default to weights_only=True, while DCDLP checkpoints
# intentionally contain the train-only CN residualizer metadata object.
_torch_load = torch.load


def _trusted_load(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _torch_load(*args, **kwargs)


torch.load = _trusted_load


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    model, payload = load_checkpoint_model(args.checkpoint, "cuda:0")
    config = payload["config"]
    dataset = load_dataset(config["dataset"], args.data_root, config.get("protocol_eval", "standard"), config["seed"])
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda:0")
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda:0"))
    metrics, _ = evaluate_split(
        model, dataset, dataset.valid_pos, config["seed"] + 777,
        config["negatives_per_positive_eval"], x, edges, "official", dataset.valid_neg,
    )
    output = {"checkpoint": str(args.checkpoint), "seed": int(config["seed"]), "metrics": metrics}
    args.output.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
