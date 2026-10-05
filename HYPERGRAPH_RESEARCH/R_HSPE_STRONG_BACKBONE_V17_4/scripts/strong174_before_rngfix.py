from __future__ import annotations
import os
os.environ.setdefault('OMP_NUM_THREADS','4');os.environ.setdefault('MKL_NUM_THREADS','4');os.environ.setdefault('OPENBLAS_NUM_THREADS','4')
import ast, copy, gc, hashlib, json, random, subprocess, sys, time, traceback
from pathlib import Path
from types import SimpleNamespace
OUT=Path(__file__).resolve().parents[1];ROOT=OUT.parent;PARENT=ROOT/'R_HSPE_BENCHMARK_V17_3';FROZEN=ROOT/'R_HSPE_FROZEN'
def read(p):return json.loads(Path(p).read_text())
def write(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);q=p.with_suffix(p.suffix+'.tmp');q.write_text(json.dumps(x,indent=2,allow_nan=False));os.replace(q,p)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(name,p):
 import importlib.util
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
b=load('backbone173',PARENT/'scripts/benchmark173.py');f=b.f;np=b.np;torch=b.torch;nn=torch.nn
ARMS=('N0','N1','C0','C1','C2');NAMES={'N0':'NCN','N1':'NCN + R-HSPE','C0':'NCNC','C1':'NCNC + R-HSPE','C2':'NCNC + NULL75'}
def ah(a):return f.m.p.v16.v61.array_hash(np.asarray(a))
def statehash(*mods):
 h=hashlib.sha256()
 for mod in mods:
  for k,v in mod.state_dict().items():h.update(k.encode());h.update(v.detach().cpu().contiguous().numpy().tobytes())
 return h.hexdigest()
def assert_frozen():
 manifest=read(FROZEN/'SOURCE_HASHES.json');assert b.sources()==manifest['sources']
 for p,h in manifest['runtime_python_source_hashes'].items():assert sha(p)==h,('FROZEN_RUNTIME_MISMATCH',p)
 a=read(OUT/'AUDIT.json') if (OUT/'AUDIT.json').exists() else None
 if a:
  assert sha(PARENT/'scripts/benchmark173.py')==a['backbone_adapter_sha256']
  for p,h in a['frozen_files'].items():assert sha(FROZEN/p)==h,('FROZEN_FILE_MISMATCH',p)
  for p,h in a['official_files'].items():assert sha(PARENT/p)==h,('OFFICIAL_FILE_MISMATCH',p)
 return manifest
def input_data(ds,test=False):
 with np.load(PARENT/'input_cache'/f'{ds}.npz') as z:
  names=('x','train','valid_pos','valid_neg')+(('test_pos','test_neg') if test else ())
  return {k:z[k].copy() for k in names}
def preflight():
 manifest=assert_frozen();assert read(PARENT/'results.json')['state']=='COMPLETE';assert read(PARENT/'results.json')['COMPETITIVENESS']=='WEAK'
 official={str(p.relative_to(PARENT)):sha(p) for p in (PARENT/'vendor').glob('NeuralCommonNeighbor-*/*') if p.is_file()}
 prior={p.replace('\\','/'):h for p,h in read(PARENT/'SOURCE_MANIFEST.json').items()}
 for p,h in official.items():assert prior[p]==h
 audits={}
 for ds in ('cora','pubmed'):
  a=input_data(ds);meta=read(PARENT/'input_audit'/f'{ds}.json')
  for key,field in (('train','train_hash'),('valid_pos','valid_positive_hash'),('valid_neg','valid_negative_hash')):assert ah(a[key])==meta[field]
  audits[ds]={'train_hash':ah(a['train']),'validation_positive_hash':ah(a['valid_pos']),'validation_negative_hash':ah(a['valid_neg']),'test_accessed':False,'seeds_phase_a':[0,1,2],'epochs_phase_a':5,'baseline_reuse':'NOT_ALLOWED_100_VS_5_OR_10_EPOCHS'}
 write(OUT/'SOURCE_HASHES.json',manifest)
 write(OUT/'AUDIT.json',{'state':'PASS','frozen_files':{str(p.relative_to(FROZEN)):sha(p) for p in FROZEN.rglob('*') if p.is_file()},'source_hashes':manifest['sources'],'frozen_config_sha256':sha(FROZEN/'FINAL_CONFIG.json'),'backbone_adapter_sha256':sha(PARENT/'scripts/benchmark173.py'),'official_files':official,'datasets':audits,'adapter':'V17.3 official_ncn/NCFG/train AST unchanged, data/evaluation identical; V17.4 overrides epoch budget to5/10 and uses final-epoch checkpoint','added_parameters':75,'test_accessed':False})
 print('PREFLIGHT_PASS',audits,flush=True)
