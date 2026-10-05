from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from candidate_models import CrossDepthPairTensor, PairConditionedDynamicTransport
from dcdlp.data.loaders import load_dataset
from dcdlp.data.negative_sampling import uniform_negative_sampling
from dcdlp.data.pair_statistics import pair_features
from dcdlp.evaluation.ranking import ranking_metrics
from dcdlp.models.dcdlp import DCDLP
from dcdlp.models.losses import link_prediction_loss
from dcdlp.train import TrainConfig, edge_index_from_graph, evaluate_split, fit_training_cn_residualizer, score_pairs
from dcdlp.utils import seed_everything


def model_config(seed: int, epochs: int, output_dir: str) -> TrainConfig:
    return TrainConfig(
        dataset="cora",
        protocol_train="uniform",
        protocol_eval="heart",
        seed=seed,
        hidden_dim=64,
        branch_dim=32,
        num_layers=2,
        dropout=0.1,
        backbone="gcn",
        lr=1e-3,
        weight_decay=1e-4,
        batch_size=512,
        pretrain_epochs=epochs,
        disentangle_epochs=0,
        negatives_per_positive_eval=50,
        ablation="A5",
        cn_feature_mode="raw",
        cn_input_schema="selective_v1",
        interaction_mode="unrestricted",
        output_dir=output_dir,
    )


def build_models(input_dim: int, config: TrainConfig, device: torch.device, candidate_name: str):
    torch.manual_seed(config.seed)
    parent = DCDLP(
        input_dim, config.hidden_dim, config.branch_dim, config.num_layers,
        config.dropout, config.backbone, use_interaction=True,
        active_branches=("degree", "cn", "residual"),
        decoder_mode="additive", cn_feature_mode=config.cn_feature_mode,
        interaction_mode=config.interaction_mode,
        cn_input_schema=config.cn_input_schema,
    ).to(device)
    torch.manual_seed(config.seed)
    candidate_class = PairConditionedDynamicTransport if candidate_name == "V2-001_PCDT" else CrossDepthPairTensor
    candidate_kwargs = {"transport_rank": 8} if candidate_name == "V2-001_PCDT" else {}
    candidate = candidate_class(
        input_dim, config.hidden_dim, config.branch_dim, config.num_layers,
        config.dropout, config.backbone, use_interaction=True,
        active_branches=("degree", "cn", "residual"),
        decoder_mode="additive", cn_feature_mode=config.cn_feature_mode,
        interaction_mode=config.interaction_mode,
        cn_input_schema=config.cn_input_schema,
        **candidate_kwargs,
    ).to(device)
    candidate.load_state_dict(parent.state_dict(), strict=False)
    return parent, candidate


def train_one(model, dataset, config: TrainConfig, edge_index, x, regressor, device, shuffle_training: bool = False):
    model.cn_branch.set_cn_regressor(regressor)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)
    rng = np.random.default_rng(config.seed)
    best_state = None
    best_mrr = -float("inf")
    started = time.perf_counter()
    if shuffle_training and hasattr(model, "shuffle_transport"):
        model.shuffle_transport = True
    if shuffle_training and hasattr(model, "shuffle_cross"):
        model.shuffle_cross = True
    for epoch in range(config.pretrain_epochs):
        model.train()
        negative = uniform_negative_sampling(
            dataset.num_nodes, dataset.all_positive, len(dataset.train_pos), config.seed * 10000 + epoch
        )
        pairs_np = np.vstack([dataset.train_pos, negative])
        labels_np = np.concatenate([np.ones(len(dataset.train_pos)), np.zeros(len(negative))])
        order = rng.permutation(len(pairs_np))
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
        valid_metrics, _ = evaluate_split(
            model, dataset, dataset.valid_pos, config.seed + 777 + epoch,
            config.negatives_per_positive_eval, x, edge_index,
            negative_method="official", official_negatives=dataset.valid_neg,
        )
        if valid_metrics["mrr"] > best_mrr:
            best_mrr = valid_metrics["mrr"]
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
    if best_state is not None:
        model.load_state_dict(best_state)
    test_metrics, _ = evaluate_split(
        model, dataset, dataset.test_pos, config.seed + 999,
        config.negatives_per_positive_eval, x, edge_index,
        negative_method="official", official_negatives=dataset.test_neg,
    )
    return test_metrics, time.perf_counter() - started


