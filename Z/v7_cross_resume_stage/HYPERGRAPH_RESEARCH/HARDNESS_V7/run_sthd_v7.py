from __future__ import annotations
import json,math,sys,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
OUT=ROOT/"HYPERGRAPH_RESEARCH"/"HARDNESS_V7"; V61=ROOT/"HYPERGRAPH_RESEARCH"/"NEGATIVE_V6_1"; V62=ROOT/"HYPERGRAPH_RESEARCH"/"CODNS_V6_2"
def jr(p): return json.loads(p.read_text(encoding="utf-8"))
def jw(p,x):
 p.parent.mkdir(parents=True,exist_ok=True); q=p.with_suffix(p.suffix+".tmp"); q.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8"); q.replace(p)
def status(phase,current=None,completed=None,**kw):
 x={"state":"RUNNING","phase":phase,"current":current,"completed":completed or [],"updated_at":time.strftime("%Y-%m-%dT%H:%M:%S%z")}; x.update(kw); jw(OUT/"status.json",x)
def main():
 import torch
 from dcdlp.data.loaders import load_dataset
 sys.path.insert(0,str(V61)); sys.path.insert(0,str(V62)); sys.path.insert(0,str(OUT))
 import run_negative_v6_1 as v61
 import run_codns_v6_2 as engine
 import train_hardness_v7 as helpers
 res=jr(OUT/"results.json")
 a=res.get("candidate_A",{}).get("validation") or {}; b=res.get("candidate_B",{}).get("validation") or {}
 if not (a.get("GO") and b.get("GO")):
  res["candidate_C"]={"status":"NOT_RUN_A_AND_B_NOT_BOTH_GO","validation":None}
  res["validation_frozen_before_test"]=True; jw(OUT/"results.json",res); return
 with np.load(V61/"strict_train_candidates_and_selections.npz",allow_pickle=False) as z: ar={k:z[k].copy() for k in z.files}
 c=ar["negative_candidates"]; scores=ar["score_graph"]; train=ar["train_positive"]; pre=ar["graph_prepool_indices"]; meta=jr(V61/"strict_pool_metadata.json")
 data=load_dataset("cora",ROOT/"data","standard",0); view=v61.TrainOnlyView(data); del data
 vp,vn,vhash=engine.validation_arrays(); engine.candidate_pool=c; engine.candidate_pool_hash=meta["candidate_pool_hash"]; engine.validation_candidate_hash=vhash
 graph=view.train_graph(); degree=np.asarray([graph.degree(i) for i in range(view.num_nodes)],dtype=np.int64)
 a4_ids,_=helpers.make_ids(c,scores,train,.25); row=np.arange(len(c))
 state=jr(OUT/"candidate_training_state.json"); state.setdefault("C_runs",{})
 summary_rows={}
 for method,kind in (("C1_UNIFORM_DROPOUT","uniform"),("C3_REVERSE_DROPOUT","reverse"),("C4_STHD","stochastic")):
  for seed in (0,1,2):
   ids=helpers.dropout_ids(c,scores,pre,kind,seed); selected=c[row,ids].copy(); key=f"{method}_seed{seed}"
   outdir=OUT/"C_STHD"/"RUNS"/key; rel=str(outdir.relative_to(ROOT)).replace("\\","/")
   status("C_STHD_validation",key,completed=list(state["C_runs"]))
   rec=engine.train_one(view,method,seed,selected,rel,vp,vn,initialize_from_v6=(seed==0),hypergraph_mode="raw")
   sm=helpers.summarize(c,scores,selected,degree); sm["selected_negative_hash"]=v61.array_hash(selected)
   state["C_runs"][key]={**rec,"selection_summary":sm}; summary_rows.setdefault(method,{})[str(seed)]={"mrr":rec["epoch10_validation_mrr"],"selection":sm}
   jw(OUT/"candidate_training_state.json",state); status("C_STHD_validation",None,completed=list(state["C_runs"]),last_finished=key)
 c0={str(s):float(v61.load_json(V61/"validation_results.json")["strict"]["by_method_seed"]["A1"][str(s)]["mrr"]) for s in (0,1,2)}
 c2=a["A4_by_seed"]; c1={str(s):summary_rows["C1_UNIFORM_DROPOUT"][str(s)]["mrr"] for s in (0,1,2)}
 c3={str(s):summary_rows["C3_REVERSE_DROPOUT"][str(s)]["mrr"] for s in (0,1,2)}
 c4={str(s):summary_rows["C4_STHD"][str(s)]["mrr"] for s in (0,1,2)}
 wins0=sum(c4[str(s)]>c0[str(s)] for s in (0,1,2)); wins1=sum(c4[str(s)]>c1[str(s)] for s in (0,1,2)); wins3=sum(c4[str(s)]>c3[str(s)] for s in (0,1,2))
 mean4=float(np.mean(list(c4.values()))); mean2=float(np.mean(list(c2.values())))
 gate={"C0_GRAPH_HARD_by_seed":c0,"C1_UNIFORM_DROPOUT_by_seed":c1,"C2_QTHS_by_seed":c2,"C3_REVERSE_DROPOUT_by_seed":c3,"C4_STHD_by_seed":c4,
  "C4_wins_vs_C0":wins0,"C4_wins_vs_C1":wins1,"C4_wins_vs_C3":wins3,"C4_mean":mean4,"C2_mean":mean2,"C4_minus_C2_mean":mean4-mean2,
  "GO":bool(wins0>=2 and wins1>=2 and wins3>=2 and mean4>np.mean(list(c0.values())))}
 res["candidate_C"]={"status":"GO" if gate["GO"] else "NO_GO","selection":{"p_max":.5,"hardness_knee":.8,"rule":"p_drop=.5*clip((Rg-.8)/.2,0,1); redraw fallback keeps top candidate if both top-2 are dropped"},"validation":gate,"per_seed_selection_statistics":summary_rows}
 candidates=[]
 if a.get("GO"): candidates.append(("A4_QTHS25",float(a["A4_mean"])))
 if b.get("GO"): candidates.append(("B4_CBHS",float(np.mean(list(b["B4_CBHS_by_seed"].values())))))
 if gate["GO"]: candidates.append(("C4_STHD",mean4))
 winner=max(candidates,key=lambda x:x[1])[0] if candidates else None
 res["winning_candidate"]=winner; res["status"]="VALIDATION_COMPLETE"; res["validation_frozen_before_test"]=True
 res["final_decision"]="GO_PENDING_TEST" if winner else "NO_HARDNESS_REGULARIZATION_SIGNAL"
 jw(OUT/"results.json",res); jw(OUT/"candidate_training_state.json",state)
 (OUT/"C_STHD"/"results.json").write_text(json.dumps({"validation":gate,"selection":res["candidate_C"]["selection"]},indent=2),encoding="utf-8")
 lines=["# STHD validation","",f"- GO: {gate['GO']}; C4 wins versus Graph-hard in {wins0}/3, uniform dropout in {wins1}/3, reverse dropout in {wins3}/3.","",json.dumps(gate,indent=2,ensure_ascii=False)]
 (OUT/"C_STHD"/"01_VALIDATION.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 status("validation_complete",None,completed=list(state["C_runs"]),winning_candidate=winner,test_evaluated=False)
 print(json.dumps({"candidate_C_GO":gate["GO"],"winner":winner,"validation_frozen_before_test":True},indent=2))
if __name__=="__main__":
 try: main()
 except Exception:
  status("C_STHD_failed",error=traceback.format_exc()); raise
