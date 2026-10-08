"""FCI structural validation: canonical RAW tokens plus leave-one-out contrasts."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1')
os.environ.setdefault('DGLBACKEND','pytorch')
import sys,json,hashlib,time,subprocess,traceback,shutil
from pathlib import Path
import numpy as np
import torch
from torch import nn

ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent
OUT=ROOT/'FCI_V19';ART=REPO/'result/innovation2/FCI_V19'
PROTO='CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1'
AGG_SHA='831570b9a4b9ebbb1d52096d832d99033d17c2853dfe812d4738d9e7a5e6adc1'
sys.path.insert(0,str(ROOT/'CHRI_V18/scripts'));import chri_v18 as v
sys.path.insert(0,str(ROOT/'CHRI_V18_1R/scripts'));import deterministic_aggregation as agg
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
torch.set_float32_matmul_precision('highest')
ORIGINAL_MAKE=v.make_net
ARMS=('Z','RAW','FCI','DIRECT','SHUFFLE','FCI_U','FCI_V')
MAP={'Z':'A1','RAW':'A2'}

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');tmp.replace(p)
def artifact(n,obj):write(ART/n,obj)
def md(n,s):ART.mkdir(parents=True,exist_ok=True);(ART/n).write_text(s+'\n')
def score_hash(p):
    h=hashlib.sha256()
    with np.load(p) as z:
        for key in ('positive','negative'):
            x=np.ascontiguousarray(z[key]);h.update(key.encode());h.update(str(x.shape).encode());h.update(str(x.dtype).encode());h.update(x.tobytes())
    return h.hexdigest()

def factors(x):
    """x[m,n,d]; every grouped reduction uses the canonical segment path."""
    m,n,d=x.shape
    rows=torch.segment_reduce(x.reshape(m*n,d),'sum',lengths=torch.full((m,),n,device=x.device,dtype=torch.long))[:,None,:]
    cols=torch.segment_reduce(x.transpose(0,1).contiguous().reshape(m*n,d),'sum',lengths=torch.full((n,),m,device=x.device,dtype=torch.long))[None,:,:]
    total=torch.segment_reduce(x.reshape(m*n,d),'sum',lengths=torch.tensor([m*n],device=x.device))
    u=(rows-x)/(n-1);vv=(cols-x)/(m-1)
    bg=(total-rows-cols+x)/((m-1)*(n-1))
    return u,vv,bg,x-u-vv+bg

def packed_factors(tokens,cu,cv):
    sizes=cu*cv;device=tokens.device
    groups=torch.repeat_interleave(torch.arange(len(cu),device=device),sizes)
    offsets=sizes.cumsum(0)-sizes
    local=torch.arange(len(tokens),device=device)-offsets[groups]
    row_offsets=cu.cumsum(0)-cu;col_offsets=cv.cumsum(0)-cv
    rows=row_offsets[groups]+torch.div(local,cv[groups],rounding_mode='floor')
    cols=col_offsets[groups]+local%cv[groups]
    row_sums=torch.segment_reduce(tokens,'sum',lengths=torch.repeat_interleave(cv,cu))
    # Transpose each ragged m*n field without atomics, then contiguous column sums.
    transpose_index=offsets[groups]+(local%cu[groups])*cv[groups]+torch.div(local,cu[groups],rounding_mode='floor')
    col_sums=torch.segment_reduce(tokens[transpose_index],'sum',lengths=torch.repeat_interleave(cu,cv))
    totals=torch.segment_reduce(tokens,'sum',lengths=sizes)
    rs=row_sums[rows];cs=col_sums[cols]
    u=(rs-tokens)/(cv[groups]-1).clamp_min(1)[:,None]
    vv=(cs-tokens)/(cu[groups]-1).clamp_min(1)[:,None]
    bg=(totals[groups]-rs-cs+tokens)/((cu[groups]-1)*(cv[groups]-1)).clamp_min(1)[:,None]
    return u,vv,bg,tokens-u-vv+bg

def algebra():
    checks=[]
    for device in ('cpu','cuda'):
        generator=torch.Generator(device='cpu').manual_seed(19000)
        a=torch.randn((4,1,16),generator=generator).to(device)
        b=torch.randn((1,5,16),generator=generator).to(device)
        x=a+b+0.37
        c=factors(x)[3];err=float(c.abs().max())
        s=torch.zeros_like(x);s[1,2]=torch.linspace(.1,1.6,16,device=device)
        observed=factors(x+s)[3]
        # Known expected centering of a single-cell injection.
        expected=s-s.sum(1,keepdim=True)/5-s.sum(0,keepdim=True)/4+s.sum((0,1),keepdim=True)/20
        expected=expected*(4*5/((4-1)*(5-1)))
        injection_error=float((observed-expected).abs().max())
        checks.append({'device':device,'additive_max_abs':err,'injection_centering_max_abs':injection_error,
            'injected_cell_recovered_max_abs':float((observed[1,2]-s[1,2]).abs().max()),
            'tolerance':1e-5,'pass':err<1e-5 and injection_error<1e-5})
        packed=packed_factors((x+s).reshape(-1,16),torch.tensor([4],device=device),torch.tensor([5],device=device))[3]
        checks[-1]['packed_vs_reference_max_abs']=float((packed.reshape(4,5,16)-observed).abs().max())
        checks[-1]['pass']=checks[-1]['pass'] and checks[-1]['packed_vs_reference_max_abs']<1e-5
    artifact('01_ALGEBRAIC_SANITY.json',{'state':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks':checks})
    return all(c['pass'] for c in checks)

class FactorPredictor(v.RelationPredictor):
    def __init__(self,structure,seed,arm,mean,std):
        super().__init__(structure,seed,'A2',mean,std)
        self.arm=arm;self.seed=seed;self._tokens=[];self._counts={};self._permutations={}
        # Capture exact canonical phi outputs: RAW and contrast share the same tensors.
        agg.install(self)
        def endpoint(pairs,side):
            answer=agg.endpoint(self,pairs,side);self._counts[side]=answer[1];return answer
        self.endpoint=endpoint
        self.relation.register_forward_hook(lambda module,args,result:self._tokens.append(result))
        canonical=self.decoder
        with torch.random.fork_rng():
            torch.manual_seed(19000+seed)
            self.psi=nn.Sequential(nn.Linear(16,16),nn.ReLU(),nn.Linear(16,16),nn.ReLU())
            self.decoder=nn.Sequential(nn.Linear(402,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
        with torch.no_grad():
            self.decoder[0].weight[:,:353].copy_(canonical[0].weight)
            self.decoder[0].bias.copy_(canonical[0].bias)
            for index in (2,4):self.decoder[index].load_state_dict(canonical[index].state_dict())
        self.capture=False;self.last_fields=None

    def permutation(self,pair,m,n,device):
        key=(int(pair[0]),int(pair[1]),m,n)
        if key not in self._permutations:
            token=f'{self.seed}/{key[0]}/{key[1]}/{m}/{n}'.encode()
            seed=int.from_bytes(hashlib.sha256(token).digest()[:4],'little')
            self._permutations[key]=np.random.RandomState(seed).permutation(m*n)
        return torch.as_tensor(self._permutations[key],device=device)

    def forward(self,pairs,b,donor=None):
        self._tokens=[];self._counts={}
        z,raw=self.representation(pairs,b,True)
        tokens=torch.cat(self._tokens,0) if self._tokens else b.new_zeros((0,16))
        # Release hook references after this forward so diagnostic buffers cannot retain graphs.
        self._tokens=[]
        dimensions=list(zip(self._counts[0].cpu().tolist(),self._counts[1].cpu().tolist()))
        cu,cv=self._counts[0],self._counts[1];sizes=cu*cv
        valid=(cu>=2)&(cv>=2);fields=[]
        if len(tokens):
            u,vv,bg,c=packed_factors(tokens,cu,cv)
            permutation=None;shuffled=None
            if self.arm=='SHUFFLE' or self.capture:
                chunks=[];offset=0
                for pair,(m,n) in zip(pairs.cpu().tolist(),dimensions):
                    chunks.append(self.permutation(pair,m,n,b.device)+offset);offset+=m*n
                permutation=torch.cat(chunks)
                xp=tokens[permutation]
                shuffled=packed_factors(xp,cu,cv)[3]
            value=tokens if self.arm=='DIRECT' else tokens-u if self.arm=='FCI_U' else tokens-vv if self.arm=='FCI_V' else shuffled if self.arm=='SHUFFLE' else c
            q=self.psi(value)
            mean=torch.segment_reduce(q,'sum',lengths=sizes)/sizes.clamp_min(1)[:,None]
            maximum=torch.segment_reduce(q,'max',lengths=sizes)
            rms=torch.sqrt(torch.segment_reduce(q*q,'sum',lengths=sizes)/sizes.clamp_min(1)[:,None]+1e-8)
            contrast=torch.cat((mean,maximum,rms,valid.to(b.dtype)[:,None]),1)
            contrast=torch.where(valid[:,None],contrast,torch.zeros_like(contrast))
            if self.capture:
                aligned=shuffled[torch.argsort(permutation)]
                assert torch.equal(tokens,xp[torch.argsort(permutation)]),'SHUFFLE_MULTISET_CHANGED'
                arrays={k:a.detach().cpu().numpy() for k,a in [('r',tokens),('u',u),('v',vv),('bg',bg),('c',c),('shuffle',aligned)]}
                offset=0
                for m,n in dimensions:
                    item={'m':m,'n':n,'valid':m>=2 and n>=2}
                    if item['valid']:item.update({k:a[offset:offset+m*n] for k,a in arrays.items()})
                    fields.append(item);offset+=m*n
        else:
            contrast=b.new_zeros((len(pairs),49))
            if self.capture:fields=[{'m':m,'n':n,'valid':False} for m,n in dimensions]
        if self.capture:self.last_fields=fields
        score=b[:,0]+self.decoder(torch.cat((z,raw,contrast),1)).flatten()
        return score,b.new_zeros(()),b.new_zeros(())

def make_net(ds,seed,arm,phase,structure=None):
    if arm in ARMS[2:]:
        stats=v.read(v.cache(ds,seed)/'normalization.json')
        structure=structure or v.Structure(v.cache(ds)/'structure.npz')
        return FactorPredictor(structure,seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda')
    return agg.install(ORIGINAL_MAKE(ds,seed,arm,phase,structure))
v.make_net=make_net
def sealed(ds,test=False):
    assert ds in ('cora','pubmed') and test is False,'TEST_SEAL_VIOLATION'
    return v.s.input_data(ds,False)
v.sealed_input=sealed

def sandbox(phase,ds,seed,arm,rep):
    out=OUT/'executions'/phase/ds/f'seed_{seed}'/arm/f'rep_{rep}';out.mkdir(parents=True,exist_ok=True)
    for p,target,d in [(out.parent/'CHRI_V18',ROOT/'CHRI_V18',True),
            (out/'scripts',ROOT/'CHRI_V18_1/scripts',True),(out/'SOURCE_HASHES.json',ROOT/'CHRI_V18_1/SOURCE_HASHES.json',False),
            (out/'cache',ROOT/'CHRI_V18_1/cache',True)]:
        if not p.exists():p.symlink_to(target,target_is_directory=d)
    return out
def job(phase,ds,seed,arm,rep=1):
    return OUT/'executions'/phase/ds/f'seed_{seed}'/arm/f'rep_{rep}/runs'/phase/ds/f'seed_{seed}'/MAP.get(arm,arm)
def check():
    for path,h in read(ART/'SOURCE_HASHES.json')['files'].items():assert sha(REPO/path)==h,'FROZEN_SOURCE_CHANGED '+path
    v.check_frozen()
def cache_check():
    for key,files in read(ART/'SOURCE_HASHES.json')['caches'].items():
        root=ROOT/'CHRI_V18_1/cache'/key
        assert {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}==files,'CACHE_CHANGED '+key

def run(phase,ds,seed,arm,rep):
    assert ds in ('cora','pubmed') and seed in range(3) and arm in ARMS
    v.OUT=sandbox(phase,ds,seed,arm,rep);check();actual=MAP.get(arm,arm)
    step=torch.optim.Adam.step;first=[True]
    def logged(optimizer,*args,**kwargs):
        answer=step(optimizer,*args,**kwargs)
        if first[0]:print('FIRST_OPTIMIZER_STEP_OK',phase,ds,seed,arm,rep,flush=True);first[0]=False
        return answer
    torch.optim.Adam.step=logged
    print('TRAIN_START',phase,ds,seed,arm,rep,flush=True)
    v.run(phase,ds,seed,actual,5)
    dest=v.job(phase,ds,seed,actual);row=read(dest/'result.json')
    row.update(variant=arm,canonical_protocol=PROTO,score_vector_sha256=score_hash(dest/'valid_epoch5_scores.npz'),replicate=rep)
    write(dest/'result.json',row)
    print('FCI_JOB_COMPLETE',phase,ds,seed,arm,rep,flush=True)

def stats(values):
    x=np.asarray(values,float)
    return {'count':len(x),'mean':float(x.mean()) if len(x) else None,
        'quantiles':np.quantile(x,[0,.25,.5,.75,.95,1]).tolist() if len(x) else []}
@torch.no_grad()
def collect(net,ds,seed,split,limit=None):
    source=v.cache(ds,seed)
    pp=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy'))
    bf=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r')
    if split=='train':pp=pp.reshape(-1,2);bf=bf.reshape(-1,257)
    net.eval();net.capture=True;allnorm={k:[] for k in ('r','u','v','bg','c','ratio','shuffle_mad','shuffle_cosine','shuffle_norm_ratio','candidate_mean','candidate_max','candidate_rms')}
    arrays={'r':[],'c':[]};count=0;smallu=smallv=valid=0;kept=0
    for begin in range(0,len(pp),256):
        p=torch.tensor(pp[begin:begin+256],device='cuda',dtype=torch.long)
        b=torch.tensor(np.asarray(bf[begin:begin+256]),device='cuda')
        net(p,b)
        for field in net.last_fields:
            count+=1;smallu+=field['m']<2;smallv+=field['n']<2
            if not field['valid']:continue
            valid+=1;r,c=field['r'],field['c'];rn=np.linalg.norm(r,axis=1);cn=np.linalg.norm(c,axis=1)
            for key in ('r','u','v','bg','c'):allnorm[key].extend(np.linalg.norm(field[key],axis=1).tolist())
            allnorm['ratio'].extend((cn/(rn+1e-8)).tolist())
            allnorm['candidate_mean'].append(float(cn.mean()));allnorm['candidate_max'].append(float(cn.max()));allnorm['candidate_rms'].append(float(np.sqrt(np.mean(cn**2))))
            sc=field['shuffle'];sn=np.linalg.norm(sc,axis=1)
            allnorm['shuffle_mad'].extend(np.mean(np.abs(c-sc),axis=1).tolist())
            allnorm['shuffle_cosine'].extend((np.sum(c*sc,axis=1)/(cn*sn+1e-12)).tolist())
            allnorm['shuffle_norm_ratio'].extend((sn/(cn+1e-8)).tolist())
            remaining=(50000 if split=='train' else 100000)-kept
            if remaining>0:
                n=min(len(c),remaining);arrays['r'].append(r[:n]);arrays['c'].append(c[:n]);kept+=n
        if limit is not None and kept>=limit:break
    net.capture=False;net.last_fields=None
    return {'population_candidates':count,'fraction_m_lt2':smallu/count,'fraction_n_lt2':smallv/count,
        'contrast_valid_fraction':valid/count,'distributions':{k:stats(x) for k,x in allnorm.items()},
        'probe_token_count':kept}, {k:np.concatenate(x) if x else np.zeros((0,16)) for k,x in arrays.items()}

def diagnose(ds,seed):
    v.OUT=sandbox('A',ds,seed,'FCI',1);check()
    net=v.load_net('A',ds,seed,'FCI')
    train,ta=collect(net,ds,seed,'train',50000)
    valid,va=collect(net,ds,seed,'valid')
    # Separately enumerate the complete training population for the edge-case fractions.
    counts=[]
    p=np.load(v.cache(ds,seed)/'epoch_1_pairs.npy').reshape(-1,2)
    with torch.no_grad():
        for begin in range(0,len(p),512):
            pairs=torch.tensor(p[begin:begin+512],device='cuda',dtype=torch.long)
            cu=net.structure.tokens(pairs,0)[2].cpu().numpy();cv=net.structure.tokens(pairs,1)[2].cpu().numpy()
            counts.append(np.column_stack((cu,cv)))
    dims=np.concatenate(counts);train_population={'population':'all epoch1 positive and negative train candidates',
        'count':len(dims),'fraction_m_lt2':float(np.mean(dims[:,0]<2)),
        'fraction_n_lt2':float(np.mean(dims[:,1]<2)),'contrast_valid_fraction':float(np.mean((dims>=2).all(1)))}
    probe={'state':'NOT_RUN','reason':'No valid tokens.'}
    if len(ta['r']) and len(va['r']):
        x=np.column_stack((ta['r'].astype(np.float64),np.ones(len(ta['r']))))
        target=ta['c'].astype(np.float64)
        coef=np.linalg.lstsq(x,target,rcond=None)[0]
        pred=np.column_stack((va['r'],np.ones(len(va['r']))))@coef;y=va['c'].astype(np.float64)
        mse=float(np.mean((pred-y)**2));variance=float(np.var(y,axis=0).mean())
        cosine=np.sum(pred*y,axis=1)/(np.linalg.norm(pred,axis=1)*np.linalg.norm(y,axis=1)+1e-12)
        probe={'state':'COMPLETE','R2':1-mse/variance if variance>1e-12 else None,'MSE':mse,'cosine_mean':float(cosine.mean()),
            'train_tokens':len(x),'validation_tokens':len(y),'fit':'train-only ordinary least squares Linear(r)->c with intercept',
            'sampling':'first 50000 valid train tokens and first 100000 valid validation tokens in fixed canonical candidate order',
            'feedback_to_training':False}
    write(OUT/'diagnostics'/ds/f'seed_{seed}.json',{'state':'COMPLETE','dataset':ds,'seed':seed,'train_population':train_population,
        'train_probe_population':train,'validation':valid,'probe':probe,'raw_multiset_unchanged_asserted':True,'test_accessed':False})

CHILDREN=[]
def batch(tasks,stage,workers=6):
    queue=list(tasks);active=[];done=0;logdir=OUT/'logs';logdir.mkdir(exist_ok=True)
    while active or queue:
        for item in list(active):
            p,args,log=item
            if p.poll() is not None:
                active.remove(item)
                if p.returncode:raise RuntimeError(f'JOB_FAILED {args}: {log}')
                done+=1
        while queue and len(active)<workers:
            args=queue.pop(0);log=logdir/('_'.join(map(str,args))+'.log')
            with log.open('a') as f:
                p=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*map(str,args)],
                    stdout=f,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,env=os.environ.copy(),start_new_session=True)
            active.append((p,args,log));CHILDREN.append(p)
        status={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(queue),
            'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',status);artifact('RUN_STATUS.json',status)
        if active:time.sleep(3)

def preflight():
    assert REPO.name in ('DCDLP-main','lchr_v2'),'WORKSPACE_GUARD'
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    assert sha(ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py')==AGG_SHA
    files={str(p.relative_to(REPO)):sha(p) for p in (OUT/'scripts').glob('*.py')}
    files[str((ART/'00_PROTOCOL.md').relative_to(REPO))]=sha(ART/'00_PROTOCOL.md')
    for folder,word in [('CHRI_V18','CHRI_KILL'),('CHRI_V18_1','V18_1_REPRODUCTION_MISMATCH'),
        ('CHRI_V18_1R','HISTORICAL_ROOT_CAUSE_IDENTIFIED'),('CHRI_V18_1C','CANONICAL_SIGNAL_PRESENT'),
        ('CHRI_V18_1S','CHRI_PHENOMENON_CONFIRMED_METHOD_NOT_IMPROVED')]:
        base=REPO/'result/innovation2'/folder
        if not base.exists():base=ROOT/folder
        texts='\n'.join(p.read_text(errors='replace') for p in base.glob('*.md'))
        assert word in texts,'HISTORY_MISMATCH '+folder
        files.update({str(p.relative_to(REPO)):sha(p) for p in base.glob('*') if p.is_file() and p.suffix in ('.json','.md')})
    v.OUT=ROOT/'CHRI_V18_1';v.check_frozen()
    for p in [ROOT/'CHRI_V18/scripts/chri_v18.py',ROOT/'CHRI_V18/scripts/chri_features.py',ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py']:
        files[str(p.relative_to(REPO))]=sha(p)
    canonical=read(ROOT/'CHRI_V18_1C/01_CANONICAL_IMPLEMENTATION.json');caches={}
    for ds in ('cora','pubmed'):
        for seed in range(3):
            root=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}'
            hashes={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}
            assert hashes==canonical['feature_caches'][ds][str(seed)]['cache_file_sha256']
            caches[f'{ds}/seed_{seed}']=hashes
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','files':files,'caches':caches,'canonical_protocol':PROTO,'aggregation_sha256':AGG_SHA})
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'workspace':'DCDLP-main','server_checkout':str(REPO),
        'canonical_protocol':PROTO,'precheck':{'dataset':'pubmed','seed':0,'arms':['FCI','DIRECT','SHUFFLE'],'replicates':2,'epochs':5},
        'phase_A':{'datasets':['cora','pubmed'],'seeds':[0,1,2],'arms':list(ARMS),'epochs':5},
        'psi':[16,16,16],'FCI_pool':'mean,max,rms,valid: 49 dimensions','decoder':[402,64,32,1],
        'decoder_initialization':'canonical RAW first353 columns/bias/later layers copied exactly; same seed19000 for added columns and psi across new arms; final layer zero',
        'canonical_token_capture':'relation forward hook captures exact phi outputs used by verified RAW segment pooling; endpoints and RAW branch unchanged',
        'shuffle':'SHA256 experiment seed plus oriented candidate IDs and field shape; deterministic full-cell permutation within candidate, not a row/column permutation; RAW tokens untouched',
        'small_sets':'all new arms use identical m>=2,n>=2 validity; branch output49 exactly zero otherwise, including DIRECT and one-sided controls',
        'A7_NULL':{'state':'NOT_RUN','reason':'Zero branch output removes effective capacity; mandatory parameter-matched DIRECT is used.'},
        'optimizer':'canonical Adam, weight_decay0','learning_rate':{ds:v.b.NCFG[ds]['prelr'] for ds in ('cora','pubmed')},
        'batch_size':{ds:v.b.NCFG[ds]['batch'] for ds in ('cora','pubmed')},'microbatch':256,'parallel_jobs':6,'threads_per_job':2,
        'ranking_neutral_tolerance':1e-8,'test_opened':False,'innovation1_modified':False,'historical_CHRI_modified':False,
        'raw_encoder_policy':'canonical architecture, initialization and supervised end-to-end training; no representation replacement'})
    for name in ['02_DATASET_CONTRAST_VALIDITY.json','03_DETERMINISM_PRECHECK.json','04_PHASE_A_RESULTS.json','05_PAIRED_CONTRASTS.json','09_FCI_DIAGNOSTICS.json']:
        artifact(name,{'state':'NOT_RUN','reason':'Prerequisite pending.'})
    for name in ['06_CAPACITY_CONTROL.md','07_FACTOR_SHUFFLE_CONTROL.md','08_RANKING_ANALYSIS.md','10_DECISION.md','FINAL_REPORT.md']:
        md(name,'# FCI V19\n\nPENDING: no efficacy conclusion yet.')
    print('FCI_PREFLIGHT_PASS',flush=True)

def summarize():
    payload={'state':'COMPLETE','datasets':{},'test_accessed':False};paired={}
    for ds in ('cora','pubmed'):
        rows=[{'seed':seed,'arms':{a:read(job('A',ds,seed,a)/'result.json') for a in ARMS}} for seed in range(3)]
        for row in rows:
            ref=row['arms']['RAW']
            for a,r in row['arms'].items():
                assert r['training_trace']==ref['training_trace'],'PAIR_TRACE_CHANGED'
                assert r['initialization']['encoder']==ref['initialization']['encoder'],'PAIR_ENCODER_INIT_CHANGED'
            assert len({row['arms'][a]['trainable_parameters'] for a in ARMS[2:]})==1,'CAPACITY_UNMATCHED'
        effects={f'FCI_vs_{a}':v.comparison(rows,'FCI',a) for a in ARMS if a!='FCI'}
        raw=effects['FCI_vs_RAW'];gates={'RAW_mean_CE':raw['ce']['mean']>0,'RAW_seed_wins':raw['ce']['wins']>=2,
            'DIRECT_mean_CE':effects['FCI_vs_DIRECT']['ce']['mean']>0,'SHUFFLE_mean_CE':effects['FCI_vs_SHUFFLE']['ce']['mean']>0,
            'Z_mean_CE':effects['FCI_vs_Z']['ce']['mean']>0}
        mrr=raw['mrr']['mean'];ranking='RANKING_NEUTRAL' if abs(mrr)<=1e-8 else 'RANKING_IMPROVED' if mrr>0 else 'RANKING_DEGRADED'
        payload['datasets'][ds]={'seed_results':rows,'effects':effects,'gates':gates,'pass':all(gates.values()),'ranking':ranking,
            'metrics':{a:{m:v.stat([r['arms'][a]['validation'][m] for r in rows]) for m in v.METRICS} for a in ARMS}}
        paired[ds]=effects
    artifact('04_PHASE_A_RESULTS.json',payload);artifact('05_PAIRED_CONTRASTS.json',{'state':'COMPLETE','datasets':paired,
        'DeltaCE':'CE(comparator)-CE(FCI)','DeltaMRR':'MRR(FCI)-MRR(comparator)'})
    return payload

def finalize(status,reason,data=None):
    v.OUT=ROOT/'CHRI_V18_1';check();cache_check()
    lines=['# FCI V19 structural validation','',f'FINAL_STATUS: {status}',f'REASON: {reason}',
        '', '## Algebraic sanity and exact deterministic duplicates','',
        json.dumps(read(ART/'01_ALGEBRAIC_SANITY.json'),indent=2),json.dumps(read(ART/'03_DETERMINISM_PRECHECK.json'),indent=2)]
    if data:
        diagnostics={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')}
        artifact('09_FCI_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':diagnostics,'causal_claim':False})
        artifact('02_DATASET_CONTRAST_VALIDITY.json',{'state':'COMPLETE','datasets':{ds:[{'seed':r['seed'],'train':r['train_population'],
            'validation':{k:r['validation'][k] for k in ('population_candidates','fraction_m_lt2','fraction_n_lt2','contrast_valid_fraction')}} for r in rr] for ds,rr in diagnostics.items()}})
        table=['| Dataset | FCI vs | Mean DeltaCE | Median DeltaCE | CE wins | Mean DeltaMRR |','|---|---|---:|---:|---:|---:|']
        for ds,item in data['datasets'].items():
            for name,e in item['effects'].items():table.append(f"| {ds} | {name} | {e['ce']['mean']:.10g} | {e['ce']['median']:.10g} | {e['ce']['wins']}/3 | {e['mrr']['mean']:.10g} |")
        text='\n'.join(table);lines+=['','## Paired validation effects','',text,'','## Candidate validity and mechanism diagnostics','',
            json.dumps(read(ART/'02_DATASET_CONTRAST_VALIDITY.json'),indent=2),
            '09_FCI_DIAGNOSTICS.json contains per-seed token/factor/contrast norm distributions, aligned true-vs-shuffle MAD/cosine/norm ratio, and train-only linear-probe validation R2/MSE/cosine. Diagnostics never change training or method selection.',
            '',json.dumps({ds:[r['probe'] for r in rr] for ds,rr in diagnostics.items()},indent=2),
            '', '## Capacity and factor identity','',
            'FCI, DIRECT, SHUFFLE and one-sided arms have equal trainable parameter counts and identical initialization streams. RAW pooling uses the exact original phi tensors. Shuffle preserves the token multiset and counts and is aligned back to original token identity for field diagnostics.',
            '', '## Ranking and decision','',json.dumps({ds:{'gates':i['gates'],'ranking':i['ranking']} for ds,i in data['datasets'].items()},indent=2)]
        md('06_CAPACITY_CONTROL.md','# DIRECT capacity control\n\n'+text+'\n\nAll new arms have exactly equal trainable parameter counts; same psi/pooling/extended decoder. See per-seed counts and gates in Phase A results.')
        md('07_FACTOR_SHUFFLE_CONTROL.md','# Within-candidate factor shuffle\n\n'+text+'\n\nPermutation preserves the raw multiset and RAW branch. Norm/cosine/MAD diagnostics are aligned by inverse permutation. See 09_FCI_DIAGNOSTICS.json. Factor identity attribution requires positive FCI-vs-SHUFFLE CE on both datasets.')
        md('08_RANKING_ANALYSIS.md','# Ranking analysis\n\n'+text+'\n\n'+json.dumps({ds:i['ranking'] for ds,i in data['datasets'].items()},indent=2))
    lines+=['',f'## Conclusion\n\n{status}. {reason}',
        '', 'TEST_OPENED: NO','INNOVATION_1_MODIFIED: NO','HISTORICAL_CHRI_MODIFIED: NO','CITESEER_RUN: NO',
        'No novelty or causal-interaction claim is made. The task ends at the preregistered five-epoch three-seed structural screen.']
    md('FINAL_REPORT.md','\n'.join(lines));md('10_DECISION.md',f'# Decision\n\n{status}\n\n{reason}')
    state={'state':'COMPLETE','final_status':status,'reason':reason,'ended_at':time.time(),'test_opened':False}
    write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
    md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: FCI_V19_STRUCTURAL_VALIDATION\nWORKSPACE: DCDLP-main\nCANONICAL_PROTOCOL: {PROTO}\nFINAL_STATUS: {status}\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_CHRI_MODIFIED: NO\nPRIMARY_ARTIFACT: result/innovation2/FCI_V19/FINAL_REPORT.md\nNEXT_EXPECTED_STEP: return evidence for targeted novelty audit if promising; otherwise return rejection diagnostics. STOP.')
    print('FCI_COMPLETE',status,flush=True)

def supervise():
    try:
        preflight()
        if not algebra():finalize('FCI_IMPLEMENTATION_ERROR','Additive/single-cell algebraic sanity failed.');return
        batch([('run','D','pubmed',0,a,r) for a in ('FCI','DIRECT','SHUFFLE') for r in (1,2)],'DETERMINISM_PRECHECK')
        records=[]
        for a in ('FCI','DIRECT','SHUFFLE'):
            rr=[read(job('D','pubmed',0,a,r)/'result.json') for r in (1,2)]
            records.append({'variant':a,'checkpoint_hashes':[r['checkpoint_sha256'] for r in rr],
                'score_hashes':[r['score_vector_sha256'] for r in rr],
                'training_trace_equal':rr[0]['training_trace']==rr[1]['training_trace'],
                'pass':rr[0]['checkpoint_sha256']==rr[1]['checkpoint_sha256'] and rr[0]['score_vector_sha256']==rr[1]['score_vector_sha256'] and rr[0]['training_trace']==rr[1]['training_trace']})
        cache_check();passed=all(r['pass'] for r in records)
        artifact('03_DETERMINISM_PRECHECK.json',{'state':'PASS' if passed else 'FAIL','pairs':records,'cached_feature_hashes_unchanged':True,'test_accessed':False})
        if not passed:finalize('DETERMINISTIC_PROTOCOL_FAILURE','Independent final checkpoint/score hashes differ.');return
        for a in ('FCI','DIRECT','SHUFFLE'):
            dest=job('A','pubmed',0,a);dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():dest.symlink_to(job('D','pubmed',0,a),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS
            if not(ds=='pubmed' and s==0 and a in ('FCI','DIRECT','SHUFFLE'))],'PHASE_A_STRUCTURAL_SCREEN')
        data=summarize()
        batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'MECHANISM_DIAGNOSTICS',workers=3)
        items=list(data['datasets'].values())
        if not all(i['gates']['RAW_mean_CE'] and i['gates']['RAW_seed_wins'] and i['gates']['Z_mean_CE'] for i in items):
            status='FCI_REJECTED_NO_GAIN';reason='FCI does not consistently beat RAW and Z on both datasets.'
        elif not all(i['gates']['DIRECT_mean_CE'] for i in items):
            status='FCI_REJECTED_CAPACITY_EXPLANATION';reason='FCI fails to beat mandatory DIRECT capacity control on both datasets.'
        elif not all(i['gates']['SHUFFLE_mean_CE'] for i in items):
            status='FCI_REJECTED_FACTOR_IDENTITY';reason='FCI fails the factor identity shuffle control on both datasets.'
        else:
            strong=data['datasets']['cora']['effects']['FCI_vs_RAW']['mrr']['mean']>0 and data['datasets']['pubmed']['effects']['FCI_vs_RAW']['mrr']['mean']>=0
            status='FCI_PROMISING_WITH_RANKING_GAIN' if strong else 'FCI_PROMISING_STRUCTURAL_SIGNAL'
            reason='All preregistered CE mean/win, DIRECT and factor-shuffle gates pass. Return for targeted novelty audit.'
        finalize(status,reason,data)
    except BaseException as err:
        for p in CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,__import__('signal').SIGTERM)
                except ProcessLookupError:pass
        failure={'state':'EXECUTION_FAILED','error':repr(err),'traceback':traceback.format_exc(),'ended_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',failure);artifact('RUN_STATUS.json',failure);artifact('ERROR.json',failure)
        print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    command=sys.argv[1]
    if command=='preflight':preflight()
    elif command=='supervise':supervise()
    elif command=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif command=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    else:raise ValueError(command)
