"""V24: exact shared-slot algebra versus nonlinear-path/depth mechanisms."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1')
import sys,json,hashlib,time,subprocess,traceback,signal,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent;OUT=ROOT/'RELREUSE_V24';ART=REPO/'result/innovation2/RELREUSE_V24'
sys.path.insert(0,str(ROOT/'GSIR_V23/scripts'));import gsir23 as g
e,v,np,torch,nn,agg=g.e,g.v,g.np,g.torch,g.nn,g.agg
e.OUT=OUT;e.ART=ART
read,write,sha,artifact,md,sandbox,job=e.read,e.write,e.sha,e.artifact,e.md,e.sandbox,e.job
PROTO=e.PROTO;ARMS=('Z','RAW','SHARED','SUM','COLLAPSED','DECWIDE','TWO','TIED','DEPTH','NOREUSE')

class SumFirst(nn.Module):
    def __init__(self,original):
        super().__init__();w=original.weight.detach()
        self.weight_z=nn.Parameter(w[:,:321].clone());self.weight_a=nn.Parameter(w[:,321:353].clone());self.weight_b=nn.Parameter(w[:,353:].clone());self.bias=nn.Parameter(original.bias.detach().clone())
    def forward(self,x):
        return torch.nn.functional.linear(x,torch.cat((self.weight_z,self.weight_a+self.weight_b),1),self.bias)
    def effective(self):return self.weight_a+self.weight_b

class ReuseDecoder(nn.Module):
    def __init__(self,arm,seed):
        super().__init__();self.arm=arm;self.last={}
        with torch.random.fork_rng():
            torch.manual_seed(24002+seed)
            if arm=='DECWIDE':self.first=nn.Linear(353,69);self.second=nn.Linear(69,34);self.final=nn.Linear(34,1)
            elif arm in ('TWO','TIED'):self.first=nn.Linear(329,74);self.second=nn.Linear(74,28);self.final=nn.Linear(28,1)
            else:self.first=nn.Linear(353,67);self.second=nn.Linear(99,31);self.final=nn.Linear(31,1)
        if arm in ('TWO','TIED'):
            with torch.random.fork_rng():torch.manual_seed(24003+seed);self.path1=nn.Linear(32,4)
            if arm=='TWO':
                with torch.random.fork_rng():torch.manual_seed(24004+seed);self.path2=nn.Linear(32,4)
        nn.init.zeros_(self.final.weight);nn.init.zeros_(self.final.bias)
    def forward(self,x):
        z,r=x[:,:321],x[:,321:];self.last={}
        if self.arm in ('TWO','TIED'):
            p1=torch.relu(self.path1(r));p2=torch.relu((self.path2 if self.arm=='TWO' else self.path1)(r));x=torch.cat((z,p1,p2),1);self.last={'p1':p1,'p2':p2}
        pre=self.first(x);h1=torch.relu(pre)
        if self.arm in ('DEPTH','NOREUSE'):
            reinject=r if self.arm=='DEPTH' else h1[:,:32];pre2=self.second(torch.cat((h1,reinject),1));before=torch.nn.functional.linear(h1,self.second.weight[:,:67],self.second.bias)
            first_r=torch.nn.functional.linear(r,self.first.weight[:,321:],None);second_r=torch.nn.functional.linear(reinject,self.second.weight[:,67:],None)
            self.last.update(first_R=first_r,second_R=second_r,before=torch.relu(before),after=torch.relu(pre2))
        else:pre2=self.second(h1)
        self.last.update(preactivation=pre,h1=h1);return self.final(torch.relu(pre2))

class Predictor(v.RelationPredictor):
    def __init__(self,structure,seed,arm,mean,std):
        super().__init__(structure,seed,'A2',mean,std);self.arm=arm;agg.install(self)
        base=self.decoder
        if arm in ('SUM','COLLAPSED'):
            # Exact historical first-layer distribution and mapping, unchanged tail.
            with torch.random.fork_rng():torch.manual_seed(21002+seed);historical=nn.Linear(385,64)
            with torch.no_grad():historical.weight[:,:353].copy_(base[0].weight);historical.bias.copy_(base[0].bias)
            if arm=='SUM':first=SumFirst(historical)
            else:
                first=copy.deepcopy(base[0])
                with torch.no_grad():first.weight[:,321:].copy_(historical.weight[:,321:353]+historical.weight[:,353:])
            self.decoder=nn.Sequential(first,*[copy.deepcopy(base[i]) for i in range(1,5)])
        else:self.decoder=ReuseDecoder(arm,seed)

def make_net(ds,seed,arm,phase,structure=None):
    if arm=='DUP':return g.m.make_net(ds,seed,'DUP',phase,structure)
    if arm in ARMS[3:]:
        stats=read(v.cache(ds,seed)/'normalization.json');return Predictor(structure or v.Structure(v.cache(ds)/'structure.npz'),seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda')
    return agg.install(e.ORIGINAL_MAKE(ds,seed,arm,phase,structure))
v.make_net=make_net

def shared_mapped_decoder(shared):
    d=shared.decoder;return nn.Sequential(SumFirst(d[0]),*[copy.deepcopy(d[i]) for i in range(1,5)])
def map_sum_state(decoder):
    state={k:t for k,t in decoder.state_dict().items() if not k.startswith('0.')};a=decoder[0]
    state['0.weight']=torch.cat((a.weight_z,a.weight_a,a.weight_b),1);state['0.bias']=a.bias
    return state
def mapped_state(net):
    if isinstance(net.decoder,nn.Sequential) and isinstance(net.decoder[0],SumFirst):
        return {**{k:t for k,t in net.state_dict().items() if not k.startswith('decoder.')},**{'decoder.'+k:t for k,t in map_sum_state(net.decoder).items()}}
    return net.state_dict()
def effective(net):
    d=net.decoder
    if isinstance(d,nn.Sequential):
        if isinstance(d[0],SumFirst):return d[0].effective()
        if d[0].in_features==385:return d[0].weight[:,321:353]+d[0].weight[:,353:]
        return d[0].weight[:,321:]
    if d.arm in ('TWO','TIED'):return d.path1.weight
    return d.first.weight[:,321:]

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
        st={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(q),'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',st);artifact('RUN_STATUS.json',st)
        if active:time.sleep(3)

def differences(a,b):
    a=np.asarray(a).reshape(-1);b=np.asarray(b).reshape(-1);return {'mean_abs':float(np.abs(a-b).mean()),'max_abs':float(np.abs(a-b).max()),'pearson':float(np.corrcoef(a,b)[0,1]) if a.std()>1e-12 and b.std()>1e-12 else None,'left_std':float(a.std()),'right_std':float(b.std())}

def equivalence(ds):
    source=v.cache(ds,0);pp=torch.tensor(np.load(source/'epoch_1_pairs.npy').reshape(-1,2)[:128],device='cuda');bb=torch.tensor(np.load(source/'epoch_1.npy').reshape(-1,257)[:128],device='cuda')
    shared=make_net(ds,0,'DUP','A')
    with torch.no_grad():z,r=shared.representation(pp,bb,True)
    tests=[]
    for dtype,tol in ((torch.float64,1e-9),(torch.float32,1e-4)):
        left=copy.deepcopy(shared.decoder).to(dtype);right=shared_mapped_decoder(shared).to(dtype);zz,rr=z.to(dtype),r.to(dtype)
        # Nondegenerate test head prevents the zero initialization from hiding errors.
        with torch.no_grad():
            w=torch.linspace(-.05,.05,32,device='cuda',dtype=dtype)[None,:];left[4].weight.copy_(w);right[4].weight.copy_(w)
        opt1=torch.optim.Adam(left.parameters(),lr=v.b.NCFG[ds]['prelr'],weight_decay=0);opt2=torch.optim.Adam(right.parameters(),lr=v.b.NCFG[ds]['prelr'],weight_decay=0)
        label=(torch.arange(len(zz),device='cuda')%2).to(dtype);steps=[]
        for step in range(11):
            opt1.zero_grad(set_to_none=True);opt2.zero_grad(set_to_none=True)
            pre1=left[0](torch.cat((zz,rr,rr),1));pre2=right[0](torch.cat((zz,rr),1));a=left(torch.cat((zz,rr,rr),1)).flatten();b=right(torch.cat((zz,rr),1)).flatten()
            loss1=torch.nn.functional.binary_cross_entropy_with_logits(a,label);loss2=torch.nn.functional.binary_cross_entropy_with_logits(b,label);loss1.backward();loss2.backward()
            wa=left[0].weight;wz=right[0].weight_z;wr=right[0].weight_a;ws=right[0].weight_b
            grad2=torch.cat((wz.grad,wr.grad,ws.grad),1)
            checks={'preactivation':torch.allclose(pre1,pre2,atol=tol,rtol=tol),'logits':torch.allclose(a,b,atol=tol,rtol=tol),'loss':torch.allclose(loss1,loss2,atol=tol,rtol=tol),'mapped_gradient':torch.allclose(wa.grad,grad2,atol=tol,rtol=tol),'effective_sum':torch.allclose(wa[:,321:353]+wa[:,353:],wr+ws,atol=tol,rtol=tol)}
            corresponding=[(left[0].bias,right[0].bias)]+[(getattr(left[i],k),getattr(right[i],k)) for i in (2,4) for k in ('weight','bias')]
            checks['all_gradients']=all(torch.allclose(p.grad,q.grad,atol=tol,rtol=tol) for p,q in corresponding)
            checks['all_mapped_parameters']=torch.allclose(wa,torch.cat((wz,wr,ws),1),atol=tol,rtol=tol) and all(torch.allclose(p,q,atol=tol,rtol=tol) for p,q in corresponding)
            all_grad_error=max([float((wa.grad-grad2).abs().max())]+[float((p.grad-q.grad).abs().max()) for p,q in corresponding])
            moment_error=0.
            if step:
                for key in ('exp_avg','exp_avg_sq'):
                    first=opt1.state[wa][key];second=torch.cat([opt2.state[p][key] for p in (wz,wr,ws)],1);moment_error=max(moment_error,float((first-second).abs().max()));checks[key]=torch.allclose(first,second,atol=tol,rtol=tol)
                    for p,q in corresponding:
                        first,second=opt1.state[p][key],opt2.state[q][key];moment_error=max(moment_error,float((first-second).abs().max()));checks[key]=checks[key] and torch.allclose(first,second,atol=tol,rtol=tol)
            steps.append({'step':step,'pass':all(checks.values()),'checks':checks,'logit_max_error':float((a-b).abs().max()),'loss_error':float((loss1-loss2).abs()),'gradient_max_error':float((wa.grad-grad2).abs().max()),'effective_sum_max_error':float((wa[:,321:353]+wa[:,353:]-wr-ws).abs().max()),'Adam_moment_max_error':moment_error,'logits_bit_identical':torch.equal(a,b)})
            steps[-1]['all_gradient_max_error']=all_grad_error
            steps[-1]['all_mapped_parameter_max_error']=max([float((wa-torch.cat((wz,wr,ws),1)).abs().max())]+[float((p-q).abs().max()) for p,q in corresponding])
            if step<10:opt1.step();opt2.step()
        tests.append({'dtype':str(dtype),'tolerance_abs_relative':tol,'pass':all(x['pass'] for x in steps),'steps':steps})
    result={'state':'PASS' if all(t['pass'] for t in tests) else 'FAIL','tests':tests,'mapped_batch':'canonical frozen initialization Z/R,128 epoch1 training candidates','nondegenerate_head':'test-only identical linear ramp; training retains canonical zero head',
        'optimizer':'Adam canonical LR, weight_decay0, each tensor element has own moments; mapped state slices compared','real_arithmetic_equivalence':True,'float32_bit_identity_required_between_formulations':False,'duplicate_within_same_method_bit_identity_required':True}
    artifact('04_SUM_PARAM_EQUIVALENCE.json',result);assert result['state']=='PASS','V24_EQUIVALENCE_IMPLEMENTATION_ERROR'

@torch.no_grad()
def initial_diagnostic():
    data={};scale={}
    for ds in ('cora','pubmed'):
        pp=torch.tensor(np.load(v.cache(ds,0)/'valid_pairs.npy')[:128],device='cuda');bb=torch.tensor(np.load(v.cache(ds,0)/'valid_b.npy')[:128],device='cuda');logits={};stats={}
        for arm in ARMS[1:]:
            net=make_net(ds,0,e.MAP.get(arm,arm),'A');z,r=net.representation(pp,bb,True)
            if arm=='SHARED':score=net(pp,bb)[0];d=net.decoder;pre=d[0](torch.cat((z,r,r),1));contrib=torch.nn.functional.linear(r,d[0].weight[:,321:353]+d[0].weight[:,353:],None)
            else:
                score=net(pp,bb)[0];d=net.decoder
                if isinstance(d,nn.Sequential):pre=d[0](torch.cat((z,r),1));contrib=torch.nn.functional.linear(r,effective(net),None)
                else:
                    pre=d.last['preactivation'];contrib=d.last.get('first_R')
                    if d.arm=='DECWIDE':contrib=torch.nn.functional.linear(r,d.first.weight[:,321:],None)
                    elif d.arm in ('TWO','TIED'):contrib=torch.nn.functional.linear(torch.cat((d.last['p1'],d.last['p2']),1),d.first.weight[:,321:],None)
            logits[arm]=score.cpu().numpy();stats[arm]={'logit_mean':float(score.mean()),'logit_std':float(score.std()),'preactivation_mean':float(pre.mean()),'preactivation_std':float(pre.std()),'relation_contribution_norm':e.distribution(torch.linalg.vector_norm(contrib,dim=1).cpu().numpy()) if contrib is not None else None}
        pairs={f'SHARED_vs_{a}':differences(logits['SHARED'],logits[a]) for a in ('RAW','SUM','COLLAPSED','TWO','DEPTH')};data[ds]=pairs;scale[ds]=stats
    artifact('06_INITIAL_FUNCTION_DIAGNOSTIC.json',{'state':'COMPLETE','datasets':data,'note':'All zero final score heads return frozen NCNC baseline at initialization, even for non-equivalent decoders; preactivation and nondegenerate equivalence tests are essential.'})
    artifact('11_INITIALIZATION_SCALE_AUDIT.json',{'state':'COMPLETE','datasets':scale,'no_initialization_retuning':True})

def preflight():
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);v.OUT=ROOT/'CHRI_V18_1';v.check_frozen();assert REPO.name in ('DCDLP-main','lchr_v2')
    assert read(ART/'01_DECODER_SOURCE_AUDIT.json')['decoder_class']=='CLASS_A_LINEAR_COLLAPSIBLE'
    previous=read(REPO/'result/innovation2/GSIR_V23/SOURCE_HASHES.json');files=dict(previous['files'])
    for p,h in files.items():assert sha(REPO/p)==h,'HISTORICAL_SOURCE_CHANGED '+p
    base=REPO/'result/innovation2/GSIR_V23';assert 'GSIR_REJECTED_NO_GAIN' in (base/'FINAL_REPORT.md').read_text();files.update({str(p.relative_to(REPO)):sha(p) for p in base.glob('*') if p.is_file() and p.suffix in ('.json','.md')})
    for p in [ROOT/'GSIR_V23/scripts/gsir23.py',*list((OUT/'scripts').glob('*.py')),*[ART/n for n in ('00_PROTOCOL.md','01_DECODER_SOURCE_AUDIT.md','01_DECODER_SOURCE_AUDIT.json','02_EQUIVALENCE_DERIVATION.md')]]:files[str(p.relative_to(REPO))]=sha(p)
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','files':files,'caches':previous['caches'],'canonical_protocol':PROTO});e.cache_check()
    counts={a:sum(p.numel() for p in make_net('pubmed',0,e.MAP.get(a,a),'A').parameters() if p.requires_grad) for a in ARMS};assert counts=={'Z':26385,'RAW':28481,'SHARED':30529,'SUM':30529,'COLLAPSED':28481,'DECWIDE':30553,'TWO':30525,'TIED':30393,'DEPTH':30562,'NOREUSE':30562}
    assert all(abs(counts[a]-30529)/30529<=.005 for a in ('SUM','DECWIDE','TWO','TIED','DEPTH','NOREUSE'))
    artifact('05_PARAMETER_AUDIT.json',{'state':'PASS','counts':counts,'relative_difference_vs_SHARED':{a:(n-30529)/30529 for a,n in counts.items()},'TIED_exception':'Weight sharing removes132 path parameters; same downstream graph retained, no dummy weights; within0.5%.','COLLAPSED':'Intentional2048 parameter reduction, not matched.'})
    equivalence('pubmed');initial_diagnostic()
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'workspace':'DCDLP-main','canonical_protocol':PROTO,'decoder_class':'CLASS_A_LINEAR_COLLAPSIBLE','SUM_applicable':True,'precheck':{'dataset':'pubmed','seed':0,'arms':['SHARED','SUM','TWO','DEPTH'],'replicates':2,'epochs':5},'phase_A':{'datasets':['cora','pubmed'],'seeds':[0,1,2],'arms':list(ARMS),'epochs':5},'counts':counts,'optimizer':'canonical Adam, weight_decay0, unchanged loss/LR/batch/microbatch','test_opened':False,'innovation1_modified':False,'historical_results_modified':False,'workers':6,'threads_per_worker':2})
    for n in ('03_SHARED_DUP_REPRODUCTION.json','07_DETERMINISM_PRECHECK.json','08_PHASE_A_RESULTS.json','09_PAIRED_CONTRASTS.json','10_OPTIMIZATION_DYNAMICS.json','12_MULTIPATH_DIAGNOSTICS.json','13_DEPTH_REUSE_DIAGNOSTICS.json'):artifact(n,{'state':'NOT_RUN','reason':'Prerequisite pending.'})
    for n in ('14_RANKING_ANALYSIS.md','15_MECHANISM_DECISION.md','FINAL_REPORT.md'):md(n,'# V24\n\nPENDING')
    print('V24_PREFLIGHT_PASS',counts,flush=True)

def run(phase,ds,seed,arm,rep):
    v.OUT=sandbox(phase,ds,seed,arm,rep);e.frozen_check();actual=e.MAP.get(arm,arm);trajectory=hashlib.sha256();mapped_trajectory=hashlib.sha256();stats=[];steps=[0];holder={};original_make=v.make_net;stepfn=torch.optim.Adam.step
    def capture(*args,**kwargs):
        net=original_make(*args,**kwargs);holder['net']=net;return net
    v.make_net=capture
    def logged(opt,*args,**kwargs):
        net=holder['net'];parameters=[p for p in net.decoder.parameters() if p.requires_grad];before=[p.detach().clone() for p in parameters];gradnorm=sum(float(p.grad.detach().square().sum()) for p in parameters if p.grad is not None)**.5
        out=stepfn(opt,*args,**kwargs);steps[0]+=1;trajectory.update(str(steps[0]).encode())
        for group in opt.param_groups:
            for p in group['params']:trajectory.update(p.detach().cpu().contiguous().numpy().tobytes())
        mapped_trajectory.update(str(steps[0]).encode());mapped_trajectory.update(g.statehash(mapped_state(net)).encode())
        update=sum(float((p.detach()-b).square().sum()) for p,b in zip(parameters,before))**.5
        stats.append({'step':steps[0],'decoder_gradient_norm':gradnorm,'decoder_parameter_norm':sum(float(p.detach().square().sum()) for p in parameters)**.5,'effective_relation_transform_norm':float(effective(net).detach().norm()),'decoder_update_norm':update})
        if steps[0]==1:print('FIRST_OPTIMIZER_STEP_OK',phase,ds,seed,arm,rep,flush=True)
        return out
    torch.optim.Adam.step=logged;print('TRAIN_START',phase,ds,seed,arm,rep,flush=True);v.run(phase,ds,seed,actual,5)
    dest=v.job(phase,ds,seed,actual);row=read(dest/'result.json');assert steps[0]>0;row.update(variant=arm,replicate=rep,canonical_protocol=PROTO,score_vector_sha256=e.score_hash(dest/'valid_epoch5_scores.npz'),optimizer_steps=steps[0],training_trajectory_sha256=trajectory.hexdigest())
    nsteps=len(stats)//5;assert nsteps*5==len(stats)
    dynamics=[]
    for epoch,h in enumerate(row['history'],1):
        entries=stats[(epoch-1)*nsteps:epoch*nsteps];dynamics.append({'epoch':epoch,'train_CE':h['loss']/2,'validation_CE':h['validation']['ce'],**{k:float(np.mean([d[k] for d in entries])) for k in entries[0] if k!='step'}})
    write(dest/'optimization_dynamics.json',{'state':'COMPLETE','epochs':dynamics,'per_step':stats,'definition':'Decoder-only gradient/parameter/update norms; effectiveR transform norm after each Adam step; logged without altering optimizer.'})
    if arm=='SUM':row['mapped_shared_state_sha256']=g.statehash({**{k:t for k,t in holder['net'].state_dict().items() if not k.startswith('decoder.')},**{'decoder.'+k:t for k,t in map_sum_state(holder['net'].decoder).items()}})
    else:row['state_tensor_sha256']=g.statehash(holder['net'].state_dict())
    row['mapped_training_trajectory_sha256']=mapped_trajectory.hexdigest()
    write(dest/'result.json',row);print('V24_JOB_COMPLETE',phase,ds,seed,arm,rep,flush=True)

def summarize():
    data={'state':'COMPLETE','datasets':{},'test_opened':False};repro=[]
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{a:read(job('A',ds,s,a)/'result.json') for a in ARMS}} for s in range(3)]
        for row in rows:
            r=g.reproduce_shared('A',ds,row['seed']);repro.append(r);assert r['pass'],'V24_HISTORICAL_REPRODUCTION_FAILURE'
            assert all(r['training_trace']==row['arms']['RAW']['training_trace'] for r in row['arms'].values())
        comparisons=[('SHARED','RAW'),('SUM','SHARED'),('COLLAPSED','SHARED'),('DECWIDE','SHARED'),('TWO','SHARED'),('TWO','DECWIDE'),('TWO','RAW'),('TWO','TIED'),('DEPTH','SHARED'),('DEPTH','DECWIDE'),('DEPTH','RAW'),('DEPTH','NOREUSE')]
        effects={f'{a}_vs_{b}':v.comparison(rows,a,b) for a,b in comparisons}
        gates={a:{'SHARED_mean':effects[f'{a}_vs_SHARED']['ce']['mean']>0,'SHARED_wins':effects[f'{a}_vs_SHARED']['ce']['wins']>=2,'DECWIDE':effects[f'{a}_vs_DECWIDE']['ce']['mean']>0,'RAW':effects[f'{a}_vs_RAW']['ce']['mean']>0} for a in ('TWO','DEPTH')};gates['DEPTH']['NOREUSE']=effects['DEPTH_vs_NOREUSE']['ce']['mean']>0
        sumagreement=[]
        for row in rows:
            a,b=row['arms']['SUM'],row['arms']['SHARED'];sumagreement.append({'seed':row['seed'],'mapped_weights_bit_identical':a['mapped_shared_state_sha256']==b['state_tensor_sha256'],'scores_bit_identical':a['score_vector_sha256']==b['score_vector_sha256'],'raw_trajectory_hash_equal':a['training_trajectory_sha256']==b['training_trajectory_sha256'],'metrics_equal':a['validation']==b['validation'],'delta_CE':b['validation']['ce']-a['validation']['ce'],'delta_MRR':a['validation']['mrr']-b['validation']['mrr']})
            aa=np.load(job('A',ds,row['seed'],'SUM')/'valid_epoch5_scores.npz');bb=np.load(job('A',ds,row['seed'],'SHARED')/'valid_epoch5_scores.npz')
            sumagreement[-1]['scores_numeric_difference']={k:differences(aa[k],bb[k]) for k in aa.files}
            sumagreement[-1]['mapped_trajectory_bit_identical']=a['mapped_training_trajectory_sha256']==b['mapped_training_trajectory_sha256']
        data['datasets'][ds]={'seed_results':rows,'effects':effects,'gates':gates,'sum_shared_agreement':sumagreement,'metrics':{a:{k:v.stat([r['arms'][a]['validation'][k] for r in rows]) for k in v.METRICS} for a in ARMS}}
    artifact('03_SHARED_DUP_REPRODUCTION.json',{'state':'PASS','datasets':repro});artifact('08_PHASE_A_RESULTS.json',data);artifact('09_PAIRED_CONTRASTS.json',{'state':'COMPLETE','datasets':{ds:d['effects'] for ds,d in data['datasets'].items()}})
    dynamics={ds:{a:[read(job('A',ds,s,a)/'optimization_dynamics.json')['epochs'] for s in range(3)] for a in ('RAW','SHARED','SUM','COLLAPSED','DECWIDE')} for ds in ('cora','pubmed')};artifact('10_OPTIMIZATION_DYNAMICS.json',{'state':'COMPLETE','datasets':dynamics,'optimizer_semantics':'Adam elementwise moments; weight_decay0, same groups/LR. SUM separately parameterized blocks map to SHARED columns; COLLAPSED receives one effective gradient/update versus two for redundant blocks. Floating kernels and gradients can change exact trajectories.'})
    return data

@torch.no_grad()
def diagnose(ds,seed):
    source=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}';result={'state':'COMPLETE','dataset':ds,'seed':seed,'test_opened':False};arrays={}
    for arm in ('TWO','TIED','DEPTH'):
        v.OUT=sandbox('A',ds,seed,arm,1);e.frozen_check();net=v.load_net('A',ds,seed,arm);arrays[arm]={};diagnostics={}
        for split in ('train','validation'):
            pairs=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy')).reshape(-1,2);features=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r').reshape(-1,257);parts={}
            for st in range(0,len(pairs),256):
                pp=torch.tensor(pairs[st:st+256],device='cuda',dtype=torch.long);bb=torch.tensor(np.array(features[st:st+256]),device='cuda');net(pp,bb)
                for k,t in net.decoder.last.items():parts.setdefault(k,[]).append(t.cpu().numpy())
                net.decoder.last={}
            a={k:np.concatenate(x) for k,x in parts.items()};arrays[arm][split]=a
            if arm in ('TWO','TIED'):
                p1,p2=a['p1'],a['p2'];diagnostics[split]={'cosine':e.distribution(e.cosine(p1,p2)),'norm_ratio_p2_p1':e.distribution(np.linalg.norm(p2,axis=1)/np.maximum(np.linalg.norm(p1,axis=1),1e-12)),'zero_fraction_p1':float((p1==0).mean()),'zero_fraction_p2':float((p2==0).mean()),'candidate_correlation':g.covariance(p1,p2),'paths_identical':bool(np.array_equal(p1,p2))}
            else:
                first=np.linalg.norm(a['first_R'],axis=1);second=np.linalg.norm(a['second_R'],axis=1);change=np.linalg.norm(a['after']-a['before'],axis=1);cos=e.cosine(a['before'],a['after']);diagnostics[split]={'first_R_norm':e.distribution(first),'second_R_norm':e.distribution(second),'hidden_change':e.distribution(change),'before_after_cosine':e.distribution(cos)}
                if split=='validation':
                    npos=len(e.sealed(ds)['valid_pos']);diagnostics[split]['descriptive_populations']={name:{'first_R_norm':e.distribution(first[ix]),'second_R_norm':e.distribution(second[ix]),'hidden_change':e.distribution(change[ix])} for name,ix in (('positive',slice(0,npos)),('negative',slice(npos,None)))}
        if arm in ('TWO','TIED'):
            t,q=arrays[arm]['train'],arrays[arm]['validation'];diagnostics['p2_from_p1_probe']=e.probe(t['p1'],t['p2'],q['p1'],q['p2'])
        result[arm]=diagnostics
    write(OUT/'diagnostics'/ds/f'seed_{seed}.json',result);print('V24_DIAGNOSTICS_COMPLETE',ds,seed,flush=True)

def finalize(data=None,status=None,reason=None):
    v.OUT=ROOT/'CHRI_V18_1';e.frozen_check();e.cache_check();survivor='NONE';table=''
    if data:
        diag={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')}
        artifact('12_MULTIPATH_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':{ds:[{'seed':r['seed'],'TWO':r['TWO'],'TIED':r['TIED']} for r in rr] for ds,rr in diag.items()},'probes_train_only':True});artifact('13_DEPTH_REUSE_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':{ds:[{'seed':r['seed'],'DEPTH':r['DEPTH']} for r in rr] for ds,rr in diag.items()},'causal_claim':False})
        passed={a:all(all(d['gates'][a].values()) for d in data['datasets'].values()) for a in ('TWO','DEPTH')};generic=all(d['effects']['DECWIDE_vs_SHARED']['ce']['mean']>=0 for d in data['datasets'].values())
        bitexact=all(x['mapped_weights_bit_identical'] and x['mapped_trajectory_bit_identical'] and x['scores_bit_identical'] and x['metrics_equal'] for d in data['datasets'].values() for x in d['sum_shared_agreement'])
        selection={a:{'worst_dataset_mean_delta_CE':min(d['effects'][f'{a}_vs_SHARED']['ce']['mean'] for d in data['datasets'].values()),'both_dataset_mean_delta_CE':float(np.mean([d['effects'][f'{a}_vs_SHARED']['ce']['mean'] for d in data['datasets'].values()])),'both_dataset_mean_delta_MRR':float(np.mean([d['effects'][f'{a}_vs_SHARED']['mrr']['mean'] for d in data['datasets'].values()])),'parameter_count':read(ART/'05_PARAMETER_AUDIT.json')['counts'][a]} for a in ('TWO','DEPTH')}
        if passed['TWO'] and passed['DEPTH']:
            winner=max(selection,key=lambda a:(selection[a]['worst_dataset_mean_delta_CE'],selection[a]['both_dataset_mean_delta_CE'],selection[a]['both_dataset_mean_delta_MRR'],-selection[a]['parameter_count']));status='RELATION_REUSE_STRUCTURAL_SIGNAL';survivor='BOTH';reason='Both mechanisms pass all preregistered CE gates; select '+winner+' by worst-dataset CE, mean CE, mean MRR, then fewer parameters. No combined model.'
        elif passed['TWO']:status='MULTIPATH_RELATION_REUSE_PROMISING';survivor='MULTIPATH';reason='TWO passes SHARED win/mean, generic capacity and RAW gates.'
        elif passed['DEPTH']:status='MULTISTAGE_RELATION_REUSE_PROMISING';survivor='MULTISTAGE';reason='DEPTH passes SHARED win/mean, generic capacity, RAW and NOREUSE gates.'
        elif generic:status='GENERIC_DECODER_CAPACITY_EXPLANATION';reason='DECWIDE matches/beats SHARED on both datasets, no structural mechanism survives.'
        else:
            if bitexact:status='SHARED_DUP_PURE_REPARAMETERIZATION';reason='Mapped full-run weights, trajectories, scores and metrics are bit-identical to SUM; no structural mechanism survives.'
            else:status=None;reason='Evidence only, awaiting user classification as explicitly requested: algebraic equivalence passes but mapped float32 training trajectories differ, no structural mechanism survives, and generic capacity does not explain both datasets. No scientific status added to the original list.'
        lines=['| Dataset | Contrast | Mean DeltaCE | CE wins | Mean DeltaMRR |','|---|---|---:|---:|---:|']
        for ds,d in data['datasets'].items():
            for name,ef in d['effects'].items():lines.append(f"| {ds} | {name} | {ef['ce']['mean']:.10g} | {ef['ce']['wins']}/3 | {ef['mrr']['mean']:.10g} |")
        table='\n'.join(lines);md('14_RANKING_ANALYSIS.md','# Ranking\n\n'+table)
        mechanism={'decoder_class':'CLASS_A_LINEAR_COLLAPSIBLE','SUM_applicable':True,'mapped_preflight_numerical_equivalence':read(ART/'04_SUM_PARAM_EQUIVALENCE.json')['state'],'full_run_bit_identity':bitexact,'SUM_agreement':{ds:d['sum_shared_agreement'] for ds,d in data['datasets'].items()},'structural_gates':{ds:d['gates'] for ds,d in data['datasets'].items()},'generic_capacity_both_datasets':generic,'surviving_structure':survivor,'independent_paths_both_datasets':all(d['effects']['TWO_vs_TIED']['ce']['mean']>0 for d in data['datasets'].values()),'optimizer_dynamics_explanation':'SUPPORTED only if mapped full runs agree and SHARED beats COLLAPSED both; otherwise UNRESOLVED; algebraic redundancy alone is not dynamics identity','test_opened':False}
        artifact('MECHANISM_EVIDENCE.json',mechanism)
        mechanism['structural_selection']=selection;mechanism['preferred_structure']=winner if survivor=='BOTH' else survivor;mechanism['classification_pending_user']=status is None
        mechanism['overparameterization_effect']='SUPPORTED' if bitexact and all(d['effects']['COLLAPSED_vs_SHARED']['ce']['mean']<0 for d in data['datasets'].values()) else 'UNRESOLVED'
        mechanism['ranking_nonnegative_vs_SHARED']={a:all(d['effects'][f'{a}_vs_SHARED']['mrr']['mean']>=0 for d in data['datasets'].values()) for a in ('TWO','DEPTH')}
        artifact('MECHANISM_EVIDENCE.json',mechanism)
        report=['# V24 shared relation mechanism dissection','',f'FINAL_STATUS: {status}',f'REASON: {reason}',f'SURVIVING_STRUCTURE: {survivor}','',table,'','## Source and exact algebra','',(ART/'01_DECODER_SOURCE_AUDIT.md').read_text(),(ART/'02_EQUIVALENCE_DERIVATION.md').read_text(),'','## Equivalence, historical reproduction and determinism','',json.dumps(read(ART/'04_SUM_PARAM_EQUIVALENCE.json'),indent=2),json.dumps(read(ART/'03_SHARED_DUP_REPRODUCTION.json'),indent=2),json.dumps(read(ART/'07_DETERMINISM_PRECHECK.json'),indent=2),'','## Complete validation metrics','',json.dumps({ds:d['metrics'] for ds,d in data['datasets'].items()},indent=2),'','## Mechanism decision','',json.dumps(mechanism,indent=2),'','## Initial scale and matched capacity','',json.dumps(read(ART/'05_PARAMETER_AUDIT.json'),indent=2),json.dumps(read(ART/'11_INITIALIZATION_SCALE_AUDIT.json'),indent=2),'','## Path/depth diagnostics','',json.dumps(diag,indent=2),'','Per-epoch dynamics are in10_OPTIMIZATION_DYNAMICS.json. Logs, scores and checkpoints remain archived under executions. No information or new function family is introduced by linear duplicated slots. Numerical equivalence and optimizer-trajectory identity are explicitly separate. No Innovation2 promotion absent strict structural gates.','TEST_OPENED: NO','INNOVATION_1_MODIFIED: NO','HISTORICAL_RESULTS_MODIFIED: NO'];md('FINAL_REPORT.md','\n'.join(report));md('15_MECHANISM_DECISION.md',f'# Decision\n\n{status}\n\n{reason}\n\n'+json.dumps(mechanism,indent=2))
    else:md('FINAL_REPORT.md',f'# V24\n\nFINAL_STATUS: {status}\n\n{reason}\n\nTEST_OPENED: NO');md('15_MECHANISM_DECISION.md',reason)
    st={'state':'COMPLETE','final_status':status,'classification_pending_user':status is None,'reason':reason,'ended_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',st);artifact('RUN_STATUS.json',st);md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: RELREUSE_V24_SHARED_DUP_MECHANISM_DISSECTION\nCANONICAL_PROTOCOL: {PROTO}\nDECODER_CLASS: CLASS_A_LINEAR_COLLAPSIBLE\nFINAL_STATUS: {status}\nSURVIVING_STRUCTURE: {survivor}\nREASON: {reason}\n{table}\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO\nPRIMARY_ARTIFACT: result/innovation2/RELREUSE_V24/FINAL_REPORT.md\nNEXT: Return evidence and STOP. No novelty claim, rescue or test.'+ ('\n\n'+json.dumps(mechanism,indent=2) if data else ''));print('V24_COMPLETE',status,flush=True)

def supervise():
    try:
        preflight();batch([('run','D','pubmed',0,a,r) for a in ('SHARED','SUM','TWO','DEPTH') for r in (1,2)],'DETERMINISM_PRECHECK')
        records=[]
        for arm in ('SHARED','SUM','TWO','DEPTH'):
            rr=[read(job('D','pubmed',0,arm,r)/'result.json') for r in (1,2)];keys=('checkpoint_sha256','score_vector_sha256','training_trajectory_sha256','history','training_trace');checks={k:rr[0][k]==rr[1][k] for k in keys};records.append({'arm':arm,'pass':all(checks.values()),'checks':checks,'hashes':{k:[r[k] for r in rr] for k in keys[:3]}})
        e.cache_check();ok=all(r['pass'] for r in records);artifact('07_DETERMINISM_PRECHECK.json',{'state':'PASS' if ok else 'FAIL','pairs':records,'canonical_caches_negatives_candidates_unchanged':True,'test_opened':False})
        reproduction=g.reproduce_shared('D','pubmed',0);artifact('03_SHARED_DUP_REPRODUCTION.json',{'state':'PASS' if reproduction['pass'] else 'FAIL','precheck':reproduction})
        if not reproduction['pass']:finalize(status='V24_HISTORICAL_REPRODUCTION_FAILURE',reason='Historical SHARED spot reproduction failed.');return
        if not ok:finalize(status='DETERMINISTIC_PROTOCOL_FAILURE',reason='Independent duplicates failed.');return
        for arm in ('SHARED','SUM','TWO','DEPTH'):
            dest=job('A','pubmed',0,arm);dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():dest.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS if not(ds=='pubmed' and s==0 and a in ('SHARED','SUM','TWO','DEPTH'))],'PHASE_A')
        data=summarize();batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'MECHANISM_DIAGNOSTICS',workers=3);finalize(data)
    except BaseException as error:
        for p in e.CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        status='V24_HISTORICAL_REPRODUCTION_FAILURE' if 'V24_HISTORICAL_REPRODUCTION_FAILURE' in str(error) else ('TEST_SEAL_VIOLATION' if 'TEST_SEAL_VIOLATION' in str(error) else 'V24_EQUIVALENCE_IMPLEMENTATION_ERROR')
        err={'state':'EXECUTION_FAILED','final_status':status,'error':repr(error),'traceback':traceback.format_exc(),'ended_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',err);artifact('RUN_STATUS.json',err);artifact('ERROR.json',err);md('FINAL_REPORT.md','# V24 execution failure\n\n'+json.dumps(err,indent=2));print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='preflight':preflight()
    elif cmd=='supervise':supervise()
    elif cmd=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif cmd=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    else:raise ValueError(cmd)
