from __future__ import annotations
import os
os.environ.setdefault('DGLBACKEND','pytorch')
os.environ.setdefault('OMP_NUM_THREADS','4')
os.environ.setdefault('OPENBLAS_NUM_THREADS','4')
os.environ.setdefault('MKL_NUM_THREADS','4')
import ast, csv, gc, hashlib, importlib.util, json, random, subprocess, sys, time, traceback
from pathlib import Path
from types import SimpleNamespace
OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parent
sys.path.insert(0,str(OUT/'.deps'))
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,indent=2,allow_nan=False));os.replace(tmp,p)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
f=load('audit173_parent',ROOT/'HSPE_V17_2/scripts/hspe_v17_2.py')
np=f.np;torch=f.torch
from dcdlp.evaluation.ranking import ranking_metrics
torch.set_num_threads(int(os.environ.get('OMP_NUM_THREADS',4)))
METRICS=('mrr','hits10','hits20','mean_positive_rank')
DATASETS=('cora','pubmed','citeseer')
def sources():return f.m.sources()
def context(ds):
 full,view=f.m.p.v16.base.init_dataset(ds)
 if ds=='citeseer':
  with np.load(ROOT/'HSPE_V17_2/third/citeseer/context.npz') as z:vp=z['valid_pos'].copy();vn=z['valid_neg'].copy()
 else:
  # Reuse exact frozen validation candidates; avoid loading token features/teachers.
  vp=f.m.p.v16.stage0.canonical_pairs(np.asarray(full.valid_pos,np.int64))
  vn,_=f.m.p.v16.make_validation_candidates(view,vp)
 with np.load(ROOT/'HSPE_V17_2/candidates'/f'{ds}_test.npz') as z:tp=z['positive'].copy();tn=z['negative'].copy()
 meta=read(ROOT/'HSPE_V17_2/candidates'/f'{ds}_test.json')
 ah=f.m.p.v16.v61.array_hash
 assert ah(tp)==meta['positive_hash'] and ah(tn)==meta['negative_hash']
 if 'train_positive_hash' in meta:
  assert ah(view.train_pos)==meta['train_positive_hash']
  assert ah(vn)==f.parent_row(ds,0,'H2_R_HSPE')['validation_candidate_hash']
 else:
  canonical=f.m.p.v16.stage0.canonical_pairs(np.asarray(view.train_pos,np.int64))
  assert ah(canonical)==read(ROOT/'HSPE_V17_2/third/citeseer/input_audit.json')['train_hash']
 return view,vp,vn,tp,tn
def preflight():
 frozen=ROOT/'R_HSPE_FROZEN';assert 'FROZEN' in (frozen/'R_HSPE_FROZEN.md').read_text()
 manifest=read(frozen/'SOURCE_HASHES.json');assert manifest['sources']==sources()
 for path,expected in manifest['runtime_python_source_hashes'].items():assert sha(path)==expected,('RUNTIME_SOURCE_MISMATCH',path)
 assert read(ROOT/'HSPE_V17_2/status.json')['state']=='COMPLETE'
 before={str(p.relative_to(frozen)):sha(p) for p in frozen.rglob('*') if p.is_file()}
 audits={}
 for ds in DATASETS:
  view,vp,vn,tp,tn=context(ds); train=f.m.p.v16.stage0.canonical_pairs(np.asarray(view.train_pos,np.int64))
  forbidden=set(map(tuple,train.tolist())); assert not any(tuple(x) in forbidden for x in tp.tolist())
  # Heldout truth is used only in this audit, never in training filters.
  assert not set(map(tuple,vp.tolist())).intersection(forbidden)
  n=view.num_nodes;arrhash=f.m.p.v16.v61.array_hash
  assert f.m.p.v16.base.split_hash(view)==manifest['dataset_split_hashes'][ds]['training_view_split_hash']
  audits[ds]={'n':n,'feature_shape':list(view.features.shape),'train_edges':len(train),'train_hash':arrhash(view.train_pos),'valid_positive_hash':arrhash(vp),'valid_negative_hash':arrhash(vn),'test_positive_hash':arrhash(tp),'test_negative_hash':arrhash(tn),'test_cache_sha256':sha(ROOT/'HSPE_V17_2/candidates'/f'{ds}_test.npz'),'test_queries':len(tp),'test_negatives':int(tn.shape[1]),'projection':'undirected train edges exactly B0 graph side; no clique expansion, no valid/test edges'}
  write(OUT/'input_audit'/f'{ds}.json',audits[ds])
  p=OUT/'input_cache'/f'{ds}.npz';p.parent.mkdir(parents=True,exist_ok=True)
  np.savez(p,x=view.features,train=train,valid_pos=vp,valid_neg=vn,test_pos=tp,test_neg=tn)
  del view;gc.collect()
 write(OUT/'FROZEN_AUDIT.json',{'state':'PASS','frozen_files':before,'frozen_config_sha256':sha(frozen/'FINAL_CONFIG.json'),'frozen_test_results_sha256':sha(frozen/'TEST_RESULTS.json'),'source_hashes':sources(),'runtime_python_source_hashes':manifest['runtime_python_source_hashes'],'datasets':audits,'runtime_evaluator_sha256':sha(Path(f.m.p.v16.ROOT)/'src/dcdlp/evaluation/ranking.py')})
 return audits
