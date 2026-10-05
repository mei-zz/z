"""Paired HL-GNN-PDG V0 screening on the official Planetoid protocol.

The parent propagation code is kept in model.py. This runner adds only:
  B1: profile direct control;
  B2: residual pair-dependent hop gate;
  B3: the same gate with profiles shuffled within each label pool.
"""

import argparse
import copy
import json
import os
import random
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import scipy.sparse as sp
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torch_geometric.transforms as T
from torch_geometric.datasets import Planetoid
from torch_geometric.io import read_planetoid_data
from torch_geometric.data import Data as PyGData
from ogb.linkproppred import Evaluator

from model import HLGNN, LinkPredictor
from utils import do_edge_split


PROFILE_DIM = 4
PROFILE_NAMES = ["log1p_cn", "log1p_degree_sum", "abs_log_degree_gap", "feature_cosine"]


class OfflinePlanetoid(Planetoid):
    """Use the already provisioned official raw files without network access."""

    def download(self):
        return None


class RawPlanetoid:
    """Minimal dataset wrapper around PyG's official raw-file parser."""

    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        if index != 0:
            raise IndexError(index)
        return self.data


def load_raw_planetoid(data_root: str, dataset_name: str) -> RawPlanetoid:
    raw_dir = Path(data_root).expanduser() / dataset_name / "raw"
    if not raw_dir.exists():
        raise FileNotFoundError(f"Planetoid raw directory does not exist: {raw_dir}")
    return RawPlanetoid(read_planetoid_data(str(raw_dir), dataset_name))


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def make_train_adjacency(edge: torch.Tensor, num_nodes: int) -> Tuple[sp.csr_matrix, np.ndarray]:
    edge_np = edge.detach().cpu().numpy().astype(np.int64, copy=False)
    row, col = edge_np[:, 0], edge_np[:, 1]
    values = np.ones(row.shape[0], dtype=np.float32)
    adj = sp.csr_matrix((values, (row, col)), shape=(num_nodes, num_nodes))
    adj = adj.maximum(adj.T).tocsr()
    adj.setdiag(0)
    adj.eliminate_zeros()
    adj.data[:] = 1.0
    degree = np.asarray(adj.sum(axis=1)).reshape(-1).astype(np.float32)
    return adj, degree


def pair_profile(
    edge: torch.Tensor,
    adj: sp.csr_matrix,
    degree: np.ndarray,
    features: np.ndarray,
) -> np.ndarray:
    """Compute the four V0 features using only the train adjacency."""
    edge_np = edge.detach().cpu().numpy().astype(np.int64, copy=False)
    src, dst = edge_np[:, 0], edge_np[:, 1]
    cn = np.asarray(adj[src].multiply(adj[dst]).sum(axis=1)).reshape(-1)
    dsrc, ddst = degree[src], degree[dst]
    denom = np.linalg.norm(features[src], axis=1) * np.linalg.norm(features[dst], axis=1)
    dot = np.einsum("ij,ij->i", features[src], features[dst])
    cosine = np.divide(dot, denom, out=np.zeros_like(dot, dtype=np.float32), where=denom > 0)
    return np.column_stack(
        [
            np.log1p(cn),
            np.log1p(dsrc + ddst),
            np.abs(np.log1p(dsrc) - np.log1p(ddst)),
            cosine,
        ]
    ).astype(np.float32, copy=False)


