from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import math
import multiprocessing as mp
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AUTONOMOUS_LP_RESEARCH_V12"
V71 = ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V7_1"
V61 = ROOT / "HYPERGRAPH_RESEARCH" / "NEGATIVE_V6_1"
V7 = ROOT / "HYPERGRAPH_RESEARCH" / "HARDNESS_V7"
V62 = ROOT / "HYPERGRAPH_RESEARCH" / "CODNS_V6_2"
sys.path[:0] = [str(ROOT / "src"), str(V71), str(V61), str(V62), str(V7),
                str(ROOT / "HYPERGRAPH_RESEARCH" / "QTHS_V8_PAPER")]

import numpy as np

ACTIVE_ARM = "BASELINE"
LAST_PAIRS = None
POSITIVE_WEIGHTS = {}
SHUFFLED_POSITIVE_WEIGHTS = {}
POSITIVE_EMA = {}
POSITIVE_PERM_MAP = {}
TRAIN_NEGATIVE_MAP = {}
NODE_PERMUTATION = None
CONSISTENCY_LOGITS = None
PATCHED = False


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical(pair):
    a, b = int(pair[0]), int(pair[1])
    return (a, b) if a <= b else (b, a)


def worker_init():
    os.environ.setdefault("OMP_NUM_THREADS", "2")
    os.environ.setdefault("MKL_NUM_THREADS", "2")
    import torch
    torch.set_num_threads(2)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass


def install_hooks():
    global PATCHED
    if PATCHED:
        return
    import torch
    from torch import nn
    from dcdlp.models.dcdlp import DCDLP
    init0, forward0, score0 = DCDLP.__init__, DCDLP.forward, DCDLP._score_state

    def init1(self, *args, **kwargs):
        init0(self, *args, **kwargs)
        hidden = int(args[1]) if len(args) >= 2 else int(kwargs.get("hidden_dim", 128))
        if ACTIVE_ARM.startswith("C1_"):
            self.v12_residual = nn.Sequential(nn.Linear(3 * hidden, 8), nn.Tanh(), nn.Linear(8, 1))
        elif ACTIVE_ARM.startswith("D1_"):
            self.v12_residual = nn.Sequential(nn.Linear(2 * hidden, 8), nn.Tanh(), nn.Linear(8, 1))
        elif ACTIVE_ARM.startswith("B2_"):
            if ACTIVE_ARM == "B2_TRIAD":
                self.v12_branch_interaction_scale = nn.Parameter(torch.zeros(2))
            else:
                self.v12_branch_calibration = nn.Parameter(torch.ones(2))
        elif ACTIVE_ARM.startswith(("X1_", "X2_")):
            branch = int(args[2]) if len(args) >= 3 else int(kwargs.get("branch_dim", 32))
            input_dim = (6 if ACTIVE_ARM.startswith("X2_") else 3) * branch
            self.v12_residual = nn.Sequential(nn.Linear(input_dim, 8), nn.Tanh(), nn.Linear(8, 1))
            nn.init.zeros_(self.v12_residual[-1].weight)
            nn.init.zeros_(self.v12_residual[-1].bias)
            if ACTIVE_ARM.startswith("X1_"):
                rng = np.random.default_rng(12012026)
                q, _ = np.linalg.qr(rng.standard_normal((3 * branch, 3 * branch)))
                qcat, _ = np.linalg.qr(rng.standard_normal((6 * branch, 3 * branch)))
                self.register_buffer("v12_random_orthogonal", torch.as_tensor(q, dtype=torch.float32))
                self.register_buffer("v12_concat_projection", torch.as_tensor(qcat, dtype=torch.float32))
            node_forward0 = self.node_encoder.forward
            def capture_graph_state(*f_args, **f_kwargs):
                state = node_forward0(*f_args, **f_kwargs)
                self._v12_graph_node_state = state
                return state
            self.node_encoder.forward = capture_graph_state

    def score1(self, h, pairs, neighbors, degrees, edge_index, apply_router):
        out = score0(self, h, pairs, neighbors, degrees, edge_index, apply_router)
        if ACTIVE_ARM.startswith("C1_"):
            out["_v12_hu"] = h[pairs[:, 0]]
            out["_v12_hv"] = h[pairs[:, 1]]
        elif ACTIVE_ARM.startswith("D1_"):
            n = h.shape[0]
            srcs, dsts = [], []
            for u, ns in enumerate(neighbors):
                for v in ns:
                    srcs.append(u)
                    dsts.append(int(v))
            sums = torch.zeros_like(h)
            counts = torch.zeros((n, 1), dtype=h.dtype, device=h.device)
            if srcs:
                src = torch.as_tensor(srcs, dtype=torch.long, device=h.device)
                dst = torch.as_tensor(dsts, dtype=torch.long, device=h.device)
                sums.index_add_(0, src, h[dst])
                counts.index_add_(0, src, torch.ones((len(src), 1), dtype=h.dtype, device=h.device))
            context = sums / counts.clamp_min(1.0)
            out["_v12_ctx_u"] = context[pairs[:, 0]]
            out["_v12_ctx_v"] = context[pairs[:, 1]]
            out["_v12_ctx_all"] = context
        elif ACTIVE_ARM.startswith(("X1_", "X2_")):
            graph = score0(self, self._v12_graph_node_state, pairs, neighbors, degrees,
                           edge_index, False)
            out["_v12_hyper_pair"] = torch.cat([out["z_degree"], out["z_cn"], out["z_residual"]], dim=-1)
            out["_v12_graph_pair"] = torch.cat([graph["z_degree"], graph["z_cn"], graph["z_residual"]], dim=-1)
        return out

    def forward1(self, x, edge_index, pairs, remove_target_edges=True, support_edge_index=None):
        global LAST_PAIRS, CONSISTENCY_LOGITS
        out = forward0(self, x, edge_index, pairs,
                       remove_target_edges=remove_target_edges,
                       support_edge_index=support_edge_index)
        CONSISTENCY_LOGITS = None
        if ACTIVE_ARM.startswith("H1_") and self.training:
            n = x.shape[0]
            a, b = edge_index[0], edge_index[1]
            lo, hi = torch.minimum(a, b), torch.maximum(a, b)
            _, inverse = torch.unique(lo * n + hi, sorted=True, return_inverse=True)
            keep_pair = torch.rand(int(inverse.max().item()) + 1, device=edge_index.device) >= 0.1
            dropped_edges = edge_index[:, keep_pair[inverse]]
            perturbed = forward0(self, x, dropped_edges, pairs,
                                 remove_target_edges=remove_target_edges,
                                 support_edge_index=None)
            CONSISTENCY_LOGITS = perturbed["logit"]
        if ACTIVE_ARM.startswith("C1_"):
            hu, hv = out["_v12_hu"], out["_v12_hv"]
            cross = hu * hv if ACTIVE_ARM == "C1_PAIR" else 0.5 * (hu.square() + hv.square())
            feature = torch.cat([hu + hv, (hu - hv).abs(), cross], dim=-1)
            out["logit"] = out["logit"] + self.v12_residual(feature).squeeze(-1)
        elif ACTIVE_ARM.startswith("D1_"):
            cu, cv = out["_v12_ctx_u"], out["_v12_ctx_v"]
            if ACTIVE_ARM == "D1_EGO_PERM":
                perm = torch.as_tensor(NODE_PERMUTATION, dtype=torch.long, device=cu.device)
                context = out["_v12_ctx_all"]
                cu, cv = context[perm[pairs[:, 0]]], context[perm[pairs[:, 1]]]
            feature = torch.cat([cu + cv, (cu - cv).abs()], dim=-1)
            out["logit"] = out["logit"] + self.v12_residual(feature).squeeze(-1)
        elif ACTIVE_ARM.startswith("X1_"):
            graph, hyper = out["_v12_graph_pair"], out["_v12_hyper_pair"]
            if ACTIVE_ARM == "X1_ORTHO":
                coefficient = (hyper * graph).sum(-1, keepdim=True) / graph.square().sum(-1, keepdim=True).clamp_min(1e-8)
                feature = hyper - coefficient * graph
            elif ACTIVE_ARM == "X1_RAW":
                feature = hyper
            elif ACTIVE_ARM == "X1_RANDOM":
                feature = hyper @ self.v12_random_orthogonal
            else:
                feature = torch.cat([graph, hyper], dim=-1) @ self.v12_concat_projection
            out["logit"] = out["logit"] + self.v12_residual(feature).squeeze(-1)
        elif ACTIVE_ARM.startswith("X2_"):
            graph, hyper = out["_v12_graph_pair"], out["_v12_hyper_pair"]
            if ACTIVE_ARM == "X2_CROSS":
                first_order = graph * hyper
            else:
                first_order = 0.5 * (graph.square() + hyper.square())
            feature = torch.cat([first_order, torch.abs(graph - hyper)], dim=-1)
            out["logit"] = out["logit"] + self.v12_residual(feature).squeeze(-1)
        elif ACTIVE_ARM.startswith("B2_"):
            if ACTIVE_ARM == "B2_TRIAD":
                dim_scale = out["z_residual"].shape[-1] ** 0.5
                interactions = torch.stack([
                    (out["z_degree"] * out["z_residual"]).sum(-1) / dim_scale,
                    (out["z_cn"] * out["z_residual"]).sum(-1) / dim_scale,
                ], dim=-1)
                out["logit"] = out["logit"] + (
                    interactions * self.v12_branch_interaction_scale
                ).sum(-1)
            else:
                out["logit"] = out["logit"] + (
                    (self.v12_branch_calibration[0] - 1.0) * out["score_degree"]
                    + (self.v12_branch_calibration[1] - 1.0) * out["score_cn"]
                )
        LAST_PAIRS = pairs.detach().cpu().numpy().copy()
        return out

    DCDLP.__init__ = init1
    DCDLP._score_state = score1
    DCDLP.forward = forward1
    PATCHED = True


