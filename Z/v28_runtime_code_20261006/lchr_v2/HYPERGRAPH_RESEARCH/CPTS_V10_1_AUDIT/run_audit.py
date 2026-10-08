"""Frozen V10.1 audit; all writes stay in this directory. Resume completed jobs."""
from __future__ import annotations
import concurrent.futures as cf
import datetime as dt
import json, multiprocessing as mp, os, sys, time, traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
HR=ROOT/'HYPERGRAPH_RESEARCH'; OUT=Path(__file__).resolve().parent
V10=HR/'CPTS_V10'; V8=HR/'QTHS_V8_PAPER'; V71=HR/'QTHS_V7_1'
sys.path[:0]=[str(ROOT/'src'),str(V8),str(V10)]
import experiment_v8 as v8
import audit_tail_structure as frozen

def readj(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def writej(p,x):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8'); t.replace(p)
def doc(name,title,x,notes=''):
 (OUT/name).write_text(f'# {title}\n\n{notes}\n\n```json\n'+json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n```\n',encoding='utf-8')
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def summary(x):
 a=np.asarray(x,dtype=float)
 return {'n':len(a),'mean':float(a.mean()),'std':float(a.std()),'median':float(np.median(a)),'min':float(a.min()),'max':float(a.max()),'quantiles_05_25_75_95':np.quantile(a,[.05,.25,.75,.95]).tolist()}
def paired(a,b):
 d=np.asarray(a)-np.asarray(b); rng=np.random.default_rng(1012026)
 ci=np.quantile(d[rng.integers(0,len(d),size=(20000,len(d)))].mean(axis=1),[.025,.975])
 return {'seed_deltas':d.tolist(),'mean_delta':float(d.mean()),'wins':int((d>0).sum()),'n':len(d),'paired_bootstrap_95pct_ci':ci.tolist(),'bootstrap_draws':20000,'bootstrap_seed':1012026}
def state(t,test=False):
 return OUT/'STATE'/('TEST' if test else 'TRAIN')/f"{t['dataset']}_{t.get('backbone','gcn')}_{t['method'].lower()}_seed{t['seed']}.json"
def oldstate(ds,bk,m,s): return V10/'STATE'/f'{ds}_{bk}_{m.lower()}_seed{s}.json'
def trainrec(ds,bk,m,s):
 p=state({'dataset':ds,'backbone':bk,'method':m,'seed':s})
 if p.exists() and readj(p).get('state')=='COMPLETE': return readj(p)
 return readj(oldstate(ds,bk,m,s))
def testrec(ds,m,s):
 p=state({'dataset':ds,'method':m,'seed':s},True)
 if p.exists() and readj(p).get('state')=='COMPLETE': return readj(p)
 return readj(V10/'STATE'/'TEST'/f'{ds}_{m.lower()}_seed{s}.json')
def ids_for(scores,method,seed):
 order,_,tail,*_=frozen.local_cpts(scores)
 if method=='CPTS': return frozen.local_cpts(scores)[-1],tail
 if method=='MATCHED_Q': assigned=np.full(len(tail),int(np.floor(tail.mean()+.5)),dtype=np.int64)
 elif method=='TS_SHUFFLE': assigned=np.random.default_rng(101000+int(seed)).permutation(tail)
 elif method=='TS_REVERSE':
  rows=np.argsort(tail,kind='stable'); assigned=np.empty_like(tail); assigned[rows]=tail[rows][::-1]
 else: raise ValueError(method)
 if method.startswith('TS_') and not np.array_equal(np.sort(assigned),np.sort(tail)): raise RuntimeError('tail multiset changed')
 return order[np.arange(len(tail)),19-assigned],assigned
def detection(scores,save):
 order,x,tail,b,b1,b2,ids=frozen.local_cpts(scores)
 gaps=np.diff(x,axis=1); cp=gaps[np.arange(len(x)),b-1]; loc=gaps.argmax(axis=1)+1
 np.savez_compressed(save,bic1=b1,bic2=b2,delta_bic=b1-b2,boundary=b,tail=tail,gap_cp=cp,gap_max=gaps.max(axis=1),largest_gap_location=loc,cp_equals_largest_gap=b==loc,selected_indices=ids,scores=scores)
 return {'tail_detection_rate':float((tail>0).mean()),'delta_bic':summary(b1-b2),'tail_size':summary(tail),'gap_cp':summary(cp),'gap_max':summary(gaps.max(axis=1)),'cp_equals_largest_gap_fraction':float((b==loc).mean())}
def features(pairs,adj):
 rows=[]
 for u,w in pairs:
  a=adj[int(u)]; b=adj[int(w)]; common=a & b
  rows.append([len(a),len(b),len(common),sum(1/np.log(len(adj[z])) for z in common if len(adj[z])>1),sum(1/len(adj[z]) for z in common)])
 return np.asarray(rows,dtype=float)
def analytical():
 from scipy.interpolate import PchipInterpolator
 from scipy.stats import spearmanr
 result={'study_status':'ANALYTICAL_RUNNING','method':'CPTS','protocol':'STRICT_TRAIN_ONLY','fixed_epoch':10,'M':20,'K':1,'started_utc':now(),'datasets':{},'workspace_verification':{'project':'DCDLP-main','local_root':'E:/我的资料库/Documents/Downloads/DCDLP-main','remote_root':str(ROOT),'workspace_info':'SERVICE_INTERNAL_ERROR','fallback':'Direct matching project and frozen V10 artifact identity after user authorized connection repair and experiment start'}}
 for ds in ('cora','pubmed','citeseer'):
  _,view,pool,scores,ph,_,_,_=v8.dataset_context(ds)
  dsdir=OUT/'ANALYSIS'/ds; dsdir.mkdir(parents=True,exist_ok=True)
  real=detection(scores,dsdir/'real.npz'); tail=frozen.local_cpts(scores)[2]
  count=np.bincount(tail,minlength=21); p=count/len(tail); nz=p[p>0]; entropy=float(-(nz*np.log(nz)).sum())
  heter={'mean':float(tail.mean()),'std':float(tail.std()),'median':float(np.median(tail)),'IQR':float(np.quantile(tail,.75)-np.quantile(tail,.25)),'entropy_nats':entropy,'normalized_entropy':entropy/np.log(18),'entropy_normalizer':'log(18): no-tail plus 17 permitted tail sizes 2..18','CV':float(tail.std()/tail.mean()),'counts_0_to_20':count.tolist(),'fraction_0_to_20':p.tolist(),'buckets_over_10pct':int((p>.1).sum()),'V10_three_bucket_gate':bool((p>.1).sum()>=3)}
  null_a=[]; range_a=[]
  mu=scores.mean(axis=1,keepdims=True); sd=scores.std(axis=1,keepdims=True)
  lo=scores.min(axis=1,keepdims=True); hi=scores.max(axis=1,keepdims=True)
  for seed in (101,102,103):
   z=np.random.default_rng(seed).normal(size=scores.shape); z=(z-z.mean(axis=1,keepdims=True))/z.std(axis=1,keepdims=True)
   a=mu+sd*z
   null_a.append(detection(a,dsdir/f'null_a_{seed}.npz'))
   # Companion addresses the range constraint; affine matching endpoints does not also match moments.
   ar=lo+(hi-lo)*(a-a.min(axis=1,keepdims=True))/(a.max(axis=1,keepdims=True)-a.min(axis=1,keepdims=True))
   range_a.append(detection(ar,dsdir/f'null_a_range_{seed}.npz'))
  sx=np.sort(scores,axis=1,kind='stable'); knots=np.array([0,5,10,14,19])
  smooth=PchipInterpolator(knots,sx[:,knots],axis=1)(np.arange(20))
  nb=detection(smooth,dsdir/'null_b.npz')
  result['datasets'][ds]={'candidate_pool_hash':ph,'real':real,'null_a_replicates':null_a,'null_a_rate':float(np.mean([x['tail_detection_rate'] for x in null_a])),'null_a_range_replicates':range_a,'null_b':nb,'heterogeneity':heter,'matched_q_fixed_removed_count':int(np.floor(tail.mean()+.5))}
  result['datasets'][ds]['TAIL_DETECTOR_NONDISCRIMINATIVE']=bool(result['datasets'][ds]['null_a_rate']>=.9 or nb['tail_detection_rate']>=.9)
  np.savez_compressed(dsdir/'frozen_selection.npz',cpts=frozen.local_cpts(scores)[-1],matched_q=ids_for(scores,'MATCHED_Q',0)[0],true_tail=tail)
  print('ANALYTICAL_COMPLETE',ds,json.dumps({'real':real['tail_detection_rate'],'null_a':result['datasets'][ds]['null_a_rate'],'null_b':nb['tail_detection_rate']}),flush=True)
  if ds!='cora': continue
  ci,ct=ids_for(scores,'CPTS',0); qi,qt=ids_for(scores,'MATCHED_Q',0)
  # Compare actual canonical edges, including duplicate candidates if present.
  same=np.all(np.sort(pool[np.arange(len(pool)),ci],axis=1)==np.sort(pool[np.arange(len(pool)),qi],axis=1),axis=1); d=~same
  shift=(ct+1)-(qt+1)
  disagree={'fraction':float(d.mean()),'same_fraction':float(same.mean()),'LOW_EFFECTIVE_DIFFERENCE':bool(same.mean()>.9),'CPTS_more_hard_fraction_on_D':float((shift[d]<0).mean()),'CPTS_less_hard_fraction_on_D':float((shift[d]>0).mean()),'mean_rank_shift_on_D':float(shift[d].mean()),'rank_shift_definition':'CPTS rank minus Matched-Q rank; negative means harder','rank_shift_distribution_on_D':summary(shift[d])}
  g=view.train_graph(); adj={int(n):set(map(int,g.neighbors(n))) for n in g.nodes()}
  cut=np.quantile(tail,[1/3,2/3]); stratum=np.where(tail<=cut[0],0,np.where(tail<=cut[1],1,2))
  pf=features(view.train_pos,adj); strata={}
  columns=['degree_u','degree_v','CN','AA','RA']
  for code,label in enumerate(('SMALL','MEDIUM','LARGE')):
   mask=stratum==code; item={'n':int(mask.sum()),'tail_size':summary(tail[mask]),'positive_structure':{k:summary(pf[mask,j]) for j,k in enumerate(columns)},'selectors':{}}
   for method in ('CPTS','MATCHED_Q','TS_SHUFFLE'):
    byseed={}
    for s in ((0,1,2,3,4) if method=='TS_SHUFFLE' else (0,)):
     ids,assigned=ids_for(scores,method,s); nf=features(pool[np.arange(len(pool)),ids],adj)
     byseed[str(s)]={'rank_from_hardest':summary((assigned+1)[mask]),'teacher_score':summary(scores[np.arange(len(scores)),ids][mask]),'negative_structure':{k:summary(nf[mask,j]) for j,k in enumerate(columns)}}
    item['selectors'][method]=byseed
   strata[label]=item
  disagree['strata_cutpoints']=cut.tolist(); disagree['strata_tie_policy']='whole equal-tail buckets: <=q1 small, <=q2 medium, rest large; no equal-tail splitting'; disagree['strata']=strata
  result['selection_disagreement']=disagree
  stability=[]
  # Only one original graph-only teacher exists in the frozen teacher directory.
  teacher_dir=HR/'NEGATIVE_V6_1'/'TEACHERS'/'Graph'/'checkpoints'
  checkpoints=list(teacher_dir.glob('*.pt'))
  if len(checkpoints)!=1: raise RuntimeError('Teacher inventory changed; inspect teachers before perturbation fallback')
  for s in (0,1,2):
   pert=scores+np.random.default_rng(20261010+s).normal(size=scores.shape)*sd*.01
   _,_,pt,pb,_,_,pi=frozen.local_cpts(pert); base_b=frozen.local_cpts(scores)[3]
   stability.append({'seed':s,'tail_size_spearman':float(spearmanr(tail,pt).statistic),'boundary_exact_match':float((base_b==pb).mean()),'selected_negative_match':float(np.all(np.sort(pool[np.arange(len(pool)),ci],axis=1)==np.sort(pool[np.arange(len(pool)),pi],axis=1),axis=1).mean())})
  result['teacher_stability']={'mode':'DETERMINISTIC_SCORE_PERTURBATION','eligible_frozen_graph_only_teachers':list(map(str,checkpoints)),'row_std_multiplier':.01,'replicates':stability,'cross_teacher_stability':'NOT_MEASURED_NO_MULTIPLE_FROZEN_GRAPH_ONLY_TEACHERS','TAIL_BOUNDARY_UNSTABLE':'UNCONFIRMED: report continuous stability; task supplied no numerical flag threshold'}
 v10=readj(V10/'results.json'); cv=readj(V10/'cora_validation_results.json')
 vd=np.mean([float(cv['methods_mrr_by_seed']['CPTS'][str(s)])-float(cv['methods_mrr_by_seed']['MATCHED_Q'][str(s)]) for s in range(3)])
 td=v10['cora_test']['paired_cpts_delta']['MATCHED_Q']['mean_delta']
 result['five_seed_gate']={'validation_delta':float(vd),'cached_test_delta':float(td),'threshold':.005,'triggered':bool(abs(vd)<.005 or abs(td)<.005),'interpretation':'Extend if either existing validation or test mean is close; V10.1 explicitly cites test closeness. All controls and rule frozen before new tests.'}
 result['V10_reused_summary']={'study_status':v10['study_status'],'final_decision':v10.get('final_decision'),'backbone_generalization':v10.get('backbone_generalization'),'cora_test':v10['cora_test'],'cora_validation':cv}
 result['study_status']='ANALYTICAL_COMPLETE_TRAINING_PENDING'; writej(OUT/'results.json',result)
 doc('00_V10_AUDIT.md','V10 frozen artifact audit',result['V10_reused_summary'],'V10 outputs are read-only. Fixed M=20,K=1, original graph teacher, BIC penalty, b=2..18, stable ordering, exact selection, raw hypergraph, epoch10. Workspace service failed; direct project/artifact verification recorded in results.json.')
 doc('01_NULL_TAIL_AUDIT.md','Null tail detection audit',{ds:{k:v for k,v in x.items() if k not in ('heterogeneity','candidate_pool_hash')} for ds,x in result['datasets'].items()},'Null A: Gaussian draws, row-standardized to exactly match empirical mean/std (range varies). A_RANGE is endpoint-matched companion (moments vary); both are affine-equivalent for BIC. Null B: monotone C1 PCHIP interpolation through ranks 0,5,10,14,19, preserves endpoints and coarse marginal; empirical moments may change. Three A seeds 101/102/103. All realized vectors and diagnostics retained; no held-out labels. No detector changes.')
 doc('02_TAIL_HETEROGENEITY.md','Tail heterogeneity',{ds:x['heterogeneity'] for ds,x in result['datasets'].items()})
 doc('05_SELECTION_DISAGREEMENT.md','Selection disagreement and shape strata',disagree,'Features use only training graph. Rank1=hardest. All shuffle seeds retained separately. This is an analysis of selections, not per-stratum held-out performance.')
 doc('07_TEACHER_STABILITY.md','Teacher boundary stability',result['teacher_stability'],'Perturbation is analysis only and is never used in training.')
 for name,title in [('03_TAIL_SIZE_SHUFFLE.md','Tail size controls'),('04_MATCHED_Q_5SEED.md','Matched-Q five seeds'),('06_CROSS_DATASET_TEST.md','Cross-dataset frozen test'),('PAPER_CLAIM_MATRIX.md','Claim matrix'),('FINAL_REPORT.md','Final report')]:
  doc(name,title,{'status':'PENDING_TRAINING_AND_TEST','five_seed_gate':result['five_seed_gate']})
 return result

def train_worker(t):
 v8.worker_init(); import torch
 old=v8.configure_backbone(t['backbone']); start=time.perf_counter(); p=state(t)
 try:
  writej(p,{'state':'RUNNING','task':t,'pid':os.getpid(),'started_utc':now()})
  _,view,pool,scores,ph,vpos,vneg,vhash=v8.dataset_context(t['dataset'])
  ids,tail=ids_for(scores,t['method'],t['seed']); selected=pool[np.arange(len(pool)),ids].copy()
  _,forbidden=v8.v61.make_train_forbidden(view)
  if any(v8.v61.canonical_edge(x) in forbidden for x in selected): raise RuntimeError('train-forbidden selected edge')
  if t['dataset']=='cora' and t['method'] in ('CPTS','MATCHED_Q'):
   with np.load(V10/'cora_selector_indices.npz',allow_pickle=False) as z:
    if not np.array_equal(ids,z[t['method'].lower()]): raise RuntimeError('V10 selector changed')
  rel=Path('HYPERGRAPH_RESEARCH')/OUT.name/'RUNS'/t['dataset'].upper()/t['backbone'].upper()/t['method']/f"seed{t['seed']}"
  (ROOT/rel).mkdir(parents=True,exist_ok=True)
  np.savez_compressed(ROOT/rel/'selection_audit.npz',selected_indices=ids,assigned_tail_size=tail)
  v8.engine.candidate_pool=pool; v8.engine.candidate_pool_hash=ph; v8.engine.validation_candidate_hash=vhash
  print('TRAIN_START',json.dumps(t),'pid',os.getpid(),flush=True)
  torch.cuda.reset_peak_memory_stats()
  rec=v8.engine.train_one(view,t['method'],int(t['seed']),selected,rel.as_posix(),vpos,vneg,initialize_from_v6=False,dataset_name=t['dataset'],hypergraph_mode='raw')
  met,params=v8.metric_for_checkpoint(rec['checkpoint'],view,vpos,vneg)
  if rec['epoch_count']!=10 or abs(met['mrr']-rec['epoch10_validation_mrr'])>1e-9: raise RuntimeError('fixed epoch10 gate failed')
  out={'state':'COMPLETE','task':t,'training_record':rec,'validation_metrics':met,'trainable_parameters':params,'train_pool_hash':ph,'validation_candidate_hash':vhash,'peak_gpu_memory_mb':float(torch.cuda.max_memory_allocated()/1024**2),'wall_seconds':time.perf_counter()-start,'completed_utc':now(),'test_evaluated':False}
  writej(p,out); print('TRAIN_COMPLETE',json.dumps(t),met['mrr'],flush=True); return out
 except Exception as e:
  writej(p,{'state':'FAILED','task':t,'error':repr(e),'traceback':traceback.format_exc()}); raise
 finally: v8.v61.load_json=old

def test_worker(t):
 v8.worker_init(); old=v8.configure_backbone('gcn'); p=state(t,True)
 try:
  _,view=v8.base.init_dataset(t['dataset'])
  ev=(V71 if t['dataset']=='citeseer' else V8)/'EVALUATION'
  with np.load(ev/f"{t['dataset']}_test_candidates.npz",allow_pickle=False) as z: pos=z['test_positive'].copy(); neg=z['test_negative_candidates'].copy()
  expected={'cora':'ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92','pubmed':'1e6a1d3fd4031479dbe0c4d1a5999b22812401cde214048645ab875c1428bf4b','citeseer':'48b69dc30431358d9c47d9792d1e1604a327a1d40c9fa440b53ed3c688470a26'}
  if v8.v61.array_hash(neg)!=expected[t['dataset']]: raise RuntimeError('frozen test hash mismatch')
  rec=trainrec(t['dataset'],'gcn',t['method'],t['seed']); checkpoint=rec['training_record']['checkpoint']
  met,params=v8.metric_for_checkpoint(checkpoint,view,pos,neg)
  out={'state':'COMPLETE','task':t,'checkpoint':checkpoint,'candidate_hash':expected[t['dataset']],'positive_hash':v8.v61.array_hash(pos),'test_metrics':met,'trainable_parameters':params,'completed_utc':now()}
  writej(p,out); print('TEST_COMPLETE',json.dumps(t),met['mrr'],flush=True); return out
 except Exception as e:
  writej(p,{'state':'FAILED','task':t,'error':repr(e),'traceback':traceback.format_exc()}); raise
 finally: v8.v61.load_json=old

def parallel(stage,tasks,worker,workers,test=False):
 pending=[t for t in tasks if not state(t,test).exists() or readj(state(t,test)).get('state')!='COMPLETE']
 status={'state':'RUNNING','stage':stage,'total_jobs':len(tasks),'completed_jobs':len(tasks)-len(pending),'workers':min(workers,len(pending)),'updated_utc':now(),'supervisor_pid':os.getpid()}
 writej(OUT/'status.json',status)
 if not pending: return
 errors=[]
 with cf.ProcessPoolExecutor(max_workers=min(workers,len(pending)),mp_context=mp.get_context('spawn')) as ex:
  futs={ex.submit(worker,t):t for t in pending}
  for f in cf.as_completed(futs):
   try: f.result(); status['completed_jobs']+=1
   except Exception as e: errors.append({'task':futs[f],'error':repr(e)})
   status.update(last_finished=futs[f],updated_utc=now(),errors=errors); writej(OUT/'status.json',status)
 if errors: raise RuntimeError(json.dumps(errors))

def validation_summary(result):
 n=5 if result['five_seed_gate']['triggered'] else 3
 vals={m:[trainrec('cora','gcn',m,s)['validation_metrics']['mrr'] for s in range(n)] for m in ('CPTS','MATCHED_Q','TS_SHUFFLE')}
 rev=[trainrec('cora','gcn','TS_REVERSE',s)['validation_metrics']['mrr'] for s in range(3)]
 sh=paired(vals['CPTS'][:3],vals['TS_SHUFFLE'][:3]); re=paired(vals['CPTS'][:3],rev)
 result['cora_validation']={'mrr_by_seed':dict(vals,TS_REVERSE=rev),'CPTS_vs_TS_SHUFFLE_3seed':sh,'CPTS_vs_TS_REVERSE_3seed':re,'CPTS_vs_MATCHED_Q':paired(vals['CPTS'],vals['MATCHED_Q']),'CPTS_vs_TS_SHUFFLE':paired(vals['CPTS'],vals['TS_SHUFFLE']),'LOCAL_PAIRING_SIGNAL':bool(sh['wins']>=2 and sh['mean_delta']>.002)}
 bk={}
 for b in ('gcn','sage','gat'):
  cp=trainrec('cora',b,'CPTS',0)['validation_metrics']['mrr']; mq=trainrec('cora',b,'MATCHED_Q',0)['validation_metrics']['mrr']; bk[b]={'seed':0,'CPTS':cp,'MATCHED_Q':mq,'delta':cp-mq}
 result['backbone_matched_seed0_sanity']=bk
 doc('03_TAIL_SIZE_SHUFFLE.md','Tail size shuffle and reverse controls',result['cora_validation'],'Seeds0/1/2 primary validation, fixed epoch10. TS-SHUFFLE permutation seed=101000+training seed. TS-REVERSE stable tail-sort, reverse assignment. Both preserve exact tail multiset; sorted tie assignment deterministic. LOCAL_PAIRING_SIGNAL requires >=2/3 wins and mean>.002.')
 writej(OUT/'results.json',result)

def finalize(result):
 n=5 if result['five_seed_gate']['triggered'] else 3
 ctest={m:[testrec('cora',m,s)['test_metrics']['mrr'] for s in range(n)] for m in ('CPTS','MATCHED_Q','TS_SHUFFLE')}
 cpaired={m:paired(ctest['CPTS'],ctest[m]) for m in ('MATCHED_Q','TS_SHUFFLE')}
 result['cora_test_extension']={'mrr_by_seed':ctest,'paired':cpaired,'baseline_three_seeds':readj(V10/'results.json')['cora_test']}
 vr=readj(V8/'results.json'); v71=readj(V71/'results.json'); cross={}
 cross['cora']={m:x['by_seed'] for m,x in result['cora_test_extension']['baseline_three_seeds']['methods_mrr'].items() if m in ('CPTS','GRAPH_HARD','SH75','MATCHED_Q','QTHS25')}
 cross['pubmed']={m:vr['pubmed']['test'][m]['by_seed'] for m in ('GRAPH_HARD','QTHS25')}
 cross['citeseer']={'GRAPH_HARD':[v71['citeseer']['test']['by_method_seed']['C1_GRAPH_HARD'][str(s)]['mrr'] for s in range(3)]}
 for ds in ('pubmed','citeseer'):
  for m in ('CPTS','SH75','MATCHED_Q'): cross[ds][m]=[testrec(ds,m,s)['test_metrics']['mrr'] for s in range(3)]
 cross_summary={ds:{'mrr_by_seed':ms,'means':{m:float(np.mean(x)) for m,x in ms.items()},'paired_CPTS':{m:paired(ms['CPTS'],x) for m,x in ms.items() if m!='CPTS'}} for ds,ms in cross.items()}
 wins=sum(x['means']['CPTS']>x['means']['GRAPH_HARD'] for x in cross_summary.values())
 other=any(all(cross_summary[ds]['means']['CPTS']-cross_summary[ds]['means'][m]>=-.005 for m in ('SH75','MATCHED_Q')) for ds in ('pubmed','citeseer'))
 general=bool(wins>=2 and other); result['cross_dataset_test']={'datasets':cross_summary,'datasets_above_graph_hard':wins,'outside_cora_not_dominated_by_both_fixed_controls':other,'CPTS_GENERALIZATION_SUPPORTED':general}
 cv=result['cora_validation']; nullfail=any(x['TAIL_DETECTOR_NONDISCRIMINATIVE'] for x in result['datasets'].values())
 # "Clearly fails" is operationalized before new results as CI upper<0 or mean<-.005.
 mq=cpaired['MATCHED_Q']; matched_ok=bool(mq['mean_delta']>=-.005 and mq['paired_bootstrap_95pct_ci'][1]>=0)
 reverse_ok=bool(cv['CPTS_vs_TS_REVERSE_3seed']['wins']>=2 and cv['CPTS_vs_TS_REVERSE_3seed']['mean_delta']>.002)
 gates={'CPTS_above_Graph_hard':cross_summary['cora']['means']['CPTS']>cross_summary['cora']['means']['GRAPH_HARD'],'five_seed_matched_not_clear_failure':matched_ok,'local_shuffle_signal':cv['LOCAL_PAIRING_SIGNAL'],'reverse_pairing_signal':reverse_ok,'null_detector_discriminative':not nullfail,'cross_dataset_generalization':general}
 all_ok=all(gates.values()); decision='FREEZE_CPTS' if all_ok else ('CHANGE_POINT_DETECTOR_NOT_VALIDATED' if nullfail else ('ADAPTIVITY_NOT_NECESSARY' if not cv['LOCAL_PAIRING_SIGNAL'] or not reverse_ok or not matched_ok else 'CPTS_GENERALIZATION_WEAK'))
 result.update(study_status='COMPLETE',completed_utc=now(),claim_gates=gates,final_decision=decision,ADAPTIVITY_NECESSARY='YES' if all_ok else ('NO' if not cv['LOCAL_PAIRING_SIGNAL'] or not reverse_ok or not matched_ok else 'UNCONFIRMED'),PAPER_STORY_SUPPORTED='YES' if all_ok else 'PARTIAL',NOVELTY_STATUS='EXACT_RULE_UNVERIFIED',NEXT_EXPECTED_STEP='Freeze audit; report empirical hardness-region effects and failed claim gates; no CPTS modification in this round.')
 doc('04_MATCHED_Q_5SEED.md','Matched-Q five-seed audit',{'gate':result['five_seed_gate'],'validation':cv,'test':result['cora_test_extension']},'20,000 paired seed-bootstrap draws, seed1012026, percentile95%CI; five seeds still give limited precision. No adaptive tuning. Original seeds0..2 reused exactly.')
 doc('06_CROSS_DATASET_TEST.md','Cross-dataset frozen test',result['cross_dataset_test'],'All comparisons use seeds0/1/2. Original Graph-hard/QTHS25 metrics reused, frozen CPTS/SH75 epoch10 checkpoints evaluated once, Matched-Q uses matched epoch10 reruns. No test-based selection.')
 doc('PAPER_CLAIM_MATRIX.md','Paper claim matrix',{'gates':gates,'backbone_mechanism_sanity':result['backbone_matched_seed0_sanity'],'decision':decision},'Per-positive tail detection claim requires every gate. Reverse signal operationalized as shuffle gate: >=2/3wins and mean>.002. Matched-Q clear failure: mean<-.005 or bootstrap CI wholly negative. Thresholds registered before new tests. Empirical performance does not validate a real extreme-tail regime when null detection>=90%.')
 doc('FINAL_REPORT.md','CPTS V10.1 final report',result,'Final decision precedence: detector failure, local-adaptivity failure, generalization failure. Multiple failures are preserved in claim_gates. No priority claim. Full row diagnostics in ANALYSIS; models/states retained in RUNS/STATE.')
 writej(OUT/'results.json',result); writej(OUT/'status.json',{'state':'COMPLETE','stage':'ALL_AUDITS','completed_utc':now(),'final_decision':decision,'no_active_training_jobs':True})
 print('AUDIT_COMPLETE',decision,flush=True)

def main():
 import fcntl
 OUT.mkdir(parents=True,exist_ok=True)
 lock=(OUT/'supervisor.lock').open('w'); fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 (OUT/'supervisor.pid').write_text(str(os.getpid()))
 if '--preflight' in sys.argv:
  v8.base.ensure_expected_runtime(); analytical(); return
 try:
  v8.base.ensure_expected_runtime()
  result=readj(OUT/'results.json') if (OUT/'results.json').exists() else analytical()
  if result.get('study_status')=='COMPLETE': print('Already complete',flush=True); return
  ext=result['five_seed_gate']['triggered']
  # Start large PubMed jobs first; remaining workers finish controls while those run.
  tasks=[{'dataset':'pubmed','backbone':'gcn','method':'MATCHED_Q','seed':s} for s in range(3)]
  tasks += [{'dataset':'cora','backbone':'gcn','method':m,'seed':s} for m in ('TS_SHUFFLE','TS_REVERSE') for s in range(3)]
  if ext: tasks += [{'dataset':'cora','backbone':'gcn','method':m,'seed':s} for m in ('CPTS','MATCHED_Q','TS_SHUFFLE') for s in (3,4)]
  tasks += [{'dataset':'citeseer','backbone':'gcn','method':'MATCHED_Q','seed':s} for s in range(3)]
  tasks += [{'dataset':'cora','backbone':bk,'method':'MATCHED_Q','seed':0} for bk in ('sage','gat')]
  writej(OUT/'execution_plan.json',{'frozen_protocol':'V10 exact CPTS; strict_train_only; M20K1; fixed_epoch10','training_jobs':tasks,'workers':6,'cpu_threads_per_worker':4,'five_seed_gate':result['five_seed_gate'],'registered_claim_gate_operationalization':{'reverse_signal':'>=2/3 wins and mean gain>.002','matched_clear_failure':'mean<-.005 OR paired bootstrap CI upper<0'},'server_connection':'SSH independently verified; workspace query service unavailable','stop_session_when':'detached supervisor and real GPU training stable; no long monitoring'})
  result['study_status']='TRAINING_RUNNING'; writej(OUT/'results.json',result)
  parallel('FROZEN_VALIDATION_TRAINING',tasks,train_worker,6)
  validation_summary(result)
  tests=[{'dataset':ds,'backbone':'gcn','method':m,'seed':s} for ds in ('pubmed','citeseer') for m in ('CPTS','SH75','MATCHED_Q') for s in range(3)]
  if ext:
   tests += [{'dataset':'cora','backbone':'gcn','method':'TS_SHUFFLE','seed':s} for s in range(3)]
   tests += [{'dataset':'cora','backbone':'gcn','method':m,'seed':s} for m in ('CPTS','MATCHED_Q','TS_SHUFFLE') for s in (3,4)]
  else: tests += [{'dataset':'cora','backbone':'gcn','method':'TS_SHUFFLE','seed':s} for s in range(3)]
  result['study_status']='FROZEN_TEST_RUNNING'; writej(OUT/'results.json',result)
  parallel('FROZEN_CHECKPOINT_TEST',tests,test_worker,3,True)
  finalize(result)
 except Exception as e:
  writej(OUT/'status.json',{'state':'FAILED','error':repr(e),'traceback':traceback.format_exc(),'updated_utc':now()}); print(traceback.format_exc(),flush=True); raise
if __name__=='__main__': main()
