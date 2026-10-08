from __future__ import annotations
import json,sys,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
OUT=ROOT/"HYPERGRAPH_RESEARCH"/"HARDNESS_V7"; V61=ROOT/"HYPERGRAPH_RESEARCH"/"NEGATIVE_V6_1"; V62=ROOT/"HYPERGRAPH_RESEARCH"/"CODNS_V6_2"
def jr(p): return json.loads(p.read_text(encoding="utf-8"))
def jw(p,x):
 p.parent.mkdir(parents=True,exist_ok=True); q=p.with_suffix(p.suffix+".tmp"); q.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8"); q.replace(p)
def status(phase,**kw):
 x={"state":"RUNNING","phase":phase,"updated_at":time.strftime("%Y-%m-%dT%H:%M:%S%z")}; x.update(kw); jw(OUT/"status.json",x)
def baseline_hash(d):
 for k in ("test_candidate_hash","shared_candidate_hash","candidate_hash"):
  if isinstance(d.get(k),str): return d[k]
 for k,v in d.items():
  if isinstance(v,dict) and ("test" in k.lower() or "result" in k.lower()):
   h=baseline_hash(v)
   if h: return h
 return None
def metric_record(test_obj,method,seed):
 by=test_obj.get("by_method_seed",{})
 if method in by and str(seed) in by[method]: return by[method][str(seed)]
 if "strict" in by and method in by["strict"] and str(seed) in by["strict"][method]: return by["strict"][method][str(seed)]
 raise RuntimeError(f"Cannot locate prior V6.1 test result for {method}, seed {seed}")
def locate_run(state,method,seed):
 key=f"{method}_seed{seed}"
 for bucket in ("A_runs","B_runs","C_runs"):
  if key in state.get(bucket,{}): return state[bucket][key]
 raise RuntimeError(f"Missing frozen validation checkpoint {key}")
