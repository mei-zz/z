"""V9 feature/topology attribution controls for the frozen LPShift protocol.

This script adds only attribution controls. It does not change DCDLP and does
not implement a new message-passing architecture.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as ssp
import torch
from torch import nn

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "V8" / "scripts"))

from dcdlp.data.negative_sampling import uniform_negative_sampling
from dcdlp.evaluation.ranking import ranking_metrics
from dcdlp.models.losses import link_prediction_loss
from dcdlp.utils import seed_everything
from lpshift_adapter import LPShiftData, sha256_array


FEATURE_NAMES = (
    "log_degree_min", "log_degree_max", "log_degree_product", "log_degree_gap",
    "log_cn", "cn_normalized", "log_aa", "log_ra", "feature_cosine",
    "feature_abs_diff",
)


class FeatureMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(2, 64), nn.ReLU(), nn.Dropout(0.1), nn.Linear(64, 1))

    def forward(self, x):
        return self.net(x[:, 8:10]).squeeze(-1)


class TopologyMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(8, 64), nn.ReLU(), nn.Dropout(0.1), nn.Linear(64, 1))

    def forward(self, x):
        return self.net(x[:, :8]).squeeze(-1)


class LinearFusion(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 1)

    def forward(self, x):
        return self.linear(x).squeeze(-1)


class ParamMatchedFusion(nn.Module):
    """10 -> 164 -> 164 -> 1: 29,029 parameters, near DCDLP's 28,966."""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 164), nn.ReLU(), nn.Dropout(0.1),
            nn.Linear(164, 164), nn.ReLU(), nn.Dropout(0.1),
            nn.Linear(164, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


def make_adjacency(adapter):
    edge = adapter.message_edge_index.detach().cpu().numpy().astype(np.int64, copy=False)
    adj = ssp.csr_matrix((np.ones(edge.shape[1], dtype=np.float32), (edge[0], edge[1])), shape=(adapter.num_nodes, adapter.num_nodes))
    adj.sum_duplicates()
    adj.data[:] = 1.0
    return adj


def pair_features(adj, features, pairs, degree_mask=None, batch_size=100000):
    """Compute ten transparent pair features from the frozen message graph.

    `degree_mask` marks target edges whose two endpoint degrees must be reduced
    by one. The common-neighbor and AA/RA terms are unchanged by removing the
    direct endpoint edge in a simple undirected graph.
    """
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    degree = np.asarray(adj.sum(axis=1)).reshape(-1).astype(np.float32)
    aa_adj = adj.multiply(np.where(degree > 1, 1.0 / np.log(np.maximum(degree, 2)), 0.0)).tocsr()
    ra_adj = adj.multiply(np.where(degree > 0, 1.0 / degree, 0.0)).tocsr()
    feat_norm = np.linalg.norm(features, axis=1)
    outputs = [[] for _ in FEATURE_NAMES]
    if degree_mask is None:
        degree_mask = np.zeros(len(pairs), dtype=bool)
    else:
        degree_mask = np.asarray(degree_mask, dtype=bool)
    for start in range(0, len(pairs), batch_size):
        rows = pairs[start:start + batch_size]
        mask = degree_mask[start:start + batch_size]
        u, v = rows[:, 0], rows[:, 1]
        du = degree[u].copy()
        dv = degree[v].copy()
        du[mask] -= 1.0
        dv[mask] -= 1.0
        du = np.maximum(du, 0.0)
        dv = np.maximum(dv, 0.0)
        common = adj[u].multiply(adj[v])
        cn = np.asarray(common.sum(axis=1)).reshape(-1).astype(np.float32)
        aa = np.asarray(adj[u].multiply(aa_adj[v]).sum(axis=1)).reshape(-1).astype(np.float32)
        ra = np.asarray(adj[u].multiply(ra_adj[v]).sum(axis=1)).reshape(-1).astype(np.float32)
        product = du * dv
        cosine = np.sum(features[u] * features[v], axis=1)
        denom = feat_norm[u] * feat_norm[v]
        cosine = np.divide(cosine, denom, out=np.zeros_like(cosine, dtype=np.float32), where=denom > 0)
        abs_diff = np.mean(np.abs(features[u] - features[v]), axis=1)
        rows_out = (
            np.log1p(np.minimum(du, dv)),
            np.log1p(np.maximum(du, dv)),
            np.log1p(product),
            np.abs(np.log1p(du) - np.log1p(dv)),
            np.log1p(cn),
            cn / np.sqrt(np.maximum(product, 1.0)),
            np.log1p(aa),
            np.log1p(ra),
            cosine,
            abs_diff,
        )
        for output, value in zip(outputs, rows_out):
            output.append(np.asarray(value, dtype=np.float32))
    return np.column_stack([np.concatenate(value) for value in outputs]).astype(np.float32, copy=False)


def metric_from_scores(pos, neg):
    return ranking_metrics(pos, neg, ks=(10, 20, 50, 100))


def score_model(model, features, device, batch_size):
    model.eval()
    outputs = []
    with torch.no_grad():
        for start in range(0, len(features), batch_size):
            batch = torch.from_numpy(np.asarray(features[start:start + batch_size])).to(device=device, dtype=torch.float32)
            outputs.append(model(batch).detach().cpu().numpy().astype(np.float32))
    return np.concatenate(outputs) if outputs else np.empty(0, dtype=np.float32)


def eval_model(model, valid_x, valid_pos_count, test_x, test_pos_count, device, batch_size):
    valid_score = score_model(model, valid_x, device, batch_size)
    test_score = score_model(model, test_x, device, batch_size)
    valid_pos, valid_neg = valid_score[:valid_pos_count], valid_score[valid_pos_count:]
    test_pos, test_neg = test_score[:test_pos_count], test_score[test_pos_count:]
    return (
        metric_from_scores(valid_pos, valid_neg.reshape(valid_pos_count, -1)),
        metric_from_scores(test_pos, test_neg.reshape(test_pos_count, -1)),
        (valid_pos, valid_neg.reshape(valid_pos_count, -1), test_pos, test_neg.reshape(test_pos_count, -1)),
    )


def model_factory(name):
    if name == "FeatureMLP":
        return FeatureMLP()
    if name == "TopologyMLP":
        return TopologyMLP()
    if name == "LinearFusion":
        return LinearFusion()
    if name == "ParamMatchedFusion":
        return ParamMatchedFusion()
    raise KeyError(name)


def prepare_pair_cache(adapter, adj, features, cache_dir, seed, epochs, batch_size):
    cache_dir.mkdir(parents=True, exist_ok=True)
    train_pos = adapter.train_pos.detach().cpu().numpy().astype(np.int64, copy=False)
    forbidden = np.asarray(sorted(adapter.message_edge_keys()), dtype=np.int64)
    positive_mask = np.ones(len(train_pos), dtype=bool)
    records = []
    for epoch in range(epochs):
        fpath = cache_dir / f"train_features_seed{seed}_epoch{epoch}.npy"
        opath = cache_dir / f"train_order_seed{seed}_epoch{epoch}.npy"
        if not fpath.exists() or not opath.exists():
            negative = uniform_negative_sampling(adapter.num_nodes, forbidden, len(train_pos), seed * 10000 + epoch)
            pos_features = pair_features(adj, features, train_pos, degree_mask=positive_mask, batch_size=batch_size)
            neg_features = pair_features(adj, features, negative, degree_mask=None, batch_size=batch_size)
            all_features = np.vstack([pos_features, neg_features]).astype(np.float32, copy=False)
            order = np.random.default_rng(seed * 1000 + epoch).permutation(len(all_features)).astype(np.int64)
            np.save(fpath, all_features)
            np.save(opath, order)
            negative_hash = sha256_array(negative)
            order_hash = sha256_array(order)
        else:
            negative_hash = None
            order_hash = sha256_array(np.load(opath, mmap_mode="r"))
        records.append({"epoch": epoch, "features": str(fpath), "order": str(opath), "negative_hash": negative_hash, "order_hash": order_hash})
    # Compute the epoch-0 training-only normalization from the complete train
    # pair set. It is reused by every learned control.
    train0 = np.load(records[0]["features"], mmap_mode="r")
    mean = np.asarray(train0.mean(axis=0), dtype=np.float32)
    std = np.asarray(train0.std(axis=0), dtype=np.float32)
    std[std < 1e-6] = 1.0
    np.save(cache_dir / "normalization_mean.npy", mean)
    np.save(cache_dir / "normalization_std.npy", std)
    # If an existing cache was reused, reconstruct the exact negative hash.
    for record in records:
        if record["negative_hash"] is None:
            epoch = record["epoch"]
            negative = uniform_negative_sampling(adapter.num_nodes, forbidden, len(train_pos), seed * 10000 + epoch)
            record["negative_hash"] = sha256_array(negative)
    return records, mean, std


def train_one(name, seed, records, mean, std, valid_x, test_x, n_train_pos, n_valid, n_test, device, batch_size, epochs, output_stem):
    seed_everything(seed)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    model = model_factory(name).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    mean_t = torch.from_numpy(mean).to(device=device)
    std_t = torch.from_numpy(std).to(device=device)
    valid_norm = ((valid_x - mean) / std).astype(np.float32, copy=False)
    test_norm = ((test_x - mean) / std).astype(np.float32, copy=False)
    best_state = None
    best_valid = -float("inf")
    best_epoch = -1
    trace = []
    started = time.perf_counter()
    for epoch_record in records:
        train_x = np.load(epoch_record["features"], mmap_mode="r")
        order = np.load(epoch_record["order"], mmap_mode="r")
        losses = []
        model.train()
        for start in range(0, len(order), batch_size):
            selected = np.asarray(order[start:start + batch_size])
            xb = torch.from_numpy(np.asarray(train_x[selected])).to(device=device, dtype=torch.float32)
            xb = (xb - mean_t) / std_t
            labels = torch.from_numpy((selected < n_train_pos).astype(np.float32)).to(device=device)
            # The train cache always concatenates equal-size positive and
            # negative blocks, so the midpoint is the positive-label boundary.
            logits = model(xb)
            loss = link_prediction_loss(logits, labels)
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            losses.append(float(loss.detach().cpu()))
        valid_score = score_model(model, valid_norm, device, batch_size)
        valid_metrics = metric_from_scores(valid_score[:n_valid], valid_score[n_valid:].reshape(n_valid, -1))
        trace.append({"epoch": epoch_record["epoch"], "mean_loss": float(np.mean(losses)), "validation": valid_metrics,
                      "negative_hash": epoch_record["negative_hash"], "order_hash": epoch_record["order_hash"]})
        if valid_metrics["mrr"] > best_valid:
            best_valid = valid_metrics["mrr"]
            best_epoch = epoch_record["epoch"]
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        del train_x, order
        gc.collect()
    model.load_state_dict(best_state)
    valid_metrics, test_metrics, scores = eval_model(model, valid_norm, n_valid, test_norm, n_test, device, batch_size)
    prediction_path = output_stem.with_name(output_stem.name + "_" + name + ".pred.npz")
    np.savez_compressed(prediction_path, valid_pos=scores[0], valid_neg=scores[1], test_pos=scores[2], test_neg=scores[3])
    return {
        "validation": valid_metrics, "test": test_metrics, "best_epoch": best_epoch,
        "runtime_seconds": time.perf_counter() - started,
        "peak_gpu_memory_mb": float(torch.cuda.max_memory_allocated(device) / 2**20) if device.type == "cuda" else None,
        "parameter_count": int(sum(value.numel() for value in model.parameters())),
        "prediction_file": str(prediction_path), "trace": trace,
        "training_budget": {"epochs": epochs, "batch_size": batch_size, "optimizer": "AdamW", "lr": 1e-3, "weight_decay": 1e-4},
    }


def fixed_result(name, valid_x, test_x, n_valid, n_test, output_stem):
    col = 8 if name == "FeatureCosine" else 7
    valid_score = valid_x[:, col]
    test_score = test_x[:, col]
    vp, vn = valid_score[:n_valid], valid_score[n_valid:]
    tp, tn = test_score[:n_test], test_score[n_test:]
    vmetrics = metric_from_scores(vp, vn.reshape(n_valid, -1))
    tmetrics = metric_from_scores(tp, tn.reshape(n_test, -1))
    prediction_path = output_stem.with_name(output_stem.name + "_" + name + ".pred.npz")
    np.savez_compressed(prediction_path, valid_pos=vp, valid_neg=vn.reshape(n_valid, -1), test_pos=tp, test_neg=tn.reshape(n_test, -1))
    return {"validation": vmetrics, "test": tmetrics, "best_epoch": None, "runtime_seconds": 0.0,
            "peak_gpu_memory_mb": None, "parameter_count": 0, "prediction_file": str(prediction_path),
            "training_budget": {"trained": False, "score": name, "tie_rule": "official average rank"}}


def run(args):
    seed_everything(args.seed)
    device = torch.device(args.device if args.device != "auto" else ("cuda" if torch.cuda.is_available() else "cpu"))
    adapter = LPShiftData.load(args.repo, args.dataset)
    features = adapter.features.detach().cpu().numpy().astype(np.float32, copy=False)
    adj = make_adjacency(adapter)
    cache_dir = Path(args.cache_dir) / (args.dataset + f"_seed{args.seed}")
    cache_started = time.perf_counter()
    records, mean, std = prepare_pair_cache(adapter, adj, features, cache_dir, args.seed, args.epochs, args.feature_batch_size)
    valid_pos = adapter.valid_pos.detach().cpu().numpy().astype(np.int64, copy=False)
    valid_neg = adapter.valid_neg.detach().cpu().numpy().astype(np.int64, copy=False)
    test_pos = adapter.test_pos.detach().cpu().numpy().astype(np.int64, copy=False)
    test_neg = adapter.test_neg.detach().cpu().numpy().astype(np.int64, copy=False)
    eval_started = time.perf_counter()
    valid_x = pair_features(adj, features, np.vstack([valid_pos, valid_neg.reshape(-1, 2)]), batch_size=args.feature_batch_size)
    test_x = pair_features(adj, features, np.vstack([test_pos, test_neg.reshape(-1, 2)]), batch_size=args.feature_batch_size)
    eval_cache_seconds = time.perf_counter() - eval_started
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    results = {
        "dataset": args.dataset, "seed": args.seed, "adapter_summary": adapter.summary(),
        "feature_names": list(FEATURE_NAMES), "normalization_mean": mean.tolist(), "normalization_std": std.tolist(),
        "protocol": {"train_negative_protocol": "uniform_non_message_edges", "target_masking": "degree statistics masked for train positives; no message encoder in controls", "test_used_for_selection": False,
                      "shared_negative_hashes": [record["negative_hash"] for record in records], "shared_order_hashes": [record["order_hash"] for record in records]},
        "cache_seconds": time.perf_counter() - cache_started, "eval_feature_seconds": eval_cache_seconds,
        "models": {},
    }
    stem = output.with_suffix("")
    results["models"]["FeatureCosine"] = fixed_result("FeatureCosine", valid_x, test_x, len(valid_pos), len(test_pos), stem)
    results["models"]["TopologyRA"] = fixed_result("TopologyRA", valid_x, test_x, len(valid_pos), len(test_pos), stem)
    for name in ("FeatureMLP", "TopologyMLP", "LinearFusion", "ParamMatchedFusion"):
        results["models"][name] = train_one(name, args.seed, records, mean, std, valid_x, test_x, len(adapter.train_pos), len(valid_pos), len(test_pos), device, args.batch_size, args.epochs, stem)
    results["control_parameter_target"] = {"DCDLP": 28966, "ParamMatchedFusion": results["models"]["ParamMatchedFusion"]["parameter_count"]}
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--cache-dir", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--epochs", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=262144)
    parser.add_argument("--feature-batch-size", type=int, default=100000)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