def phasepath(phase,ds):return OUT/'phases'/phase/ds
def jobpath(phase,ds,seed,arm):return phasepath(phase,ds)/f'seed_{seed}'/arm
def prepare(phase,ds,epochs,seeds,workers=24):
 assert_frozen();dest=phasepath(phase,ds);dest.mkdir(parents=True,exist_ok=True);done=dest/'FEATURE_READY.json'
 if done.exists():return
 a=input_data(ds);_,view=f.m.p.v16.base.init_dataset(ds);meta=read(FROZEN/'SOURCE_HASHES.json')['dataset_split_hashes'][ds];assert f.m.p.v16.base.split_hash(view)==meta['training_view_split_hash']
 from torch_geometric.utils import negative_sampling
 # Installed official sampler uses Python random.sample and consumes no torch RNG.
 from torch_geometric.utils._negative_sampling import sample
 src=__import__('inspect').getsource(sample);assert 'random.sample' in src and 'randperm' not in src
 tr=torch.as_tensor(a['train'].T,dtype=torch.long);ei=torch.cat((tr,tr.flip(0)),dim=1)
 allpairs=[a['train']];schedules={};started=time.perf_counter();old=random.getstate()
 try:
  for seed in seeds:
   random.seed(seed);neg=[negative_sampling(ei,len(a['x'])).T.numpy() for _ in range(epochs)]
   schedule=np.stack(neg);assert len(neg[0])>=len(a['train']);schedules[str(seed)]={'epoch_negative_hashes':[ah(x) for x in neg]}
   np.save(dest/f'negatives_seed{seed}.npy',schedule);allpairs.extend(neg)
 finally:random.setstate(old)
 write(dest/'sampling.json',{'state':'COMPLETE','seeds':seeds,'epochs':epochs,'sampler_source_sha256':hashlib.sha256(src.encode()).hexdigest(),'negative_schedules':schedules,'semantics':'precomputed same official calls; runtime resampling must equal schedule exactly; no sampler changes','heldout_label_filter':False})
 unique=np.unique(f.m.p.v16.stage0.canonical_pairs(np.vstack(allpairs)),axis=0)
 write(dest/'feature_progress.json',{'state':'BUILD_TRAIN','unique_pairs':len(unique),'workers':workers,'test_accessed':False})
 # Call the frozen V17.2 constructor, including exact target mask and ECDF.
 oldout=f.OUT;f.OUT=dest;write(dest/'SOURCE_HASHES.json',read(FROZEN/'SOURCE_HASHES.json'))
 try:
  train,tm=f.make_features(ds,'train',view,unique,a['train'],workers)
  valid,vm=f.make_features(ds,'valid',view,np.vstack((a['valid_pos'],a['valid_neg'].reshape(-1,2))),np.empty((0,2),np.int64),workers)
 finally:f.OUT=oldout
 # Validate new candidate cache against previously frozen validation descriptors.
 if ds in ('cora','pubmed'):
  vmeta=read(ROOT/'HSPE_V17_1/features'/ds/'metadata.json')
  with np.load(ROOT/'NHMC_V16/experiments'/f'stage1_{ds}/cache/valid'/f'{ds}_pair_features.npz') as z:
   assert np.array_equal(valid['keys'],z['keys']) and np.array_equal(valid['offsets'],z['offsets']) and np.array_equal(valid['support'],z['support'])
  oldrank=np.load(vmeta['splits']['valid']['rank_path']);assert np.array_equal(oldrank,valid['tokens_rank'])
 del train,valid;gc.collect()
 write(done,{'state':'COMPLETE','dataset':ds,'phase':phase,'seeds':seeds,'epochs':epochs,'feature_cache_seconds':time.perf_counter()-started,'train':tm,'valid':vm,'validation_frozen_descriptor_parity':'BITWISE_EQUAL' if ds in ('cora','pubmed') else 'FROZEN_CONSTRUCTOR','test_accessed':False})
 print('FEATURE_READY',phase,ds,time.perf_counter()-started,flush=True)
class Residual(nn.Module):
 def __init__(self,view,ds,null=False):
  super().__init__();self.null=null;self.store=None
  # Reuse actual frozen constructor and its original Linear modules; retain RNG.
  with torch.random.fork_rng(devices=[torch.cuda.current_device()]):
   dummy=SimpleNamespace();ref=f.m.make_model(f.m.model_class('H2_R_HSPE',dummy,dummy),view,ds)
   self.encoder=ref.nhmc_encoder;self.head=ref.nhmc_residual
  del ref
  assert sum(p.numel() for p in self.parameters())==75
  assert (self.encoder.in_features,self.encoder.out_features,self.head.in_features,self.head.out_features)==(6,8,18,1)
  assert not torch.count_nonzero(self.head.weight) and not torch.count_nonzero(self.head.bias)
 def forward(self,pairs):
  if self.null:
   h=torch.relu(self.encoder(torch.ones((len(pairs),6),device=pairs.device)))
   summary=torch.cat((h,h,torch.ones((len(pairs),2),device=pairs.device)),dim=1)
  else:
   st=self.store;rows=st.lookup(pairs)
   mean,maximum=f.m.p.v16._pool_nhmc(st.real,st.offsets,rows,self.encoder)
   count=(st.offsets[rows+1]-st.offsets[rows]).to(mean.dtype)
   summary=torch.cat((mean,maximum,torch.log1p(count).unsqueeze(1),torch.log1p(st.support[rows]).unsqueeze(1)),dim=1)
  return self.head(summary).squeeze(-1)