def inputs(ds):
 with np.load(OUT/'input_cache'/f'{ds}.npz') as z:return {k:z[k].copy() for k in z.files}
def extracted(path,names,scope):
 t=ast.parse(Path(path).read_text());nodes=[x for x in t.body if isinstance(x,(ast.FunctionDef,ast.ClassDef)) and x.name in names]
 assert {x.name for x in nodes}==set(names)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),scope);return scope
def jobpath(ds,method,seed):return OUT/'runs'/ds/method/f'seed_{seed}'
def stat(values):
 r=f.stat(values) if len(values)>1 else {'mean':float(values[0]),'std':None,'median':float(values[0]),'min':float(values[0]),'max':float(values[0]),'per_seed':values}
 return r
def metriccell(mm):return f"{mm['mean']:.6f} ± "+(f"{mm['std']:.6f}" if mm['std'] is not None else 'NA (one seed)')
def prog(job,**kw):write(job/'progress.json',{'updated':time.time(),**kw})
def official_ncn():
 vendor=next((OUT/'vendor').glob('NeuralCommonNeighbor-*'));sys.path.insert(0,str(vendor))
 # Explicit aliases avoid an unrelated project's module named utils/model.
 u=load('utils',vendor/'utils.py');m=load('model',vendor/'model.py')
 import torch.nn.functional as F
 from torch_sparse import SparseTensor
 from torch_geometric.utils import negative_sampling
 scope={'torch':torch,'np':np,'F':F,'SparseTensor':SparseTensor,'negative_sampling':negative_sampling,'PermIterator':u.PermIterator,'Iterable':__import__('typing').Iterable}
 extracted(vendor/'NeighborOverlap.py',{'train','set_seed'},scope)
 return m,scope
NCFG={
 'cora':dict(xdp=.7,tdp=.3,pt=.75,preedp=.4,predp=.05,gnndp=.05,scale=4.3,offset=2.8,alpha=1.,gnnlr=.0043,prelr=.0024,batch=1152,twolayerlin=False),
 'citeseer':dict(xdp=.4,tdp=0.,pt=.75,preedp=0.,predp=.55,gnndp=.75,scale=6.5,offset=4.4,alpha=.4,gnnlr=.0085,prelr=.0078,batch=384,twolayerlin=True),
 'pubmed':dict(xdp=.3,tdp=0.,pt=.5,preedp=0.,predp=.05,gnndp=.1,scale=5.3,offset=.5,alpha=.3,gnnlr=.0097,prelr=.002,batch=2048,twolayerlin=False)}