def positive_weights(view):
    adj = [set() for _ in range(view.num_nodes)]
    for u, v in view.train_graph().edges():
        adj[int(u)].add(int(v))
        adj[int(v)].add(int(u))
    cn = np.asarray([len(adj[int(u)] & adj[int(v)]) for u, v in view.train_pos], dtype=np.int64)
    order = np.argsort(cn, kind="stable")
    ranks = np.empty(len(order), dtype=np.float64)
    ranks[order] = np.arange(len(order), dtype=np.float64) / max(1, len(order) - 1)
    weights = (2.0 - ranks)
    weights /= weights.mean()
    shuffled = weights[np.random.default_rng(731001).permutation(len(weights))]
    real = {canonical(edge): float(w) for edge, w in zip(view.train_pos, weights)}
    perm = {canonical(edge): float(w) for edge, w in zip(view.train_pos, shuffled)}
    return real, perm


def loss_hook(arm):
    import torch
    from torch.nn import functional as F
    calls = {"n": 0}

    def loss(logits, labels, *args, **kwargs):
        pos, neg = logits[labels > 0.5], logits[labels <= 0.5]
        if arm.startswith("F3_") and len(pos) and len(neg):
            if LAST_PAIRS is None or len(LAST_PAIRS) != len(labels):
                raise RuntimeError("local pair-ranking hook could not align the training pair batch")
            negative_rows = {}
            positive_rows = []
            for row_id, (edge, label) in enumerate(zip(LAST_PAIRS, labels.detach().cpu().tolist())):
                key = canonical(edge)
                if label > 0.5:
                    positive_rows.append((key, row_id))
                else:
                    negative_rows.setdefault(key, []).append(row_id)
            aligned = []
            for positive_key, positive_row in positive_rows:
                selected_key = TRAIN_NEGATIVE_MAP.get(positive_key)
                available = negative_rows.get(selected_key, [])
                if available:
                    aligned.append((positive_row, available.pop(0)))
            bce = F.binary_cross_entropy_with_logits(logits, labels)
            if aligned:
                positive_indices = torch.as_tensor([row[0] for row in aligned], dtype=torch.long, device=logits.device)
                negative_indices = torch.as_tensor([row[1] for row in aligned], dtype=torch.long, device=logits.device)
                if arm == "F3_SHUFFLED" and len(aligned) > 1:
                    negative_indices = negative_indices.roll(1)
                pairwise = F.softplus(logits[negative_indices] - logits[positive_indices]).mean()
                return bce + 0.1 * pairwise
            return bce
        if arm.startswith("F2_") and len(pos) and len(neg):
            bce = F.binary_cross_entropy_with_logits(logits, labels)
            k = min(10, len(neg))
            if arm == "F2_TOP10":
                selected = torch.topk(neg, k=k, largest=True, sorted=False).values
            else:
                calls["n"] += 1
                gen = torch.Generator(device=neg.device)
                gen.manual_seed(93000 + calls["n"])
                idx = torch.randperm(len(neg), generator=gen, device=neg.device)[:k]
                selected = neg[idx]
            return bce + 0.1 * F.softplus(selected.unsqueeze(0) - pos.unsqueeze(1)).mean()
        if arm.startswith("H1_"):
            if CONSISTENCY_LOGITS is None or len(CONSISTENCY_LOGITS) != len(labels):
                raise RuntimeError("topology consistency view is missing for a training batch")
            clean = torch.sigmoid(logits)
            perturbed = torch.sigmoid(CONSISTENCY_LOGITS)
            aux_terms=[]
            for label_value in (1.0,0.0):
                idx=torch.nonzero(labels == label_value,as_tuple=False).flatten()
                if len(idx)<2:
                    continue
                target=perturbed[idx]
                if arm == "H1_PAIRSHUFFLE":
                    target=target[torch.roll(torch.arange(len(idx),device=idx.device),1)]
                aux_terms.append(F.mse_loss(clean[idx],target))
            aux=torch.stack(aux_terms).mean() if aux_terms else logits.new_zeros(())
            return F.binary_cross_entropy_with_logits(logits,labels)+0.1*aux
        if arm.startswith("G2_"):
            if LAST_PAIRS is None or len(LAST_PAIRS)!=len(labels):
                raise RuntimeError("positive-difficulty hook could not align the training pair batch")
            per=F.binary_cross_entropy_with_logits(logits,labels,reduction="none")
            weights=torch.ones_like(labels)
            pos_idx=torch.nonzero(labels>0.5,as_tuple=False).flatten()
            raw=[]
            observed=[]
            for i in pos_idx.detach().cpu().tolist():
                key=canonical(LAST_PAIRS[i])
                hardness=float(torch.sigmoid(-logits[i].detach()).cpu())
                previous=POSITIVE_EMA.get(key,hardness)
                if arm=="G2_INSTANT":
                    signal=hardness
                elif arm=="G2_SHUFFLED":
                    paired=POSITIVE_PERM_MAP.get(key,key)
                    signal=POSITIVE_EMA.get(paired,hardness)
                else:
                    signal=previous
                raw.append(1.0+0.5*signal)
                observed.append((key,hardness))
            if raw:
                positive_weights=torch.as_tensor(raw,dtype=logits.dtype,device=logits.device)
                positive_weights=positive_weights/positive_weights.mean().clamp_min(1e-8)
                weights[pos_idx]=positive_weights
            for key,hardness in observed:
                POSITIVE_EMA[key]=0.8*POSITIVE_EMA.get(key,hardness)+0.2*hardness
            return (per*weights).mean()
        if arm.startswith("F1_") and len(pos) and len(neg):
            k = min(10, len(neg))
            if arm == "F1_TOP10":
                selected = torch.topk(neg, k=k, largest=True, sorted=False).values
            else:
                calls["n"] += 1
                gen = torch.Generator(device=neg.device)
                gen.manual_seed(91000 + calls["n"])
                idx = torch.randperm(len(neg), generator=gen, device=neg.device)[:k]
                selected = neg[idx]
            return F.softplus(selected.unsqueeze(0) - pos.unsqueeze(1)).mean()
        if arm.startswith("G1_"):
            if LAST_PAIRS is None or len(LAST_PAIRS) != len(labels):
                raise RuntimeError("positive-weight hook could not align the train pair batch")
            mapping = POSITIVE_WEIGHTS if arm == "G1_CLOSURE" else SHUFFLED_POSITIVE_WEIGHTS
            weights = torch.ones_like(labels)
            for i, (edge, label) in enumerate(zip(LAST_PAIRS, labels.detach().cpu().tolist())):
                if label > 0.5:
                    key = canonical(edge)
                    if key not in mapping:
                        raise RuntimeError("weight lookup received a non-training positive")
                    weights[i] = mapping[key]
            per_sample = F.binary_cross_entropy_with_logits(logits, labels, reduction="none")
            return (per_sample * weights).mean()
        return F.binary_cross_entropy_with_logits(logits, labels)
    return loss


