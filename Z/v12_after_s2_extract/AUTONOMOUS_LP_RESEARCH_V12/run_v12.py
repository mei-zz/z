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
NODE_PERMUTATION = None
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
        return out

    def forward1(self, x, edge_index, pairs, remove_target_edges=True, support_edge_index=None):
        global LAST_PAIRS
        out = forward0(self, x, edge_index, pairs,
                       remove_target_edges=remove_target_edges,
                       support_edge_index=support_edge_index)
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
    NODE_PERMUTATION = np.random.default_rng(810331).permutation(view.num_nodes)
    sampler = task.get("sampler", "SH75")
    selected = v8.selected_edges({"method": sampler, "seed": seed, "alpha": None}, pool, scores, view.train_pos)
    if selected.shape != (len(view.train_pos), 2):
        raise RuntimeError("SH75 sample shape mismatch")
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


def build_stage2_tasks():
    common = {"stage":"stage2", "dataset":"cora", "seed":0, "epochs":10,
              "sampler":"QTHS25", "priority":"P1", "estimated_cost":"2 Stage-1-equivalents",
              "status":"QUEUED", "gpu_mem_estimate":"under 1 GiB per process"}
    rows = [("S2_B0","BASELINE","baseline","QTHS25 strong baseline", "matched strong baseline")]
    for innovation, treatment, control, definition, control_definition in [
        ("F1","F1_TOP10","F1_RANDOM10","Batch-top ten pairwise ranking loss","Random-ten pairwise loss control"),
        ("D1","D1_EGO","D1_EGO_PERM","Target-masked one-hop ego-context residual","Node-permuted ego-context control"),
    ]:
        rows.extend([
            (f"S2_{innovation}",treatment,innovation,definition,"candidate"),
            (f"S2_{innovation}_CTRL",control,innovation,control_definition,"matched control"),
        ])
    tasks_out=[]
    for i,(candidate_id,arm,innovation,definition,purpose) in enumerate(rows,1):
        tasks_out.append({**common,"job_id":f"V12-S2-{i:02d}","candidate_id":candidate_id,
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
            }[innovation]
            tasks_out.append({**common,"job_id":f"V12-S3-{innovation}-s{seed}",
                              "candidate_id":f"S3_{innovation}_s{seed}","arm":treatment,
                              "innovation":innovation,"family":innovation,"seed":seed,
                              "definition":definition,"purpose":"candidate"})
            tasks_out.append({**common,"job_id":f"V12-S3-{innovation}-CTRL-s{seed}",
                              "candidate_id":f"S3_{innovation}_CTRL_s{seed}","arm":control,
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
    for innovation in innovations:
        treatment,control={"F1":("F1_TOP10","F1_RANDOM10"),"D1":("D1_EGO","D1_EGO_PERM")}[innovation]
        paired=[]
        for seed,arms in sorted(by_seed.items()):
            if treatment in arms and control in arms and "BASELINE" in arms:
                b=float(arms["BASELINE"]["validation_metrics"]["mrr"])
                c=float(arms[treatment]["validation_metrics"]["mrr"])
                m=float(arms[control]["validation_metrics"]["mrr"])
                paired.append({"seed":seed,"baseline_mrr":b,"candidate_mrr":c,"matched_control_mrr":m,
                               "delta":c-b,"control_delta":c-m})
        if stage=="stage2":
            if not paired:
                decisions[innovation]={"decision":"INFRASTRUCTURE_FAILURE","paired":paired}
                continue
            row=paired[0]
            effect=row["delta"]>=0.003 or (row["baseline_mrr"]>0 and row["delta"]/row["baseline_mrr"]>=0.01)
            go=effect and row["candidate_mrr"]>row["baseline_mrr"] and row["candidate_mrr"]>row["matched_control_mrr"]
            decisions[innovation]={"decision":"STAGE2_GO" if go else "REJECT","paired":paired,
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
          "STAGE2_COMPLETE" if stage=="stage2" else "STAGE3_NO_GO")
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
                    "decision":d.get("decision",row.get("state")),"novelty_status":"CONCEPTUAL_OVERLAP",
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


def run_stage3(workers):
    stage2=json.loads((OUT/"stage2_results.json").read_text(encoding="utf-8"))
    innovations=[k for k,v in stage2["decision"]["decisions"].items() if v["decision"]=="STAGE2_GO"]
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
    parser.add_argument("--run-stage2",action="store_true")
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
    elif args.run_stage2:
        print(json.dumps(run_stage2(args.workers),indent=2,ensure_ascii=False))
    elif args.run_stage3:
        print(json.dumps(run_stage3(args.workers),indent=2,ensure_ascii=False))
    else:
        parser.error("choose --preflight, --pilot or --run-stage1")


if __name__=="__main__":
    main()

