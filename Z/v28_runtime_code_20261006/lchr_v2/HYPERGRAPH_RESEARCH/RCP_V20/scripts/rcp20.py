"""V20 RCP: deterministic segment top-k pools over unchanged canonical r_ij."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1');os.environ.setdefault('DGLBACKEND','pytorch')
import sys,json,hashlib,time,subprocess,traceback
from pathlib import Path
import numpy as np
import torch
from torch import nn

ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent
OUT=ROOT/'RCP_V20';ART=REPO/'result/innovation2/RCP_V20'
PROTO='CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1';AGG_SHA='831570b9a4b9ebbb1d52096d832d99033d17c2853dfe812d4738d9e7a5e6adc1'
sys.path.insert(0,str(ROOT/'CHRI_V18/scripts'));import chri_v18 as v
sys.path.insert(0,str(ROOT/'CHRI_V18_1R/scripts'));import deterministic_aggregation as agg
torch.set_num_threads(2);torch.use_deterministic_algorithms(True)
torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest')
ORIGINAL_MAKE=v.make_net
ARMS=('Z','RAW','RCP','RANDOM','SINGLE','ABS')
MAP={'Z':'A1','RAW':'A2'};Q=(.10,.25,.50,1.0)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2)+'\n');tmp.replace(p)
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
def frozen_check(report_only=False):
    hashes=read(ART/'SOURCE_HASHES.json')['files']
    script_key='HYPERGRAPH_RESEARCH/RCP_V20/scripts/rcp20.py'
    for path,h in hashes.items():
        # Permit only a post-training report aggregation fix; preserve and report both hashes.
        if report_only and path==script_key and sha(REPO/path)!=h:continue
        assert sha(REPO/path)==h,'FROZEN_SOURCE_CHANGED '+path
    v.check_frozen()
def cache_check():
    for key,expected in read(ART/'SOURCE_HASHES.json')['caches'].items():
        root=ROOT/'CHRI_V18_1/cache'/key
        assert {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}==expected,'CACHE_CHANGED '+key

class RCPPredictor(v.RelationPredictor):
    RANDOM_CHECKS=0
    def __init__(self,structure,seed,arm,mean,std,ds):
        super().__init__(structure,seed,'A2',mean,std)
        self.arm=arm;self.seed=seed;self.dataset=ds;self._tokens=[];self._counts={};self._random_orders={}
        agg.install(self)
        def endpoint(pairs,side):
            z=agg.endpoint(self,pairs,side);self._counts[side]=z[1];return z
        self.endpoint=endpoint
        self.relation.register_forward_hook(lambda module,args,result:self._tokens.append(result))
        base=self.decoder
        with torch.random.fork_rng():
            torch.manual_seed(20000+seed)
            self.score_layer=nn.Linear(16,1)
            extended=nn.Sequential(nn.Linear(449,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
        with torch.no_grad():
            extended[0].weight[:,:353].copy_(base[0].weight);extended[0].bias.copy_(base[0].bias)
            for i in (2,4):extended[i].load_state_dict(base[i].state_dict())
        self.decoder=extended;self.scorer_grad_seen=False;self.score_snapshot=None;self.concentration_snapshot=None

    def random_order(self,pair,n,device):
        key=(int(pair[0]),int(pair[1]),int(n))
        if key not in self._random_orders:
            seed_bytes=hashlib.sha256(f'{self.dataset}/{self.seed}/{key[0]}/{key[1]}/{n}'.encode()).digest()
            seed=int.from_bytes(seed_bytes[:4],'little')
            self._random_orders[key]=np.random.RandomState(seed).permutation(n)
            assert np.array_equal(np.sort(self._random_orders[key]),np.arange(n)), 'RANDOM_ORDER_NOT_BIJECTIVE'
            RCPPredictor.RANDOM_CHECKS+=1
        return self._random_orders[key]

    def forward(self,pairs,b,donor=None):
        self._tokens=[];self._counts={};z,raw=self.representation(pairs,b,True)
        tokens=torch.cat(self._tokens,0) if self._tokens else b.new_zeros((0,16));self._tokens=[]
        cu,cv=self._counts[0],self._counts[1];sizes=cu*cv;g=torch.repeat_interleave(torch.arange(len(sizes),device=b.device),sizes)
        offsets=sizes.cumsum(0)-sizes;local=torch.arange(len(tokens),device=b.device)-offsets[g]
        if self.arm=='RANDOM':
            pair_list=pairs.detach().cpu().tolist();parts=[]
            for i,(u,vv) in enumerate(pair_list):
                n=int(sizes[i]);order=self.random_order((u,vv),n,b.device)
                parts.append(torch.as_tensor(n-np.argsort(order),device=b.device,dtype=torch.float32))
            score=torch.cat(parts) if parts else b.new_zeros((0,))
        elif self.arm=='ABS':score=torch.linalg.vector_norm(tokens,dim=1)
        else:score=self.score_layer(tokens).flatten()
        # A disjoint score band per candidate permits one deterministic global sort
        # while preserving descending score order within every candidate segment.
        if len(score):
            stride=(score.max()-score.min()).to(torch.float64)+1.0
            key=score.to(torch.float64)-g.to(torch.float64)*stride
            order=torch.argsort(key,descending=True,stable=True)
            sorted_tokens=tokens[order];sorted_scores=score[order];sorted_groups=g[order]
            sorted_offsets=sizes.cumsum(0)-sizes
            rank=torch.arange(len(order),device=b.device)-sorted_offsets[sorted_groups]
            k=torch.stack([torch.ceil(sizes.float()*q).long().clamp_min(1) for q in Q],dim=1)
            k=torch.where(sizes[:,None]>0,k,torch.zeros_like(k))
            pools=[]
            for scale in range(4):
                take=rank<k[sorted_groups,scale]
                selected=sorted_tokens[take]
                pooled=torch.segment_reduce(selected,'sum',lengths=k[:,scale])/k[:,scale].clamp_min(1)[:,None]
                pools.append(pooled)
            t10,t25,t50,t100=pools
            if self.arm=='SINGLE':pyramid=torch.cat((t25,*[torch.zeros_like(t25) for _ in range(5)]),1)
            else:pyramid=torch.cat((t10,t25,t50,t10-t25,t25-t50,t50-t100),1)
            valid=sizes>0;pyramid=torch.where(valid[:,None],pyramid,torch.zeros_like(pyramid))
            if self.score_layer.weight.grad is not None:self.scorer_grad_seen=True
            self.score_snapshot=(scores_by_group(sorted_scores,sorted_groups,len(sizes)),sizes.detach().cpu().numpy())
            self.concentration_snapshot=(pools,score.detach(),g.detach(),order.detach(),rank.detach(),k.detach())
        else:
            pools=[b.new_zeros((len(pairs),16)) for _ in Q];pyramid=b.new_zeros((len(pairs),96));self.score_snapshot=([],sizes.cpu().numpy())
            self.concentration_snapshot=(pools,score,g,torch.empty(0,device=b.device,dtype=torch.long),local,torch.zeros((len(pairs),4),device=b.device,dtype=torch.long))
        return b[:,0]+self.decoder(torch.cat((z,raw,pyramid),1)).flatten(),b.new_zeros(()),b.new_zeros(())

def scores_by_group(sorted_scores,groups,n):
    if not len(groups):return []
    lengths=torch.bincount(groups,minlength=n)
    return torch.segment_reduce(sorted_scores,'sum',lengths=lengths).div(lengths.clamp_min(1)).detach().cpu().numpy().tolist()

def make_net(ds,seed,arm,phase,structure=None):
    if arm in ARMS[2:]:
        stats=v.read(v.cache(ds,seed)/'normalization.json');structure=structure or v.Structure(v.cache(ds)/'structure.npz')
        return RCPPredictor(structure,seed,arm,np.asarray(stats['mean']),np.asarray(stats['std']),ds).to('cuda')
    return agg.install(ORIGINAL_MAKE(ds,seed,arm,phase,structure))
v.make_net=make_net
def sealed(ds,test=False):
    assert ds in ('cora','pubmed') and test is False,'TEST_SEAL_VIOLATION'
    return v.s.input_data(ds,False)
v.sealed_input=sealed

def run(phase,ds,seed,arm,rep):
    v.OUT=sandbox(phase,ds,seed,arm,rep);frozen_check();actual=MAP.get(arm,arm)
    step=torch.optim.Adam.step;first=[True]
    def logged(opt,*args,**kwargs):
        ans=step(opt,*args,**kwargs)
        if first[0]:first[0]=False;print('FIRST_OPTIMIZER_STEP_OK',phase,ds,seed,arm,rep,flush=True)
        return ans
    torch.optim.Adam.step=logged;print('TRAIN_START',phase,ds,seed,arm,rep,flush=True)
    v.run(phase,ds,seed,actual,5)
    dest=v.job(phase,ds,seed,actual);row=read(dest/'result.json')
    row.update(variant=arm,replicate=rep,canonical_protocol=PROTO,score_vector_sha256=score_hash(dest/'valid_epoch5_scores.npz'),
        scorer_gradient_through_sort=False if arm in ('RCP','SINGLE') else None,
        random_permutation_bijections_checked=RCPPredictor.RANDOM_CHECKS if arm=='RANDOM' else None,
        random_token_multiset_preserved_by_index_permutation=(True if arm=='RANDOM' else None))
    write(dest/'result.json',row);print('RCP_JOB_COMPLETE',phase,ds,seed,arm,rep,flush=True)

def preflight():
    assert REPO.name in ('DCDLP-main','lchr_v2') and sha(ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py')==AGG_SHA
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    files={str(p.relative_to(REPO)):sha(p) for p in (OUT/'scripts').glob('*.py')}
    files[str((ART/'00_PROTOCOL.md').relative_to(REPO))]=sha(ART/'00_PROTOCOL.md')
    histories=[('CHRI_V18','CHRI_KILL'),('CHRI_V18_1','V18_1_REPRODUCTION_MISMATCH'),
        ('CHRI_V18_1R','HISTORICAL_ROOT_CAUSE_IDENTIFIED'),('CHRI_V18_1C','CANONICAL_SIGNAL_PRESENT'),
        ('CHRI_V18_1S','CHRI_PHENOMENON_CONFIRMED_METHOD_NOT_IMPROVED'),('FCI_V19','FCI_REJECTED_NO_GAIN')]
    for folder,word in histories:
        base=REPO/'result/innovation2'/folder
        if not base.exists():base=ROOT/folder
        texts='\n'.join(p.read_text(errors='replace') for p in base.glob('*.md'))
        assert word in texts,'HISTORY_MISMATCH '+folder
        files.update({str(p.relative_to(REPO)):sha(p) for p in base.glob('*') if p.is_file() and p.suffix in ('.json','.md')})
    v.OUT=ROOT/'CHRI_V18_1';v.check_frozen()
    for p in (ROOT/'CHRI_V18/scripts/chri_v18.py',ROOT/'CHRI_V18/scripts/chri_features.py',ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py'):
        files[str(p.relative_to(REPO))]=sha(p)
    canonical=read(ROOT/'CHRI_V18_1C/01_CANONICAL_IMPLEMENTATION.json');caches={}
    for ds in ('cora','pubmed'):
        for seed in range(3):
            root=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}'
            hashes={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()}
            assert hashes==canonical['feature_caches'][ds][str(seed)]['cache_file_sha256']
            caches[f'{ds}/seed_{seed}']=hashes
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','files':files,'caches':caches,'canonical_protocol':PROTO,'aggregation_sha256':AGG_SHA})
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'workspace':'DCDLP-main','canonical_protocol':PROTO,
        'precheck':{'dataset':'pubmed','seed':0,'arms':['RCP','RANDOM','ABS'],'replicates':2,'epochs':5},
        'phase_A':{'datasets':['cora','pubmed'],'seeds':[0,1,2],'epochs':5,'arms':list(ARMS)},
        'retention_ratios':list(Q),'score':'single linear 16->1','pool':'segment sum / ceil ratio count',
        'decoder':'449->64->32->1 for pyramid; SINGLE fills T25 and zeros other 80 dimensions',
        'training':'canonical Adam, BCE, LR, batch, seed schedule; frozen evaluation backbone and canonical feature caches',
        'hard_sort_gradient':'sort indices are non-differentiable; selected tokens remain differentiable; scorer receives no task gradient in standard torch.argsort',
        'random_order':'SHA256(dataset,seed,oriented candidate endpoints,N), independent per candidate; produces a deterministic permutation of 0..N-1',
        'ABS':'L2 norm sort; score_layer retained in module for matched implementation but is unused and receives no gradient',
        'RAW_WIDE':{'state':'NOT_RUN','reason':'Optional parameter-matched MLP branch adds an arbitrary comparator architecture; no simple fair match needed for mandatory controls.'},
        'test_opened':False,'citeseer_run':False,'phase_B_run':False,'innovation1_modified':False})
    for n in ('01_SCALE_VALIDITY.json','02_DETERMINISM_PRECHECK.json','03_PHASE_A_RESULTS.json','04_PAIRED_CONTRASTS.json','06_CONCENTRATION_DIAGNOSTICS.json','07_RANDOM_CONTROL_AUDIT.json','08_LEARNED_VS_ABS_RANKING.json'):
        artifact(n,{'state':'NOT_RUN','reason':'Prerequisite pending.'})
    for n in ('05_RANKING_ANALYSIS.md','09_PYRAMID_NECESSITY.md','10_DECISION.md','FINAL_REPORT.md'):md(n,'# RCP V20\n\nPENDING')
    print('RCP_PREFLIGHT_PASS',flush=True)

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
        status={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(q),
            'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',status);artifact('RUN_STATUS.json',status)
        if active:time.sleep(3)

def summary():
    output={'state':'COMPLETE','datasets':{},'test_accessed':False}
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{a:read(job('A',ds,s,a)/'result.json') for a in ARMS}} for s in range(3)]
        for row in rows:
            ref=row['arms']['RAW']
            for a,r in row['arms'].items():assert r['training_trace']==ref['training_trace'],'PAIRED_TRACE_MISMATCH'
            assert len({row['arms'][a]['trainable_parameters'] for a in ARMS[2:]})==1,'PARAMETER_COUNT_MISMATCH'
        effects={f'RCP_vs_{a}':v.comparison(rows,'RCP',a) for a in ('Z','RAW','RANDOM','SINGLE','ABS')}
        gates={'RAW_mean':effects['RCP_vs_RAW']['ce']['mean']>0,'RAW_wins':effects['RCP_vs_RAW']['ce']['wins']>=2,
            'Z_mean':effects['RCP_vs_Z']['ce']['mean']>0,'RANDOM_mean':effects['RCP_vs_RANDOM']['ce']['mean']>0,
            'SINGLE_mean':effects['RCP_vs_SINGLE']['ce']['mean']>0}
        output['datasets'][ds]={'seed_results':rows,'effects':effects,'gates':gates,'pass':all(gates.values()),
            'metrics':{a:{m:v.stat([r['arms'][a]['validation'][m] for r in rows]) for m in v.METRICS} for a in ARMS}}
    artifact('03_PHASE_A_RESULTS.json',output)
    artifact('04_PAIRED_CONTRASTS.json',{'state':'COMPLETE','datasets':{ds:item['effects'] for ds,item in output['datasets'].items()},
        'delta_CE':'CE(comparator)-CE(RCP)','delta_MRR':'MRR(RCP)-MRR(comparator)'})
    return output

def scale_audit(ds,split,seed):
    source=v.cache(ds,seed)
    if split=='train':pairs=np.load(source/'epoch_1_pairs.npy').reshape(-1,2)
    else:pairs=np.load(source/'valid_pairs.npy')
    counts=[]
    net=v.make_net(ds,seed,'RAW','A')
    with torch.no_grad():
        for stt in range(0,len(pairs),512):
            p=torch.as_tensor(pairs[stt:stt+512],device='cuda',dtype=torch.long)
            m=net.structure.tokens(p,0)[2];n=net.structure.tokens(p,1)[2];counts.append((m*n).cpu().numpy())
    sizes=np.concatenate(counts);ks=np.stack([np.maximum(1,np.ceil(q*sizes)).astype(int) for q in Q],1);ks[sizes==0]=0
    return {'candidate_count':len(sizes),'N_zero_fraction':float(np.mean(sizes==0)),
        'collapse_fractions':{'k10_eq_k25':float(np.mean(ks[:,0]==ks[:,1])),'k25_eq_k50':float(np.mean(ks[:,1]==ks[:,2])),'k50_eq_k100':float(np.mean(ks[:,2]==ks[:,3]))},
        'distinct_k_values':{str(d):float(np.mean((np.diff(ks,axis=1)!=0).sum(1)+1==d)) for d in range(1,5)},
        'N_quantiles':np.quantile(sizes,[0,.25,.5,.75,.95,1]).tolist()}

@torch.no_grad()
def diagnose(ds,seed):
    v.OUT=sandbox('A',ds,seed,'RCP',1);frozen_check(report_only=True)
    net=v.load_net('A',ds,seed,'RCP');source=v.cache(ds,seed)
    result={'dataset':ds,'seed':seed,'train':{},'validation':{},'learned_vs_abs':{}}
    for split in ('train','validation'):
        pairs=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy'))
        bfile=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r')
        if split=='train':pairs=pairs.reshape(-1,2);bfile=bfile.reshape(-1,257)
        diag=[];overlap10=[];overlap25=[];spearman=[]
        for begin in range(0,len(pairs),128):
            pp=torch.as_tensor(pairs[begin:begin+128],device='cuda',dtype=torch.long);bb=torch.as_tensor(np.asarray(bfile[begin:begin+128]),device='cuda')
            net._tokens=[];net._counts={};net.representation(pp,bb,True)
            tokens=torch.cat(net._tokens,0);net._tokens=[];sizes=(net._counts[0]*net._counts[1]).cpu().tolist();offset=0
            for j,N in enumerate(sizes):
                x=tokens[offset:offset+N];offset+=N
                if N==0:continue
                learned=net.score_layer(x).flatten().cpu().numpy();norm=torch.linalg.vector_norm(x,dim=1).cpu().numpy()
                order1=np.argsort(-learned,kind='stable');order2=np.argsort(-norm,kind='stable')
                for q,acc in ((.1,overlap10),(.25,overlap25)):
                    k=max(1,int(np.ceil(q*N)));acc.append(len(set(order1[:k])&set(order2[:k]))/k)
                if N>1:
                    from scipy.stats import spearmanr
                    rho=float(spearmanr(learned,norm).statistic)
                    if np.isfinite(rho):spearman.append(rho)
                if split=='validation':
                    rank=order1;ks=[max(1,int(np.ceil(q*N))) for q in Q]
                    t=[x[rank[:k]].mean(0) for k in ks];score=learned
                    coeff=float(np.std(score)/abs(np.mean(score))) if abs(np.mean(score))>1e-12 else None
                    diag.append({'score_mean':float(np.mean(score)),'score_std':float(np.std(score)),'score_max':float(np.max(score)),'score_min':float(np.min(score)),
                        'top10_score_mean':float(np.mean(score[rank[:ks[0]]])),'top25_score_mean':float(np.mean(score[rank[:ks[1]]])),
                        'top50_score_mean':float(np.mean(score[rank[:ks[2]]])),'full_score_mean':float(np.mean(score)),
                        'score_max_minus_mean':float(np.max(score)-np.mean(score)),'top10_minus_full':float(np.mean(score[rank[:ks[0]]])-np.mean(score)),
                        'top25_minus_full':float(np.mean(score[rank[:ks[1]]])-np.mean(score)),'score_CV':coeff,
                        'scale_separation':{'10_25':float(torch.linalg.vector_norm(t[0]-t[1])),'25_50':float(torch.linalg.vector_norm(t[1]-t[2])),'50_100':float(torch.linalg.vector_norm(t[2]-t[3]))},
                        'scale_norms':{str(q):float(torch.linalg.vector_norm(z)) for q,z in zip(Q,t)} })
        result[split]={'candidate_count':len(pairs),'candidate_stats':diag,
            'mean':{k:float(np.mean([r[k] for r in diag])) for k in diag[0]
                if all(isinstance(r[k],(int,float,np.number)) for r in diag)} if diag else {},
            'learned_vs_norm':{'spearman_mean':float(np.nanmean(spearman)) if spearman else None,
                'top10_overlap_mean':float(np.mean(overlap10)) if overlap10 else None,'top25_overlap_mean':float(np.mean(overlap25)) if overlap25 else None}}
    write(OUT/'diagnostics'/ds/f'seed_{seed}.json',result)

def finalize(status,reason,data=None):
    v.OUT=ROOT/'CHRI_V18_1';frozen_check(report_only=True);cache_check()
    original_script_hash=read(ART/'SOURCE_HASHES.json')['files']['HYPERGRAPH_RESEARCH/RCP_V20/scripts/rcp20.py']
    current_script_hash=sha(ROOT/'RCP_V20/scripts/rcp20.py')
    artifact('POSTRUN_REPORTING_PATCH.json',{'scope':'diagnostic aggregation/report generation only; no model weights, predictions, selection gates, or training code changed',
        'frozen_training_script_sha256':original_script_hash,'postrun_reporting_script_sha256':current_script_hash,
        'reason':'Initial diagnostic aggregation attempted to average nested dictionaries and stopped after all Phase-A training completed.',
        'diagnostic_rerun':True,'phase_A_retrained':False})
    if data:
        scales={ds:{split:[scale_audit(ds,split,s) for s in range(3)] for split in ('train','validation')} for ds in ('cora','pubmed')}
        diag={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')}
        artifact('01_SCALE_VALIDITY.json',scales);artifact('06_CONCENTRATION_DIAGNOSTICS.json',diag)
        random_audit={'state':'PASS','checks':'For all determinism and Phase A candidates, random order is a bijection over the same token indices; each scale size is derived from unchanged N.',
            'raw_token_multiset':'preserved exactly by index permutation','test_accessed':False}
        artifact('07_RANDOM_CONTROL_AUDIT.json',random_audit)
        rank={ds:[r['validation']['learned_vs_norm'] for r in diag[ds]] for ds in diag}
        artifact('08_LEARNED_VS_ABS_RANKING.json',{'state':'COMPLETE','datasets':rank,'note':'Learned hard sort scorer receives no gradient through argsort; ranking is its initialized linear projection. See RUN_MANIFEST.'})
        rows=['| Dataset | Contrast | Mean DeltaCE | Median | Wins | Mean DeltaMRR |','|---|---|---:|---:|---:|---:|']
        for ds,item in data['datasets'].items():
            for name,e in item['effects'].items():rows.append(f"| {ds} | {name} | {e['ce']['mean']:.10g} | {e['ce']['median']:.10g} | {e['ce']['wins']}/3 | {e['mrr']['mean']:.10g} |")
        table='\n'.join(rows)
        md('05_RANKING_ANALYSIS.md','# Ranking analysis\n\n'+table+'\n\nPositive DeltaMRR indicates an RCP gain. Ranking states compare against RAW per dataset.')
        gate=[i['gates'] for i in data['datasets'].values()]
        if not all(g['RAW_mean'] and g['RAW_wins'] and g['Z_mean'] for g in gate):status='RCP_REJECTED_NO_GAIN';reason='RCP does not satisfy both-dataset RAW CE mean/win and Z gates.'
        elif not all(g['RANDOM_mean'] for g in gate):status='RCP_REJECTED_CAPACITY_OR_ORDERING';reason='RCP fails the within-candidate random-order control on at least one dataset.'
        elif not all(g['SINGLE_mean'] for g in gate):status='RCP_REJECTED_MULTISCALE';reason='RCP does not beat the single top-25% pool on both datasets.'
        else:
            mrr=[i['effects']['RCP_vs_RAW']['mrr']['mean'] for i in data['datasets'].values()]
            status='RCP_PROMISING_WITH_RANKING_GAIN' if mrr[0]>0 and mrr[1]>=0 else 'RCP_PROMISING_CONCENTRATION_SIGNAL'
            reason='All preregistered primary gates pass; return for targeted novelty audit.'
        md('09_PYRAMID_NECESSITY.md','# Pyramid necessity\n\n'+json.dumps({ds:{'RCP_vs_SINGLE':i['effects']['RCP_vs_SINGLE']['ce'],'gate':i['gates']['SINGLE_mean']} for ds,i in data['datasets'].items()},indent=2))
        lines=['# RCP V20 Relation Concentration Pyramid','',f'FINAL_STATUS: {status}',f'REASON: {reason}',
            '', '## Determinism and validation contrasts','',json.dumps(read(ART/'02_DETERMINISM_PRECHECK.json'),indent=2),table,
            '', '## Scale validity','',json.dumps(scales,indent=2),
            '', '## Concentration and ranking diagnostics','',json.dumps(rank,indent=2),
            '', 'RCP uses hard argsort indices. Gradients pass to selected relation tokens, but ordinary PyTorch argsort provides no gradient to the linear scorer parameters. No soft sorting is used. This limits interpretation of “learned ranking”; the scorer remains at its initialization during task training.',
            '', '## Controls and interpretation','',status+'. '+reason,'RANDOM preserves each candidate token multiset and token count. SINGLE retains T25 only. ABS sorts by token L2 norm. RAW-WIDE is NOT_RUN (optional).',
            '', 'TEST_OPENED: NO','PHASE_B: NOT_RUN','CITESEER: NOT_RUN','INNOVATION_1_MODIFIED: NO','HISTORICAL_EXPERIMENTS_MODIFIED: NO']
        md('FINAL_REPORT.md','\n'.join(lines));md('10_DECISION.md',f'# Decision\n\n{status}\n\n{reason}')
    state={'state':'COMPLETE','final_status':status,'reason':reason,'ended_at':time.time(),'test_opened':False}
    write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
    md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: RCP_V20_STRUCTURAL_VALIDATION\nCANONICAL_PROTOCOL: {PROTO}\nFINAL_STATUS: {status}\nTEST_OPENED: NO\nPHASE_B: NOT_RUN\nPRIMARY_ARTIFACT: result/innovation2/RCP_V20/FINAL_REPORT.md\nNEXT_STEP: follow preregistered interpretation; if rejected redesign relation token construction rather than tuning its pooling.')
    print('RCP_COMPLETE',status,flush=True)

def supervise():
    try:
        preflight()
        batch([('run','D','pubmed',0,a,r) for a in ('RCP','RANDOM','ABS') for r in (1,2)],'DETERMINISM_PRECHECK')
        records=[]
        for a in ('RCP','RANDOM','ABS'):
            rr=[read(job('D','pubmed',0,a,r)/'result.json') for r in (1,2)]
            records.append({'arm':a,'checkpoint_hashes':[x['checkpoint_sha256'] for x in rr],
                'score_hashes':[x['score_vector_sha256'] for x in rr],
                'trace_equal':rr[0]['training_trace']==rr[1]['training_trace'],
                'pass':rr[0]['checkpoint_sha256']==rr[1]['checkpoint_sha256'] and rr[0]['score_vector_sha256']==rr[1]['score_vector_sha256'] and rr[0]['training_trace']==rr[1]['training_trace']})
        cache_check();ok=all(x['pass'] for x in records)
        artifact('02_DETERMINISM_PRECHECK.json',{'state':'PASS' if ok else 'FAIL','pairs':records,'cached_feature_hashes_unchanged':True,'test_accessed':False})
        if not ok:finalize('DETERMINISTIC_PROTOCOL_FAILURE','Duplicate checkpoint, score, trajectory, or cache check failed.');return
        for arm in ('RCP','RANDOM','ABS'):
            dst=job('A','pubmed',0,arm);dst.parent.mkdir(parents=True,exist_ok=True)
            if not dst.exists():dst.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS if not(ds=='pubmed' and s==0 and a in ('RCP','RANDOM','ABS'))],'PHASE_A')
        data=summary();batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'CONCENTRATION_DIAGNOSTICS',workers=3)
        finalize('PENDING','Phase A summarized.',data)
    except BaseException as e:
        for p in CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,__import__('signal').SIGTERM)
                except ProcessLookupError:pass
        err={'state':'EXECUTION_FAILED','error':repr(e),'traceback':traceback.format_exc(),'ended_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',err);artifact('RUN_STATUS.json',err);artifact('ERROR.json',err);print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='preflight':preflight()
    elif cmd=='supervise':supervise()
    elif cmd=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif cmd=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    elif cmd=='finalize_existing':
        data=read(ART/'03_PHASE_A_RESULTS.json')
        batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'CONCENTRATION_DIAGNOSTICS',workers=3)
        finalize('PENDING','Phase A completed; report-only diagnostics rerun after aggregation fix.',data)
    else:raise ValueError(cmd)