def ncn(ds,method,seed,smoke=False):
 from torch_sparse import SparseTensor
 job=jobpath(ds,method,seed);job.mkdir(parents=True,exist_ok=True);dest=job/'result.json'
 if dest.exists() and not smoke:return
 m,scope=official_ncn();scope['set_seed'](seed);random.seed(seed)
 a=inputs(ds);dev=torch.device('cuda');x=torch.as_tensor(a['x'],dtype=torch.float32,device=dev);n=len(x)
 train=torch.as_tensor(a['train'],dtype=torch.long,device=dev);ei=torch.cat((train.t(),train.t().flip(0)),dim=1)
 adj=SparseTensor.from_edge_index(ei,sparse_sizes=(n,n)).to_symmetric().coalesce()
 data=SimpleNamespace(x=x,edge_index=ei,adj_t=adj,num_nodes=n);c=NCFG[ds]
 model=m.GCN(x.shape[1],256,256,1,c['gnndp'],True,False,-1,'puregcn',True,0.,xdropout=c['xdp'],taildropout=c['tdp'],noinputlin=False).to(dev)
 kwargs=dict(cndeg=-1,use_xlin=True,tailact=True,twolayerlin=c['twolayerlin'],beta=1.)
 if method=='NCNC':kwargs.update(depth=1,splitsize=131072,scale=c['scale'],offset=c['offset'],trainresdeg=-1,testresdeg=-1,pt=c['pt'],learnablept=False,alpha=c['alpha'])
 predictor=m.predictor_dict['cn1' if method=='NCN' else 'incn1cn1'](256,256,1,3,c['predp'],c['preedp'],True,**kwargs).to(dev)
 optimizer=torch.optim.Adam([{'params':model.parameters(),'lr':c['gnnlr']},{'params':predictor.parameters(),'lr':c['prelr']}])
 parameters=sum(p.numel() for obj in (model,predictor) for p in obj.parameters());start=time.perf_counter();trainsec=0.;best=-float('inf');bestepoch=None
 torch.cuda.reset_peak_memory_stats()
 def evaluate(pos,neg,save=None):
  model.eval();predictor.eval();torch.cuda.synchronize();st=time.perf_counter()
  with torch.no_grad():
   h=model(x,adj)
   def score(pairs):
    parts=[]
    # API batching only. Completion split limits memory without changing neighborhoods.
    for i in range(0,len(pairs),512 if method=='NCNC' else 8192):
     edge=torch.as_tensor(pairs[i:i+(512 if method=='NCNC' else 8192)],dtype=torch.long,device=dev).t()
     parts.append(predictor(h,adj,edge).flatten().cpu().numpy())
    return np.concatenate(parts)
   ps=score(pos);ns=score(neg.reshape(-1,2)).reshape(len(pos),neg.shape[1])
  torch.cuda.synchronize();elapsed=time.perf_counter()-st;metrics=ranking_metrics(ps,ns)
  if save is not None:np.savez_compressed(save,positive=ps,negative=ns)
  return metrics,elapsed
 epochs=1 if smoke else 100
 for epoch in range(1,epochs+1):
  torch.cuda.synchronize();t=time.perf_counter();loss=scope['train'](model,predictor,data,{'train':{'edge':train}},optimizer,c['batch'],True,[],None);torch.cuda.synchronize();trainsec+=time.perf_counter()-t
  assert np.isfinite(loss)
  metrics,es=evaluate(a['valid_pos'],a['valid_neg'])
  if metrics['mrr']>best:
   best=metrics['mrr'];bestepoch=epoch
   torch.save({'model':model.state_dict(),'predictor':predictor.state_dict(),'epoch':epoch,'valid':metrics},job/'best.pt')
  prog(job,state='SMOKE' if smoke else 'RUNNING',epoch=epoch,epochs=epochs,loss=float(loss),valid_mrr=metrics['mrr'],best_valid_mrr=best,train_seconds=trainsec,elapsed_seconds=time.perf_counter()-start,parameters=parameters)
  print(ds,method,seed,epoch,loss,metrics['mrr'],flush=True)
 checkpoint=torch.load(job/'best.pt',map_location=dev,weights_only=False);model.load_state_dict(checkpoint['model']);predictor.load_state_dict(checkpoint['predictor'])
 if smoke:write(job/'smoke.json',{'state':'PASS','parameters':parameters,'validation':checkpoint['valid']});return
 metrics,inference=evaluate(a['test_pos'],a['test_neg'],job/'test_scores.npz')
 result={'state':'COMPLETE','dataset':ds,'method':method,'seed':seed,'metrics':metrics,'parameters':parameters,'train_seconds':trainsec,'total_seconds':time.perf_counter()-start,'inference_seconds':inference,'peak_gpu_allocated_mb':torch.cuda.max_memory_allocated()/1024**2,'config':{**c,'hidden':256,'layers':1,'epochs':100,'predictor_layers':3,'maskinput':True,'splitsize':131072 if method=='NCNC' else None},'best_epoch':bestepoch,'best_validation':checkpoint['valid'],'selection':'validation MRR only; first maximum; test evaluated once','official_source':read(OUT/'NCN_source.json'),'candidate_audit':read(OUT/'input_audit'/f'{ds}.json'),'negative_filter':'official PyG negative_sampling; training graph only'}
 write(dest,result);prog(job,state='COMPLETE',epoch=100)
def official_nslr():
 vendor=next((OUT/'vendor').glob('NSLR-HMANN-*'));sys.path.insert(0,str(vendor))
 import networkx as nx
 if not hasattr(nx,'from_numpy_matrix'):nx.from_numpy_matrix=nx.from_numpy_array
 att=load('nslr_attention173',vendor/'attention.py');hg=load('nslr_hypergraph173',vendor/'Hypergraph.py')
 import dgl,dgl.function as fn,torch.nn as nn,torch.nn.functional as F
 scope={'nn':nn,'F':F,'torch':torch,'fn':fn}
 extracted(vendor/'train.py',{'MLPPredictor','compute_loss'},scope)
 return att,hg,scope,dgl
def nslr_prepare(ds):
 dest=OUT/'nslr_cache'/ds;dest.mkdir(parents=True,exist_ok=True)
 if (dest/'metadata.json').exists():return
 att,hg,s,dgl=official_nslr();a=inputs(ds);n=len(a['x']);start=time.perf_counter()
 # Official dense NSLR construction, alpha=1, threshold=.25, nonbinary incidence.
 A=np.eye(n);tr=a['train'];A[tr[:,0],tr[:,1]]=1.;A[tr[:,1],tr[:,0]]=1.
 write(dest/'progress.json',{'state':'DENSE_OFFICIAL_CONSTRUCTION','n':n,'started':time.time(),'blas_threads':os.environ['OMP_NUM_THREADS']})
 graph,H=hg.construct_hypergraph(A,is_binary=False)
 assert np.isfinite(H).all();g=dgl.add_self_loop(dgl.from_networkx(graph));np.save(dest/'H.npy',H.astype(np.float32));dgl.save_graphs(str(dest/'graph.bin'),[g])
 write(dest/'metadata.json',{'state':'COMPLETE','n':n,'graph_edges':int(g.num_edges()),'construction_seconds':time.perf_counter()-start,'incidence_sha256':sha(dest/'H.npy'),'graph_sha256':sha(dest/'graph.bin'),'official_source':read(OUT/'NSLR-HMANN_source.json'),'train_hash':read(OUT/'input_audit'/f'{ds}.json')['train_hash'],'selfloops':'official loader adds selfloops before NSLR; constructor unchanged'})