def source_hashes():
    paths = [
        ROOT / "src/dcdlp/train.py",
        ROOT / "src/dcdlp/models/dcdlp.py",
        ROOT / "src/dcdlp/evaluate.py",
        ROOT / "src/dcdlp/evaluation/ranking.py",
        ROOT / "HYPERGRAPH_RESEARCH/QTHS_V8_PAPER/experiment_v8.py",
        ROOT / "HYPERGRAPH_RESEARCH/QTHS_V7_1/experiment_v71.py",
        ROOT / "HYPERGRAPH_RESEARCH/CODNS_V6_2/run_codns_v6_2.py",
        ROOT / "HYPERGRAPH_RESEARCH/NEGATIVE_V6_1/run_negative_v6_1.py",
        Path(__file__).resolve(),
    ]
    return {str(p.relative_to(ROOT)): sha256_file(p) for p in paths}


def run_one(task):
    global ACTIVE_ARM, LAST_PAIRS, POSITIVE_WEIGHTS, SHUFFLED_POSITIVE_WEIGHTS, NODE_PERMUTATION
    global POSITIVE_EMA, POSITIVE_PERM_MAP, TRAIN_NEGATIVE_MAP
    worker_init()
    import torch
    import experiment_v8 as v8
    from dcdlp import train as train_module
    ACTIVE_ARM = task["arm"]
    LAST_PAIRS = None
    install_hooks()
    dataset = task.get("dataset", "cora")
    seed = int(task.get("seed", 0))
    full, view, pool, scores, pool_hash, vp, vn, valid_hash = v8.dataset_context(dataset)
    if v8.v61.array_hash(pool) != pool_hash:
        raise RuntimeError("strict training candidate-pool hash mismatch")
    POSITIVE_WEIGHTS, SHUFFLED_POSITIVE_WEIGHTS = positive_weights(view)
    POSITIVE_EMA={}
    positive_keys=[canonical(edge) for edge in view.train_pos]
    positive_perm=np.random.default_rng(120221).permutation(len(positive_keys))
    POSITIVE_PERM_MAP={key:positive_keys[int(positive_perm[i])] for i,key in enumerate(positive_keys)}
    NODE_PERMUTATION = np.random.default_rng(810331).permutation(view.num_nodes)
    sampler = task.get("sampler", "SH75")
    selected = v8.selected_edges({"method": sampler, "seed": seed, "alpha": None}, pool, scores, view.train_pos)
    if selected.shape != (len(view.train_pos), 2):
        raise RuntimeError("SH75 sample shape mismatch")
    TRAIN_NEGATIVE_MAP = {
        canonical(positive): canonical(negative)
        for positive, negative in zip(view.train_pos, selected)
    }
    train_edges = {canonical(edge) for edge in view.train_graph().edges()}
    if any(canonical(edge) in train_edges for edge in selected):
        raise RuntimeError("SH75 sample contains a training/message edge")
    v8.engine.EPOCHS = int(task["epochs"])
    v8.engine.candidate_pool, v8.engine.candidate_pool_hash = pool, pool_hash
    v8.engine.validation_candidate_hash = valid_hash
    old_loss = train_module.link_prediction_loss
    train_module.link_prediction_loss = loss_hook(ACTIVE_ARM)
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    rel = folder.relative_to(ROOT).as_posix()
    started = time.perf_counter()
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()
    try:
        rec = v8.engine.train_one(
            view, f"V12_{task['candidate_id']}_{task['arm']}", seed, selected, rel,
            vp, vn, initialize_from_v6=False, dataset_name=dataset, hypergraph_mode="raw",
        )
        metrics, params = v8.metric_for_checkpoint(rec["checkpoint"], view, vp, vn)
        recorded_mrr = rec.get("epoch10_validation_mrr")
        if recorded_mrr is None or not math.isclose(float(metrics["mrr"]), float(recorded_mrr), rel_tol=0, abs_tol=1e-8):
            raise RuntimeError("fixed-final-epoch validation recheck mismatch")
        torch.cuda.synchronize()
        result = {
            **task,
            "state": "COMPLETE",
            "validation_metrics": metrics,
            "trainable_parameters": int(params),
            "train_seconds": float(rec.get("train_seconds", rec.get("runtime", {}).get("train_seconds", 0.0))),
            "total_wall_seconds": float(time.perf_counter() - started),
            "peak_gpu_memory_mb": float(torch.cuda.max_memory_allocated() / (1024 * 1024)),
            "checkpoint": str(rec["checkpoint"]),
            "checkpoint_sha256": sha256_file(Path(rec["checkpoint"])),
            "train_pool_hash": pool_hash,
            "sampler": sampler,
            "validation_candidate_hash": valid_hash,
            "selected_negative_hash": v8.v61.array_hash(selected),
            "test_evaluated": False,
            "source_hashes": source_hashes(),
            "candidate_patch_id": hashlib.sha256(
                (sha256_file(Path(__file__)) + task["candidate_id"] + task["arm"] + task["definition"]).encode()
            ).hexdigest(),
            "train_record": rec,
            "completed_at_utc": utc_now(),
        }
        atomic_json(folder / "result.json", result)
        return result
    except Exception as exc:
        result = {**task, "state": "FAILED", "error": repr(exc),
                  "traceback": traceback.format_exc(), "test_evaluated": False,
                  "completed_at_utc": utc_now()}
        atomic_json(folder / "result.json", result)
        return result
    finally:
        train_module.link_prediction_loss = old_loss
        torch.cuda.empty_cache()


def tasks():
    rows = [
        ("B0", "BASELINE", "SH75 plus BCE matched reference", "BCE baseline for the candidates"),
        ("F1", "F1_TOP10", "Softplus ranking of positives against batch-top ten SH75 negatives", "V12-F1"),
        ("F1", "F1_RANDOM10", "Softplus ranking of positives against random ten SH75 negatives", "V12-F1 matched control"),
        ("G1", "G1_CLOSURE", "Train-only positive closure-rank weights", "V12-G1"),
        ("G1", "G1_SHUFFLED", "Same positive weights under a fixed train-positive permutation", "V12-G1 matched control"),
        ("C1", "C1_PAIR", "Symmetric endpoint product MLP residual", "V12-C1"),
        ("C1", "C1_SELF", "Same-size MLP using endpoint self-moments", "V12-C1 parameter control"),
        ("D1", "D1_EGO", "One-hop target-masked pair-context residual", "V12-D1"),
        ("D1", "D1_EGO_PERM", "Same residual using fixed node-permuted context", "V12-D1 mechanism control"),
    ]
    output = []
    for i, (cid, arm, definition, purpose) in enumerate(rows, 1):
        output.append({
            "job_id": f"V12-S1-{i:02d}", "candidate_id": cid, "arm": arm,
            "family": {"F1":"F", "G1":"G", "C1":"B/C", "D1":"D"}.get(cid, "baseline"),
            "definition": definition, "purpose": purpose, "stage": "stage1",
            "dataset": "cora", "seed": 0, "epochs": 5, "priority": "P2",
            "estimated_cost": "1 Stage-1-equivalent", "status": "QUEUED",
            "gpu_mem_estimate": "under 1 GiB per process; verify pilot",
        })
    return output