class PredictorWithResidual(nn.Module):
 def __init__(self,base,residual):super().__init__();self.base=base;self.residual=residual
 def setalpha(self,alpha):return self.base.setalpha(alpha)
 def forward(self,x,adj,edge,*args,**kw):
  s=self.base(x,adj,edge,*args,**kw);d=self.residual(edge.T)
  return s+d.reshape((-1,)+(1,)*(s.ndim-1))
 def multidomainforward(self,x,adj,edge,*args,**kw):
  # Completion recursion stays entirely in base, so plug-in is applied once.
  s=self.base.multidomainforward(x,adj,edge,*args,**kw);d=self.residual(edge.T)
  return s+d.reshape((-1,)+(1,)*(s.ndim-1))
def feature_store(phase,ds,split):
 path=phasepath(phase,ds)/'features'/ds/split/'cache.npz'
 with np.load(path) as z:cache={k:z[k].copy() for k in z.files}
 st=f.new_store(cache,SimpleNamespace(num_nodes=read(phasepath(phase,ds)/'features'/ds/split/'metadata.json')['identity'].get('n',len(input_data(ds)['x']))),'H2_R_HSPE')
 return st
def make_models(ds,seed,arm):
 from torch_sparse import SparseTensor
 m,scope=b.official_ncn();scope['set_seed'](seed);random.seed(seed)
 a=input_data(ds);x=torch.as_tensor(a['x'],dtype=torch.float32,device='cuda');n=len(x);train=torch.as_tensor(a['train'],dtype=torch.long,device='cuda');ei=torch.cat((train.T,train.T.flip(0)),dim=1)
 adj=SparseTensor.from_edge_index(ei,sparse_sizes=(n,n)).to_symmetric().coalesce();data=SimpleNamespace(x=x,edge_index=ei,adj_t=adj,num_nodes=n);c=b.NCFG[ds]
 model=m.GCN(x.shape[1],256,256,1,c['gnndp'],True,False,-1,'puregcn',True,0.,xdropout=c['xdp'],taildropout=c['tdp'],noinputlin=False).to('cuda')
 kwargs=dict(cndeg=-1,use_xlin=True,tailact=True,twolayerlin=c['twolayerlin'],beta=1.)
 is_nc=arm.startswith('C')
 if is_nc:kwargs.update(depth=1,splitsize=131072,scale=c['scale'],offset=c['offset'],trainresdeg=-1,testresdeg=-1,pt=c['pt'],learnablept=False,alpha=c['alpha'])
 pred=m.predictor_dict['incn1cn1' if is_nc else 'cn1'](256,256,1,3,c['predp'],c['preedp'],True,**kwargs).to('cuda');initial=statehash(model,pred)
 residual=None
 if arm not in ('N0','C0'):
  _,view=f.m.p.v16.base.init_dataset(ds);residual=Residual(view,ds,arm=='C2').to('cuda');pred=PredictorWithResidual(pred,residual)
 optimizer=torch.optim.Adam([{'params':model.parameters(),'lr':c['gnnlr']},{'params':pred.parameters(),'lr':c['prelr']}])
 return model,pred,residual,optimizer,data,train,scope,a,initial
@torch.no_grad()
def evaluate(model,pred,residual,data,pos,neg,store,method,save=None):
 model.eval();pred.eval()
 if residual is not None:residual.store=store
 torch.cuda.synchronize();start=time.perf_counter();h=model(data.x,data.adj_t);batch=512 if method.startswith('C') else 8192
 def score(pairs):
  parts=[]
  for i in range(0,len(pairs),batch):
   edge=torch.as_tensor(pairs[i:i+batch],dtype=torch.long,device='cuda').T
   parts.append(pred(h,data.adj_t,edge).flatten().cpu().numpy())
  return np.concatenate(parts)
 ps=score(pos);ns=score(neg.reshape(-1,2)).reshape(len(pos),neg.shape[1]);torch.cuda.synchronize()
 if save is not None:np.savez_compressed(save,positive=ps,negative=ns)
 return b.ranking_metrics(ps,ns),time.perf_counter()-start
