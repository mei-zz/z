from __future__ import annotations
import argparse, concurrent.futures, hashlib, importlib.util, json, math, os, subprocess, sys, time, traceback
from pathlib import Path

os.environ.setdefault("NHMC_RUNTIME_ROOT", "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HMC_V15/runtime")
OUT = Path(__file__).resolve().parents[1]
V16_OUT = OUT.parent / "NHMC_V16"
V16_SCRIPT = V16_OUT / "scripts" / "nhmc_stage1.py"
DATASETS = ("cora", "pubmed")
ARMS = ("B0_BASELINE", "C1_HISTOGRAM", "C2_SIZE_SHUFFLE", "C3_PARAM_MATCHED", "H1_HSPE_REAL")
# The frozen stage-1 module imports its sibling stage-0 script by module name.
# Include the frozen script directory explicitly when loading it by file path.
sys.path.insert(0, str(V16_SCRIPT.parent))
spec = importlib.util.spec_from_file_location("hspe_v17_v16_stage1", V16_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load frozen V16 code: {V16_SCRIPT}")
v16 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = v16
spec.loader.exec_module(v16)
import numpy as np
import torch
from torch import nn

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""): h.update(block)
    return h.hexdigest()

def write_json(path: Path, value: object) -> None:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    os.replace(tmp, path)

