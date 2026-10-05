import argparse
import copy
import hashlib
import json
import os
import random
import sys
from collections import defaultdict

import numpy as np
import torch

sys.path.insert(0, os.environ.get("NODEDUP_DIR", "/home/ubuntu/AFDR_V10/NodeDup"))


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def cache_path(data_dir, dataset):
    return os.path.join(data_dir, f"{dataset}-1.0-1.0-1.0-1.0-500neg-induc.pkl")


def add_adj(adj, edge):
    u, v = int(edge[0]), int(edge[1])
    if u == v:
        return
    adj[u].add(v)
    adj[v].add(u)


def all_positive_adjacency(split_edge, n):
    adj = [set() for _ in range(n)]
    for e in split_edge["train"]["edge"].tolist():
        add_adj(adj, e)
    for split in ("valid", "test"):
        for item in split_edge[split]["new"].values():
            for j in range(item["positive"].size(1)):
                add_adj(adj, item["positive"][:, j].tolist())
    return adj


def edge_type(u, v, old_count):
    u_new, v_new = u >= old_count, v >= old_count
    if not u_new and not v_new:
        return "old-old"
    if u_new and v_new:
        return "new-new"
    return "old-new"


def make_partition(old_count, n_nodes, seed, new_new_edges):
    nodes = list(range(old_count, n_nodes))
    rng = random.Random(seed)
    # Coverage is a structural precondition, not a performance-based choice:
    # reserve the first new-new edge for validation and the first disjoint
    # new-new edge for test, then fill the remaining node partition by seed.
    new_new_edges = sorted(tuple(sorted(e)) for e in new_new_edges)
    val_anchor = set(new_new_edges[0]) if new_new_edges else set()
    test_anchor = set()
    for e in new_new_edges[1:]:
        if not (set(e) & val_anchor):
            test_anchor = set(e)
            break
    if new_new_edges and not test_anchor:
        raise RuntimeError("Cannot construct disjoint validation/test new-new coverage")
    remaining = [x for x in nodes if x not in val_anchor and x not in test_anchor]
    rng.shuffle(remaining)
    n_val = max(len(val_anchor), len(nodes) // 2)
    val_nodes = set(val_anchor) | set(remaining[: n_val - len(val_anchor)])
    test_nodes = set(nodes) - val_nodes
    if not test_anchor <= test_nodes:
        raise RuntimeError("Test anchor was not preserved")
    return val_nodes, test_nodes


def validation_negatives(source, original_neg, allowed, adj, count, seed):
    allowed = set(allowed)
    chosen = []
    seen = set()
    for target in original_neg[1].tolist():
        target = int(target)
        if target in allowed and target != source and target not in seen:
            chosen.append(target)
            seen.add(target)
        if len(chosen) == count:
            break
    if len(chosen) < count:
        pool = [
            x for x in allowed
            if x != source and x not in adj[source] and x not in seen
        ]
        random.Random(seed).shuffle(pool)
        chosen.extend(pool[: count - len(chosen)])
    if len(chosen) != count:
        raise RuntimeError(f"Could not create {count} validation negatives for node {source}")
    return torch.tensor([[source] * count, chosen], dtype=torch.long)


def groups_from_candidates(candidate_dict, category_filter=None):
    groups = []
    for source in sorted(candidate_dict):
        item = candidate_dict[source]
        groups.append({
            "source": int(source),
            "category": category_filter or "mixed",
            "positive": item["positive"].clone(),
            "negative": item["negative"].clone(),
        })
    return groups


def build_protocol(cache, partition_seed=113, neg_count=500):
    train_data, inference_data, split_edge = cache
    old_count = int(train_data.x.size(0))
    n_nodes = int(inference_data.x.size(0))
    original_test = split_edge["test"]["new"]
    new_new_edges = set()
    for item in original_test.values():
        e = item["positive"]
        for j in range(e.size(1)):
            u, v = int(e[0, j]), int(e[1, j])
            if u >= old_count and v >= old_count:
                new_new_edges.add((u, v))
    val_nodes, test_nodes = make_partition(old_count, n_nodes, partition_seed, new_new_edges)
    adj = all_positive_adjacency(split_edge, n_nodes)

    old_valid = groups_from_candidates(split_edge["valid"]["new"], "old-old")
    val_by_category = defaultdict(list)
    test_by_category = defaultdict(list)

    # Build one group per source and edge type. A cross validation-new/test-new
    # edge is deliberately excluded from both target sets, so target-node sets
    # are disjoint. It remains only an observed graph/context fact if present in
    # the fixed inference graph.
    val_pos = defaultdict(lambda: defaultdict(list))
    test_pos = defaultdict(lambda: defaultdict(list))
    val_neg_src = {}
    test_neg_src = {}
    for source in sorted(original_test):
        source = int(source)
        item = original_test[source]
        val_neg_src[source] = item["negative"].clone()
        test_neg_src[source] = item["negative"].clone()
        for j in range(item["positive"].size(1)):
            u = int(item["positive"][0, j])
            v = int(item["positive"][1, j])
            new_endpoints = [x for x in (u, v) if x >= old_count]
            category = edge_type(u, v, old_count)
            if new_endpoints and all(x in val_nodes for x in new_endpoints):
                val_pos[source][category].append((u, v))
            elif new_endpoints and all(x in test_nodes for x in new_endpoints):
                test_pos[source][category].append((u, v))
            elif not new_endpoints:
                test_pos[source][category].append((u, v))
            # Cross-group target edges are excluded from both target sets.

    allowed_val = set(range(old_count)) | val_nodes
    for source in sorted(val_pos):
        for category in sorted(val_pos[source]):
            pairs = val_pos[source][category]
            if not pairs:
                continue
            pos = torch.tensor(pairs, dtype=torch.long).t().contiguous()
            neg = validation_negatives(
                source, val_neg_src[source], allowed_val, adj, neg_count,
                seed=910000 + source,
            )
            val_by_category[category].append({
                "source": source, "category": category,
                "positive": pos, "negative": neg,
            })

    for source in sorted(test_pos):
        for category in sorted(test_pos[source]):
            pairs = test_pos[source][category]
            if not pairs:
                continue
            pos = torch.tensor(pairs, dtype=torch.long).t().contiguous()
            neg = test_neg_src[source].clone()
            test_by_category[category].append({
                "source": source, "category": category,
                "positive": pos, "negative": neg,
            })

    val_new = [g for cat in sorted(val_by_category) for g in val_by_category[cat]]
    test_new = [g for cat in sorted(test_by_category) for g in test_by_category[cat]]
    combined = old_valid + val_new

    def positive_nodes(groups):
        out = set()
        for g in groups:
            out.update(int(x) for x in g["positive"].reshape(-1).tolist())
        return out

    val_target_nodes = positive_nodes(val_new) - set(range(old_count))
    test_target_nodes = positive_nodes(test_new) - set(range(old_count))
    overlap = sorted(val_target_nodes & test_target_nodes)
    if overlap:
        raise RuntimeError(f"Validation-new/test-new overlap: {overlap[:10]}")
    if not val_target_nodes <= val_nodes:
        raise RuntimeError("Validation target contains a node outside validation-new partition")
    if not test_target_nodes <= test_nodes:
        raise RuntimeError("Test target contains a node outside test-new partition")

    manifest = {
        "old_count": old_count,
        "node_count": n_nodes,
        "partition_seed": partition_seed,
        "partition_rule": "first disjoint new-new edge anchors plus seeded fill",
        "original_new_new_positive_edges": len(new_new_edges),
        "validation_new_nodes": sorted(val_nodes),
        "test_new_nodes": sorted(test_nodes),
        "n_validation_new_target_nodes": len(val_target_nodes),
        "n_test_new_target_nodes": len(test_target_nodes),
        "validation_positive_counts": {k: sum(g["positive"].size(1) for g in v) for k, v in val_by_category.items()},
        "test_positive_counts": {k: sum(g["positive"].size(1) for g in v) for k, v in test_by_category.items()},
        "validation_source_counts": {k: len(v) for k, v in val_by_category.items()},
        "test_source_counts": {k: len(v) for k, v in test_by_category.items()},
        "cross_partition_edges_excluded": True,
    }
    canonical = json.dumps(manifest, sort_keys=True).encode()
    manifest["manifest_sha256"] = hashlib.sha256(canonical).hexdigest()
    return {
        "train_data": train_data,
        "inference_data": inference_data,
        "split_edge": split_edge,
        "old_valid": old_valid,
        "val_new": val_new,
        "combined": combined,
        "test_new": test_new,
        "val_by_category": dict(val_by_category),
        "test_by_category": dict(test_by_category),
        "manifest": manifest,
    }


def make_score_groups(groups, h, predictor, device):
    result = []
    predictor.eval()
    with torch.no_grad():
        for g in groups:
            pos = g["positive"].to(device)
            neg = g["negative"].to(device)
            pos_scores = predictor(h[pos[0]], h[pos[1]]).reshape(-1)
            neg_scores = predictor(h[neg[0]], h[neg[1]]).reshape(-1)
            result.append((g, pos_scores.detach().cpu(), neg_scores.detach().cpu()))
    return result


def summarize_scored(scored):
    if not scored:
        return {"n_positive": 0, "mrr": None, "hits@10": None, "hits@20": None, "hits@50": None}
    mrr, h10, h20, h50 = [], [], [], []
    for _, pos, neg in scored:
        ranks = (neg.view(1, -1) > pos.view(-1, 1)).sum(1).float()
        ties = (neg.view(1, -1) >= pos.view(-1, 1)).sum(1).float()
        rank = 0.5 * (ranks + ties) + 1.0
        mrr.extend((1.0 / rank).tolist())
        h10.extend((rank <= 10).float().tolist())
        h20.extend((rank <= 20).float().tolist())
        h50.extend((rank <= 50).float().tolist())
    return {
        "n_positive": len(mrr),
        "mrr": float(np.mean(mrr)),
        "hits@10": float(np.mean(h10)),
        "hits@20": float(np.mean(h20)),
        "hits@50": float(np.mean(h50)),
    }


def score_metrics(groups, h, predictor, device):
    return summarize_scored(make_score_groups(groups, h, predictor, device))


def test_category_metrics(groups, h, predictor, device):
    return {cat: score_metrics(gs, h, predictor, device) for cat, gs in sorted(groups.items())}


def feature_proxy_scores(groups, x, kind, edge_index=None):
    n = x.size(0)
    if kind == "feature_cosine":
        x = torch.nn.functional.normalize(x.float(), p=2, dim=1)
        matrix = None
    else:
        adj = torch.zeros((n, n), dtype=torch.float32)
        ei = edge_index.cpu()
        adj[ei[0], ei[1]] = 1.0
        adj[ei[1], ei[0]] = 1.0
        if kind == "cn":
            matrix = adj @ adj.t()
        elif kind == "ra":
            inv = torch.zeros(n)
            deg = adj.sum(1)
            inv[deg > 0] = 1.0 / deg[deg > 0]
            matrix = (adj * inv.view(1, -1)) @ adj.t()
        else:
            raise ValueError(kind)
    scored = []
    for g in groups:
        pos, neg = g["positive"], g["negative"]
        if kind == "feature_cosine":
            ps = (x[pos[0]] * x[pos[1]]).sum(1)
            ns = (x[neg[0]] * x[neg[1]]).sum(1)
        else:
            ps = matrix[pos[0], pos[1]]
            ns = matrix[neg[0], neg[1]]
        scored.append((g, ps, ns))
    return summarize_scored(scored)


def run_one(dataset, augment, seed, data_dir, output_dir, epochs, device_name):
    # PyTorch 2.8 compatibility for trusted local benchmark cache only.
    cache = torch.load(cache_path(data_dir, dataset), map_location="cpu", weights_only=False)
    protocol = build_protocol(cache)
    train_cpu = copy.deepcopy(protocol["train_data"])
    split = copy.deepcopy(protocol["split_edge"])
    if augment == "duplicated":
        from main import data_augmentation
        train_cpu, split = data_augmentation(train_cpu, split, "duplicated", 2, 1, "cold")
    split["full_train"] = split["train"]["edge"]
    train_data = train_cpu.to(device_name)
    inference_data = protocol["inference_data"].to(device_name)
    from main import train as official_train
    from models import SAGE, LinkPredictor

    set_seed(seed)
    in_dim = int(inference_data.x.size(1))
    model = SAGE(dataset, in_dim, 256, 256, 2, 0.5).to(device_name)
    predictor = LinkPredictor("sum", 256, 256, 1, 2, 0.5).to(device_name)
    lr = 5e-4 if dataset == "cora" else 1e-4
    optimizer = torch.optim.Adam(list(model.parameters()) + list(predictor.parameters()), lr=lr)
    old_valid = protocol["old_valid"]
    val_new = protocol["val_new"]
    combined = protocol["combined"]
    histories = []
    states = []
    for epoch in range(1, epochs + 1):
        loss = official_train(model, predictor, train_data, split, optimizer, 64 * 1024, "sage", dataset, "induc")
        model.eval()
        predictor.eval()
        with torch.no_grad():
            h = model(inference_data.x, inference_data.edge_index)
        old_metrics = score_metrics(old_valid, h, predictor, device_name)
        new_metrics = score_metrics(val_new, h, predictor, device_name)
        combined_metrics = score_metrics(combined, h, predictor, device_name)
        histories.append({
            "epoch": epoch,
            "loss": float(loss),
            "old_old": old_metrics,
            "new": new_metrics,
            "combined": combined_metrics,
        })
        states.append({
            "model": {k: v.detach().cpu().clone() for k, v in model.state_dict().items()},
            "predictor": {k: v.detach().cpu().clone() for k, v in predictor.state_dict().items()},
        })

    def best(key, metric):
        return max(range(len(histories)), key=lambda i: (histories[i][key][metric], -histories[i]["epoch"]))

    selected = {
        "A_old_hits20": best("old_old", "hits@20"),
        "B_old_mrr": best("old_old", "mrr"),
        "C_combined_hits20": best("combined", "hits@20"),
        "D_combined_mrr": best("combined", "mrr"),
    }
    test_results = {}
    for rule, idx in selected.items():
        model.load_state_dict(states[idx]["model"])
        predictor.load_state_dict(states[idx]["predictor"])
        model.eval(); predictor.eval()
        with torch.no_grad():
            h = model(inference_data.x, inference_data.edge_index)
        all_test = score_metrics(protocol["test_new"], h, predictor, device_name)
        cats = test_category_metrics(protocol["test_by_category"], h, predictor, device_name)
        test_results[rule] = {
            "selected_epoch": histories[idx]["epoch"],
            "selection_metrics": histories[idx],
            "test_overall": all_test,
            "test_by_category": cats,
        }

    x_cpu = protocol["inference_data"].x.cpu()
    ei_cpu = protocol["inference_data"].edge_index.cpu()
    proxy_groups = {"old_old": old_valid, "new": val_new, "combined": combined, "test": protocol["test_new"]}
    proxies = {}
    for kind in ("feature_cosine", "cn", "ra"):
        proxies[kind] = {name: feature_proxy_scores(gs, x_cpu, kind, ei_cpu) for name, gs in proxy_groups.items()}

    out = {
        "dataset": dataset,
        "augment": augment,
        "seed": seed,
        "training": {"epochs": epochs, "lr": lr, "hidden": 256, "layers": 2, "dropout": 0.5, "predictor": "sum", "batch_size": 65536},
        "selection_metric_test_used": False,
        "protocol": protocol["manifest"],
        "history": histories,
        "selected": test_results,
        "proxies": proxies,
    }
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{dataset}_{augment}_seed{seed}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({"dataset": dataset, "augment": augment, "seed": seed, "path": path, "selected_epochs": {k: v["selected_epoch"] for k, v in test_results.items()}}, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=["cora", "citeseer"])
    ap.add_argument("--augment", required=True, choices=["none", "duplicated"])
    ap.add_argument("--seed", required=True, type=int)
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--output-dir", default="/home/ubuntu/AFDR_V11/results")
    ap.add_argument("--epochs", type=int, default=100)
    ap.add_argument("--device", default="cuda:0")
    args = ap.parse_args()
    run_one(args.dataset, args.augment, args.seed, args.data_dir, args.output_dir, args.epochs, torch.device(args.device if torch.cuda.is_available() else "cpu"))


if __name__ == "__main__":
    main()