def build_stage1b_tasks():
    common={"stage":"stage1b","dataset":"cora","seed":0,"epochs":5,"sampler":"QTHS25",
            "priority":"P1","estimated_cost":"1 Stage-1-equivalent","status":"QUEUED",
            "gpu_mem_estimate":"under 1 GiB per process"}
    rows=[("S1B_B0","BASELINE","baseline","QTHS25 plus BCE strong reference","matched strong baseline"),
          ("S1B_F2","F2_TOP10","F2","BCE-anchored batch-hard pairwise auxiliary loss","candidate"),
          ("S1B_F2_CTRL","F2_RANDOM10","F2","BCE plus random-ten pairwise auxiliary control","matched control"),
          ("S1B_H1","H1_DROP","H1","Train-edge-dropout pair-score consistency","candidate"),
          ("S1B_H1_CTRL","H1_PAIRSHUFFLE","H1","Compute-matched label-stratified shuffled-pair consistency","matched control")]
    return [{**common,"job_id":f"V12-S1B-{i:02d}","candidate_id":cid,"arm":arm,"innovation":innovation,
             "family":innovation if innovation!="baseline" else "baseline","definition":definition,"purpose":purpose}
            for i,(cid,arm,innovation,definition,purpose) in enumerate(rows,1)]


def build_stage1c_tasks():
    common={"stage":"stage1c","dataset":"cora","seed":0,"epochs":5,"sampler":"QTHS25",
            "priority":"P1","estimated_cost":"1 Stage-1-equivalent","status":"QUEUED",
            "gpu_mem_estimate":"under 1 GiB per process"}
    rows=[("S1C_B0","BASELINE","baseline","QTHS25 plus BCE strong reference","matched strong baseline"),
          ("S1C_X1","X1_ORTHO","X1","Orthogonalized Raw-HG pair-representation residual","candidate"),
          ("S1C_X1_RAW","X1_RAW","X1","Same-size residual MLP on unprojected Raw-HG pair representation","parameter-matched control"),
          ("S1C_X1_RANDOM","X1_RANDOM","X1","Same-size residual MLP after fixed random orthogonal rotation","random-projection control"),
          ("S1C_X1_CONCAT","X1_CONCAT","X1","Same-size residual MLP on fixed-projected Graph/Raw-HG concatenation","same-dimension concatenation control")]
    return [{**common,"job_id":f"V12-S1C-{i:02d}","candidate_id":cid,"arm":arm,"innovation":innovation,
             "family":innovation if innovation!="baseline" else "baseline","definition":definition,"purpose":purpose}
            for i,(cid,arm,innovation,definition,purpose) in enumerate(rows,1)]


def build_stage1d_tasks():
    common={"stage":"stage1d","dataset":"cora","seed":0,"epochs":5,"sampler":"QTHS25",
            "priority":"P1","estimated_cost":"1 Stage-1-equivalent","status":"QUEUED",
            "gpu_mem_estimate":"under 1 GiB per process"}
    rows=[("S1D_B0","BASELINE","baseline","QTHS25 plus BCE strong reference","matched strong baseline"),
          ("S1D_G2","G2_PERSIST","G2","EMA persistent-positive-difficulty BCE weighting","candidate"),
          ("S1D_G2_INSTANT","G2_INSTANT","G2","Current-batch positive-difficulty weighting","instantaneous-difficulty control"),
          ("S1D_G2_SHUFFLE","G2_SHUFFLED","G2","EMA difficulty under fixed positive-edge permutation","shuffled-persistence control")]
    return [{**common,"job_id":f"V12-S1D-{i:02d}","candidate_id":cid,"arm":arm,"innovation":innovation,
             "family":innovation if innovation!="baseline" else "baseline","definition":definition,"purpose":purpose}
            for i,(cid,arm,innovation,definition,purpose) in enumerate(rows,1)]


def build_stage1e_tasks():
    common={"stage":"stage1e","dataset":"cora","seed":0,"epochs":5,"sampler":"QTHS25",
            "priority":"P1","estimated_cost":"1 Stage-1-equivalent","status":"QUEUED",
            "gpu_mem_estimate":"under 1 GiB per process"}
    rows=[("S1E_B0","BASELINE","baseline","QTHS25 plus BCE strong reference","matched strong baseline"),
          ("S1E_X2","X2_CROSS","X2","Zero-initialized residual MLP on aligned Graph/Raw-HG pairwise products plus branch disagreement","candidate"),
          ("S1E_X2_SELF","X2_SELF","X2","Same-parameter residual MLP replacing cross-view product with within-view self moments","parameter-matched mechanism control")]
    return [{**common,"job_id":f"V12-S1E-{i:02d}","candidate_id":cid,"arm":arm,"innovation":innovation,
             "family":innovation if innovation!="baseline" else "baseline","definition":definition,"purpose":purpose}
            for i,(cid,arm,innovation,definition,purpose) in enumerate(rows,1)]


def build_stage1f_tasks():
    common={"stage":"stage1f","dataset":"cora","seed":0,"epochs":5,"sampler":"QTHS25",
            "priority":"P1","estimated_cost":"1 Stage-1-equivalent","status":"QUEUED",
            "gpu_mem_estimate":"under 1 GiB per process"}
    rows=[("S1F_B0","BASELINE","baseline","QTHS25 plus BCE strong reference","matched strong baseline"),
          ("S1F_B2","B2_TRIAD","B2","Zero-initialized residual-branch bilinear coactivation with degree and common-neighbor branches","candidate"),
          ("S1F_B2_SCALE","B2_SCALE","B2","Two-scalar degree/common-neighbor score calibration without cross-branch interaction","parameter-matched decoder control")]
    return [{**common,"job_id":f"V12-S1F-{i:02d}","candidate_id":cid,"arm":arm,"innovation":innovation,
             "family":innovation if innovation!="baseline" else "baseline","definition":definition,"purpose":purpose}
            for i,(cid,arm,innovation,definition,purpose) in enumerate(rows,1)]


def build_stage1g_tasks():
    common={"stage":"stage1g","dataset":"cora","seed":0,"epochs":5,"sampler":"QTHS25",
            "priority":"P1","estimated_cost":"1 Stage-1-equivalent","status":"QUEUED",
            "gpu_mem_estimate":"under 1 GiB per process"}
    rows=[("S1G_B0","BASELINE","baseline","QTHS25 plus BCE strong reference","matched strong baseline"),
          ("S1G_F3","F3_PAIRED","F3","BCE-anchored pairwise ranking against the QTHS25 negative assigned to the same training positive","candidate"),
          ("S1G_F3_SHUFFLE","F3_SHUFFLED","F3","Same pairwise term with a fixed cyclic mismatch among in-batch assigned negatives","pair-identity mechanism control")]
    return [{**common,"job_id":f"V12-S1G-{i:02d}","candidate_id":cid,"arm":arm,"innovation":innovation,
             "family":"F" if innovation=="F3" else "baseline","definition":definition,"purpose":purpose}
            for i,(cid,arm,innovation,definition,purpose) in enumerate(rows,1)]


def preflight():
    worker_init()
    import torch
    import experiment_v8 as v8
    info = v8.base.ensure_expected_runtime()
    full, view, pool, scores, pool_hash, vp, vn, valid_hash = v8.dataset_context("cora")
    if pool.shape != (len(view.train_pos), 20, 2) or scores.shape != pool.shape[:2]:
        raise RuntimeError("unexpected fixed train-pool dimensions")
    selected = v8.selected_edges({"method":"SH75","seed":0,"alpha":None}, pool, scores, view.train_pos)
    if not torch.cuda.is_available() or "V100" not in torch.cuda.get_device_name(0):
        raise RuntimeError("expected the audited Tesla V100 server")
    record = {
        "state":"PREFLIGHT_PASS", "workspace":"DCDLP-main", "dataset":"cora",
        "split_hash":v8.base.split_hash(view), "train_pool_hash":pool_hash,
        "validation_candidate_hash":valid_hash, "train_positive_count":int(len(view.train_pos)),
        "validation_positive_count":int(len(vp)), "pool_shape":list(pool.shape),
        "selected_negative_hash":v8.v61.array_hash(selected),
        "test_loaded":False, "test_enabled":False, "source_hashes":source_hashes(),
        "runtime":info, "gpu":torch.cuda.get_device_name(0),
        "gpu_total_bytes":int(torch.cuda.get_device_properties(0).total_memory),
        "cpu_count":os.cpu_count(), "worker_count":6, "completed_at_utc":utc_now(),
    }
    atomic_json(OUT / "preflight.json", record)
    return record