def nslr(ds,seed,smoke=False):
 job=jobpath(ds,'NSLR-HMANN',seed);job.mkdir(parents=True,exist_ok=True);dest=job/'result.json'
 if dest.exists() and not smoke:return
 att,hg,s,dgl=official_nslr();torch.manual_seed(seed);np.random.seed(seed);random.seed(seed)
 cache=OUT/'nslr_cache'/ds;g=dgl.load_graphs(str(cache/'graph.bin'))[0][0].to('cuda');H=torch.as_tensor(np.load(cache/'H.npy'),device='cuda');a=inputs(ds);n=len(a['x'])
 # Official random 64-dimensional features are not optimizer parameters.
 x=torch.nn.Embedding(n,64).weight.detach().to('cuda')
 model=att.Multi_view_Attention(64,32,32,[8,2],.5).to('cuda');pred=s['MLPPredictor'](32).to('cuda')
 optim=torch.optim.Adam(list(model.parameters())+list(pred.parameters()),lr=.01)
 tr=a['train'];directed=np.vstack((tr,tr[:,::-1]));forbid=set((directed[:,0]*n+directed[:,1]).tolist());rng=np.random.RandomState(seed)
 # Uniform fixed sample, with replacement, from train-only off-diagonal complement.
 negatives=[]
 while len(negatives)<len(directed):
  pairs=rng.randint(0,n,size=(len(directed),2))
  negatives.extend([p for p in pairs.tolist() if p[0]!=p[1] and p[0]*n+p[1] not in forbid])
 neg=np.asarray(negatives[:len(directed)],np.int64)
 pg=dgl.add_self_loop(dgl.graph((directed[:,0],directed[:,1]),num_nodes=n)).to('cuda');ng=dgl.add_self_loop(dgl.graph((neg[:,0],neg[:,1]),num_nodes=n)).to('cuda')
 def evaluate(pos,neg,save=None):
  model.eval();pred.eval();torch.cuda.synchronize();st=time.perf_counter()
  with torch.no_grad():
   h=model(g,x,H)
   def score(pairs):
    all=[]
    for i in range(0,len(pairs),8192):
     p=pairs[i:i+8192];dg=dgl.graph((p[:,0],p[:,1]),num_nodes=n).to('cuda');all.append(pred(dg,h).cpu().numpy())
    return np.concatenate(all)
   ps=score(pos);ns=score(neg.reshape(-1,2)).reshape(len(pos),neg.shape[1])
  torch.cuda.synchronize();seconds=time.perf_counter()-st
  if save is not None:np.savez_compressed(save,positive=ps,negative=ns)
  return ranking_metrics(ps,ns),seconds
 epochs=1 if smoke else 5000;start=time.perf_counter();trainsec=0.;best=-float('inf');bestepoch=None
 torch.cuda.reset_peak_memory_stats()
 for epoch in range(1,epochs+1):
  model.train();pred.train();torch.cuda.synchronize();st=time.perf_counter();h=model(g,x,H);ps=pred(pg,h);ns=pred(ng,h)
  # Execute author's exact CPU BCE expression, retaining autograd across device copy.
  loss=s['compute_loss'](ps.cpu(),ns.cpu());assert torch.isfinite(loss);optim.zero_grad();loss.backward();optim.step();torch.cuda.synchronize();trainsec+=time.perf_counter()-st
  if epoch%25==0 or epoch==epochs or epoch==1:
   metrics,_=evaluate(a['valid_pos'],a['valid_neg'])
   # Official release uses final epoch; validation logged diagnostically, no test selection.
   prog(job,state='SMOKE' if smoke else 'RUNNING',epoch=epoch,epochs=epochs,loss=float(loss),valid_mrr=metrics['mrr'],train_seconds=trainsec,elapsed_seconds=time.perf_counter()-start)
   print(ds,'NSLR-HMANN',seed,epoch,float(loss),metrics['mrr'],flush=True)
 if smoke:write(job/'smoke.json',{'state':'PASS','validation':metrics});return
 torch.save({'model':model.state_dict(),'predictor':pred.state_dict(),'epoch':5000},job/'final.pt')
 metrics,inference=evaluate(a['test_pos'],a['test_neg'],job/'test_scores.npz')
 write(dest,{'state':'COMPLETE','dataset':ds,'method':'NSLR-HMANN','seed':seed,'metrics':metrics,'parameters':sum(p.numel() for z in (model,pred) for p in z.parameters()),'train_seconds':trainsec,'total_seconds':time.perf_counter()-start,'inference_seconds':inference,'peak_gpu_allocated_mb':torch.cuda.max_memory_allocated()/1024**2,'official_source':read(OUT/'NSLR-HMANN_source.json'),'config':{'in':64,'hidden':32,'out':32,'heads':[8,2],'dropout':.5,'lr':.01,'epochs':5000,'feature':'fixed random embedding64, excluded optimizer','decoder':'official MLPPredictor','loss':'official compute_loss'},'selection':'fixed final epoch5000; test evaluated once','candidate_audit':read(OUT/'input_audit'/f'{ds}.json'),'negative_filter':'train-only offdiagonal complement uniform replacement fixed 1:1 directed sample; official selfloops on both label graphs','construction':read(cache/'metadata.json'),'device_adapter':'CUDA execution; no architecture/loss modification'})
 prog(job,state='COMPLETE',epoch=5000)