def run(phase,ds,seed,arm,epochs):
 assert_frozen();job=jobpath(phase,ds,seed,arm);job.mkdir(parents=True,exist_ok=True)
 if (job/'result.json').exists():return
 model,pred,res,optimizer,data,train,scope,a,initial=make_models(ds,seed,arm)
 ts=vs=None
 if res is not None and arm!='C2':ts=feature_store(phase,ds,'train');vs=feature_store(phase,ds,'valid');res.store=vs
 base_params=sum(p.numel() for obj in (model,pred.base if res else pred) for p in obj.parameters());params=sum(p.numel() for obj in (model,pred) for p in obj.parameters());assert params-base_params==(75 if res else 0)
 zero={'base_initial_state_sha256':initial,'added_parameters':params-base_params}
 if res is not None:
  model.eval();pred.eval()
  with torch.no_grad():
   edge=torch.as_tensor(a['valid_pos'][:32],device='cuda',dtype=torch.long).T;h=model(data.x,data.adj_t);plain=pred.base(h,data.adj_t,edge);delta=res(edge.T);combined=plain+delta.reshape_as(plain)
   error=float((combined-plain).abs().max());assert error<=5e-7 and float(delta.abs().max())==0
  zero.update(initial_logit_max_abs_error=error,zero_head=True)
 write(job/'zero_init.json',zero)
 schedule=np.load(phasepath(phase,ds)/f'negatives_seed{seed}.npy',mmap_mode='r');neg_sampler=scope['negative_sampling'];iterator=scope['PermIterator'];trace=[];epochctx={}
 def checked_neg(*args,**kw):
  neg=neg_sampler(*args,**kw);array=neg.T.cpu().numpy();expected=schedule[epochctx['epoch']-1];assert np.array_equal(array,expected),'STOP_NEGATIVE_SAMPLE_MISMATCH'
  epochctx['negative_hash']=ah(array);return neg
 def checked_iter(*args,**kw):
  it=iterator(*args,**kw);epochctx['permutation_hash']=ah(it.idx.cpu().numpy());return it
 scope['negative_sampling']=checked_neg;scope['PermIterator']=checked_iter
 train_seconds=0.;valid_seconds=0.;start=time.perf_counter();torch.cuda.reset_peak_memory_stats();history=[]
 for epoch in range(1,epochs+1):
  epochctx['epoch']=epoch
  if res is not None:res.store=ts
  torch.cuda.synchronize();t=time.perf_counter();loss=scope['train'](model,pred,data,{'train':{'edge':train}},optimizer,b.NCFG[ds]['batch'],True,[],None);torch.cuda.synchronize();train_seconds+=time.perf_counter()-t;assert np.isfinite(loss)
  metric,seconds=evaluate(model,pred,res,data,a['valid_pos'],a['valid_neg'],vs,arm,job/f'valid_epoch{epoch}_scores.npz');valid_seconds+=seconds
  trace.append({'epoch':epoch,**{k:epochctx[k] for k in ('negative_hash','permutation_hash')},'torch_cuda_rng_sha256':hashlib.sha256(torch.cuda.get_rng_state().cpu().numpy().tobytes()).hexdigest()});history.append({'epoch':epoch,'loss':float(loss),'validation':metric})
  write(job/'progress.json',{'state':'RUNNING','phase':phase,'dataset':ds,'seed':seed,'arm':arm,'epoch':epoch,'epochs':epochs,'validation':metric,'train_seconds':train_seconds,'updated_at':time.time(),'test_accessed':False})
  print(phase,ds,seed,arm,epoch,loss,metric['mrr'],flush=True)
 torch.save({'model':model.state_dict(),'predictor':pred.state_dict(),'epoch':epochs,'arm':arm,'dataset':ds,'seed':seed},job/'final.pt')
 result={'state':'COMPLETE','phase':phase,'dataset':ds,'seed':seed,'arm':arm,'method':NAMES[arm],'epochs':epochs,'validation':metric,'history':history,'checkpoint':str(job/'final.pt'),'checkpoint_sha256':sha(job/'final.pt'),'base_initial_state_sha256':initial,'rng_and_sample_trace':trace,'train_seconds':train_seconds,'validation_seconds':valid_seconds,'wall_seconds':time.perf_counter()-start,'parameters':params,'base_parameters':base_params,'added_parameters':params-base_params,'percentage_overhead':100*(params-base_params)/base_params,'peak_gpu_mb':torch.cuda.max_memory_allocated()/1024**2,'selection':'fixed final epoch, as V17.4 final integration requirement','test_accessed':False,'sources':{'frozen':read(OUT/'AUDIT.json')['source_hashes'],'backbone_adapter':read(OUT/'AUDIT.json')['backbone_adapter_sha256'],'integration_adapter':sha(Path(__file__))},'config':{**b.NCFG[ds],'epochs':epochs,'backbone_hidden':256,'residual_encoder':6 if res else None,'residual_hidden':8 if res else None,'residual_head':18 if res else None,'optimizer':'same two-group Adam; residual in predictor LR group','negative_sampler':'unchanged official sampler, checked against deterministic cache'}}
 write(job/'result.json',result);write(job/'progress.json',{'state':'COMPLETE','epoch':epochs,'test_accessed':False})