def decide(results):
    by = {r["arm"]:r for r in results if r.get("state") == "COMPLETE"}
    if "BASELINE" not in by:
        return {"state":"INFRASTRUCTURE_FAILURE","reason":"matched SH75+BCE baseline did not complete"}
    baseline = float(by["BASELINE"]["validation_metrics"]["mrr"])
    decisions = {}
    for cid, treatment, control in [
        ("V12-F1","F1_TOP10","F1_RANDOM10"),
        ("V12-G1","G1_CLOSURE","G1_SHUFFLED"),
        ("V12-C1","C1_PAIR","C1_SELF"),
        ("V12-D1","D1_EGO","D1_EGO_PERM"),
    ]:
        if treatment not in by or control not in by:
            decisions[cid] = {"decision":"INFRASTRUCTURE_FAILURE"}
            continue
        candidate = float(by[treatment]["validation_metrics"]["mrr"])
        matched = float(by[control]["validation_metrics"]["mrr"])
        delta = candidate - baseline
        effect = delta >= 0.003 or (baseline > 0 and delta / baseline >= 0.01)
        passed = effect and candidate > matched
        decisions[cid] = {
            "decision":"STAGE1_GO" if passed else "REJECT",
            "baseline_mrr":baseline,"candidate_mrr":candidate,
            "matched_control_mrr":matched,"delta":delta,
            "relative_delta":delta / baseline if baseline else None,
            "beats_control":candidate > matched,"effect_gate":bool(effect),
        }
    return {"state":"STAGE1_BATCH_COMPLETE","baseline_mrr":baseline,"candidates":decisions}


def write_queue(task_list, complete, failed, running):
    fields=["job_id","candidate","stage","dataset","seed","priority","estimated_cost","status",
            "gpu_mem_estimate","start_time","end_time","result"]
    lines=["\t".join(fields)]
    for task in task_list:
        job=task["job_id"]
        status="COMPLETE" if job in complete else ("FAILED" if job in failed else ("RUNNING" if job in running else "QUEUED"))
        result=failed.get(job,"experiments/"+task["candidate_id"]+"/"+task["arm"]+"/result.json" if status=="COMPLETE" else "")
        values=[job,task["candidate_id"]+":"+task["arm"],task["stage"],task["dataset"],str(task["seed"]),
                task["priority"],task["estimated_cost"],status,task["gpu_mem_estimate"],"","",result]
        lines.append("\t".join(values))
    (OUT/"EXPERIMENT_QUEUE.tsv").write_text("\n".join(lines)+"\n",encoding="utf-8")


def write_ledger(results, decision):
    import csv
    path = OUT / "EXPERIMENT_LEDGER.tsv"
    arms = {r.get("arm"): r for r in results}
    baseline = float(arms["BASELINE"]["validation_metrics"]["mrr"]) if "BASELINE" in arms else None
    controls = {"F1_TOP10":"F1_RANDOM10", "F1_RANDOM10":"F1_RANDOM10",
                "G1_CLOSURE":"G1_SHUFFLED", "G1_SHUFFLED":"G1_SHUFFLED",
                "C1_PAIR":"C1_SELF", "C1_SELF":"C1_SELF",
                "D1_EGO":"D1_EGO_PERM", "D1_EGO_PERM":"D1_EGO_PERM",
                "BASELINE":"BASELINE"}
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(["exp_id","timestamp_utc","candidate_id","family","parent_state","dataset","seed","epochs",
                         "change_summary","baseline_mrr","candidate_mrr","delta","control_mrr","params",
                         "runtime_s","peak_gpu_mb","decision","novelty_status","checkpoint_sha256","source_hashes","notes"])
        for row in results:
            arm = row.get("arm", "")
            metric = row.get("validation_metrics", {}).get("mrr")
            d = decision.get("candidates", {}).get(row.get("candidate_id", ""), {})
            control_arm = controls.get(arm)
            control_mrr = arms.get(control_arm, {}).get("validation_metrics", {}).get("mrr", "")
            writer.writerow([
                row.get("job_id",""), row.get("completed_at_utc",""), row.get("candidate_id",""),
                row.get("family",""), "clean_baseline", row.get("dataset","cora"), row.get("seed",0),
                row.get("epochs",5), row.get("definition",""), "" if baseline is None else baseline,
                "" if metric is None else metric, "" if metric is None or baseline is None else metric-baseline,
                control_mrr, row.get("trainable_parameters",""), row.get("total_wall_seconds",""),
                row.get("peak_gpu_memory_mb",""), d.get("decision",row.get("state","UNKNOWN")),
                "NOT_SEARCHED", row.get("checkpoint_sha256",""),
                json.dumps(row.get("source_hashes",{}),sort_keys=True),
                "test_evaluated=false; validation-only",
            ])

def run_batch(workers):
    OUT.mkdir(parents=True, exist_ok=True)
    pf=preflight()
    task_list=tasks()
    cache={}
    pending=[]
    complete=set()
    for task in task_list:
        result_file=OUT/"experiments"/task["candidate_id"]/task["arm"]/"result.json"
        if result_file.exists():
            try:
                prior=json.loads(result_file.read_text(encoding="utf-8"))
                if prior.get("state")=="COMPLETE":
                    cache[task["arm"]]=prior
                    complete.add(task["job_id"])
                    continue
            except Exception:
                pass
        pending.append(task)
    failed={}
    running={t["job_id"] for t in pending}
    write_queue(task_list,complete,failed,running)
    atomic_json(OUT/"status.json",{
        "state":"RUNNING","phase":"STAGE1_FIRST_BATCH","workspace":"DCDLP-main",
        "gpu":pf["gpu"],"cpu_count":pf["cpu_count"],"worker_count":workers,
        "completed":len(complete),"total":len(task_list),"test_evaluated":False,
        "started_at_utc":utc_now(),
    })
    results=list(cache.values())
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(workers,len(pending)),
                                    mp_context=mp.get_context("spawn"),
                                    initializer=worker_init) as pool:
            futures={pool.submit(run_one,t):t for t in pending}
            for future in cf.as_completed(futures):
                task=futures[future]
                running.discard(task["job_id"])
                try:
                    result=future.result()
                except Exception as exc:
                    result={**task,"state":"FAILED","error":repr(exc),"traceback":traceback.format_exc()}
                results.append(result)
                if result.get("state")=="COMPLETE":
                    complete.add(task["job_id"])
                else:
                    failed[task["job_id"]]=result.get("error","unknown failure")
                write_queue(task_list,complete,failed,running)
                atomic_json(OUT/"status.json",{
                    "state":"RUNNING","phase":"STAGE1_FIRST_BATCH","completed":len(complete),
                    "total":len(task_list),"completed_jobs":sorted(complete),"failed_jobs":failed,
                    "gpu":pf["gpu"],"worker_count":workers,"test_evaluated":False,"updated_at_utc":utc_now(),
                })
    decision=decide(results)
    write_ledger(results, decision)
    atomic_json(OUT/"results.json",{
        "status":decision["state"],"phase1_stage1":decision,"experiments":results,
        "test_evaluated":False,"source_hashes":pf["source_hashes"],"preflight":pf,
        "generated_at_utc":utc_now(),
    })
    atomic_json(OUT/"status.json",{
        "state":decision["state"],"phase":"stage1_first_batch_complete",
        "test_evaluated":False,"decisions":decision,"completed":len(complete),
        "total":len(task_list),"updated_at_utc":utc_now(),
    })
    report=[
        "# V12 First Batch Report","","State: "+decision["state"],"",
        "Cora standard, seed 0, five fixed epochs, SH75-matched training negatives, fixed-final-epoch validation MRR. Test was not loaded or evaluated.","",
        "Matched SH75+BCE baseline MRR: "+str(decision.get("baseline_mrr","NA")),"",
        "| Candidate | Decision | Candidate MRR | Delta vs baseline | Matched control MRR |",
        "|---|---|---:|---:|---:|",
    ]
    for cid,value in decision.get("candidates",{}).items():
        report.append("| "+cid+" | "+str(value.get("decision"))+" | "+str(value.get("candidate_mrr","NA"))+" | "+str(value.get("delta","NA"))+" | "+str(value.get("matched_control_mrr","NA"))+" |")
    report += ["","Stage1_GO is not a PAPER_CANDIDATE. Novelty review and Stage 2/3 are still required.",
               "This report is only the first falsification batch. If all ideas fail, derive another batch from the observed failure modes under the registered budget.",""]
    (OUT/"experiments"/"FIRST_BATCH_REPORT.md").write_text("\n".join(report),encoding="utf-8")