def finalize():
 audit=read(OUT/'FROZEN_AUDIT.json');frozen=ROOT/'R_HSPE_FROZEN'
 assert all(sha(frozen/p)==h for p,h in audit['frozen_files'].items())
 assert audit['source_hashes']==sources()
 tests=read(frozen/'TEST_RESULTS.json');third=read(ROOT/'HSPE_V17_2/THIRD_DATASET.json')
 rows={ds:{} for ds in DATASETS}
 for ds in ('cora','pubmed'):
  for seedrow in tests[ds]['seed_results']:
   for arm,r in seedrow['arms'].items():
    name='R-HSPE' if arm=='H2_R_HSPE' else arm
    training=f.parent_row(ds,seedrow['seed'],arm)
    row={**r,'seed':seedrow['seed'],'method':name,'inference_seconds':r['scoring_seconds'],'train_seconds':training.get('train_seconds'),'reused_frozen':True,'training_peak_gpu_mb':training.get('peak_gpu_allocated_mb')}
    rows[ds].setdefault(name,[]).append(row)
 # Third dataset's test objects reside in its own frozen summary, schema checked explicitly.
 for seedrow in third['test_seed_results']:
  for arm,r in seedrow['arms'].items():
   name='R-HSPE' if arm=='H2_R_HSPE' else arm
   training=third['validation_seed_results'][seedrow['seed']]['arms'][arm]
   rows['citeseer'].setdefault(name,[]).append({**r,'seed':seedrow['seed'],'method':name,'inference_seconds':r['scoring_seconds'],'train_seconds':training.get('train_seconds'),'reused_frozen':True,'training_peak_gpu_mb':training.get('peak_gpu_allocated_mb')})
 failures=[];expected=45
 for path in (OUT/'runs').glob('*/*/seed_*/result.json'):
  r=read(path);rows[r['dataset']].setdefault(r['method'],[]).append(r)
 for path in (OUT/'runs').glob('*/*/seed_*/error.json'):failures.append(read(path))
 summary={};ranks={};effects={}
 for ds in DATASETS:
  summary[ds]={}
  for method,rr in rows[ds].items():
   rr.sort(key=lambda r:r['seed']);summary[ds][method]={'seeds':[r['seed'] for r in rr],'n':len(rr),'metrics':{k:stat([r['metrics'][k] for r in rr]) for k in METRICS},'parameters':rr[0]['parameters'],'mean_train_seconds':float(np.mean([r['train_seconds'] for r in rr if r.get('train_seconds') is not None])) if any(r.get('train_seconds') is not None for r in rr) else None,'mean_inference_seconds':float(np.mean([r['inference_seconds'] for r in rr])),'max_peak_gpu_mb':max(max(r['peak_gpu_allocated_mb'],r.get('training_peak_gpu_mb') or 0) for r in rr),'reused':rr[0].get('reused_frozen',False)}
  order=sorted(summary[ds],key=lambda k:summary[ds][k]['metrics']['mrr']['mean'],reverse=True);ranks[ds]={k:i+1 for i,k in enumerate(order)}
  rivals=[k for k in order if k!='R-HSPE'];strong=rivals[0];aa={r['seed']:r['metrics']['mrr'] for r in rows[ds]['R-HSPE']};bb={r['seed']:r['metrics']['mrr'] for r in rows[ds][strong]};shared=sorted(set(aa)&set(bb));d=[aa[s]-bb[s] for s in shared]
  effects[ds]={'strongest':strong,'shared_seed_labels':shared,'deltas':d,'mean':float(np.mean(d)),'median':float(np.median(d)),'wins':sum(x>0 for x in d),'strict_paired_rng_test':False,'mean_gap_all_seeds':summary[ds]['R-HSPE']['metrics']['mrr']['mean']-summary[ds][strong]['metrics']['mrr']['mean']}
 completed=sum(len(rows[ds].get(k,[])) for ds in DATASETS for k in ('NCN','NCNC','NSLR-HMANN'));done=completed+len(failures)>=expected
 coverage='COMPLETE' if completed==expected else 'PARTIAL'
 # Descriptive decision thresholds fixed before starting third-party tests.
 top2=sum(ranks[ds]['R-HSPE']<=2 for ds in DATASETS);rangeok=sum(effects[ds]['mean_gap_all_seeds']>=-.02 for ds in DATASETS)
 strong=top2>=2 and all(effects[ds]['mean_gap_all_seeds']>=-.02 for ds in DATASETS)
 lowparam=all(summary[ds]['R-HSPE']['parameters']<min([summary[ds][k]['parameters'] for k in ('NCN','NCNC') if k in summary[ds]] or [float('inf')]) for ds in DATASETS)
 competitive=('STRONG' if strong else 'ACCEPTABLE' if rangeok>=2 and lowparam else 'WEAK') if done else 'PENDING'
 results={'state':'COMPLETE' if done else 'RUNNING','fair_baseline_benchmark':coverage,'completed_jobs':completed,'expected_jobs':expected,'failures':failures,'summary':summary,'seed_results':rows,'ranks':ranks,'effects':effects,'R_HSPE_FROZEN':True,'INNOVATION_1_METHOD_VALIDATED':'YES','TEST_GENERALIZATION':'YES','THIRD_DATASET':'YES','NO_EXACT_COLLISION_IN_FOCUSED_AUDIT':'YES','COMPETITIVENESS':competitive,'PAPER_READY_INNOVATION_1':'YES' if done and coverage=='COMPLETE' and competitive in ('STRONG','ACCEPTABLE') else 'NO','decision_caveat':'0.02 absolute MRR is a preregistered descriptive lag/range threshold, not a significance test; current tested baseline set only','NO_SOTA_CLAIM':True}
 write(OUT/'results.json',results)
 methods=sorted(set(k for ds in DATASETS for k in summary[ds]))
 lines=['# Fair benchmark main table','','Only frozen-protocol reruns and hash-compatible frozen results. Sample SD (ddof=1). **Best**, *second best*, by mean MRR within this table only. Citeseer frozen R-HSPE/B0 use 3 seeds; third-party methods target 5.','','| Method | Cora MRR | PubMed MRR | Citeseer MRR | Params | Fair protocol |','|---|---:|---:|---:|---|---|']
 csvrows=[]
 for method in methods:
  cells=[];pp=[]
  for ds in DATASETS:
   r=summary[ds].get(method)
   if r:
    mm=r['metrics']['mrr'];cell=metriccell(mm)+f" (n={r['n']})";rank=ranks[ds][method];cell='**'+cell+'**' if rank==1 else '*'+cell+'*' if rank==2 else cell;cells.append(cell);pp.append(f"{ds}:{r['parameters']}")
    csvrows.append({'dataset':ds,'method':method,'n':r['n'],'seeds':','.join(map(str,r['seeds'])),'rank':rank,'parameters':r['parameters'],**{k+'_mean':r['metrics'][k]['mean'] for k in METRICS},**{k+'_std':r['metrics'][k]['std'] for k in METRICS},'mean_train_seconds':r['mean_train_seconds'],'mean_inference_seconds':r['mean_inference_seconds'],'peak_gpu_mb':r['max_peak_gpu_mb'],'fair_protocol':'YES'})
   else:cells.append('PENDING / NOT RUN')
  lines.append('| '+method+' | '+' | '.join(cells)+' | '+'; '.join(pp)+' | YES (available cells) |')
 (OUT/'PAPER_MAIN_TABLE.md').write_text('\n'.join(lines)+'\n')
 if csvrows:
  with (OUT/'PAPER_MAIN_TABLE.csv').open('w',newline='') as fh:w=csv.DictWriter(fh,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
 for ds,prefix in zip(DATASETS,('03','04','05')):
  ls=[f'# {ds.title()} results','','| Method | MRR | Hits@10 | Hits@20 | Mean positive rank | Seeds | Train sec | Inference sec | Peak GPU MB |','|---|---:|---:|---:|---:|---|---:|---:|---:|']
  for method in sorted(summary[ds],key=lambda k:ranks[ds][k]):
   r=summary[ds][method];cells=[metriccell(r['metrics'][k]) for k in METRICS]
   ls.append('| '+method+' | '+' | '.join(cells)+f" | {r['seeds']} | {r['mean_train_seconds']} | {r['mean_inference_seconds']:.3f} | {r['max_peak_gpu_mb']:.1f} |")
  ls+=['','R-HSPE versus highest other mean MRR (matching seed labels are descriptive, not strict paired RNG tests):','',json.dumps(effects[ds],indent=2)]
  if ds=='pubmed':ls+=['','R-HSPE MRR improves over B0, but Hits@10 and Hits@20 are slightly lower; all metrics above are retained.']
  (OUT/f'{prefix}_{ds.upper()}_RESULTS.md').write_text('\n'.join(ls)+'\n')
 report=['# V17.3 benchmark report','',f"STATUS: {results['state']}",f'R_HSPE_FROZEN: TRUE',f'FAIR_BASELINE_BENCHMARK: {coverage}',f'COMPLETED_JOBS: {completed}/{expected}',f'COMPETITIVENESS: {competitive}',f"PAPER_READY_INNOVATION_1: {results['PAPER_READY_INNOVATION_1']}",'INNOVATION_1_METHOD_VALIDATED: YES','TEST_GENERALIZATION: YES','THIRD_DATASET: YES','NO_EXACT_COLLISION_IN_FOCUSED_AUDIT: YES (limited audit, no priority proof)','','## Dataset rankings','']
 for ds in DATASETS:report+=[f"{ds.upper()}_R_HSPE: {summary[ds]['R-HSPE']['metrics']['mrr']}",f"BEST_ON_{ds.upper()}: {min(ranks[ds],key=ranks[ds].get)}",f"R_HSPE_RANK_{ds.upper()}: {ranks[ds]['R-HSPE']}"]
 report+=['','## Coverage','']
 for method in ('NSLR-HMANN','NCN','NCNC'):report.append(f"{method}: "+'; '.join(f"{ds} {len(rows[ds].get(method,[]))}/5 seeds" for ds in DATASETS))
 report+=['HMNE: REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION','HMRLH: REFERENCE_ONLY / NO_VERIFIED_IMPLEMENTATION','CCLPH: REFERENCE_ONLY / NO_VERIFIED_COMPLETE_IMPLEMENTATION; pairwise scoring is supported in paper, not categorically TASK_MISMATCH','DIRECTLY_COMPARABLE_METHODS: '+', '.join(methods),'REFERENCE_ONLY_METHODS: HMNE, HMRLH, CCLPH, Tier C','PARAMETER_EFFICIENCY: R-HSPE adds 75 parameters; absolute totals and measured baseline costs in CSV; frozen training timing unavailable is NA, not zero.','NOVELTY_STATUS: context-driven candidate-specific hyperedge-pair residual; no size-causality or first-ever claim.','NEXT_EXPECTED_STEP: retrieve completed benchmark and decide paper positioning; keep Innovation1 frozen; do not start Innovation2.','','## Failures',json.dumps(failures,indent=2),'','## Effect sizes',json.dumps(effects,indent=2),'','## Decision limits','Competition thresholds fixed before third-party test access: third-dataset lag/strong-range threshold 0.02 absolute MRR, descriptive only. Different model RNGs do not justify a paired significance test. Rankings cover only rerun methods. Frozen Citeseer has 3 seeds. Missing reference-only original numeric scores remain NOT_VERIFIED, never fabricated.']
 (OUT/'FINAL_REPORT.md').write_text('\n'.join(report)+'\n')
 (OUT/'C2C_HANDOFF.md').write_text('STATUS: '+('EXECUTED' if done else 'RUNNING')+'\nDIRECTION: R_HSPE_PUBLICATION_BENCHMARK\nR_HSPE: FROZEN\n'+json.dumps({k:results[k] for k in ('ranks','effects','COMPETITIVENESS','PAPER_READY_INNOVATION_1')},indent=2)+'\nNEXT_EXPECTED_STEP: retrieve results; no Innovation2 launch\n')
 error=OUT/'aggregation_error.json'
 if error.exists():error.unlink()
 return results
def supervisor():
 # Preparation is separated from GPU jobs and bounded to one dense inverse at a time.
 previous=read(OUT/'status.json') if (OUT/'status.json').exists() else {}
 gpuqueue=[('ncn',ds,method,str(seed)) for ds in DATASETS for seed in range(5) for method in ('NCN','NCNC')]
 prepqueue=[('prepare-nslr',ds) for ds in ('cora','citeseer','pubmed')]
 nslrqueue=[];gpu=[];prep=None;finished=previous.get('finished',[]);failed=previous.get('failed',[])
 class Adopted:
  def __init__(self,pid,args):self.pid=pid;self.args=args;self.returncode=None
  def poll(self):
   try:
    state=Path(f'/proc/{self.pid}/stat').read_text().split(')')[1].split()[0]
    if state not in ('Z','X'):return None
   except FileNotFoundError:pass
   if self.args[0]=='prepare-nslr':ok=(OUT/'nslr_cache'/self.args[1]/'metadata.json').exists()
   else:
    ds=self.args[1];method=self.args[2] if self.args[0]=='ncn' else 'NSLR-HMANN';seed=int(self.args[-1]);ok=(jobpath(ds,method,seed)/'result.json').exists()
   self.returncode=0 if ok else 1;return self.returncode
 for entry in previous.get('gpu_jobs',[]):
  args=tuple(entry['args']);gpu.append({'proc':Adopted(entry['pid'],args),'args':args,'key':'_'.join(args)})
 entry=previous.get('preparation')
 if entry:
  args=tuple(entry['args']);prep={'proc':Adopted(entry['pid'],args),'args':args,'key':'_'.join(args)}
 active={tuple(x['args']) for x in gpu}
 gpuqueue=[a for a in gpuqueue if a not in active and not any((jobpath(a[1],a[2],int(a[3]))/file).exists() for file in ('result.json','error.json'))]
 prepqueue=[a for a in prepqueue if (prep is None or a!=tuple(prep['args'])) and not (OUT/'nslr_cache'/a[1]/'metadata.json').exists()]
 for ds in DATASETS:
  if (OUT/'nslr_cache'/ds/'metadata.json').exists():
   for seed in range(5):
    args=('nslr',ds,str(seed))
    if args not in active and not any((jobpath(ds,'NSLR-HMANN',seed)/file).exists() for file in ('result.json','error.json')):nslrqueue.append(args)
 logs=OUT/'logs';logs.mkdir(exist_ok=True)
 def launch(args,threads):
  key='_'.join(args);log=(logs/(key+'.log')).open('a');env=os.environ.copy()
  for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):env[k]=str(threads)
  proc=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*args],stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,env=env);log.close();return {'proc':proc,'args':args,'key':key}
 while gpuqueue or prepqueue or nslrqueue or gpu or prep:
  if prep is not None and prep['proc'].poll() is not None:
   code=prep['proc'].returncode;ds=prep['args'][1]
   if code==0:nslrqueue.extend([('nslr',ds,str(s)) for s in range(5)])
   else:
    for s in range(5):write(jobpath(ds,'NSLR-HMANN',s)/'error.json',{'dataset':ds,'method':'NSLR-HMANN','seed':s,'error':'official construction failed; see '+prep['key']+'.log'})
   finished.append({'args':prep['args'],'code':code});prep=None
  for item in list(gpu):
   code=item['proc'].poll()
   if code is not None:
    gpu.remove(item);finished.append({'args':item['args'],'code':code})
    if code:failed.append(item['args'])
  if prep is None and prepqueue:prep=launch(prepqueue.pop(0),16)
  # Cora/Citeseer two concurrent GPU jobs. PubMed dense NSLR runs alone.
  busy_dense=any(t['args'][0]=='nslr' and t['args'][1]=='pubmed' for t in gpu)
  while len(gpu)<2 and not busy_dense:
   q=nslrqueue if nslrqueue else gpuqueue
   if not q:break
   args=q[0]
   if args[0]=='nslr' and args[1]=='pubmed' and gpu:break
   q.pop(0);gpu.append(launch(args,4))
   if args[0]=='nslr' and args[1]=='pubmed':busy_dense=True
  write(OUT/'status.json',{'state':'RUNNING','pid':os.getpid(),'updated':time.time(),'gpu_jobs':[{'pid':x['proc'].pid,'args':x['args']} for x in gpu],'preparation':None if prep is None else {'pid':prep['proc'].pid,'args':prep['args']},'queued_gpu':len(gpuqueue)+len(nslrqueue),'queued_preparations':len(prepqueue),'finished':finished,'failed':failed})
  try:finalize()
  except Exception as e:write(OUT/'aggregation_error.json',{'error':repr(e),'traceback':traceback.format_exc()})
  time.sleep(10)
 final=finalize();write(OUT/'status.json',{'state':final['state'],'benchmark':final['fair_baseline_benchmark'],'finished':finished,'failed':failed,'ended':time.time()})
if __name__=='__main__':
 command=sys.argv[1]
 try:
  if command=='preflight':print(preflight(),flush=True)
  elif command=='prepare-nslr':nslr_prepare(sys.argv[2])
  elif command=='ncn':ncn(sys.argv[2],sys.argv[3],int(sys.argv[4]))
  elif command=='nslr':nslr(sys.argv[2],int(sys.argv[3]))
  elif command=='smoke-ncn':ncn(sys.argv[2],sys.argv[3],int(sys.argv[4]),True)
  elif command=='smoke-nslr':nslr(sys.argv[2],int(sys.argv[3]),True)
  elif command=='finalize':print(finalize()['state'])
  elif command=='supervise':supervisor()
  else:raise ValueError(command)
 except Exception as e:
  if command in ('ncn','nslr'):
   ds=sys.argv[2];method=sys.argv[3] if command=='ncn' else 'NSLR-HMANN';seed=int(sys.argv[4] if command=='ncn' else sys.argv[3]);write(jobpath(ds,method,seed)/'error.json',{'dataset':ds,'method':method,'seed':seed,'error':repr(e),'traceback':traceback.format_exc()})
  raise
