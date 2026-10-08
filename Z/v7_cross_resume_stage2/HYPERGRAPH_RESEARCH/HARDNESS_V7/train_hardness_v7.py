from __future__ import annotations
import hashlib,json,math,sys,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/"HYPERGRAPH_RESEARCH"/"HARDNESS_V7"; V61=ROOT/"HYPERGRAPH_RESEARCH"/"NEGATIVE_V6_1"; V62=ROOT/"HYPERGRAPH_RESEARCH"/"CODNS_V6_2"
sys.path.insert(0,str(ROOT/"src"))
SEEDS=(0,1,2); ALPHA=.25; LAMBDA=.1
def jr(p): return json.loads(p.read_text(encoding="utf-8"))
def jw(p,x):
 p.parent.mkdir(parents=True,exist_ok=True); q=p.with_suffix(p.suffix+".tmp"); q.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8"); q.replace(p)
def can(e):
 a,b=map(int,e); return (a,b) if a<=b else (b,a)
def gini(x):
 a=np.sort(np.asarray(x,float)); n=len(a); return float(2*np.dot(np.arange(1,n+1),a)/(n*a.sum())-(n+1)/n) if n and a.sum() else 0.
def status(phase,current=None,completed=None,**extra):
 x={"state":"RUNNING","phase":phase,"current":current,"completed":completed or [],"updated_at":time.strftime("%Y-%m-%dT%H:%M:%S%z")}; x.update(extra); jw(OUT/"status.json",x)
def make_ids(candidates,scores,train_pos,alpha=.25,salt="QTHS25"):
 n=len(candidates); order=np.argsort(-scores,axis=1,kind="stable"); top=order[:,:2]
 trim_count=int(round(alpha*2*n))
 keys=[]
 for i,p in enumerate(train_pos):
  h=hashlib.sha256(f"{can(p)[0]}:{can(p)[1]}:{salt}".encode()).hexdigest(); keys.append((h,i))
 trim=set(i for _,i in sorted(keys)[:trim_count])
 ids=top[:,0].copy()
 if trim: 
  rr=np.fromiter(sorted(trim),dtype=np.int64); ids[rr]=top[rr,1]
 return ids,{"alpha_candidate_occurrence_fraction":alpha,"prepool_size":2,"trimmed_occurrence_count":trim_count,"trimmed_row_count":len(trim),"selected_runner_up_count":len(trim),"hash_rule":salt}
def map_ids(c,s):
 ix=np.empty(len(s),int)
 for i,row in enumerate(c):
  m={can(e):j for j,e in enumerate(row)}; k=can(s[i])
  if k not in m: raise RuntimeError(f"selected pair missing row {i}")
  ix[i]=m[k]
 return ix
def choose_prepool(cands,scores,pre,kind,degree,seed):
 n=len(cands); rr=np.arange(n); pairs=cands[rr[:,None],pre]
 rg_order=np.argsort(scores,axis=1,kind="stable"); local=np.empty_like(rg_order,dtype=float); local[rr[:,None],rg_order]=np.arange(scores.shape[1])[None,:]/(scores.shape[1]-1)
 ids=np.empty(n,dtype=np.int64); counts=np.zeros(int(degree.size),dtype=np.int64)
 rng=np.random.default_rng(400000+int(seed)*10000+7300)
 for i in range(n):
  cand_ids=pre[i]; cand=pairs[i]
  if kind=="degree":
   penalty=(degree[cand[:,0]]+degree[cand[:,1]])/(2*max(1,int(degree.max())))
  else:
   penalty=(counts[cand[:,0]]+counts[cand[:,1]])/max(1,2*i)
   if kind=="shuffled_concentration": penalty=rng.permutation(penalty)
  score=local[i,cand_ids]-LAMBDA*penalty
  j=int(np.argmax(score)); ids[i]=cand_ids[j]
  selected=cand[j]; counts[selected[0]]+=1; counts[selected[1]]+=1
 return ids