def build_stage2_tasks(innovations=("F1","D1"), stage="stage2"):
    common = {"stage":"stage2", "dataset":"cora", "seed":0, "epochs":10,
              "sampler":"QTHS25", "priority":"P1", "estimated_cost":"2 Stage-1-equivalents",
              "status":"QUEUED", "gpu_mem_estimate":"under 1 GiB per process"}
    rows = [("S2_B0","BASELINE","baseline","QTHS25 strong baseline", "matched strong baseline")]
    config={
        "F1":("F1_TOP10","F1_RANDOM10","Batch-top ten pairwise ranking loss","Random-ten pairwise loss control"),
        "D1":("D1_EGO","D1_EGO_PERM","Target-masked one-hop ego-context residual","Node-permuted ego-context control"),
        "F2":("F2_TOP10","F2_RANDOM10","BCE-anchored batch-hard pairwise auxiliary loss","BCE plus random-ten pairwise auxiliary control"),
        "H1":("H1_DROP","H1_PAIRSHUFFLE","Train-edge-dropout pair-score consistency","Compute-matched shuffled-pair consistency control"),
        "X1":("X1_ORTHO",("X1_RAW","X1_RANDOM","X1_CONCAT"),"Orthogonalized Raw-HG pair residual",("Unprojected residual control","Random-rotation control","Projected concatenation control")),
        "G2":("G2_PERSIST",("G2_INSTANT","G2_SHUFFLED"),"EMA persistent-positive-difficulty BCE weighting",("Instantaneous-difficulty control","Shuffled-persistence control")),
        "X2":("X2_CROSS","X2_SELF","Aligned Graph/Raw-HG bilinear pair interaction residual","Parameter-matched within-view self-moment residual control"),
        "B2":("B2_TRIAD","B2_SCALE","Residual-structural bilinear branch coactivation","Parameter-matched branch-score calibration control"),
        "F3":("F3_PAIRED","F3_SHUFFLED","BCE-anchored identity-aligned local pairwise ranking auxiliary","Fixed cyclic pair-mismatch control"),
    }
    for innovation in innovations:
        treatment,controls,definition,control_definitions=config[innovation]
        controls=(controls,) if isinstance(controls,str) else controls
        control_definitions=(control_definitions,) if isinstance(control_definitions,str) else control_definitions
        rows.append((f"S2_{innovation}",treatment,innovation,definition,"candidate"))
        for control,control_definition in zip(controls,control_definitions):
            rows.append((f"S2_{innovation}_CTRL_{control}",control,innovation,control_definition,"matched control"))
    tasks_out=[]
    for i,(candidate_id,arm,innovation,definition,purpose) in enumerate(rows,1):
        tasks_out.append({**common,"stage":stage,"job_id":f"V12-{stage.upper()}-{i:02d}","candidate_id":candidate_id,
                          "arm":arm,"innovation":innovation,"family":innovation if innovation!="baseline" else "baseline",
                          "definition":definition,"purpose":purpose})
    return tasks_out


def build_stage3_tasks(innovations):
    common = {"stage":"stage3", "dataset":"cora", "epochs":10,
              "sampler":"QTHS25", "priority":"P1", "estimated_cost":"2 Stage-1-equivalents",
              "status":"QUEUED", "gpu_mem_estimate":"under 1 GiB per process"}
    tasks_out=[]
    for seed in range(3):
        tasks_out.append({**common,"job_id":f"V12-S3-B0-s{seed}","candidate_id":f"S3_B0_s{seed}",
                          "arm":"BASELINE","innovation":"baseline","family":"baseline","seed":seed,
                          "definition":"QTHS25 strong baseline","purpose":"matched strong baseline"})
        for innovation in innovations:
            treatment,control,definition,control_definition = {
                "F1":("F1_TOP10","F1_RANDOM10","Batch-top ten pairwise ranking loss","Random-ten pairwise loss control"),
                "D1":("D1_EGO","D1_EGO_PERM","Target-masked one-hop ego-context residual","Node-permuted ego-context control"),
                "F2":("F2_TOP10","F2_RANDOM10","BCE-anchored batch-hard pairwise auxiliary loss","BCE plus random-ten pairwise auxiliary control"),
                "H1":("H1_DROP","H1_PAIRSHUFFLE","Train-edge-dropout pair-score consistency","Compute-matched shuffled-pair consistency control"),
                "X1":("X1_ORTHO",("X1_RAW","X1_RANDOM","X1_CONCAT"),"Orthogonalized Raw-HG pair residual",("Unprojected residual control","Random-rotation control","Projected concatenation control")),
                "G2":("G2_PERSIST",("G2_INSTANT","G2_SHUFFLED"),"EMA persistent-positive-difficulty BCE weighting",("Instantaneous-difficulty control","Shuffled-persistence control")),
                "X2":("X2_CROSS","X2_SELF","Aligned Graph/Raw-HG bilinear pair interaction residual","Parameter-matched within-view self-moment residual control"),
                "B2":("B2_TRIAD","B2_SCALE","Residual-structural bilinear branch coactivation","Parameter-matched branch-score calibration control"),
                "F3":("F3_PAIRED","F3_SHUFFLED","BCE-anchored identity-aligned local pairwise ranking auxiliary","Fixed cyclic pair-mismatch control"),
            }[innovation]
            controls=(controls,) if isinstance(controls,str) else controls
            control_definitions=(control_definitions,) if isinstance(control_definitions,str) else control_definitions
            tasks_out.append({**common,"job_id":f"V12-S3-{innovation}-s{seed}",
                              "candidate_id":f"S3_{innovation}_s{seed}","arm":treatment,
                              "innovation":innovation,"family":innovation,"seed":seed,
                              "definition":definition,"purpose":"candidate"})
            for control,control_definition in zip(controls,control_definitions):
                tasks_out.append({**common,"job_id":f"V12-S3-{innovation}-{control}-s{seed}",
                                  "candidate_id":f"S3_{innovation}_{control}_s{seed}","arm":control,
                                  "innovation":innovation,"family":innovation,"seed":seed,
                                  "definition":control_definition,"purpose":"matched control"})
    return tasks_out