def main():
 res=jr(OUT/"results.json")
 if res.get("status")!="VALIDATION_COMPLETE" or not res.get("validation_frozen_before_test"):
  raise RuntimeError("Test is gated until all validation decisions and the winner are frozen")
 if (OUT/"test_results.json").exists() and jr(OUT/"test_results.json").get("test_evaluated_once"):
  raise RuntimeError("Refusing a second V7 test evaluation")
 winner=res.get("winning_candidate")
 if not winner:
  tr={"test_status":"NOT_RUN_NO_VALIDATION_GO","test_evaluated_once":False,"reason":"No registered candidate passed validation"}
  jw(OUT/"test_results.json",tr); res["TEST"]=tr; res["status"]="COMPLETE"; res["final_decision"]="NO_HARDNESS_REGULARIZATION_SIGNAL"; res["NOVELTY_STATUS"]="NO_EXACT_MATCH_FOUND_IN_FOCUSED_SEARCH"; jw(OUT/"results.json",res)
  (OUT/"03_CROSS_DATASET.md").write_text("# Cross-dataset confirmation\n\nNot run: no V7 candidate passed the validation gate, so Cora test remained closed.\n",encoding="utf-8")
  status("complete",test_evaluated=False,final_decision=res["final_decision"]); return
 # All validation comparisons are now frozen; test identities are first read below.
 status("test_evaluation_started",test_evaluated=False,winner=winner)
 import torch
 from dcdlp.data.loaders import load_dataset
 from dcdlp.data.negative_sampling import grouped_negatives,uniform_negative_sampling
 from dcdlp.train import edge_index_from_graph
 sys.path.insert(0,str(V61)); sys.path.insert(0,str(V62))
 import run_negative_v6_1 as v61
 import run_codns_v6_2 as engine
 vstate=jr(OUT/"candidate_training_state.json"); old=jr(V61/"test_results.json")
 full=load_dataset("cora",ROOT/"data","standard",0)
 test_pos=np.asarray(full.test_pos,dtype=np.int64).copy()
 test_pool=uniform_negative_sampling(full.num_nodes,full.all_positive,20*len(test_pos),999)
 test_neg=grouped_negatives(test_pos,test_pool,20,1000)
 test_hash=v61.array_hash(test_neg); expected=baseline_hash(old)
 if expected is None: raise RuntimeError("V6.1 shared test-candidate hash is absent")
 if test_hash!=expected: raise RuntimeError(f"shared test candidate hash mismatch: {test_hash} != {expected}")
 for m in ("A1","A3"):
  for s in (0,1,2):
   rec=metric_record(old,m,s)
   if rec.get("candidate_hash") not in (None,test_hash): raise RuntimeError(f"historical {m} test candidate hash mismatch")
   ck=res.get("A1_A3_run_audit",{}).get(f"S_{m}_seed{s}",{}).get("checkpoint")
   if ck and rec.get("checkpoint") and ck!=rec["checkpoint"]: raise RuntimeError(f"historical {m} checkpoint path mismatch")
 # Pick the best validated A/B mechanism as a control; if winner itself is the only GO method, alias it.
 go=[]
 a=res.get("candidate_A",{}).get("validation") or {}
 b=res.get("candidate_B",{}).get("validation") or {}
 if a.get("GO"): go.append(("A4_QTHS25",float(a["A4_mean"])))
 if b.get("GO"): go.append(("B4_CBHS",float(np.mean(list(b["B4_CBHS_by_seed"].values())))))
 control=max(go,key=lambda x:x[1])[0] if go else winner
 data=full
 view=v61.TrainOnlyView(data)
 valid_methods={"A1","A3",control,winner}
 by={}
 for method in ("A1","A3"):
  by[method]={str(s):metric_record(old,method,s) for s in (0,1,2)}
 cache={}
 for method in dict.fromkeys((control,winner)):
  cache[method]={}
  for seed in (0,1,2):
   rec=locate_run(vstate,method,seed); ck=rec["checkpoint"]
   metric=engine.eval_fixed_candidates(ck,view,test_pos,test_neg)
   cache[method][str(seed)]={**metric,"checkpoint":ck,"candidate_hash":test_hash}
   del metric
  by[method]=cache[method]
 means={}
 for method in valid_methods:
  means[method]=float(np.mean([by[method][str(s)]["mrr"] for s in (0,1,2)]))
 wvals=np.array([by[winner][str(s)]["mrr"] for s in (0,1,2)])
 a1=np.array([by["A1"][str(s)]["mrr"] for s in (0,1,2)])
 a3=np.array([by["A3"][str(s)]["mrr"] for s in (0,1,2)])
 wins_a1=int(np.sum(wvals>a1)); wins_a3=int(np.sum(wvals>a3))
 supported=bool(wvals.mean()>a1.mean() and wins_a1>=2)
 test={"test_status":"COMPLETE","test_evaluated_once":True,"test_candidate_hash":test_hash,"matches_v6_1_shared_candidates":True,
  "test_positive_count":int(len(test_pos)),"negatives_per_positive":20,"negative_pool_seed":999,"grouping_seed":1000,
  "by_method_seed":by,"mean_mrr":means,"winner":winner,"best_mechanism_control":control,
  "winner_minus_A1_by_seed":(wvals-a1).tolist(),"winner_minus_A3_by_seed":(wvals-a3).tolist(),
  "winner_wins_vs_A1":wins_a1,"winner_wins_vs_A3":wins_a3,"supported_vs_graph_hard":supported,
  "supported_vs_random_veto":bool(wvals.mean()>a3.mean() and wins_a3>=2),
  "cross_dataset_gate":"OPEN" if supported else "CLOSED"}
 jw(OUT/"test_results.json",test)
 res["TEST"]=test; res["test_evaluated_once"]=True
 res["final_decision"]="GO_PENDING_SECOND_DATASET" if supported else "VALIDATION_GO_TEST_NOT_SUPPORTED"
 res["NOVELTY_STATUS"]="NO_EXACT_MATCH_FOUND_IN_FOCUSED_SEARCH"
 jw(OUT/"results.json",res)
 if supported:
  (OUT/"03_CROSS_DATASET.md").write_text("# Cross-dataset confirmation\n\nCora test improved over Graph-hard in mean and in at least two of three seeds. The task gate is open; run the registered seed-0 screen on Citeseer (Pubmed fallback) next. No dataset-specific hyperparameter changes.\n",encoding="utf-8")
  status("second_dataset_pending",test_evaluated=True,cross_dataset_gate="OPEN",winner=winner)
 else:
  (OUT/"03_CROSS_DATASET.md").write_text("# Cross-dataset confirmation\n\nNot run: the frozen winner did not pass the Cora test support gate (mean and 2/3 seed wins over Graph-hard).\n",encoding="utf-8")
  res["status"]="COMPLETE"; jw(OUT/"results.json",res); status("complete",test_evaluated=True,cross_dataset_gate="CLOSED",final_decision=res["final_decision"])
 print(json.dumps({"test_status":test["test_status"],"winner":winner,"mean_mrr":means,"supported_vs_graph_hard":supported,"supported_vs_random_veto":test["supported_vs_random_veto"]},indent=2))
if __name__=="__main__":
 try: main()
 except Exception:
  status("test_failed",error=traceback.format_exc()); raise