def stat(v):return {**f.stat(v),'wins':sum(x>0 for x in v)}
def summarize(phase,datasets,seeds,arms):
 rows={};effects={};checks={}
 for ds in datasets:
  rows[ds]=[]
  for seed in seeds:
   rr={a:read(jobpath(phase,ds,seed,a)/'result.json') for a in arms};assert all(r['test_accessed'] is False for r in rr.values())
   for baseline,augments in (('N0',('N1',)),('C0',('C1','C2'))):
    if baseline not in rr:continue
    for aug in augments:
     if aug not in rr:continue
     assert rr[baseline]['base_initial_state_sha256']==rr[aug]['base_initial_state_sha256'],'STOP_INIT_MISMATCH'
     assert rr[baseline]['rng_and_sample_trace']==rr[aug]['rng_and_sample_trace'],'STOP_SAMPLING_PERMUTATION_OR_RNG_MISMATCH'
   rows[ds].append({'seed':seed,'arms':rr})
  effect={}
  for name,a,c in (('delta_ncn','N1','N0'),('delta_ncnc','C1','C0'),('delta_null','C1','C2')):
   if a in arms and c in arms:effect[name]=stat([r['arms'][a]['validation']['mrr']-r['arms'][c]['validation']['mrr'] for r in rows[ds]])
  effects[ds]=effect
  primary=effect['delta_ncnc'];null=effect['delta_null'];n=len(seeds)
  checks[ds]={'nc_nc_pass':primary['wins']>=(2 if n==3 else 4) and primary['mean']>0 and (primary['median']>0 if phase!='third' else True),'null_pass':null['wins']>=(2 if n==3 else 3) and null['mean']>0,'initialization_negative_and_rng_match':True}
  checks[ds]['pass']=checks[ds]['nc_nc_pass'] and checks[ds]['null_pass'] if phase!='third' else checks[ds]['nc_nc_pass']
 return {'state':'COMPLETE','phase':phase,'datasets':list(datasets),'seeds':seeds,'seed_results':rows,'effects':effects,'gates':checks,'all_pass':all(v['pass'] for v in checks.values()),'test_accessed':False,'backbone_independent':all(effects[ds].get('delta_ncn',{'mean':0})['mean']>0 for ds in datasets)}
def test_feature(ds):
 # Read test arrays only after both formal validation gates passed.
 formal=read(OUT/'PHASE_B.json');assert formal['all_pass']
 a=input_data(ds,True);_,view=f.m.p.v16.base.init_dataset(ds);dest=phasepath('B' if ds!='citeseer' else 'third',ds)
 old=f.OUT;f.OUT=dest
 try:f.make_features(ds,'test',view,np.vstack((a['test_pos'],a['test_neg'].reshape(-1,2))),np.empty((0,2),np.int64),24)
 finally:f.OUT=old
def test_run(ds,seed,arm):
 assert read(OUT/'PHASE_B.json')['all_pass'];assert_frozen();phase='third' if ds=='citeseer' else 'B';job=jobpath(phase,ds,seed,arm);dest=job/'test_result.json'
 if dest.exists():return
 ref=read(job/'result.json');model,pred,res,optimizer,data,train,scope,a,initial=make_models(ds,seed,arm)
 ck=torch.load(job/'final.pt',map_location='cuda',weights_only=False);assert sha(job/'final.pt')==ref['checkpoint_sha256'];model.load_state_dict(ck['model']);pred.load_state_dict(ck['predictor'])
 st=feature_store(phase,ds,'test') if res is not None and arm!='C2' else None;a=input_data(ds,True);torch.cuda.reset_peak_memory_stats()
 metrics,seconds=evaluate(model,pred,res,data,a['test_pos'],a['test_neg'],st,arm,job/'test_scores.npz')
 write(dest,{'state':'COMPLETE','dataset':ds,'seed':seed,'arm':arm,'epochs':10,'metrics':metrics,'checkpoint_sha256':ref['checkpoint_sha256'],'inference_seconds':seconds,'peak_gpu_mb':torch.cuda.max_memory_allocated()/1024**2,'test_candidate_metadata':read(PARENT/'input_audit'/f'{ds}.json'),'configuration_frozen_before_test':True})
def test_summary(datasets,ncn):
 result={};passes={}
 for ds in datasets:
  phase='third' if ds=='citeseer' else 'B';seeds=list(range(3 if ds=='citeseer' else 5));arms=('C0','C1','C2')+(('N0','N1') if ncn and ds!='citeseer' else ())
  rr=[{'seed':s,'arms':{a:read(jobpath(phase,ds,s,a)/'test_result.json') for a in arms}} for s in seeds]
  effects={}
  for name,a,c in (('delta_ncnc','C1','C0'),('delta_null','C1','C2'),('delta_ncn','N1','N0')):
   if a in arms and c in arms:effects[name]=stat([r['arms'][a]['metrics']['mrr']-r['arms'][c]['metrics']['mrr'] for r in rr])
  d=effects['delta_ncnc'];passes[ds]=d['wins']>=(4 if ds=='cora' else 3 if ds=='pubmed' else 2) and d['mean']>0 and (d['median']>0 if ds!='citeseer' else True)
  result[ds]={'seeds':seeds,'seed_results':rr,'effects':effects,'metrics':{a:{k:f.stat([r['arms'][a]['metrics'][k] for r in rr]) for k in b.METRICS} for a in arms},'pass':passes[ds]}
 return {'state':'COMPLETE','datasets':result,'passes':passes,'cora_pubmed_pass':passes['cora'] and passes['pubmed']}
