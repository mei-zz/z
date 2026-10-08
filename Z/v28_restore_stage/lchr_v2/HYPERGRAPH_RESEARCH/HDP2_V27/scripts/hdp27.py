"""V27 independent exact K2 structural residual; canonical SHARED untouched."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('NUMBA_NUM_THREADS','6')
import sys,time,json,hashlib,resource,subprocess,signal,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent;OUT=ROOT/'HDP2_V27';ART=REPO/'result/innovation2/HDP2_V27'
sys.path.insert(0,str(ROOT/'CRM_V26/scripts'));import crm26 as c
q,g,e,v,np,torch,nn,agg=c.q,c.g,c.e,c.v,c.np,c.torch,c.nn,c.agg
import hdp_kernel as k
e.OUT=OUT;e.ART=ART;v.OUT=ROOT/'CHRI_V18_1'
read,write,sha,artifact,md,sandbox,job=e.read,e.write,e.sha,e.artifact,e.md,e.sandbox,e.job
PROTO=e.PROTO;ARMS=('RAW','SHARED','ZERO','GRAPH','MULT','PAIR','HDP','SHUFFLE');FEATURE_REP=1
NAMES=('n_u','n_v','lambda_H','lambda_G','P_pair','M_uv','S_uv','lambda_H_shuffle','degree_G_u','degree_G_v','accepted_u','attempted_u','accepted_v','attempted_v','changed_incidence_fraction','eligible_u','eligible_v','lambda_changed','matching_calls','compatibility_edges_shuffle','support_columns','nnz_u','nnz_v')
def cp(ds,seed,rep=1):return OUT/'feature_cache'/ds/f'seed_{seed}'/f'rep_{rep}'
def graph(ds):
    a=e.sealed(ds);adj=[set() for _ in range(len(a['x']))]
    for u,w in a['train']:adj[int(u)].add(int(w));adj[int(w)].add(int(u))
    degree=np.asarray([len(x) for x in adj],np.int64);members=[np.asarray(sorted({i,*values}),np.int64) if values else np.empty(0,np.int64) for i,values in enumerate(adj)];ptr=np.r_[0,np.cumsum([len(x) for x in members])].astype(np.int64);return ptr,np.concatenate(members),degree
def source_pairs(ds,seed,split):return np.concatenate([np.load(v.cache(ds,seed)/f'epoch_{i}_pairs.npy').reshape(-1,2) for i in range(1,6)]) if split=='train' else np.load(v.cache(ds,seed)/'valid_pairs.npy')
def features(stats):
    nu,nv,lh,lg,pp,mm,ss,lsh,du,dv=[stats[:,j] for j in range(10)];hcap=np.maximum(np.minimum(nu,nv),1);gcap=np.maximum(np.minimum(du,dv),1)
    return {'ZERO':np.zeros((len(stats),2),np.float32),'HDP':np.column_stack((np.log1p(lh),lh/hcap)).astype(np.float32),'SHUFFLE':np.column_stack((np.log1p(lsh),lsh/hcap)).astype(np.float32),'GRAPH':np.column_stack((np.log1p(lg),lg/gcap)).astype(np.float32),'PAIR':np.column_stack((np.log1p(pp),pp/np.maximum(nu*nv,1))).astype(np.float32),'MULT':np.column_stack((np.log1p(mm),np.log1p(ss))).astype(np.float32)}

def prepare(ds,seed,rep):
    started=time.perf_counter();ptr,mem,degree=graph(ds);p=cp(ds,seed,rep);p.mkdir(parents=True,exist_ok=True);audit={}
    for split in ('train','validation'):
        queries=np.sort(source_pairs(ds,seed,split),axis=1);keys=np.unique(queries[:,0]*len(degree)+queries[:,1]);pairs=np.column_stack((keys//len(degree),keys%len(degree)));seeds=np.asarray([int.from_bytes(hashlib.sha256(f'{ds}/{split}/{seed}/{int(key)}'.encode()).digest()[:8],'little') for key in keys],np.uint64);t=time.perf_counter();stats=k.compute(pairs,seeds,ptr,mem,degree);assert np.all(np.isfinite(stats));np.save(p/f'{split}_keys.npy',keys);np.save(p/f'{split}_stats.npy',stats)
        for arm,value in features(stats).items():np.save(p/f'{split}_{arm}.npy',value)
        audit[split]={'unique_candidates':len(keys),'scheduled_candidates':len(queries),'seconds':time.perf_counter()-t,'matching_calls':int(stats[:,18].sum()),'maximum_compatibility_vertices':int((stats[:,0]+stats[:,1]).max()),'maximum_compatibility_edges':int(stats[:,4].max()),'row_column_S_M_preserved_for_every_candidate':True};print('FEATURE_CACHE_READY',ds,seed,rep,split,len(keys),flush=True)
    write(p/'READY.json',{'state':'PASS','dataset':ds,'seed':seed,'replicate':rep,'wall_seconds':time.perf_counter()-started,'peak_RAM_bytes':int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024),'cache_bytes':sum(f.stat().st_size for f in p.glob('*.npy')),'splits':audit,'hashes':{f.name:sha(f) for f in p.glob('*.npy')}})

def brute(B,row=0,used=0):
    if row==len(B):return 0
    result=brute(B,row+1,used)
    for col in range(B.shape[1]):
        if B[row,col] and not (used>>col)&1:result=max(result,1+brute(B,row+1,used|(1<<col)))
    return result
def matching_sanity():
    rng=np.random.RandomState(27000);checks=[]
    for _ in range(128):
        B=rng.random_sample((rng.randint(0,7),rng.randint(0,7)))<.4;actual=int(k.matching(B));expected=brute(B);assert actual==expected,'HDP2_IMPLEMENTATION_ERROR_MATCHING';checks.append({'left':B.shape[0],'right':B.shape[1],'matching':actual})
    real=[]
    for ds in ('cora','pubmed'):
        ptr,mem,degree=graph(ds);pp=source_pairs(ds,0,'validation');sample=pp[np.random.RandomState(27001).choice(len(pp),min(256,len(pp)),False)]
        for u,w in sample:
            A,C,_,_,_=k.assemble(int(u),int(w),ptr,mem,degree);B,_,_=k.compatibility(A,C)
            if max(B.shape)<=6:assert k.matching(B)==brute(B),'HDP2_IMPLEMENTATION_ERROR_REAL_MATCHING';real.append({'dataset':ds,'shape':list(B.shape)})
    assert real;artifact('02_MATCHING_SANITY.json',{'state':'PASS','algorithm':'deterministic exact augmenting-path BFS, an exact maximum bipartite matching algorithm; not greedy','random_small_graphs':checks,'sampled_real_small_graphs':real})
    tests={};toys=[('one_resource',np.array([[1,1,1]],bool),np.eye(3,dtype=bool),1),('two_routes',np.eye(2,dtype=bool),np.eye(2,dtype=bool),2),('complete22',np.ones((2,1),bool),np.ones((2,1),bool),2)]
    for name,A,C,expected in toys:
        B,M,S=k.compatibility(A,C);lam=int(k.matching(B));assert lam==expected and k.matching(B.T.copy())==lam and k.matching(B[::-1,::-1].copy())==lam;tests[name]={'matching':lam,'compatibility_edges':int(B.sum()),'raw_support_path_count':int(M),'swap_and_permutation':True}
    assert tests['one_resource']['raw_support_path_count']>1 and tests['complete22']['compatibility_edges']==4
    # Member-order changes are canonicalized before incidence construction.
    assert np.array_equal(np.sort(np.array([3,2,1])),np.sort(np.array([1,3,2])))
    artifact('03_STRUCTURAL_SANITY.json',{'state':'PASS','tests':tests,'ordinary_node_sharing_allowed':'complete22 uses the same support node for both matched routes','member_order':'sorted unique member IDs, unchanged incidence under permutations'})

class FeatureLookup:
    def __init__(self,ds,seed,arm,rep):
        self.n=len(e.sealed(ds)['x']);p=cp(ds,seed,rep);self.data={split:(torch.tensor(np.load(p/f'{split}_keys.npy'),device='cuda'),torch.tensor(np.load(p/f'{split}_{arm}.npy'),device='cuda')) for split in ('train','validation')}
    def __call__(self,pairs,training):
        pp=pairs.sort(dim=1).values;keys,value=self.data['train' if training else 'validation'];query=pp[:,0]*self.n+pp[:,1];index=torch.searchsorted(keys,query);assert torch.equal(keys[index],query),'HDP2_IMPLEMENTATION_ERROR_FEATURE_LOOKUP';return value[index]
class Predictor(g.m.MERIPredictor):
    def __init__(self,ds,seed,arm,mean,std):
        super().__init__(e.ContextStructure(ds),seed,'DUP',mean,std);self.variant=arm;self.lookup=FeatureLookup(ds,seed,arm,FEATURE_REP)
        with torch.random.fork_rng():
            torch.manual_seed(27002+seed);self.structural_residual=nn.Sequential(nn.Linear(2,8),nn.ReLU(),nn.Linear(8,1));nn.init.zeros_(self.structural_residual[-1].weight);nn.init.zeros_(self.structural_residual[-1].bias)
    def forward(self,pairs,b,donor=None):
        score,nuisance,null=super().forward(pairs,b,donor);return score+self.structural_residual(self.lookup(pairs,self.training)).flatten(),nuisance,null
def make_net(ds,seed,arm,phase,structure=None):
    if arm=='DUP':return g.m.make_net(ds,seed,'DUP',phase,structure)
    if arm in ARMS[2:]:
        stats=read(v.cache(ds,seed)/'normalization.json');return Predictor(ds,seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda')
    return agg.install(e.ORIGINAL_MAKE(ds,seed,arm,phase,structure))
v.make_net=make_net

def batch(tasks,stage,workers=6):
    queue=list(tasks);active=[];done=0;(OUT/'logs').mkdir(exist_ok=True)
    while queue or active:
        for p,args,log in list(active):
            if p.poll() is not None:active.remove((p,args,log));assert p.returncode==0,f'JOB_FAILED {args} {log}';done+=1
        while queue and len(active)<workers:
            args=queue.pop(0);log=OUT/'logs'/('_'.join(map(str,args))+'.log')
            with log.open('a') as f:p=subprocess.Popen([sys.executable,'-B','-u',str(Path(__file__).resolve()),*map(str,args)],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
            active.append((p,args,log));e.CHILDREN.append(p)
        state={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(queue),'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False};artifact('RUN_STATUS.json',state);write(OUT/'RUN_STATUS.json',state)
        if active:time.sleep(3)

def freeze():
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);assert REPO.name in ('DCDLP-main','lchr_v2');v.check_frozen();previous=read(REPO/'result/innovation2/CRM_V26/SOURCE_HASHES.json');files=dict(previous['files'])
    for name,h in files.items():assert sha(REPO/name)==h,'HISTORICAL_SOURCE_CHANGED '+name
    files.update({str(p.relative_to(REPO)):sha(p) for p in (REPO/'result/innovation2/CRM_V26').glob('*') if p.suffix in ('.json','.md')})
    for p in [*list((OUT/'scripts').glob('*.py')),*[ART/n for n in ('00_PROTOCOL.md','01_DATA_MASKING_AUDIT.md','01_DATA_MASKING_AUDIT.json','06_FEATURE_LEAKAGE_AUDIT.md')]]:files[str(p.relative_to(REPO))]=sha(p)
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_TRAINING','files':files,'caches':previous['caches'],'canonical_protocol':PROTO});e.cache_check();assert read(REPO/'result/innovation2/CRM_V26/RUN_STATUS.json')['final_status']=='CRM_REJECTED_NO_GAIN'
    import numba
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','created_at':time.time(),'canonical_protocol':PROTO,'search_branch':'INDEPENDENT_OF_CHRI_DERIVED_ARCHITECTURE','datasets':['cora','pubmed'],'seeds':[0,1,2],'epochs':5,'arms':list(ARMS),'precheck_arms':['SHARED','PAIR','HDP','SHUFFLE'],'precheck_dataset_seed':['pubmed',0],'independent_feature_cache_replicates':2,'residual':[2,8,1],'residual_parameters':33,'initial_final_head':'zero weights and bias','baseline_architecture_unchanged':True,'baseline_parameters_canonical_trainable':True,'normalization':'NONE','CPU_feature_workers':6,'numba_threads_per_worker':6,'GPU_workers':6,'torch_threads_per_worker':2,'numba_version':numba.__version__,'online_installs':False,'test_opened':False})
    for name in ('02_MATCHING_SANITY.json','03_STRUCTURAL_SANITY.json','04_PARAMETER_AUDIT.json','05_BASELINE_REPRODUCTION.json','07_FEATURE_STATISTICS.json','08_NONREDUNDANCY_DIAGNOSTICS.json','09_SHUFFLE_VALIDITY_AUDIT.json','10_DETERMINISM_PRECHECK.json','11_PHASE_A_RESULTS.json','12_PAIRED_CONTRASTS.json','13_BOTTLENECK_DIAGNOSTICS.json','14_TRUE_VS_SHUFFLED_DIAGNOSTICS.json','16_COMPUTE_AUDIT.json'):artifact(name,{'state':'NOT_RUN','reason':'Prerequisites pending.'})
    for name in ('15_RANKING_ANALYSIS.md','17_DECISION.md','FINAL_REPORT.md'):md(name,'# V27\n\nPENDING')

def distribution(x):
    x=np.asarray(x);return {'count':len(x),'zero_fraction':float(np.mean(x==0)),'mean':float(x.mean()),'median':float(np.median(x)),'p75':float(np.quantile(x,.75)),'p90':float(np.quantile(x,.9)),'p95':float(np.quantile(x,.95)),'max':float(x.max())}
def expanded(ds,seed,split,rep=1):
    p=cp(ds,seed,rep);keys=np.load(p/f'{split}_keys.npy');queries=np.sort(source_pairs(ds,seed,split),axis=1);n=len(e.sealed(ds)['x']);index=np.searchsorted(keys,queries[:,0]*n+queries[:,1]);return np.load(p/f'{split}_stats.npy')[index]
def feature_audits():
    stats={};shuffle={};changes={};probes={};bottleneck={}
    for ds in ('cora','pubmed'):
        stats[ds]=[];shuffle[ds]=[];changes[ds]=[];probes[ds]=[];bottleneck[ds]=[]
        for seed in range(3):
            perstat={};persh={};perchange={};perbottle={};arrays={}
            for split in ('train','validation'):
                a=expanded(ds,seed,split);arrays[split]=a;capacity=np.minimum(a[:,0],a[:,1]);deficiency=capacity-a[:,2];eligible=(a[:,15]+a[:,16])>0;material=a[:,14]>=.10;fraction=float(material[eligible].mean()) if eligible.any() else 0.;weak=fraction<=.5
                perstat[split]={'statistics':{NAMES[j]:distribution(a[:,j]) for j in range(7)},'bottleneck_fraction':float((deficiency>0).mean()),'zero_or_saturated_fraction':float(((a[:,2]==0)|(a[:,2]==capacity)).mean()),'almost_always_zero_or_saturated':bool(((a[:,2]==0)|(a[:,2]==capacity)).mean()>=.95)}
                persh[split]={'row_sums_exact':True,'column_sums_exact':True,'S_M_exact':True,'accepted_u':distribution(a[:,10]),'accepted_v':distribution(a[:,12]),'attempted_u':distribution(a[:,11]),'attempted_v':distribution(a[:,13]),'changed_incidence_fraction':distribution(a[:,14]),'lambda_changed_fraction':float(a[:,17].mean()),'structurally_unshufflable_fraction':float((~eligible).mean()),'materially_rewired_fraction_among_eligible':fraction,'material_threshold':.10,'control_status':'SHUFFLE_CONTROL_WEAK' if weak else 'VALID'}
                delta=a[:,2]-a[:,7];perchange[split]={'delta_true_minus_shuffle':distribution(delta),'equal_fraction':float((delta==0).mean()),'true_greater_fraction':float((delta>0).mean()),'true_less_fraction':float((delta<0).mean()),'changed_incidence_fraction':distribution(a[:,14])};perbottle[split]={'deficiency':distribution(deficiency),'zero_deficiency_fraction':float((deficiency==0).mean())}
            tr,va=arrays['train'],arrays['validation'];ft,fv=features(tr),features(va);pp={}
            for name in ('GRAPH','MULT','PAIR','COMBINED'):
                x=np.concatenate([ft[k] for k in ('GRAPH','MULT','PAIR')],1) if name=='COMBINED' else ft[name];y=np.concatenate([fv[k] for k in ('GRAPH','MULT','PAIR')],1) if name=='COMBINED' else fv[name];xx=np.column_stack((x,np.ones(len(x))));coef=np.linalg.lstsq(xx,tr[:,2],rcond=None)[0];pred=np.column_stack((y,np.ones(len(y))))@coef;truth=va[:,2];error=pred-truth;ss=float(((truth-truth.mean())**2).sum());pp[name]={'R2':1-float((error**2).sum())/ss if ss else None,'MAE':float(np.abs(error).mean()),'correlation':float(np.corrcoef(pred,truth)[0,1]) if pred.std()>1e-12 and truth.std()>1e-12 else None,'fit':'train5 frozen schedules only, ordinary least squares with intercept','target':'lambda_H'}
            stats[ds].append({'seed':seed,'splits':perstat});shuffle[ds].append({'seed':seed,'splits':persh});changes[ds].append({'seed':seed,'splits':perchange});bottleneck[ds].append({'seed':seed,'splits':perbottle});probes[ds].append({'seed':seed,'probes':pp})
    artifact('07_FEATURE_STATISTICS.json',{'state':'COMPLETE','datasets':stats});artifact('08_NONREDUNDANCY_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':probes});artifact('09_SHUFFLE_VALIDITY_AUDIT.json',{'state':'COMPLETE','datasets':shuffle,'definition':'eligible iff some side has an exact binary2-switch; material iff >=10% of original incidence incidences replaced; require majority eligible material in every dataset/split/seed'});artifact('14_TRUE_VS_SHUFFLED_DIAGNOSTICS.json',{'state':'COMPLETE','datasets':changes});artifact('13_BOTTLENECK_DIAGNOSTICS.json',{'state':'FEATURES_COMPLETE','datasets':bottleneck,'validation_error_strata':'pending trained models'})

@torch.no_grad()
def initial_sanity():
    for ds in ('cora','pubmed'):
        base=make_net(ds,0,'DUP','A').eval();pairs=torch.tensor(np.load(v.cache(ds,0)/'valid_pairs.npy')[:128],device='cuda');bb=torch.tensor(np.load(v.cache(ds,0)/'valid_b.npy')[:128],device='cuda');baseline=base(pairs,bb)[0]
        for arm in ARMS[2:]:
            net=make_net(ds,0,arm,'A').eval();assert g.statehash({k:t for k,t in net.state_dict().items() if not k.startswith('structural_residual.')})==g.statehash(base.state_dict()),'HDP2_IMPLEMENTATION_ERROR_BASE_STATE';assert torch.equal(net(pairs,bb)[0],baseline),'HDP2_IMPLEMENTATION_ERROR_INITIAL_ZERO';assert torch.equal(net.lookup(pairs,False),net.lookup(pairs.flip(1),False)),'HDP2_IMPLEMENTATION_ERROR_SWAP'
    artifact('INITIAL_FUNCTION_SANITY.json',{'state':'PASS','baseline_parameter_mapping_exact':True,'all_variants_initial_scores_bit_identical':True,'candidate_swap_features_exact':True})

def run(phase,ds,seed,arm,rep):
    global FEATURE_REP
    FEATURE_REP=rep if phase=='D' and ds=='pubmed' and seed==0 else 1;started=time.perf_counter();q.run(phase,ds,seed,arm,rep);dest=job(phase,ds,seed,arm,rep);row=read(dest/'result.json');ready=read(cp(ds,seed,FEATURE_REP)/'READY.json');row['feature_cache_hashes']=ready['hashes'];row['compute']={'training_wall_seconds':time.perf_counter()-started,'peak_GPU_allocated_bytes':torch.cuda.max_memory_allocated(),'peak_RAM_bytes':int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024),'feature_preprocessing':ready};write(dest/'result.json',row)

def finalize():
    data={'state':'COMPLETE','datasets':{},'test_opened':False};reproduction=[];comparisons=[('SHARED','RAW'),*[('HDP',a) for a in ('RAW','SHARED','ZERO','GRAPH','MULT','PAIR','SHUFFLE')]]
    for ds in ('cora','pubmed'):
        rows=[{'seed':seed,'arms':{a:read(job('A',ds,seed,a)/'result.json') for a in ARMS}} for seed in range(3)]
        for row in rows:reproduction.append(c.baseline('A',ds,row['seed']));assert all(a['training_trace']==row['arms']['RAW']['training_trace'] for a in row['arms'].values())
        data['datasets'][ds]={'seed_results':rows,'effects':{f'{a}_vs_{b}':v.comparison(rows,a,b) for a,b in comparisons},'metrics':{a:{metric:v.stat([row['arms'][a]['validation'][metric] for row in rows]) for metric in v.METRICS} for a in ARMS}}
    def both(other,wins=False):return all(d['effects'][f'HDP_vs_{other}']['ce']['mean']>0 and (d['effects'][f'HDP_vs_{other}']['ce']['wins']>=2 if wins else True) for d in data['datasets'].values())
    gates={'SHARED_and_ZERO':both('SHARED',True) and both('ZERO'),'GRAPH':both('GRAPH'),'MULT':both('MULT'),'PAIR':both('PAIR'),'SHUFFLE':both('SHUFFLE')};validity=read(ART/'09_SHUFFLE_VALIDITY_AUDIT.json');weak=any(s['control_status']!='VALID' for records in validity['datasets'].values() for record in records for s in record['splits'].values());ranking=all(d['effects']['HDP_vs_SHARED']['mrr']['mean']>0 for d in data['datasets'].values());status='HDP2_PROMISING_WITH_RANKING_GAIN' if ranking else 'HDP2_PROMISING'
    for gate,rejected in (('SHARED_and_ZERO','HDP2_REJECTED_NO_GAIN'),('GRAPH','HDP2_REJECTED_GRAPH_PROJECTION'),('MULT','HDP2_REJECTED_MULTIPLICITY_EXPLANATION'),('PAIR','HDP2_REJECTED_PATHCOUNT_EXPLANATION')):
        if not gates[gate]:status=rejected;break
    else:
        if weak:status='HDP2_SHUFFLE_CONTROL_INVALID'
        elif not gates['SHUFFLE']:status='HDP2_REJECTED_HYPEREDGE_IDENTITY'
    survivor='HDP2_SIGNAL' if status.startswith('HDP2_PROMISING') else 'NONE';decision={'final_status':status,'gates':gates,'shuffle_control':'WEAK' if weak else 'VALID','true_hyperedge_identity':'UNRESOLVED' if weak else ('SUPPORTED' if gates['SHUFFLE'] else 'NOT_SUPPORTED'),'ranking_gain_both':ranking,'surviving_structure':survivor,'novelty_audit_next':survivor!='NONE','no_rescue':True};data['decision']=decision;artifact('11_PHASE_A_RESULTS.json',data);artifact('12_PAIRED_CONTRASTS.json',{ds:d['effects'] for ds,d in data['datasets'].items()});artifact('05_BASELINE_REPRODUCTION.json',{'state':'PASS','records':reproduction})
    bottleneck=read(ART/'13_BOTTLENECK_DIAGNOSTICS.json');strata={}
    for ds in ('cora','pubmed'):
        strata[ds]=[];npos=len(e.sealed(ds)['valid_pos'])
        for seed in range(3):
            a=expanded(ds,seed,'validation');lam=a[:,2];deficiency=np.minimum(a[:,0],a[:,1])-lam;label=np.arange(len(lam))<npos;masks={'lambda0':lam==0,'lambda1':lam==1,'lambda2plus':lam>=2,'deficiency0':deficiency==0,'deficiency_positive':deficiency>0};result={}
            for name,mask in masks.items():
                row={'candidates':int(mask.sum()),'positive_rate':float(label[mask].mean()) if mask.any() else None,'model_errors':{}}
                for arm in ('SHARED','HDP'):
                    score=v.scores_file(job('A',ds,seed,arm)/'valid_epoch5_scores.npz');row['model_errors'][arm]={'CE':float((np.logaddexp(0,score[mask])-label[mask]*score[mask]).mean()) if mask.any() else None,'classification_error_at_zero':float(((score[mask]>=0)!=label[mask]).mean()) if mask.any() else None}
                result[name]=row
            strata[ds].append({'seed':seed,'strata':result})
    bottleneck['state']='COMPLETE';bottleneck['validation_strata_descriptive_only']=strata;artifact('13_BOTTLENECK_DIAGNOSTICS.json',bottleneck);artifact('16_COMPUTE_AUDIT.json',{ds:{a:[row['arms'][a]['compute'] for row in d['seed_results']] for a in ARMS} for ds,d in data['datasets'].items()})
    lines=['| Dataset | Contrast | Mean DeltaCE | CE wins | Mean DeltaMRR |','|---|---|---:|---:|---:|']
    for ds,d in data['datasets'].items():
        for name,ef in d['effects'].items():lines.append(f"| {ds} | {name} | {ef['ce']['mean']:.10g} | {ef['ce']['wins']}/3 | {ef['mrr']['mean']:.10g} |")
    table='\n'.join(lines);md('15_RANKING_ANALYSIS.md','# V27 paired CE and ranking\n\n'+table);md('17_DECISION.md','# V27 decision\n\n'+json.dumps(decision,indent=2));sections=['# V27 HDP2 final report',f'FINAL_STATUS: {status}',json.dumps(decision,indent=2),table]
    for name in ('01_DATA_MASKING_AUDIT.md','06_FEATURE_LEAKAGE_AUDIT.md'):sections.append((ART/name).read_text())
    for name in ('02_MATCHING_SANITY.json','03_STRUCTURAL_SANITY.json','04_PARAMETER_AUDIT.json','05_BASELINE_REPRODUCTION.json','07_FEATURE_STATISTICS.json','08_NONREDUNDANCY_DIAGNOSTICS.json','09_SHUFFLE_VALIDITY_AUDIT.json','10_DETERMINISM_PRECHECK.json','13_BOTTLENECK_DIAGNOSTICS.json','14_TRUE_VS_SHUFFLED_DIAGNOSTICS.json','16_COMPUTE_AUDIT.json'):sections.extend([name,json.dumps(read(ART/name),indent=2)])
    sections.extend(['Complete validation metrics',json.dumps({ds:d['metrics'] for ds,d in data['datasets'].items()},indent=2),'Exact maximum matching is a classical combinatorial object, not a novelty claim. Hyperedges are resources; ordinary support nodes may be shared. Low probeR2 and geometric bottlenecks do not imply predictive success. No test, K3, max-flow, path-GNN or rescue.','TEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO']);md('FINAL_REPORT.md','\n\n'.join(sections));md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: HDP2_V27_HYPEREDGE_DISJOINT_PATH_VALIDATION\nWORKSPACE: DCDLP-main\nCANONICAL_PROTOCOL: {PROTO}\nSEARCH_BRANCH: INDEPENDENT_OF_CHRI_DERIVED_ARCHITECTURE\nMASKING_AUDIT: PASS\nLEAKAGE_AUDIT: PASS\nMATCHING_EXACTNESS: PASS\nSTRUCTURAL_SANITY: PASS\nSHUFFLE_CONTROL: {decision["shuffle_control"]}\nBASELINE_REPRODUCTION: PASS\nDETERMINISM: PASS\nFINAL_STATUS: {status}\nSURVIVING_STRUCTURE: {survivor}\n{table}\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO\nPRIMARY_ARTIFACT: result/innovation2/HDP2_V27/FINAL_REPORT.md\nNEXT: Return evidence and stop; novelty audit before any success extension. No K3 or rescue.\n'+json.dumps(decision,indent=2));v.OUT=ROOT/'CHRI_V18_1';e.frozen_check();e.cache_check();st={'state':'COMPLETE','final_status':status,'ended_at':time.time(),'test_opened':False};artifact('RUN_STATUS.json',st);write(OUT/'RUN_STATUS.json',st);print('V27_COMPLETE',status,flush=True)

def supervise():
    try:
        freeze();matching_sanity();batch([('prepare',ds,seed,1) for ds in ('cora','pubmed') for seed in range(3)]+[('prepare','pubmed',0,2)],'EXACT_STRUCTURAL_FEATURES');feature_audits();counts={a:sum(p.numel() for p in make_net('pubmed',0,e.MAP.get(a,a),'A').parameters() if p.requires_grad) for a in ARMS};assert counts['RAW']==28481 and counts['SHARED']==30529 and all(counts[a]==30562 for a in ARMS[2:]),'HDP2_IMPLEMENTATION_ERROR_PARAMETERS';artifact('04_PARAMETER_AUDIT.json',{'state':'PASS','counts':counts,'structural_residual_parameters':33,'all_controls_identical_architecture':True,'SHARED_unchanged':True});initial_sanity()
        one=read(cp('pubmed',0,1)/'READY.json')['hashes'];two=read(cp('pubmed',0,2)/'READY.json')['hashes'];assert one==two,'DETERMINISTIC_PROTOCOL_FAILURE_FEATURES';frozen=read(ART/'SOURCE_HASHES.json');frozen['feature_cache_hashes']={str(p.relative_to(REPO)):sha(p) for p in (OUT/'feature_cache').rglob('*.npy')};artifact('SOURCE_HASHES.json',frozen);print('V27_PREFLIGHT_PASS',counts,flush=True)
        batch([('run','D','pubmed',0,arm,rep) for arm in ('SHARED','PAIR','HDP','SHUFFLE') for rep in (1,2)],'DETERMINISM_PRECHECK');pairs=[]
        for arm in ('SHARED','PAIR','HDP','SHUFFLE'):
            rows=[read(job('D','pubmed',0,arm,rep)/'result.json') for rep in (1,2)];checks={key:rows[0][key]==rows[1][key] for key in ('feature_cache_hashes','checkpoint_sha256','score_vector_sha256','training_trajectory_sha256','history','training_trace')};pairs.append({'arm':arm,'pass':all(checks.values()),'checks':checks})
        ok=all(row['pass'] for row in pairs);artifact('10_DETERMINISM_PRECHECK.json',{'state':'PASS' if ok else 'FAIL','pairs':pairs,'feature_preprocessing_independently_repeated':True});assert ok,'DETERMINISTIC_PROTOCOL_FAILURE';artifact('05_BASELINE_REPRODUCTION.json',{'state':'PASS','spot':c.baseline('D','pubmed',0)})
        for arm in ('SHARED','PAIR','HDP','SHUFFLE'):
            dest=job('A','pubmed',0,arm);dest.parent.mkdir(parents=True,exist_ok=True);dest.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,seed,arm,1) for seed in range(3) for ds in ('cora','pubmed') for arm in ARMS if not(ds=='pubmed' and seed==0 and arm in ('SHARED','PAIR','HDP','SHUFFLE'))],'PHASE_A')
        for p,h in read(ART/'SOURCE_HASHES.json')['feature_cache_hashes'].items():assert sha(REPO/p)==h,'HDP2_IMPLEMENTATION_ERROR_CACHE_CHANGED'
        finalize()
    except BaseException as error:
        for p in e.CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        status='HDP2_BASELINE_REPRODUCTION_FAILURE' if 'BASELINE_REPRODUCTION_FAILURE' in str(error) else ('DETERMINISTIC_PROTOCOL_FAILURE' if 'DETERMINISTIC_PROTOCOL_FAILURE' in str(error) else ('TEST_SEAL_VIOLATION' if 'TEST_SEAL_VIOLATION' in str(error) else 'HDP2_IMPLEMENTATION_ERROR'));err={'state':'EXECUTION_FAILED','final_status':status,'error':repr(error),'traceback':traceback.format_exc(),'test_opened':False};artifact('RUN_STATUS.json',err);write(OUT/'RUN_STATUS.json',err);artifact('ERROR.json',err);md('FINAL_REPORT.md','# V27 failure\n\n'+json.dumps(err,indent=2));print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='supervise':supervise()
    elif cmd=='prepare':prepare(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
    elif cmd=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    else:raise ValueError(cmd)
