from __future__ import annotations
import hashlib,json,sys,time,traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
OUT=ROOT/"HYPERGRAPH_RESEARCH"/"HARDNESS_V7"; V61=ROOT/"HYPERGRAPH_RESEARCH"/"NEGATIVE_V6_1"; V62=ROOT/"HYPERGRAPH_RESEARCH"/"CODNS_V6_2"
def jr(p): return json.loads(p.read_text(encoding="utf-8"))
def jw(p,x):
 p.parent.mkdir(parents=True,exist_ok=True); q=p.with_suffix(p.suffix+".tmp"); q.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding="utf-8"); q.replace(p)
def status(phase,current=None,**kw):
 x={"state":"RUNNING","phase":phase,"current":current,"updated_at":time.strftime("%Y-%m-%dT%H:%M:%S%z")}; x.update(kw); jw(OUT/"status.json",x)
def select_random_veto(scores,seed):
 n=len(scores); order=np.argsort(-scores,axis=1,kind="stable")[:,:2]; rng=np.random.default_rng(400000+seed*10000+7710)
 veto=rng.integers(0,2,size=n); return order[np.arange(n),1-veto]
def main():
 import torch,networkx as nx
 from torch_geometric.data.data import Data
 torch.serialization.add_safe_globals([Data])
 from dcdlp.data.loaders import load_dataset
 from dcdlp.data.negative_sampling import grouped_negatives,uniform_negative_sampling
 from dcdlp.evaluate import load_checkpoint_model
 from dcdlp.train import edge_index_from_graph,score_pairs
 res=jr(OUT/"results.json"); test=res.get("TEST",{})
 if res.get("status")!="VALIDATION_COMPLETE" or not test.get("supported_vs_graph_hard"):
  raise RuntimeError("Second dataset is gated until Cora test beats Graph-hard")
 sys.path.insert(0,str(V61)); sys.path.insert(0,str(V62)); sys.path.insert(0,str(OUT))
 import run_negative_v6_1 as v61
 import run_codns_v6_2 as engine
 import train_hardness_v7 as helpers
 winner=res["winning_candidate"]
 full=None; name=None; errors={}
 for candidate in ("citeseer","pubmed"):
  try:
   full=load_dataset(candidate,ROOT/"data","standard",0); name=candidate; break
  except Exception as exc: errors[candidate]=f"{type(exc).__name__}: {exc}"
 if full is None:
  result={"status":"CROSS_DATASET_UNAVAILABLE","errors":errors}
  jw(OUT/"cross_dataset_results.json",result)
  res=jr(OUT/"results.json"); res["SECOND_DATASET"]=result; res["status"]="COMPLETE"; res["final_decision"]="GO_CORA_ONLY"; jw(OUT/"results.json",res)
  (OUT/"03_CROSS_DATASET.md").write_text("# Cross-dataset confirmation\n\nCiteseer and Pubmed could not be loaded. The Cora test gate passed, but transfer evidence is unavailable.\n",encoding="utf-8")
  status("complete",second_dataset_status=result["status"]); return
 view=v61.TrainOnlyView(full); valid_pos=np.asarray(full.valid_pos,dtype=np.int64).copy()
 # Validation candidates are evaluation-only; they are never part of the sampler or Graph-teacher pool.
 val_seed=72200
 val_pool=uniform_negative_sampling(full.num_nodes,full.all_positive,max(20*len(valid_pos),20),val_seed)
 valid_neg=grouped_negatives(valid_pos,val_pool,20,val_seed+1); val_hash=v61.array_hash(valid_neg)
 forbidden_rows,forbidden=v61.make_train_forbidden(view)
 train_seed,group_seed=20261002,20261003
 raw=uniform_negative_sampling(view.num_nodes,forbidden_rows,len(view.train_pos)*20,train_seed)
 candidates=grouped_negatives(view.train_pos,raw,20,group_seed)
 if candidates.shape!=(len(view.train_pos),20,2): raise RuntimeError(f"{name} candidate pool shape mismatch")
 if any(v61.canonical_edge(x) in forbidden for x in candidates.reshape(-1,2)): raise RuntimeError(f"{name} train pool contains forbidden edge")
 pool_hash=v61.array_hash(candidates); split_hash=hashlib.sha256((v61.array_hash(view.train_pos)+v61.array_hash(view.features)+str(view.num_nodes)).encode("ascii")).hexdigest()
 engine.candidate_pool=candidates; engine.candidate_pool_hash=pool_hash; engine.validation_candidate_hash=val_hash
 graph=view.train_graph(); degree=np.asarray([graph.degree(i) for i in range(view.num_nodes)],dtype=np.int64)
 # Teacher is trained on uniform negatives from the frozen train-only pool; it never sees held-out edge identities.
 tdir=OUT/"CROSS_DATASET"/name/"TEACHER_GRAPH"; rel=str(tdir.relative_to(ROOT)).replace("\\","/")
 status("cross_dataset_teacher",name)
 teacher=engine.train_one(view,f"{name}_GRAPH_TEACHER",0,None,rel,valid_pos,valid_neg,initialize_from_v6=False,dataset_name=name,hypergraph_mode="disabled")
 model,_=load_checkpoint_model(teacher["checkpoint"],device="cuda"); x=torch.as_tensor(view.features,dtype=torch.float32,device="cuda"); edge_index=edge_index_from_graph(view.train_graph(),torch.device("cuda"))
 with torch.no_grad():
  output=score_pairs(model,x,edge_index,candidates.reshape(-1,2),batch_size=8192)
  scores=np.asarray(output["logit"],dtype=np.float32).reshape(len(view.train_pos),20)
 del model; torch.cuda.empty_cache()
 pre=np.argsort(scores,axis=1,kind="stable")[:,-2:]
 qths_ids,qmeta=helpers.make_ids(candidates,scores,view.train_pos,.25)
 def ids_for(code,seed):
  if code=="A4_QTHS25": return qths_ids
  if code=="B4_CBHS": return helpers.choose_prepool(candidates,scores,pre,"concentration",degree,seed)
  if code=="C4_STHD": return helpers.dropout_ids(candidates,scores,pre,"stochastic",seed)
  raise RuntimeError(f"Unsupported transfer rule: {code}")
 methods=("Graph-hard","Random-veto","Winner"); metric_rows={m:{} for m in methods}; run_rows={}
 proceed=False
 for seed in (0,1,2):
  if seed>0 and not proceed: break
  for method in methods:
   if method=="Graph-hard": selected=candidates[np.arange(len(view.train_pos)),np.argmax(scores,axis=1)].copy()
   elif method=="Random-veto": selected=candidates[np.arange(len(view.train_pos)),select_random_veto(scores,seed)].copy()
   else: selected=candidates[np.arange(len(view.train_pos)),ids_for(winner,seed)].copy()
   outdir=OUT/"CROSS_DATASET"/name/method.replace("-","_")/f"seed{seed}"; rel=str(outdir.relative_to(ROOT)).replace("\\","/")
   status("cross_dataset_screen" if seed==0 else "cross_dataset_confirmation",f"{method}_seed{seed}")
   rec=engine.train_one(view,f"{name}_{method}",seed,selected,rel,valid_pos,valid_neg,initialize_from_v6=False,dataset_name=name,hypergraph_mode="raw")
   metric_rows[method][str(seed)]={"mrr":rec["epoch10_validation_mrr"],"checkpoint":rec["checkpoint"],"selected_negative_hash":rec["selected_negative_hash"],"checkpoint_rule":"FIXED_EPOCH_10"}
   run_rows[f"{method}_seed{seed}"]=rec
  if seed==0:
   proceed=metric_rows["Winner"]["0"]["mrr"]>metric_rows["Graph-hard"]["0"]["mrr"]
   screen={"seed0_mrr":{m:metric_rows[m]["0"]["mrr"] for m in methods},"proceed_to_three_seeds":bool(proceed)}
   jw(OUT/"cross_dataset_results.json",{"status":"RUNNING","dataset":name,"winner":winner,"candidate_pool_hash":pool_hash,"split_hash":split_hash,"validation_candidate_hash":val_hash,"teacher_checkpoint":teacher["checkpoint"],"teacher_state_hash":teacher["model_state_hash"],"teacher_scores_hash":v61.array_hash(scores),"qths_rule":qmeta,"seed0_screen":screen,"metrics":metric_rows,"run_records":run_rows,"heldout_identity_used_in_training_pool":False,"test_split_metrics_evaluated":False})
   if not proceed: break
 result=jr(OUT/"cross_dataset_results.json")
 if proceed:
  means={m:float(np.mean([metric_rows[m][str(s)]["mrr"] for s in (0,1,2)])) for m in methods}
  std={m:float(np.std([metric_rows[m][str(s)]["mrr"] for s in (0,1,2)],ddof=1)) for m in methods}
  wins=int(sum(metric_rows["Winner"][str(s)]["mrr"]>metric_rows["Graph-hard"][str(s)]["mrr"] for s in (0,1,2)))
  supported=bool(means["Winner"]>means["Graph-hard"] and wins>=2)
  result.update({"status":"SUPPORTED" if supported else "CROSS_DATASET_INCONCLUSIVE","mean_mrr":means,"sample_sd_mrr":std,"winner_wins_vs_graph_hard":wins,"supported":supported})
 else:
  result.update({"status":"CROSS_DATASET_INCONCLUSIVE","supported":False})
 result["metrics"]=metric_rows; result["run_records"]=run_rows
 jw(OUT/"cross_dataset_results.json",result)
 res=jr(OUT/"results.json"); res["SECOND_DATASET"]=result
 res["final_decision"]="STRONG_GO" if result.get("supported") else "GO_CORA_ONLY"
 res["status"]="COMPLETE"; jw(OUT/"results.json",res)
 lines=["# Cross-dataset confirmation","",f"- Dataset: {name}; transfer rule: {winner}; no dataset-specific parameter tuning.",
  f"- Train-only pool hash: {pool_hash}; split hash: {split_hash}; validation candidate hash: {val_hash}.",
  f"- Held-out identities were not used to exclude the training pool. The full-positive set is used only for validation-negative filtering; no test-split metrics are evaluated.",
  f"- Seed-0 screen: {json.dumps(result.get('seed0_screen',{}),ensure_ascii=False)}."]
 if result.get("mean_mrr"): lines.append(f"- Three-seed mean validation MRR: {json.dumps(result['mean_mrr'],ensure_ascii=False)}; Winner wins vs Graph-hard in {result['winner_wins_vs_graph_hard']}/3. Supported={result.get('supported')}.")
 else: lines.append("- Winner did not exceed Graph-hard at seed 0, so the registered three-seed confirmation was not run.")
 (OUT/"03_CROSS_DATASET.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 status("complete",second_dataset=name,second_dataset_status=result["status"],final_decision=res["final_decision"],test_evaluated=True)
 print(json.dumps({"dataset":name,"status":result["status"],"seed0_screen":result.get("seed0_screen"),"mean_mrr":result.get("mean_mrr")},indent=2))
if __name__=="__main__":
 try: main()
 except Exception:
  status("cross_dataset_failed",error=traceback.format_exc()); raise