def read_json(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def _expected_keys(pairs: np.ndarray, n: int) -> np.ndarray:
    canonical = v16.stage0.canonical_pairs(np.asarray(pairs, dtype=np.int64))
    return np.asarray([v16.pair_key(p, n) for p in np.unique(canonical, axis=0)], dtype=np.int64)

def _load_cache(ds: str, split: str, pairs: np.ndarray, n: int) -> tuple[dict, dict]:
    d = V16_OUT / "experiments" / f"stage1_{ds}" / "cache" / split
    archive, meta_path, raw = d / f"{ds}_pair_features.npz", d / f"{ds}_cache.json", d / f"{ds}_native_tokens.npy"
    if not archive.is_file() or not meta_path.is_file() or not raw.is_file():
        raise RuntimeError(f"Missing frozen V16 {ds}/{split} pair-feature cache")
    meta = read_json(meta_path); archive_hash = sha256_file(archive); raw_hash = sha256_file(raw)
    if archive_hash != meta.get("pair_feature_archive_sha256") or raw_hash != meta.get("raw_tokens_sha256"):
        raise RuntimeError(f"V16 {ds}/{split} cache checksum mismatch")
    with np.load(archive, allow_pickle=False) as z: cache = {k: z[k].copy() for k in z.files}
    expected = _expected_keys(pairs, n); offsets = cache["offsets"]
    if not np.array_equal(cache["keys"], expected): raise RuntimeError(f"V16 {ds}/{split} candidate keys changed")
    if len(offsets) != len(expected)+1 or offsets[0] != 0 or offsets[-1] != len(cache["tokens_real"]):
        raise RuntimeError(f"V16 {ds}/{split} offsets invalid")
    if cache["tokens_real"].shape[1] != 6 or cache["support"].shape != (len(expected),):
        raise RuntimeError(f"V16 {ds}/{split} feature shape changed")
    if not np.isfinite(cache["tokens_real"]).all(): raise RuntimeError(f"V16 {ds}/{split} nonfinite token")
    return cache, {"archive": str(archive), "archive_sha256": archive_hash,
                   "raw_tokens": str(raw), "raw_tokens_sha256": raw_hash,
                   "pair_count": len(expected), "token_count": int(offsets[-1]), "metadata": meta}

def _source_hashes() -> dict:
    return {"v16_stage1": sha256_file(V16_SCRIPT),
            "stage0": sha256_file(Path(v16.stage0.__file__)),
            "qths_v71": sha256_file(Path(v16.base.__file__)),
            "negative_v61": sha256_file(Path(v16.v61.__file__)),
            "codns_engine": sha256_file(Path(v16.engine.__file__)),
            "dcdlp_train": sha256_file(Path(v16.ROOT)/"src"/"dcdlp"/"train.py"),
            "baseline_config": sha256_file(Path(v16.v61.BASELINE)/"H"/"config.json")}

def build_context(ds: str) -> dict:
    ds = ds.lower(); full, view = v16.base.init_dataset(ds)
    train_pos = v16.stage0.canonical_pairs(np.asarray(view.train_pos, dtype=np.int64))
    pool, pool_hash, teacher_scores, teacher_meta = v16._fixed_train_pool(ds, view)
    if teacher_scores.shape != pool.shape[:2]: raise RuntimeError(f"{ds} QTHS25 teacher shape mismatch")
    qids, qmeta = v16.v7.make_ids(pool, teacher_scores, train_pos, .25)
    selected = pool[np.arange(len(train_pos)), qids].copy()
    _, forbidden = v16.v61.make_train_forbidden(view)
    if any(v16.v61.canonical_edge(p) in forbidden for p in selected):
        raise RuntimeError(f"{ds} QTHS25 selection contains a train/message edge")
    valid_pos = v16.stage0.canonical_pairs(np.asarray(full.valid_pos, dtype=np.int64))
    valid_neg, sampling = v16.make_validation_candidates(view, valid_pos)
    valid_hash = v16.v61.array_hash(valid_neg); selected_hash = v16.v61.array_hash(selected)
    train_pairs = np.vstack((train_pos, selected)); valid_pairs = np.vstack((valid_pos, valid_neg.reshape(-1,2)))
    train_cache, train_info = _load_cache(ds, "train", train_pairs, view.num_nodes)
    valid_cache, valid_info = _load_cache(ds, "valid", valid_pairs, view.num_nodes)
    result_path = V16_OUT / "experiments" / f"stage1_{ds}" / "results.json"
    ref = read_json(result_path)
    if ref.get("state") != "COMPLETE": raise RuntimeError(f"V16 {ds} reference not complete")
    for name, row in ref.get("arms", {}).items():
        if (row.get("train_pool_hash"), row.get("selected_negative_hash"), row.get("validation_candidate_hash")) != (pool_hash, selected_hash, valid_hash):
            raise RuntimeError(f"V16 {ds}/{name} does not match current split/sampler/validation candidates")
    v16.engine.candidate_pool = pool; v16.engine.candidate_pool_hash = pool_hash
    v16.engine.validation_candidate_hash = valid_hash
    sources = _source_hashes(); old_sources = ref.get("source_hashes", {})
    strict_src = all(old_sources.get(k) == sources[v] for k,v in (
        ("stage1_script","v16_stage1"),("stage0_script","stage0"),
        ("experiment_v71","qths_v71"),("run_negative_v6_1","negative_v61")))
    audit = {"dataset": ds, "train_positive_hash": v16.v61.array_hash(train_pos),
             "train_pool_hash": pool_hash, "selected_negative_hash": selected_hash,
             "validation_positive_hash": v16.v61.array_hash(valid_pos),
             "validation_candidate_hash": valid_hash, "validation_positive_count": int(len(valid_pos)),
             "validation_negative_count_per_positive": int(valid_neg.shape[1]),
             "validation_sampling": sampling, "qths25": qmeta, "graph_teacher": teacher_meta,
             "train_cache": train_info, "validation_cache": valid_info,
             "v16_source_hashes": old_sources, "current_source_hashes": sources,
             "v16_reuse_source_hashes_equal": bool(strict_src),
             "heldout_test_identities_used": False, "test_evaluated": False}
    del full, teacher_scores
    return {"view":view,"train_pos":train_pos,"selected":selected,"pool":pool,
            "valid_pos":valid_pos,"valid_neg":valid_neg,"pool_hash":pool_hash,
            "selected_hash":selected_hash,"valid_hash":valid_hash,"train_cache":train_cache,
            "valid_cache":valid_cache,"audit":audit,"reference":ref,"teacher_meta":teacher_meta}

def _hist_features(cache: dict) -> np.ndarray:
    tok = np.asarray(cache["tokens_real"], dtype=np.float32)[:, :3]
    offs = np.asarray(cache["offsets"], dtype=np.int64); supports = cache["support"]
    out = np.zeros((len(offs)-1, 17), dtype=np.float32)
    tri = {(i,j): k for k,(i,j) in enumerate(zip(*np.triu_indices(5)))}
    for r,(lo,hi) in enumerate(zip(offs[:-1],offs[1:])):
        n = int(hi-lo)
        if n:
            part=tok[lo:hi]; a=np.rint(np.expm1((part[:,0]-part[:,1])*.5)).astype(np.int64)
            b=np.rint(np.expm1((part[:,0]+part[:,1])*.5)).astype(np.int64)
            def sb(x): return np.where(x<=2,0,np.where(x<=4,1,np.where(x<=8,2,np.where(x<=16,3,4)))).astype(np.int64)
            x,y=sb(a),sb(b); lo_bin,hi_bin=np.minimum(x,y),np.maximum(x,y)
            ids=np.fromiter((tri[(int(i),int(j))] for i,j in zip(lo_bin,hi_bin)),dtype=np.int64,count=n)
            out[r,:15]=np.bincount(ids,minlength=15).astype(np.float32)/n
        out[r,15]=math.log1p(n); out[r,16]=math.log1p(max(0.,float(supports[r])))
    return out

def _support_bin(x: int) -> int:
    return 0 if x<=0 else 1 if x==1 else 2 if x==2 else 3 if x<=4 else 4 if x<=8 else 5 if x<=16 else 6 if x<=32 else 7
def _degree_bin(x: int) -> int:
    return 0 if x<=0 else 1 if x==1 else 2 if x==2 else 3 if x<=4 else 4 if x<=8 else 5 if x<=16 else 6 if x<=32 else 7
def _sorted_multiset(a: np.ndarray) -> np.ndarray:
    return a[np.lexsort((a[:,2],a[:,1],a[:,0]))] if len(a) else a

def _size_shuffle(cache: dict, view, ds: str, seed: int, split: str) -> tuple[np.ndarray,dict]:
    keys=np.asarray(cache["keys"],dtype=np.int64); offs=np.asarray(cache["offsets"],dtype=np.int64)
    sizes=np.asarray(cache["tokens_real"],dtype=np.float32)[:,:3]; counts=np.diff(offs)
    supports=np.asarray(cache["support"],dtype=np.int64); n=int(view.num_nodes)
    pairs=np.column_stack((keys//n,keys%n)); graph=view.train_graph()
    deg=np.fromiter((graph.degree(i) for i in range(n)),dtype=np.int64,count=n)
    db1=np.fromiter((_degree_bin(int(deg[u])) for u in pairs[:,0]),dtype=np.int8,count=len(keys))
    db2=np.fromiter((_degree_bin(int(deg[v])) for v in pairs[:,1]),dtype=np.int8,count=len(keys))
    sb=np.fromiter((_support_bin(int(x)) for x in supports),dtype=np.int8,count=len(keys))
    strata={}
    for i in range(len(keys)):
        k=(int(counts[i]),int(sb[i]),int(min(db1[i],db2[i])),int(max(db1[i],db2[i])))
        strata.setdefault(k,[]).append(i)
    source=np.arange(len(keys),dtype=np.int64)
    dsid={"cora":1,"pubmed":2}[ds]; splitid={"train":1,"valid":2}[split]
    seed_used=17170000+dsid*100000+splitid*1000+int(seed); rng=np.random.default_rng(seed_used)
    eligible=0
    for k in sorted(strata):
        rows=np.asarray(strata[k],dtype=np.int64)
        if len(rows)>1:
            eligible+=len(rows); order=rng.permutation(rows); shift=int(rng.integers(1,len(order)))
            source[order]=np.roll(order,shift)
    shuffled=np.empty_like(sizes); changed=0
    for i,donor in enumerate(source):
        lo,hi=int(offs[i]),int(offs[i+1]); dlo,dhi=int(offs[donor]),int(offs[donor+1])
        if hi-lo != dhi-dlo: raise RuntimeError("Size-shuffle changed token count")
        shuffled[lo:hi]=sizes[dlo:dhi]
        if not np.array_equal(_sorted_multiset(sizes[lo:hi]),_sorted_multiset(sizes[dlo:dhi])): changed+=1
    out=np.zeros((len(shuffled),6),dtype=np.float32)
    if len(out): out[:,:3]=shuffled
    frac=changed/max(1,len(keys))
    meta={"dataset":ds,"seed":seed,"split":split,"seed_used":seed_used,
          "stratum_count":len(strata),"multi_candidate_strata":sum(len(v)>1 for v in strata.values()),
          "eligible_candidate_count":eligible,"candidate_count":len(keys),
          "informative_pair_count":changed,"informative_shuffle_fraction":float(frac),
          "shuffle_power":"ADEQUATE_SHUFFLE_POWER" if frac>=.30 else "LOW_SHUFFLE_POWER",
          "matching":"exact token count; support-count bin; sorted endpoint-degree bins; split-isolated",
          "support_bins":"0,1,2,3-4,5-8,9-16,17-32,>=33",
          "degree_bins":"0,1,2,3-4,5-8,9-16,17-32,>=33",
          "source_index_sha256":hashlib.sha256(source.tobytes()).hexdigest(),
          "size_multiset_sha256":hashlib.sha256(shuffled.tobytes()).hexdigest()}
    return out,meta

class Store:
    def __init__(self,cache,n,device):
        self.n_nodes=int(n); self.keys=torch.as_tensor(cache["keys"],dtype=torch.long,device=device)
        self.offsets=torch.as_tensor(cache["offsets"],dtype=torch.long,device=device)
        self.real=torch.as_tensor(cache["tokens_real"],dtype=torch.float32,device=device)
        self.support=torch.as_tensor(cache["support"],dtype=torch.float32,device=device); self.hist=None
    def lookup(self,pairs):
        lo=torch.minimum(pairs[:,0],pairs[:,1]); hi=torch.maximum(pairs[:,0],pairs[:,1])
        wanted=lo*self.n_nodes+hi; rows=torch.searchsorted(self.keys,wanted)
        if torch.any(rows>=len(self.keys)) or torch.any(self.keys[rows]!=wanted): raise KeyError("Pair absent from frozen cache")
        return rows

def _hist_class(ts,vs):
    from dcdlp.models.dcdlp import DCDLP as Base
    class HistDCDLP(Base):
        def __init__(self,*a,**kw):
            super().__init__(*a,**kw)
            with torch.random.fork_rng(devices=[]):
                self.hspe_hist_residual=nn.Linear(17,1)
                nn.init.zeros_(self.hspe_hist_residual.weight); nn.init.zeros_(self.hspe_hist_residual.bias)
        def forward(self,x,edge_index,pairs,remove_target_edges=True,support_edge_index=None):
            out=super().forward(x,edge_index,pairs,remove_target_edges=remove_target_edges,support_edge_index=support_edge_index)
            st=ts if self.training else vs; delta=self.hspe_hist_residual(st.hist[st.lookup(pairs)]).squeeze(-1)
            out["logit"]=out["logit"]+delta; out["nhmc_delta"]=delta; return out
    return HistDCDLP

def _model_class(arm,ts,vs):
    from dcdlp.models.dcdlp import DCDLP
    if arm=="B0_BASELINE": return DCDLP
    if arm=="C1_HISTOGRAM": return _hist_class(ts,vs)
    return v16.make_model_class("C1_NHMC_SIZE",ts,vs)

def _zero_audit(ds,view,valid_pos,ts,vs,epochs):
    from dcdlp.train import ablation_profile,edge_index_from_graph
    from dcdlp.models.dcdlp import DCDLP
    cfg=v16.make_config(ds,OUT/"experiments"/"zero_init_probe",epochs); profile=ablation_profile(cfg.ablation)
    kw=dict(input_dim=view.features.shape[1],hidden_dim=cfg.hidden_dim,branch_dim=cfg.branch_dim,
            num_layers=cfg.num_layers,dropout=cfg.dropout,backbone=cfg.backbone,
            use_interaction=profile["interaction"],active_branches=profile["active"],decoder_mode=profile["decoder"],
            cn_feature_mode=cfg.cn_feature_mode,cn_regressor=None,interaction_mode=cfg.interaction_mode,
            cn_input_schema=cfg.cn_input_schema,hypergraph_mode=cfg.hypergraph_mode,
            hypergraph_construction=cfg.hypergraph_construction,ghhr_enabled=False,
            complementarity_fusion_mode="none",fusion_gate_hidden_dim=cfg.fusion_gate_hidden_dim,
            fusion_margin_graph_threshold=cfg.fusion_margin_graph_threshold,
            fusion_margin_hypergraph_threshold=cfg.fusion_margin_hypergraph_threshold)
    def make(cls):
        return cls(kw["input_dim"],kw["hidden_dim"],kw["branch_dim"],kw["num_layers"],kw["dropout"],kw["backbone"],
                   use_interaction=kw["use_interaction"],active_branches=kw["active_branches"],decoder_mode=kw["decoder_mode"],
                   cn_feature_mode=kw["cn_feature_mode"],cn_regressor=kw["cn_regressor"],interaction_mode=kw["interaction_mode"],
                   cn_input_schema=kw["cn_input_schema"],hypergraph_mode=kw["hypergraph_mode"],
                   hypergraph_construction=kw["hypergraph_construction"],ghhr_enabled=False,
                   complementarity_fusion_mode="none",fusion_gate_hidden_dim=kw["fusion_gate_hidden_dim"],
                   fusion_margin_graph_threshold=kw["fusion_margin_graph_threshold"],
                   fusion_margin_hypergraph_threshold=kw["fusion_margin_hypergraph_threshold"]).to("cuda")
    torch.manual_seed(0);torch.cuda.manual_seed_all(0); base=make(DCDLP).eval()
    base_state=base.state_dict(); base_params=int(sum(p.numel() for p in base.parameters() if p.requires_grad))
    x=torch.as_tensor(view.features,dtype=torch.float32,device="cuda"); edge=edge_index_from_graph(view.train_graph(),torch.device("cuda"))
    pair=torch.as_tensor(valid_pos[:1],dtype=torch.long,device="cuda")
    with torch.no_grad(): base_logit=base(x,edge,pair,remove_target_edges=True)["logit"]
    audits={}
    for arm in ("C1_HISTOGRAM","H1_HSPE_REAL"):
        torch.manual_seed(0);torch.cuda.manual_seed_all(0); model=make(_model_class(arm,ts,vs)).eval()
        same=all(torch.equal(base_state[k],model.state_dict()[k]) for k in base_state)
        with torch.no_grad(): output=model(x,edge,pair,remove_target_edges=True)
        name="hspe_hist_residual" if arm=="C1_HISTOGRAM" else "nhmc_residual"
        params=list(getattr(model,name).parameters()); zero=all(int(torch.count_nonzero(p).item())==0 for p in params)
        error=float(torch.max(torch.abs(base_logit-output["logit"])).detach().cpu())
        added=int(sum(p.numel() for p in model.parameters() if p.requires_grad)-base_params)
        audits[arm]={"base_initialization_identical":bool(same),"zero_initialized_residual":bool(zero),
                     "initial_logit_max_abs_difference":error,"added_trainable_parameters":added,
                     "added_parameter_fraction":added/max(1,base_params)}
        if not same or not zero or error>2e-7: raise RuntimeError(f"{ds} {arm} zero-init mismatch: {audits[arm]}")
        del model;torch.cuda.empty_cache()
    del base;torch.cuda.empty_cache()
    audits["baseline_trainable_parameters"]=base_params;audits["parameter_cap_fraction"]=.01
    if audits["H1_HSPE_REAL"]["added_parameter_fraction"]>.01: raise RuntimeError(f"{ds} HSPE parameter cap exceeded")
    return audits

def v16_result_path(ds: str) -> Path:
    return V16_OUT / "experiments" / f"stage1_{ds}" / "results.json"

def _reuse(ctx,ds,seed,arm):
    if ds!="pubmed" or seed!=0 or arm not in {"B0_BASELINE","H1_HSPE_REAL"}: return None
    ref=ctx["reference"]; curr=ctx["audit"]["current_source_hashes"]; old=ref.get("source_hashes",{})
    keys=(("stage1_script","v16_stage1"),("stage0_script","stage0"),("experiment_v71","qths_v71"),("run_negative_v6_1","negative_v61"))
    if not all(old.get(k)==curr[v] for k,v in keys): return None
    source_arm="C1_NHMC_SIZE" if arm=="H1_HSPE_REAL" else arm; row=ref.get("arms",{}).get(source_arm)
    if not row: return None
    expected=(ctx["pool_hash"],ctx["selected_hash"],ctx["valid_hash"])
    found=(row.get("train_pool_hash"),row.get("selected_negative_hash"),row.get("validation_candidate_hash"))
    if (row.get("state")!="COMPLETE" or row.get("seed")!=0 or row.get("epochs")!=5 or
        row.get("test_evaluated") is not False or expected!=found): return None
    artifact=v16_result_path(ds).parent/f"{source_arm}.json"; ckpt=Path(row.get("checkpoint",""))
    if not artifact.is_file() or not ckpt.is_file(): return None
    out=dict(row);out.update({"arm":arm,"state":"COMPLETE","reused_from":"REUSED_FROM_V16",
        "source_arm":source_arm,"reuse_result_sha256":sha256_file(artifact),
        "reuse_checkpoint_sha256":sha256_file(ckpt),"reuse_source_hashes":old,
        "reuse_checks":{"seed":0,"epochs":5,"train_pool_hash_match":True,
            "selected_negative_hash_match":True,"validation_candidate_hash_match":True,
            "source_hash_match":True,"feature_definition":"V16 exact C1 size-only encoder" if arm=="H1_HSPE_REAL" else "V16 exact frozen baseline"}})
    return out

def _run_arm(ctx,ds,seed,arm,epochs,ts,vs,hist_cls,modes):
    from dcdlp import train as tm
    from dcdlp.train import edge_index_from_graph,score_pairs
    from dcdlp.evaluation.ranking import ranking_metrics
    from dcdlp.models.dcdlp import DCDLP as Base
    old_ep,old_out=v16.engine.EPOCHS,v16.engine.OUT;old_cls,old_train=tm.DCDLP,tm.train_model
    job=OUT/"experiments"/("stage1_5epoch" if epochs==5 else "stage2_10epoch")/ds/f"seed_{seed}"
    v16.engine.EPOCHS=int(epochs);v16.engine.OUT=job/"engine_state"
    v16.engine.candidate_pool=ctx["pool"];v16.engine.candidate_pool_hash=ctx["pool_hash"]
    v16.engine.validation_candidate_hash=ctx["valid_hash"]
    real_t,real_v=ts.real,vs.real
    if arm=="C2_SIZE_SHUFFLE":ts.real,vs.real=modes["C2"]
    elif arm=="C3_PARAM_MATCHED":ts.real,vs.real=modes["C3"]
    cls=hist_cls if arm=="C1_HISTOGRAM" else Base if arm=="B0_BASELINE" else v16.make_model_class("C1_NHMC_SIZE",ts,vs)
    captured=[]
    def cap(*a,**kw):
        model,result=old_train(*a,**kw);captured.append(model);return model,result
    tm.DCDLP=cls;tm.train_model=cap
    arm_dir=job/"arms"/arm
    try:
        torch.cuda.reset_peak_memory_stats()
        rec=v16.engine.train_one(ctx["view"],f"HSPE_V17_{arm}",int(seed),ctx["selected"],str(arm_dir),
            ctx["valid_pos"],ctx["valid_neg"],initialize_from_v6=False,dataset_name=ds,hypergraph_mode="raw")
    finally:
        tm.train_model=old_train;tm.DCDLP=old_cls;v16.engine.EPOCHS=old_ep;v16.engine.OUT=old_out;ts.real,vs.real=real_t,real_v
    if len(captured)!=1: raise RuntimeError(f"{ds} seed{seed} {arm}: expected one trained model")
    model=captured[0].eval();x=torch.as_tensor(ctx["view"].features,dtype=torch.float32,device="cuda")
    edge=edge_index_from_graph(ctx["view"].train_graph(),torch.device("cuda"));t=time.perf_counter()
    with torch.no_grad():
        pos=score_pairs(model,x,edge,ctx["valid_pos"],batch_size=8192)["logit"]
        neg=score_pairs(model,x,edge,ctx["valid_neg"].reshape(-1,2),batch_size=8192)["logit"]
    score_sec=time.perf_counter()-t;metrics=ranking_metrics(pos,neg.reshape(len(pos),ctx["valid_neg"].shape[1]))
    params=int(sum(p.numel() for p in model.parameters() if p.requires_grad));base_params=ctx["baseline_params"]
    ckpt=Path(rec.get("checkpoint",""));out={"state":"COMPLETE","dataset":ds,"seed":seed,"epochs":epochs,
        "arm":arm,"validation_only":True,"test_evaluated":False,"train_pool_hash":ctx["pool_hash"],
        "selected_negative_hash":ctx["selected_hash"],"validation_positive_hash":ctx["audit"]["validation_positive_hash"],
        "validation_candidate_hash":ctx["valid_hash"],"validation_metrics":{k:float(v) for k,v in metrics.items()
            if isinstance(v,(int,float,np.floating,np.integer))},
        "train_seconds":float(rec.get("train_seconds",0)),"wall_seconds":float(rec.get("wall_seconds",0)),
        "validation_scoring_seconds":float(score_sec),"peak_gpu_allocated_mb":float(torch.cuda.max_memory_allocated()/(1024**2)),
        "trainable_parameters":params,"added_hspe_parameters":params-base_params,
        "added_parameter_fraction":(params-base_params)/max(1,base_params),
        "checkpoint":str(ckpt),"checkpoint_sha256":sha256_file(ckpt) if ckpt.is_file() else None,
        "model_state_hash":rec.get("model_state_hash"),"source_hashes":ctx["audit"]["current_source_hashes"],
        "sampler":"V16 exact QTHS25; one fixed selected negative per train positive across epochs"}
    if arm=="C1_HISTOGRAM":
        out.update({"histogram_bins":["2","3-4","5-8","9-16",">=17"],"unordered_pair_bins":15,
                    "histogram_features":17,"residual_parameters":18,"single_linear_zero_init":True,
                    "hist_feature_hash_train":ctx["hist_train_hash"],"hist_feature_hash_validation":ctx["hist_valid_hash"]})
    if arm=="C2_SIZE_SHUFFLE":out.update({"shuffle_power_train":ctx["shuffle_train_meta"],"shuffle_power_validation":ctx["shuffle_valid_meta"]})
    if arm in {"H1_HSPE_REAL","C2_SIZE_SHUFFLE","C3_PARAM_MATCHED"}:
        out["encoder_definition"]="V16 exact C1: Linear(6,8), ReLU, mean/max pooling, log token/support counts, zero-init Linear(18,1) residual"
    if arm!="B0_BASELINE" and out["added_parameter_fraction"]>.01:raise RuntimeError(f"{ds}/{arm} exceeds 1% parameter cap")
    write_json(job/f"{arm}.json",out);del captured[:];del model;torch.cuda.empty_cache();return out

def run_one(ds:str,seed:int,epochs:int)->None:
    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS","4")))
    try: torch.set_num_interop_threads(1)
    except RuntimeError: pass
    if not torch.cuda.is_available():raise RuntimeError("CUDA unavailable")
    ctx=build_context(ds);dev=torch.device("cuda")
    ts,vs=Store(ctx["train_cache"],ctx["view"].num_nodes,dev),Store(ctx["valid_cache"],ctx["view"].num_nodes,dev)
    ht,hv=_hist_features(ctx["train_cache"]),_hist_features(ctx["valid_cache"])
    ts.hist=torch.as_tensor(ht,dtype=torch.float32,device=dev);vs.hist=torch.as_tensor(hv,dtype=torch.float32,device=dev)
    ctx["hist_train_hash"]=hashlib.sha256(ht.tobytes()).hexdigest();ctx["hist_valid_hash"]=hashlib.sha256(hv.tobytes()).hexdigest()
    c2t,ctx["shuffle_train_meta"]=_size_shuffle(ctx["train_cache"],ctx["view"],ds,seed,"train")
    c2v,ctx["shuffle_valid_meta"]=_size_shuffle(ctx["valid_cache"],ctx["view"],ds,seed,"valid")
    c2t=torch.as_tensor(c2t,dtype=torch.float32,device=dev);c2v=torch.as_tensor(c2v,dtype=torch.float32,device=dev)
    c3t=np.zeros_like(ctx["train_cache"]["tokens_real"],dtype=np.float32);c3v=np.zeros_like(ctx["valid_cache"]["tokens_real"],dtype=np.float32)
    if len(c3t):c3t[:,:3]=1.
    if len(c3v):c3v[:,:3]=1.
    modes={"C2":(c2t,c2v),"C3":(torch.as_tensor(c3t,dtype=torch.float32,device=dev),torch.as_tensor(c3v,dtype=torch.float32,device=dev))}
    hist_cls=_hist_class(ts,vs)
    zero=_zero_audit(ds,ctx["view"],ctx["valid_pos"],ts,vs,epochs)
    ctx["baseline_params"]=int(zero["baseline_trainable_parameters"])
    job=OUT/"experiments"/("stage1_5epoch" if epochs==5 else "stage2_10epoch")/ds/f"seed_{seed}"
    status=job/"status.json";write_json(status,{"state":"RUNNING","dataset":ds,"seed":seed,"epochs":epochs,
        "phase":"training_five_frozen_arms" if epochs==5 else "training_five_frozen_arms_10epoch",
        "test_evaluated":False,"current_arm":None,
        "input_audit":ctx["audit"],"zero_init_audit":zero,"shuffle_power_train":ctx["shuffle_train_meta"],
        "shuffle_power_validation":ctx["shuffle_valid_meta"],"completed_arms":[]})
    arms={}
    for arm in ARMS:
        write_json(status,{"state":"RUNNING","dataset":ds,"seed":seed,"epochs":epochs,
            "phase":"training_five_frozen_arms" if epochs==5 else "training_five_frozen_arms_10epoch",
            "test_evaluated":False,"current_arm":arm,"completed_arms":list(arms)})
        row=_reuse(ctx,ds,seed,arm) if epochs==5 else None
        if row is None:row=_run_arm(ctx,ds,seed,arm,epochs,ts,vs,hist_cls,modes)
        else:write_json(job/f"{arm}.json",row)
        arms[arm]=row
        write_json(status,{"state":"RUNNING","dataset":ds,"seed":seed,"epochs":epochs,
            "phase":"training_five_frozen_arms" if epochs==5 else "training_five_frozen_arms_10epoch",
            "test_evaluated":False,"current_arm":arm,
            "last_completed_arm":arm,"completed_arms":list(arms),"input_hashes":{
                "train_pool_hash":ctx["pool_hash"],"selected_negative_hash":ctx["selected_hash"],
                "validation_candidate_hash":ctx["valid_hash"]}})
    result={"state":"COMPLETE","dataset":ds,"seed":seed,"epochs":epochs,"validation_only":True,
        "test_evaluated":False,"arms":arms,"mrr":{k:float(v["validation_metrics"]["mrr"]) for k,v in arms.items()},
        "input_audit":ctx["audit"],"zero_init_audit":zero,"baseline_trainable_parameters":ctx["baseline_params"],
        "shuffle_power":{"train":ctx["shuffle_train_meta"],"validation":ctx["shuffle_valid_meta"]},
        "hist_feature_hashes":{"train":ctx["hist_train_hash"],"validation":ctx["hist_valid_hash"]}}
    write_json(job/"results.json",result);write_json(status,{"state":"COMPLETE","dataset":ds,"seed":seed,
        "epochs":epochs,"test_evaluated":False,"completed_arms":list(arms),"decision":"PENDING_PAIRED_SEED_AGGREGATION"})

def _gate(seeds:dict,epochs:int,adequate:bool)->dict:
    rows=[seeds[str(s)] for s in (0,1,2)];controls=("B0_BASELINE","C1_HISTOGRAM","C2_SIZE_SHUFFLE","C3_PARAM_MATCHED")
    gate={};dataset_pass=True
    for ctrl in controls:
        ds=[float(r["mrr"]["H1_HSPE_REAL"]-r["mrr"][ctrl]) for r in rows]
        mean=float(np.mean(ds));wins=int(sum(x>0 for x in ds));required=.003 if ctrl=="B0_BASELINE" else .002
        active=ctrl!="C2_SIZE_SHUFFLE" or adequate
        mean_ok=(mean>=required) if epochs==5 or ctrl=="B0_BASELINE" else (mean>required)
        passed=(wins>=2 and mean_ok) if active else None
        gate[ctrl]={"paired_deltas":ds,"mean_delta":mean,"seed_wins":wins,
                    "required_wins":2,"required_mean_delta":required,"active_gate":active,"passes":passed}
        if active and not passed:dataset_pass=False
    return {"dataset":rows[0]["dataset"],"epochs":epochs,"shuffle_adequate":adequate,
            "controls":gate,"passed":bool(dataset_pass)}

def summarize_phase(phase:str,epochs:int)->dict:
    out={}
    for ds in DATASETS:
        seeds={str(s):read_json(OUT/"experiments"/phase/ds/f"seed_{s}"/"results.json") for s in (0,1,2)}
        powers=[(float(seeds[str(s)]["shuffle_power"]["train"]["informative_shuffle_fraction"]),
                 float(seeds[str(s)]["shuffle_power"]["validation"]["informative_shuffle_fraction"])) for s in (0,1,2)]
        adequate=all(a>=.30 and b>=.30 for a,b in powers)
        gate=_gate(seeds,epochs,adequate)
        out[ds]={"seeds":seeds,"shuffle_power_by_seed":powers,"shuffle_adequate":adequate,
                 "gate":gate,"passed":gate["passed"]}
    go=all(out[d]["passed"] for d in DATASETS)
    return {"state":"COMPLETE","epochs":epochs,"datasets":out,"cross_dataset_go":go,
            "decision":"CROSS_DATASET_GO" if go else "HSPE_EARLY_REJECT"}

def _write_results(data):
    write_json(OUT/"results.json",data);write_report(data)

def write_report(data):
    lines=["# HSPE V17 — execution report","",f"**Status: {data.get('state','PREFLIGHT')}**","",
        "Candidate: HSPE; V16 origin: C1_NHMC_SIZE. Test evaluated: false.","",
        "H1 uses the exact V16 C1 size-only set encoder: Linear(6,8), ReLU, mean/max pooling, log token/support counts, and a zero-initialized Linear(18,1) residual. No overlap inputs are used.","",
        "C1 is a zero-initialized single Linear(17,1) on 15 normalized unordered size-pair histogram bins plus log token/support counts. C2 assigns complete size-token multisets within split, exact token-count, shared-support-bin, and sorted endpoint-degree-bin strata. C3 uses the H1 encoder/head with constant [1,1,1] size descriptors and real token/support counts.",""]
    def section(key,title):
        arr=[f"## {title}",""];stage=data.get(key)
        if not stage:return arr+["Pending.",""]
        arr += [f"Decision: **{stage['decision']}**.",""]
        for ds in DATASETS:
            item=stage["datasets"][ds];arr += [f"### {ds.title()}",f"Dataset gate passed: {item['passed']}; shuffle adequate: {item['shuffle_adequate']}.","",
                "| Seed | B0 | Histogram | Size-shuffle | Parameter-matched | HSPE-REAL |","|---:|---:|---:|---:|---:|---:|"]
            for s in ("0","1","2"):
                m=item["seeds"][s]["mrr"];arr.append(f"| {s} | {m['B0_BASELINE']:.6f} | {m['C1_HISTOGRAM']:.6f} | {m['C2_SIZE_SHUFFLE']:.6f} | {m['C3_PARAM_MATCHED']:.6f} | {m['H1_HSPE_REAL']:.6f} |")
            arr += ["","| Comparator | Mean H1−control | Wins | Gate |","|---|---:|---:|---|"]
            for ctrl,row in item["gate"]["controls"].items():
                state="NOT REQUIRED: LOW SHUFFLE POWER" if row["passes"] is None else "PASS" if row["passes"] else "FAIL"
                arr.append(f"| {ctrl} | {row['mean_delta']:+.6f} | {row['seed_wins']}/3 | {state} |")
            arr.append("")
        return arr
    lines+=section("stage1_5epoch","Cora/PubMed 5E × 3 seeds")
    lines+=section("stage2_10epoch","Cora/PubMed 10E × 3 seeds")
    lines += ["## Novelty and test","",f"Novelty: {data.get('novelty',{}).get('status','PENDING_BEFORE_TEST')}.",
              f"Test: {data.get('test_status','OFF')}.","","## Artifacts","",
              "Per-seed results, control deltas, shuffle audit, code/cache hashes, and reuse provenance are in `results.json` and `experiments/`. Logs are in `logs/`.",""]
    (OUT/"FINAL_REPORT.md").write_text("\n".join(lines),encoding="utf-8")

def _initial():
    return {"state":"PREFLIGHT","candidate":"HSPE","v16_origin":"C1_NHMC_SIZE promoted to preregistered candidate",
        "protocol":{"datasets":list(DATASETS),"seeds":[0,1,2],"stage1_epochs":5,"stage2_epochs":10,
            "arms":list(ARMS),"max_concurrent_jobs":4,"test_evaluated":False,"parameter_cap_fraction":.01,
            "shuffle_gate":"all seeds require >=30% changed multisets in both train and validation"},
        "input_audits":{},"stage1_5epoch":None,"stage2_10epoch":None,
        "novelty":{"status":"PENDING_BEFORE_TEST"},"test_status":"OFF","final_decision":"PENDING_5E"}

def _status(state,**kw):
    path=OUT/"diagnostics"/"stage1_5epoch_status.json";obj=read_json(path) if path.exists() else {}
    obj.update({"state":state,"updated_at":time.time(),**kw});write_json(path,obj)

def run_phase(phase,epochs,concurrency):
    tasks=[(d,s) for d in DATASETS for s in (0,1,2)];pending=list(tasks);running={};completed=[];failed=[]
    phase_file=OUT/"diagnostics"/f"{phase}_status.json";logs=OUT/"logs";logs.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env.setdefault("OMP_NUM_THREADS","4");env.setdefault("MKL_NUM_THREADS","4")
    env.setdefault("OPENBLAS_NUM_THREADS","1");env.setdefault("NUMEXPR_NUM_THREADS","1")
    def save(state):
        write_json(phase_file,{"state":state,"phase":phase,"epochs":epochs,"max_concurrent_jobs":concurrency,
            "completed_jobs":completed,"active_jobs":[{"dataset":v[1],"seed":v[2],"pid":v[0].pid} for v in running.values()],
            "failed_jobs":failed,"test_evaluated":False,"updated_at":time.time()})
    save("RUNNING")
    while pending or running:
        while pending and len(running)<concurrency and not failed:
            ds,seed=pending.pop(0);log=logs/f"{phase}_{ds}_seed{seed}.log"
            with log.open("ab",buffering=0) as stream:
                p=subprocess.Popen([sys.executable,"-u",str(Path(__file__).resolve()),"run-one",ds,str(seed),str(epochs)],
                    stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,env=env,start_new_session=True)
            running[p.pid]=(p,ds,seed,str(log));save("RUNNING")
        done=[]
        for pid,(p,ds,seed,log) in list(running.items()):
            code=p.poll()
            if code is not None:
                if code==0:completed.append({"dataset":ds,"seed":seed,"pid":pid,"log":log})
                else:failed.append({"dataset":ds,"seed":seed,"pid":pid,"exit_code":code,"log":log})
                done.append(pid)
        for pid in done:running.pop(pid,None)
        if done:save("FAILED" if failed else "RUNNING")
        if running:time.sleep(5)
        elif pending and failed:break
    if failed:save("FAILED");raise RuntimeError(f"{phase} failed: {failed}")
    save("COMPLETE");return summarize_phase(phase,epochs)

def run_all(concurrency):
    if not 2<=concurrency<=4:raise ValueError("V17 concurrency must be between 2 and 4")
    OUT.mkdir(parents=True,exist_ok=True);data=_initial();_write_results(data);_status("PREFLIGHT")
    try:
        audits={}
        for ds in DATASETS:
            ctx=build_context(ds);audits[ds]=ctx["audit"];del ctx
        data["input_audits"]=audits;data["state"]="STAGE1_5E_RUNNING";_write_results(data)
        _status("STAGE1_5E_RUNNING",max_concurrent_jobs=concurrency,planned_jobs=6,completed_jobs=[],active_jobs=[],test_evaluated=False)
        one=run_phase("stage1_5epoch",5,concurrency);data["stage1_5epoch"]=one
        data["state"]="STAGE1_5E_COMPLETE";data["final_decision"]=one["decision"];_write_results(data)
        _status("STAGE1_5E_COMPLETE",decision=one["decision"],test_evaluated=False)
        if not one["cross_dataset_go"]:
            data["state"]="HSPE_EARLY_REJECT";data["final_decision"]="HSPE_EARLY_REJECT";_write_results(data)
            _status("HSPE_EARLY_REJECT",decision=data["final_decision"],test_evaluated=False);return
        data["state"]="STAGE2_10E_RUNNING";data["final_decision"]="PENDING_10E";_write_results(data)
        _status("STAGE2_10E_RUNNING",max_concurrent_jobs=concurrency,planned_jobs=6,completed_jobs=[],active_jobs=[],test_evaluated=False)
        two=run_phase("stage2_10epoch",10,concurrency);data["stage2_10epoch"]=two
        if two["cross_dataset_go"]:
            data["state"]="HSPE_VALIDATION_CONFIRMED_AWAITING_NOVELTY";data["final_decision"]=data["state"]
            data["test_status"]="OFF_PENDING_FOCUSED_NOVELTY_SEARCH"
        else:data["state"]="HSPE_VALIDATION_REJECTED";data["final_decision"]=data["state"]
        _write_results(data);_status(data["state"],decision=data["final_decision"],test_evaluated=False)
    except Exception as e:
        data["state"]="FAILED";data["final_decision"]="FAILED";data["error"]=str(e);_write_results(data)
        _status("FAILED",error=str(e),traceback=traceback.format_exc(),test_evaluated=False);raise

def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("run-all");a.add_argument("--concurrency",type=int,default=4)
    b=sub.add_parser("run-one");b.add_argument("dataset",choices=DATASETS);b.add_argument("seed",type=int);b.add_argument("epochs",type=int)
    args=ap.parse_args()
    if args.cmd=="run-all":run_all(args.concurrency)
    else:run_one(args.dataset,args.seed,args.epochs)

if __name__=="__main__":main()
