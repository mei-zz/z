"""Run gated CPTS V10 test, dataset and backbone stages on frozen caches."""
from __future__ import annotations
import concurrent.futures as cf
import json, multiprocessing as mp, os, sys, time, traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
HR=ROOT/'HYPERGRAPH_RESEARCH'; OUT=HR/'CPTS_V10'; V71=HR/'QTHS_V7_1'; V8DIR=HR/'QTHS_V8_PAPER'
sys.path[:0]=[str(ROOT/'src'),str(V8DIR),str(OUT)]
import experiment_v8 as v8
import audit_tail_structure as audit

def readj(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def writej(p,x):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(x,indent=2,ensure_ascii=False),encoding='utf-8'); t.replace(p)
def state_path(t): return OUT/'STATE'/f"{t['dataset']}_{t['backbone']}_{t['method'].lower()}_seed{t['seed']}.json"
def train_worker(t):
 v8.worker_init(); import torch
 old=v8.configure_backbone(t['backbone']); start=time.perf_counter(); p=state_path(t)
 try:
  _,view,pool,scores,pool_hash,vpos,vneg,vhash=v8.dataset_context(t['dataset'])
  if t['method']=='CPTS':
   ids=audit.local_cpts(scores)[-1]; selected=pool[np.arange(len(pool)),ids].copy()
  elif t['method']=='SH75': selected=v8.selected_edges({'method':'SH75','seed':int(t['seed'])},pool,scores,view.train_pos)
  else: raise ValueError(t)
  _,forbidden=v8.v61.make_train_forbidden(view)
  if any(v8.v61.canonical_edge(x) in forbidden for x in selected): raise RuntimeError('selector emitted train-forbidden edge')
  v8.engine.candidate_pool=pool; v8.engine.candidate_pool_hash=pool_hash; v8.engine.validation_candidate_hash=vhash
  rel=(Path('HYPERGRAPH_RESEARCH')/'CPTS_V10'/'RUNS'/t['dataset'].upper()/t['backbone'].upper()/t['method']/f"seed{t['seed']}").as_posix()
  torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats()
  rec=v8.engine.train_one(view,t['method'],int(t['seed']),selected,rel,vpos,vneg,initialize_from_v6=False,dataset_name=t['dataset'],hypergraph_mode='raw')
  metrics,params=v8.metric_for_checkpoint(rec['checkpoint'],view,vpos,vneg)
  if abs(metrics['mrr']-float(rec['epoch10_validation_mrr']))>1e-9: raise RuntimeError('fixed epoch-10 validation did not reproduce')
  torch.cuda.synchronize()
  out={'state':'COMPLETE','task':t,'training_record':rec,'validation_metrics':metrics,'trainable_parameters':params,'train_pool_hash':pool_hash,'validation_candidate_hash':vhash,'peak_gpu_memory_mb':float(torch.cuda.max_memory_allocated()/1024**2),'wall_seconds':time.perf_counter()-start,'test_evaluated':False}
  writej(p,out); return out
 except Exception as e:
  writej(p,{'state':'FAILED','task':t,'error':repr(e),'traceback':traceback.format_exc()}); raise
 finally: v8.v61.load_json=old

def eval_worker(t):
 v8.worker_init(); old=v8.configure_backbone('gcn'); start=time.perf_counter()
 try:
  _,view=v8.base.init_dataset(t['dataset']); arpath=V8DIR/'EVALUATION'/f"{t['dataset']}_test_candidates.npz"; meta=readj(V8DIR/'EVALUATION'/f"{t['dataset']}_test_candidates.json")
  with np.load(arpath,allow_pickle=False) as z: pos=z['test_positive'].copy(); neg=z['test_negative_candidates'].copy()
  if v8.v61.array_hash(neg)!=meta['candidate_hash']: raise RuntimeError('test candidate hash mismatch')
  metrics,params=v8.metric_for_checkpoint(t['checkpoint'],view,pos,neg)
  out={'state':'COMPLETE','task':{k:v for k,v in t.items() if k!='checkpoint'},'test_metrics':metrics,'checkpoint':t['checkpoint'],'candidate_hash':meta['candidate_hash'],'trainable_parameters':params,'wall_seconds':time.perf_counter()-start}
  writej(OUT/'STATE'/'TEST'/f"{t['dataset']}_{t['method'].lower()}_seed{t['seed']}.json",out); return out
 finally: v8.v61.load_json=old