def stage_decisions(results, innovations, stage):
    by_seed={}
    for row in results:
        if row.get("state")=="COMPLETE":
            by_seed.setdefault(int(row.get("seed",0)),{})[row.get("arm")]=row
    baseline_rows=[v["BASELINE"] for v in by_seed.values() if "BASELINE" in v]
    decisions={}
    arm_map={"F1":("F1_TOP10","F1_RANDOM10"),"D1":("D1_EGO","D1_EGO_PERM"),
             "F2":("F2_TOP10","F2_RANDOM10"),"H1":("H1_DROP","H1_PAIRSHUFFLE"),
             "X1":("X1_ORTHO",("X1_RAW","X1_RANDOM","X1_CONCAT")),
             "G2":("G2_PERSIST",("G2_INSTANT","G2_SHUFFLED")),
             "X2":("X2_CROSS","X2_SELF"),"B2":("B2_TRIAD","B2_SCALE"),
             "F3":("F3_PAIRED","F3_SHUFFLED")}
    for innovation in innovations:
        treatment,controls=arm_map[innovation]
        controls=(controls,) if isinstance(controls,str) else controls
        paired=[]
        for seed,arms in sorted(by_seed.items()):
            if treatment in arms and all(control in arms for control in controls) and "BASELINE" in arms:
                b=float(arms["BASELINE"]["validation_metrics"]["mrr"])
                c=float(arms[treatment]["validation_metrics"]["mrr"])
                control_values={control:float(arms[control]["validation_metrics"]["mrr"]) for control in controls}
                m=max(control_values.values())
                paired.append({"seed":seed,"baseline_mrr":b,"candidate_mrr":c,"matched_control_mrr":m,
                               "control_metrics":control_values,"delta":c-b,"control_delta":c-m})
        if stage in {"stage1b","stage1c","stage1d","stage1e","stage1f","stage1g","stage2","stage2b","stage2c","stage2d","stage2e","stage2f","stage2g"}:
            if not paired:
                decisions[innovation]={"decision":"INFRASTRUCTURE_FAILURE","paired":paired}
                continue
            row=paired[0]
            effect=row["delta"]>=0.003 or (row["baseline_mrr"]>0 and row["delta"]/row["baseline_mrr"]>=0.01)
            go=effect and row["candidate_mrr"]>row["baseline_mrr"] and row["candidate_mrr"]>row["matched_control_mrr"]
            go_label="STAGE1_GO" if stage in {"stage1b","stage1c","stage1d","stage1e","stage1f","stage1g"} else "STAGE2_GO"
            decisions[innovation]={"decision":go_label if go else "REJECT","paired":paired,
                                   "effect_gate":bool(effect),"strong_baseline":"QTHS25"}
        else:
            if len(paired)<3:
                decisions[innovation]={"decision":"INFRASTRUCTURE_FAILURE","paired":paired}
                continue
            gains=[p["delta"] for p in paired]
            control_gains=[p["control_delta"] for p in paired]
            wins=sum(g>0 for g in gains)
            control_wins=sum(g>0 for g in control_gains)
            go=wins>=2 and sum(gains)/len(gains)>0 and control_wins>=2 and sum(control_gains)/len(control_gains)>0
            decisions[innovation]={"decision":"LOCAL_GO" if go else "REJECT","paired":paired,
                                   "mean_gain":sum(gains)/len(gains),"wins_vs_baseline":wins,
                                   "mean_gain_vs_control":sum(control_gains)/len(control_gains),
                                   "wins_vs_control":control_wins,"strong_baseline":"QTHS25"}
    state="LOCAL_GO" if stage=="stage3" and any(v["decision"]=="LOCAL_GO" for v in decisions.values()) else (
          {"stage1b":"STAGE1B_COMPLETE","stage1c":"STAGE1C_COMPLETE","stage1d":"STAGE1D_COMPLETE","stage1e":"STAGE1E_COMPLETE","stage1f":"STAGE1F_COMPLETE","stage1g":"STAGE1G_COMPLETE"}.get(stage,"STAGE2_COMPLETE") if stage in {"stage1b","stage1c","stage1d","stage1e","stage1f","stage1g","stage2","stage2b","stage2c","stage2d","stage2e","stage2f","stage2g"} else "STAGE3_NO_GO")
    return {"state":state,"stage":stage,"decisions":decisions,
            "completed_pairs":sum(len(v.get("paired",[])) for v in decisions.values()),
            "test_evaluated":False,"updated_at_utc":utc_now()}


