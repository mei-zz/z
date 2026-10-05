"""Protocol-preserving DCDLP Parent runner for LPShift.

This runner is intentionally conservative: the model is the existing DCDLP
Parent, not a new architecture. It keeps the official directed message graph
and uses a cached unmasked encoding for held-out candidates, which is
semantically exact because the adapter has verified that all held-out
candidates are absent from the message graph.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as ssp
import torch
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcdlp.data.negative_sampling import uniform_negative_sampling
from dcdlp.evaluation.ranking import ranking_metrics
from dcdlp.models.dcdlp import DCDLP
from dcdlp.models.losses import link_prediction_loss
from dcdlp.utils import seed_everything
from lpshift_adapter import LPShiftData, sha256_array


def tensor_hash(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode())
        digest.update(str(value.dtype).encode())
        digest.update(json.dumps(list(value.shape)).encode())
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def build_neighbors(edge_index: torch.Tensor, num_nodes: int) -> list[set[int]]:
    neighbors = [set() for _ in range(num_nodes)]
    for raw_u, raw_v in edge_index.detach().cpu().t().tolist():
        u, v = int(raw_u), int(raw_v)
        if u == v:
            continue
        neighbors[u].add(v)
        neighbors[v].add(u)
    return neighbors


def degrees_from_neighbors(neighbors: list[set[int]], device: torch.device) -> torch.Tensor:
    return torch.as_tensor([len(values) for values in neighbors], dtype=torch.float32, device=device)


def target_mask_keys(pairs: torch.Tensor, message_keys: set[tuple[int, int]]) -> set[tuple[int, int]]:
    output = set()
    for raw_u, raw_v in pairs.detach().cpu().tolist():
        u, v = int(raw_u), int(raw_v)
        key = (min(u, v), max(u, v))
        if key in message_keys:
            output.add(key)
    return output


def degrees_after_mask(base_neighbors: list[set[int]], removed_keys: set[tuple[int, int]], device: torch.device) -> torch.Tensor:
    values = np.asarray([len(item) for item in base_neighbors], dtype=np.float32)
    for u, v in removed_keys:
        values[u] -= 1.0
        values[v] -= 1.0
    return torch.as_tensor(values, dtype=torch.float32, device=device)


def masked_adjacency(base_adj: ssp.csr_matrix, removed_keys: set[tuple[int, int]]) -> ssp.csr_matrix:
    if not removed_keys:
        return base_adj
    rows = []
    cols = []
    for u, v in removed_keys:
        rows.extend([u, v])
        cols.extend([v, u])
    removal = ssp.csr_matrix(
        (np.ones(len(rows), dtype=np.float32), (np.asarray(rows), np.asarray(cols))),
        shape=base_adj.shape,
    )
    output = base_adj - removal
    output.eliminate_zeros()
    output.data[:] = 1.0
    return output


def decode(model: DCDLP, h: torch.Tensor, pairs: torch.Tensor,
           base_neighbors: list[set[int]], degrees: torch.Tensor,
           adjacency: ssp.csr_matrix,
           removed_keys: set[tuple[int, int]] | None = None) -> dict[str, torch.Tensor]:
    """Decode with the exact DCDLP raw-CN semantics without copying all sets.

    The old implementation copied every node's neighbor set on each batch.
    Here the immutable message-graph sets are reused and only common-neighbor
    entries incident to a currently masked target edge are filtered.
    """
    removed_keys = removed_keys or set()
    z_degree, score_degree = model.degree_branch(degrees, pairs)
    node_messages = model.cn_branch.node_mlp(h)
    pairs_np = pairs.detach().cpu().numpy().astype(np.int64, copy=False)
    common_rows = adjacency[pairs_np[:, 0]].multiply(adjacency[pairs_np[:, 1]]).tocsr()
    raw_counts_np = np.diff(common_rows.indptr).astype(np.float32, copy=False)
    raw_cn = h.new_tensor(raw_counts_np)
    pooled_sum = h.new_zeros((len(pairs_np), node_messages.shape[1]))
    pooled_max = h.new_full((len(pairs_np), node_messages.shape[1]), float("-inf"))
    if common_rows.nnz:
        row_ids = np.repeat(np.arange(len(pairs_np), dtype=np.int64), np.diff(common_rows.indptr))
        row_tensor = torch.as_tensor(row_ids, dtype=torch.long, device=h.device)
        col_tensor = torch.as_tensor(common_rows.indices, dtype=torch.long, device=h.device)
        common_messages = node_messages[col_tensor]
        pooled_sum.index_add_(0, row_tensor, common_messages)
        pooled_max = torch.scatter_reduce(
            pooled_max, 0,
            row_tensor[:, None].expand(-1, common_messages.shape[1]),
            common_messages, reduce="amax", include_self=True,
        )
    pooled_sum = pooled_sum / torch.sqrt(raw_cn[:, None] + 1.0)
    empty = raw_counts_np == 0
    if np.any(empty):
        empty_mask = torch.as_tensor(empty, dtype=torch.bool, device=h.device)[:, None]
        pooled_max = torch.where(empty_mask, model.cn_branch.empty_token[None, :], pooled_max)
    raw_log_cn = torch.log1p(raw_cn)
    degree_array = degrees.detach()[pairs[:, [0, 1]]].cpu().numpy().astype(float, copy=False)
    degree_product = h.new_tensor(degree_array[:, 0] * degree_array[:, 1])
    normalized = raw_cn / degree_product.clamp_min(1.0).sqrt()
    zeros = torch.zeros_like(raw_log_cn)
    explicit = torch.stack([raw_log_cn, zeros], dim=-1)
    rows = torch.cat([pooled_sum, pooled_max, explicit], dim=-1)
    z_cn = model.cn_branch.encoder(rows)
    score_cn = model.cn_branch.scorer(z_cn).squeeze(-1)
    cn_statistics = {
        "cn_raw": raw_cn,
        "cn_log_raw": raw_log_cn,
        "cn_expected": torch.full_like(raw_log_cn, float("nan")),
        "cn_residual_feature": torch.full_like(raw_log_cn, float("nan")),
        "cn_normalized": normalized,
    }
    z_residual, score_residual = model.residual_branch(h, pairs)
    if "degree" not in model.active_branches:
        z_degree, score_degree = torch.zeros_like(z_degree), torch.zeros_like(score_degree)
    if "cn" not in model.active_branches:
        z_cn, score_cn = torch.zeros_like(z_cn), torch.zeros_like(score_cn)
    if "residual" not in model.active_branches:
        z_residual, score_residual = torch.zeros_like(z_residual), torch.zeros_like(score_residual)
    projected = z_degree @ model.interaction
    raw_interaction = model.interaction_scale * (projected * z_cn).sum(-1) / z_cn.shape[-1] ** 0.5
    score_interaction = (
        torch.zeros_like(raw_interaction)
        if model.interaction_mode == "disabled" else raw_interaction
    )
    if model.decoder_mode == "concat":
        logit = model.concat_decoder(torch.cat([z_degree, z_cn, z_residual], dim=-1)).squeeze(-1) + model.bias
    else:
        logit = score_degree + score_cn + score_residual + score_interaction + model.bias
    denominator = score_degree.abs() + score_cn.abs() + score_residual.abs() + score_interaction.abs()
    share = score_interaction.abs() / (denominator + 1e-8)
    return {
        "logit": logit,
        "score_degree": score_degree,
        "score_cn": score_cn,
        "score_residual": score_residual,
        "score_interaction": score_interaction,
        "interaction_share": share,
        **cn_statistics,
    }


def uniform_negatives_without_heldout_labels(adapter: LPShiftData, count: int, seed: int) -> np.ndarray:
    """Sample train negatives while reading only the message graph.

    This intentionally does not use adapter.valid_pos, adapter.test_pos,
    valid_neg or test_neg. It therefore differs from the historical DCDLP
    helper, which used all_positive and implicitly read held-out labels.
    """
    message_pairs = adapter.message_edge_index.detach().cpu().numpy().T
    forbidden = np.asarray(sorted(adapter.message_edge_keys()), dtype=np.int64)
    return uniform_negative_sampling(adapter.num_nodes, forbidden, count, seed)


def train_batch(model, x, edge_index, base_neighbors, message_keys, base_adj, pairs, labels, optimizer, device):
    masked_edge_index = LPShiftData.mask_target_edges(edge_index, pairs)
    removed_keys = target_mask_keys(pairs, message_keys)
    degrees = degrees_after_mask(base_neighbors, removed_keys, device)
    h = model.node_encoder(x, masked_edge_index)
    outputs = decode(model, h, pairs, base_neighbors, degrees, masked_adjacency(base_adj, removed_keys), removed_keys)
    loss = link_prediction_loss(outputs["logit"], labels)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
    return float(loss.detach().cpu())


@torch.no_grad()
def score_with_cached_encoding(model, h, pairs_np, base_neighbors, degrees, base_adj, device, chunk_size):
    scores = []
    for start in range(0, len(pairs_np), chunk_size):
        pairs = torch.as_tensor(pairs_np[start:start + chunk_size], dtype=torch.long, device=device)
        scores.append(decode(model, h, pairs, base_neighbors, degrees, base_adj)["logit"].detach().cpu().numpy())
    return np.concatenate(scores, axis=0) if scores else np.empty(0, dtype=np.float32)


@torch.no_grad()
def evaluate(model, adapter, x, edge_index, base_neighbors, base_adj, device, batch_size, return_scores=False):
    model.eval()
    h = model.node_encoder(x, edge_index)
    degrees = degrees_from_neighbors(base_neighbors, device)
    valid_pos = adapter.valid_pos.detach().cpu().numpy().astype(np.int64)
    valid_neg = adapter.valid_neg.detach().cpu().numpy().astype(np.int64)
    test_pos = adapter.test_pos.detach().cpu().numpy().astype(np.int64)
    test_neg = adapter.test_neg.detach().cpu().numpy().astype(np.int64)
    def one(pos, neg):
        pos_score = score_with_cached_encoding(model, h, pos, base_neighbors, degrees, base_adj, device, batch_size)
        neg_score = score_with_cached_encoding(model, h, neg.reshape(-1, 2), base_neighbors, degrees, base_adj, device, batch_size)
        neg_score = neg_score.reshape(len(pos), neg.shape[1])
        metrics = ranking_metrics(pos_score, neg_score, ks=(10, 20, 50, 100))
        labels = np.concatenate([np.ones(len(pos)), np.zeros(len(neg_score.reshape(-1)))])
        values = np.concatenate([pos_score, neg_score.reshape(-1)])
        metrics["auc"] = float(roc_auc_score(labels, values))
        metrics["ap"] = float(average_precision_score(labels, values))
        if return_scores:
            return metrics, {"pos": pos_score, "neg": neg_score}
        return metrics
    valid = one(valid_pos, valid_neg)
    test = one(test_pos, test_neg)
    if return_scores:
        return valid[0], test[0], {
            "valid_pos": valid[1]["pos"], "valid_neg": valid[1]["neg"],
            "test_pos": test[1]["pos"], "test_neg": test[1]["neg"],
        }
    return valid, test


def make_model(input_dim: int, seed: int, device: torch.device) -> DCDLP:
    seed_everything(seed)
    model = DCDLP(
        input_dim, hidden_dim=64, branch_dim=32, num_layers=2, dropout=0.1,
        backbone="gcn", use_interaction=True,
        active_branches=("degree", "cn", "residual"), decoder_mode="additive",
        cn_feature_mode="raw", cn_regressor=None,
        interaction_mode="unrestricted", cn_input_schema="selective_v1",
    )
    return model.to(device)


def run(args):
    seed_everything(args.seed)
    device = torch.device(args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    adapter = LPShiftData.load(args.repo, args.dataset)
    x = adapter.features.to(device=device, dtype=torch.float32)
    # Keep the exact official tensor in the adapter, but pass the equivalent
    # one-orientation view to DCDLP's unchanged GCNLayer, which adds reverses.
    edge_index = adapter.dcdlp_edge_index.to(device=device, dtype=torch.long)
    base_neighbors = adapter.message_neighbors()
    message_keys = adapter.message_edge_keys()
    edge_cpu = adapter.message_edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
    base_adj = ssp.csr_matrix((np.ones(edge_cpu.shape[1], dtype=np.float32),
                               (edge_cpu[0], edge_cpu[1])), shape=(adapter.num_nodes, adapter.num_nodes))
    base_adj.sum_duplicates()
    base_adj.data[:] = 1.0
    model = make_model(x.shape[1], args.seed, device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    config = {
        "hidden_dim": 64, "branch_dim": 32, "num_layers": 2, "dropout": 0.1,
        "backbone": "gcn", "lr": 1e-3, "weight_decay": 1e-4,
        "batch_size": args.batch_size, "epochs": args.epochs,
        "train_negative_protocol": "uniform_non_message_edges",
        "target_masking": True, "selection_metric": "validation_mrr",
        "test_used_for_selection": False,
    }
    if args.smoke:
        train_pos = adapter.train_pos[: args.smoke_pairs].detach().cpu().numpy().astype(np.int64)
        train_neg = uniform_negatives_without_heldout_labels(adapter, len(train_pos), args.seed * 10000)
        pairs_np = np.vstack([train_pos, train_neg])
        labels_np = np.concatenate([np.ones(len(train_pos)), np.zeros(len(train_neg))]).astype(np.float32)
        pairs = torch.as_tensor(pairs_np, dtype=torch.long, device=device)
        labels = torch.as_tensor(labels_np, dtype=torch.float32, device=device)
        started = time.perf_counter()
        loss = train_batch(model, x, edge_index, base_neighbors, message_keys, base_adj, pairs, labels, optimizer, device)
        train_seconds = time.perf_counter() - started
        model.eval()
        with torch.no_grad():
            masked_edge = LPShiftData.mask_target_edges(edge_index, torch.as_tensor(adapter.valid_pos[:args.smoke_pairs], device=device))
            h = model.node_encoder(x, masked_edge)
            valid_degrees = degrees_after_mask(base_neighbors, set(), device)
            valid_pairs = torch.as_tensor(adapter.valid_pos[:args.smoke_pairs], device=device)
            valid_out = decode(model, h, valid_pairs, base_neighbors, valid_degrees, base_adj)
        result = {"mode": "smoke", "dataset": args.dataset, "seed": args.seed,
                  "loss": loss, "train_seconds": train_seconds,
                  "valid_batch_shape": list(valid_out["logit"].shape),
                  "peak_gpu_memory_mb": float(torch.cuda.max_memory_allocated(device) / 2**20) if device.type == "cuda" else None,
                  "adapter_summary": adapter.summary()}
        print(json.dumps(result, indent=2))
        return result

    train_pos = adapter.train_pos.detach().cpu().numpy().astype(np.int64)
    best_state = None
    best_valid = -float("inf")
    best_epoch = -1
    trace = []
    started = time.perf_counter()
    for epoch in range(args.epochs):
        model.train()
        train_neg = uniform_negatives_without_heldout_labels(adapter, len(train_pos), args.seed * 10000 + epoch)
        pairs_np = np.vstack([train_pos, train_neg])
        labels_np = np.concatenate([np.ones(len(train_pos)), np.zeros(len(train_neg))]).astype(np.float32)
        order = np.random.default_rng(args.seed * 1000 + epoch).permutation(len(pairs_np))
        losses = []
        for start in range(0, len(order), args.batch_size):
            selected = order[start:start + args.batch_size]
            pairs = torch.as_tensor(pairs_np[selected], dtype=torch.long, device=device)
            labels = torch.as_tensor(labels_np[selected], dtype=torch.float32, device=device)
            losses.append(train_batch(model, x, edge_index, base_neighbors, message_keys, base_adj, pairs, labels, optimizer, device))
        valid_metrics, test_metrics = evaluate(model, adapter, x, edge_index, base_neighbors, base_adj, device, args.eval_batch_size)
        row = {"epoch": epoch, "mean_loss": float(np.mean(losses)), "validation": valid_metrics,
               "test_descriptive": test_metrics, "negative_hash": sha256_array(train_neg),
               "order_hash": sha256_array(order)}
        trace.append(row)
        if valid_metrics["mrr"] > best_valid:
            best_valid = valid_metrics["mrr"]
            best_epoch = epoch
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
    if best_state is None:
        raise RuntimeError("No checkpoint was selected")
    model.load_state_dict(best_state)
    if args.save_predictions:
        valid_metrics, test_metrics, predictions = evaluate(
            model, adapter, x, edge_index, base_neighbors, base_adj, device,
            args.eval_batch_size, return_scores=True,
        )
    else:
        valid_metrics, test_metrics = evaluate(model, adapter, x, edge_index, base_neighbors, base_adj, device, args.eval_batch_size)
    checkpoint_path = Path(args.checkpoint) if args.checkpoint else Path(args.output).with_suffix(".pt")
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "model": model.state_dict(),
        "config": config,
        "dataset": args.dataset,
        "seed": args.seed,
        "best_epoch": best_epoch,
        "validation": valid_metrics,
        "test": test_metrics,
        "test_used_for_selection": False,
        "adapter_summary": adapter.summary(),
    }, checkpoint_path)
    result = {
        "mode": "formal", "dataset": args.dataset, "seed": args.seed,
        "config": config, "adapter_summary": adapter.summary(),
        "best_epoch": best_epoch, "validation": valid_metrics, "test": test_metrics,
        "trace": trace, "runtime_seconds": time.perf_counter() - started,
        "peak_gpu_memory_mb": float(torch.cuda.max_memory_allocated(device) / 2**20) if device.type == "cuda" else None,
        "parameter_count": int(sum(value.numel() for value in model.parameters())),
        "best_state_hash": tensor_hash(model.state_dict()),
        "gpu_name": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        "test_used_for_selection": False,
        "checkpoint": str(checkpoint_path),
    }
    if args.save_predictions:
        prediction_path = str(Path(args.output).with_suffix(".pred.npz"))
        np.savez_compressed(prediction_path, **predictions)
        result["prediction_file"] = prediction_path
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=65536)
    parser.add_argument("--eval-batch-size", type=int, default=65536)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--smoke-pairs", type=int, default=512)
    parser.add_argument("--save-predictions", action="store_true")
    parser.add_argument("--checkpoint", default=None)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