def parallel(stage,tasks,worker,max_workers=6):
 status={'state':'RUNNING','stage':stage,'workers':min(max_workers,len(tasks)),'total_jobs':len(tasks),'completed_jobs':0,'test_enabled':stage=='CORA_TEST'}
 writej(OUT/'status.json',status); rs=[]
 with cf.ProcessPoolExecutor(max_workers=min(max_workers,len(tasks)),mp_context=mp.get_context('spawn')) as ex:
  futures={ex.submit(worker,t):t for t in tasks}
  for f in cf.as_completed(futures):
   r=f.result(); rs.append(r); status['completed_jobs']+=1; status['last_completed']=r.get('task',{}); status['last_job_wall_seconds']=r.get('wall_seconds'); writej(OUT/'status.json',status)
 return rs

def stats(vals): return {'by_seed':[float(x) for x in vals],'mean':float(np.mean(vals)),'sample_std':float(np.std(vals,ddof=1)),'n':len(vals)}
def paired(a,b):
 d=[float(x-y) for x,y in zip(a,b)]; return {'by_seed':d,'mean_delta':float(np.mean(d)),'wins':int(sum(x>0 for x in d))}
def checkpoint_from_state(ds,bk,method,seed):
 if method=='SH75' and ds=='cora' and bk=='gcn':
  return readj(V8DIR/'RUNS'/'CORA'/'GCN'/'SH75'/f'seed{seed}'/'codns_run.json')['checkpoint']
 return readj(state_path({'dataset':ds,'backbone':bk,'method':method,'seed':seed}))['training_record']['checkpoint']