def shuffle_rows(profile: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    return profile[rng.permutation(profile.shape[0])].copy()


class ProfileDirectPredictor(nn.Module):
    """Original LinkPredictor MLP with the four profile values appended."""

    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int, num_layers: int, dropout: float):
        super().__init__()
        self.lins = nn.ModuleList()
        self.lins.append(nn.Linear(in_channels + PROFILE_DIM, hidden_channels))
        for _ in range(num_layers - 2):
            self.lins.append(nn.Linear(hidden_channels, hidden_channels))
        self.lins.append(nn.Linear(hidden_channels, out_channels))
        self.dropout = dropout

    def reset_parameters(self) -> None:
        for lin in self.lins:
            lin.reset_parameters()

    def forward(self, x_i: torch.Tensor, x_j: torch.Tensor, profile: torch.Tensor) -> torch.Tensor:
        x = torch.cat([x_i * x_j, profile], dim=-1)
        for lin in self.lins[:-1]:
            x = lin(x)
            x = F.relu(x)
            x = F.dropout(x, p=self.dropout, training=self.training)
        return torch.sigmoid(self.lins[-1](x))


class HLGNNPDG(HLGNN):
    """HL-GNN with a residual, zero-at-initialization pair hop gate."""

    def __init__(self, data, args, gate_hidden: int = 32):
        super().__init__(data, args)
        self.gate = nn.Sequential(
            nn.Linear(PROFILE_DIM, gate_hidden),
            nn.Tanh(),
            nn.Linear(gate_hidden, self.K + 1),
        )
        nn.init.zeros_(self.gate[-1].weight)
        nn.init.zeros_(self.gate[-1].bias)
        self.gate_scale = nn.Parameter(torch.zeros(()))

    def pair_weights(self, profile: torch.Tensor) -> torch.Tensor:
        delta = torch.tanh(self.gate(profile))
        # The official source constructs temp from a NumPy array (float64),
        # while node features are float32. Match the endpoint representation
        # dtype before broadcasting a batch-shaped weight matrix.
        base = self.temp.to(dtype=profile.dtype)
        c = torch.mean(torch.abs(base))
        return base.unsqueeze(0) + c * torch.tanh(self.gate_scale).to(profile.dtype) * delta

    def forward_hops(self, x: torch.Tensor, adj_t, edge_weight) -> List[torch.Tensor]:
        """Materialize hops only for evaluation; training uses forward_pair."""
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.lin1(x)
        adj_t = self._normalized_adj(adj_t, edge_weight)
        hops = [x]
        for _ in range(self.K):
            x = self.propagate(adj_t, x=x, edge_weight=edge_weight, size=None)
            hops.append(x)
        return hops

    @staticmethod
    def _normalized_adj(adj_t, edge_weight):
        from torch_geometric.nn.conv.gcn_conv import gcn_norm

        return gcn_norm(adj_t, edge_weight, adj_t.size(0), dtype=torch.float)

    def forward_pair(
        self,
        x: torch.Tensor,
        adj_t,
        edge_weight,
        edge: torch.Tensor,
        profile: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Stream each hop into the current edge batch without a hop stack."""
        weights = self.pair_weights(profile)
        x = F.dropout(x, p=self.dropout, training=self.training)
        x = self.lin1(x)
        adj_t = self._normalized_adj(adj_t, edge_weight)
        src, dst = edge[0], edge[1]
        h_src = x[src] * weights[:, 0].unsqueeze(-1)
        h_dst = x[dst] * weights[:, 0].unsqueeze(-1)
        for k in range(self.K):
            x = self.propagate(adj_t, x=x, edge_weight=edge_weight, size=None)
            h_src = h_src + x[src] * weights[:, k + 1].unsqueeze(-1)
            h_dst = h_dst + x[dst] * weights[:, k + 1].unsqueeze(-1)
        return h_src, h_dst, weights


def batches(num_items: int, batch_size: int, seed: int, epoch: int):
    generator = torch.Generator(device="cpu")
    generator.manual_seed(seed * 1000003 + epoch * 9176 + 17)
    perm = torch.randperm(num_items, generator=generator)
    for start in range(0, num_items, batch_size):
        yield perm[start : start + batch_size]


def predict_parent_edges(model, predictor, data, edges, profile, batch_size, device, variant):
    h = model(data.x, data.adj_t, data.edge_weight)
    outputs = []
    for inds in DataLoader(range(edges.size(0)), batch_size=batch_size, shuffle=False):
        batch_edges = edges[inds].t().to(device)
        profile_batch = torch.from_numpy(profile[inds.numpy()]).to(device)
        if variant == "B2" or variant == "B3":
            src, dst, _ = model.forward_pair(data.x, data.adj_t, data.edge_weight, batch_edges, profile_batch)
            out = predictor(src, dst)
        elif variant == "B1":
            src, dst = batch_edges[0], batch_edges[1]
            out = predictor(h[src], h[dst], profile_batch)
        else:
            src, dst = batch_edges[0], batch_edges[1]
            out = predictor(h[src], h[dst])
        outputs.append(out.reshape(-1).detach().cpu())
    return torch.cat(outputs, dim=0)


@torch.no_grad()
def predict_pdg_edges_from_hops(model, predictor, hops, edges, profile, batch_size, device):
    """Evaluate PDG with one shared hop pass and small edge chunks."""
    outputs = []
    all_weights = []
    for inds in DataLoader(range(edges.size(0)), batch_size=batch_size, shuffle=False):
        edge = edges[inds].t().to(device)
        weights = model.pair_weights(torch.from_numpy(profile[inds.numpy()]).to(device))
        src, dst = edge[0], edge[1]
        h_src = hops[0][src] * weights[:, 0].unsqueeze(-1)
        h_dst = hops[0][dst] * weights[:, 0].unsqueeze(-1)
        for k in range(model.K):
            h_src = h_src + hops[k + 1][src] * weights[:, k + 1].unsqueeze(-1)
            h_dst = h_dst + hops[k + 1][dst] * weights[:, k + 1].unsqueeze(-1)
        outputs.append(predictor(h_src, h_dst).reshape(-1).detach().cpu())
        all_weights.append(weights.detach().cpu())
    return torch.cat(outputs), torch.cat(all_weights)


@torch.no_grad()
def evaluate(model, predictor, data, split_edge, profiles, batch_size, device, variant, evaluator):
    model.eval()
    predictor.eval()
    if variant in ("B2", "B3"):
        hops = model.forward_hops(data.x, data.adj_t, data.edge_weight)
        pos_train, w_train = predict_pdg_edges_from_hops(model, predictor, hops, split_edge["train"]["edge"], profiles["train_pos"], batch_size, device)
        pos_valid, w_valid = predict_pdg_edges_from_hops(model, predictor, hops, split_edge["valid"]["edge"], profiles["valid_pos"], batch_size, device)
        neg_valid, w_valid_neg = predict_pdg_edges_from_hops(model, predictor, hops, split_edge["valid"]["edge_neg"], profiles["valid_neg"], batch_size, device)
        pos_test, w_test_pos = predict_pdg_edges_from_hops(model, predictor, hops, split_edge["test"]["edge"], profiles["test_pos"], batch_size, device)
        neg_test, w_test_neg = predict_pdg_edges_from_hops(model, predictor, hops, split_edge["test"]["edge_neg"], profiles["test_neg"], batch_size, device)
        weights = {
            "test_pos": w_test_pos,
            "test_neg": w_test_neg,
        }
    else:
        pos_train = predict_parent_edges(model, predictor, data, split_edge["train"]["edge"], profiles["train_pos"], batch_size, device, variant)
        pos_valid = predict_parent_edges(model, predictor, data, split_edge["valid"]["edge"], profiles["valid_pos"], batch_size, device, variant)
        neg_valid = predict_parent_edges(model, predictor, data, split_edge["valid"]["edge_neg"], profiles["valid_neg"], batch_size, device, variant)
        pos_test = predict_parent_edges(model, predictor, data, split_edge["test"]["edge"], profiles["test_pos"], batch_size, device, variant)
        neg_test = predict_parent_edges(model, predictor, data, split_edge["test"]["edge_neg"], profiles["test_neg"], batch_size, device, variant)
        weights = None
    metric = {}
    for k in (10, 50, 100):
        evaluator.K = k
        metric[f"Hits@{k}_valid"] = float(evaluator.eval({"y_pred_pos": pos_valid, "y_pred_neg": neg_valid})[f"hits@{k}"])
        metric[f"Hits@{k}_test"] = float(evaluator.eval({"y_pred_pos": pos_test, "y_pred_neg": neg_test})[f"hits@{k}"])
    metric["Hits@100_train"] = float(evaluator.eval({"y_pred_pos": pos_train, "y_pred_neg": neg_valid})["hits@100"])
    return metric, weights, {"test_pos": pos_test, "test_neg": neg_test}


def train_epoch(model, predictor, data, train_edges, train_profile, optimizer, batch_size, device, variant, seed, epoch, negative_generator, adj, degree, features, b3_rng):
    model.train()
    predictor.train()
    total_loss = 0.0
    total_examples = 0
    for inds in batches(train_edges.size(0), batch_size, seed, epoch):
        optimizer.zero_grad(set_to_none=True)
        pos_edge = train_edges[inds].t().to(device)
        pos_profile = train_profile[inds].to(device)
        neg_cpu = torch.randint(0, data.num_nodes, pos_edge.shape, generator=negative_generator, device="cpu")
        neg_edge = neg_cpu.contiguous()  # [2, batch], matching the official edge layout
        neg_profile_np = pair_profile(neg_edge.t(), adj, degree, features)
        if variant == "B3":
            neg_profile_np = shuffle_rows(neg_profile_np, b3_rng)
        neg_profile = torch.from_numpy(neg_profile_np).to(device)
        if variant in ("B2", "B3"):
            combined_edge = torch.cat([pos_edge, neg_edge.to(device)], dim=1)
            combined_profile = torch.cat([pos_profile, neg_profile], dim=0)
            combined_src, combined_dst, _ = model.forward_pair(
                data.x, data.adj_t, data.edge_weight, combined_edge, combined_profile
            )
            split_at = pos_edge.size(1)
            pos_src, pos_dst = combined_src[:split_at], combined_dst[:split_at]
            neg_src, neg_dst = combined_src[split_at:], combined_dst[split_at:]
            pos_out = predictor(pos_src, pos_dst)
            neg_out = predictor(neg_src, neg_dst)
        else:
            h = model(data.x, data.adj_t, data.edge_weight)
            if variant == "B1":
                pos_out = predictor(h[pos_edge[0]], h[pos_edge[1]], pos_profile)
                neg_out = predictor(h[neg_edge[0].to(device)], h[neg_edge[1].to(device)], neg_profile)
            else:
                pos_out = predictor(h[pos_edge[0]], h[pos_edge[1]])
                neg_out = predictor(h[neg_edge[0].to(device)], h[neg_edge[1].to(device)])
        loss = -torch.log(pos_out + 1e-15).mean() - torch.log(1 - neg_out + 1e-15).mean()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(predictor.parameters(), 1.0)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        count = pos_out.numel()
        total_loss += float(loss.item()) * count
        total_examples += count
    return total_loss / max(total_examples, 1)


def init_equivalence(data, args, profiles, device, batch_size):
    """Compare a copied parent and zero-gated PDG in eval mode."""
    set_seed(args.seed + 700000)
    parent = HLGNN(data, args).to(device)
    parent_pred = LinkPredictor(data.num_features, args.hidden_channels, 1, args.mlp_num_layers, args.dropout).to(device)
    pdg = HLGNNPDG(data, args).to(device)
    pdg_pred = LinkPredictor(data.num_features, args.hidden_channels, 1, args.mlp_num_layers, args.dropout).to(device)
    pdg.load_state_dict(parent.state_dict(), strict=False)
    pdg_pred.load_state_dict(parent_pred.state_dict())
    parent.eval(); parent_pred.eval(); pdg.eval(); pdg_pred.eval()
    edge = torch.cat([data._split_edge_for_sanity["valid"]["edge"][:16], data._split_edge_for_sanity["valid"]["edge_neg"][:16]], dim=0).t().to(device)
    profile = torch.from_numpy(np.concatenate([profiles["valid_pos"][:16], profiles["valid_neg"][:16]], axis=0)).to(device)
    with torch.no_grad():
        hp = parent(data.x, data.adj_t, data.edge_weight)
        lp = parent_pred(hp[edge[0]], hp[edge[1]])
        hs, hd, _ = pdg.forward_pair(data.x, data.adj_t, data.edge_weight, edge, profile)
        ld = pdg_pred(hs, hd)
    return float(torch.max(torch.abs(lp - ld)).item())


def subgroup_report(weights: Dict[str, torch.Tensor], test_profiles: Dict[str, np.ndarray], thresholds: Dict[str, List[float]], global_temp: np.ndarray):
    profiles = np.concatenate([test_profiles["test_pos"], test_profiles["test_neg"]], axis=0)
    weights_np = torch.cat([weights["test_pos"], weights["test_neg"]], dim=0).numpy()
    t = np.asarray(global_temp)
    abs_w = np.abs(weights_np)
    depth = (abs_w * np.arange(abs_w.shape[1], dtype=np.float32)).sum(axis=1) / (abs_w.sum(axis=1) + 1e-12)
    delta = np.abs(weights_np - t[None, :]).mean(axis=1)
    out = {}
    cn = profiles[:, 0]
    out["CN=0"] = _group_stats(depth, delta, cn == 0)
    out["CN=1"] = _group_stats(depth, delta, cn == np.log(2.0))
    out["CN>=2"] = _group_stats(depth, delta, cn >= np.log(3.0))
    degree = profiles[:, 1]
    dq = thresholds["degree"]
    out["degree_low"] = _group_stats(depth, delta, degree <= dq[0])
    out["degree_medium"] = _group_stats(depth, delta, (degree > dq[0]) & (degree <= dq[1]))
    out["degree_high"] = _group_stats(depth, delta, degree > dq[1])
    sim = profiles[:, 3]
    sq = thresholds["similarity"]
    out["similarity_low"] = _group_stats(depth, delta, sim <= sq[0])
    out["similarity_medium"] = _group_stats(depth, delta, (sim > sq[0]) & (sim <= sq[1]))
    out["similarity_high"] = _group_stats(depth, delta, sim > sq[1])
    return out


def _group_stats(depth, delta, mask):
    if not np.any(mask):
        return {"count": 0, "depth_mean": None, "depth_std": None, "delta_mean": None}
    return {
        "count": int(mask.sum()),
        "depth_mean": float(depth[mask].mean()),
        "depth_std": float(depth[mask].std()),
        "delta_mean": float(delta[mask].mean()),
    }


def run(args):
    set_seed(args.seed)
    device = torch.device(f"cuda:{args.device}" if torch.cuda.is_available() else "cpu")
    dataset = load_raw_planetoid(args.data_root, args.dataset)
    split_edge = do_edge_split(dataset)
    raw_data = dataset[0]
    # Current PyG versions classify the split helper's auxiliary edge tensors
    # as edge attributes inside ToSparseTensor. Keep only the official train
    # graph and node features for the propagation object.
    data = PyGData(x=raw_data.x, edge_index=split_edge["train"]["edge"].t())
    data.num_nodes = raw_data.num_nodes
    data = T.ToSparseTensor(remove_edge_index=False)(data).to(device)
    data._split_edge_for_sanity = split_edge
    features = data.x.detach().cpu().numpy().astype(np.float32, copy=False)
    train_adj, degree = make_train_adjacency(split_edge["train"]["edge"], data.num_nodes)
    profiles = {
        "train_pos": pair_profile(split_edge["train"]["edge"], train_adj, degree, features),
        "valid_pos": pair_profile(split_edge["valid"]["edge"], train_adj, degree, features),
        "valid_neg": pair_profile(split_edge["valid"]["edge_neg"], train_adj, degree, features),
        "test_pos": pair_profile(split_edge["test"]["edge"], train_adj, degree, features),
        "test_neg": pair_profile(split_edge["test"]["edge_neg"], train_adj, degree, features),
    }
    if args.variant == "B3":
        b3_rng = np.random.default_rng(args.seed + 310001)
        for key in ("train_pos", "valid_pos", "valid_neg", "test_pos", "test_neg"):
            profiles[key] = shuffle_rows(profiles[key], b3_rng)
    else:
        b3_rng = np.random.default_rng(args.seed + 310001)
    profile_train = torch.from_numpy(profiles["train_pos"])
    model_args = argparse.Namespace(K=args.K, init=args.init, alpha=args.alpha, dropout=args.dropout)
    if args.variant in ("B2", "B3"):
        model = HLGNNPDG(data, model_args).to(device)
        predictor = LinkPredictor(data.num_features, args.hidden_channels, 1, args.mlp_num_layers, args.dropout).to(device)
    elif args.variant == "B1":
        model = HLGNN(data, model_args).to(device)
        predictor = ProfileDirectPredictor(data.num_features, args.hidden_channels, 1, args.mlp_num_layers, args.dropout).to(device)
    else:
        model = HLGNN(data, model_args).to(device)
        predictor = LinkPredictor(data.num_features, args.hidden_channels, 1, args.mlp_num_layers, args.dropout).to(device)
    if args.variant == "B2":
        sanity = init_equivalence(data, argparse.Namespace(**vars(args)), profiles, device, args.batch_size)
        # The sanity check uses a separate construction seed; restore the
        # requested experiment seed before any stochastic training operation.
        set_seed(args.seed)
    else:
        sanity = None
    params = sum(p.numel() for p in list(model.parameters()) + list(predictor.parameters()) if p.requires_grad)
    optimizer = torch.optim.Adam(list(model.parameters()) + list(predictor.parameters()), lr=args.lr)
    evaluator = Evaluator(name="ogbl-collab")
    negative_generator = torch.Generator(device="cpu")
    negative_generator.manual_seed(args.seed + 10000019)
    history = []
    best_valid = -float("inf")
    best_epoch = -1
    best_state = None
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats(device)
    total_start = time.perf_counter()
    epoch_times = []
    for epoch in range(1, args.epochs + 1):
        epoch_start = time.perf_counter()
        loss = train_epoch(
            model, predictor, data, split_edge["train"]["edge"], profile_train,
            optimizer, args.batch_size, device, args.variant, args.seed, epoch,
            negative_generator, train_adj, degree, features, b3_rng,
        )
        metric, weights, preds = evaluate(model, predictor, data, split_edge, profiles, args.eval_batch_size, device, args.variant, evaluator)
        epoch_time = time.perf_counter() - epoch_start
        epoch_times.append(epoch_time)
        row = {"epoch": epoch, "loss": loss, "epoch_runtime_sec": epoch_time, **metric}
        history.append(row)
        if metric["Hits@100_valid"] > best_valid:
            best_valid = metric["Hits@100_valid"]
            best_epoch = epoch
            best_state = {
                "model": {key: value.detach().cpu().clone() for key, value in model.state_dict().items()},
                "predictor": {key: value.detach().cpu().clone() for key, value in predictor.state_dict().items()},
            }
        print(json.dumps({"variant": args.variant, "dataset": args.dataset, "seed": args.seed, "epoch": epoch, "loss": loss, "valid_hits100": metric["Hits@100_valid"], "test_hits100": metric["Hits@100_test"], "epoch_sec": epoch_time}, ensure_ascii=False), flush=True)
    model.load_state_dict(best_state["model"])
    predictor.load_state_dict(best_state["predictor"])
    final_metric, final_weights, _ = evaluate(model, predictor, data, split_edge, profiles, args.eval_batch_size, device, args.variant, evaluator)
    total_runtime = time.perf_counter() - total_start
    peak_allocated = torch.cuda.max_memory_allocated(device) if torch.cuda.is_available() else 0
    peak_reserved = torch.cuda.max_memory_reserved(device) if torch.cuda.is_available() else 0
    global_temp = model.temp.detach().cpu().numpy().tolist()
    diagnostics = None
    if args.variant in ("B2", "B3"):
        weights_np = torch.cat([final_weights["test_pos"], final_weights["test_neg"]], dim=0).numpy()
        abs_w = np.abs(weights_np)
        depth = (abs_w * np.arange(abs_w.shape[1], dtype=np.float32)).sum(axis=1) / (abs_w.sum(axis=1) + 1e-12)
        profile_train_all = np.concatenate([pair_profile(split_edge["train"]["edge"], train_adj, degree, features), pair_profile(split_edge["train"]["edge_neg"], train_adj, degree, features)], axis=0)
        thresholds = {
            "degree": np.quantile(profile_train_all[:, 1], [1/3, 2/3]).tolist(),
            "similarity": np.quantile(profile_train_all[:, 3], [1/3, 2/3]).tolist(),
        }
        diagnostics = {
            "expected_depth": {
                "mean": float(depth.mean()),
                "std": float(depth.std()),
                "quantiles": {str(q): float(np.quantile(depth, q)) for q in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]},
            },
            "mean_abs_w_minus_t": float(np.abs(weights_np - np.asarray(global_temp)[None, :]).mean()),
            "pairwise_std_w_mean": float(weights_np.std(axis=0).mean()),
            "pairwise_std_w_max": float(weights_np.std(axis=0).max()),
            "subgroups": subgroup_report(final_weights, {k: profiles[k] for k in ("test_pos", "test_neg")}, thresholds, np.asarray(global_temp)),
            "thresholds_train_only": thresholds,
        }
    result = {
        "dataset": args.dataset,
        "variant": args.variant,
        "seed": args.seed,
        "config": vars(args),
        "device": str(device),
        "trainable_parameters": int(params),
        "global_temp_final": global_temp,
        "initial_equivalence_max_abs_logit_diff": sanity,
        "best_epoch": best_epoch,
        "best_valid_hits100": float(best_valid),
        "best_metrics": final_metric,
        "mean_epoch_runtime_sec": float(np.mean(epoch_times)),
        "std_epoch_runtime_sec": float(np.std(epoch_times)),
        "total_runtime_sec": float(total_runtime),
        "peak_gpu_memory_allocated_mb": float(peak_allocated / 1024**2),
        "peak_gpu_memory_reserved_mb": float(peak_reserved / 1024**2),
        "history": history,
        "diagnostics": diagnostics,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"completed": str(output), "best_epoch": best_epoch, "best_metrics": final_metric, "total_runtime_sec": total_runtime}, ensure_ascii=False), flush=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["cora", "citeseer"], required=True)
    parser.add_argument("--variant", choices=["B0", "B1", "B2", "B3"], required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--data-root", default="~/dataset")
    parser.add_argument("--output", required=True)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--hidden-channels", type=int, default=8192)
    parser.add_argument("--mlp-num-layers", type=int, default=None)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--eval-batch-size", type=int, default=2048)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--K", type=int, default=20)
    parser.add_argument("--alpha", type=float, default=0.2)
    parser.add_argument("--init", default="RWR", choices=["SGC", "RWR", "KI", "Random"])
    args = parser.parse_args()
    if args.mlp_num_layers is None:
        args.mlp_num_layers = 3 if args.dataset == "cora" else 2
    return args


if __name__ == "__main__":
    run(parse_args())
