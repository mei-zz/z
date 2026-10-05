from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcdlp.data.loaders import load_dataset
from dcdlp.data.negative_sampling import uniform_negative_sampling
from dcdlp.data.pair_statistics import pair_features
from dcdlp.evaluation.ranking import ranking_metrics
from dcdlp.models.dcdlp import DCDLP
from dcdlp.models.losses import link_prediction_loss
from dcdlp.train import TrainConfig, edge_index_from_graph, evaluate_split, fit_training_cn_residualizer, score_pairs
from dcdlp.utils import array_hash, seed_everything, stable_hash
from v4_models import MODEL_CLASSES


MODEL_IDS = ["A_EarlyEarly", "B_LateLate", "C_CDPT", "D_ConcatMLP", "E_FixedRandom"]


def make_config(dataset: str, seed: int, epochs: int, output_dir: str) -> TrainConfig:
    return TrainConfig(
        dataset=dataset, protocol_train="uniform", protocol_eval="heart", seed=seed,
        hidden_dim=64, branch_dim=32, num_layers=2, dropout=0.1, backbone="gcn",
        lr=1e-3, weight_decay=1e-4, batch_size=512, pretrain_epochs=epochs,
        disentangle_epochs=0, negatives_per_positive_eval=50, ablation="A5",
        cn_feature_mode="raw", cn_input_schema="selective_v1", interaction_mode="unrestricted",
        output_dir=output_dir,
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def code_hashes() -> dict[str, str]:
    paths = [
        ROOT / "src" / "dcdlp" / "models" / "dcdlp.py",
        ROOT / "src" / "dcdlp" / "models" / "node_encoder.py",
        ROOT / "src" / "dcdlp" / "train.py",
        ROOT / "AUTONOMOUS_MODEL_INNOVATION_V4" / "scripts" / "v4_models.py",
        ROOT / "AUTONOMOUS_MODEL_INNOVATION_V4" / "scripts" / "v4_runner.py",
    ]
    return {str(path.relative_to(ROOT)): sha256_file(path) for path in paths}


def tensor_state_hash(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(json.dumps(list(value.shape)).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def rng_hashes() -> dict[str, str | None]:
    output = {"torch_cpu": hashlib.sha256(torch.get_rng_state().cpu().numpy().tobytes()).hexdigest()}
    if torch.cuda.is_available():
        output["torch_cuda"] = hashlib.sha256(torch.cuda.get_rng_state().cpu().numpy().tobytes()).hexdigest()
    else:
        output["torch_cuda"] = None
    return output


def instantiate(model_id: str, input_dim: int, config: TrainConfig, parent_state, device):
    common = dict(
        hidden_dim=config.hidden_dim, branch_dim=config.branch_dim, num_layers=config.num_layers,
        dropout=config.dropout, backbone=config.backbone, use_interaction=True,
        active_branches=("degree", "cn", "residual"), decoder_mode="additive",
        cn_feature_mode=config.cn_feature_mode, interaction_mode=config.interaction_mode,
        cn_input_schema=config.cn_input_schema,
    )
    model = MODEL_CLASSES[model_id](input_dim, **common)
    model.load_state_dict(parent_state, strict=False)
    return model.to(device)


def train_one(model, dataset, config, edge_index, x, regressor, device):
    seed_everything(config.seed)
    model.cn_branch.set_cn_regressor(regressor)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    rng = np.random.default_rng(config.seed)
    trace = []
    best_state = None
    best_validation_mrr = -float("inf")
    best_epoch = -1
    started = time.perf_counter()
    for epoch in range(config.pretrain_epochs):
        model.train()
        negative = uniform_negative_sampling(
            dataset.num_nodes, dataset.all_positive, len(dataset.train_pos), config.seed * 10000 + epoch,
        )
        pairs_np = np.vstack([dataset.train_pos, negative])
        labels_np = np.concatenate([np.ones(len(dataset.train_pos)), np.zeros(len(negative))])
        order = rng.permutation(len(pairs_np))
        trace.append({
            "epoch": epoch,
            "negative_hash": array_hash(negative),
            "order_hash": array_hash(order),
            "negative_seed": config.seed * 10000 + epoch,
        })
        for start in range(0, len(order), config.batch_size):
            selected = order[start:start + config.batch_size]
            pairs = torch.as_tensor(pairs_np[selected], dtype=torch.long, device=device)
            labels = torch.as_tensor(labels_np[selected], dtype=torch.float32, device=device)
            optimizer.zero_grad(set_to_none=True)
            outputs = model(x, edge_index, pairs, remove_target_edges=True)
            loss = link_prediction_loss(outputs["logit"], labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
        validation_metrics, _ = evaluate_split(
            model, dataset, dataset.valid_pos, config.seed + 777 + epoch,
            config.negatives_per_positive_eval, x, edge_index,
            negative_method="official", official_negatives=dataset.valid_neg,
        )
        trace[-1]["validation_mrr"] = float(validation_metrics["mrr"])
        if validation_metrics["mrr"] > best_validation_mrr:
            best_validation_mrr = validation_metrics["mrr"]
            best_epoch = epoch
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    validation_best, _ = evaluate_split(
        model, dataset, dataset.valid_pos, config.seed + 1777,
        config.negatives_per_positive_eval, x, edge_index,
        negative_method="official", official_negatives=dataset.valid_neg,
    )
    test_metrics, _ = evaluate_split(
        model, dataset, dataset.test_pos, config.seed + 999,
        config.negatives_per_positive_eval, x, edge_index,
        negative_method="official", official_negatives=dataset.test_neg,
    )
    peak_gpu_mb = None
    if device.type == "cuda":
        peak_gpu_mb = float(torch.cuda.max_memory_allocated(device) / (1024 ** 2))
    return validation_best, test_metrics, best_epoch, time.perf_counter() - started, peak_gpu_mb, trace, tensor_state_hash(model.state_dict())


def simple_cn_proxy(dataset):
    graph = dataset.train_graph()
    positives = np.asarray(dataset.test_pos, dtype=np.int64)
    negatives = np.asarray(dataset.test_neg, dtype=np.int64)
    flat = negatives.reshape(-1, 2)
    pos_cn = pair_features(graph, positives, dataset.features)["cn"].astype(float)
    neg_cn = pair_features(graph, flat, dataset.features)["cn"].astype(float).reshape(len(positives), -1)
    return ranking_metrics(pos_cn, neg_cn)


def summarize_score_path(model, dataset, edge_index, x):
    output = score_pairs(model, x, edge_index, np.asarray(dataset.test_pos, dtype=np.int64))
    values = np.asarray(output["score_cross_depth"], dtype=float)
    return {
        "mean_abs": float(np.mean(np.abs(values))),
        "std": float(np.std(values)),
        "max_abs": float(np.max(np.abs(values))) if len(values) else 0.0,
        "nonzero_fraction": float(np.mean(np.abs(values) > 1e-8)) if len(values) else 0.0,
        "depth_scale": float(model.depth_scale.detach().cpu()),
        "operator_norm": float(model.depth_operator.detach().norm().cpu()) if hasattr(model, "depth_operator") else 0.0,
        "operator_trainable": bool(hasattr(model, "depth_operator") and model.depth_operator.requires_grad),
    }


def run_model(model_id, dataset, config, edge_index, x, regressor, parent_state, device, hashes):
    seed_everything(config.seed)
    model = instantiate(model_id, x.shape[1], config, parent_state, device)
    init_hash = tensor_state_hash(model.state_dict())
    init_rng = rng_hashes()
    validation_metrics, test_metrics, best_epoch, seconds, peak_gpu_mb, trace, best_hash = train_one(
        model, dataset, config, edge_index, x, regressor, device,
    )
    data_hash = stable_hash({
        "train": array_hash(dataset.train_pos), "valid": array_hash(dataset.valid_pos),
        "test": array_hash(dataset.test_pos), "valid_neg": array_hash(np.asarray(dataset.valid_neg)),
        "test_neg": array_hash(np.asarray(dataset.test_neg)),
    })
    return model, {
        "model_id": model_id, "dataset": dataset.name, "seed": config.seed,
        "config": asdict(config), "config_hash": stable_hash(asdict(config) | {"model_id": model_id}),
        "code_hashes": hashes, "data_hash": data_hash, "init_state_hash": init_hash,
        "init_rng_hashes": init_rng, "final_rng_hashes": rng_hashes(),
        "training_trace": trace, "best_state_hash": best_hash, "best_epoch": best_epoch,
        "test_used_for_selection": False, "selection_metric": "validation_mrr",
        "metrics": {"validation_best": validation_metrics, "test_report": test_metrics},
        "score_path": summarize_score_path(model, dataset, edge_index, x),
        "parameter_count": {
            "total": int(sum(value.numel() for value in model.parameters())),
            "trainable": int(sum(value.numel() for value in model.parameters() if value.requires_grad)),
        },
        "runtime_seconds": seconds, "peak_gpu_memory_mb": peak_gpu_mb,
        "gpu_name": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        "deterministic_algorithms": bool(torch.are_deterministic_algorithms_enabled()),
        "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--dataset", choices=["cora", "citeseer", "pubmed"], default="cora")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--models", default=",".join(MODEL_IDS))
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--strict-determinism", action="store_true")
    args = parser.parse_args()
    if args.strict_determinism:
        torch.use_deterministic_algorithms(True)
    seed_everything(args.seed)
    device = torch.device(args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    dataset = load_dataset(args.dataset, Path(args.data_root), protocol="heart", seed=args.seed)
    graph = dataset.train_graph()
    edge_index = edge_index_from_graph(graph, device)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device=device)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    config = make_config(args.dataset, args.seed, args.epochs, str(output_dir))
    regressor, regressor_metadata = fit_training_cn_residualizer(dataset, config)
    seed_everything(args.seed)
    parent_template = DCDLP(
        x.shape[1], config.hidden_dim, config.branch_dim, config.num_layers,
        config.dropout, config.backbone, use_interaction=True,
        active_branches=("degree", "cn", "residual"), decoder_mode="additive",
        cn_feature_mode=config.cn_feature_mode, interaction_mode=config.interaction_mode,
        cn_input_schema=config.cn_input_schema,
    )
    parent_state = {key: value.detach().clone() for key, value in parent_template.state_dict().items()}
    hashes = code_hashes()
    proxy = simple_cn_proxy(dataset)
    results = []
    selected_models = [item.strip() for item in args.models.split(",") if item.strip()]
    for model_id in selected_models:
        if model_id not in MODEL_IDS:
            raise ValueError(f"Unknown model id: {model_id}")
        model, result = run_model(model_id, dataset, config, edge_index, x, regressor, parent_state, device, hashes)
        result["cn_regressor_metadata"] = regressor_metadata
        result["controls"] = {"simple_cn_proxy_test": proxy}
        checkpoint = output_dir / f"{args.dataset}_seed{args.seed}_{model_id}.pt"
        torch.save({"model": model.state_dict(), "config": asdict(config), "model_id": model_id,
                    "code_hashes": hashes, "data_hash": result["data_hash"]}, checkpoint)
        result["checkpoint"] = str(checkpoint)
        output = output_dir / f"{args.dataset}_seed{args.seed}_{model_id}.json"
        output.write_text(json.dumps(result, indent=2), encoding="utf-8")
        results.append(result)
    manifest = output_dir / f"{args.dataset}_seed{args.seed}_manifest.json"
    manifest.write_text(json.dumps({
        "dataset": args.dataset, "seed": args.seed, "epochs": args.epochs,
        "models": [item["model_id"] for item in results], "test_used_for_selection": False,
        "data_hash": results[0]["data_hash"] if results else None,
        "deterministic_algorithms": bool(torch.are_deterministic_algorithms_enabled()),
    }, indent=2), encoding="utf-8")
    print(json.dumps({"dataset": args.dataset, "seed": args.seed, "results": results}, indent=2))


if __name__ == "__main__":
    main()