def reports(state,decision,extra=None):
 extra=extra or {};payload={'state':state,'decision':decision,'R_HSPE_FROZEN':True,'MECHANISM':'CONTEXT_DRIVEN','SIZE_CAUSAL_CLAIM':'NOT_SUPPORTED','INNOVATION_1':'PAPER_READY' if decision=='INNOVATION_1_PAPER_READY' else 'NOT_PAPER_READY',**extra}
 for phase,filename,mdname in (('A','PHASE_A.json','02_PHASE_A.md'),('B','PHASE_B.json','03_PHASE_B.md'),('third','THIRD.json','04_CITESEER.md')):
  if not (OUT/filename).exists():
   (OUT/mdname).write_text(f'# {phase}\n\nPENDING / NOT_REACHED\n');continue
  s=read(OUT/filename);payload[phase]=s
  lines=[f'# Phase {phase} validation','','| Dataset | Arm | MRR mean ± sample SD | Hits@10 | Hits@20 | Mean rank |','|---|---|---:|---:|---:|---:|']
  for ds,rr in s['seed_results'].items():
   for arm in rr[0]['arms']:
    cells=[]
    for k in b.METRICS:
     v=f.stat([r['arms'][arm]['validation'][k] for r in rr]);cells.append(f"{v['mean']:.6f} ± {v['std']:.6f}")
    lines.append('| '+ds+' | '+NAMES[arm]+' | '+' | '.join(cells)+' |')
  lines+=['','## Paired deltas and gates','',json.dumps({'effects':s['effects'],'gates':s['gates']},indent=2)];(OUT/mdname).write_text('\n'.join(lines)+'\n')
 if (OUT/'TEST.json').exists():payload['test']=read(OUT/'TEST.json')
 write(OUT/'results.json',payload)
 (OUT/'05_TEST.md').write_text('# One-shot test\n\n'+(json.dumps(payload['test'],indent=2) if 'test' in payload else 'TEST OFF / NOT_REACHED')+'\n')
 if 'test' in payload:
  lines=['# Matched10-epoch transfer test main table','','V17.3 rows use100 epochs; those results remain separately labeled reference anchors. Direct plug-in contrasts below are matched10-epoch final checkpoints, same seeds/splits/candidates. No ranking mixes5/10/100-epoch results.','','| Dataset | Arm | MRR mean±SD | Hits@10 mean±SD | Hits@20 mean±SD | Mean rank mean±SD | Rank (matched arms) |','|---|---|---:|---:|---:|---:|---:|']
  for ds,item in payload['test']['datasets'].items():
   order=sorted(item['metrics'],key=lambda a:item['metrics'][a]['mrr']['mean'],reverse=True)
   for i,a in enumerate(order):
    cells=[f"{item['metrics'][a][k]['mean']:.6f} ± {item['metrics'][a][k]['std']:.6f}" for k in b.METRICS];lines.append('| '+ds+' | '+NAMES[a]+' | '+' | '.join(cells)+f' | {i+1} |')
  (OUT/'06_MAIN_TABLE.md').write_text('\n'.join(lines)+'\n')
 else:(OUT/'06_MAIN_TABLE.md').write_text('# Main table\n\nValidation gates pending or failed; no new test-table entry. V17.3 frozen100-epoch table remains the reference audit.\n')
 interpretation='Complementarity to NCNC is supported by the specified validation and test gates.' if decision=='INNOVATION_1_PAPER_READY' else 'No paper-ready conclusion; interpret the recorded phase gates and measured deltas. A failed short-budget screen supports rejection under this protocol, not a proof of universal information redundancy.'
 (OUT/'07_INTERPRETATION.md').write_text('# Interpretation\n\n'+interpretation+'\n\nMECHANISM: CONTEXT_DRIVEN\nSIZE_CAUSAL_CLAIM: NOT_SUPPORTED\nNo post-result rescue. Matching train negatives and RNG traces are explicitly verified; cross-backbone matching is not asserted.\n')
 summary=['# V17.4 strong backbone transfer','','STATUS: '+state,'DECISION: '+decision,'R_HSPE_FROZEN: TRUE','INNOVATION_1: '+payload['INNOVATION_1'],'COMPLEMENTARY_SIGNAL: '+('SUPPORTED' if decision=='INNOVATION_1_PAPER_READY' else 'NOT_SUPPORTED / PENDING'),'TEST: '+('COMPLETE' if 'test' in payload else 'OFF / NOT_REACHED'),'MAIN_TABLE_RANK: see06_MAIN_TABLE.md','NEXT_EXPECTED_STEP: retrieve results and decide scientific positioning; no automatic Innovation2.','','Added parameters:75; overhead depends on host architecture, recorded per arm. NCN/NCNC backbone unchanged. Training/inference/feature-cache seconds and peak GPU memory in per-arm results and phase feature metadata.','Baseline reuse rejected because prior epochs100 differ from current5/10; epoch budget and final-checkpoint rule explicitly follow V17.4.','PhaseA and B compare identical initialization, official train sampler, per-epoch negatives, permutations and CUDA RNG trace within each host/seed.','',interpretation]
 for key in ('A','B','third'):
  if key in payload:summary+=['',key+' EFFECTS:',json.dumps(payload[key]['effects'],indent=2),key+' GATES:',json.dumps(payload[key]['gates'],indent=2)]
 if 'test' in payload:summary+=['','TEST EFFECTS:',json.dumps({ds:v['effects'] for ds,v in payload['test']['datasets'].items()},indent=2)]
 summary+=['','DETAILS:',json.dumps(extra,indent=2)];(OUT/'FINAL_REPORT.md').write_text('\n'.join(summary)+'\n')
 (OUT/'C2C_HANDOFF.md').write_text('STATUS: '+('EXECUTED' if state=='COMPLETE' else state)+'\nDIRECTION: R_HSPE_STRONG_BACKBONE_TRANSFER\nR_HSPE: FROZEN\nDECISION: '+decision+'\nINNOVATION_1: '+payload['INNOVATION_1']+'\nNEXT_EXPECTED_STEP: retrieve and assess results; no Innovation2\n')
 return payload
