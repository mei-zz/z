from __future__ import annotations
import csv,gzip,hashlib,json,math,time,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/"HYPERGRAPH_RESEARCH"/"HARDNESS_V7"; V61=ROOT/"HYPERGRAPH_RESEARCH"/"NEGATIVE_V6_1"
SEEDS=(0,1,2); EPOCHS=10
def jr(p): return json.loads(p.read_text(encoding="utf-8"))
def jw(p,x):
 p.parent.mkdir(parents=True,exist_ok=True); q=p.with_suffix(p.suffix+".tmp"); q.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8"); q.replace(p)
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()
def can(e):
 a,b=map(int,e); return (a,b) if a<=b else (b,a)
def pct_rows(x):
 x=np.asarray(x); o=np.argsort(x,axis=1,kind="stable"); r=np.empty_like(o,dtype=float); i=np.arange(len(x))[:,None]; r[i,o]=np.arange(x.shape[1])[None,:]; return r/max(1,x.shape[1]-1)
def pct_all(x):
 x=np.asarray(x); z=x.ravel(); o=np.argsort(z,kind="stable"); r=np.empty(len(z)); r[o]=np.arange(len(z)); return (r/max(1,len(z)-1)).reshape(x.shape)
def qs(x):
 x=np.asarray(x,float); return {k:float(v) for k,v in dict(mean=x.mean(),median=np.median(x),p90=np.quantile(x,.9),p95=np.quantile(x,.95),p99=np.quantile(x,.99),max=x.max()).items()}
def gini(x):
 x=np.sort(np.asarray(x,float)); n=len(x); return float(2*np.dot(np.arange(1,n+1),x)/(n*x.sum())-(n+1)/n) if n and x.sum() else 0.
def map_ids(c,s):
 out=np.empty(len(s),int)
 for i,row in enumerate(c):
  d={can(e):j for j,e in enumerate(row)}; k=can(s[i])
  if k not in d: raise RuntimeError(f"selected negative missing at row {i}")
  out[i]=d[k]
 return out
