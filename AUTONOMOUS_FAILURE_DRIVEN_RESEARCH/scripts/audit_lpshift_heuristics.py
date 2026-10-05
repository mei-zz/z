"""Evaluate fixed heuristics on the official LPShift generated split.

This script is an audit tool, not a training script.  It uses the graph and
negative arrays written by LPShift and reproduces the ranking convention in
the repository's eval.py.  It is intended to run in the remote mei_env.
"""

import argparse
import hashlib
import json
import os
import time

import numpy as np
import scipy.sparse as ssp
import torch


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pair_scores(adj, pairs, kind, batch_size=100000):
    pairs = np.asarray(pairs, dtype=np.int64)
    deg = np.asarray(adj.sum(axis=1)).reshape(-1)
    if kind == "cn":
        weighted = adj
    elif kind == "aa":
        weights = np.zeros_like(deg, dtype=np.float64)
        nz = deg > 1.0
        weights[nz] = 1.0 / np.log(deg[nz])
        weighted = adj.multiply(weights).tocsr()
    elif kind == "ra":
        weights = np.zeros_like(deg, dtype=np.float64)
        nz = deg > 0.0
        weights[nz] = 1.0 / deg[nz]
        weighted = adj.multiply(weights).tocsr()
    elif kind == "pa":
        return (deg[pairs[:, 0]] * deg[pairs[:, 1]]).astype(np.float32)
    else:
        raise ValueError(kind)

    out = np.empty(pairs.shape[0], dtype=np.float32)
    for start in range(0, pairs.shape[0], batch_size):
        stop = min(start + batch_size, pairs.shape[0])
        src = pairs[start:stop, 0]
        dst = pairs[start:stop, 1]
        out[start:stop] = np.asarray(adj[src].multiply(weighted[dst]).sum(axis=1)).reshape(-1)
    return out


def evaluate(pos, neg, scores):
    pos_score = torch.from_numpy(scores[: len(pos)])
    neg_score = torch.from_numpy(scores[len(pos):]).view(len(pos), -1)
    optimistic = (neg_score >= pos_score.view(-1, 1)).sum(dim=1)
    pessimistic = (neg_score > pos_score.view(-1, 1)).sum(dim=1)
    rank = 0.5 * (optimistic + pessimistic) + 1.0
    result = {
        "MRR": round((1.0 / rank).mean().item(), 4),
        "Hits@1": round((rank <= 1).float().mean().item(), 4),
        "Hits@3": round((rank <= 3).float().mean().item(), 4),
        "Hits@10": round((rank <= 10).float().mean().item(), 4),
        "Hits@20": round((rank <= 20).float().mean().item(), 4),
        "Hits@50": round((rank <= 50).float().mean().item(), 4),
        "Hits@100": round((rank <= 100).float().mean().item(), 4),
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--dataset", default="ogbl-collab_CN_2_1_0_seed1")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    os.chdir(args.repo)
    ds_dir = os.path.join("dataset", args.dataset + "Dataset")
    data = torch.load(os.path.join(ds_dir, args.dataset + "Dataset.pt"), weights_only=False)
    split = torch.load(os.path.join(ds_dir, args.dataset + "Dataset_split.pt"), weights_only=False)

    edge_index = data.edge_index.detach().cpu().numpy().astype(np.int64)
    n = int(data.num_nodes)
    adj = ssp.csr_matrix((np.ones(edge_index.shape[1], dtype=np.float32),
                          (edge_index[0], edge_index[1])), shape=(n, n))
    adj.sum_duplicates()
    adj.data[:] = 1.0

    result = {
        "dataset": args.dataset,
        "node_count": n,
        "message_graph_edges_directed": int(edge_index.shape[1]),
        "heuristics": {},
        "files": {},
    }
    for split_name in ("valid", "test"):
        pos = split[split_name]["edge"].detach().cpu().numpy().astype(np.int64)
        neg = split[split_name]["edge_neg"].detach().cpu().numpy().astype(np.int64)
        pair_matrix = np.concatenate([pos, neg.reshape(-1, 2)], axis=0)
        split_result = {"positive_count": int(pos.shape[0]), "negative_per_positive": int(neg.shape[1])}
        for kind in ("cn", "aa", "ra", "pa"):
            start = time.time()
            scores = pair_scores(adj, pair_matrix, kind)
            split_result[kind] = evaluate(pos, neg, scores)
            split_result[kind]["seconds"] = round(time.time() - start, 3)
        result["heuristics"][split_name] = split_result
        for name in ("edge_neg",):
            path = os.path.join(ds_dir, "heart_" + split_name + "_samples.npy")
            if os.path.exists(path):
                result["files"][split_name + "_negative_file"] = {
                    "path": path,
                    "bytes": os.path.getsize(path),
                    "sha256": sha256_file(path),
                }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