def main():
 v8.base.ensure_expected_runtime(); import torch
 if not torch.cuda.is_available(): raise RuntimeError('CUDA unavailable')
 result=readj(OUT/'results.json'); v71=readj(V71/'results.json'); v8r=readj(V8DIR/'results.json')
 # Cora one-time test, only after the completed validation GO.
 cv=readj(OUT/'cora_validation_results.json')
 if cv['final_decision_at_validation']!='GO': raise RuntimeError('Cora validation is not GO; test gate closed')
 cora_test_tasks=[]
 for m in ('CPTS','SH75','MATCHED_Q','RANDOM_MATCHED'):
  for s in (0,1,2): cora_test_tasks.append({'dataset':'cora','method':m,'seed':s,'checkpoint':checkpoint_from_state('cora','gcn',m,s)})
 parallel('CORA_TEST',cora_test_tasks,eval_worker,4)
 tc=v71['cora']['test']['by_method_seed']; ctest={}
 for label,key in [('GRAPH_HARD','C1_GRAPH_HARD'),('QTHS25','C3_QTHS25')]: ctest[label]=[float(tc[key][str(s)]['mrr']) for s in (0,1,2)]
 for m in ('CPTS','SH75','MATCHED_Q','RANDOM_MATCHED'):
  ctest[m]=[readj(OUT/'STATE'/'TEST'/f"cora_{m.lower()}_seed{s}.json")['test_metrics']['mrr'] for s in (0,1,2)]
 cdelta={m:paired(ctest['CPTS'],ctest[m]) for m in ('GRAPH_HARD','QTHS25','SH75','MATCHED_Q','RANDOM_MATCHED')}
 cmean={m:stats(v) for m,v in ctest.items()}
 ctest_go=(cdelta['GRAPH_HARD']['mean_delta']>0 and cdelta['GRAPH_HARD']['wins']>=2 and cdelta['QTHS25']['mean_delta']>=-.002 and cdelta['QTHS25']['wins']>=2 and cdelta['SH75']['mean_delta']>=-.005)
 ctest_result={'methods_mrr':cmean,'paired_cpts_delta':cdelta,'supported':bool(ctest_go),'candidate_hash':readj(V8DIR/'EVALUATION'/'cora_test_candidates.json')['candidate_hash'],'interpretation':'support requires CPTS > Graph-hard (mean and >=2/3 wins), CPTS within 0.002 of QTHS25 and >=2/3 wins, and no SH75 lead greater than 0.005'}
 result['cora_test']=ctest_result
 lines=['# Cora test','','Frozen V8/V7.1 candidate set; evaluated once after validation GO; fixed epoch 10; seeds 0–2. Cached Graph-hard and QTHS25 checkpoints were reused; new CPTS, SH75 and matched controls were evaluated.','', '| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |','|---|---:|---:|---:|---:|']
 for m,x in cmean.items(): lines.append(f"| {m} | {x['by_seed'][0]:.6f} | {x['by_seed'][1]:.6f} | {x['by_seed'][2]:.6f} | {x['mean']:.6f} ± {x['sample_std']:.6f} |")
 lines+=['','| CPTS vs | Paired deltas | Mean delta | Wins/3 |','|---|---|---:|---:|']
 for m,x in cdelta.items(): lines.append(f"| {m} | {np.round(x['by_seed'],6).tolist()} | {x['mean_delta']:+.6f} | {x['wins']}/3 |")
 lines+=['',f"Cora test gate: **{'SUPPORTED' if ctest_go else 'NOT SUPPORTED'}**.",'']
 (OUT/'05_CORA_TEST.md').write_text('\n'.join(lines),encoding='utf-8')
 if not ctest_go:
  result['study_status']='CORA_TEST_NOT_SUPPORTED_STOPPED_BY_GATE'; writej(OUT/'results.json',result); writej(OUT/'status.json',{'state':'COMPLETE','stage':'CORA_TEST','decision':'CORA_TEST_NOT_SUPPORTED','completed_jobs':len(cora_test_tasks),'test_enabled':True}); return
 # PubMed: train-only CPTS and SH75, compare with exact cached Graph-hard/QTHS25 validation arms.
 p_tasks=[{'dataset':'pubmed','backbone':'gcn','method':m,'seed':s} for m in ('CPTS','SH75') for s in (0,1,2)]
 parallel('PUBMED_VALIDATION',p_tasks,train_worker,6)
 pv=v8r['pubmed']['validation']; pvals={'GRAPH_HARD':[float(x) for x in pv['GRAPH_HARD']['by_seed']],'QTHS25':[float(x) for x in pv['QTHS25']['by_seed']]}
 for m in ('CPTS','SH75'): pvals[m]=[readj(state_path({'dataset':'pubmed','backbone':'gcn','method':m,'seed':s}))['validation_metrics']['mrr'] for s in (0,1,2)]
 ppaired={m:paired(pvals['CPTS'],pvals[m]) for m in ('GRAPH_HARD','QTHS25','SH75')}; pstat={m:stats(x) for m,x in pvals.items()}
 reversal=(ppaired['GRAPH_HARD']['mean_delta']<-.005 and ppaired['SH75']['mean_delta']<-.005 and ppaired['GRAPH_HARD']['wins']<=1)
 result['pubmed']={'validation':pstat,'cpts_paired_delta':ppaired,'clear_reversal':bool(reversal),'candidate_pool_hash':result['datasets']['pubmed']['candidate_pool_hash']}
 lines=['# PubMed','','Frozen graph-teacher candidate pool; same BIC rule; GCN, fixed epoch 10, seeds 0–2. Graph-hard and QTHS25 validation results reused from V8; CPTS and SH75 trained under V10.','', '| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |','|---|---:|---:|---:|---:|']
 for m,x in pstat.items(): lines.append(f"| {m} | {x['by_seed'][0]:.6f} | {x['by_seed'][1]:.6f} | {x['by_seed'][2]:.6f} | {x['mean']:.6f} ± {x['sample_std']:.6f} |")
 lines+=['','| CPTS vs | Paired deltas | Mean delta | Wins/3 |','|---|---|---:|---:|']
 for m,x in ppaired.items(): lines.append(f"| {m} | {np.round(x['by_seed'],6).tolist()} | {x['mean_delta']:+.6f} | {x['wins']}/3 |")
 lines+=['',f"Clear reversal flag: **{reversal}** (defined before continuation as CPTS mean at least 0.005 below both Graph-hard and SH75, with at most one win vs Graph-hard).",'']
 (OUT/'06_PUBMED.md').write_text('\n'.join(lines),encoding='utf-8')
 if reversal:
  result['study_status']='PUBMED_CLEAR_REVERSAL_STOPPED'; writej(OUT/'results.json',result); writej(OUT/'status.json',{'state':'COMPLETE','stage':'PUBMED_VALIDATION','decision':'PUBMED_CLEAR_REVERSAL','completed_jobs':len(p_tasks),'test_enabled':False}); return
 # Citeseer continuation.
 ci_tasks=[{'dataset':'citeseer','backbone':'gcn','method':m,'seed':s} for m in ('CPTS','SH75') for s in (0,1,2)]
 parallel('CITESEER_VALIDATION',ci_tasks,train_worker,6)
 cv1=v71['citeseer']['validation']['runs']; gh_ci=[float(cv1['C1_GRAPH_HARD'][str(s)]['validation_metrics']['mrr']) for s in (0,1,2)]
 civals={'GRAPH_HARD':gh_ci}
 for m in ('CPTS','SH75'): civals[m]=[readj(state_path({'dataset':'citeseer','backbone':'gcn','method':m,'seed':s}))['validation_metrics']['mrr'] for s in (0,1,2)]
 cipaired={m:paired(civals['CPTS'],civals[m]) for m in ('GRAPH_HARD','SH75')}; cistat={m:stats(x) for m,x in civals.items()}
 result['citeseer']={'validation':cistat,'cpts_paired_delta':cipaired,'interpretation':'neutral result is allowed; no selector-rule tuning'}
 lines=['# Citeseer','','Frozen train-only graph-teacher pool; same BIC rule; GCN, fixed epoch 10, seeds 0–2. Graph-hard validation reused from V7.1.','', '| Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |','|---|---:|---:|---:|---:|']
 for m,x in cistat.items(): lines.append(f"| {m} | {x['by_seed'][0]:.6f} | {x['by_seed'][1]:.6f} | {x['by_seed'][2]:.6f} | {x['mean']:.6f} ± {x['sample_std']:.6f} |")
 lines+=['','| CPTS vs | Paired deltas | Mean delta | Wins/3 |','|---|---|---:|---:|']
 for m,x in cipaired.items(): lines.append(f"| {m} | {np.round(x['by_seed'],6).tolist()} | {x['mean_delta']:+.6f} | {x['wins']}/3 |")
 lines+=['','Citeseer is descriptive; neutral performance is allowed and no rule changes are permitted.','']
 (OUT/'07_CITESEER.md').write_text('\n'.join(lines),encoding='utf-8')
 # Backbone: Cora CPTS SAGE/GAT; cached Graph-hard validations reused, GCN from V10.
 b_tasks=[{'dataset':'cora','backbone':bk,'method':'CPTS','seed':s} for bk in ('sage','gat') for s in (0,1,2)]
 parallel('BACKBONE_VALIDATION',b_tasks,train_worker,6)
 bg=v8r['backbone_generalization']['by_backbone']; backbone={}
 gcn_cpts=[readj(state_path({'dataset':'cora','backbone':'gcn','method':'CPTS','seed':s}))['validation_metrics']['mrr'] for s in (0,1,2)]
 backbone['gcn']={'GRAPH_HARD':stats([float(x) for x in readj(OUT/'cora_validation_results.json')['methods_mrr_by_seed']['GRAPH_HARD'].values()]),'CPTS':stats([readj(state_path({'dataset':'cora','backbone':'gcn','method':'CPTS','seed':s}))['validation_metrics']['mrr'] for s in (0,1,2)])}
 for bk in ('sage','gat'):
  gh=[float(x) for x in bg[bk]['methods']['GRAPH_HARD']['by_seed']]
  cp=[readj(state_path({'dataset':'cora','backbone':bk,'method':'CPTS','seed':s}))['validation_metrics']['mrr'] for s in (0,1,2)]
  backbone[bk]={'GRAPH_HARD':stats(gh),'CPTS':stats(cp),'cpts_minus_graph_hard':paired(cp,gh)}
  backbone[bk]['cpts_minus_graph_hard']=paired(cp,gh)
 # Add GCN paired data from Cora validation.
 backbone['gcn']['cpts_minus_graph_hard']=paired(gcn_cpts,[float(readj(OUT/'cora_validation_results.json')['methods_mrr_by_seed']['GRAPH_HARD'][str(s)]) for s in (0,1,2)])
 result['backbone_generalization']={'by_backbone':backbone,'backbone_count':3}
 lines=['# Backbone generalization','','Cora, fixed epoch 10, seeds 0–2. Frozen Graph-hard baselines reused from V7.1/V8; CPTS uses the unchanged local BIC selector.','', '| Backbone | Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |','|---|---|---:|---:|---:|---:|']
 for bk,ms in backbone.items():
  for m,x in ms.items():
   if m=='cpts_minus_graph_hard': continue
   lines.append(f"| {bk.upper()} | {m} | {x['by_seed'][0]:.6f} | {x['by_seed'][1]:.6f} | {x['by_seed'][2]:.6f} | {x['mean']:.6f} ± {x['sample_std']:.6f} |")
 lines+=['','| Backbone | CPTS − Graph-hard paired delta | Mean delta | Wins/3 |','|---|---|---:|---:|']
 for bk,x in backbone.items():
  p=x['cpts_minus_graph_hard']; lines.append(f"| {bk.upper()} | {np.round(p['by_seed'],6).tolist()} | {p['mean_delta']:+.6f} | {p['wins']}/3 |")
 (OUT/'08_BACKBONE.md').write_text('\n'.join(lines),encoding='utf-8')
 result['study_status']='ALL_GATED_STAGES_COMPLETE'; result['backbone_generalization']['positive_backbone_count']=sum(1 for x in backbone.values() if x['cpts_minus_graph_hard']['mean_delta']>0)
 writej(OUT/'results.json',result)
 status={'state':'COMPLETE','stage':'ALL_GATED_STAGES','decision':'CORA_TEST_SUPPORTED','completed_jobs':len(cora_test_tasks)+len(p_tasks)+len(ci_tasks)+len(b_tasks),'test_enabled':True,'no_active_training_jobs':True}; writej(OUT/'status.json',status)
 print(json.dumps({'cora_test':ctest_result,'pubmed':result['pubmed'],'citeseer':result['citeseer'],'backbone_generalization':result['backbone_generalization'],'status':status},indent=2))
if __name__=='__main__': main()