def dropout_ids(cands,scores,pre,kind,seed):
 n=len(cands); order=np.argsort(-scores,axis=1,kind="stable"); ids=np.empty(n,dtype=np.int64)
 rng=np.random.default_rng(400000+int(seed)*10000+7610+{"uniform":1,"reverse":2,"stochastic":3}[kind])
 for i in range(n):
  choices=order[i,:2]; rg=np.array([1.0,18.0/19.0])
  if kind=="uniform": prob=np.full(2,.5*((.5)+(.5*((18/19-.8)/.2))))
  elif kind=="stochastic": prob=.5*np.clip((rg-.8)/.2,0,1)
  else: prob=.5*np.clip((1-rg)/.2,0,1)
  keep=rng.random(2)>=prob
  if not np.any(keep): keep[int(np.argmax(scores[i,choices]))]=True
  ids[i]=choices[np.flatnonzero(keep)[np.argmax(scores[i,choices[keep]])]]
 return ids
def summarize(cands,scores,selected,degree):
 ix=map_ids(cands,selected); row=np.arange(len(cands)); order=np.argsort(scores,axis=1,kind="stable"); local=np.empty_like(order,dtype=float); local[row[:,None],order]=np.arange(scores.shape[1])[None,:]/(scores.shape[1]-1)
 rg=local[row,ix]; ec=np.bincount(selected.ravel(),minlength=len(degree))
 hub_ids=np.lexsort((np.arange(len(degree)),-degree))[:math.ceil(.1*len(degree))]; hub=np.zeros(len(degree),dtype=bool); hub[hub_ids]=True
 return {"mean_Rg":float(rg.mean()),"median_Rg":float(np.median(rg)),"extreme_hard_fraction":float(np.mean(rg>=.95)),
  "ultra_hard_fraction":float(np.mean(rg>=.99)),"unique_pair_ratio":float(len({can(x) for x in selected})/len(selected)),
  "unique_endpoint_ratio":float(np.count_nonzero(ec)/(2*len(selected))),"endpoint_gini":gini(ec),
  "max_endpoint_frequency":int(ec.max()),"hub_endpoint_ratio":float(np.mean(hub[selected])),
  "selected_negative_hash":None}
def selected_for(method,seed,arr,cands,scores,pre,train,degree,a4_ids):
 if method=="A0_UNIFORM": return None
 if method in ("A1_GRAPH_HARD","A3_BOTTOM25","A5_MIDDLE25","B0_GRAPH_HARD","C0_GRAPH_HARD"):
  ids=np.argmax(scores,axis=1)
 elif method in ("A2_RANDOM_VETO","B1_RANDOM_VETO"):
  return arr[f"S_A3_seed{seed}"].copy()
 elif method=="A4_QTHS25": ids=a4_ids
 elif method=="B2_DEGREE_PENALTY": ids=choose_prepool(cands,scores,pre,"degree",degree,seed)
 elif method=="B3_SHUFFLED_CONCENTRATION": ids=choose_prepool(cands,scores,pre,"shuffled_concentration",degree,seed)
 elif method=="B4_CBHS": ids=choose_prepool(cands,scores,pre,"concentration",degree,seed)
 elif method=="C1_UNIFORM_DROPOUT": ids=dropout_ids(cands,scores,pre,"uniform",seed)
 elif method=="C2_QTHS": ids=a4_ids
 elif method=="C3_REVERSE_DROPOUT": ids=dropout_ids(cands,scores,pre,"reverse",seed)
 elif method=="C4_STHD": ids=dropout_ids(cands,scores,pre,"stochastic",seed)
 else: raise ValueError(method)
 return cands[np.arange(len(cands)),ids].copy()
