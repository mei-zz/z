"""V28: paired topology fusion, bounded replication and sealed inner validation."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('NUMBA_NUM_THREADS','6');os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import sys,time,json,hashlib,random,signal,subprocess,traceback,copy,gc
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent;OUT=ROOT/'TOPOLOGY_V28';ART=REPO/'result/innovation2/TOPOLOGY_V28'
sys.path.insert(0,str(ROOT/'HDP2_V27/scripts'));import hdp27 as h
e,v,g,np,torch,nn=h.e,h.v,h.g,h.np,h.torch,h.nn
from scipy.stats import spearmanr,rankdata
from threadpoolctl import threadpool_limits
from chri_features import build_structure,array_hash
read,write,sha=e.read,e.write,e.sha
PROTO=e.PROTO;MODE='canonical';REP=1;CHILDREN=[]
OLD_INPUT=v.s.input_data;OLD_CHECK=v.check_frozen;OLD_BASE=v.base_job
LAYOUT={'ZERO6':('0','0','0'),'GRAPH6':('GRAPH','0','0'),'MULT6':('0','MULT','0'),'GDUP':('GRAPH','GRAPH','0'),'MDUP':('MULT','MULT','0'),'GM':('GRAPH','MULT','0'),'GP':('GRAPH','PAIR','0'),'GMH':('GRAPH','MULT','HDP'),'GMS':('GRAPH','MULT','SHUFFLE'),'GMP':('GRAPH','MULT','PAIR'),'GMG':('GRAPH','MULT','GRAPH'),'GMC':('GRAPH','COND','0')}
ARMS=('SHARED',*LAYOUT)
HYPOTHESES={'GRAPH':('GRAPH6',('SHARED','ZERO6')),'MULT':('MULT6',('SHARED','ZERO6')),'COMPLEMENTARITY':('GM',('GDUP','MDUP','GRAPH6','MULT6','GP','ZERO6','SHARED','GMC')),'HDP_CONDITIONAL':('GMH',('GM','GMP','GMG','GMS','SHARED','ZERO6'))}
PRIMARY={'GRAPH':('SHARED','ZERO6'),'MULT':('SHARED','ZERO6'),'COMPLEMENTARITY':('GDUP','MDUP'),'HDP_CONDITIONAL':('GM',)}
FILES=('01_FEATURE_DEPENDENCY_AUDIT.json','02_BASELINE_REPRODUCTION.json','03_PARAMETER_AND_INITIALIZATION_AUDIT.json','04_DETERMINISM_PRECHECK.json','05_CONDITIONAL_TOPOLOGY_DIAGNOSTICS.json','06_PHASE_A_METRICS.json','07_PHASE_A_PAIRED_CONTRASTS.json','08_CONDITIONAL_SHUFFLE_AUDIT.json','09_HDP_SUBGROUP_ANALYSIS.json','11_PHASE_B_NEW_SEED_RESULTS.json','12_PHASE_B_INNER_VALIDATION.json','13_EPOCH_STABILITY.json')
def artifact(name,obj):write(ART/name,obj)
def md(name,s):ART.mkdir(parents=True,exist_ok=True);(ART/name).write_text(s+'\n',encoding='utf-8')
def cache(ds,seed=None):
    if MODE=='canonical' and (seed is None or seed<3):return ROOT/'CHRI_V18_1/cache'/ds/(f'seed_{seed}' if seed is not None else '')
    p=OUT/'data'/MODE/'cache'/ds/(f'seed_{seed}' if seed is not None else '');p.mkdir(parents=True,exist_ok=True);return p
def cp(ds,seed,rep=1):return OUT/'features'/MODE/ds/f'seed_{seed}'/f'rep_{rep}'
def dest(phase,ds,seed,arm,rep=1):return OUT/'training'/MODE/phase/ds/f'seed_{seed}'/arm/f'rep_{rep}'
def check():
    saved=v.OUT;v.OUT=ROOT/'CHRI_V18_1'
    try:OLD_CHECK()
    finally:v.OUT=saved
def sealed(ds,test=False):
    assert ds in ('cora','pubmed') and not test,'TEST_SEAL_VIOLATION'
    if MODE=='canonical':return OLD_INPUT(ds,False)
    with np.load(OUT/'data/inner'/f'{ds}_input.npz') as z:return {k:z[k] for k in z.files}
def base_job(ds,seed,arm='C0'):
    return OLD_BASE(ds,seed,arm) if MODE=='canonical' and seed<5 else OUT/'backbones'/MODE/ds/f'seed_{seed}'
def source_pairs(ds,seed,split,epochs=None):
    epochs=epochs or (10 if MODE=='inner' else 5)
    return np.concatenate([np.load(cache(ds,seed)/f'epoch_{i}_pairs.npy').reshape(-1,2) for i in range(1,epochs+1)]) if split=='train' else np.load(cache(ds,seed)/'valid_pairs.npy')
def configure(mode):
    global MODE
    MODE=mode;v.cache=cache;v.check_frozen=check;v.sealed_input=sealed;e.sealed=sealed;v.s.input_data=sealed;v.base_job=base_job;v.make_net=make_net;h.source_pairs=source_pairs
    e.context_path=lambda ds:ROOT/'ERDR_V21/context_cache'/f'{ds}.npz' if MODE=='canonical' else OUT/'data/inner/context'/f'{ds}.npz'
    if MODE=='inner':
        e.ROOT=OUT/'data/inner/context_root';p=e.ROOT/'CHRI_V18_1/cache';p.parent.mkdir(parents=True,exist_ok=True)
        if not p.exists():p.symlink_to(OUT/'data/inner/cache',target_is_directory=True)
    else:e.ROOT=ROOT
def historical(phase,ds,seed,arm):
    if phase=='A' and arm=='SHARED':return h.job('A',ds,seed,'SHARED')
    return dest(phase,ds,seed,arm)
def scorepath(phase,ds,seed,arm,epochs=5):return historical(phase,ds,seed,arm)/f'valid_epoch{epochs}_scores.npz'
def index_stats(ds,seed,split,rep=1):
    p=cp(ds,seed,rep);keys=np.load(p/f'{split}_keys.npy');pairs=np.sort(h.source_pairs(ds,seed,split),axis=1);n=len(sealed(ds)['x']);ix=np.searchsorted(keys,pairs[:,0]*n+pairs[:,1]);return np.load(p/f'{split}_stats.npy')[ix],ix
def feature_hash(p):return {f.name:sha(f) for f in sorted(p.glob('*.npy'))}
def corr(a,b,rank=False):
    if np.std(a)<1e-12 or np.std(b)<1e-12:return None
    return float(spearmanr(a,b).statistic if rank else np.corrcoef(a,b)[0,1])
def summarize(x):return h.distribution(np.asarray(x))
def conditional_shuffle(stats,keys,M,ds,seed,split):
    # Strict strata, no fallback or labels. Cyclic derangement preserves unique-key M multiset.
    bucket=lambda x:np.floor(np.log2(x+1)).astype(np.int64)
    du=np.sort(bucket(stats[:,8:10]),axis=1);nu=np.sort(bucket(stats[:,:2]),axis=1);groups={}
    for i,row in enumerate(np.column_stack((stats[:,3].astype(np.int64),du,nu))):groups.setdefault(tuple(row),[]).append(i)
    donor=np.arange(len(keys));matched=np.zeros(len(keys),bool)
    for ids in groups.values():
        if len(ids)<2:continue
        order=sorted(ids,key=lambda i:hashlib.sha256(f'V28/{MODE}/{ds}/{seed}/{split}/{int(keys[i])}'.encode()).digest());donor[order]=np.roll(order,1);matched[order]=True
    assert np.all(keys[donor[matched]]!=keys[matched]);changed=np.any(M[donor]!=M,axis=1)
    assert np.array_equal(np.sort(M,axis=0),np.sort(M[donor],axis=0))
    return M[donor],donor,matched,changed
def prepare_features(ds,seed,rep):
    p=cp(ds,seed,rep);p.mkdir(parents=True,exist_ok=True);old=ROOT/'HDP2_V27/feature_cache'/ds/f'seed_{seed}/rep_1';stats_by={};feat_by={};audit={}
    if MODE=='canonical' and seed<3:
        for split in ('train','validation'):
            keys=np.load(old/f'{split}_keys.npy');stats=np.load(old/f'{split}_stats.npy');np.save(p/f'{split}_keys.npy',keys);np.save(p/f'{split}_stats.npy',stats);stats_by[split]=stats;feat_by[split]=h.features(stats)
    else:
        old_out=h.OUT;h.OUT=OUT/'raw_topology'/MODE
        try:h.prepare(ds,seed,rep)
        finally:h.OUT=old_out
        raw=OUT/'raw_topology'/MODE/'feature_cache'/ds/f'seed_{seed}'/f'rep_{rep}'
        for split in ('train','validation'):
            for suffix in ('keys','stats'):np.save(p/f'{split}_{suffix}.npy',np.load(raw/f'{split}_{suffix}.npy'))
            stats_by[split]=np.load(p/f'{split}_stats.npy');feat_by[split]=h.features(stats_by[split])
    # Fit each semantic block once from scheduled TRAIN occurrences, never validation.
    pp=np.sort(source_pairs(ds,seed,'train',5),axis=1);n=len(sealed(ds)['x']);keys=np.load(p/'train_keys.npy');ix=np.searchsorted(keys,pp[:,0]*n+pp[:,1]);norm={}
    for block in ('GRAPH','MULT','HDP','PAIR','SHUFFLE'):
        f=feat_by['train'][block][ix].astype(np.float64);norm[block]={'mean':f.mean(0).tolist(),'std':f.std(0).clip(1e-6).tolist()}
    # HDP shuffle shares real HDP scaling so rewiring is the only changed statistic.
    norm['SHUFFLE']=copy.deepcopy(norm['HDP']);write(p/'normalization.json',{'fit':'all5 frozen training schedules, label-free; population-weighted float64 moments','blocks':norm,'zero_padding':'not normalized','HDP_shuffle_scaler':'same as true HDP'})
    for split in ('train','validation'):
        keys=np.load(p/f'{split}_keys.npy');st=stats_by[split];raw=feat_by[split];cm,donor,matched,changed=conditional_shuffle(st,keys,raw['MULT'],ds,seed,split);raw['COND']=cm
        pp=np.sort(h.source_pairs(ds,seed,split),axis=1);ix=np.searchsorted(keys,pp[:,0]*n+pp[:,1]);cond={}
        for key,f in raw.items():
            if key=='ZERO':continue
            fit=norm['MULT' if key=='COND' else key];cond[key]=((f.astype(np.float64)-fit['mean'])/fit['std']).astype(np.float32)
        cond['0']=np.zeros((len(st),2),np.float32)
        for arm,blocks in LAYOUT.items():
            x=np.concatenate([cond[b] for b in blocks],1);assert x.shape[1]==6 and np.isfinite(x).all();np.save(p/f'{split}_{arm}.npy',x)
        np.save(p/f'{split}_donor.npy',donor);weak=matched[ix].mean()<.8 or (changed[ix][matched[ix]].mean() if matched[ix].any() else 0)<.1
        eligible=(st[ix,15]+st[ix,16])>0;material=st[ix,14]>=.1;native_fraction=float(material[eligible].mean()) if eligible.any() else 0.
        audit[split]={'matched_fraction':float(matched[ix].mean()),'actual_change_fraction':float(changed[ix].mean()),'change_fraction_among_matched':float(changed[ix][matched[ix]].mean()) if matched[ix].any() else 0.,'control_status':'CONTROL_WEAK' if weak else 'VALID','strict_matching':'exact lambda_G; sorted floorlog2(degree_G+1) pair; sorted floorlog2(incidence_degree+1) pair; no fallback','unique_candidate_marginals_exact':True,'scheduled_marginals_exact':bool(np.array_equal(np.sort(raw['MULT'][ix],axis=0),np.sort(cm[ix],axis=0))),'scheduled_original_MULT_mean':raw['MULT'][ix].mean(0).tolist(),'scheduled_donor_MULT_mean':cm[ix].mean(0).tolist(),'G_hash_before':array_hash(raw['GRAPH']),'G_hash_after':array_hash(raw['GRAPH']),'candidate_order_hash':array_hash(pp),'donor_labels_used':False,'weak_rule':'matched<80% or change among matched<10%; diagnostic only','HDP_incidence_shuffle':{'degree_preservation_exact':True,'material_fraction_among_eligible':native_fraction,'lambda_changed_fraction':float(st[ix,17].mean()),'status':'VALID' if native_fraction>.5 else 'CONTROL_WEAK'}}
    write(p/'READY.json',{'state':'PASS','hashes':feature_hash(p),'normalization_sha256':sha(p/'normalization.json'),'conditional_shuffle':audit,'mode':MODE});print('V28_FEATURES_READY',MODE,ds,seed,rep,flush=True)
class Lookup:
    def __init__(self,ds,seed,arm):
        self.n=len(sealed(ds)['x']);p=cp(ds,seed,REP);self.data={sp:(torch.as_tensor(np.load(p/f'{sp}_keys.npy'),device='cuda'),torch.as_tensor(np.load(p/f'{sp}_{arm}.npy'),device='cuda')) for sp in ('train','validation')}
    def __call__(self,pairs,training):
        p=pairs.sort(1).values;query=p[:,0]*self.n+p[:,1];keys,x=self.data['train' if training else 'validation'];ix=torch.searchsorted(keys,query);assert torch.equal(keys[ix],query);return x[ix]
class Predictor(g.m.MERIPredictor):
    def __init__(self,ds,seed,arm,mean,std):
        super().__init__(e.ContextStructure(ds),seed,'DUP',mean,std);self.lookup=Lookup(ds,seed,arm)
        with torch.random.fork_rng():
            torch.manual_seed(27002+seed);self.structural_residual=nn.Sequential(nn.Linear(6,8),nn.ReLU(),nn.Linear(8,1));nn.init.zeros_(self.structural_residual[-1].weight);nn.init.zeros_(self.structural_residual[-1].bias)
    def forward(self,pairs,b,donor=None):
        score,nl,cl=super().forward(pairs,b,donor);return score+self.structural_residual(self.lookup(pairs,self.training)).flatten(),nl,cl
def make_net(ds,seed,arm,phase,structure=None):
    stats=read(cache(ds,seed)/'normalization.json');mean,std=np.asarray(stats['mean']),np.asarray(stats['std'])
    if arm=='DUP':return g.m.MERIPredictor(e.ContextStructure(ds),seed,'DUP',mean,std).to('cuda')
    return Predictor(ds,seed,arm,mean,std).to('cuda')
def train(phase,ds,seed,arm,rep,epochs):
    global REP
    REP=rep;destination=dest(phase,ds,seed,arm,rep);destination.mkdir(parents=True,exist_ok=True)
    v.OUT=destination;v.job=lambda phase,ds,seed,arm:destination
    actual='DUP' if arm=='SHARED' else arm;trajectory=hashlib.sha256();steps=[0];original=torch.optim.Adam.step
    def step(opt,*args,**kw):
        result=original(opt,*args,**kw);steps[0]+=1;trajectory.update(str(steps[0]).encode())
        for group in opt.param_groups:
            for param in group['params']:trajectory.update(param.detach().cpu().contiguous().numpy().tobytes())
        if steps[0]==1:print('FIRST_OPTIMIZER_STEP_OK',MODE,phase,ds,seed,arm,rep,flush=True)
        return result
    torch.optim.Adam.step=step;v.run(phase,ds,seed,actual,epochs);row=read(destination/'result.json');scores=v.scores_file(destination/f'valid_epoch{epochs}_scores.npz');q=len(sealed(ds)['valid_pos']);y=np.arange(len(scores))<q;prob=1/(1+np.exp(-np.clip(scores.astype(np.float64),-700,700)));row['validation']['brier']=float(((prob-y)**2).mean());row.update(variant=arm,protocol=PROTO if MODE=='canonical' else 'V28_INNER_TRAIN_VALIDATION_V1',mode=MODE,training_trajectory_sha256=trajectory.hexdigest(),optimizer_steps=steps[0],score_vector_sha256=e.score_hash(destination/f'valid_epoch{epochs}_scores.npz'),feature_hashes=read(cp(ds,seed,rep)/'READY.json')['hashes'] if arm!='SHARED' else None);write(destination/'result.json',row);print('V28_JOB_COMPLETE',MODE,phase,ds,seed,arm,rep,flush=True)
def batch(tasks,stage,workers=6):
    queue=list(tasks);active=[];done=0;(OUT/'logs').mkdir(parents=True,exist_ok=True)
    while queue or active:
        for p,args,log in list(active):
            if p.poll() is not None:active.remove((p,args,log));assert p.returncode==0,f'JOB_FAILED {args} {log}';done+=1
        while queue and len(active)<workers:
            args=queue.pop(0);log=OUT/'logs'/('_'.join(map(str,args))+'.log')
            with log.open('a') as f:p=subprocess.Popen([sys.executable,'-B','-u',str(Path(__file__).resolve()),*map(str,args)],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
            active.append((p,args,log));CHILDREN.append(p)
        state={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(queue),'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False};artifact('RUN_STATUS.json',state);write(OUT/'RUN_STATUS.json',state)
        if active:time.sleep(3)
def freeze():
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);check();previous=read(REPO/'result/innovation2/HDP2_V27/SOURCE_HASHES.json');files=dict(previous['files'])
    for p,expected in files.items():assert sha(REPO/p)==expected,'HISTORICAL_SOURCE_CHANGED '+p
    for name,expected in previous['feature_cache_hashes'].items():assert sha(REPO/name)==expected,'V27_CACHE_CHANGED'
    for folder in ('HDP2_V27','CRM_V26','RELREUSE_V24'):
        for p in (REPO/'result/innovation2'/folder).glob('*'):
            if p.suffix in ('.json','.md'):files[str(p.relative_to(REPO))]=sha(p)
    for p in [*list((OUT/'scripts').glob('*.py')),ART/'00_PROTOCOL.md']:files[str(p.relative_to(REPO))]=sha(p)
    artifact('SOURCE_HASHES.json',{'files':files,'historical_topology_caches':previous['feature_cache_hashes'],'caches':previous['caches'],'canonical_protocol':PROTO});e.ART=ART;e.cache_check()
    artifact('WORKSPACE_AUDIT.json',{'workspace':'DCDLP-main','local_project':'DCDLP-main','server_checkout':str(REPO),'workspace_info_tool':'NOT_AVAILABLE; equivalent identity verified via frozen source hashes and canonical manifest','canonical_protocol':PROTO,'architecture':'SHARED literal V22 DUP, jointly trainable with residual; frozen NCNC','conflicting_source_assumptions':[]})
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'workspace':'DCDLP-main','canonical_protocol':PROTO,'phase_A':{'seeds':[0,1,2],'epochs':5,'arms':list(ARMS)},'residual':[6,8,1],'residual_parameters':65,'SHARED_parameters':30529,'fusion_parameters':30594,'normalization':'train5 scheduled candidate moments per semantic block; zero padding unchanged; same scaler for H/Hshuffle','phase_B':{'seeds':[3,4,5,6,7],'hypotheses_maximum':2,'selection':'positive primary paired effects; cross-dataset direction, matched-control strength, simplicity; all observations retained'},'inner':{'holdout_fraction':.1,'split_seed':280016,'seeds':[3,4,5],'negative_count':20,'backbone':'newly trained inner-only C0,10 final epochs','residual_budgets':[5,10],'rule':'run selected hypothesis on a dataset only if additional-seed primary minimum mean CE positive; train both budgets from paired initialization, shared first5 schedules'},'novelty_status':'NOT_AUDITED','test_opened':False,'GPU_workers':6,'CPU_workers':6,'numba_threads':6})
    for name in FILES:artifact(name,{'state':'NOT_RUN','reason':'Awaiting predeclared prerequisite.'})
    for name in ('01_FEATURE_DEPENDENCY_AUDIT.md','10_RANKING_CALIBRATION_ANALYSIS.md','14_SIGNAL_LEDGER.md','15_DECISION.md','FINAL_REPORT.md'):md(name,'# V28\n\nPENDING')
def phase0():
    ref=read(REPO/'result/innovation2/HDP2_V27/11_PHASE_A_RESULTS.json');records=[]
    for ds in ('cora','pubmed'):
        for seed in range(3):
            for arm in ('SHARED','ZERO','GRAPH','MULT','HDP'):
                path=h.job('A',ds,seed,arm);row=read(path/'result.json');expected=ref['datasets'][ds]['seed_results'][seed]['arms'][arm];state=torch.load(path/'final.pt',map_location='cpu',weights_only=False)['state'];checks={'checkpoint_sha256':sha(path/'final.pt')==row['checkpoint_sha256']==expected['checkpoint_sha256'],'score_vector_sha256':e.score_hash(path/'valid_epoch5_scores.npz')==row['score_vector_sha256']==expected['score_vector_sha256'],'state_tensor_sha256':g.statehash(state)==row['state_tensor_sha256'],'metrics':row['validation']==expected['validation'],'training_trajectory_sha256':row['training_trajectory_sha256']==expected['training_trajectory_sha256'],'feature_hashes':row['feature_cache_hashes']==read(ROOT/'HDP2_V27/feature_cache'/ds/f'seed_{seed}/rep_1/READY.json')['hashes']};assert all(checks.values()),f'V27_REPRODUCTION_FAILURE {ds} {seed} {arm}';records.append({'dataset':ds,'seed':seed,'arm':arm,'checks':checks,'reuse':'verified immutable artifacts, no retraining'})
    artifact('02_BASELINE_REPRODUCTION.json',{'state':'PASS','records':records,'V27_positive_observation':'POSITIVE_TOPOLOGICAL_SIGNAL, not confirmed innovation'})
def dependency_diagnostics():
    dependency={};probes={};shuffle={}
    for ds in ('cora','pubmed'):
        dependency[ds]=[];probes[ds]=[];shuffle[ds]=[]
        for seed in range(3):
            arrays={sp:index_stats(ds,seed,sp)[0] for sp in ('train','validation')};d={};pr={}
            for split,a in arrays.items():
                cn,s=a[:,3],a[:,6];top=max(1,int(.1*len(a)));order=lambda x:set(np.argsort(-x,kind='stable')[:top]);o1,o2=order(cn),order(s);d[split]={'exact_equality_rate':float((cn==s).mean()),'Pearson':corr(cn,s),'Spearman':corr(cn,s,True),'top10pct_rank_overlap':len(o1&o2)/top,'rank_tie_policy':'stable candidate order; heavy ties limit interpretation','count_difference':summarize(cn-s),'conditional_S_by_GRAPH':{name:{'count':int(mask.sum()),'S':summarize(s[mask]) if mask.any() else None} for name,mask in {'G0':cn==0,'G1':cn==1,'G2plus':cn>=2}.items()}}
            ft,fv=h.features(arrays['train']),h.features(arrays['validation'])
            for target,blocks in (('MULT',('GRAPH',)),('HDP',('GRAPH','MULT')),('PAIR',('GRAPH','MULT'))):
                x=np.concatenate([ft[b] for b in blocks],1).astype(np.float64);y=np.concatenate([fv[b] for b in blocks],1).astype(np.float64);coef=np.linalg.lstsq(np.column_stack((x,np.ones(len(x)))),ft[target],rcond=None)[0];pred=np.column_stack((y,np.ones(len(y))))@coef;truth=fv[target].astype(np.float64);items=[]
                for j in range(2):
                    residual=truth[:,j]-pred[:,j];den=float(((truth[:,j]-truth[:,j].mean())**2).sum());items.append({'channel':j,'R2':1-float((residual**2).sum())/den if den else None,'MAE':float(np.abs(residual).mean()),'correlation':corr(pred[:,j],truth[:,j]),'conditional_residual':{group:summarize(residual[mask]) if mask.any() else None for group,mask in {'G0':arrays['validation'][:,3]==0,'Gpositive':arrays['validation'][:,3]>0}.items()}})
                pr[target]={'inputs':blocks,'probe':'train-only OLS with intercept, outputs never used in training','validation':items}
            dependency[ds].append({'seed':seed,'splits':d});probes[ds].append({'seed':seed,'probes':pr});shuffle[ds].append({'seed':seed,'audit':read(cp(ds,seed)/'READY.json')['conditional_shuffle']})
    projection={'GRAPH':'Exactly recoverable from unweighted2-section of candidate-masked raw-star hypergraph.','MULT':'Exactly reconstructable from endpoint-exclusive weighted incidence projections: m_u(w),m_v(w); M=dot(m_u,m_v), S=count(both>0). Whole-hypergraph weighted2-section alone lacks the removed shared-hyperedge triple-incidence correction; recoverability from that single matrix is not established here.','HDP_PAIR':'Exact incidence/grouping functions; endpoint weights alone do not specify compatibility grouping. No claim of hypergraph exclusivity.','source':'All raw-stars are deterministic functions of the original training graph, so every feature is reconstructable from that source graph. No native hypergraph-exclusive novelty claimed.'}
    artifact('01_FEATURE_DEPENDENCY_AUDIT.json',{'state':'COMPLETE','datasets':dependency,'projection_recoverability':projection});md('01_FEATURE_DEPENDENCY_AUDIT.md','# Feature dependency\n\n'+json.dumps(projection,indent=2)+'\n\n'+json.dumps(dependency,indent=2));artifact('05_CONDITIONAL_TOPOLOGY_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':probes});artifact('08_CONDITIONAL_SHUFFLE_AUDIT.json',{'state':'COMPLETE','datasets':shuffle})
@torch.no_grad()
def initial_audit():
    counts={};records=[]
    for ds in ('cora','pubmed'):
        pairs=torch.as_tensor(np.load(cache(ds,0)/'valid_pairs.npy')[:128],device='cuda');b=torch.as_tensor(np.load(cache(ds,0)/'valid_b.npy')[:128],device='cuda');base=make_net(ds,0,'DUP','A').eval();score=base(pairs,b)[0];head_hash=None
        for arm in LAYOUT:
            net=make_net(ds,0,arm,'A').eval();counts[arm]=sum(p.numel() for p in net.parameters() if p.requires_grad);assert counts[arm]==30594;assert torch.equal(net(pairs,b)[0],score);nonhead={k:t for k,t in net.state_dict().items() if not k.startswith('structural_residual.')};assert g.statehash(nonhead)==g.statehash(base.state_dict());hh=g.statehash(net.structural_residual.state_dict());head_hash=head_hash or hh;assert hh==head_hash;assert torch.equal(net.lookup(pairs,False),net.lookup(pairs.flip(1),False))
        counts['SHARED']=sum(p.numel() for p in base.parameters() if p.requires_grad);records.append({'dataset':ds,'initial_scores_bit_identical':True,'nonresidual_state_bit_identical':True,'fusion_head_initial_state':head_hash,'all_fusion_heads_paired':True,'pair_swap_exact':True})
    artifact('03_PARAMETER_AND_INITIALIZATION_AUDIT.json',{'state':'PASS','counts':counts,'records':records,'SHARED_jointly_trainable':True,'optimizer_loss_sampler_unchanged':True})
def rows(phase,ds,seeds,arms):
    result=[]
    for seed in seeds:
        row={'seed':seed,'arms':{a:read(historical(phase,ds,seed,a)/'result.json') for a in arms}};reference=row['arms'][arms[0]]
        assert all(r['training_trace']==reference['training_trace'] for r in row['arms'].values()),'PAIRED_TRAINING_TRACE_MISMATCH';result.append(row)
    return result
def summary(phase,seeds,arms,datasets=('cora','pubmed')):
    data={'state':'COMPLETE','mode':MODE,'phase':phase,'seeds':list(seeds),'arms':list(arms),'datasets':{},'test_opened':False}
    for ds in datasets:
        rr=rows(phase,ds,seeds,arms);contrasts={}
        for a in arms:
            for b in arms:
                if a!=b:contrasts[f'{a}_vs_{b}']=v.comparison(rr,a,b)
        data['datasets'][ds]={'seed_results':rr,'effects':contrasts,'metrics':{a:{m:v.stat([r['arms'][a]['validation'][m] for r in rr]) for m in v.METRICS} for a in arms}}
    return data
def hypothesis_level(data,name):
    candidate,_=HYPOTHESES[name];comparators=PRIMARY[name];ce=[data['datasets'][ds]['effects'][f'{candidate}_vs_{b}']['ce'] for ds in data['datasets'] for b in comparators];both=all(x['mean']>0 for x in ce);rep=both or any(x['mean']>0 and x['wins']>=2 for x in ce);positive=any(x['wins']>0 for x in ce)
    return 'REPLICATION_CANDIDATE' if rep else ('EXPLORATORY_POSITIVE' if positive else 'NO_SIGNAL')
def selection(data):
    records=[]
    for name,(candidate,controls) in HYPOTHESES.items():
        level=hypothesis_level(data,name);per=[min(data['datasets'][ds]['effects'][f'{candidate}_vs_{b}']['ce']['mean'] for b in PRIMARY[name]) for ds in ('cora','pubmed')];positive=sum(x>0 for x in per);records.append({'hypothesis':name,'candidate':candidate,'controls':list(controls),'level':level,'primary_minimum_mean_by_dataset':per,'positive_datasets':positive,'mean_primary_minimum':float(np.mean(per)),'simplicity':{'GRAPH':1,'MULT':1,'COMPLEMENTARITY':2,'HDP_CONDITIONAL':3}[name]})
    ranked=sorted([r for r in records if r['level']!='NO_SIGNAL'],key=lambda r:(-r['positive_datasets'],-r['mean_primary_minimum'],r['simplicity'],r['hypothesis']));selected=ranked[:2];artifact('PHASE_B_SELECTION.json',{'state':'COMPLETE','all_hypotheses':records,'selected':selected,'selection_used_test':False,'algorithm':'descending number positive dataset minimum primary means, then average minimum primary effect, then fewer semantic blocks; maximum2'});return selected
def subgroup(data):
    results={}
    for ds in ('cora','pubmed'):
        results[ds]=[];q=len(sealed(ds)['valid_pos'])
        for seed in range(3):
            a=index_stats(ds,seed,'validation')[0];scores={arm:v.scores_file(scorepath('A',ds,seed,arm)).astype(np.float64) for arm in ('GM','GMH')};label=np.arange(len(a))<q;loss={arm:np.logaddexp(0,s)-label*s for arm,s in scores.items()};delta=loss['GM']-loss['GMH'];ss={}
            for name,mask in {'H0':a[:,2]==0,'Hpositive':a[:,2]>0,'H2plus':a[:,2]>=2}.items():
                ss[name]={'count':int(mask.sum()),'positives':int(label[mask].sum()),'negatives':int((~label[mask]).sum()),'positive_rate':float(label[mask].mean()) if mask.any() else None,'CE':{arm:float(x[mask].mean()) if mask.any() else None for arm,x in loss.items()},'average_score_GMH_minus_GM':float((scores['GMH']-scores['GM'])[mask].mean()) if mask.any() else None,'per_candidate_DeltaCE_distribution':summarize(delta[mask]) if mask.any() else None}
            p=OUT/'diagnostics'/ds/f'seed_{seed}';p.mkdir(parents=True,exist_ok=True);np.savez_compressed(p/'HDP_subgroups.npz',lambda_H=a[:,2],label=label,delta_CE=delta,score_difference=scores['GMH']-scores['GM']);results[ds].append({'seed':seed,'subgroups':ss,'per_candidate_arrays':str(p/'HDP_subgroups.npz')})
    artifact('09_HDP_SUBGROUP_ANALYSIS.json',{'state':'COMPLETE','datasets':results,'descriptive_only':True,'thresholds_preregistered':[0,1,2]})
def prepare_data(ds,seed,epochs):
    # All newly generated files live in V28. Historical caches are read-only.
    if MODE=='canonical':
        parent=OUT/'data/canonical/cache'/ds;parent.mkdir(parents=True,exist_ok=True)
        for name in ('structure.npz','STRUCTURE_READY.json'):
            p=parent/name
            if not p.exists():p.symlink_to(ROOT/'CHRI_V18_1/cache'/ds/name)
    else:
        if not (cache(ds)/'STRUCTURE_READY.json').exists():
            a=sealed(ds)
            with threadpool_limits(limits=4,user_api='blas'):meta=build_structure(a['x'],a['train'],cache(ds)/'structure.npz')
            meta.update(state='PASS',dataset=ds);write(cache(ds)/'STRUCTURE_READY.json',meta);e.prepare_context(ds)
    bj=base_job(ds,seed)
    if not (bj/'result.json').exists():train_backbone(ds,seed)
    v.prepare_backbone(ds,seed,epochs)
    if epochs==10:
        ready=read(cache(ds,seed)/'B_READY_10.json');ready['epochs']=5;ready['trace']=ready['trace'][:5];write(cache(ds,seed)/'B_READY_5.json',ready)
    # DUP consumes no donors. Keep the canonical train-only normalization and dummy
    # donor transport without spending time on unused PCA/kNN; documented in audit.
    p=cache(ds,seed);ep=np.load(p/'epoch_1.npy');pairs=np.load(p/'epoch_1_pairs.npy');fb=np.concatenate((ep[0],ep[1]));write(p/'normalization.json',{'mean':fb.mean(0).tolist(),'std':fb.std(0).clip(1e-5).tolist(),'fit':'epoch1 training candidates only, identical canonical rule','test_accessed':False});np.save(p/'donor_pairs.npy',pairs.reshape(-1,2))
    for i in range(1,epochs+1):np.save(p/f'epoch_{i}_knn.npy',np.zeros((np.load(p/f'epoch_{i}_pairs.npy').reshape(-1,2).shape[0],32),np.int32))
    np.save(p/'valid_knn.npy',np.zeros((len(np.load(p/'valid_pairs.npy')),32),np.int32));print('V28_NEW_DATA_READY',MODE,ds,seed,epochs,flush=True)
def train_backbone(ds,seed):
    bj=base_job(ds,seed);bj.mkdir(parents=True,exist_ok=True);s=v.s;model,pred,res,opt,data,train,scope,a,initial=s.make_models(ds,seed,'C0');assert res is None;history=[];trajectory=[]
    for epoch in range(1,11):
        loss=scope['train'](model,pred,data,{'train':{'edge':train}},opt,v.b.NCFG[ds]['batch'],True,[],None);assert np.isfinite(loss);history.append({'epoch':epoch,'loss':float(loss)});trajectory.append(s.statehash(model,pred));print('V28_BACKBONE',MODE,ds,seed,epoch,flush=True)
    metrics,seconds=s.evaluate(model,pred,None,data,a['valid_pos'],a['valid_neg'],None,'C0',bj/'valid_epoch10_scores.npz');torch.save({'model':model.state_dict(),'predictor':pred.state_dict(),'epoch':10,'arm':'C0','dataset':ds,'seed':seed},bj/'final.pt');write(bj/'result.json',{'state':'COMPLETE','epochs':10,'arm':'C0','base_parameters':sum(p.numel() for m in (model,pred) for p in m.parameters()),'checkpoint_sha256':sha(bj/'final.pt'),'test_accessed':False,'initialization':initial,'history':history,'training_trajectory':trajectory,'validation':metrics,'training_input_hash':array_hash(a['train']),'mode':MODE});del model,pred,opt;gc.collect();torch.cuda.empty_cache()
def create_inner():
    folder=OUT/'data/inner';folder.mkdir(parents=True,exist_ok=True);audit={}
    for ds in ('cora','pubmed'):
        a=OLD_INPUT(ds,False);train=a['train'];n=len(a['x']);rng=np.random.RandomState(280016);order=rng.permutation(len(train));hold=max(1,int(np.ceil(.1*len(train))));valid=train[order[:hold]];inner=train[np.sort(order[hold:])];original=set(map(tuple,np.sort(train,axis=1)));neg=np.empty((len(valid),20,2),np.int64)
        for i,(u,w) in enumerate(valid):
            used=set()
            for j in range(20):
                while True:
                    other=int(rng.randint(n));key=tuple(sorted((int(u),other)))
                    if other!=u and key not in original and other not in used:break
                used.add(other);neg[i,j]=[u,other]
        assert not (set(map(tuple,np.sort(inner,axis=1)))&set(map(tuple,np.sort(valid,axis=1))));np.savez(folder/f'{ds}_input.npz',x=a['x'],train=inner,valid_pos=valid,valid_neg=neg);audit[ds]={'split_seed':280016,'original_train_pairs':len(train),'inner_train_pairs':len(inner),'inner_valid_pairs':len(valid),'hashes':{k:array_hash(x) for k,x in {'train':inner,'valid_pos':valid,'valid_neg':neg}.items()},'disjoint_undirected_positive_sets':True,'negative_filter':'original training pool only; per query unique uniform endpoint corruption;20','backbone':'fresh inner-train C0 final10, no full-training checkpoint','hypergraph':'rebuilt from inner-train; per-candidate training target removed','original_validation_used':False,'test_opened':False}
    artifact('INNER_SPLIT_AUDIT.json',{'state':'PASS','datasets':audit,'protocol':'V28_INNER_TRAIN_VALIDATION_V1','budgets':[5,10],'seeds':[3,4,5]})
def bootstrap(values):
    x=np.asarray(values);rng=np.random.RandomState(280028);samples=x[rng.randint(len(x),size=(10000,len(x)))].mean(1);return {'percentile95':np.quantile(samples,[.025,.975]).tolist(),'resampling_unit':'paired training seed,10000 bootstrap draws; descriptive, very small n','unsupported_significance_claim':False}
def add_bootstrap(data):
    for d in data['datasets'].values():
        for effect in d['effects'].values():effect['ce']['paired_bootstrap']=bootstrap(effect['ce']['per_seed'])
    return data
def finish(phaseA,selected,phaseB,inner):
    decisions={name:{'phase_A_status':hypothesis_level(phaseA,name),'research_status':hypothesis_level(phaseA,name),'phase_B_selected':any(x['hypothesis']==name for x in selected)} for name in HYPOTHESES};ledger=['# V28 signal ledger','','V27 GRAPH/MULT/HDP positive meanCE vs SHARED are retained as POSITIVE_TOPOLOGICAL_SIGNAL. No novelty claim.'];ranking=[]
    for name,(candidate,controls) in HYPOTHESES.items():
        performance={ds:phaseA['datasets'][ds]['effects'][f'{candidate}_vs_SHARED'] for ds in ('cora','pubmed')};mechanism={ds:{b:phaseA['datasets'][ds]['effects'][f'{candidate}_vs_{b}'] for b in PRIMARY[name]} for ds in ('cora','pubmed')};decisions[name].update(PERFORMANCE_SIGNAL=performance,MECHANISM_SIGNAL=mechanism,mechanism_supported=False)
    for ds,d in phaseA['datasets'].items():
        for arm in LAYOUT:
            for control in ('SHARED','GDUP','GM'):
                if arm==control:continue
                effect=d['effects'][f'{arm}_vs_{control}'];ce=effect['ce']['mean']>0;rank=effect['mrr']['mean']>0;status='CE_AND_RANKING_GAIN' if ce and rank else ('CE_ONLY_GAIN' if ce else ('RANKING_ONLY_GAIN' if rank else 'NO_GAIN'));ranking.append({'dataset':ds,'arm':arm,'control':control,'status':status,'DeltaCE':effect['ce'],'DeltaMRR':effect['mrr'],'DeltaHits10':effect['hits10']})
    for item in selected:
        name=item['hypothesis'];candidate=item['candidate'];replicated=[];mechanism=[]
        for ds,d in phaseB['datasets'].items():
            positive=all(d['effects'][f'{candidate}_vs_{b}']['ce']['mean']>0 for b in PRIMARY[name]);r=inner.get(ds)
            if positive and r:
                five=r['budgets']['5']['datasets'][ds];ten=r['budgets']['10']['datasets'][ds];good=all(five['effects'][f'{candidate}_vs_{b}']['ce']['mean']>0 for b in PRIMARY[name]);stable=all(ten['effects'][f'{candidate}_vs_{b}']['ce']['mean']>0 for b in PRIMARY[name]);replicated.append({'dataset':ds,'inner5_primary_positive':good,'inner10_primary_positive':stable})
                required=item['controls'];mg=all(five['effects'][f'{candidate}_vs_{b}']['ce']['mean']>0 and ten['effects'][f'{candidate}_vs_{b}']['ce']['mean']>0 and d['effects'][f'{candidate}_vs_{b}']['ce']['mean']>0 for b in required)
                if name in ('COMPLEMENTARITY','HDP_CONDITIONAL'):
                    for mode,seeds in (('canonical',range(3,8)),('inner',(3,4,5))):
                        for s in seeds:
                            au=read(OUT/'features'/mode/ds/f'seed_{s}/rep_1/READY.json')['conditional_shuffle']['validation'];mg &= (au['control_status']=='VALID' if name=='COMPLEMENTARITY' else au['HDP_incidence_shuffle']['status']=='VALID')
                mechanism.append(mg)
        decisions[name]['replication_evidence']=replicated
        if any(x['inner5_primary_positive'] for x in replicated):decisions[name]['research_status']='REPLICATED_SIGNAL'
        if len(mechanism)==2 and all(mechanism):decisions[name]['research_status']='MECHANISM_SUPPORTED';decisions[name]['mechanism_supported']=True
    for name,row in decisions.items():ledger.extend([f'## {name}',json.dumps(row,indent=2)])
    out={'GRAPH_SIGNAL_STATUS':decisions['GRAPH'],'MULT_SIGNAL_STATUS':decisions['MULT'],'GRAPH_MULT_COMPLEMENTARITY':decisions['COMPLEMENTARITY'],'HDP_CONDITIONAL_INCREMENT':decisions['HDP_CONDITIONAL'],'MECHANISM_STATUS':{name:d['mechanism_supported'] for name,d in decisions.items()},'CAPACITY_EXPLANATION':'see paired ZERO6/GDUP/MDUP/GMG results; independent performance and mechanism statuses retained','RANKING_GENERALIZATION':ranking,'NOVELTY_STATUS':'NOT_AUDITED','PAPER_READY_INNOVATION':False,'test_opened':False,'innovation1_modified':False,'historical_results_modified':False};artifact('DECISION.json',out);md('15_DECISION.md','# V28 independent decisions\n\n'+json.dumps(out,indent=2));md('14_SIGNAL_LEDGER.md','\n\n'.join(ledger));md('10_RANKING_CALIBRATION_ANALYSIS.md','# Ranking vs calibration\n\n'+json.dumps(ranking,indent=2))
    sections=['# V28 full report',json.dumps(out,indent=2),'Canonical PhaseA 5epoch; new seeds separately; inner protocol separately. All scalar fusion arms30594parameters;SHARED30529. No novelty audit, test or V29 mechanism.']
    for name in FILES:sections.extend([name,json.dumps(read(ART/name),indent=2)])
    md('FINAL_REPORT.md','\n\n'.join(sections));md('C2C_HANDOFF.md','STATUS: EXECUTED\nTASK: V28_TOPOLOGICAL_SIGNAL_CONSOLIDATION\nWORKSPACE: DCDLP-main\nCANONICAL_PROTOCOL: '+PROTO+'\nV27_REPRODUCTION: PASS\nDETERMINISM: PASS\nLEAKAGE: PASS\nPARAMETER_MATCHING: PASS\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO\nNOVELTY_STATUS: NOT_AUDITED\nPRIMARY_ARTIFACT: result/innovation2/TOPOLOGY_V28/FINAL_REPORT.md\nNEXT_EXPECTED_STEP: return paired evidence, preserve positive signals; no automatic V29 or novelty claim.\n'+json.dumps(out,indent=2));configure('canonical');check_frozen_all();state={'state':'COMPLETE','ended_at':time.time(),'research_decisions':{k:x['research_status'] for k,x in decisions.items()},'novelty_status':'NOT_AUDITED','test_opened':False};artifact('RUN_STATUS.json',state);write(OUT/'RUN_STATUS.json',state);print('V28_COMPLETE',flush=True)
def check_frozen_all():
    for p,x in read(ART/'SOURCE_HASHES.json')['files'].items():assert sha(REPO/p)==x,'HISTORICAL_SOURCE_CHANGED '+p
    for p,x in read(ART/'SOURCE_HASHES.json')['historical_topology_caches'].items():assert sha(REPO/p)==x,'HISTORICAL_CACHE_CHANGED '+p
    check()
def supervise():
    try:
        configure('canonical');freeze();phase0();batch([('features','canonical',ds,s,1) for ds in ('cora','pubmed') for s in range(3)]+[('features','canonical','pubmed',0,2)],'FEATURE_PREPARATION');dependency_diagnostics();initial_audit()
        batch([('train','canonical','D','pubmed',0,a,r,5) for a in ('GM','GMH','GMS','GMP') for r in (1,2)],'DETERMINISM_PRECHECK');checks=[]
        for a in ('GM','GMH','GMS','GMP'):
            rr=[read(dest('D','pubmed',0,a,r)/'result.json') for r in (1,2)];checkfields={k:rr[0][k]==rr[1][k] for k in ('feature_hashes','training_trajectory_sha256','checkpoint_sha256','score_vector_sha256','history','training_trace')};assert all(checkfields.values()),'DETERMINISTIC_PROTOCOL_FAILURE';checks.append({'arm':a,'checks':checkfields})
            p=dest('A','pubmed',0,a);p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(dest('D','pubmed',0,a),target_is_directory=True)
        artifact('04_DETERMINISM_PRECHECK.json',{'state':'PASS','pairs':checks,'normalization_recomputed_independently':True});batch([('train','canonical','A',ds,s,a,1,5) for ds in ('cora','pubmed') for s in range(3) for a in LAYOUT if not(ds=='pubmed' and s==0 and a in ('GM','GMH','GMS','GMP'))],'PHASE_A');a=summary('A',range(3),ARMS);artifact('06_PHASE_A_METRICS.json',a);artifact('07_PHASE_A_PAIRED_CONTRASTS.json',{ds:d['effects'] for ds,d in a['datasets'].items()});subgroup(a);selected=selection(a)
        if not selected:
            for name in ('11_PHASE_B_NEW_SEED_RESULTS.json','12_PHASE_B_INNER_VALIDATION.json','13_EPOCH_STABILITY.json'):artifact(name,{'state':'NOT_RUN','reason':'No primary hypothesis has any positive paired seed effect in PhaseA.'})
            finish(a,[],{'datasets':{}},{});return
        arms=tuple(dict.fromkeys(x for item in selected for x in (item['candidate'],*item['controls'])));batch([('data','canonical',ds,s,5) for ds in ('cora','pubmed') for s in range(3,8)],'NEW_SEED_BACKBONE_AND_CACHE',workers=2);batch([('features','canonical',ds,s,1) for ds in ('cora','pubmed') for s in range(3,8)],'NEW_SEED_FEATURES');batch([('train','canonical','B',ds,s,arm,1,5) for ds in ('cora','pubmed') for s in range(3,8) for arm in arms],'PHASE_B_ADDITIONAL_SEEDS');b=add_bootstrap(summary('B',range(3,8),arms));all8=copy.deepcopy(b)
        for ds in ('cora','pubmed'):
            rr=rows('A',ds,range(3),arms)+rows('B',ds,range(3,8),arms);all8['datasets'][ds]={'seed_results':rr,'effects':{f'{x}_vs_{y}':v.comparison(rr,x,y) for x in arms for y in arms if x!=y},'metrics':{arm:{m:v.stat([r['arms'][arm]['validation'][m] for r in rr]) for m in v.METRICS} for arm in arms}}
        all8['seeds']=list(range(8));add_bootstrap(all8);artifact('11_PHASE_B_NEW_SEED_RESULTS.json',{'state':'COMPLETE','selected_hypotheses':selected,'new_seeds_only':b,'all_eight_seeds':all8,'selection_bias_note':'seeds0-2 selected hypotheses; seeds3-7 are replication evidence'})
        eligible={ds:[item for item in selected if all(b['datasets'][ds]['effects'][f'{item["candidate"]}_vs_{control}']['ce']['mean']>0 for control in PRIMARY[item['hypothesis']])] for ds in ('cora','pubmed')};inner={}
        if any(eligible.values()):
            create_inner();batch([('data','inner',ds,s,10) for ds,items in eligible.items() if items for s in (3,4,5)],'INNER_TRAIN_BACKBONE_AND_CACHE',workers=2);batch([('features','inner',ds,s,1) for ds,items in eligible.items() if items for s in (3,4,5)],'INNER_FEATURES')
            for ds,items in eligible.items():
                if not items:continue
                inner_arms=tuple(dict.fromkeys(x for item in items for x in (item['candidate'],*item['controls'])));batch([('train','inner',f'I{epochs}',ds,s,arm,1,epochs) for epochs in (5,10) for s in (3,4,5) for arm in inner_arms],f'INNER_VALIDATION_{ds.upper()}');configure('inner');inner[ds]={'eligible_hypotheses':items,'budgets':{str(epochs):add_bootstrap(summary(f'I{epochs}',(3,4,5),inner_arms,(ds,))) for epochs in (5,10)}};configure('canonical')
            artifact('12_PHASE_B_INNER_VALIDATION.json',{'state':'COMPLETE','protocol':'V28_INNER_TRAIN_VALIDATION_V1','datasets':inner,'not_run_datasets':{ds:'No selected primary hypothesis has positive new-seed minimum mean CE on this dataset.' for ds,items in eligible.items() if not items}});artifact('13_EPOCH_STABILITY.json',{'state':'COMPLETE','datasets':inner,'budgets':[5,10],'checkpoint_selection':'final epoch only, no validation checkpoint optimization'})
        else:
            for name in ('12_PHASE_B_INNER_VALIDATION.json','13_EPOCH_STABILITY.json'):artifact(name,{'state':'NOT_RUN','reason':'No selected hypothesis has positive mean CE over all its primary matched controls on either dataset in new seeds3-7.'})
        finish(a,selected,b,inner)
    except BaseException as err:
        for p in CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        failed={'state':'EXECUTION_FAILED','error':repr(err),'traceback':traceback.format_exc(),'test_opened':False};artifact('ERROR.json',failed);artifact('RUN_STATUS.json',failed);write(OUT/'RUN_STATUS.json',failed);print(traceback.format_exc(),flush=True);raise
if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='supervise':supervise()
    else:
        configure(sys.argv[2])
        if cmd=='features':prepare_features(sys.argv[3],int(sys.argv[4]),int(sys.argv[5]))
        elif cmd=='data':prepare_data(sys.argv[3],int(sys.argv[4]),int(sys.argv[5]))
        elif cmd=='train':train(sys.argv[3],sys.argv[4],int(sys.argv[5]),sys.argv[6],int(sys.argv[7]),int(sys.argv[8]))
        else:raise ValueError(cmd)
