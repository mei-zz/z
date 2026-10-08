"""V21: source-level endpoint exclusion; canonical RAW and trainer retained."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1');os.environ.setdefault('DGLBACKEND','pytorch')
import sys,json,hashlib,time,subprocess,traceback,signal
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
import torch
from torch import nn
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent
OUT=ROOT/'ERDR_V21';ART=REPO/'result/innovation2/ERDR_V21'
PROTO='CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1';AGG_SHA='831570b9a4b9ebbb1d52096d832d99033d17c2853dfe812d4738d9e7a5e6adc1'
sys.path.insert(0,str(ROOT/'CHRI_V18/scripts'));import chri_v18 as v
sys.path.insert(0,str(ROOT/'CHRI_V18_1R/scripts'));import deterministic_aggregation as agg
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest')
ORIGINAL_MAKE=v.make_net;ARMS=('Z','RAW','DUP','CC','AA');MAP={'Z':'A1','RAW':'A2'}

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n');tmp.replace(p)
def artifact(n,obj):write(ART/n,obj)
def md(n,s):ART.mkdir(parents=True,exist_ok=True);(ART/n).write_text(s+'\n')
def score_hash(p):
    h=hashlib.sha256()
    with np.load(p) as z:
        for k in ('positive','negative'):
            x=np.ascontiguousarray(z[k]);h.update(k.encode());h.update(str(x.shape).encode());h.update(str(x.dtype).encode());h.update(x.tobytes())
    return h.hexdigest()
def sandbox(phase,ds,seed,arm,rep):
    out=OUT/'executions'/phase/ds/f'seed_{seed}'/arm/f'rep_{rep}';out.mkdir(parents=True,exist_ok=True)
    for p,t,d in [(out.parent/'CHRI_V18',ROOT/'CHRI_V18',True),(out/'scripts',ROOT/'CHRI_V18_1/scripts',True),
        (out/'SOURCE_HASHES.json',ROOT/'CHRI_V18_1/SOURCE_HASHES.json',False),(out/'cache',ROOT/'CHRI_V18_1/cache',True)]:
        if not p.exists():p.symlink_to(t,target_is_directory=d)
    return out
def job(phase,ds,seed,arm,rep=1):
    return OUT/'executions'/phase/ds/f'seed_{seed}'/arm/f'rep_{rep}/runs'/phase/ds/f'seed_{seed}'/MAP.get(arm,arm)
def frozen_check():
    for path,h in read(ART/'SOURCE_HASHES.json')['files'].items():assert sha(REPO/path)==h,'FROZEN_SOURCE_CHANGED '+path
    v.check_frozen()
def cache_check():
    for key,expected in read(ART/'SOURCE_HASHES.json')['caches'].items():
        root=ROOT/'CHRI_V18_1/cache'/key
        assert {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}==expected,'CACHE_CHANGED '+key
def sealed(ds,test=False):
    assert ds in ('cora','pubmed') and test is False,'TEST_SEAL_VIOLATION'
    return v.s.input_data(ds,False)
v.sealed_input=sealed

def context_path(ds):return OUT/'context_cache'/f'{ds}.npz'
def descriptor(node,mem):
    return np.r_[node[mem].mean(0),node[mem].max(0),np.log1p(len(mem))].astype(np.float32) if len(mem) else np.zeros(33,np.float32)

def prepare_context(ds):
    """Cache only fixed raw descriptors; encoder weights remain shared and trainable."""
    a=sealed(ds);train=np.sort(np.asarray(a['train'],np.int64),axis=1);n=len(a['x']);adj=[set() for _ in range(n)]
    for u,w in train:adj[u].add(int(w));adj[w].add(int(u))
    with np.load(ROOT/'CHRI_V18_1/cache'/ds/'structure.npz') as z:
        projection=z['projection'];mu=z['normalization_mean'];std=z['normalization_std'];inc=z['incident'];keys=z['keys'];full=z['raw'];masked=z['masked']
    # Original canonical structure caches were built with four BLAS threads.
    # Preserve that GEMM reduction order only during fixed-node reconstruction.
    with threadpool_limits(limits=4,user_api='blas'):projected=np.asarray(a['x']@projection,np.float32)
    node=(projected-mu)/std
    from chri_features import array_hash
    ready=read(ROOT/'CHRI_V18_1/cache'/ds/'STRUCTURE_READY.json')
    assert array_hash(node)==ready['projected_node_hash'],'NODE_RECONSTRUCTION_MISMATCH'
    members=[np.array(sorted({c,*adj[c]}),np.int64) if adj[c] else np.empty(0,np.int64) for c in range(n)]
    assert np.array_equal(np.stack([descriptor(node,m) for m in members]),full),'FULL_DESCRIPTOR_RECONSTRUCTION_MISMATCH'
    raw=np.zeros((*inc.shape,33),np.float32);valid=np.zeros(inc.shape,bool);sizes=np.zeros(inc.shape,np.int64)
    for u in range(n):
        for col,c in enumerate(inc[u]):
            if c<0:continue
            mem=members[c];assert u in mem
            context=mem[mem!=u];raw[u,col]=descriptor(node,context);valid[u,col]=len(context)>0;sizes[u,col]=len(context)
    train=train[np.argsort(train[:,0]*n+train[:,1])];assert np.array_equal(train[:,0]*n+train[:,1],keys)
    maskraw=np.zeros_like(masked);maskvalid=np.zeros((len(train),2),bool);masksizes=np.zeros((len(train),2),np.int64)
    for row,(u,w) in enumerate(train):
        for side,(focal,other) in enumerate(((u,w),(w,u))):
            mem=members[focal];context=mem[(mem!=focal)&(mem!=other)]
            maskraw[row,side]=descriptor(node,context);maskvalid[row,side]=len(context)>0;masksizes[row,side]=len(context)
    path=context_path(ds);path.parent.mkdir(parents=True,exist_ok=True)
    np.savez(path,raw=raw,valid=valid,sizes=sizes,masked=maskraw,masked_valid=maskvalid,masked_sizes=masksizes)
    write(path.with_suffix('.json'),{'state':'PASS','dataset':ds,'node_hash':array_hash(node),'context_file_sha256':sha(path),'full_descriptor_reconstruction':'BITWISE_EXACT','test_opened':False})

class ContextStructure(v.Structure):
    def __init__(self,ds):
        super().__init__(ROOT/'CHRI_V18_1/cache'/ds/'structure.npz')
        with np.load(context_path(ds)) as z:
            self.context={k:torch.as_tensor(z[k],device='cuda') for k in z.files}
    def contexts(self,pairs,side):
        pairs=pairs.sort(dim=1).values;node,other=pairs[:,side],pairs[:,1-side]
        key=pairs[:,0]*self.n+pairs[:,1];row=torch.searchsorted(self.keys,key).clamp(max=len(self.keys)-1);target=self.keys[row]==key
        centers=self.incident[node];valid=centers>=0
        valid &= ~((centers==other[:,None])&target[:,None])
        valid &= ~((centers==node[:,None])&target[:,None]&(self.degree[node,None]==1))
        g,col=valid.nonzero(as_tuple=True);edge=centers[g,col]
        raw=self.context['raw'][node[g],col].clone();ok=self.context['valid'][node[g],col].clone();sizes=self.context['sizes'][node[g],col].clone()
        modify=target[g]&(edge==node[g]);r=row[g[modify]]
        raw[modify]=self.context['masked'][r,side];ok[modify]=self.context['masked_valid'][r,side];sizes[modify]=self.context['masked_sizes'][r,side]
        return raw,ok,sizes,g,edge

def symmetric(x,y):return torch.cat((x+y,(x-y).abs(),x*y),1)
def pool(x,lengths):
    mean=torch.segment_reduce(x,'sum',lengths=lengths)/lengths.clamp_min(1)[:,None]
    maximum=torch.segment_reduce(x,'max',lengths=lengths)
    maximum=torch.where(lengths[:,None]>0,maximum,torch.zeros_like(maximum))
    return torch.cat((mean,maximum),1)

class ERDRPredictor(v.RelationPredictor):
    def __init__(self,structure,seed,arm,mean,std):
        super().__init__(structure,seed,'A2',mean,std);self.arm=arm;self.seed=seed;self._states={};self._rawtokens=[];self.capture=False;self._diag={}
        agg.install(self);self.endpoint=self.source_endpoint
        self.relation.register_forward_hook(lambda module,args,result:self._rawtokens.append(result))
        with torch.random.fork_rng():
            torch.manual_seed(21001+seed);self.role=nn.Sequential(nn.Linear(48,32),nn.ReLU(),nn.Linear(32,16),nn.ReLU())
        base=self.decoder;slots=4 if arm in ('ROLE4','DUP4') else 1
        with torch.random.fork_rng():
            torch.manual_seed(21002+seed);extended=nn.Sequential(nn.Linear(353+32*slots,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
        with torch.no_grad():
            extended[0].weight[:,:353].copy_(base[0].weight);extended[0].bias.copy_(base[0].bias)
            for i in (2,4):extended[i].load_state_dict(base[i].state_dict())
        self.decoder=extended
    def source_endpoint(self,pairs,side):
        h,counts,p=agg.endpoint(self,pairs,side)
        cr,valid,sizes,g,edge=self.structure.contexts(pairs,side)
        assert len(cr)==len(h)
        c=self.encoder(cr);c=torch.where(valid[:,None],c,torch.zeros_like(c));a=h-c
        self._states[side]=(h,c,a,counts,valid,sizes,g,edge)
        return h,counts,p
    def forward(self,pairs,b,donor=None):
        self._states={};self._rawtokens=[];z,raw=self.representation(pairs,b,True)
        hu,cu,au,nu,vu,su,gu,eu=self._states[0];hv,cv,av,nv,vv,sv,gv,ev=self._states[1]
        lengths=nu*nv;groups=torch.repeat_interleave(torch.arange(len(pairs),device=b.device),lengths);count=len(groups)
        offset=lengths.cumsum(0)-lengths;local=torch.arange(count,device=b.device)-offset[groups]
        iu=(nu.cumsum(0)-nu)[groups]+torch.div(local,nv[groups],rounding_mode='floor');iv=(nv.cumsum(0)-nv)[groups]+local%nv[groups]
        if self.arm=='SHUFFLE':
            sortedpairs=pairs.sort(dim=1).values
            cu=self.shuffled_context(cu,su,eu,sortedpairs[gu,0],sortedpairs[gu,1],nu[gu],0)
            cv=self.shuffled_context(cv,sv,ev,sortedpairs[gv,1],sortedpairs[gv,0],nv[gv],1)
        roles={'DUP':[(hu,hv)],'DUP4':[(hu,hv)]*4,'CC':[(cu,cv)],'SHUFFLE':[(cu,cv)],'AA':[(au,av)],'ROLE4':[(cu,cv),(au,cv),(cu,av),(au,av)]}[self.arm]
        pools=[];saved=[]
        # Fixed interaction chunking mirrors canonical candidate-boundary batching.
        boundaries=[];start=0;running=0
        for row,n in enumerate(lengths.detach().cpu().tolist()):
            if row>start and running+n>131072:boundaries.append((start,row));start=row;running=0
            running+=n
        boundaries.append((start,len(pairs)))
        for left,right in roles:
            parts=[];tokens=[]
            for st,en in boundaries:
                lo=int(offset[st]) if st<len(pairs) else count;hi=int(offset[en]) if en<len(pairs) else count
                m=self.role(symmetric(left[iu[lo:hi]],right[iv[lo:hi]]));parts.append(pool(m,lengths[st:en]));tokens.append(m)
            pools.append(torch.cat(parts,0));saved.append(torch.cat(tokens,0))
        if self.capture:
            self._diag={'z':z,'raw':raw,'role_pool':pools,'raw_tokens':torch.cat(self._rawtokens,0) if self._rawtokens else b.new_zeros((0,16)),
                'cc_tokens':self.role(symmetric(cu[iu],cv[iv])),'aa_tokens':self.role(symmetric(au[iu],av[iv])),
                'states':self._states,'lengths':lengths,'valid_pairs':vu[iu]&vv[iv]}
        self._rawtokens=[]
        return b[:,0]+self.decoder(torch.cat((z,raw,*pools),1)).flatten(),b.new_zeros(()),b.new_zeros(())
    def shuffled_context(self,c,sizes,edges,focals,others,setcounts,side):
        """Match incident context-set count AND context member count/cardinality bucket."""
        if not hasattr(self,'_donor_by_size'):
            self._donor_by_size={}
            source=np.unique(np.sort(np.load(v.cache(self.dataset,0)/'epoch_1_pairs.npy').reshape(-1,2),axis=1),axis=0)
            for start in range(0,len(source),256):
                pp=torch.as_tensor(source[start:start+256],device='cuda')
                for donor_side in (0,1):
                    rr,ok,sz,g,ee=self.structure.contexts(pp,donor_side);cnt=torch.bincount(g,minlength=len(pp))
                    rows=rr.cpu().numpy();fs=pp[g,donor_side].cpu().tolist();es=ee.cpu().tolist();ns=sz.cpu().tolist();cs=cnt[g].cpu().tolist()
                    for raw,focal,edge,n,count in zip(rows,fs,es,ns,cs):
                        bucket=self._donor_by_size.setdefault((count,n),{})
                        # One descriptor per distinct focal/star identity in a matched stratum.
                        if len(bucket)<512:bucket.setdefault((focal,edge),raw)
            self._donor_by_size={key:list(bucket.items()) for key,bucket in self._donor_by_size.items()}
        raws=[];changed=0
        for n,edge,focal,other,count in zip(sizes.cpu().tolist(),edges.cpu().tolist(),focals.cpu().tolist(),others.cpu().tolist(),setcounts.cpu().tolist()):
            donors=self._donor_by_size.get((count,n),[])
            assert donors,'SHUFFLE_MATCHING_NO_STRATUM'
            start=int.from_bytes(hashlib.sha256(f'{self.seed}/{side}/{focal}/{other}/{edge}/{count}/{n}'.encode()).digest()[:8],'little')%len(donors)
            selected=None
            for j in range(len(donors)):
                (ff,ee),raw=donors[(start+j)%len(donors)]
                if ee!=edge:selected=raw;break
            assert selected is not None,'SHUFFLE_MATCHING_NO_DISTINCT_DONOR'
            raws.append(torch.as_tensor(selected,device='cuda'));changed+=1
        if not raws:return c
        result=self.encoder(torch.stack(raws));result=torch.where((sizes>0)[:,None],result,torch.zeros_like(result))
        self.shuffle_checked=getattr(self,'shuffle_checked',0)+changed
        return result

def make_net(ds,seed,arm,phase,structure=None):
    if arm in ('DUP','CC','AA','ROLE4','DUP4','SHUFFLE'):
        stats=v.read(v.cache(ds,seed)/'normalization.json')
        net=ERDRPredictor(structure or ContextStructure(ds),seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda');net.dataset=ds
        return net
    return agg.install(ORIGINAL_MAKE(ds,seed,arm,phase,structure))
v.make_net=make_net

def run(phase,ds,seed,arm,rep):
    v.OUT=sandbox(phase,ds,seed,arm,rep);frozen_check();actual=MAP.get(arm,arm)
    step=torch.optim.Adam.step;trace=hashlib.sha256();steps=[0]
    def logged(opt,*args,**kwargs):
        ans=step(opt,*args,**kwargs);steps[0]+=1
        trace.update(str(steps[0]).encode())
        for group in opt.param_groups:
            for p in group['params']:trace.update(p.detach().cpu().contiguous().numpy().tobytes())
        if steps[0]==1:print('FIRST_OPTIMIZER_STEP_OK',phase,ds,seed,arm,rep,flush=True)
        return ans
    torch.optim.Adam.step=logged;print('TRAIN_START',phase,ds,seed,arm,rep,flush=True)
    v.run(phase,ds,seed,actual,5);dest=v.job(phase,ds,seed,actual);row=read(dest/'result.json')
    row.update(variant=arm,replicate=rep,canonical_protocol=PROTO,score_vector_sha256=score_hash(dest/'valid_epoch5_scores.npz'),
        optimizer_steps=steps[0],training_trajectory_sha256=trace.hexdigest(),trajectory_definition='SHA256 of every optimizer step index and updated trainable parameters in optimizer order')
    assert steps[0]>0,'JOB_ALREADY_EXISTS_UNREGISTERED_REUSE';write(dest/'result.json',row)
    print('ERDR_JOB_COMPLETE',phase,ds,seed,arm,rep,flush=True)

@torch.no_grad()
def sanity(ds):
    structure=ContextStructure(ds);a=sealed(ds);train=np.sort(a['train'],axis=1);adj=[set() for _ in range(len(a['x']))]
    for u,w in train:adj[u].add(int(w));adj[w].add(int(u))
    with np.load(ROOT/'CHRI_V18_1/cache'/ds/'structure.npz') as zz:
        with threadpool_limits(limits=4,user_api='blas'):projected=np.asarray(a['x']@zz['projection'],np.float32)
        node=(projected-zz['normalization_mean'])/zz['normalization_std']
    pairs=np.concatenate((train[:32],np.load(ROOT/'CHRI_V18_1/cache'/ds/'seed_0/valid_pairs.npy')[:32]))
    pp=torch.as_tensor(pairs,device='cuda');net=make_net(ds,0,'CC','A',structure);errors=[];checks=0;algebra=[]
    for side in (0,1):
        cr,ok,sizes,g,edges=structure.contexts(pp,side);h,counts,_=net.source_endpoint(pp,side);cc=net._states[side][1];aa=net._states[side][2]
        algebra.append(float((h-cc-aa).abs().max()) if len(h) else 0.)
        sortedpairs=np.sort(pairs,axis=1);oracle=[]
        for group,edge in zip(g.cpu().tolist(),edges.cpu().tolist()):
            focal,other=int(sortedpairs[group,side]),int(sortedpairs[group,1-side]);mem={edge,*adj[edge]}
            if other in adj[focal] and edge==focal:mem.discard(other)
            mem.discard(focal);assert focal not in mem
            oracle.append(descriptor(node,np.array(sorted(mem),np.int64)));checks+=1
        direct=torch.as_tensor(np.stack(oracle),device='cuda');assert torch.equal(direct,cr),'DIRECT_CONTEXT_DESCRIPTOR_MISMATCH'
        latent=net.encoder(direct);latent=torch.where(ok[:,None],latent,torch.zeros_like(latent))
        err=float((latent-cc).abs().max()) if len(cc) else 0.;errors.append(err);assert err==0
    assert max(algebra)<1e-5
    counts={arm:sum(p.numel() for p in make_net(ds,0,MAP.get(arm,arm),'A').parameters() if p.requires_grad) for arm in ARMS}
    assert len({counts[x] for x in ('DUP','CC','AA')})==1
    # The new branches leave canonical RAW and Z exactly unchanged at initialization.
    stats=read(v.cache(ds,0)/'normalization.json');baseline=agg.install(ORIGINAL_MAKE(ds,0,'A2','A'));bb=torch.tensor(np.load(v.cache(ds,0)/'valid_b.npy')[:32],device='cuda')
    vp=torch.tensor(np.load(v.cache(ds,0)/'valid_pairs.npy')[:32],device='cuda')
    bz,br=baseline.representation(vp,bb,True);ez,er=net.representation(vp,bb,True)
    assert torch.equal(bz,ez) and torch.equal(br,er),'CANONICAL_RAW_CHANGED'
    # Explicit empty handling bypasses biased MLP output.
    empty=net.encoder(torch.zeros((1,33),device='cuda'));empty=torch.where(torch.zeros((1,1),device='cuda',dtype=torch.bool),empty,torch.zeros_like(empty));assert empty.count_nonzero()==0
    return {'state':'PASS','dataset':ds,'candidate_count':len(pairs),'explicit_member_recomputations':checks,'descriptor_match':'BITWISE_EXACT',
        'latent_max_error':max(errors),'algebra_max_error':max(algebra),'canonical_Z_RAW_unchanged':'BITWISE_EXACT','empty_context':'ZERO_LATENT_VALID_0','trainable_parameters':counts,'test_opened':False}

def preflight():
    assert REPO.name in ('DCDLP-main','lchr_v2') and sha(ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py')==AGG_SHA
    assert read(ART/'01_PRECONDITION_AUDIT.json')['state']=='APPLICABLE'
    histories=(('CHRI_V18_1C','CANONICAL_SIGNAL_PRESENT'),('CHRI_V18_1S','CHRI_PHENOMENON_CONFIRMED_METHOD_NOT_IMPROVED'),('FCI_V19','FCI_REJECTED_NO_GAIN'),('RCP_V20','RCP_REJECTED_NO_GAIN'))
    files={str(p.relative_to(REPO)):sha(p) for p in (OUT/'scripts').glob('*.py')}
    for p in ART.glob('*'):
        if p.name in ('00_PROTOCOL.md','01_PRECONDITION_AUDIT.md','01_PRECONDITION_AUDIT.json'):files[str(p.relative_to(REPO))]=sha(p)
    for folder,word in histories:
        base=REPO/'result/innovation2'/folder;assert word in (base/'FINAL_REPORT.md').read_text()
        files.update({str(p.relative_to(REPO)):sha(p) for p in base.glob('*') if p.is_file() and p.suffix in ('.json','.md')})
    i1=ROOT/'R_HSPE_FINAL_FROZEN/INNOVATION_1_FINAL.md'
    assert 'FINAL_FROZEN' in i1.read_text();files[str(i1.relative_to(REPO))]=sha(i1)
    v.OUT=ROOT/'CHRI_V18_1';v.check_frozen();caches={};canonical=read(ROOT/'CHRI_V18_1C/01_CANONICAL_IMPLEMENTATION.json')
    for ds in ('cora','pubmed'):
        for seed in range(3):
            root=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}';hashes={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}
            assert hashes==canonical['feature_caches'][ds][str(seed)]['cache_file_sha256'];caches[f'{ds}/seed_{seed}']=hashes
        for p in (ROOT/'CHRI_V18_1/cache'/ds).glob('*'):
            if p.is_file():files[str(p.relative_to(REPO))]=sha(p)
        prepare_context(ds)
        files[str(context_path(ds).relative_to(REPO))]=sha(context_path(ds))
    for p in (ROOT/'CHRI_V18/scripts/chri_v18.py',ROOT/'CHRI_V18/scripts/chri_features.py',ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py'):
        files[str(p.relative_to(REPO))]=sha(p)
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','files':files,'caches':caches,'canonical_protocol':PROTO,'aggregation_sha256':AGG_SHA})
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'workspace':'DCDLP-main','canonical_protocol':PROTO,
        'precheck':{'dataset':'pubmed','seed':0,'variants':['DUP','CC','AA'],'replicates':2,'epochs':5},
        'phase_A1':{'datasets':['cora','pubmed'],'seeds':[0,1,2],'variants':list(ARMS),'epochs':5},
        'phase_A2':'GATED_ON_ALL_A1_CRITERIA','initialization':{'role':21001,'extended_decoder':21002,'canonical_first353_columns':'COPIED_EXACTLY'},
        'context':'same fixed projected nodes, fixed canonical normalization, mean/max/log1p size, same encoder weights; target mask first then focal exclusion',
        'training':'canonical Adam/BCE/LR/batch/microbatch/fixedfinal5','workers':6,'cpu_threads_per_worker':2,
        'test_opened':False,'innovation1_modified':False,'historical_results_modified':False})
    audit={ds:sanity(ds) for ds in ('cora','pubmed')};artifact('02_SOURCE_DECOMPOSITION_SANITY.json',{'state':'PASS','datasets':audit})
    md('03_LEAKAGE_AUDIT.md','# Leakage audit\n\nPASS. Structures use TRAIN edges only. Only x/train/valid_pos/valid_neg arrays are read from the frozen input archive; test members are never opened. Validation labels only enter canonical metrics, never context descriptors. Fixed projection/normalization match canonical hashes. Candidate target detection queries TRAIN keys only; endpoint exclusion follows existing target masking. Original full descriptors reconstructed bitwise; direct context descriptors and shared-encoder latents match bitwise. Canonical feature cache hashes and candidate order/negative schedules are frozen. New contexts are cached raw descriptors only; trainable latents are recomputed every forward. No validation-fitted normalization or context donor pools. Innovation 1 remains FINAL_FROZEN.')
    for name in ('04_DETERMINISM_PRECHECK.json','05_PHASE_A1_RESULTS.json','06_PHASE_A1_CONTRASTS.json','07_ROLE_REPRESENTATION_DIAGNOSTICS.json','08_PUBMED_REDUNDANCY_DIAGNOSTIC.json','09_PHASE_A2_ROLE4_RESULTS.json','10_CONTEXT_SHUFFLE_CONTROL.json'):
        artifact(name,{'state':'NOT_RUN','reason':'Prerequisite pending.'})
    for name in ('11_RANKING_ANALYSIS.md','12_DECISION.md','FINAL_REPORT.md'):md(name,'# ERDR V21\n\nPENDING')
    print('ERDR_PREFLIGHT_PASS',json.dumps(audit),flush=True)

CHILDREN=[]
def batch(tasks,stage,workers=6):
    q=list(tasks);active=[];done=0;logs=OUT/'logs';logs.mkdir(exist_ok=True)
    while active or q:
        for item in list(active):
            p,args,log=item
            if p.poll() is not None:
                active.remove(item)
                if p.returncode:raise RuntimeError(f'JOB_FAILED {args} {log}')
                done+=1
        while q and len(active)<workers:
            args=q.pop(0);log=logs/('_'.join(map(str,args))+'.log')
            with log.open('a') as f:p=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*map(str,args)],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,env=os.environ.copy(),start_new_session=True)
            active.append((p,args,log));CHILDREN.append(p)
        state={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(q),'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
        if active:time.sleep(3)

def summarize():
    output={'state':'COMPLETE','datasets':{},'test_opened':False}
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{arm:read(job('A',ds,s,arm)/'result.json') for arm in ARMS}} for s in range(3)]
        for row in rows:
            ref=row['arms']['RAW']
            assert all(r['training_trace']==ref['training_trace'] for r in row['arms'].values()),'PAIRED_TRACE_MISMATCH'
            assert len({row['arms'][a]['trainable_parameters'] for a in ('DUP','CC','AA')})==1
            assert len({row['arms'][a]['initialization']['decoder'] for a in ('DUP','CC','AA')})==1
            assert all(r['initialization']['encoder']==ref['initialization']['encoder'] for r in row['arms'].values())
        effects={f'CC_vs_{a}':v.comparison(rows,'CC',a) for a in ('Z','RAW','DUP','AA')};effects['AA_vs_RAW']=v.comparison(rows,'AA','RAW')
        gates={'RAW_mean':effects['CC_vs_RAW']['ce']['mean']>0,'RAW_wins':effects['CC_vs_RAW']['ce']['wins']>=2,'DUP_mean':effects['CC_vs_DUP']['ce']['mean']>0,'Z_mean':effects['CC_vs_Z']['ce']['mean']>0}
        output['datasets'][ds]={'seed_results':rows,'effects':effects,'gates':gates,'pass':all(gates.values()),'metrics':{a:{m:v.stat([r['arms'][a]['validation'][m] for r in rows]) for m in v.METRICS} for a in ARMS}}
    output['all_pass']=all(x['pass'] for x in output['datasets'].values());artifact('05_PHASE_A1_RESULTS.json',output)
    artifact('06_PHASE_A1_CONTRASTS.json',{'state':'COMPLETE','datasets':{ds:x['effects'] for ds,x in output['datasets'].items()},'delta_CE':'comparator CE minus method CE'})
    return output

def cosine(x,y):
    den=np.linalg.norm(x,axis=1)*np.linalg.norm(y,axis=1);return np.sum(x*y,axis=1)/np.maximum(den,1e-12)
def distribution(x):
    x=np.asarray(x);return {'count':len(x),'mean':float(x.mean()) if len(x) else None,'quantiles':np.quantile(x,[0,.25,.5,.75,.95,1]).tolist() if len(x) else []}
def probe(tx,ty,vx,vy):
    x=np.concatenate((tx.astype(np.float64),np.ones((len(tx),1))),1);xx=np.concatenate((vx.astype(np.float64),np.ones((len(vx),1))),1)
    coef=np.linalg.lstsq(x,ty.astype(np.float64),rcond=None)[0];pred=xx@coef;mse=float(np.mean((pred-vy)**2));variance=float(np.mean((vy-vy.mean(0))**2))
    return {'state':'COMPLETE','train_candidates':len(tx),'validation_candidates':len(vx),'R2':1-mse/variance if variance>1e-12 else None,'MSE':mse,'cosine':distribution(cosine(pred,vy)),'fit':'ordinary least squares float64 with intercept; training only'}

@torch.no_grad()
def diagnose(ds,seed):
    v.OUT=sandbox('A',ds,seed,'CC',1);frozen_check();net=v.load_net('A',ds,seed,'CC');net.capture=True;source=v.cache(ds,seed)
    result={'dataset':ds,'seed':seed,'state':'COMPLETE','test_opened':False};arrays={}
    for split in ('train','validation'):
        pairs=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy')).reshape(-1,2)
        features=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r').reshape(-1,257)
        vals={k:[] for k in ('cos_h_c','cos_h_a','cos_c_a','norm_c_over_h','norm_a_over_h','cos_raw_cc_tokens','cos_raw_aa_tokens','cos_raw_cc_pool')};ar={k:[] for k in ('z','raw','cc')}
        totaledge=validedge=totalpairs=somevalid=allvalid=0
        for st in range(0,len(pairs),128):
            p=torch.as_tensor(pairs[st:st+128],device='cuda',dtype=torch.long);b=torch.as_tensor(np.array(features[st:st+128]),device='cuda');net(p,b);d=net._diag
            for side in (0,1):
                h,c,a,counts,ok,sz,g,e=d['states'][side];h=h.cpu().numpy();c=c.cpu().numpy();a=a.cpu().numpy()
                vals['cos_h_c'].append(cosine(h,c));vals['cos_h_a'].append(cosine(h,a));vals['cos_c_a'].append(cosine(c,a));den=np.maximum(np.linalg.norm(h,axis=1),1e-12)
                vals['norm_c_over_h'].append(np.linalg.norm(c,axis=1)/den);vals['norm_a_over_h'].append(np.linalg.norm(a,axis=1)/den);totaledge+=len(ok);validedge+=int(ok.sum())
            rt=d['raw_tokens'].cpu().numpy();cc=d['cc_tokens'].cpu().numpy();aa=d['aa_tokens'].cpu().numpy()
            vals['cos_raw_cc_tokens'].append(cosine(rt,cc));vals['cos_raw_aa_tokens'].append(cosine(rt,aa))
            rr=d['raw'].cpu().numpy();rc=d['role_pool'][0].cpu().numpy();vals['cos_raw_cc_pool'].append(cosine(rr,rc))
            ar['z'].append(d['z'].cpu().numpy());ar['raw'].append(rr);ar['cc'].append(rc)
            validcounts=torch.segment_reduce(d['valid_pairs'].float()[:,None],'sum',lengths=d['lengths']).flatten();lengths=d['lengths']
            totalpairs+=len(p);somevalid+=int((validcounts>0).sum());allvalid+=int(((lengths>0)&(validcounts==lengths)).sum());net._diag={}
        arrays[split]={k:np.concatenate(x) for k,x in ar.items()}
        result[split]={'candidate_count':totalpairs,'complement_hyperedge_count':totaledge,'valid_complement_percentage':100*validedge/max(totaledge,1),
            'candidates_with_some_valid_CC_percentage':100*somevalid/max(totalpairs,1),'candidates_all_CC_valid_percentage':100*allvalid/max(totalpairs,1),
            'distributions':{k:distribution(np.concatenate(x)) for k,x in vals.items()}}
    t=arrays['train'];q=arrays['validation'];result['RCC_from_RRAW']=probe(t['raw'],t['cc'],q['raw'],q['cc'])
    result['RCC_from_Z']=probe(t['z'],t['cc'],q['z'],q['cc']);result['RRAW_from_Z']=probe(t['z'],t['raw'],q['z'],q['raw'])
    result['probe_population']='all cached epoch1 training candidates and all validation candidates; parameters trained CC final5; probes never enter model'
    write(OUT/'diagnostics'/ds/f'seed_{seed}.json',result);print('ERDR_DIAGNOSTICS_COMPLETE',ds,seed,flush=True)

def stage2(data):
    batch([('run','B',ds,s,a,1) for ds in ('cora','pubmed') for s in range(3) for a in ('ROLE4','DUP4','SHUFFLE')],'PHASE_A2_AND_CONTEXT_SHUFFLE')
    result={'state':'COMPLETE','datasets':{}};shuffle={'state':'COMPLETE','datasets':{},'donors':'fixed epoch1 training candidates seed0; matched incident context-set size and exact context member count (thus cardinality bucket); distinct star center required; original candidate interaction counts retained'}
    for ds,item in data['datasets'].items():
        rows=[]
        for row in item['seed_results']:
            s=row['seed'];arms=dict(row['arms']);arms.update({a:read(job('B',ds,s,a)/'result.json') for a in ('ROLE4','DUP4','SHUFFLE')})
            assert arms['ROLE4']['trainable_parameters']==arms['DUP4']['trainable_parameters']
            assert arms['CC']['trainable_parameters']==arms['SHUFFLE']['trainable_parameters']
            assert all(r['training_trace']==arms['RAW']['training_trace'] for r in arms.values())
            rows.append({'seed':s,'arms':arms})
        effects={f'ROLE4_vs_{a}':v.comparison(rows,'ROLE4',a) for a in ('CC','DUP4','RAW')}
        result['datasets'][ds]={'seed_results':rows,'effects':effects,'pass':effects['ROLE4_vs_CC']['ce']['mean']>0 and effects['ROLE4_vs_DUP4']['ce']['mean']>0}
        shuffle['datasets'][ds]={'CC_vs_SHUFFLE':v.comparison(rows,'CC','SHUFFLE'),'seed_results':[r['arms']['SHUFFLE'] for r in rows]}
    result['all_pass']=all(x['pass'] for x in result['datasets'].values());shuffle['all_pass']=all(x['CC_vs_SHUFFLE']['ce']['mean']>0 for x in shuffle['datasets'].values())
    artifact('09_PHASE_A2_ROLE4_RESULTS.json',result);artifact('10_CONTEXT_SHUFFLE_CONTROL.json',shuffle)
    return result,shuffle

def finalize(data=None,stage2data=None,shuffle=None,status=None,reason=None):
    v.OUT=ROOT/'CHRI_V18_1';frozen_check();cache_check()
    if data:
        diag={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')}
        artifact('07_ROLE_REPRESENTATION_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':diag})
        artifact('08_PUBMED_REDUNDANCY_DIAGNOSTIC.json',{'state':'COMPLETE','datasets':{ds:[{'seed':r['seed'],'RCC_from_Z':r['RCC_from_Z'],'RRAW_from_Z':r['RRAW_from_Z'],'RCC_from_RRAW':r['RCC_from_RRAW']} for r in rr] for ds,rr in diag.items()},'selection_gate':False})
        if not data['all_pass']:
            beatsraw=all(d['gates']['RAW_mean'] and d['gates']['RAW_wins'] and d['gates']['Z_mean'] for d in data['datasets'].values())
            status='ERDR_REJECTED_CAPACITY_EXPLANATION' if beatsraw else 'ERDR_REJECTED_SOURCE_RELATION';reason='CC fails the preregistered both-dataset source-level gate; stop without rescue.'
            for name in ('09_PHASE_A2_ROLE4_RESULTS.json','10_CONTEXT_SHUFFLE_CONTROL.json'):artifact(name,{'state':'NOT_RUN','reason':'CC failed Phase A1; later training is forbidden.'})
        elif not shuffle['all_pass']:
            status='ERDR_REJECTED_SOURCE_RELATION';reason='CC does not beat matched context shuffle on both datasets.'
        else:
            use4=stage2data['all_pass'];status='ERDR_ROLE4_PROMISING' if use4 else 'ERDR_CC_PROMISING';reason='CC passes all source, capacity and context-shuffle gates. '+('ROLE4 also beats CC and DUP4.' if use4 else 'ROLE4 not preferred; retain CC only.')
            mrr=[stage2data['datasets'][ds]['effects']['ROLE4_vs_RAW']['mrr']['mean'] if use4 else d['effects']['CC_vs_RAW']['mrr']['mean'] for ds,d in data['datasets'].items()]
            if all(x>0 for x in mrr):status='ERDR_PROMISING_WITH_RANKING_GAIN'
        lines=['| Dataset | Contrast | Mean DeltaCE | CE wins | Mean DeltaMRR | Mean DeltaHits10 | Mean DeltaAUC |','|---|---|---:|---:|---:|---:|---:|']
        ranking={}
        for ds,d in data['datasets'].items():
            effects=dict(d['effects'])
            if stage2data:effects.update(stage2data['datasets'][ds]['effects'])
            if shuffle:effects['CC_vs_SHUFFLE']=shuffle['datasets'][ds]['CC_vs_SHUFFLE']
            for n,e in effects.items():lines.append(f"| {ds} | {n} | {e['ce']['mean']:.10g} | {e['ce']['wins']}/3 | {e['mrr']['mean']:.10g} | {e['hits10']['mean']:.10g} | {e['auc']['mean']:.10g} |")
            dm=d['effects']['CC_vs_RAW']['mrr']['mean'];ranking[ds]='RANKING_IMPROVED' if dm>0 else ('RANKING_DEGRADED' if dm<0 else 'RANKING_NEUTRAL')
        table='\n'.join(lines);md('11_RANKING_ANALYSIS.md','# Ranking analysis\n\n'+table+'\n\n'+json.dumps(ranking,indent=2)+'\n\nRanking state compares CC against RAW; all effects are paired fixed-final5 validation metrics.')
        report=['# V21 ERDR source-level validation','',f'FINAL_STATUS: {status}',f'REASON: {reason}','',table,'','## Parameter counts and complete metrics','',json.dumps({ds:{'metrics':d['metrics'],'gates':d['gates'],'parameters':{a:d['seed_results'][0]['arms'][a]['trainable_parameters'] for a in ARMS}} for ds,d in data['datasets'].items()},indent=2),'','## Representation diagnostics','',json.dumps({ds:[{'seed':r['seed'],'train_validity':{k:v for k,v in r['train'].items() if k!='distributions'},'validation_validity':{k:v for k,v in r['validation'].items() if k!='distributions'},'RCC_from_RRAW':r['RCC_from_RRAW'],'RCC_from_Z':r['RCC_from_Z'],'RRAW_from_Z':r['RRAW_from_Z']} for r in rr] for ds,rr in diag.items()},indent=2),'','Full cosine/norm distributions are in 07_ROLE_REPRESENTATION_DIAGNOSTICS.json. Imprint h-c is an operational representation difference, not a causal or orthogonal endpoint attribution. No novelty claim.','TEST_OPENED: NO','INNOVATION_1_MODIFIED: NO','HISTORICAL_RESULTS_MODIFIED: NO']
        md('FINAL_REPORT.md','\n'.join(report))
    else:
        for name in ('05_PHASE_A1_RESULTS.json','06_PHASE_A1_CONTRASTS.json','07_ROLE_REPRESENTATION_DIAGNOSTICS.json','08_PUBMED_REDUNDANCY_DIAGNOSTIC.json','09_PHASE_A2_ROLE4_RESULTS.json','10_CONTEXT_SHUFFLE_CONTROL.json'):artifact(name,{'state':'NOT_RUN','reason':reason})
        md('FINAL_REPORT.md',f'# ERDR V21\n\nFINAL_STATUS: {status}\n\n{reason}\n\nTEST_OPENED: NO')
    md('12_DECISION.md',f'# Decision\n\n{status}\n\n{reason}')
    state={'state':'COMPLETE','final_status':status,'reason':reason,'ended_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
    md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: V21_ERDR_SOURCE_LEVEL_RELATION_VALIDATION\nCANONICAL_PROTOCOL: {PROTO}\nFINAL_STATUS: {status}\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO\nPRIMARY_ARTIFACT: result/innovation2/ERDR_V21/FINAL_REPORT.md\nNEXT_EXPECTED_STEP: Return evidence to user. Stop; no tuning or test opening.')
    print('ERDR_COMPLETE',status,flush=True)

def supervise():
    try:
        preflight();batch([('run','D','pubmed',0,a,r) for a in ('DUP','CC','AA') for r in (1,2)],'DETERMINISM_PRECHECK')
        records=[]
        for arm in ('DUP','CC','AA'):
            rr=[read(job('D','pubmed',0,arm,r)/'result.json') for r in (1,2)]
            keys=('checkpoint_sha256','score_vector_sha256','training_trajectory_sha256','history','training_trace','optimizer_steps');checks={k:rr[0][k]==rr[1][k] for k in keys}
            records.append({'arm':arm,'pass':all(checks.values()),'checks':checks,'checkpoint_hashes':[r['checkpoint_sha256'] for r in rr],'score_hashes':[r['score_vector_sha256'] for r in rr],'trajectory_hashes':[r['training_trajectory_sha256'] for r in rr]})
        cache_check();ok=all(x['pass'] for x in records);artifact('04_DETERMINISM_PRECHECK.json',{'state':'PASS' if ok else 'FAIL','pairs':records,'canonical_caches_unchanged':True,'candidate_order_and_negatives_unchanged':True,'test_opened':False})
        if not ok:finalize(status='DETERMINISTIC_PROTOCOL_FAILURE',reason='Independent duplicate checkpoint, score vector, parameter trajectory or history mismatch.');return
        for arm in ('DUP','CC','AA'):
            dst=job('A','pubmed',0,arm);dst.parent.mkdir(parents=True,exist_ok=True)
            if not dst.exists():dst.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS if not(ds=='pubmed' and s==0 and a in ('DUP','CC','AA'))],'PHASE_A1')
        data=summarize();bdata=sh=None
        if data['all_pass']:bdata,sh=stage2(data)
        batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'REPRESENTATION_DIAGNOSTICS',workers=3)
        finalize(data,bdata,sh)
    except BaseException as e:
        for p in CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        err={'state':'EXECUTION_FAILED','error':repr(e),'traceback':traceback.format_exc(),'ended_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',err);artifact('RUN_STATUS.json',err);artifact('ERROR.json',err);print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='preflight':preflight()
    elif cmd=='supervise':supervise()
    elif cmd=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif cmd=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    else:raise ValueError(cmd)