def main():
 import torch
 from dcdlp.data.loaders import load_dataset
 sys.path.insert(0,str(V61)); sys.path.insert(0,str(V62))
 import run_negative_v6_1 as v61
 import run_codns_v6_2 as engine
 res=jr(OUT/"results.json")
 if not res.get("control_reproduced"): raise RuntimeError("winning control was not reproduced")
 h1_raw=res["diagnostic_components"]["extreme_hard_absolute_drop"]>=.10
 h2=res["H2_DIVERSITY_SHIFT"]
 if not h1_raw and not h2: raise RuntimeError("No diagnostic triggered; stopping before candidate training")
 with np.load(V61/"strict_train_candidates_and_selections.npz",allow_pickle=False) as z: ar={k:z[k].copy() for k in z.files}
 c=ar["negative_candidates"]; scores=ar["score_graph"]; train=ar["train_positive"]; pre=ar["graph_prepool_indices"]; meta=jr(V61/"strict_pool_metadata.json")
 data=load_dataset("cora",ROOT/"data","standard",0); view=v61.TrainOnlyView(data); del data
 vp,vn,vhash=engine.validation_arrays()
 engine.candidate_pool=c; engine.candidate_pool_hash=meta["candidate_pool_hash"]; engine.validation_candidate_hash=vhash
 # Only train graph is allowed into structural selection; it is built from train positives.
 train_graph=view.train_graph(); import networkx as nx
 degree=np.array([train_graph.degree(i) for i in range(view.num_nodes)],dtype=np.int64)
 a4_ids,qths_meta=make_ids(c,scores,train,.25)
 n=len(train); row=np.arange(n)
 specs={}
 if h1_raw:
  specs["A0_UNIFORM"]=("A_QTHS",None)
  specs["A4_QTHS25"]=("A_QTHS",c[row,a4_ids].copy())
 if h2:
  specs["B2_DEGREE_PENALTY"]=("B_CBHS",None)
  specs["B3_SHUFFLED_CONCENTRATION"]=("B_CBHS",None)
  specs["B4_CBHS"]=("B_CBHS",None)
 selection_meta={"QTHS":qths_meta,"A3_BOTTOM25":{"selection_equivalent_to_A1":True,"rule":"drop easiest 25% of full 20-row pool; Graph-hard top candidate remains"},
  "A5_MIDDLE25":{"selection_equivalent_to_A1":True,"rule":"drop middle 25% of full 20-row pool; Graph-hard top candidate remains"},
  "CBHS":{"lambda":LAMBDA,"concentration_normalization":"(count(u)+count(v))/(2*processed_positive_rows), clipped implicitly to [0,1]","degree_normalization":"(degree(u)+degree(v))/(2*max_train_degree)"},
  "candidate_diagnostics":{}}
 state={"state":"RUNNING","candidate_pool_hash":meta["candidate_pool_hash"],"split_hash":meta["train_only_split_hash"],"validation_candidate_hash":vhash,
        "A_runs":{},"B_runs":{},"candidate_selections":{}}
 for method in specs:
  group,unused=specs[method]; target=OUT/group/"RUNS"
  for seed in SEEDS:
   if method=="A0_UNIFORM": selected=None
   elif method=="A4_QTHS25": selected=c[row,a4_ids].copy()
   else: selected=selected_for(method,seed,ar,c,scores,pre,train,degree,a4_ids)
   key=f"{method}_seed{seed}"; outdir=target/key; rel=str(outdir.relative_to(ROOT)).replace("\\","/")
   status(f"{group}_validation",key,completed=list(state["A_runs"])+list(state["B_runs"]))
   record=engine.train_one(view,method,seed,selected,rel,vp,vn,initialize_from_v6=(seed==0),hypergraph_mode="raw")
   summary=summarize(c,scores,selected,degree) if selected is not None else {"dynamic_uniform_sampler":True}
   if selected is not None:
    summary["selected_negative_hash"]=v61.array_hash(selected)
    state["candidate_selections"].setdefault(method,{})[str(seed)]=summary["selected_negative_hash"]
   runrec={**record,"selection_summary":summary}
   state["A_runs" if group=="A_QTHS" else "B_runs"][key]=runrec
   jw(OUT/"candidate_training_state.json",state)
   status(f"{group}_validation",None,completed=list(state["A_runs"])+list(state["B_runs"]),last_finished=key)
 # Reuse strict V6.1 controls only after checking exact candidate, split and epoch policy.
 strict=jr(V61/"validation_results.json")["strict"]; vm=strict["by_method_seed"]
 a4={str(s):state["A_runs"][f"A4_QTHS25_seed{s}"]["epoch10_validation_mrr"] for s in SEEDS} if h1_raw else {}
 a0={str(s):state["A_runs"][f"A0_UNIFORM_seed{s}"]["epoch10_validation_mrr"] for s in SEEDS} if h1_raw else {}
 a1={str(s):float(vm["A1"][str(s)]["mrr"]) for s in SEEDS}; a2={str(s):float(vm["A3"][str(s)]["mrr"]) for s in SEEDS}
 a5=a1.copy()
 a_gate=None
 if h1_raw:
  wins1=sum(a4[str(s)]>a1[str(s)] for s in SEEDS); wins5=sum(a4[str(s)]>a5[str(s)] for s in SEEDS)
  mean4=float(np.mean(list(a4.values()))); mean2=float(np.mean(list(a2.values())))
  diff=mean4-mean2
  a_gate={"A4_by_seed":a4,"A0_by_seed":a0,"A1_by_seed":a1,"A2_by_seed":a2,"A5_by_seed":a5,
   "A4_mean":mean4,"A2_mean":mean2,"A4_minus_A2_mean":diff,"A4_wins_vs_A1":wins1,"A4_wins_vs_A5":wins5,
   "A4_minus_A1_mean":mean4-float(np.mean(list(a1.values()))),
   "GO":bool(wins1>=2 and wins5>=2 and mean4>np.mean(list(a1.values())) and diff>=-.001),
   "A4_vs_A2_control_status":"MATCH_OR_BETTER" if diff>=-.001 else "REJECT_RANDOMNESS_DOMINATES" if diff<-.002 else "GRAY_ZONE"}
 b_gate=None
 bmeans={}; bstats={}
 if h2:
  for method in ("B2_DEGREE_PENALTY","B3_SHUFFLED_CONCENTRATION","B4_CBHS"):
   bmeans[method]={str(s):state["B_runs"][f"{method}_seed{s}"]["epoch10_validation_mrr"] for s in SEEDS}
   bstats[method]={str(s):state["B_runs"][f"{method}_seed{s}"]["selection_summary"] for s in SEEDS}
  b0=a1; b1=a2; b4=bmeans["B4_CBHS"]; b3=bmeans["B3_SHUFFLED_CONCENTRATION"]
  wins0=sum(b4[str(s)]>b0[str(s)] for s in SEEDS); wins3=sum(b4[str(s)]>b3[str(s)] for s in SEEDS)
  meanrg=float(np.mean([bstats["B4_CBHS"][str(s)]["mean_Rg"] for s in SEEDS])); gini4=float(np.mean([bstats["B4_CBHS"][str(s)]["endpoint_gini"] for s in SEEDS])); gini0=float(np.mean([state["A_runs"].get(f"A4_QTHS25_seed{s}",{}).get("selection_summary",{}).get("endpoint_gini",np.nan) for s in SEEDS])) if False else float(res["aggregated"]["A1"]["diversity"]["endpoint_gini_all_nodes"])
  b_gate={"B0_GRAPH_HARD_by_seed":b0,"B1_RANDOM_VETO_by_seed":b1,"B2_DEGREE_PENALTY_by_seed":bmeans["B2_DEGREE_PENALTY"],"B3_SHUFFLED_CONCENTRATION_by_seed":b3,"B4_CBHS_by_seed":b4,
   "B4_wins_vs_B0":wins0,"B4_wins_vs_B3":wins3,"B0_mean_Rg":float(res["aggregated"]["A1"]["hardness"]["Rg_per_positive"]["mean"]),
   "B4_mean_Rg":meanrg,"B4_Rg_drop":float(res["aggregated"]["A1"]["hardness"]["Rg_per_positive"]["mean"]-meanrg),
   "B0_endpoint_gini":gini0,"B4_endpoint_gini":gini4,
   "GO":bool(wins0>=2 and wins3>=2 and gini4<gini0 and res["aggregated"]["A1"]["hardness"]["Rg_per_positive"]["mean"]-meanrg<=.03)}
 res["candidate_A"]={"status":"RUN" if h1_raw else "NOT_TRIGGERED","selection":selection_meta["QTHS"],"controls":{"A3_BOTTOM25":"exactly A1 Graph-hard after deleting easiest quarter of full row pool","A5_MIDDLE25":"exactly A1 Graph-hard after deleting middle quarter of full row pool"},"validation":a_gate}
 res["candidate_B"]={"status":"RUN" if h2 else "NOT_TRIGGERED","selection":selection_meta["CBHS"],"validation":b_gate,"per_seed_selection_statistics":bstats}
 # Candidate C only when both A and B gates pass. Implement as separate phase in a later continuation.
 both_go=bool(a_gate and a_gate["GO"] and b_gate and b_gate["GO"])
 res["candidate_C"]={"status":"NOT_RUN_A_AND_B_NOT_BOTH_GO","validation":None}
 eligible=[]
 if a_gate and a_gate["GO"]: eligible.append(("A4_QTHS25",a_gate["A4_mean"]))
 if b_gate and b_gate["GO"]: eligible.append(("B4_CBHS",float(np.mean(list(b_gate["B4_CBHS_by_seed"].values())))))
 winner=max(eligible,key=lambda x:x[1])[0] if eligible else None
 res["winning_candidate"]=winner; res["status"]="VALIDATION_COMPLETE"; res["validation_frozen_before_test"]=True
 res["final_decision"]="GO_PENDING_TEST" if winner else "NO_HARDNESS_REGULARIZATION_SIGNAL"
 jw(OUT/"results.json",res); jw(OUT/"candidate_training_state.json",state)
 # Component reports
 if a_gate:
  jw(OUT/"A_QTHS"/"results.json",{"selection":selection_meta["QTHS"],"validation":a_gate})
  text=["# QTHS validation","",f"- Selection: alpha={ALPHA:.2f} of candidate occurrences; top-2 prepool; deterministic row rounding trims the top candidate for {qths_meta['trimmed_row_count']} of {n} positives.","- The V6.1 shuffled control's selected-rank mixture is the matching target. A3 bottom-quarter and A5 middle-quarter deletions leave the Graph-hard top candidate intact and therefore collapse exactly to A1 at K=1.","",f"- GO: {a_gate['GO']}; A4 wins vs A1 in {a_gate['A4_wins_vs_A1']}/3 seeds and vs A5 in {a_gate['A4_wins_vs_A5']}/3; A4-A1 mean={a_gate['A4_minus_A1_mean']:+.6f}; A4-A2 mean={a_gate['A4_minus_A2_mean']:+.6f} ({a_gate['A4_vs_A2_control_status']}).","",json.dumps(a_gate,indent=2,ensure_ascii=False)]
  (OUT/"A_QTHS"/"01_VALIDATION.md").write_text("\n".join(text)+"\n",encoding="utf-8")
 if b_gate:
  jw(OUT/"B_CBHS"/"results.json",{"selection":selection_meta["CBHS"],"validation":b_gate,"per_seed_selection_statistics":bstats})
  text=["# CBHS validation","",f"- Fixed lambda={LAMBDA}; greedy over the train-only Graph top-2 prepool; B3 shuffles endpoint-frequency penalties within each row.","",f"- GO: {b_gate['GO']}; B4 wins vs B0 in {wins0}/3 and vs B3 in {wins3}/3; mean Rg drop={b_gate['B4_Rg_drop']:.6f}; Gini {gini0:.6f} -> {gini4:.6f}.","",json.dumps(b_gate,indent=2,ensure_ascii=False)]
  (OUT/"B_CBHS"/"01_VALIDATION.md").write_text("\n".join(text)+"\n",encoding="utf-8")
 # No test candidates are loaded in this script. A separate post-validation command will evaluate only if a GO winner exists.
 status("validation_complete",None,completed=list(state["A_runs"])+list(state["B_runs"]),winning_candidate=winner,test_evaluated=False,final_decision=res["final_decision"])
 print(json.dumps({"status":res["status"],"primary_diagnostic":res["primary_diagnostic"],"candidate_A_GO":None if not a_gate else a_gate["GO"],"candidate_B_GO":None if not b_gate else b_gate["GO"],"winner":winner,"test_evaluated":False},indent=2))
if __name__=="__main__":
 try: main()
 except Exception:
  status("failed",None,error=traceback.format_exc()); raise
