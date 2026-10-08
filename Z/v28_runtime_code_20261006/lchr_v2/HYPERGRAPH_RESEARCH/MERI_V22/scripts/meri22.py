"""V22 MERI: one shared canonical relation operator, mixed role differences."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1')
import sys,json,hashlib,time,traceback,signal,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent;OUT=ROOT/'MERI_V22';ART=REPO/'result/innovation2/MERI_V22'
sys.path.insert(0,str(ROOT/'ERDR_V21/scripts'));import erdr21 as e
np,torch,nn,v,agg=e.np,e.torch,e.nn,e.v,e.agg
e.OUT=OUT;e.ART=ART;e.context_path=lambda ds:ROOT/'ERDR_V21/context_cache'/f'{ds}.npz'
read,write,sha,artifact,md,sandbox,job=e.read,e.write,e.sha,e.artifact,e.md,e.sandbox,e.job
PROTO=e.PROTO;ARMS=('Z','RAW','DUP','MERI','FIRST','SHUFFLE');MAP=e.MAP

def mixed(ff,fc,cf,cc):return ff-fc-cf+cc

def permutation(pairs,counts,seed):
    """Candidate-local nonzero rotation; preserves the context multiset exactly."""
    parts=[];offset=0;eligible=0
    for (u,w),n in zip(pairs.sort(dim=1).values.cpu().tolist(),counts.cpu().tolist()):
        shift=1+int.from_bytes(hashlib.sha256(f'{seed}/{u}/{w}/{n}'.encode()).digest()[:8],'little')%(n-1) if n>1 else 0
        order=(torch.arange(n,device=pairs.device)+shift)%max(n,1)
        assert torch.equal(torch.sort(order).values,torch.arange(n,device=pairs.device)),'SHUFFLE_NOT_BIJECTIVE'
        parts.append(order+offset);offset+=n;eligible+=int(n>1)
    return torch.cat(parts) if parts else torch.empty(0,device=pairs.device,dtype=torch.long),eligible

class MERIPredictor(v.RelationPredictor):
    def __init__(self,structure,seed,arm,mean,std):
        super().__init__(structure,seed,'A2',mean,std);self.arm=arm;self.seed=seed;self.capture=False;self._states={};self._rawtokens=[];self._collect=False;self._diag={}
        agg.install(self);self.endpoint=lambda pairs,side:e.ERDRPredictor.source_endpoint(self,pairs,side)
        def hook(module,args,result):
            if self._collect:self._rawtokens.append(result)
        self.relation.register_forward_hook(hook)
        base=self.decoder
        with torch.random.fork_rng():
            torch.manual_seed(21002+seed);ext=nn.Sequential(nn.Linear(385,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
        with torch.no_grad():
            ext[0].weight[:,:353].copy_(base[0].weight);ext[0].bias.copy_(base[0].bias)
            for i in (2,4):ext[i].load_state_dict(base[i].state_dict())
        self.decoder=ext
    def forward(self,pairs,b,donor=None):
        self._states={};self._rawtokens=[];self._collect=True;z,raw=self.representation(pairs,b,True);self._collect=False
        ff=torch.cat(self._rawtokens,0) if self._rawtokens else b.new_zeros((0,16));self._rawtokens=[]
        hu,cu,au,nu,vu,su,gu,eu=self._states[0];hv,cv,av,nv,vv,sv,gv,ev=self._states[1]
        lengths=nu*nv;groups=torch.repeat_interleave(torch.arange(len(pairs),device=b.device),lengths);count=len(groups)
        offset=lengths.cumsum(0)-lengths;local=torch.arange(count,device=b.device)-offset[groups]
        iu=(nu.cumsum(0)-nu)[groups]+torch.div(local,nv[groups],rounding_mode='floor');iv=(nv.cumsum(0)-nv)[groups]+local%nv[groups]
        order,eligible=permutation(pairs,nv,self.seed) if self.arm=='SHUFFLE' or self.capture else (torch.arange(len(cv),device=b.device),0)
        cfcontext=cv[order] if self.arm=='SHUFFLE' else cv;vfcontext=vv[order] if self.arm=='SHUFFLE' else vv
        valid=vu[iu]&vfcontext[iv];validlengths=(torch.bincount(gu[vu],minlength=len(pairs))*torch.bincount(gv[vfcontext],minlength=len(pairs)))
        assert int(validlengths.sum())==int(valid.sum()),'VALID_TOKEN_COUNTS_CHANGED'
        boundaries=[];start=0;running=0
        for row,n in enumerate(lengths.cpu().tolist()):
            if row>start and running+n>131072:boundaries.append((start,row));start=row;running=0
            running+=n
        boundaries.append((start,len(pairs)));pools=[];roleparts={k:[] for k in ('fc','cf','cc','m','du','dv')}
        for st,en in boundaries:
            lo=int(offset[st]) if st<len(pairs) else count;hi=int(offset[en]) if en<len(pairs) else count
            x,y=iu[lo:hi],iv[lo:hi];F=ff[lo:hi];ok=valid[lo:hi]
            if self.arm=='DUP' and not self.capture:T=F
            else:
                fc=self.relation(e.symmetric(hu[x],cfcontext[y]));cf=self.relation(e.symmetric(cu[x],hv[y]));cc=self.relation(e.symmetric(cu[x],cfcontext[y]))
                m=mixed(F,fc,cf,cc);du=F-cf;dv=F-fc
                T=F if self.arm=='DUP' else (.5*(du+dv) if self.arm=='FIRST' else m)
                if self.capture:
                    for k,val in zip(roleparts,(fc,cf,cc,m,du,dv)):roleparts[k].append(val)
            pools.append(e.pool(T[ok],validlengths[st:en]))
        pooled=torch.cat(pools,0)
        if self.capture:
            self._diag={'z':z,'raw':raw,'pooled':pooled,'ff':ff,'valid':valid,'lengths':lengths,'validlengths':validlengths,
                'states':self._states,'right_permutation':order,'shuffle_eligible_candidates':eligible,
                **{k:torch.cat(parts,0) for k,parts in roleparts.items()}}
        return b[:,0]+self.decoder(torch.cat((z,raw,pooled),1)).flatten(),b.new_zeros(()),b.new_zeros(())

def make_net(ds,seed,arm,phase,structure=None):
    if arm in ARMS[2:]:
        stats=read(v.cache(ds,seed)/'normalization.json')
        return MERIPredictor(structure or e.ContextStructure(ds),seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda')
    return agg.install(e.ORIGINAL_MAKE(ds,seed,arm,phase,structure))
v.make_net=make_net

def batch(tasks,stage,workers=6):
    # Launch THIS script explicitly; V21's launcher must never launch historical jobs.
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

def algebra():
    gen=torch.Generator().manual_seed(22001);a=[torch.randn((19,16),generator=gen,dtype=torch.float64) for _ in range(4)]
    ce,cf,ae,af=a;he,hf=ce+ae,cf+af;W=torch.randn((16,16),generator=gen,dtype=torch.float64)
    op=lambda x,y:x@W+torch.sin(y)
    zero=mixed(op(he,hf),op(he,cf),op(ce,hf),op(ce,cf));ea=float(zero.abs().max())
    bil=lambda x,y:torch.einsum('bi,ij,bj->b',x,W,y)
    mb=mixed(bil(he,hf),bil(he,cf),bil(ce,hf),bil(ce,cf));eb=float((mb-bil(ae,af)).abs().max())
    ff,fc,cff,cc=[torch.randn((19,16),generator=gen,dtype=torch.float64) for _ in range(4)]
    explicit=torch.stack([torch.stack([ff[i,j]-fc[i,j]-cff[i,j]+cc[i,j] for j in range(16)]) for i in range(19)])
    ec=float((mixed(ff,fc,cff,cc)-explicit).abs().max())
    obj={'state':'PASS' if max(ea,eb,ec)<1e-10 else 'FAIL','additive_max_error':ea,'bilinear_cross_term_max_error':eb,'explicit_formula_max_error':ec,'tolerance':1e-10,'dtype':'float64'}
    artifact('01_ALGEBRAIC_SANITY.json',obj);assert obj['state']=='PASS','MERI_IMPLEMENTATION_ERROR_ALGEBRA'

@torch.no_grad()
def source_audit(ds):
    net=make_net(ds,0,'MERI','A');net.capture=True;base=agg.install(e.ORIGINAL_MAKE(ds,0,'A2','A'));bt=[]
    base.relation.register_forward_hook(lambda module,args,result:bt.append(result))
    pp=torch.as_tensor(np.load(v.cache(ds,0)/'valid_pairs.npy')[:128],device='cuda');bb=torch.tensor(np.load(v.cache(ds,0)/'valid_b.npy')[:128],device='cuda')
    bz,br=base.representation(pp,bb,True);net(pp,bb);d=net._diag
    assert torch.equal(d['ff'],torch.cat(bt,0)) and torch.equal(bz,d['z']) and torch.equal(br,d['raw']),'CANONICAL_RAW_IDENTITY_FAIL'
    # Reuse V21's independent explicit membership reconstruction oracle unchanged.
    context=e.sanity(ds)
    counts={arm:sum(p.numel() for p in make_net(ds,0,MAP.get(arm,arm),'A').parameters() if p.requires_grad) for arm in ARMS}
    assert len({counts[a] for a in ARMS[2:]})==1,'PARAMETER_MISMATCH'
    original={k:d[k].clone() for k in ('ff','z','raw')};net.arm='SHUFFLE';net(pp,bb);sh=net._diag
    assert all(torch.equal(sh[k],original[k]) for k in original),'SHUFFLE_CHANGED_RAW_Z'
    for side in (0,1):
        assert torch.equal(d['states'][side][1],sh['states'][side][1]),'SHUFFLE_CHANGED_CONTEXT_INPUT'
    assert torch.equal(sh['validlengths'],d['validlengths']),'SHUFFLE_CHANGED_TOKEN_COUNT'
    return {'state':'PASS','canonical_FF_Z_RAW_identity':'BITWISE_EXACT','V21_context_recomputation':context,
        'shared_relation_operator':'literal SAME self.relation module for all four evaluations','new_relation_parameters':0,
        'trainable_parameters':counts,'shuffle_RAW_Z_unchanged':'BITWISE_EXACT','shuffle_valid_token_counts_unchanged':True,'test_opened':False}

def preflight():
    assert REPO.name in ('DCDLP-main','lchr_v2') and sha(ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py')==e.AGG_SHA
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);v.OUT=ROOT/'CHRI_V18_1';v.check_frozen()
    files={str(p.relative_to(REPO)):sha(p) for p in (OUT/'scripts').glob('*.py')}
    files[str((ART/'00_PROTOCOL.md').relative_to(REPO))]=sha(ART/'00_PROTOCOL.md')
    for folder,state in (('CHRI_V18_1C','CANONICAL_SIGNAL_PRESENT'),('CHRI_V18_1S','CHRI_PHENOMENON_CONFIRMED_METHOD_NOT_IMPROVED'),('FCI_V19','FCI_REJECTED_NO_GAIN'),('RCP_V20','RCP_REJECTED_NO_GAIN'),('ERDR_V21','ERDR_REJECTED_SOURCE_RELATION')):
        base=REPO/'result/innovation2'/folder;assert state in (base/'FINAL_REPORT.md').read_text()
        files.update({str(p.relative_to(REPO)):sha(p) for p in base.glob('*') if p.is_file() and p.suffix in ('.json','.md')})
    old=read(REPO/'result/innovation2/ERDR_V21/SOURCE_HASHES.json')
    for path,h in old['files'].items():assert sha(REPO/path)==h,'V21_FROZEN_MISMATCH '+path
    files.update(old['files'])
    files[str((ROOT/'ERDR_V21/scripts/erdr21.py').relative_to(REPO))]=sha(ROOT/'ERDR_V21/scripts/erdr21.py')
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','files':files,'caches':old['caches'],'canonical_protocol':PROTO,'V21_context_cache_reused':True})
    e.cache_check();algebra();audit={ds:source_audit(ds) for ds in ('cora','pubmed')};artifact('02_SOURCE_CONSISTENCY.json',{'state':'PASS','datasets':audit,'test_opened':False})
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'canonical_protocol':PROTO,'workspace':'DCDLP-main',
        'precheck':{'dataset':'pubmed','seed':0,'variants':['MERI','FIRST','SHUFFLE'],'replicates':2,'epochs':5},
        'phase_A':{'datasets':['cora','pubmed'],'seeds':[0,1,2],'variants':list(ARMS),'epochs':5},
        'phi':'single literal shared canonical 48->32->16 ReLU; NO new relation parameters','token':'FF-FC-CF+CC',
        'FIRST':'0.5*((FF-CF)+(FF-FC)), invariant to endpoint exchange','DUP':'identity second pool of FF',
        'pool':'signed deterministic segment mean/max over valid interactions; zero if none','decoder':'385->64->32->1 matched all new arms; first353 columns copied canonical; seed21002+seed',
        'shuffle':'candidate-local right-context nonzero cyclic rotation, SHA256(seed,sorted_u,sorted_v,count); singleton unchanged; validity permuted with context',
        'test_opened':False,'phase_B_run':False,'citeseer_run':False,'innovation1_modified':False,'historical_results_modified':False,'workers':6,'cpu_threads_per_worker':2})
    md('06_FIRST_ORDER_CONTROL.md','# First-order control\n\nFIRST token = (d_U+d_V)/2 = FF-(CF+FC)/2. Fixed symmetric combination, 16d tokens, mean/max 32d pooled branch, same shared phi and decoder as MERI. No second-order difference and no extra parameters. No coefficient tuning.')
    for name in ('03_DETERMINISM_PRECHECK.json','04_PHASE_A_RESULTS.json','05_PAIRED_CONTRASTS.json','07_SHUFFLE_CONTROL_AUDIT.json','08_MERI_DIAGNOSTICS.json','09_NONREDUNDANCY_PROBES.json'):artifact(name,{'state':'NOT_RUN','reason':'Prerequisite pending.'})
    for name in ('10_RANKING_ANALYSIS.md','11_DECISION.md','FINAL_REPORT.md'):md(name,'# MERI V22\n\nPENDING')
    print('MERI_PREFLIGHT_PASS',json.dumps(audit),flush=True)

def summarize():
    output={'state':'COMPLETE','datasets':{},'test_opened':False}
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{a:read(job('A',ds,s,a)/'result.json') for a in ARMS}} for s in range(3)]
        for row in rows:
            ref=row['arms']['RAW'];assert all(r['training_trace']==ref['training_trace'] for r in row['arms'].values()),'PAIRED_INPUT_TRACE_MISMATCH'
            assert len({row['arms'][a]['trainable_parameters'] for a in ARMS[2:]})==1
            assert len({row['arms'][a]['initialization']['decoder'] for a in ARMS[2:]})==1
            for key in ('encoder','relation'):assert all(r['initialization'][key]==ref['initialization'][key] for r in row['arms'].values())
        effects={f'MERI_vs_{a}':v.comparison(rows,'MERI',a) for a in ('RAW','DUP','FIRST','SHUFFLE','Z')}
        gates={'RAW_mean':effects['MERI_vs_RAW']['ce']['mean']>0,'RAW_wins':effects['MERI_vs_RAW']['ce']['wins']>=2,
            **{a+'_mean':effects[f'MERI_vs_{a}']['ce']['mean']>0 for a in ('DUP','FIRST','SHUFFLE','Z')}}
        output['datasets'][ds]={'seed_results':rows,'effects':effects,'gates':gates,'pass':all(gates.values()),'metrics':{a:{m:v.stat([r['arms'][a]['validation'][m] for r in rows]) for m in v.METRICS} for a in ARMS}}
    output['all_pass']=all(x['pass'] for x in output['datasets'].values());artifact('04_PHASE_A_RESULTS.json',output)
    artifact('05_PAIRED_CONTRASTS.json',{'state':'COMPLETE','datasets':{ds:x['effects'] for ds,x in output['datasets'].items()},'delta_CE':'CE(comparator)-CE(MERI)'})
    return output

@torch.no_grad()
def diagnose(ds,seed):
    v.OUT=sandbox('A',ds,seed,'MERI',1);e.frozen_check();net=v.load_net('A',ds,seed,'MERI');net.capture=True;source=v.cache(ds,seed)
    result={'state':'COMPLETE','dataset':ds,'seed':seed,'test_opened':False};arrays={};audit={'state':'PASS','contexts_original':hashlib.sha256(),'contexts_shuffle_recovered':hashlib.sha256(),'raw_original':hashlib.sha256(),'raw_shuffle':hashlib.sha256(),'candidate_count':0,'shuffle_eligible_candidates':0,'checked_token_count':0}
    for split in ('train','validation'):
        pairs=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy')).reshape(-1,2);features=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r').reshape(-1,257)
        vals={k:[] for k in ('norm_FF','norm_FC','norm_CF','norm_CC','norm_MERI','norm_MERI_over_FF','cos_MERI_FF','cos_MERI_dU','cos_MERI_dV')}
        ar={k:[] for k in ('z','raw','meri')};means=[];maxima=[];hasvalid=[];validtokens=totaltokens=0
        for st in range(0,len(pairs),128):
            pp=torch.tensor(pairs[st:st+128],device='cuda',dtype=torch.long);bb=torch.tensor(np.array(features[st:st+128]),device='cuda');net.arm='MERI';net(pp,bb);d=net._diag
            ok=d['valid'];xs={k:d[k][ok].cpu().numpy() for k in ('ff','fc','cf','cc','m','du','dv')};norms={k:np.linalg.norm(x,axis=1) for k,x in xs.items()}
            if split=='validation':
                for name,k in (('norm_FF','ff'),('norm_FC','fc'),('norm_CF','cf'),('norm_CC','cc'),('norm_MERI','m')):vals[name].append(norms[k])
                vals['norm_MERI_over_FF'].append(norms['m']/np.maximum(norms['ff'],1e-12))
                for name,k in (('cos_MERI_FF','ff'),('cos_MERI_dU','du'),('cos_MERI_dV','dv')):vals[name].append(e.cosine(xs['m'],xs[k]))
            norms_gpu=torch.linalg.vector_norm(d['m'][ok],dim=1)[:,None];lengths=d['validlengths'];pooled=e.pool(norms_gpu,lengths).cpu().numpy();means.append(pooled[:,0]);maxima.append(pooled[:,1]);hasvalid.append((lengths>0).cpu().numpy())
            validtokens+=int(ok.sum());totaltokens+=len(ok)
            ar['z'].append(d['z'].cpu().numpy());ar['raw'].append(d['raw'].cpu().numpy());ar['meri'].append(d['pooled'].cpu().numpy())
            # Actual shuffled forward with SAME weights; all RAW/Z and context sources fixed.
            net.arm='SHUFFLE';net(pp,bb);sh=net._diag
            assert torch.equal(d['ff'],sh['ff']) and torch.equal(d['raw'],sh['raw']) and torch.equal(d['z'],sh['z']),'SHUFFLE_CONTROL_INVALID_RAW'
            assert torch.equal(d['lengths'],sh['lengths']) and torch.equal(d['validlengths'],sh['validlengths']),'SHUFFLE_CONTROL_INVALID_COUNTS'
            for side in (0,1):
                c=d['states'][side][1];sc=sh['states'][side][1];assert torch.equal(c,sc)
                if side==1:sc=sc[sh['right_permutation']][torch.argsort(sh['right_permutation'])]
                assert torch.equal(c,sc),'SHUFFLE_CONTROL_INVALID_CONTEXT_MULTISET'
                audit['contexts_original'].update(c.cpu().contiguous().numpy().tobytes());audit['contexts_shuffle_recovered'].update(sc.cpu().contiguous().numpy().tobytes())
            audit['raw_original'].update(d['ff'].cpu().contiguous().numpy().tobytes());audit['raw_shuffle'].update(sh['ff'].cpu().contiguous().numpy().tobytes())
            audit['candidate_count']+=len(pp);audit['shuffle_eligible_candidates']+=sh['shuffle_eligible_candidates'];audit['checked_token_count']+=len(ok);net._diag={}
        arrays[split]={k:np.concatenate(parts) for k,parts in ar.items()};mn=np.concatenate(means);mx=np.concatenate(maxima);hv=np.concatenate(hasvalid)
        result[split]={'candidate_count':len(pairs),'valid_MERI_token_candidate_percentage':float(hv.mean()*100),'valid_token_count':validtokens,'total_RAW_token_count':totaltokens}
        if split=='validation':
            npos=int(e.sealed(ds)['valid_pos'].shape[0]);pop={'positive':np.arange(len(pairs))<npos,'negative':np.arange(len(pairs))>=npos}
            result[split].update(token_distributions={k:e.distribution(np.concatenate(x)) for k,x in vals.items()},
                candidate_magnitude={name:{'valid_candidates':int((mask&hv).sum()),'mean_token_norm':e.distribution(mn[mask&hv]),'max_token_norm':e.distribution(mx[mask&hv])} for name,mask in pop.items()},
                label_use='descriptive only; invalid candidate zero omitted from magnitude populations')
    t,q=arrays['train'],arrays['validation'];result['MERI_from_RAW']=e.probe(t['raw'],t['meri'],q['raw'],q['meri']);result['MERI_from_Z']=e.probe(t['z'],t['meri'],q['z'],q['meri'])
    for k in ('contexts_original','contexts_shuffle_recovered','raw_original','raw_shuffle'):audit[k]=audit[k].hexdigest()
    audit['shuffle_eligible_candidate_percentage']=100*audit['shuffle_eligible_candidates']/max(1,audit['candidate_count']);audit['singleton_groups']='unchanged, unshufflable; not treated as positive correspondence evidence'
    result['shuffle_audit']=audit;write(OUT/'diagnostics'/ds/f'seed_{seed}.json',result);print('MERI_DIAGNOSTICS_COMPLETE',ds,seed,flush=True)

def finalize(data=None,status=None,reason=None):
    v.OUT=ROOT/'CHRI_V18_1';e.frozen_check();e.cache_check();table='';diag=None
    if data:
        diag={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')}
        artifact('08_MERI_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':diag})
        artifact('09_NONREDUNDANCY_PROBES.json',{'state':'COMPLETE','datasets':{ds:[{'seed':r['seed'],'MERI_from_RAW':r['MERI_from_RAW'],'MERI_from_Z':r['MERI_from_Z']} for r in rr] for ds,rr in diag.items()},'used_for_training_or_gate':False})
        artifact('07_SHUFFLE_CONTROL_AUDIT.json',{'state':'PASS','datasets':{ds:[r['shuffle_audit'] for r in rr] for ds,rr in diag.items()},'semantics':read(ART/'RUN_MANIFEST.json')['shuffle']})
        gates=[d['gates'] for d in data['datasets'].values()]
        if not all(g['RAW_mean'] and g['RAW_wins'] and g['Z_mean'] for g in gates):status='MERI_REJECTED_NO_GAIN';reason='MERI fails the both-dataset RAW/Z CE gate.'
        elif not all(g['DUP_mean'] for g in gates):status='MERI_REJECTED_CAPACITY_EXPLANATION';reason='MERI does not beat DUP in mean CE on both datasets.'
        elif not all(g['FIRST_mean'] for g in gates):status='MERI_REJECTED_FIRST_ORDER_EXPLANATION';reason='MERI does not beat FIRST in mean CE on both datasets.'
        elif not all(g['SHUFFLE_mean'] for g in gates):status='MERI_REJECTED_CORRESPONDENCE';reason='MERI does not beat SHUFFLE in mean CE on both datasets.'
        else:
            status='MERI_PROMISING_WITH_RANKING_GAIN' if all(d['effects']['MERI_vs_RAW']['mrr']['mean']>0 for d in data['datasets'].values()) else 'MERI_PROMISING_MIXED_ROLE_SIGNAL';reason='All preregistered source, capacity, first-order and correspondence gates pass.'
        lines=['| Dataset | Contrast | Mean DeltaCE | CE wins | Mean DeltaMRR | Mean DeltaHits10 | Mean DeltaAUC |','|---|---|---:|---:|---:|---:|---:|'];ranking={}
        for ds,d in data['datasets'].items():
            for name,ef in d['effects'].items():lines.append(f"| {ds} | {name} | {ef['ce']['mean']:.10g} | {ef['ce']['wins']}/3 | {ef['mrr']['mean']:.10g} | {ef['hits10']['mean']:.10g} | {ef['auc']['mean']:.10g} |")
            mrr=d['effects']['MERI_vs_RAW']['mrr']['mean'];ranking[ds]='RANKING_IMPROVED' if mrr>0 else ('RANKING_DEGRADED' if mrr<0 else 'RANKING_NEUTRAL')
        table='\n'.join(lines);md('10_RANKING_ANALYSIS.md','# Ranking\n\n'+table+'\n\n'+json.dumps(ranking,indent=2))
        first={ds:d['effects']['MERI_vs_FIRST'] for ds,d in data['datasets'].items()};md('06_FIRST_ORDER_CONTROL.md',(ART/'06_FIRST_ORDER_CONTROL.md').read_text()+'\n\n## Paired FIRST comparison\n\n'+json.dumps(first,indent=2)+'\n\nMixed-effect necessity requires positive mean CE gain over FIRST on both datasets.')
        report=['# V22 MERI Mixed Endpoint-Role Interaction','',f'FINAL_STATUS: {status}',f'REASON: {reason}','',table,'','## Algebra, sources, determinism','',json.dumps(read(ART/'01_ALGEBRAIC_SANITY.json'),indent=2),json.dumps(read(ART/'02_SOURCE_CONSISTENCY.json'),indent=2),json.dumps(read(ART/'03_DETERMINISM_PRECHECK.json'),indent=2),'','## Complete validation metrics and gates','',json.dumps({ds:{'metrics':d['metrics'],'gates':d['gates'],'parameters':{a:d['seed_results'][0]['arms'][a]['trainable_parameters'] for a in ARMS}} for ds,d in data['datasets'].items()},indent=2),'','## Magnitude, correspondence and nonredundancy','',json.dumps(diag,indent=2),'','FIRST is the fixed symmetric average of the two first-order differences, not their separate concatenation. DUP repeats full/full relation pooling using the SAME phi. SHUFFLE power excludes right-context singleton sets; multiset and RAW hash preservation is audited with the same model weights. All magnitude population comparisons are descriptive, not tuned. No causal or novelty claim.','TEST_OPENED: NO','PHASE_B: NOT_RUN','INNOVATION_1_MODIFIED: NO','HISTORICAL_RESULTS_MODIFIED: NO']
        md('FINAL_REPORT.md','\n'.join(report))
    else:
        for name in ('04_PHASE_A_RESULTS.json','05_PAIRED_CONTRASTS.json','07_SHUFFLE_CONTROL_AUDIT.json','08_MERI_DIAGNOSTICS.json','09_NONREDUNDANCY_PROBES.json'):artifact(name,{'state':'NOT_RUN','reason':reason})
        md('FINAL_REPORT.md',f'# MERI V22\n\nFINAL_STATUS: {status}\n\n{reason}\n\nTEST_OPENED: NO')
    md('11_DECISION.md',f'# Decision\n\n{status}\n\n{reason}')
    state={'state':'COMPLETE','final_status':status,'reason':reason,'ended_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
    handoff=['STATUS: EXECUTED','TASK: MERI_V22_MIXED_ENDPOINT_ROLE_VALIDATION','WORKSPACE: DCDLP-main',f'CANONICAL_PROTOCOL: {PROTO}',f'FINAL_STATUS: {status}',f'REASON: {reason}','',table]
    if diag:handoff+=['',json.dumps({ds:[{'seed':r['seed'],'MERI_FROM_RAW_R2':r['MERI_from_RAW']['R2'],'MERI_FROM_Z_R2':r['MERI_from_Z']['R2']} for r in rr] for ds,rr in diag.items()},indent=2)]
    handoff+=['TEST_OPENED: NO','INNOVATION_1_MODIFIED: NO','HISTORICAL_RESULTS_MODIFIED: NO','PRIMARY_ARTIFACT: result/innovation2/MERI_V22/FINAL_REPORT.md','NEXT_EXPECTED_STEP: Return evidence to user and STOP. No test, rescue tuning or autonomous continuation.'];md('C2C_HANDOFF.md','\n'.join(handoff));print('MERI_COMPLETE',status,flush=True)

def supervise():
    try:
        preflight();batch([('run','D','pubmed',0,a,r) for a in ('MERI','FIRST','SHUFFLE') for r in (1,2)],'DETERMINISM_PRECHECK')
        records=[]
        for arm in ('MERI','FIRST','SHUFFLE'):
            rr=[read(job('D','pubmed',0,arm,r)/'result.json') for r in (1,2)];keys=('checkpoint_sha256','score_vector_sha256','training_trajectory_sha256','history','training_trace','optimizer_steps');checks={k:rr[0][k]==rr[1][k] for k in keys}
            records.append({'arm':arm,'pass':all(checks.values()),'checks':checks,'checkpoint_hashes':[r['checkpoint_sha256'] for r in rr],'score_hashes':[r['score_vector_sha256'] for r in rr],'trajectory_hashes':[r['training_trajectory_sha256'] for r in rr]})
        e.cache_check();ok=all(r['pass'] for r in records);artifact('03_DETERMINISM_PRECHECK.json',{'state':'PASS' if ok else 'FAIL','pairs':records,'canonical_caches_unchanged':True,'candidate_order_and_negatives_unchanged':True,'test_opened':False})
        if not ok:finalize(status='DETERMINISTIC_PROTOCOL_FAILURE',reason='Duplicate checkpoint/score/trajectory/history gate failed.');return
        for arm in ('MERI','FIRST','SHUFFLE'):
            dest=job('A','pubmed',0,arm);dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():dest.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS if not(ds=='pubmed' and s==0 and a in ('MERI','FIRST','SHUFFLE'))],'PHASE_A')
        data=summarize();batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'MERI_DIAGNOSTICS',workers=3);finalize(data)
    except BaseException as error:
        for p in e.CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        err={'state':'EXECUTION_FAILED','error':repr(error),'traceback':traceback.format_exc(),'ended_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',err);artifact('RUN_STATUS.json',err);artifact('ERROR.json',err);print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='preflight':preflight()
    elif cmd=='supervise':supervise()
    elif cmd=='run':e.run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif cmd=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    else:raise ValueError(cmd)