def launch(args,threads=4):
 logs=OUT/'logs';logs.mkdir(exist_ok=True);env=os.environ.copy()
 for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):env[k]=str(threads)
 log=logs/('_'.join(map(str,args))+'.log')
 with log.open('a') as fh:p=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*map(str,args)],stdin=subprocess.DEVNULL,stdout=fh,stderr=subprocess.STDOUT,env=env,start_new_session=True)
 return {'proc':p,'args':args,'log':str(log)}
def batch(jobs,stage,parallel=2):
 queue=list(jobs);active=[]
 while queue or active:
  for x in list(active):
   if x['proc'].poll() is not None:
    active.remove(x)
    if x['proc'].returncode:raise RuntimeError('STOP_JOB_FAILED '+str(x['args'])+' '+x['log'])
  while queue and len(active)<parallel:active.append(launch(queue.pop(0)))
  write(OUT/'status.json',{'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'updated_at':time.time(),'queued_jobs':len(queue),'active':[{'pid':x['proc'].pid,'args':x['args'],'log':x['log']} for x in active]})
  if active:time.sleep(5)
def phase_execute(phase,datasets,seeds,epochs,arms):
 # First dataset GPU training overlaps second dataset CPU feature construction.
 preps={ds:launch(('prepare',phase,ds,epochs,','.join(map(str,seeds))),threads=4) for ds in datasets[:1]};pending=list(datasets[1:]);waiting=[(ds,s,a) for ds in datasets for s in seeds for a in arms];active=[];ready=set()
 while waiting or active or preps:
  for ds,x in list(preps.items()):
   if x['proc'].poll() is not None:
    if x['proc'].returncode:raise RuntimeError('STOP_FEATURE_FAILED '+ds+' '+x['log'])
    ready.add(ds);del preps[ds]
  if not preps and pending:
   ds=pending.pop(0);preps[ds]=launch(('prepare',phase,ds,epochs,','.join(map(str,seeds))),threads=4)
  for x in list(active):
   if x['proc'].poll() is not None:
    active.remove(x)
    if x['proc'].returncode:raise RuntimeError('STOP_TRAIN_FAILED '+str(x['args'])+' '+x['log'])
  while len(active)<2:
   available=next((j for j in waiting if j[0] in ready),None)
   if available is None:break
   waiting.remove(available);ds,s,a=available
   if (jobpath(phase,ds,s,a)/'result.json').exists():continue
   active.append(launch(('run',phase,ds,s,a,epochs)))
  write(OUT/'status.json',{'state':'RUNNING','stage':'PHASE_'+phase,'supervisor_pid':os.getpid(),'updated_at':time.time(),'queued_jobs':len(waiting),'feature_preparation':[{'dataset':ds,'pid':x['proc'].pid} for ds,x in preps.items()],'active':[{'pid':x['proc'].pid,'args':x['args'],'log':x['log']} for x in active]})
  if active or preps:time.sleep(5)
def supervise():
 try:
  assert_frozen();reports('RUNNING','PHASE_A_RUNNING');phase_execute('A',('cora','pubmed'),[0,1,2],5,ARMS)
  a=summarize('A',('cora','pubmed'),[0,1,2],ARMS);write(OUT/'PHASE_A.json',a)
  if not a['all_pass']:
   decision='STRONG_BACKBONE_TRANSFER_DATASET_DEPENDENT' if any(x['pass'] for x in a['gates'].values()) else 'R_HSPE_REDUNDANT_TO_NCNC'
   reports('COMPLETE',decision,{'test_accessed':False,'stop_reason':'PhaseA strict dual-dataset gate not passed'});write(OUT/'status.json',{'state':'COMPLETE','decision':decision,'test_accessed':False,'ended_at':time.time()});return
  reports('RUNNING','PHASE_B_RUNNING');phase_execute('B',('cora','pubmed'),list(range(5)),10,ARMS)
  formal=summarize('B',('cora','pubmed'),list(range(5)),ARMS);write(OUT/'PHASE_B.json',formal)
  if not formal['all_pass']:
   reports('COMPLETE','R_HSPE_REDUNDANT_TO_STRONG_PAIRWISE_BACKBONE',{'test_accessed':False,'stop_reason':'Formal validation gate not passed'});write(OUT/'status.json',{'state':'COMPLETE','decision':'R_HSPE_REDUNDANT_TO_STRONG_PAIRWISE_BACKBONE','test_accessed':False,'ended_at':time.time()});return
  # Freeze exact10-epoch integration before any test score or third-dataset training.
  checkpoints={str(jobpath('B',ds,s,arm)/'final.pt'):sha(jobpath('B',ds,s,arm)/'final.pt') for ds in ('cora','pubmed') for s in range(5) for arm in ARMS}
  write(OUT/'INTEGRATION_FROZEN.json',{'state':'FROZEN','checkpoints':checkpoints,'configuration':'V17.4 additive75param decoder residual; fixed final10epochs; no tuning','adapter_sha256':sha(Path(__file__)),'frozen_before_test':time.time()})
  reports('RUNNING','STRONG_BACKBONE_TRANSFER_CONFIRMED');phase_execute('third',('citeseer',),[0,1,2],10,('C0','C1','C2'))
  third=summarize('third',('citeseer',),[0,1,2],('C0','C1','C2'));write(OUT/'THIRD.json',third)
  datasets=('cora','pubmed')+(('citeseer',) if third['all_pass'] else ())
  for ds in datasets:
   task=launch(('test-features',ds));task['proc'].wait()
   if task['proc'].returncode:raise RuntimeError('STOP_TEST_FEATURES_FAILED '+task['log'])
  jobs=[]
  for ds in datasets:
   arms=('C0','C1','C2')+(('N0','N1') if formal['backbone_independent'] and ds!='citeseer' else ())
   jobs.extend([('test',ds,s,arm) for s in range(3 if ds=='citeseer' else 5) for arm in arms])
  batch(jobs,'ONE_SHOT_TEST');tests=test_summary(datasets,formal['backbone_independent']);write(OUT/'TEST.json',tests)
  decision='INNOVATION_1_PAPER_READY' if tests['cora_pubmed_pass'] else 'R_HSPE_REDUNDANT_TO_STRONG_PAIRWISE_BACKBONE'
  flags=['STRONG_BACKBONE_TRANSFER_CONFIRMED']
  if formal['backbone_independent']:flags.append('BACKBONE_INDEPENDENT_TRANSFER_SUPPORTED')
  flags.append('THREE_DATASET_TRANSFER_SUPPORTED' if 'citeseer' in tests['datasets'] and tests['passes']['citeseer'] else 'THIRD_DATASET_TRANSFER_FAIL')
  if any(abs(formal['effects'][ds]['delta_ncnc']['mean'])<.002 for ds in ('cora','pubmed')):flags.append('STATISTICALLY_DIRECTIONAL_BUT_SMALL')
  reports('COMPLETE',decision,{'flags':flags,'test_accessed':True});write(OUT/'status.json',{'state':'COMPLETE','decision':decision,'flags':flags,'ended_at':time.time()})
 except Exception as e:
  write(OUT/'ERROR.json',{'error':repr(e),'traceback':traceback.format_exc()});reports('STOPPED_AUDIT_OR_EXECUTION_FAILURE','STOP',{'error':repr(e)});write(OUT/'status.json',{'state':'STOPPED_AUDIT_OR_EXECUTION_FAILURE','error':repr(e),'ended_at':time.time()});raise
if __name__=='__main__':
 command=sys.argv[1]
 if command=='preflight':preflight()
 elif command=='prepare':prepare(sys.argv[2],sys.argv[3],int(sys.argv[4]),list(map(int,sys.argv[5].split(','))))
 elif command=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
 elif command=='test-features':test_feature(sys.argv[2])
 elif command=='test':test_run(sys.argv[2],int(sys.argv[3]),sys.argv[4])
 elif command=='supervise':supervise()
 else:raise ValueError(command)
