"""V25: fixed local set replacement, same canonical H/phi/decoder/trainer."""
import os
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(k,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import sys,time,json,hashlib,subprocess,traceback,signal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent;OUT=ROOT/'RER_V25';ART=REPO/'result/innovation2/RER_V25'
sys.path.insert(0,str(ROOT/'RELREUSE_V24/scripts'));import reuse24 as q
g,e,v,np,torch,nn,agg=q.g,q.e,q.v,q.np,q.torch,q.nn,q.agg
e.OUT=OUT;e.ART=ART
read,write,sha,artifact,md,sandbox,job=e.read,e.write,e.sha,e.artifact,e.md,e.sandbox,e.job
ARMS=('Z','RAW','SHARED','U','V','ONE','BI','SHUFFLE');PROTO=e.PROTO;CURRENT=None
v.OUT=ROOT/'CHRI_V18_1'
def cp(ds,seed,split):return OUT/'local_cache'/ds/f'seed_{seed}'/split
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);np.save(p,x)

def prepare(ds,seed):
    """Fixed descriptors only: recompute learned H every optimizer step."""
    a=e.sealed(ds);n=len(a['x']);adj=[set() for _ in range(n)]
    for u,w in a['train']:adj[int(u)].add(int(w));adj[int(w)].add(int(u))
    mem=[np.array(sorted({i,*adj[i]}),np.int64) if adj[i] else np.empty(0,np.int64) for i in range(n)]
    with np.load(v.cache(ds)/'structure.npz') as z:s={k:z[k] for k in z.files}
    from threadpoolctl import threadpool_limits
    from chri_features import array_hash
    with threadpool_limits(limits=4,user_api='blas'):node=(np.asarray(a['x']@s['projection'],np.float32)-s['normalization_mean'])/s['normalization_std']
    assert array_hash(node)==read(v.cache(ds)/'STRUCTURE_READY.json')['projected_node_hash'],'RER_IMPLEMENTATION_ERROR_NODE'
    assert np.array_equal(np.stack([e.descriptor(node,m) for m in mem]),s['raw']),'RER_IMPLEMENTATION_ERROR_RAW_RECONSTRUCTION'
    degree=s['degree'];quart=np.quantile(degree[degree>0]+1,[.25,.5,.75]);db=np.minimum(np.floor(np.log2(np.maximum(degree,1))).astype(int),3);ib=np.searchsorted(quart,degree+1,side='right')
    audits={};sanity=[]
    for split in ('train','validation'):
        arrays=[np.load(v.cache(ds,seed)/f'epoch_{i}_pairs.npy').reshape(-1,2) for i in range(1,6)] if split=='train' else [np.load(v.cache(ds,seed)/'valid_pairs.npy')]
        allpairs=np.sort(np.concatenate(arrays),axis=1);keys=np.unique(allpairs[:,0]*n+allpairs[:,1]);pairs=np.column_stack((keys//n,keys%n));path=cp(ds,seed,split);save(path/'keys.npy',keys)
        pools={}
        for index,(u,w) in enumerate(pairs):
            for endpoint in (u,w):pools.setdefault((int(db[endpoint]),int(ib[endpoint])),{}).setdefault(int(endpoint),index)
        pools={k:list(val.items()) for k,val in pools.items()}
        out={k:[] for k in ('true0','true1','shuffle0','shuffle1','self0','self1','collision0','collision1','change0','change1')};offsets=[[],[]];donors=[];tokens=coll=cc=0;agreements=0
        for index,(u,w) in enumerate(pairs):
            u,w=int(u),int(w);target=w in adj[u];row=int(np.searchsorted(s['keys'],u*n+w));anycoll=False;donorpair=[]
            for side,(focal,other) in enumerate(((u,w),(w,u))):
                pool=pools[(int(db[other]),int(ib[other]))];start=int.from_bytes(hashlib.sha256(f'{ds}/{seed}/{split}/{u}/{w}/{side}'.encode()).digest()[:8],'little')%len(pool);donor=None
                for j in range(len(pool)):
                    value,di=pool[(start+j)%len(pool)]
                    if value not in (focal,other) and di!=index:donor=value;break
                assert donor is not None,'RER_IMPLEMENTATION_ERROR_NO_MATCHED_DONOR'
                donorpair.append(donor);agreements+=int(db[donor]==db[other] and ib[donor]==ib[other]);offsets[side].append(len(out[f'true{side}']))
                centers=s['incident'][focal];centers=centers[centers>=0];centers=centers[~((centers==other)&target)];centers=centers[~((centers==focal)&target&(degree[focal]==1))]
                for edge in centers:
                    original=mem[edge]
                    if target and edge==focal:original=original[original!=other]
                    assert focal in original
                    context=original[original!=focal];collision=other in context;virtual=np.union1d(context,[other]);shuffled=np.union1d(context,[donor]);selfmem=np.union1d(context,[focal]);selfraw=e.descriptor(node,selfmem)
                    expected=s['masked'][row,side] if target and edge==focal else s['raw'][edge]
                    assert np.array_equal(selfraw,expected),'RER_IMPLEMENTATION_ERROR_SELF_DESCRIPTOR'
                    out[f'true{side}'].append(e.descriptor(node,virtual));out[f'shuffle{side}'].append(e.descriptor(node,shuffled));out[f'self{side}'].append(selfraw);out[f'collision{side}'].append(collision);out[f'change{side}'].append(len(virtual)-len(original));tokens+=1;coll+=int(collision);anycoll|=collision
            donors.append(donorpair);cc+=int(anycoll)
        for side in (0,1):offsets[side].append(len(out[f'true{side}']));save(path/f'offset{side}.npy',np.asarray(offsets[side],np.int64))
        for k,values in out.items():save(path/(k+'.npy'),np.asarray(values,dtype=np.float32 if k.startswith(('true','shuffle','self')) else np.int8).reshape(-1,33) if k.startswith(('true','shuffle','self')) else np.asarray(values,np.int8))
        save(path/'donors.npy',np.asarray(donors,np.int64))
        # Schedule-weighted exact frequencies, retaining duplicate occurrences.
        ix=np.searchsorted(keys,allpairs[:,0]*n+allpairs[:,1]);weights=np.bincount(ix,minlength=len(keys));per_coll=np.zeros(len(keys),np.int64);per_tokens=np.zeros(len(keys),np.int64)
        for side in (0,1):
            off=np.asarray(offsets[side]);c=np.asarray(out[f'collision{side}']);pref=np.r_[0,np.cumsum(c)];per_coll+=pref[off[1:]]-pref[off[:-1]];per_tokens+=np.diff(off)
        audits[split]={'unique_candidates':len(keys),'scheduled_candidates':len(allpairs),'scheduled_hyperedges':int(weights@per_tokens),'hyperedge_collision_rate':float((weights@per_coll)/max(weights@per_tokens,1)),'candidate_collision_rate':float((weights@(per_coll>0))/max(len(allpairs),1)),'unique_hyperedge_collision_rate':coll/max(tokens,1),'cardinality_change':'-1 iff counterpart already belongs to context, otherwise0','matching_degree_and_incidence_bucket_agreement':agreements/(2*len(keys)),'changed_counterparts':2*len(keys),'donors_same_split':True,'label_matching':False,'self_descriptor_bit_identity':True}
        print('CACHE_PREPARED',ds,seed,split,len(keys),tokens,flush=True)
    write(OUT/'cache_audits'/ds/f'seed_{seed}.json',{'state':'PASS','dataset':ds,'seed':seed,'splits':audits,'projection_and_full_descriptor_bit_identity':True})

class LocalStructure(v.Structure):
    def __init__(self,ds,seed):
        super().__init__(v.cache(ds)/'structure.npz');self.local={}
        for split in ('train','validation'):
            path=cp(ds,seed,split);self.local[split]={p.stem:np.load(p,mmap_mode='r') for p in path.glob('*.npy')}
    def virtual(self,pairs,side,split,kind):
        p=pairs.sort(dim=1).values.detach().cpu().numpy();cache=self.local[split];key=p[:,0]*self.n+p[:,1];ix=np.searchsorted(cache['keys'],key);assert np.array_equal(cache['keys'][ix],key)
        off=cache[f'offset{side}'];starts=off[ix];counts=off[ix+1]-starts;groups=np.repeat(np.arange(len(p)),counts);local=np.arange(int(counts.sum()))-np.repeat(np.cumsum(counts)-counts,counts);indices=starts[groups]+local
        data=np.asarray(cache[f'{kind}{side}'][indices]);return torch.tensor(data,device=pairs.device),counts

class Predictor(v.RelationPredictor):
    def __init__(self,structure,seed,arm,mean,std):
        super().__init__(structure,seed,'A2',mean,std);self.arm=arm;self.capture=False;self.diag={};self.virtual_count=0;self.self_mode=False;agg.install(self)
        base=self.decoder
        with torch.random.fork_rng():torch.manual_seed(21002+seed);ext=nn.Sequential(nn.Linear(385,64),nn.ReLU(),nn.Linear(64,32),nn.ReLU(),nn.Linear(32,1))
        with torch.no_grad():
            ext[0].weight[:,:353].copy_(base[0].weight);ext[0].bias.copy_(base[0].bias)
            for i in (2,4):ext[i].load_state_dict(base[i].state_dict())
        self.decoder=ext
    def forward(self,pairs,b,donor=None):
        z,raw=self.representation(pairs,b,True);hu,nu,_=self.endpoint(pairs,0);hv,nv,_=self.endpoint(pairs,1)
        split='train' if self.training else 'validation';kind='self' if self.self_mode else ('shuffle' if self.arm=='SHUFFLE' else 'true')
        du,cu=self.structure.virtual(pairs,0,split,kind);dv,cv=self.structure.virtual(pairs,1,split,kind);assert np.array_equal(cu,nu.cpu().numpy()) and np.array_equal(cv,nv.cpu().numpy())
        su,sv=self.encoder(du),self.encoder(dv);self.virtual_count+=len(du)+len(dv)
        sizes=nu*nv;count=int(sizes.sum());groups=torch.repeat_interleave(torch.arange(len(pairs),device=b.device),sizes);offset=sizes.cumsum(0)-sizes;local=torch.arange(count,device=b.device)-offset[groups];iu=(nu.cumsum(0)-nu)[groups]+torch.div(local,nv[groups],rounding_mode='floor');iv=(nv.cumsum(0)-nv)[groups]+local%nv[groups]
        bounds=[];st=0;running=0
        for row,n in enumerate(sizes.cpu().tolist()):
            if row>st and running+n>131072:bounds.append((st,row));st=row;running=0
            running+=n
        bounds.append((st,len(pairs)));parts=[];oneparts=[]
        for st,en in bounds:
            lo=int(offset[st]) if st<len(pairs) else count;hi=int(offset[en]) if en<len(pairs) else count;x,y=iu[lo:hi],iv[lo:hi]
            if self.arm=='U':token=self.relation(e.symmetric(su[x],hv[y]))
            elif self.arm=='V':token=self.relation(e.symmetric(hu[x],sv[y]))
            elif self.arm=='ONE':token=.5*(self.relation(e.symmetric(su[x],hv[y]))+self.relation(e.symmetric(hu[x],sv[y])))
            else:token=self.relation(e.symmetric(su[x],sv[y]))
            parts.append(e.pool(token,sizes[st:en]))
            if self.capture:oneparts.append(e.pool(.5*(self.relation(e.symmetric(su[x],hv[y]))+self.relation(e.symmetric(hu[x],sv[y]))),sizes[st:en]))
        r=torch.cat(parts);score=b[:,0]+self.decoder(torch.cat((z,raw,r),1)).flatten()
        if self.capture:
            normu=(su-hu).norm(dim=1);normv=(sv-hv).norm(dim=1);both=torch.cat((normu,normv));lengths=nu+nv
            # Concatenate side norms per candidate for candidate-contiguous reduction.
            seq=[];a0=c0=0
            for a,c in zip(nu.cpu().tolist(),nv.cpu().tolist()):seq.append(torch.cat((normu[a0:a0+a],normv[c0:c0+c])));a0+=a;c0+=c
            norms=torch.cat(seq);mean=torch.segment_reduce(norms,'sum',lengths=lengths)/lengths.clamp_min(1);maximum=torch.segment_reduce(norms,'max',lengths=lengths);maximum=torch.where(lengths>0,maximum,torch.zeros_like(maximum))
            self.diag={'z':z,'raw':raw,'bi':r,'one':torch.cat(oneparts),'mean_norm':mean,'max_norm':maximum,'relation_change':(r-raw).norm(dim=1),'u_norm':normu,'v_norm':normv,'u_cos':torch.nn.functional.cosine_similarity(su,hu),'v_cos':torch.nn.functional.cosine_similarity(sv,hv)}
        return score,b.new_zeros(()),b.new_zeros(())

def make_net(ds,seed,arm,phase,structure=None):
    global CURRENT
    if arm=='DUP':net=g.m.make_net(ds,seed,'DUP',phase,structure)
    elif arm in ('U','V','ONE','BI','SHUFFLE'):
        stats=read(v.cache(ds,seed)/'normalization.json');net=Predictor(structure or LocalStructure(ds,seed),seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda')
    else:net=agg.install(e.ORIGINAL_MAKE(ds,seed,arm,phase,structure))
    CURRENT=net;return net
v.make_net=make_net

def batch(tasks,stage,workers=6):
    queue=list(tasks);active=[];done=0;(OUT/'logs').mkdir(exist_ok=True)
    while active or queue:
        for p,args,log in list(active):
            if p.poll() is not None:
                active.remove((p,args,log));assert p.returncode==0,f'JOB_FAILED {args} {log}';done+=1
        while queue and len(active)<workers:
            args=queue.pop(0);log=OUT/'logs'/('_'.join(map(str,args))+'.log')
            with log.open('a') as f:p=subprocess.Popen([sys.executable,'-B','-u',str(Path(__file__).resolve()),*map(str,args)],stdout=f,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,start_new_session=True)
            active.append((p,args,log));e.CHILDREN.append(p)
        state={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'completed_stage_jobs':done,'queued':len(queue),'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],'updated_at':time.time(),'test_opened':False};write(OUT/'RUN_STATUS.json',state);artifact('RUN_STATUS.json',state)
        if active:time.sleep(3)

@torch.no_grad()
def sanity(ds):
    base=make_net(ds,0,'DUP','A').eval();net=make_net(ds,0,'BI','A').eval();net.capture=True;net.self_mode=True;assert g.statehash(base.state_dict())==g.statehash(net.state_dict()),'RER_IMPLEMENTATION_ERROR_MAPPED_STATE'
    pairs=torch.tensor(np.load(v.cache(ds,0)/'valid_pairs.npy')[:128],device='cuda');b=torch.tensor(np.load(v.cache(ds,0)/'valid_b.npy')[:128],device='cuda');left=base(pairs,b)[0];right=net(pairs,b)[0];z,raw=base.representation(pairs,b,True)
    checks={'self_relation_max_error':float((net.diag['bi']-raw).abs().max()),'self_hyperedge_u_max_error':float(net.diag['u_norm'].max()),'self_hyperedge_v_max_error':float(net.diag['v_norm'].max()),'self_shared_logit_max_error':float((left-right).abs().max())};assert max(checks.values())<1e-6,'RER_IMPLEMENTATION_ERROR_SELF'
    net.self_mode=False;score=net(pairs,b)[0];pooled=net.diag['bi'].clone();swapped=net(pairs.flip(1),b)[0];checks2={'pooled_max_error':float((pooled-net.diag['bi']).abs().max()),'logits_max_error':float((score-swapped).abs().max()),'orientation':'canonical sorted candidate order on both inputs'};assert max(checks2[k] for k in ('pooled_max_error','logits_max_error'))<1e-6,'RER_IMPLEMENTATION_ERROR_SWAP'
    shuffle=make_net(ds,0,'SHUFFLE','A').eval();shuffle.capture=True;shuffle(pairs,b);checks3={'same_Z':torch.equal(net.diag['z'],shuffle.diag['z']),'same_RAW':torch.equal(net.diag['raw'],shuffle.diag['raw']),'same_parameters':g.statehash(net.state_dict())==g.statehash(shuffle.state_dict()),'token_counts_unchanged':True};assert all(checks3.values()),'RER_IMPLEMENTATION_ERROR_SHUFFLE'
    write(OUT/'sanity'/f'{ds}.json',{'state':'PASS','self':checks,'swap':checks2,'shuffle':checks3,'test_opened':False})

def freeze():
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);v.OUT=ROOT/'CHRI_V18_1';v.check_frozen();previous=read(REPO/'result/innovation2/RELREUSE_V24/SOURCE_HASHES.json');files=dict(previous['files'])
    for p,h in files.items():assert sha(REPO/p)==h,'HISTORICAL_SOURCE_CHANGED '+p
    for directory in ('RELREUSE_V24','CHRI_V18_1C','CHRI_V18_1S','FCI_V19','RCP_V20','ERDR_V21','MERI_V22','GSIR_V23'):
        files.update({str(p.relative_to(REPO)):sha(p) for p in (REPO/'result/innovation2'/directory).glob('*') if p.suffix in ('.json','.md')})
    own=[Path(__file__),*[ART/n for n in ('00_PROTOCOL.md','01_SOURCE_AUDIT.md','01_SOURCE_AUDIT.json','02_LEAKAGE_AUDIT.md')]];files.update({str(p.relative_to(REPO)):sha(p) for p in own});artifact('SOURCE_HASHES.json',{'files':files,'caches':previous['caches'],'canonical_protocol':PROTO,'state':'FROZEN_BEFORE_TRAINING'});e.cache_check()
    assert read(ART/'01_SOURCE_AUDIT.json')['local_recomputation_applicable']
    assert read(REPO/'result/innovation2/RELREUSE_V24/RUN_STATUS.json')['state']=='COMPLETE'
    manifest={'state':'REGISTERED','canonical_protocol':PROTO,'datasets':['cora','pubmed'],'seeds':[0,1,2],'epochs':5,'arms':list(ARMS),'precheck':{'dataset':'pubmed','seed':0,'arms':['SHARED','ONE','BI','SHUFFLE'],'independent_replicates':2},'test_opened':False,'workers':6,'threads_per_worker':2,'optional_random':'NOT_RUN: primary matched shuffle sufficient; no delay','target_masking':'exact canonical training-visible candidate graph target removal before replacement','virtual_cache':'fixed descriptors only, no learned encoder state cached'};artifact('RUN_MANIFEST.json',manifest)
    for name in ('03_SUBSTITUTION_COLLISION_AUDIT.json','04_SUBSTITUTION_SANITY.json','05_PARAMETER_AUDIT.json','06_ENDPOINT_SWAP_INVARIANCE.json','07_DETERMINISM_PRECHECK.json','08_PHASE_A_RESULTS.json','09_PAIRED_CONTRASTS.json','10_SHUFFLE_CONTROL_AUDIT.json','11_SUBSTITUTION_DIAGNOSTICS.json','12_NONREDUNDANCY_PROBES.json','14_COMPUTE_AUDIT.json'):artifact(name,{'state':'NOT_RUN','reason':'Awaiting prerequisites.'})
    for name in ('13_RANKING_ANALYSIS.md','15_DECISION.md','FINAL_REPORT.md'):md(name,'# V25\n\nPENDING')

def run(phase,ds,seed,arm,rep):
    started=time.perf_counter();torch.cuda.reset_peak_memory_stats();q.run(phase,ds,seed,arm,rep);p=job(phase,ds,seed,arm,rep);row=read(p/'result.json');row['compute']={'training_and_reporting_wall_seconds':time.perf_counter()-started,'peak_GPU_allocated_bytes':torch.cuda.max_memory_allocated(),'virtual_hyperedge_recomputation_count':getattr(CURRENT,'virtual_count',0),'local_descriptor_cache_bytes':sum(p.stat().st_size for p in (OUT/'local_cache'/ds/f'seed_{seed}').rglob('*.npy')) if arm in ('U','V','ONE','BI','SHUFFLE') else 0,'canonical_feature_cache_bytes':sum(p.stat().st_size for p in v.cache(ds,seed).glob('*') if p.is_file())};write(p/'result.json',row)

@torch.no_grad()
def diagnose(ds,seed):
    v.OUT=sandbox('A',ds,seed,'BI',1);e.frozen_check();net=v.load_net('A',ds,seed,'BI');net.capture=True;outputs={}
    for split in ('train','validation'):
        net.train(split=='train');source=v.cache(ds,seed);pairs=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy')).reshape(-1,2);features=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r').reshape(-1,257);parts={}
        for st in range(0,len(pairs),256):
            net(torch.tensor(pairs[st:st+256],device='cuda'),torch.tensor(np.array(features[st:st+256]),device='cuda'))
            for key,value in net.diag.items():parts.setdefault(key,[]).append(value.cpu().numpy())
            net.diag={}
        outputs[split]={k:np.concatenate(values) for k,values in parts.items()}
    train,valid=outputs['train'],outputs['validation'];probes={name:e.probe(train[name],train['bi'],valid[name],valid['bi']) for name in ('raw','z','one')};diag={split:{k:e.distribution(values[k]) for k in ('mean_norm','max_norm','relation_change','u_norm','v_norm','u_cos','v_cos')} for split,values in outputs.items()};npos=len(e.sealed(ds)['valid_pos']);diag['validation_populations']={name:{k:e.distribution(valid[k][ix]) for k in ('mean_norm','max_norm','relation_change')} for name,ix in (('positive',slice(0,npos)),('negative',slice(npos,None)))};write(OUT/'diagnostics'/ds/f'seed_{seed}.json',{'state':'COMPLETE','seed':seed,'dataset':ds,'probes':probes,'substitution':diag,'probe_train_only':True,'test_opened':False});print('DIAGNOSTICS_COMPLETE',ds,seed,flush=True)

def finalize():
    data={'state':'COMPLETE','datasets':{},'test_opened':False};reproduction=[];comparisons=[('SHARED','RAW'),('BI','RAW'),('BI','SHARED'),('BI','SHUFFLE'),('BI','ONE'),('ONE','RAW'),('ONE','SHARED'),('ONE','SHUFFLE'),('U','SHARED'),('V','SHARED'),('U','V')]
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{a:read(job('A',ds,s,a)/'result.json') for a in ARMS}} for s in range(3)]
        for row in rows:
            r=g.reproduce_shared('A',ds,row['seed']);assert r['pass'],'RER_IMPLEMENTATION_ERROR_HISTORY';reproduction.append(r)
            assert all(a['training_trace']==row['arms']['RAW']['training_trace'] for a in row['arms'].values())
        effects={f'{a}_vs_{b}':v.comparison(rows,a,b) for a,b in comparisons};data['datasets'][ds]={'seed_results':rows,'effects':effects,'metrics':{a:{k:v.stat([r['arms'][a]['validation'][k] for r in rows]) for k in v.METRICS} for a in ARMS}}
    def both(a,b):return all(d['effects'][f'{a}_vs_{b}']['ce']['mean']>0 for d in data['datasets'].values())
    def wins(a):return all(d['effects'][f'{a}_vs_SHARED']['ce']['wins']>=2 for d in data['datasets'].values())
    main=both('BI','RAW') and both('BI','SHARED') and wins('BI');specific=both('BI','SHUFFLE');reciprocal=both('BI','ONE');one=both('ONE','RAW') and both('ONE','SHARED') and wins('ONE') and both('ONE','SHUFFLE');rank=all(d['effects']['BI_vs_SHARED']['mrr']['mean']>0 for d in data['datasets'].values())
    if main and specific and reciprocal:status='RER_RECIPROCAL_WITH_RANKING_GAIN' if rank else 'RER_RECIPROCAL_PROMISING';survivor='RECIPROCAL_REPLACEMENT'
    elif (main and specific) or one:status='RER_CANDIDATE_CONDITIONING_PROMISING';survivor='CANDIDATE_CONDITIONING'
    elif not both('BI','RAW'):status='RER_REJECTED_NO_GAIN';survivor='NONE'
    elif not main:status='RER_REJECTED_DUP_BASELINE';survivor='NONE'
    else:status='RER_REJECTED_CANDIDATE_SPECIFICITY';survivor='NONE'
    data['decision']={'final_status':status,'surviving_structure':survivor,'BI_primary_gate':main,'BI_specificity_gate':specific,'BI_reciprocity_gate':reciprocal,'ONE_conditioning_gate':one,'BI_ranking_gain_both':rank};artifact('08_PHASE_A_RESULTS.json',data);artifact('09_PAIRED_CONTRASTS.json',{ds:d['effects'] for ds,d in data['datasets'].items()});artifact('SHARED_HISTORICAL_REPRODUCTION.json',{'state':'PASS','records':reproduction})
    diag={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')};artifact('11_SUBSTITUTION_DIAGNOSTICS.json',{ds:[{'seed':r['seed'],'substitution':r['substitution']} for r in rr] for ds,rr in diag.items()});artifact('12_NONREDUNDANCY_PROBES.json',{ds:[{'seed':r['seed'],'probes':r['probes'],'train_only':True} for r in rr] for ds,rr in diag.items()});artifact('14_COMPUTE_AUDIT.json',{ds:{a:[r['arms'][a]['compute'] for r in d['seed_results']] for a in ('RAW','SHARED','BI')} for ds,d in data['datasets'].items()})
    lines=['| Dataset | Contrast | Mean DeltaCE | CE wins | Mean DeltaMRR |','|---|---|---:|---:|---:|']
    for ds,d in data['datasets'].items():
        for name,ef in d['effects'].items():lines.append(f"| {ds} | {name} | {ef['ce']['mean']:.10g} | {ef['ce']['wins']}/3 | {ef['mrr']['mean']:.10g} |")
    table='\n'.join(lines);md('13_RANKING_ANALYSIS.md','# V25 paired CE and ranking\n\n'+table);md('15_DECISION.md','# V25 decision\n\n'+json.dumps(data['decision'],indent=2))
    sections=['# V25 final report',f'FINAL_STATUS: {status}',f'SURVIVING_STRUCTURE: {survivor}',table]
    for name in ('01_SOURCE_AUDIT.md','02_LEAKAGE_AUDIT.md'):sections.append((ART/name).read_text())
    for name in ('03_SUBSTITUTION_COLLISION_AUDIT.json','04_SUBSTITUTION_SANITY.json','05_PARAMETER_AUDIT.json','06_ENDPOINT_SWAP_INVARIANCE.json','07_DETERMINISM_PRECHECK.json','10_SHUFFLE_CONTROL_AUDIT.json','11_SUBSTITUTION_DIAGNOSTICS.json','12_NONREDUNDANCY_PROBES.json','14_COMPUTE_AUDIT.json'):sections.extend([name,json.dumps(read(ART/name),indent=2)])
    sections.extend(['All validation metrics and per-seed values',json.dumps({ds:d['metrics'] for ds,d in data['datasets'].items()},indent=2),'No causal claim. No novel method claim before targeted novelty audit. No rescue, test, PhaseB or Innovation1 combination. U/V follow canonical sorted IDs; not semantic endpoint roles.','TEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO']);md('FINAL_REPORT.md','\n\n'.join(sections));md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: RER_V25_RECIPROCAL_ENDPOINT_REPLACEMENT_VALIDATION\nWORKSPACE: DCDLP-main\nCANONICAL_PROTOCOL: {PROTO}\nSOURCE_PRECONDITION: PASS\nSELF_REPLACEMENT_RAW_IDENTITY: PASS\nSELF_REPLACEMENT_SHARED_DUP_IDENTITY: PASS\nLEAKAGE_AUDIT: PASS\nENDPOINT_SWAP_INVARIANCE: PASS\nDETERMINISM: PASS\nFINAL_STATUS: {status}\nSURVIVING_STRUCTURE: {survivor}\n{table}\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO\nPRIMARY_ARTIFACT: result/innovation2/RER_V25/FINAL_REPORT.md\nNEXT: Return evidence then stop. No rescue or test.\n'+json.dumps(data['decision'],indent=2));v.OUT=ROOT/'CHRI_V18_1';e.frozen_check();e.cache_check();st={'state':'COMPLETE','final_status':status,'ended_at':time.time(),'test_opened':False};artifact('RUN_STATUS.json',st);write(OUT/'RUN_STATUS.json',st);print('V25_COMPLETE',status,flush=True)

def supervise():
    try:
        freeze();batch([('prepare',ds,s) for ds in ('cora','pubmed') for s in range(3)],'LOCAL_DESCRIPTOR_PREPARATION')
        audits={ds:[read(OUT/'cache_audits'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')};artifact('03_SUBSTITUTION_COLLISION_AUDIT.json',{'state':'PASS','datasets':audits,'train_frequency':'all5 frozen schedules weighted by occurrences','validation_frequency':'exact frozen candidate list'});artifact('10_SHUFFLE_CONTROL_AUDIT.json',{'state':'PASS','datasets':audits,'changed_only':'local substitution endpoint identities','same_RAW_Z_parameters_contexts_counts_order':True,'matching':'log2 incidence-degree bin clipped3 and incidence-count training-node quartile, no labels','optional_random':'NOT_RUN'})
        counts={a:sum(p.numel() for p in make_net('pubmed',0,e.MAP.get(a,a),'A').parameters() if p.requires_grad) for a in ARMS};assert counts['Z']==26385 and counts['RAW']==28481 and all(counts[a]==30529 for a in ARMS[2:]),'RER_IMPLEMENTATION_ERROR_PARAMETERS';artifact('05_PARAMETER_AUDIT.json',{'state':'PASS','counts':counts})
        for ds in ('cora','pubmed'):sanity(ds)
        records={ds:read(OUT/'sanity'/f'{ds}.json') for ds in ('cora','pubmed')};artifact('04_SUBSTITUTION_SANITY.json',{'state':'PASS','datasets':records,'self_descriptor_all_cached_tokens_bit_identical':True,'tolerance':1e-6});artifact('06_ENDPOINT_SWAP_INVARIANCE.json',{'state':'PASS','datasets':records,'tolerance':1e-6})
        frozen=read(ART/'SOURCE_HASHES.json');frozen['local_virtual_cache_hashes']={str(p.relative_to(REPO)):sha(p) for p in (OUT/'local_cache').rglob('*.npy')};artifact('SOURCE_HASHES.json',frozen);print('V25_PREFLIGHT_PASS',counts,flush=True)
        batch([('run','D','pubmed',0,a,r) for a in ('SHARED','ONE','BI','SHUFFLE') for r in (1,2)],'DETERMINISM_PRECHECK');pairs=[]
        for arm in ('SHARED','ONE','BI','SHUFFLE'):
            rows=[read(job('D','pubmed',0,arm,r)/'result.json') for r in (1,2)];checks={k:rows[0][k]==rows[1][k] for k in ('checkpoint_sha256','score_vector_sha256','training_trajectory_sha256','history','training_trace')};pairs.append({'arm':arm,'pass':all(checks.values()),'checks':checks})
        artifact('07_DETERMINISM_PRECHECK.json',{'state':'PASS' if all(p['pass'] for p in pairs) else 'FAIL','pairs':pairs});assert all(p['pass'] for p in pairs),'DETERMINISTIC_PROTOCOL_FAILURE';assert g.reproduce_shared('D','pubmed',0)['pass'],'RER_IMPLEMENTATION_ERROR_HISTORY'
        for arm in ('SHARED','ONE','BI','SHUFFLE'):
            dest=job('A','pubmed',0,arm);dest.parent.mkdir(parents=True,exist_ok=True);dest.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS if not(ds=='pubmed' and s==0 and a in ('SHARED','ONE','BI','SHUFFLE'))],'PHASE_A');batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'DIAGNOSTICS',3)
        for p,h in read(ART/'SOURCE_HASHES.json')['local_virtual_cache_hashes'].items():assert sha(REPO/p)==h,'RER_IMPLEMENTATION_ERROR_LOCAL_CACHE_CHANGED'
        finalize()
    except BaseException as error:
        for p in e.CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        status='DETERMINISTIC_PROTOCOL_FAILURE' if 'DETERMINISTIC_PROTOCOL_FAILURE' in str(error) else ('TEST_SEAL_VIOLATION' if 'TEST_SEAL_VIOLATION' in str(error) else 'RER_IMPLEMENTATION_ERROR');err={'state':'EXECUTION_FAILED','final_status':status,'error':repr(error),'traceback':traceback.format_exc(),'test_opened':False};artifact('RUN_STATUS.json',err);write(OUT/'RUN_STATUS.json',err);artifact('ERROR.json',err);md('FINAL_REPORT.md','# V25 failure\n\n'+json.dumps(err,indent=2));print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='supervise':supervise()
    elif cmd=='prepare':prepare(sys.argv[2],int(sys.argv[3]))
    elif cmd=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif cmd=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    else:raise ValueError(cmd)