def shuffled_control(model, dataset, config, edge_index, x):
    model.eval()
    if hasattr(model, "shuffle_transport"):
        model.shuffle_transport = True
    else:
        model.shuffle_cross = True
    try:
        metrics, _ = evaluate_split(
            model, dataset, dataset.test_pos, config.seed + 1999,
            config.negatives_per_positive_eval, x, edge_index,
            negative_method="official", official_negatives=dataset.test_neg,
        )
    finally:
        if hasattr(model, "shuffle_transport"):
            model.shuffle_transport = False
        else:
            model.shuffle_cross = False
    return metrics


def cn_proxy(dataset, seed: int):
    graph = dataset.train_graph()
    positives = np.asarray(dataset.test_pos, dtype=np.int64)
    negatives = np.asarray(dataset.test_neg, dtype=np.int64)
    flat = negatives.reshape(-1, 2)
    pos_cn = pair_features(graph, positives, dataset.features)["cn"].astype(float)
    neg_cn = pair_features(graph, flat, dataset.features)["cn"].astype(float).reshape(len(positives), -1)
    return ranking_metrics(pos_cn, neg_cn)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--output", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--candidate", choices=["V2-001_PCDT", "V2-002_CDPT"], default="V2-001_PCDT")
    parser.add_argument("--train-shuffled-control", action="store_true")
    args = parser.parse_args()
    seed_everything(args.seed)
    device = torch.device(args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    dataset = load_dataset("cora", Path(args.data_root), protocol="heart", seed=args.seed)
    graph = dataset.train_graph()
    edge_index = edge_index_from_graph(graph, device)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device=device)
    config = model_config(args.seed, args.epochs, str(Path(args.output).parent))
    regressor, regressor_metadata = fit_training_cn_residualizer(dataset, config)
    parent, candidate = build_models(x.shape[1], config, device, args.candidate)
    parent_metrics, parent_seconds = train_one(parent, dataset, config, edge_index, x, regressor, device)
    candidate_metrics, candidate_seconds = train_one(candidate, dataset, config, edge_index, x, regressor, device)
    shuffled_metrics = shuffled_control(candidate, dataset, config, edge_index, x)
    trained_shuffled_metrics = None
    trained_shuffled_seconds = None
    if args.train_shuffled_control:
        _, shuffled_model = build_models(x.shape[1], config, device, args.candidate)
        trained_shuffled_metrics, trained_shuffled_seconds = train_one(
            shuffled_model, dataset, config, edge_index, x, regressor, device,
            shuffle_training=True,
        )
    proxy_metrics = cn_proxy(dataset, args.seed)
    metric_names = ["mrr", "hits10", "hits20", "hits50", "hits100", "auc", "ap"]
    result = {
        "candidate": args.candidate,
        "dataset": "cora",
        "protocol": "heart",
        "seed": args.seed,
        "epochs": args.epochs,
        "device": str(device),
        "metrics": {"parent": {key: parent_metrics.get(key) for key in metric_names},
                    "candidate": {key: candidate_metrics.get(key) for key in metric_names},
                    "shuffled_transport": {key: shuffled_metrics.get(key) for key in metric_names},
                    "trained_shuffled_control": ({key: trained_shuffled_metrics.get(key) for key in metric_names}
                                                   if trained_shuffled_metrics is not None else None),
                    "cn_proxy": {key: proxy_metrics.get(key) for key in metric_names}},
        "delta_candidate_minus_parent": {key: float(candidate_metrics[key] - parent_metrics[key]) for key in metric_names},
        "runtime_seconds": {"parent": parent_seconds, "candidate": candidate_seconds,
                            "trained_shuffled_control": trained_shuffled_seconds},
        "parameter_count": {"parent": sum(value.numel() for value in parent.parameters()),
                             "candidate": sum(value.numel() for value in candidate.parameters())},
        "cn_regressor_metadata": regressor_metadata,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