def run_registered_stage(stage, task_list, workers):
    OUT.mkdir(parents=True,exist_ok=True)
    pf=preflight()
    complete=set(); failed={}; pending=[]; results=[]
    for task in task_list:
        f=OUT/"experiments"/task["candidate_id"]/task["arm"]/"result.json"
        if f.exists():
            try:
                prior=json.loads(f.read_text(encoding="utf-8"))
                if prior.get("state")=="COMPLETE" and prior.get("job_id")==task["job_id"]:
                    results.append(prior); complete.add(task["job_id"]); continue
            except Exception:
                pass
        pending.append(task)
    running={t["job_id"] for t in pending}
    write_queue(task_list,complete,failed,running)
    atomic_json(OUT/"status.json",{"state":"RUNNING","phase":stage,"completed":len(complete),
                                    "total":len(task_list),"test_evaluated":False,"gpu":pf["gpu"],
                                    "worker_count":workers,"started_at_utc":utc_now()})
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(workers,len(pending)),mp_context=mp.get_context("spawn"),
                                    initializer=worker_init) as pool:
            futures={pool.submit(run_one,t):t for t in pending}
            for future in cf.as_completed(futures):
                task=futures[future]; running.discard(task["job_id"])
                try:
                    result=future.result()
                except Exception as exc:
                    result={**task,"state":"FAILED","error":repr(exc),"traceback":traceback.format_exc(),
                            "test_evaluated":False,"completed_at_utc":utc_now()}
                results.append(result)
                if result.get("state")=="COMPLETE": complete.add(task["job_id"])
                else: failed[task["job_id"]]=result.get("error","unknown failure")
                write_queue(task_list,complete,failed,running)
                atomic_json(OUT/"status.json",{"state":"RUNNING","phase":stage,"completed":len(complete),
                                                "total":len(task_list),"failed_jobs":failed,
                                                "test_evaluated":False,"gpu":pf["gpu"],"worker_count":workers,
                                                "updated_at_utc":utc_now()})
    innovations=sorted({t["innovation"] for t in task_list if t.get("innovation") not in (None,"baseline")})
    decision=stage_decisions(results,innovations,stage)
    atomic_json(OUT/f"{stage}_results.json",{"results":results,"decision":decision,"preflight":pf})
    ledger=OUT/"EXPERIMENT_LEDGER.tsv"
    import csv
    with ledger.open("r",newline="",encoding="utf-8") as stream:
        old=list(csv.DictReader(stream,delimiter="\t")); fields=list(old[0].keys()) if old else []
    seen={r.get("exp_id") for r in old}
    new=[]
    for row in results:
        if row.get("job_id") in seen: continue
        baseline=next((p["baseline_mrr"] for v in decision["decisions"].values() for p in v.get("paired",[]) if p["seed"]==row.get("seed")),None)
        metric=row.get("validation_metrics",{}).get("mrr")
        d=decision["decisions"].get(row.get("innovation"),{})
        paired=next((p for p in d.get("paired",[]) if p["seed"]==row.get("seed")),{})
        new.append({"exp_id":row.get("job_id"),"timestamp_utc":row.get("completed_at_utc"),
                    "candidate_id":row.get("candidate_id"),"family":row.get("family"),
                    "parent_state":"V12-"+row.get("stage","").upper(),"dataset":row.get("dataset"),
                    "seed":row.get("seed"),"epochs":row.get("epochs"),"change_summary":row.get("definition"),
                    "baseline_mrr":"" if baseline is None else baseline,"candidate_mrr":"" if metric is None else metric,
                    "delta":"" if metric is None or baseline is None else metric-baseline,
                    "control_mrr":paired.get("matched_control_mrr",""),"params":row.get("trainable_parameters",""),
                    "runtime_s":row.get("total_wall_seconds",""),"peak_gpu_mb":row.get("peak_gpu_memory_mb",""),
                    "decision":d.get("decision",row.get("state")),
                    "novelty_status":"CONCEPTUAL_OVERLAP" if row.get("innovation") in {"F1","D1","G1","C1"} else "NOT_SEARCHED",
                    "checkpoint_sha256":row.get("checkpoint_sha256",""),
                    "source_hashes":json.dumps(row.get("source_hashes",{}),sort_keys=True),
                    "notes":"test_evaluated=false; QTHS25 matched sampler"})
    if new:
        with ledger.open("a",newline="",encoding="utf-8") as stream:
            writer=csv.DictWriter(stream,fieldnames=fields,delimiter="\t",extrasaction="ignore")
            writer.writerows(new)
    aggregate=json.loads((OUT/"results.json").read_text(encoding="utf-8"))
    aggregate[stage]=decision
    oldids={r.get("job_id") for r in aggregate.get("experiments",[])}
    aggregate.setdefault("experiments",[]).extend(r for r in results if r.get("job_id") not in oldids)
    aggregate["test_evaluated"]=False; aggregate["updated_at_utc"]=utc_now()
    atomic_json(OUT/"results.json",aggregate)
    atomic_json(OUT/"status.json",{"state":decision["state"],"phase":stage,"completed":len(complete),
                                    "total":len(task_list),"failed_jobs":failed,"decisions":decision,
                                    "test_evaluated":False,"updated_at_utc":utc_now()})
    lines=[f"# V12 {stage.title()} report","",f"State: {decision['state']}",
           "Dataset: Cora; fixed-final-epoch MRR; QTHS25 strong sampler held constant across arms.",
           "Test was not loaded or evaluated.","", "| Candidate | Decision | Seed | Candidate MRR | Baseline MRR | Matched control |", "|---|---|---:|---:|---:|---:|"]
    for innovation,value in decision["decisions"].items():
        for p in value.get("paired",[]):
            lines.append(f"| {innovation} | {value['decision']} | {p['seed']} | {p['candidate_mrr']:.6f} | {p['baseline_mrr']:.6f} | {p['matched_control_mrr']:.6f} |")
    (OUT/f"{stage.upper()}_REPORT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return decision


def run_stage2(workers):
    return run_registered_stage("stage2",build_stage2_tasks(),workers)


def run_stage1b(workers):
    return run_registered_stage("stage1b",build_stage1b_tasks(),workers)


def run_stage1c(workers):
    return run_registered_stage("stage1c",build_stage1c_tasks(),workers)


def run_stage1d(workers):
    return run_registered_stage("stage1d",build_stage1d_tasks(),workers)


def run_stage1e(workers):
    return run_registered_stage("stage1e",build_stage1e_tasks(),workers)


def run_stage1f(workers):
    return run_registered_stage("stage1f",build_stage1f_tasks(),workers)


def run_stage1g(workers):
    return run_registered_stage("stage1g",build_stage1g_tasks(),workers)


def run_stage2b(workers):
    batch=json.loads((OUT/"stage1b_results.json").read_text(encoding="utf-8"))
    innovations=[k for k,v in batch["decision"]["decisions"].items() if v["decision"]=="STAGE1_GO"]
    if not innovations:
        return {"state":"NO_STAGE1B_GO","decisions":{}}
    return run_registered_stage("stage2b",build_stage2_tasks(innovations,stage="stage2b"),workers)


def run_stage2c(workers):
    batch=json.loads((OUT/"stage1c_results.json").read_text(encoding="utf-8"))
    innovations=[k for k,v in batch["decision"]["decisions"].items() if v["decision"]=="STAGE1_GO"]
    if not innovations: return {"state":"NO_STAGE1C_GO","decisions":{}}
    return run_registered_stage("stage2c",build_stage2_tasks(innovations,stage="stage2c"),workers)


def run_stage2d(workers):
    batch=json.loads((OUT/"stage1d_results.json").read_text(encoding="utf-8"))
    innovations=[k for k,v in batch["decision"]["decisions"].items() if v["decision"]=="STAGE1_GO"]
    if not innovations: return {"state":"NO_STAGE1D_GO","decisions":{}}
    return run_registered_stage("stage2d",build_stage2_tasks(innovations,stage="stage2d"),workers)


def run_stage2e(workers):
    batch=json.loads((OUT/"stage1e_results.json").read_text(encoding="utf-8"))
    innovations=[k for k,v in batch["decision"]["decisions"].items() if v["decision"]=="STAGE1_GO"]
    if not innovations: return {"state":"NO_STAGE1E_GO","decisions":{}}
    return run_registered_stage("stage2e",build_stage2_tasks(innovations,stage="stage2e"),workers)


def run_stage2f(workers):
    batch=json.loads((OUT/"stage1f_results.json").read_text(encoding="utf-8"))
    innovations=[k for k,v in batch["decision"]["decisions"].items() if v["decision"]=="STAGE1_GO"]
    if not innovations: return {"state":"NO_STAGE1F_GO","decisions":{}}
    return run_registered_stage("stage2f",build_stage2_tasks(innovations,stage="stage2f"),workers)


def run_stage2g(workers):
    batch=json.loads((OUT/"stage1g_results.json").read_text(encoding="utf-8"))
    innovations=[k for k,v in batch["decision"]["decisions"].items() if v["decision"]=="STAGE1_GO"]
    if not innovations: return {"state":"NO_STAGE1G_GO","decisions":{}}
    return run_registered_stage("stage2g",build_stage2_tasks(innovations,stage="stage2g"),workers)


def run_stage3(workers):
    innovations=[]
    for name in ("stage2_results.json","stage2b_results.json","stage2c_results.json","stage2d_results.json","stage2e_results.json","stage2f_results.json","stage2g_results.json"):
        path=OUT/name
        if path.exists():
            stage2=json.loads(path.read_text(encoding="utf-8"))
            innovations.extend(k for k,v in stage2["decision"]["decisions"].items() if v["decision"]=="STAGE2_GO")
    innovations=list(dict.fromkeys(innovations))
    if not innovations:
        atomic_json(OUT/"status.json",{"state":"NO_STAGE2_GO","phase":"stage2","test_evaluated":False,
                                        "updated_at_utc":utc_now()})
        return {"state":"NO_STAGE2_GO","decisions":{}}
    return run_registered_stage("stage3",build_stage3_tasks(innovations),workers)


def pilot():
    pf=preflight()
    task=tasks()[0]
    result=run_one(task)
    atomic_json(OUT/"pilot_status.json",{"preflight":pf,"result":result,"test_evaluated":False})
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--preflight",action="store_true")
    parser.add_argument("--pilot",action="store_true")
    parser.add_argument("--run-stage1",action="store_true")
    parser.add_argument("--run-stage1b",action="store_true")
    parser.add_argument("--run-stage1c",action="store_true")
    parser.add_argument("--run-stage1d",action="store_true")
    parser.add_argument("--run-stage1e",action="store_true")
    parser.add_argument("--run-stage1f",action="store_true")
    parser.add_argument("--run-stage1g",action="store_true")
    parser.add_argument("--run-stage2",action="store_true")
    parser.add_argument("--run-stage2b",action="store_true")
    parser.add_argument("--run-stage2c",action="store_true")
    parser.add_argument("--run-stage2d",action="store_true")
    parser.add_argument("--run-stage2e",action="store_true")
    parser.add_argument("--run-stage2f",action="store_true")
    parser.add_argument("--run-stage2g",action="store_true")
    parser.add_argument("--run-stage3",action="store_true")
    parser.add_argument("--workers",type=int,default=6)
    args=parser.parse_args()
    if not 1<=args.workers<=8:
        raise SystemExit("workers must be between 1 and 8")
    if args.preflight:
        print(json.dumps(preflight(),indent=2,ensure_ascii=False))
    elif args.pilot:
        print(json.dumps(pilot(),indent=2,ensure_ascii=False))
    elif args.run_stage1:
        run_batch(args.workers)
    elif args.run_stage1b:
        print(json.dumps(run_stage1b(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage1c:
        print(json.dumps(run_stage1c(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage1d:
        print(json.dumps(run_stage1d(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage1e:
        print(json.dumps(run_stage1e(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage1f:
        print(json.dumps(run_stage1f(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage1g:
        print(json.dumps(run_stage1g(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage2:
        print(json.dumps(run_stage2(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage2b:
        print(json.dumps(run_stage2b(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage2c:
        print(json.dumps(run_stage2c(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage2d:
        print(json.dumps(run_stage2d(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage2e:
        print(json.dumps(run_stage2e(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage2f:
        print(json.dumps(run_stage2f(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage2g:
        print(json.dumps(run_stage2g(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage3:
        print(json.dumps(run_stage3(args.workers),indent=2,ensure_ascii=False))
    else:
        parser.error("choose --preflight, --pilot or --run-stage1")


if __name__=="__main__":
    main()

