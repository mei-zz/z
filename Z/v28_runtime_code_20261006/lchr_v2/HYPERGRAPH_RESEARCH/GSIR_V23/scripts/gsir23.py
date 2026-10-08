"""Amended V23: preserve RAW, shared history, independent capacity, global swap."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1')
import sys,json,hashlib,time,subprocess,traceback,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent;OUT=ROOT/'GSIR_V23';ART=REPO/'result/innovation2/GSIR_V23'
sys.path.insert(0,str(ROOT/'MERI_V22/scripts'));import meri22 as m
e,v,np,torch,nn,agg=m.e,m.v,m.np,m.torch,m.nn,m.agg
e.OUT=OUT;e.ART=ART;e.MAP['SHARED']='DUP'
read,write,sha,artifact,md,sandbox,job=e.read,e.write,e.sha,e.artifact,e.md,e.sandbox,e.job
PROTO=e.PROTO;ARMS=('Z','RAW','SHARED','INDEP','WIDE','EVEN','GSIR','COORDSWAP')

def statehash(state):
    h=hashlib.sha256()
    for k in sorted(state):h.update(k.encode());h.update(state[k].detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()
def ordered(x,y):return torch.cat((x,y,x-y,x*y),1)
def channels(psi,x,y):
    a,b=psi(ordered(x,y)),psi(ordered(y,x));return .5*(a+b),.5*(a-b).abs()

class GSIRPredictor(v.RelationPredictor):
    def __init__(self,structure,seed,arm,mean,std,ds):
        super().__init__(structure,seed,'A2',mean,std);self.arm=arm;self.seed=seed;self.dataset=ds;self.capture=False;self._states={};self._rawtokens=[];self._collect=False;self._diag={};self._masks={}
        agg.install(self)
        def endpoint(pairs,side):
            out=agg.endpoint(self,pairs,side);self._states[side]=out;return out
        self.endpoint=endpoint
        def hook(module,args,result):
            if self._collect:self._rawtokens.append(result)
        self.relation.register_forward_hook(hook)
        indim,hidden,width=(48,32,16) if arm=='INDEP' else ((48,36,14) if arm=='WIDE' else ((64,26,16) if arm in ('EVEN','EVEN_COORD') else (64,29,8)))
        with torch.random.fork_rng():
            torch.manual_seed(23002+seed);self.extra=nn.Sequential(nn.Linear(indim,hidden),nn.ReLU(),nn.Linear(hidden,width),nn.ReLU())
        added=2*width if arm in ('INDEP','WIDE','EVEN','EVEN_COORD') else 4*width;base=self.decoder
        with torch.random.fork_rng():
            torch.manual_seed(21002+seed);ext=nn.Sequential(nn.Linear(353+added,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
        with torch.no_grad():
            ext[0].weight[:,:353].copy_(base[0].weight);ext[0].bias.copy_(base[0].bias)
            for i in (2,4):ext[i].load_state_dict(base[i].state_dict())
        self.decoder=ext
    def masks(self,pairs,lengths):
        parts=[]
        for (u,w),n in zip(pairs.sort(dim=1).values.cpu().tolist(),lengths.cpu().tolist()):
            key=(u,w)
            if key not in self._masks:
                seed=int.from_bytes(hashlib.sha256(f'{self.dataset}/{self.seed}/{u}/{w}'.encode()).digest()[:4],'little')
                mask=np.random.RandomState(seed).randint(0,2,size=(n,16)).astype(bool);mask[:,0]=False;mask[:,-1]=True;self._masks[key]=mask
            assert len(self._masks[key])==n,'MASK_TOKEN_COUNT_CHANGED';parts.append(self._masks[key])
        return torch.as_tensor(np.concatenate(parts),device=pairs.device) if parts else torch.zeros((0,16),device=pairs.device,dtype=torch.bool)
    def forward(self,pairs,b,donor=None):
        self._states={};self._rawtokens=[];self._collect=True;z,raw=self.representation(pairs,b,True);self._collect=False
        ff=torch.cat(self._rawtokens,0) if self._rawtokens else b.new_zeros((0,16));self._rawtokens=[]
        hu,nu,_=self._states[0];hv,nv,_=self._states[1];lengths=nu*nv
        g=torch.repeat_interleave(torch.arange(len(pairs),device=b.device),lengths);count=len(g);offset=lengths.cumsum(0)-lengths;local=torch.arange(count,device=b.device)-offset[g]
        iu=(nu.cumsum(0)-nu)[g]+torch.div(local,nv[g],rounding_mode='floor');iv=(nv.cumsum(0)-nv)[g]+local%nv[g]
        x,y=hu[iu],hv[iv];originalx,originaly=x,y;mask=None
        if self.arm in ('COORDSWAP','EVEN_COORD'):
            mask=self.masks(pairs,lengths);x,y=torch.where(mask,y,x),torch.where(mask,x,y)
        boundaries=[];start=0;running=0
        for row,n in enumerate(lengths.cpu().tolist()):
            if row>start and running+n>131072:boundaries.append((start,row));start=row;running=0
            running+=n
        boundaries.append((start,len(pairs)));pools=[];tokens=[];evens=[];odds=[]
        for st,en in boundaries:
            lo=int(offset[st]) if st<len(pairs) else count;hi=int(offset[en]) if en<len(pairs) else count;xx,yy=x[lo:hi],y[lo:hi]
            if self.arm in ('INDEP','WIDE'):
                t=self.extra(e.symmetric(xx,yy));p=e.pool(t,lengths[st:en])
            else:
                even,odd=channels(self.extra,xx,yy);t=torch.cat((even,odd),1)
                p=e.pool(even,lengths[st:en]) if self.arm in ('EVEN','EVEN_COORD') else torch.cat((e.pool(even,lengths[st:en]),e.pool(odd,lengths[st:en])),1)
                if self.capture:evens.append(even);odds.append(odd)
            pools.append(p)
            if self.capture:tokens.append(t)
        added=torch.cat(pools,0)
        if self.capture:self._diag={'z':z,'raw':raw,'added':added,'ff':ff,'extra_tokens':torch.cat(tokens,0),'x':originalx,'y':originaly,'fed_x':x,'fed_y':y,'lengths':lengths,'mask':mask,
            'even':torch.cat(evens,0) if evens else None,'odd':torch.cat(odds,0) if odds else None}
        return b[:,0]+self.decoder(torch.cat((z,raw,added),1)).flatten(),b.new_zeros(()),b.new_zeros(())

def make_net(ds,seed,arm,phase,structure=None):
    if arm=='DUP':return m.make_net(ds,seed,'DUP',phase,structure) # literal historical V22
    if arm in ('INDEP','WIDE','EVEN','GSIR','COORDSWAP','EVEN_COORD'):
        stats=read(v.cache(ds,seed)/'normalization.json')
        return GSIRPredictor(structure or v.Structure(v.cache(ds)/'structure.npz'),seed,arm,np.asarray(stats['mean']),np.asarray(stats['std']),ds).to('cuda')
    return agg.install(e.ORIGINAL_MAKE(ds,seed,arm,phase,structure))
v.make_net=make_net

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
            with log.open('a') as f:p=subprocess.Popen([sys.executable,'-B','-u',str(Path(__file__).resolve()),*map(str,args)],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,env=os.environ.copy(),start_new_session=True)
            active.append((p,args,log));e.CHILDREN.append(p)
        state={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(q),'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
        if active:time.sleep(3)

@torch.no_grad()
def sanity():
    assert read(ART/'02_COLLISION_SANITY.json')['state']=='PASS'
    gen=torch.Generator().manual_seed(23003);psi=nn.Sequential(nn.Linear(64,29),nn.ReLU(),nn.Linear(29,8),nn.ReLU())
    with torch.random.fork_rng():
        torch.manual_seed(23003)
        for module in psi:
            if isinstance(module,nn.Linear):module.reset_parameters()
    x=torch.zeros((1,16));y=x.clone();x[0,:2]=torch.tensor([1.,2.]);y[0,:2]=torch.tensor([3.,4.]);xx=x.clone();yy=y.clone();xx[0,1]=4;yy[0,1]=2
    assert torch.equal(e.symmetric(x,y),e.symmetric(xx,yy));a,b=channels(psi,x,y);c,d=channels(psi,xx,yy);sep=float((torch.cat((a,b),1)-torch.cat((c,d),1)).abs().max());assert sep>1e-6,'NO_EXPRESSIVITY_WITNESS'
    artifact('03_EXPRESSIVITY_WITNESS.json',{'state':'PASS','maximum_GSIR_channel_difference':sep,'RAW_feature_error':0,'psi':[64,29,8],'seed':23003,'empirical_success':False})
    rx=torch.randn((128,16),generator=gen);ry=torch.randn((128,16),generator=gen);a,b=channels(psi,rx,ry);c,d=channels(psi,ry,rx)
    synthetic={'even':float((a-c).abs().max()),'odd':float((b-d).abs().max())};assert max(synthetic.values())==0
    real={};coord={};counts=None
    for ds in ('cora','pubmed'):
        net=make_net(ds,0,'GSIR','A');net.capture=True;base=agg.install(e.ORIGINAL_MAKE(ds,0,'A2','A'));capt=[];base.relation.register_forward_hook(lambda module,args,out:capt.append(out))
        pp=torch.tensor(np.load(v.cache(ds,0)/'valid_pairs.npy')[:128],device='cuda');bb=torch.tensor(np.load(v.cache(ds,0)/'valid_b.npy')[:128],device='cuda');bz,br=base.representation(pp,bb,True);net(pp,bb);data=net._diag
        assert torch.equal(bz,data['z']) and torch.equal(br,data['raw']) and torch.equal(torch.cat(capt,0),data['ff']),'RAW_SOURCE_CHANGED'
        x,y=data['x'],data['y'];a,b=channels(net.extra,x,y);c,d=channels(net.extra,y,x);pa=torch.cat((e.pool(a,data['lengths']),e.pool(b,data['lengths'])),1);pb=torch.cat((e.pool(c,data['lengths']),e.pool(d,data['lengths'])),1)
        # Swapping endpoint sets transposes each candidate's Cartesian enumeration.
        nu,nv=net._states[0][1],net._states[1][1];parts=[];pos=0
        for leftn,rightn in zip(nu.cpu().tolist(),nv.cpu().tolist()):
            n=leftn*rightn;parts.append(torch.arange(pos,pos+n,device=pp.device).reshape(leftn,rightn).T.reshape(-1));pos+=n
        transpose=torch.cat(parts);reordered=torch.cat((e.pool(c[transpose],data['lengths']),e.pool(d[transpose],data['lengths'])),1)
        err={'even':float((a-c).abs().max()),'odd':float((b-d).abs().max()),'pooled':float((pa-pb).abs().max()),'pooled_transposed_enumeration':float((pa-reordered).abs().max())};assert max(err.values())<=1e-6
        real[ds]={'state':'PASS','errors':err,'canonical_RAW_source_identity':'BITWISE_EXACT','tokens':len(x)}
        mask=net.masks(pp,data['lengths']);sx,sy=torch.where(mask,y,x),torch.where(mask,x,y);f=e.symmetric(x,y);sf=e.symmetric(sx,sy);err=(f-sf).abs().max(0).values;assert float(err.max())==0
        assert ((mask.sum(1)>0)&(mask.sum(1)<16)).all();dist=torch.linalg.vector_norm(torch.cat((x,y),1)-torch.cat((sx,sy),1),dim=1)
        coord[ds]={'state':'PASS','sum_max_error':float(err[:16].max()),'abs_difference_max_error':float(err[16:32].max()),'product_max_error':float(err[32:].max()),'ordered_concat_L2':e.distribution(dist.cpu().numpy()),'changed_coordinate_fraction':float((sx!=x).float().mean()),'all_masks_mixed':True}
        counts={arm:sum(p.numel() for p in make_net(ds,0,e.MAP.get(arm,arm),'A').parameters() if p.requires_grad) for arm in ARMS}
        assert counts=={'Z':26385,'RAW':28481,'SHARED':30529,'INDEP':32625,'WIDE':32555,'EVEN':32651,'GSIR':32654,'COORDSWAP':32654}
    artifact('04_COORDSWAP_AUDIT.json',{'state':'PASS','datasets':coord});artifact('05_GLOBAL_SWAP_INVARIANCE.json',{'state':'PASS','synthetic_errors':synthetic,'real':real,'tolerance':1e-6,'pooled_exchange':'same complete interaction multiset; exact channel invariantization, segment mean/max invariant within floating summation tolerance'})
    return counts

def preflight():
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);v.OUT=ROOT/'CHRI_V18_1';v.check_frozen();assert REPO.name in ('lchr_v2','DCDLP-main')
    previous=read(REPO/'result/innovation2/MERI_V22/SOURCE_HASHES.json')
    for p,h in previous['files'].items():assert sha(REPO/p)==h,'HISTORICAL_SOURCE_CHANGED '+p
    files=dict(previous['files'])
    for folder,word in (('CHRI_V18_1C','CANONICAL_SIGNAL_PRESENT'),('CHRI_V18_1S','CHRI_PHENOMENON_CONFIRMED_METHOD_NOT_IMPROVED'),('FCI_V19','FCI_REJECTED_NO_GAIN'),('RCP_V20','RCP_REJECTED_NO_GAIN'),('ERDR_V21','ERDR_REJECTED_SOURCE_RELATION'),('MERI_V22','MERI_REJECTED_NO_GAIN')):
        base=REPO/'result/innovation2'/folder;assert word in (base/'FINAL_REPORT.md').read_text()
        files.update({str(p.relative_to(REPO)):sha(p) for p in base.glob('*') if p.is_file() and p.suffix in ('.json','.md')})
    for p in [ROOT/'MERI_V22/scripts/meri22.py',*list((OUT/'scripts').glob('*.py')),*[ART/n for n in ('00_PROTOCOL.md','00_PROTOCOL_AMENDMENT_DUP_CONTROL.md','01_RAW_SYMMETRY_AUDIT.md','01_RAW_SYMMETRY_AUDIT.json','02_COLLISION_SANITY.json')]]:files[str(p.relative_to(REPO))]=sha(p)
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','files':files,'caches':previous['caches'],'canonical_protocol':PROTO});e.cache_check();counts=sanity()
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'workspace':'DCDLP-main','canonical_protocol':PROTO,'amendment_approved_before_training':True,'historical_V22_modified':False,
        'precheck':{'dataset':'pubmed','seed':0,'variants':['SHARED','INDEP','GSIR','COORDSWAP'],'replicates':2,'epochs':5},'phase_A':{'datasets':['cora','pubmed'],'seeds':[0,1,2],'variants':list(ARMS),'epochs':5},'trainable_parameters':counts,
        'architecture':{'INDEP':[48,32,16],'WIDE':[48,36,14],'EVEN':[64,26,16],'GSIR':[64,29,8]},'initialization_extra_encoder':23002,'initialization_decoder':21002,
        'shared_dup':'exact V22 MERIPredictor DUP, historical full FF shared relation + same decoder','coord_mask':'SHA256(dataset,seed,sorted candidate id) RNG rows indexed by relation token; firstfalse,lasttrue, fixed across epochs',
        'allowed_parameter_error':'0.5%; GSIR0.0889%, EVEN0.0797%, WIDE0.2146% vsINDEP','test_opened':False,'citeseer_run':False,'phase_B_run':False,'workers':6,'threads_per_worker':2})
    for n in ('06_DETERMINISM_PRECHECK.json','06A_SHARED_DUP_REPRODUCTION.json','06B_INDEP_DUP_DETERMINISM.json','07_PHASE_A_RESULTS.json','08_PAIRED_CONTRASTS.json','09_DUP_DIVERSITY_DIAGNOSTIC.json','09A_INDEP_DUP_DIVERSITY.json','10_COLLISION_FREQUENCY_DIAGNOSTIC.json','EVEN_COORDSWAP_RESULTS.json'):artifact(n,{'state':'NOT_RUN','reason':'Prerequisite pending.'})
    for n in ('11_RANKING_ANALYSIS.md','12_DECISION.md','FINAL_REPORT.md'):md(n,'# GSIR V23\n\nPENDING')
    print('GSIR_PREFLIGHT_PASS',counts,flush=True)

def reproduce_shared(phase,ds,seed):
    r=read(job(phase,ds,seed,'SHARED')/'result.json');historical=ROOT/'MERI_V22/executions/A'/ds/f'seed_{seed}/DUP/rep_1/runs/A'/ds/f'seed_{seed}/DUP'
    # PubMedseed0 Phase-A was a symlink to the V22 determinism first replicate.
    h=read(historical/'result.json');a=torch.load(job(phase,ds,seed,'SHARED')/'final.pt',map_location='cpu',weights_only=False)['state'];b=torch.load(historical/'final.pt',map_location='cpu',weights_only=False)['state']
    checks={'state_tensor_hash':statehash(a)==statehash(b),'validation_score_hash':r['score_vector_sha256']==h['score_vector_sha256'],
        'trajectory_hash':r['training_trajectory_sha256']==h['training_trajectory_sha256'],'validation_metrics':r['validation']==h['validation'],'history':r['history']==h['history'],'initialization':r['initialization']==h['initialization'],'cached_training_trace':r['training_trace']==h['training_trace'],'parameters':r['trainable_parameters']==h['trainable_parameters']==30529}
    return {'dataset':ds,'seed':seed,'pass':all(checks.values()),'checks':checks,'state_sha256':statehash(a),'historical_state_sha256':statehash(b),'checkpoint_file_hashes':[r['checkpoint_sha256'],h['checkpoint_sha256']],
        'phase_metadata_same':r['phase']==h['phase'],'metadata_note':'Different phase labels change archive bytes; state/score/trajectory hashes are exact required historical identity.'}

def summarize():
    data={'state':'COMPLETE','datasets':{},'test_opened':False};reproductions=[]
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{a:read(job('A',ds,s,a)/'result.json') for a in ARMS}} for s in range(3)]
        for row in rows:
            ref=row['arms']['RAW'];assert all(r['training_trace']==ref['training_trace'] for r in row['arms'].values())
            assert all(r['initialization']['encoder']==ref['initialization']['encoder'] and r['initialization']['relation']==ref['initialization']['relation'] for r in row['arms'].values())
            rr=reproduce_shared('A',ds,row['seed']);reproductions.append(rr);assert rr['pass'],'SHARED_DUP_HISTORICAL_REPRODUCTION_FAILED'
        effects={f'GSIR_vs_{a}':v.comparison(rows,'GSIR',a) for a in ('RAW','SHARED','INDEP','WIDE','EVEN','COORDSWAP')}
        effects['INDEP_vs_SHARED']=v.comparison(rows,'INDEP','SHARED')
        for a in ('RAW','SHARED','INDEP','WIDE'):effects[f'EVEN_vs_{a}']=v.comparison(rows,'EVEN',a)
        data['datasets'][ds]={'seed_results':rows,'effects':effects,'metrics':{a:{met:v.stat([r['arms'][a]['validation'][met] for r in rows]) for met in v.METRICS} for a in ARMS}}
    artifact('06A_SHARED_DUP_REPRODUCTION.json',{'state':'PASS','datasets':reproductions,'historical_V22_modified':False});artifact('07_PHASE_A_RESULTS.json',data);artifact('08_PAIRED_CONTRASTS.json',{'state':'COMPLETE','datasets':{ds:d['effects'] for ds,d in data['datasets'].items()}})
    return data

def basic_pass(data,arm):
    return all(d['effects'][f'{arm}_vs_RAW']['ce']['mean']>0 and d['effects'][f'{arm}_vs_RAW']['ce']['wins']>=2 and all(d['effects'][f'{arm}_vs_{a}']['ce']['mean']>0 for a in ('INDEP','WIDE')) for d in data['datasets'].values())

def covariance(x,y):
    x=x.astype(np.float64);y=y.astype(np.float64);xx=x-x.mean(0);yy=y-y.mean(0);cov=xx.T@yy/max(len(x)-1,1);corr=cov/np.maximum(x.std(0,ddof=1)[:,None]*y.std(0,ddof=1)[None,:],1e-12)
    return {'cross_covariance':cov.tolist(),'cross_correlation':corr.tolist(),'mean_abs_correlation':float(np.abs(corr).mean()),'max_abs_correlation':float(np.abs(corr).max())}
def distances(arrays):
    from scipy.spatial.distance import pdist,squareform
    from scipy.stats import spearmanr
    dist={k:pdist(a.astype(np.float64)) for k,a in arrays.items()};out={}
    for k,d in dist.items():
        mat=squareform(d);np.fill_diagonal(mat,np.inf);near=mat.min(1);positive=d[d>1e-12];scale=float(np.median(positive)) if len(positive) else 0
        out[k]={'sample_tokens':len(arrays[k]),'median_nonzero_distance':scale,'exact_collision_fraction':float(np.mean(near<=1e-12)),'near_collision_fraction':float(np.mean(near<=max(1e-12,1e-3*scale))),'near_threshold_relative_to_median':1e-3}
    out['distance_rank_correlations']={f'{a}_vs_{b}':float(spearmanr(dist[a],dist[b]).statistic) if np.std(dist[a])>0 and np.std(dist[b])>0 else None for a,b in (('ordered','symmetric'),('ordered','gsir'),('symmetric','gsir'))}
    return out

@torch.no_grad()
def diagnose(ds,seed):
    source=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}';report={'state':'COMPLETE','dataset':ds,'seed':seed,'test_opened':False};probes={}
    allarrays={};samples={};diversity={};channel={}
    for arm in ('INDEP','GSIR'):
        v.OUT=sandbox('A',ds,seed,arm,1);e.frozen_check();net=v.load_net('A',ds,seed,arm);net.capture=True;allarrays[arm]={}
        for split in ('train','validation'):
            pairs=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy')).reshape(-1,2);features=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r').reshape(-1,257)
            arr={k:[] for k in ('raw','extra')};cos=[];ratio=[];token1=[];token2=[];sample={k:[] for k in ('ordered','symmetric','gsir')};kept=0
            for st in range(0,len(pairs),128):
                pp=torch.tensor(pairs[st:st+128],device='cuda',dtype=torch.long);bb=torch.tensor(np.array(features[st:st+128]),device='cuda');net(pp,bb);d=net._diag
                arr['raw'].append(d['raw'].cpu().numpy());arr['extra'].append(d['added'].cpu().numpy())
                if arm=='INDEP':
                    x,y=d['ff'].cpu().numpy(),d['extra_tokens'].cpu().numpy();cos.append(e.cosine(x,y))
                    if split=='validation':token1.append(x);token2.append(y)
                else:
                    x,y=d['even'].cpu().numpy(),d['odd'].cpu().numpy();cos.append(e.cosine(x,y));ratio.append(np.linalg.norm(y,axis=1)/np.maximum(np.linalg.norm(x,axis=1),1e-12))
                    take=min(512-kept,len(x))
                    if take>0:
                        # Uniformly spaced deterministic indices in the current token block.
                        ix=torch.as_tensor(np.linspace(0,len(x)-1,take,dtype=int),device='cuda');sample['ordered'].append(torch.cat((d['x'][ix],d['y'][ix]),1).cpu().numpy());sample['symmetric'].append(e.symmetric(d['x'][ix],d['y'][ix]).cpu().numpy());sample['gsir'].append(d['extra_tokens'][ix].cpu().numpy());kept+=take
                net._diag={}
            a={k:np.concatenate(parts) for k,parts in arr.items()};allarrays[arm][split]=a
            if arm=='INDEP':
                diversity[split]={'token_cosine':e.distribution(np.concatenate(cos)),'pooled_cosine':e.distribution(e.cosine(a['raw'],a['extra']))}
                if split=='validation':diversity[split]['cross_statistics']=covariance(np.concatenate(token1),np.concatenate(token2))
            else:
                channel[split]={'even_odd_cosine':e.distribution(np.concatenate(cos)),'odd_over_even_norm':e.distribution(np.concatenate(ratio))};samples[split]=distances({k:np.concatenate(a) for k,a in sample.items()})
    t,q=allarrays['INDEP']['train'],allarrays['INDEP']['validation'];probes['branch2_from_branch1']=e.probe(t['raw'],t['extra'],q['raw'],q['extra'])
    report.update(independent_branch_diversity=diversity,independent_probe=probes,GSIR_channels=channel,collision_distances=samples)
    write(OUT/'diagnostics'/ds/f'seed_{seed}.json',report);print('GSIR_DIAGNOSTICS_COMPLETE',ds,seed,flush=True)

def finalize(data=None,even_control=None,status=None,reason=None):
    v.OUT=ROOT/'CHRI_V18_1';e.frozen_check();e.cache_check();lines=[];survivor='NONE';odd='NOT_SUPPORTED'
    if data:
        full=basic_pass(data,'GSIR') and all(d['effects']['GSIR_vs_COORDSWAP']['ce']['mean']>0 for d in data['datasets'].values());full_over_even=all(d['effects']['GSIR_vs_EVEN']['ce']['mean']>0 for d in data['datasets'].values())
        evenpass=even_control is not None and even_control['all_pass']
        if full and full_over_even:status='GSIR_PROMISING';survivor='EVEN_PLUS_ODD';odd='SUPPORTED';reason='Full GSIR passes all structural gates and beats EVEN mean CE on both datasets.'
        elif evenpass:status='GSIR_EVEN_PROMISING';survivor='EVEN';odd='NOT_NEEDED';reason='EVEN passes its RAW, capacity and matched coordinate-swap gates; retain EVEN only.'
        elif full:status='GSIR_PROMISING';survivor='EVEN_PLUS_ODD';odd='NOT_SUPPORTED';reason='Full GSIR passes structural gates; extra odd-channel benefit over EVEN is not established cross-dataset.'
        else:
            d=list(data['datasets'].values())
            if not all(x['effects']['GSIR_vs_RAW']['ce']['mean']>0 and x['effects']['GSIR_vs_RAW']['ce']['wins']>=2 for x in d):status='GSIR_REJECTED_NO_GAIN';reason='Full GSIR fails the both-dataset RAW mean/win gate; EVEN does not independently survive.'
            elif not all(x['effects']['GSIR_vs_INDEP']['ce']['mean']>0 for x in d):
                sharedbetter=any(x['effects']['GSIR_vs_SHARED']['ce']['mean']<=0 for x in d)
                status='GSIR_REJECTED_DECODER_CAPACITY' if sharedbetter else 'GSIR_REJECTED_INDEPENDENT_CAPACITY';reason='GSIR fails independent capacity gate; historical shared duplicate comparison reported separately.'
            elif not all(x['effects']['GSIR_vs_WIDE']['ce']['mean']>0 for x in d):status='GSIR_REJECTED_GENERIC_CAPACITY';reason='GSIR fails WIDE gate.'
            else:status='GSIR_REJECTED_GLOBAL_PAIRING';reason='GSIR fails coordinate-swap structural falsification.'
        if survivor=='EVEN_PLUS_ODD' and all(d['effects']['GSIR_vs_RAW']['mrr']['mean']>0 for d in data['datasets'].values()):status='GSIR_PROMISING_WITH_RANKING_GAIN'
        diag={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')}
        div={'state':'COMPLETE','datasets':{ds:[{'seed':r['seed'],'diversity':r['independent_branch_diversity'],'probe':r['independent_probe'],'GSIR_channels':r['GSIR_channels']} for r in rr] for ds,rr in diag.items()},'shared_duplicate_diversity':'NOT_APPLICABLE: same phi, same tokens; exact reproduction reported in06A'}
        artifact('09_DUP_DIVERSITY_DIAGNOSTIC.json',div);artifact('09A_INDEP_DUP_DIVERSITY.json',div);artifact('10_COLLISION_FREQUENCY_DIAGNOSTIC.json',{'state':'COMPLETE','datasets':{ds:[{'seed':r['seed'],'distances':r['collision_distances']} for r in rr] for ds,rr in diag.items()},'labels_used':False,'sample_scope':'deterministic up to512 tokens, earliest blocks with uniformly spaced within-block indices; not an unbiased full-population collision frequency estimate'})
        lines=['| Dataset | Contrast | Mean DeltaCE | CE wins | Mean DeltaMRR |','|---|---|---:|---:|---:|']
        for ds,d in data['datasets'].items():
            for name,ef in d['effects'].items():lines.append(f"| {ds} | {name} | {ef['ce']['mean']:.10g} | {ef['ce']['wins']}/3 | {ef['mrr']['mean']:.10g} |")
        ranking={ds:('RANKING_IMPROVED' if d['effects']['GSIR_vs_RAW']['mrr']['mean']>0 else ('RANKING_DEGRADED' if d['effects']['GSIR_vs_RAW']['mrr']['mean']<0 else 'RANKING_NEUTRAL')) for ds,d in data['datasets'].items()}
        table='\n'.join(lines);md('11_RANKING_ANALYSIS.md','# Ranking\n\n'+table+'\n\n'+json.dumps(ranking,indent=2)+'\n\nRanking is descriptive and never optimized separately.')
        report=['# V23 amended GSIR final report','',f'FINAL_STATUS: {status}',f'REASON: {reason}',f'SURVIVING_STRUCTURE: {survivor}',f'ODD_CHANNEL: {odd}','',table,'','## Historical control correction','V22 DUP is shared phi plus duplicated representation/decoder slots. It is NOT an independent relation basis. Amendment occurred BEFORE all V23 training. Original audits are retained unchanged. SHARED-DUP is reproduced exactly in state weights, trajectory, prediction vectors and metrics; phase metadata difference is explicitly documented.','',json.dumps(read(ART/'06A_SHARED_DUP_REPRODUCTION.json'),indent=2),'','## Complete metrics and parameter counts','',json.dumps({ds:d['metrics'] for ds,d in data['datasets'].items()},indent=2),json.dumps(read(ART/'RUN_MANIFEST.json'),indent=2),'','## Preflight and determinism','',json.dumps({n:read(ART/n) for n in ('03_EXPRESSIVITY_WITNESS.json','04_COORDSWAP_AUDIT.json','05_GLOBAL_SWAP_INVARIANCE.json','06_DETERMINISM_PRECHECK.json')},indent=2),'','## Independent diversity and global-pair distance diagnostics','',json.dumps(diag,indent=2),'','## EVEN matched control','',json.dumps(even_control or read(ART/'EVEN_COORDSWAP_RESULTS.json'),indent=2),'','Synthetic collision separation is expressivity evidence only. Real-data distance diagnostics are label-free sampled statistics, not proof of predictive information loss. Parameter matching differences are all below0.5%. No novelty or causal claim.','TEST_OPENED: NO','INNOVATION_1_MODIFIED: NO','HISTORICAL_RESULTS_MODIFIED: NO']
        md('FINAL_REPORT.md','\n'.join(report))
    else:md('FINAL_REPORT.md',f'# GSIR V23\n\nFINAL_STATUS: {status}\n\n{reason}\n\nTEST_OPENED: NO')
    md('12_DECISION.md',f'# Decision\n\n{status}\n\n{reason}\n\nSURVIVING_STRUCTURE: {survivor}\nODD_CHANNEL: {odd}')
    state={'state':'COMPLETE','final_status':status,'reason':reason,'ended_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
    md('C2C_HANDOFF.md','\n'.join(['STATUS: EXECUTED','TASK: GSIR_V23_GLOBAL_SWAP_RELATION_VALIDATION',f'CANONICAL_PROTOCOL: {PROTO}',f'FINAL_STATUS: {status}',f'SURVIVING_STRUCTURE: {survivor}',f'ODD_CHANNEL: {odd}','TRAINING_STARTED_BEFORE_AMENDMENT: NO','SHARED_DUP_HISTORY: REPRODUCED' if data else 'SHARED_DUP_HISTORY: SEE06A','\n'.join(lines),'TEST_OPENED: NO','HISTORICAL_RESULTS_MODIFIED: NO','INNOVATION_1_MODIFIED: NO','PRIMARY_ARTIFACT: result/innovation2/GSIR_V23/FINAL_REPORT.md','NEXT_EXPECTED_STEP: Return evidence to user and STOP; no rescue or test.']));print('GSIR_COMPLETE',status,flush=True)

def supervise():
    try:
        preflight();batch([('run','D','pubmed',0,a,r) for a in ('SHARED','INDEP','GSIR','COORDSWAP') for r in (1,2)],'DETERMINISM_PRECHECK')
        records=[]
        for arm in ('SHARED','INDEP','GSIR','COORDSWAP'):
            rr=[read(job('D','pubmed',0,arm,r)/'result.json') for r in (1,2)];keys=('checkpoint_sha256','score_vector_sha256','training_trajectory_sha256','history','training_trace');checks={k:rr[0][k]==rr[1][k] for k in keys};records.append({'arm':arm,'pass':all(checks.values()),'checks':checks,'hashes':{k:[r[k] for r in rr] for k in keys[:3]}})
        e.cache_check();ok=all(x['pass'] for x in records);artifact('06_DETERMINISM_PRECHECK.json',{'state':'PASS' if ok else 'FAIL','pairs':records,'canonical_caches_unchanged':True,'candidate_order_negatives_permutations_unchanged':True,'test_opened':False});artifact('06B_INDEP_DUP_DETERMINISM.json',records[1])
        reproduction=reproduce_shared('D','pubmed',0);artifact('06A_SHARED_DUP_REPRODUCTION.json',{'state':'PASS' if reproduction['pass'] else 'FAIL','precheck':reproduction})
        if not ok or not reproduction['pass']:finalize(status='DETERMINISTIC_PROTOCOL_FAILURE',reason='Duplicate or historical SHARED-DUP reproduction gate failed.');return
        for arm in ('SHARED','INDEP','GSIR','COORDSWAP'):
            dest=job('A','pubmed',0,arm);dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():dest.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS if not(ds=='pubmed' and s==0 and a in ('SHARED','INDEP','GSIR','COORDSWAP'))],'PHASE_A')
        data=summarize();control=None;full_wins_even=all(d['effects']['GSIR_vs_EVEN']['ce']['mean']>0 for d in data['datasets'].values())
        if not full_wins_even and basic_pass(data,'EVEN'):
            batch([('run','B',ds,s,'EVEN_COORD',1) for ds in ('cora','pubmed') for s in range(3)],'MATCHED_EVEN_COORDSWAP')
            control={'state':'COMPLETE','datasets':{}}
            for ds,d in data['datasets'].items():
                rows=[{'seed':r['seed'],'arms':{'EVEN':r['arms']['EVEN'],'EVEN_COORD':read(job('B',ds,r['seed'],'EVEN_COORD')/'result.json')}} for r in d['seed_results']];ef=v.comparison(rows,'EVEN','EVEN_COORD');control['datasets'][ds]={'effects':ef,'seed_results':rows,'pass':ef['ce']['mean']>0}
            control['all_pass']=all(x['pass'] for x in control['datasets'].values());artifact('EVEN_COORDSWAP_RESULTS.json',control)
        else:artifact('EVEN_COORDSWAP_RESULTS.json',{'state':'NOT_RUN','reason':'EVEN did not emerge as a both-dataset RAW/capacity-passing alternative to FULL; no extra experiment justified.'})
        batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'REPRESENTATION_DIAGNOSTICS',workers=3);finalize(data,control)
    except BaseException as error:
        for p in e.CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        err={'state':'EXECUTION_FAILED','final_status':'TEST_SEAL_VIOLATION' if 'TEST_SEAL_VIOLATION' in str(error) else 'GSIR_IMPLEMENTATION_ERROR','error':repr(error),'traceback':traceback.format_exc(),'ended_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',err);artifact('RUN_STATUS.json',err);artifact('ERROR.json',err);md('FINAL_REPORT.md','# GSIR execution failure\n\n'+json.dumps(err,indent=2));print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='preflight':preflight()
    elif cmd=='supervise':supervise()
    elif cmd=='run':e.run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif cmd=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    else:raise ValueError(cmd)