def graph_stats(train,nodes,pairs):
 from scipy.sparse import csr_matrix
 from scipy.sparse.csgraph import shortest_path
 e=np.asarray(train,int); r=np.r_[e[:,0],e[:,1]]; c=np.r_[e[:,1],e[:,0]]
 a=csr_matrix((np.ones(len(r),dtype=np.uint8),(r,c)),shape=(nodes,nodes)); a.data[:]=1; a.eliminate_zeros()
 deg=np.asarray(a.sum(axis=1)).ravel().astype(int); ds=shortest_path(a.astype(float),directed=False,unweighted=True)
 ns=[a.indices[a.indptr[i]:a.indptr[i+1]] for i in range(nodes)]
 p=np.asarray(pairs,int); cn=np.zeros(len(p),int); ja=np.zeros(len(p)); aa=np.zeros(len(p)); ra=np.zeros(len(p))
 for i,(u,v) in enumerate(p):
  x=np.intersect1d(ns[u],ns[v],assume_unique=True); k=len(x); cn[i]=k; un=deg[u]+deg[v]-k; ja[i]=k/un if un else 0.
  if k:
   d=deg[x]; aa[i]=sum(1/math.log(int(t)) for t in d if t>1); ra[i]=sum(1/int(t) for t in d if t>0)
 dd=ds[p[:,0],p[:,1]]; sp=np.array(["disconnected" if not np.isfinite(x) else "1" if x<=1 else str(int(x)) if x<5 else ">=5" for x in dd],object)
 order=np.lexsort((np.arange(nodes),-deg)); hub=np.zeros(nodes,bool); hub[order[:math.ceil(.1*nodes)]]=True
 return deg,cn,ja,aa,ra,sp,hub
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for x in ("A_QTHS","B_CBHS","C_STHD"): (OUT/x).mkdir(exist_ok=True)
 m=jr(V61/"strict_pool_metadata.json"); st=jr(V61/"training_state.json"); v=jr(V61/"validation_results.json")
 with np.load(V61/"strict_train_candidates_and_selections.npz",allow_pickle=False) as z: ar={k:z[k].copy() for k in z.files}
 c=ar["negative_candidates"]; pos=ar["train_positive"]; sc=ar["score_graph"]; n=int(m["num_nodes"])
 if c.shape!=(4488,20,2) or sc.shape!=(4488,20): raise RuntimeError("frozen candidate shape mismatch")
 sys.path.insert(0,str(V61)); import run_negative_v6_1 as v61
 ph=v61.array_hash(c); th=v61.array_hash(pos); expected="aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455"
 if ph!=m["candidate_pool_hash"] or th!=m["train_positive_hash"] or st.get("pool_hash")!=ph or st.get("split_hash_train_only")!=m["train_only_split_hash"]: raise RuntimeError("V6.1 split/pool hash audit failed")
 if v["validation_candidate_hash"]!=expected or m["prepool_multiplier"]!=2 or m["realized_veto_count_per_positive"]!=1: raise RuntimeError("V6.1 validation/veto metadata mismatch")
 run_audit={}; vb=v["strict"]["by_method_seed"]
 for method,prefix in (("A1","S_A1_seed"),("A3","S_A3_seed")):
  for seed in SEEDS:
   key=f"S_{method}_seed{seed}"; rec=st["training_runs"][key]; sel=ar[prefix+str(seed)]; vr=vb[method][str(seed)]
   if v61.array_hash(sel)!=rec["selected_negative_hash"] or vr["checkpoint_rule"]!="fixed_final_epoch_10" or vr["candidate_hash"]!=expected: raise RuntimeError(f"{key} provenance mismatch")
   cp=Path(rec["checkpoint"])
   if not cp.exists(): raise RuntimeError(f"missing checkpoint for {key}")
   run_audit[key]={"selected_negative_hash":rec["selected_negative_hash"],"checkpoint":str(cp),"checkpoint_file_sha256":sha(cp),"validation_mrr":vr["mrr"],"checkpoint_rule":vr["checkpoint_rule"],"validation_candidate_hash":vr["candidate_hash"]}
 local=pct_rows(sc); glob=pct_all(sc); selected_all=np.concatenate([ar[f"S_{m}_seed{s}"] for m in ("A1","A3") for s in SEEDS])
 deg,cn,ja,aa,ra,sp,hub=graph_stats(pos,n,selected_all); per={}; records=[]; offset=0
 for method,prefix in (("A1","S_A1_seed"),("A3","S_A3_seed")):
  for seed in SEEDS:
   sel=ar[prefix+str(seed)]; k=len(sel); ix=map_ids(c,sel); rr=np.arange(k); rg=local[rr,ix]; gg=glob[rr,ix]; raw=sc[rr,ix]; du=deg[sel[:,0]]; dv=deg[sel[:,1]]
   pc={}
   for e in sel:
    z=can(e); pc[z]=pc.get(z,0)+1
   ec=np.bincount(sel.ravel(),minlength=n); used=ec[ec>0]; slots=2*k; top1=np.argsort(ec,kind="stable")[-max(1,math.ceil(.01*n)):]; top10=np.argsort(ec,kind="stable")[-max(1,math.ceil(.1*n)):]
   cn0,ja0,aa0,ra0,sp0=cn[offset:offset+k],ja[offset:offset+k],aa[offset:offset+k],ra[offset:offset+k],sp[offset:offset+k]; offset+=k
   sm={"n_selected":k,"Rg_per_positive":qs(rg),"Rg_global_pool":qs(gg),"Graph_raw_score":qs(raw),
    "extreme_hard_Rg_ge_0.95":float(np.mean(rg>=.95)),"ultra_hard_Rg_ge_0.99":float(np.mean(rg>=.99)),
    "local_top1pct":float(np.mean(rg>=.99)),"local_top5pct":float(np.mean(rg>=.95)),"local_top10pct":float(np.mean(rg>=.90)),
    "global_top1pct":float(np.mean(gg>=.99)),"global_top5pct":float(np.mean(gg>=.95)),"global_top10pct":float(np.mean(gg>=.90)),
    "unique_pair_count":len(pc),"unique_pair_ratio":len(pc)/k,"unique_endpoint_count":int(np.count_nonzero(ec)),"unique_endpoint_ratio":float(np.count_nonzero(ec)/slots),
    "endpoint_gini_all_nodes":gini(ec),"endpoint_gini_used_nodes_only":gini(used),"max_endpoint_frequency":int(ec.max()),
    "top1pct_endpoint_coverage":float(ec[top1].sum()/slots),"top10pct_endpoint_contribution":float(ec[top10].sum()/slots),
    "hub_endpoint_ratio":float(np.mean(hub[sel])),"pair_reuse_count_max":max(pc.values()),"pair_reused_occurrences":int(sum(q for q in pc.values() if q>1)),
    "per_positive_unique_across_10_epochs_mean":1.0,"adjacent_epoch_pair_overlap_jaccard":[1.0]*9,"selection_is_static_across_epochs":True,
    "degree_u":qs(du),"degree_v":qs(dv),"degree_product":qs(du.astype(float)*dv),"common_neighbors":qs(cn0),"jaccard":qs(ja0),"adamic_adar":qs(aa0),"resource_allocation":qs(ra0),
    "shortest_path_bucket_counts":{b:int(np.sum(sp0==b)) for b in ("1","2","3","4",">=5","disconnected")}}
   per[f"{method}_seed{seed}"]=sm
   for epoch in range(1,EPOCHS+1):
    for i,(u,w) in enumerate(sel):
     records.append({"method":method,"seed":seed,"epoch":epoch,"positive_row":i,"u":int(u),"v":int(w),"Rg_per_positive":float(rg[i]),"Rg_global_pool":float(gg[i]),"graph_raw_score":float(raw[i]),
      "degree_u":int(du[i]),"degree_v":int(dv[i]),"degree_product":int(du[i]*dv[i]),"common_neighbors":int(cn0[i]),"jaccard":float(ja0[i]),"adamic_adar":float(aa0[i]),"resource_allocation":float(ra0[i]),"shortest_path_bucket":str(sp0[i]),
      "pair_reuse_count":int(pc[can((u,w))]),"endpoint_reuse_count_u":int(ec[u]),"endpoint_reuse_count_v":int(ec[w])})
 with gzip.open(OUT/"A_QTHS"/"A1_A3_selected_negative_statistics.csv.gz","wt",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=list(records[0])); w.writeheader(); w.writerows(records)
 agg={}
 for method in ("A1","A3"):
  z=[per[f"{method}_seed{s}"] for s in SEEDS]; h={}
  for key in ("Rg_per_positive","Rg_global_pool","Graph_raw_score"): h[key]={q:float(np.mean([x[key][q] for x in z])) for q in z[0][key]}
  for key in ("extreme_hard_Rg_ge_0.95","ultra_hard_Rg_ge_0.99","local_top1pct","local_top5pct","local_top10pct","global_top1pct","global_top5pct","global_top10pct"): h[key]=float(np.mean([x[key] for x in z]))
  dkeys=("unique_pair_ratio","unique_endpoint_ratio","endpoint_gini_all_nodes","endpoint_gini_used_nodes_only","max_endpoint_frequency","top1pct_endpoint_coverage","top10pct_endpoint_contribution","hub_endpoint_ratio","pair_reuse_count_max","pair_reused_occurrences")
  agg[method]={"hardness":h,"diversity":{q:float(np.mean([x[q] for x in z])) for q in dkeys}}
  for key in ("degree_u","degree_v","degree_product","common_neighbors","jaccard","adamic_adar","resource_allocation"): agg[method][key]={q:float(np.mean([x[key][q] for x in z])) for q in z[0][key]}
 a1,a3=agg["A1"],agg["A3"]; ex=a1["hardness"]["extreme_hard_Rg_ge_0.95"]-a3["hardness"]["extreme_hard_Rg_ge_0.95"]
 ud=abs(a3["diversity"]["unique_endpoint_ratio"]-a1["diversity"]["unique_endpoint_ratio"])/max(a1["diversity"]["unique_endpoint_ratio"],1e-12)
 gd=a1["diversity"]["endpoint_gini_all_nodes"]-a3["diversity"]["endpoint_gini_all_nodes"]; ug=(a3["diversity"]["unique_endpoint_ratio"]-a1["diversity"]["unique_endpoint_ratio"])/max(a1["diversity"]["unique_endpoint_ratio"],1e-12); hd=a1["diversity"]["hub_endpoint_ratio"]-a3["diversity"]["hub_endpoint_ratio"]
 h1raw=ex>=.10; h1=h1raw and ud<.05; h2=gd>=.01 or ug>=.10 or hd>=.05; both=h1raw and h2; means=v["strict"]["mean_mrr"]
 result={"status":"ANALYSIS_COMPLETE","control_reproduced":means["A3"]>means["A1"],"A1_mean_validation":means["A1"],"A3_mean_validation":means["A3"],"winning_control_delta":means["A3"]-means["A1"],
  "primary_diagnostic":"BOTH" if both else "HARDNESS_SHIFT" if h1 else "DIVERSITY_SHIFT" if h2 else "NONE","H1_RAW_EXTREME_HARDNESS_SIGNAL":bool(h1raw),"H1_ISOLATED_HARDNESS_SHIFT":bool(h1),"H2_DIVERSITY_SHIFT":bool(h2),
  "diagnostic_components":{"extreme_hard_absolute_drop":float(ex),"unique_endpoint_relative_difference":float(ud),"endpoint_gini_absolute_drop":float(gd),"unique_endpoint_relative_gain":float(ug),"hub_endpoint_ratio_absolute_drop":float(hd)},
  "validation_candidate_hash":expected,"candidate_pool_hash":ph,"train_only_split_hash":m["train_only_split_hash"],"teacher_hashes":{q:x["checkpoint_hash"] for q,x in m["teacher_records"].items()},
  "A1_A3_run_audit":run_audit,"per_run_statistics":per,"aggregated":agg,"selected_stats_file":str(OUT/"A_QTHS"/"A1_A3_selected_negative_statistics.csv.gz"),
  "veto_ratio_audit":{"nominal":m["veto_ratio_nominal"],"prepool_size":m["prepool_multiplier"],"veto_count_per_positive":m["realized_veto_count_per_positive"],"realized_fraction_of_prepool":m["realized_veto_fraction_of_prepool"],
   "QTHS_quantile_rounding_note":"With K=1 and a top-2 prepool, alpha=.25 is non-integral per positive. QTHS applies alpha over candidate occurrences by deterministic rounding across rows: trim the top candidate in half of rows, keep both in the rest, then select the hardest survivor. This matches the shuffled control's effective selected-rank mixture while using train-only identities."}}
 jw(OUT/"results.json",result)
 (OUT/"00_V61_CONTROL_AUDIT.md").write_text("# V6.1 A1/A3 strict control audit\n\n"+f"- Reproduced: {result['control_reproduced']}; fixed epoch 10 validation A1={means['A1']:.6f}, A3={means['A3']:.6f}, delta={means['A3']-means['A1']:+.6f}.\n- Split hash: {m['train_only_split_hash']}; pool hash: {ph}; validation candidate hash: {expected}.\n- Teacher state hashes: Graph {m['teacher_records']['Graph']['checkpoint_hash']}; Raw-HG {m['teacher_records']['Raw-HG']['checkpoint_hash']}.\n- All six selection hashes match V6.1 state. Checkpoint file hashes are recorded in results.json. Sampler uses only frozen train positives and the 20-candidate pool.\n"+f"- V6.1 nominal veto={m['veto_ratio_nominal']:.2f}, but it removes 1 of 2 candidates per positive (50% realized prepool trim); this is recorded for QTHS calibration.\n",encoding="utf-8")
 lines=["# Hardness distribution: A1 vs A3\n","Rg_per_positive is the rank percentile among the same positive's 20 train-only candidates; Rg_global_pool is the percentile among all 89,760 candidate occurrences. Top-1/5/10% are reported on both scales. Statistics are repeated for each epoch because V6.1 selections are static.","\n| Method | Mean Rg | Median | P90 | P95 | P99 | Max | Extreme >=.95 | Ultra >=.99 | local top 1/5/10% | global top 1/5/10% |","|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|"]
 for method in ("A1","A3"):
  q=agg[method]["hardness"]["Rg_per_positive"]; z=agg[method]["hardness"]
  lines.append(f"| {method} | {q['mean']:.6f} | {q['median']:.6f} | {q['p90']:.6f} | {q['p95']:.6f} | {q['p99']:.6f} | {q['max']:.6f} | {z['extreme_hard_Rg_ge_0.95']:.2%} | {z['ultra_hard_Rg_ge_0.99']:.2%} | {z['local_top1pct']:.2%}/{z['local_top5pct']:.2%}/{z['local_top10pct']:.2%} | {z['global_top1pct']:.2%}/{z['global_top5pct']:.2%}/{z['global_top10pct']:.2%} |")
 lines.append("\nGraph raw-score quantiles and per-seed values are in results.json; epoch-level rows are in A_QTHS/A1_A3_selected_negative_statistics.csv.gz.")
 (OUT/"01_HARDNESS_DISTRIBUTION.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 lines=["# Diversity analysis: A1 vs A3\n","Endpoint Gini includes all Cora nodes, including unused nodes. Hub endpoints are exactly the top 10% of nodes by train-graph degree, ties broken by node ID.","\n| Method | unique pair ratio | unique endpoint ratio | Gini | max endpoint frequency | top-1% coverage | top-10% contribution | hub endpoint ratio | pair reuse max |","|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
 for method in ("A1","A3"):
  z=agg[method]["diversity"]; lines.append(f"| {method} | {z['unique_pair_ratio']:.3%} | {z['unique_endpoint_ratio']:.3%} | {z['endpoint_gini_all_nodes']:.6f} | {z['max_endpoint_frequency']} | {z['top1pct_endpoint_coverage']:.3%} | {z['top10pct_endpoint_contribution']:.3%} | {z['hub_endpoint_ratio']:.3%} | {z['pair_reuse_count_max']} |")
 lines.extend(["",f"- H1 raw extreme-hardness signal: {'present' if h1raw else 'absent'}; isolated H1 condition (unique-endpoint difference <5%): {h1}; extreme-hard decrease {ex:.2%}; unique-endpoint difference {ud:.2%}.",f"- H2: {'DIVERSITY_SHIFT' if h2 else 'not triggered'}; thresholds Gini drop >=.01, unique endpoint gain >=10%, or hub ratio drop >=5pp.","- Adjacent-epoch overlap is 1.0 and per-positive distinct negatives across epochs is 1.0 because the historical V6.1 sampler was static."])
 (OUT/"02_DIVERSITY_ANALYSIS.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 jw(OUT/"status.json",{"state":"RUNNING","phase":"analysis_complete","control_reproduced":result["control_reproduced"],"primary_diagnostic":result["primary_diagnostic"],"updated_at":time.strftime("%Y-%m-%dT%H:%M:%S%z")})
 print(json.dumps({k:result[k] for k in ("status","control_reproduced","A1_mean_validation","A3_mean_validation","primary_diagnostic","diagnostic_components")},indent=2))
if __name__=="__main__": main()
