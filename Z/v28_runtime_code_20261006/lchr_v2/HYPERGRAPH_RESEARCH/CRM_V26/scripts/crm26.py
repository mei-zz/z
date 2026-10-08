"""V26 fixed candidate-relative moments; original attributes/H/RAW untouched."""
import os
for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):os.environ.setdefault(key,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
import sys,time,json,hashlib,subprocess,signal,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parent;OUT=ROOT/'CRM_V26';ART=REPO/'result/innovation2/CRM_V26'
sys.path.insert(0,str(ROOT/'RER_V25/scripts'));import rer25 as r
q,g,e,v,np,torch,nn,agg=r.q,r.g,r.e,r.v,r.np,r.torch,r.nn,r.agg
e.OUT=OUT;e.ART=ART;v.OUT=ROOT/'CHRI_V18_1'
read,write,sha,artifact,md,sandbox,job=e.read,e.write,e.sha,e.artifact,e.md,e.sandbox,e.job
ARMS=('Z','RAW','SHARED','CAPACITY','MEAN','MOM2','CONTEXT','SHUFFLE');PROTO=e.PROTO;CURRENT=None
def path(ds):return OUT/'moment_cache'/ds
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);np.save(p,x)

def prepare(ds):
    started=time.perf_counter();a=e.sealed(ds);n=len(a['x']);adj=[set() for _ in range(n)]
    for u,w in a['train']:adj[int(u)].add(int(w));adj[int(w)].add(int(u))
    members=[np.array(sorted({c,*adj[c]}),np.int64) if adj[c] else np.empty(0,np.int64) for c in range(n)]
    with np.load(v.cache(ds)/'structure.npz') as z:s={k:z[k] for k in z.files}
    from threadpoolctl import threadpool_limits
    from chri_features import array_hash
    with threadpool_limits(limits=4,user_api='blas'):node=(np.asarray(a['x']@s['projection'],np.float32)-s['normalization_mean'])/s['normalization_std']
    assert array_hash(node)==read(v.cache(ds)/'STRUCTURE_READY.json')['projected_node_hash'],'CRM_IMPLEMENTATION_ERROR_NODE'
    assert np.array_equal(np.stack([e.descriptor(node,m) for m in members]),s['raw']),'CRM_IMPLEMENTATION_ERROR_RAW_DESCRIPTOR'
    z=node.astype(np.float64);fullsum=np.stack([z[m].sum(0) for m in members]);fullsquare=np.stack([(z[m]**2).sum(0) for m in members]);ids=np.full(s['incident'].shape,-1,np.int64);masked=np.empty((len(s['keys']),2),np.int64);stats=[];sizes=[];focals=[];edges=[];hashes=[];degreebucket=[];checks=[];maxerr=0.;float32err=0.
    def add(focal,edge,removed=None):
        nonlocal maxerr,float32err
        context=members[edge];context=context[context!=focal]
        if removed is not None:context=context[context!=removed]
        count=len(context);ss=fullsum[edge]-z[focal];sq=fullsquare[edge]-z[focal]**2
        if removed is not None:ss=ss-z[removed];sq=sq-z[removed]**2
        mean=ss/count if count else np.zeros(16);variance=np.maximum(sq/max(count,1)-mean**2,0) if count else np.zeros(16)
        index=len(stats);stats.append(np.r_[mean,variance].astype(np.float32));sizes.append(count);focals.append(focal);edges.append(edge);hashes.append(hashlib.sha256(context.tobytes()).hexdigest());degreebucket.append(min(int(np.floor(np.log2(max(float(s['degree'][context].mean()) if count else 0,1)))),3))
        if index%97==0 or removed is not None and index%101==0:
            direct=z[context];m=direct.mean(0) if count else np.zeros(16);var=((direct-m)**2).mean(0) if count else np.zeros(16);mu=(direct-z[focal]).mean(0) if count else np.zeros(16);qq=((direct-z[focal])**2).mean(0) if count else np.zeros(16);cached_mu=mean-z[focal] if count else np.zeros(16);cached_q=variance+cached_mu**2
            errors=[np.max(np.abs(mean-m)),np.max(np.abs(variance-var)),np.max(np.abs(cached_mu-mu)),np.max(np.abs(cached_q-qq))];maxerr=max(maxerr,float(max(errors)));assert all(np.allclose(x,y,atol=1e-10,rtol=1e-10) for x,y in ((mean,m),(variance,var),(cached_mu,mu),(cached_q,qq))),'CRM_IMPLEMENTATION_ERROR_MOMENT_IDENTITY'
            mf,vf=stats[-1][:16],stats[-1][16:];muf=mf-node[focal] if count else np.zeros(16,np.float32);qf=vf+muf**2 if count else np.zeros(16,np.float32);float32err=max(float32err,float(np.max(np.abs(qf-qq))));assert np.allclose(qf,qq,atol=1e-5,rtol=1e-5),'CRM_IMPLEMENTATION_ERROR_FLOAT32'
            perm=np.random.RandomState(index).permutation(context);assert np.array_equal(z[np.sort(perm)],direct),'CRM_IMPLEMENTATION_ERROR_ORDER';checks.append(index)
        return index
    for focal in range(n):
        for col,edge in enumerate(s['incident'][focal]):
            if edge>=0:ids[focal,col]=add(focal,int(edge))
    for row,key in enumerate(s['keys']):
        u,w=int(key//n),int(key%n);masked[row,0]=add(u,u,w);masked[row,1]=add(w,w,u)
    p=path(ds)
    constant=np.repeat(z[0:1],7,axis=0);zero_mu=(constant-z[0]).mean(0);zero_q=((constant-z[0])**2).mean(0);assert np.array_equal(zero_mu,np.zeros(16)) and np.array_equal(zero_q,np.zeros(16)),'CRM_IMPLEMENTATION_ERROR_CONSTANT_ZERO'
    for key,val in {'node':node,'ids':ids,'masked_ids':masked,'stats':np.asarray(stats),'sizes':np.asarray(sizes,np.int64),'focals':np.asarray(focals,np.int64),'edges':np.asarray(edges,np.int64),'composition_hash':np.asarray(hashes),'degree_bucket':np.asarray(degreebucket,np.int8)}.items():save(p/(key+'.npy'),val)
    write(p/'READY.json',{'state':'PASS','dataset':ds,'seconds':time.perf_counter()-started,'contexts':len(stats),'valid_contexts':int(np.count_nonzero(sizes)),'sanity_samples':len(checks),'float64_max_error':maxerr,'float32_q_max_error':float32err,'float64_tolerance':1e-10,'float32_abs_relative_tolerance':1e-5,'member_order_bit_identity':'canonical sorted member IDs before aggregation','identical_member_zero_case':True,'empty_moments_zero':True,'statistics':'float64 sums/squared sums; float32 cached means and centered second moments; nonnegative clamp only floating roundoff','bytes':sum(f.stat().st_size for f in p.glob('*.npy')),'node_and_full_RAW_reconstruction_bit_exact':True});print('MOMENTS_PREPARED',ds,len(stats),flush=True)

def context_indices(pairs,side,s,ids,masked):
    pairs=np.sort(pairs,axis=1);n=len(s['degree']);key=pairs[:,0]*n+pairs[:,1];rows=np.minimum(np.searchsorted(s['keys'],key),len(s['keys'])-1);target=s['keys'][rows]==key;focal,other=pairs[:,side],pairs[:,1-side];centers=s['incident'][focal];valid=centers>=0;valid &= ~((centers==other[:,None])&target[:,None]);valid &= ~((centers==focal[:,None])&target[:,None]&(s['degree'][focal,None]==1));groups,cols=np.nonzero(valid);edge=centers[groups,cols];ci=ids[focal[groups],cols].copy();change=target[groups]&(edge==focal[groups]);ci[change]=masked[rows[groups[change]],side];return ci,np.bincount(groups,minlength=len(pairs))

def donors(ds,seed):
    p=path(ds);ids=np.load(p/'ids.npy');masked=np.load(p/'masked_ids.npy');sizes=np.load(p/'sizes.npy');hashes=np.load(p/'composition_hash.npy');buckets=np.load(p/'degree_bucket.npy');stats=np.load(p/'stats.npy');node=np.load(p/'node.npy');focals=np.load(p/'focals.npy')
    with np.load(v.cache(ds)/'structure.npz') as z:s={k:z[k] for k in z.files}
    audits={}
    for split in ('train','validation'):
        pp=np.concatenate([np.load(v.cache(ds,seed)/f'epoch_{i}_pairs.npy').reshape(-1,2) for i in range(1,6)]) if split=='train' else np.load(v.cache(ds,seed)/'valid_pairs.npy');counts=[];indices=[]
        for side in (0,1):ci,cc=context_indices(pp,side,s,ids,masked);indices.append(ci);counts.append(cc)
        used=np.unique(np.concatenate(indices));by_size={};by_joint={}
        for ci in used:
            if sizes[ci]>0:by_size.setdefault(int(sizes[ci]),[]).append(int(ci));by_joint.setdefault((int(sizes[ci]),int(buckets[ci])),[]).append(int(ci))
        mapping=np.arange(len(sizes));matched=changed=eligible=0;uncovered=[]
        for ci in used:
            if not sizes[ci]:continue
            eligible+=1;selected=None;pool=by_joint[(int(sizes[ci]),int(buckets[ci]))]
            for choices in (pool,by_size[int(sizes[ci])]):
                offset=int.from_bytes(hashlib.sha256(f'{ds}/{seed}/{split}/{ci}'.encode()).digest()[:8],'little')%len(choices)
                for j in range(len(choices)):
                    candidate=choices[(offset+j)%len(choices)]
                    if candidate!=ci and hashes[candidate]!=hashes[ci]:selected=candidate;break
                if selected is not None:break
            if selected is None:uncovered.append(int(ci));continue
            mapping[ci]=selected;matched+=int(buckets[selected]==buckets[ci]);changed+=1
        save(p/f'donors_{seed}_{split}.npy',mapping)
        validcounts=[np.bincount(np.repeat(np.arange(len(pp)),counts[side])[sizes[indices[side]]>0],minlength=len(pp)) for side in (0,1)];token_counts=counts[0]*counts[1];validpairs=validcounts[0]*validcounts[1]
        weights=np.bincount(np.concatenate(indices),minlength=len(sizes));uncovered_weight=int(weights[uncovered].sum()) if uncovered else 0
        audits[split]={'scheduled_candidates':len(pp),'incident_hyperedges':int(sum(c.sum() for c in counts)),'valid_context_fraction':float(sum(c.sum() for c in validcounts)/max(sum(c.sum() for c in counts),1)),'both_contexts_valid_relation_pair_fraction':float(validpairs.sum()/max(token_counts.sum(),1)),'exact_cardinality_match':bool(np.array_equal(sizes[mapping[used]],sizes[used])),'degree_bucket_match_fraction':matched/max(eligible,1),'changed_member_composition_fraction':changed/max(eligible,1),'uncovered_context_ids':uncovered,'uncovered_scheduled_hyperedges':uncovered_weight,'donors_same_split':True,'label_matching':False,'matching_fallback':'only exact cardinality retained when optional mean-member degree bucket has no different composition donor; explicitly counted','member_order_shuffle_is_not_used':True}
        assert not uncovered,'CRM_IMPLEMENTATION_ERROR_SHUFFLE_COVERAGE'
        mu=stats[used,:16]-node[focals[used]];qq=stats[used,16:]+mu**2;save(p/f'sanity_geometry_{seed}_{split}.npy',np.column_stack((np.linalg.norm(mu,axis=1),np.linalg.norm(qq,axis=1))))
    write(OUT/'donor_audits'/ds/f'seed_{seed}.json',{'state':'PASS','dataset':ds,'seed':seed,'splits':audits});print('DONORS_PREPARED',ds,seed,flush=True)

class MomentStructure(v.Structure):
    def __init__(self,ds,seed):
        super().__init__(v.cache(ds)/'structure.npz');p=path(ds);self.moment={k:torch.tensor(np.load(p/(k+'.npy')),device='cuda') for k in ('node','ids','masked_ids','stats','sizes')};self.donors={split:torch.tensor(np.load(p/f'donors_{seed}_{split}.npy'),device='cuda') for split in ('train','validation')}
    def moments(self,pairs,side,split,shuffled=False):
        pairs=pairs.sort(dim=1).values;focal,other=pairs[:,side],pairs[:,1-side];key=pairs[:,0]*self.n+pairs[:,1];rows=torch.searchsorted(self.keys,key).clamp(max=len(self.keys)-1);target=self.keys[rows]==key;centers=self.incident[focal];valid=centers>=0;valid &= ~((centers==other[:,None])&target[:,None]);valid &= ~((centers==focal[:,None])&target[:,None]&(self.degree[focal,None]==1));groups,cols=valid.nonzero(as_tuple=True);edge=centers[groups,cols];ci=self.moment['ids'][focal[groups],cols].clone();modify=target[groups]&(edge==focal[groups]);ci[modify]=self.moment['masked_ids'][rows[groups[modify]],side];counts=torch.bincount(groups,minlength=len(pairs));ok=self.moment['sizes'][ci]>0;donor=self.donors[split][ci] if shuffled else ci;raw=self.moment['stats'][donor];mean,var=raw[:,:16],raw[:,16:];mu=mean-self.moment['node'][focal[groups]];qq=var+mu.square();mu=torch.where(ok[:,None],mu,torch.zeros_like(mu));qq=torch.where(ok[:,None],qq,torch.zeros_like(qq));return mu,qq,mean,var,ok,groups,counts,ci

class Predictor(v.RelationPredictor):
    def __init__(self,structure,seed,arm,mean,std):
        super().__init__(structure,seed,'A2',mean,std);self.arm=arm;self.capture=False;self.diag={};agg.install(self)
        with torch.random.fork_rng():
            torch.manual_seed(26001+seed);self.psi=nn.Sequential(nn.Linear(96,4),nn.ReLU(),nn.Linear(4,16))
        with torch.random.fork_rng():
            torch.manual_seed(26002+seed);self.decoder=nn.Sequential(nn.Linear(385,58),nn.ReLU(),nn.Linear(58,66),nn.ReLU(),nn.Linear(66,1));nn.init.zeros_(self.decoder[-1].weight);nn.init.zeros_(self.decoder[-1].bias)
    def forward(self,pairs,b,donor=None):
        z,raw=self.representation(pairs,b,True);hu,nu,_=self.endpoint(pairs,0);hv,nv,_=self.endpoint(pairs,1);split='train' if self.training else 'validation';u=self.structure.moments(pairs,0,split,self.arm=='SHUFFLE');w=self.structure.moments(pairs,1,split,self.arm=='SHUFFLE');assert torch.equal(nu,u[6]) and torch.equal(nv,w[6]);sizes=nu*nv;groups=torch.repeat_interleave(torch.arange(len(pairs),device=b.device),sizes);offset=sizes.cumsum(0)-sizes;local=torch.arange(len(groups),device=b.device)-offset[groups];iu=(nu.cumsum(0)-nu)[groups]+torch.div(local,nv[groups],rounding_mode='floor');iv=(nv.cumsum(0)-nv)[groups]+local%nv[groups];ok=u[4][iu]&w[4][iv];validlengths=torch.bincount(groups[ok],minlength=len(pairs));bounds=[];st=0;running=0
        for row,n in enumerate(sizes.cpu().tolist()):
            if row>st and running+n>131072:bounds.append((st,row));st=row;running=0
            running+=n
        bounds.append((st,len(pairs)));output=[];captures={k:[] for k in ('mean','context','capacity')}
        for st,en in bounds:
            lo=int(offset[st]) if st<len(pairs) else len(groups);hi=int(offset[en]) if en<len(pairs) else len(groups);x=iu[lo:hi][ok[lo:hi]];y=iv[lo:hi][ok[lo:hi]];first=e.symmetric(u[0][x],w[0][y]);second=e.symmetric(u[1][x],w[1][y]);feature=torch.cat((first,second),1)
            rawfeature=e.symmetric(hu[x],hv[y]);context=torch.cat((e.symmetric(u[2][x],w[2][y]),e.symmetric(u[3][x],w[3][y])),1)
            if self.arm=='MEAN':feature=torch.cat((first,torch.zeros_like(second)),1)
            elif self.arm=='CONTEXT':feature=context
            elif self.arm=='CAPACITY':feature=torch.cat((rawfeature,rawfeature),1)
            output.append(e.pool(self.psi(feature),validlengths[st:en]))
            if self.capture:
                for key,xx in (('mean',torch.cat((first,torch.zeros_like(second)),1)),('context',context),('capacity',torch.cat((rawfeature,rawfeature),1))):captures[key].append(e.pool(self.psi(xx),validlengths[st:en]))
        pooled=torch.cat(output);score=b[:,0]+self.decoder(torch.cat((z,raw,pooled),1)).flatten()
        if self.capture:self.diag={'z':z,'raw':raw,'mom2':pooled,**{k:torch.cat(parts) for k,parts in captures.items()},'hu':hu,'hv':hv,'mu':torch.cat((u[0],w[0])),'q':torch.cat((u[1],w[1])),'m':torch.cat((u[2],w[2])),'var':torch.cat((u[3],w[3])),'context_id':torch.cat((u[7],w[7])),'u_mu':u[0],'v_mu':w[0],'u_q':u[1],'v_q':w[1],'u_count':nu,'v_count':nv}
        return score,b.new_zeros(()),b.new_zeros(())

def make_net(ds,seed,arm,phase,structure=None):
    global CURRENT
    if arm=='DUP':net=g.m.make_net(ds,seed,'DUP',phase,structure)
    elif arm in ARMS[3:]:
        stats=read(v.cache(ds,seed)/'normalization.json');net=Predictor(structure or MomentStructure(ds,seed),seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda')
    else:net=agg.install(e.ORIGINAL_MAKE(ds,seed,arm,phase,structure))
    CURRENT=net;return net
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
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);assert REPO.name in ('DCDLP-main','lchr_v2');v.check_frozen();previous=read(REPO/'result/innovation2/RER_V25/SOURCE_HASHES.json');files=dict(previous['files'])
    for name,h in files.items():assert sha(REPO/name)==h,'HISTORICAL_SOURCE_CHANGED '+name
    for name in ('RER_V25','RELREUSE_V24'):
        files.update({str(p.relative_to(REPO)):sha(p) for p in (REPO/'result/innovation2'/name).glob('*') if p.suffix in ('.json','.md')})
    for p in [Path(__file__),*[ART/name for name in ('00_PROTOCOL.md','01_SOURCE_PRECONDITION_AUDIT.md','01_SOURCE_PRECONDITION_AUDIT.json','06_LEAKAGE_AUDIT.md')]]:files[str(p.relative_to(REPO))]=sha(p)
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_TRAINING','files':files,'caches':previous['caches'],'canonical_protocol':PROTO});e.cache_check();assert read(REPO/'result/innovation2/RER_V25/RUN_STATUS.json')['final_status']=='RER_REJECTED_DUP_BASELINE'
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','workspace':'DCDLP-main','canonical_protocol':PROTO,'datasets':['cora','pubmed'],'seeds':[0,1,2],'epochs':5,'arms':list(ARMS),'precheck_arms':['SHARED','CAPACITY','MOM2','SHUFFLE'],'precheck_dataset_seed':['pubmed',0],'independent_replicates':2,'decoder':[385,58,66,1],'psi':[96,4,16],'user_approved_exact_parameter_solution':True,'trainable_parameters':30529,'workers':6,'threads_per_worker':2,'test_opened':False,'no_rescue':True})
    for name in ('02_CONTEXT_VALIDITY.json','03_MOMENT_SANITY.json','04_BASELINE_REPRODUCTION.json','05_PARAMETER_AUDIT.json','07_SWAP_INVARIANCE.json','08_DETERMINISM_PRECHECK.json','09_PHASE_A_RESULTS.json','10_PAIRED_CONTRASTS.json','11_MOMENT_DIAGNOSTICS.json','12_NONREDUNDANCY_PROBES.json','13_RAW_COLLISION_DIAGNOSTIC.json','14_SHUFFLE_CONTROL_AUDIT.json','16_COMPUTE_AUDIT.json'):artifact(name,{'state':'NOT_RUN','reason':'Prerequisites pending.'})
    for name in ('15_RANKING_ANALYSIS.md','17_DECISION.md','FINAL_REPORT.md'):md(name,'# V26\n\nPENDING')

@torch.no_grad()
def sanity(ds):
    nets={a:make_net(ds,0,a,'A').eval() for a in ARMS[3:]};p=torch.tensor(np.load(v.cache(ds,0)/'valid_pairs.npy')[:128],device='cuda');b=torch.tensor(np.load(v.cache(ds,0)/'valid_b.npy')[:128],device='cuda');net=nets['MOM2'];net.capture=True;score=net(p,b)[0];pool=net.diag['mom2'].clone();z,raw=net.diag['z'].clone(),net.diag['raw'].clone();swapped=net(p.flip(1),b)[0];checks={'pooled_max_error':float((pool-net.diag['mom2']).abs().max()),'logit_max_error':float((score-swapped).abs().max()),'shared_CRM_initial_state':len({g.statehash(n.state_dict()) for n in nets.values()})==1};shuf=nets['SHUFFLE'];shuf.capture=True;shuf(p,b);checks.update(shuffle_preserves_Z=torch.equal(z,shuf.diag['z']),shuffle_preserves_RAW=torch.equal(raw,shuf.diag['raw']));assert checks['pooled_max_error']<1e-6 and checks['logit_max_error']<1e-6 and all(checks[k] for k in ('shared_CRM_initial_state','shuffle_preserves_Z','shuffle_preserves_RAW')),'CRM_IMPLEMENTATION_ERROR_SWAP_OR_SHUFFLE';write(OUT/'sanity'/f'{ds}.json',{'state':'PASS','checks':checks,'tolerance':1e-6})

def run(phase,ds,seed,arm,rep):
    started=time.perf_counter();q.run(phase,ds,seed,arm,rep);p=job(phase,ds,seed,arm,rep);row=read(p/'result.json');row['compute']={'wall_seconds':time.perf_counter()-started,'peak_GPU_allocated_bytes':torch.cuda.max_memory_allocated(),'moment_cache_bytes':sum(p.stat().st_size for p in path(ds).glob('*.npy')) if arm in ARMS[3:] else 0,'preprocessing_seconds':read(path(ds)/'READY.json')['seconds'] if arm in ARMS[3:] else 0};write(p/'result.json',row)

@torch.no_grad()
def diagnose(ds,seed):
    from scipy.spatial import cKDTree
    from scipy.stats import spearmanr
    v.OUT=sandbox('A',ds,seed,'MOM2',1);e.frozen_check();net=v.load_net('A',ds,seed,'MOM2');net.capture=True;output={};norms={};cloud={}
    for split in ('train','validation'):
        net.train(split=='train');source=v.cache(ds,seed);pairs=np.load(source/('epoch_1_pairs.npy' if split=='train' else 'valid_pairs.npy')).reshape(-1,2);features=np.load(source/('epoch_1.npy' if split=='train' else 'valid_b.npy'),mmap_mode='r').reshape(-1,257);parts={};distributions={};candidate={k:[] for k in ('mean_mu','max_mu','mean_q','max_q')};cloud[split]=[];seen=set()
        for st in range(0,len(pairs),256):
            net(torch.tensor(pairs[st:st+256],device='cuda'),torch.tensor(np.array(features[st:st+256]),device='cuda'));d=net.diag
            for k in ('z','raw','mom2','mean','context','capacity'):parts.setdefault(k,[]).append(d[k].cpu().numpy())
            for k in ('mu','q','m','var'):distributions.setdefault(k,[]).append(d[k].norm(dim=1).cpu().numpy())
            distributions.setdefault('q_mu_ratio',[]).append((d['q'].norm(dim=1)/(d['mu'].norm(dim=1)+1e-12)).cpu().numpy())
            if len(seen)<4096:
                h=torch.cat((d['hu'],d['hv']));indices=[]
                for j,ci in enumerate(d['context_id'].cpu().tolist()):
                    if ci not in seen and len(seen)<4096:seen.add(ci);indices.append(j)
                cloud[split].append({'h':h[indices].cpu().numpy(),'mu':d['mu'][indices].cpu().numpy(),'q':d['q'][indices].cpu().numpy()})
            a0=b0=0
            for cu,cv in zip(d['u_count'].cpu().tolist(),d['v_count'].cpu().tolist()):
                for k in ('mu','q'):
                    val=torch.cat((d['u_'+k][a0:a0+cu],d['v_'+k][b0:b0+cv])).norm(dim=1);candidate['mean_'+k].append(float(val.mean()) if len(val) else 0.);candidate['max_'+k].append(float(val.max()) if len(val) else 0.)
                a0+=cu;b0+=cv
            net.diag={}
        output[split]={k:np.concatenate(values) for k,values in parts.items()};norms[split]={'incident_hyperedges':{k:e.distribution(np.concatenate(values)) for k,values in distributions.items()},'candidate':{k:e.distribution(values) for k,values in candidate.items()}}
    train,valid=output['train'],output['validation'];probes={k:e.probe(train[k],train['mom2'],valid[k],valid['mom2']) for k in ('raw','z','mean','context')};collision={}
    for split,items in cloud.items():
        cl={k:np.concatenate([x[k] for x in items]) for k in ('h','mu','q')};tree=cKDTree(cl['h']);dist,index=tree.query(cl['h'],k=2,workers=2);neighbors=np.where(index[:,0]!=np.arange(len(index)),index[:,0],index[:,1]);hd=np.linalg.norm(cl['h']-cl['h'][neighbors],axis=1);mu=np.linalg.norm(cl['mu']-cl['mu'][neighbors],axis=1);qd=np.linalg.norm(cl['q']-cl['q'][neighbors],axis=1);corr=float(spearmanr(hd,qd).statistic) if np.std(hd)>1e-12 and np.std(qd)>1e-12 else None
        collision[split]={'label_free':True,'sample_size':len(hd),'selection':'first4096 distinct hyperedge/focal-context IDs within this split, nearest other context under canonical h_e; no labels','h_distance':e.distribution(hd),'mu_distance':e.distribution(mu),'q_distance':e.distribution(qd),'spearman_h_q_distance':corr,'descriptive_only':True}
    write(OUT/'diagnostics'/ds/f'seed_{seed}.json',{'state':'COMPLETE','dataset':ds,'seed':seed,'moments':norms,'probes':probes,'probe_train_only':True,'raw_collision':collision,'test_opened':False});print('DIAGNOSTICS_COMPLETE',ds,seed,flush=True)

def baseline(phase,ds,seed):
    shared=g.reproduce_shared(phase,ds,seed);new=read(job(phase,ds,seed,'RAW')/'result.json') if phase=='A' else None;raw=None
    if new:
        oldroot=ROOT/'RER_V25/executions/A'/ds/f'seed_{seed}/RAW/rep_1/runs/A'/ds/f'seed_{seed}/A2';old=read(oldroot/'result.json');raw={k:new[k]==old[k] for k in ('validation','score_vector_sha256','training_trajectory_sha256')};state=torch.load(job(phase,ds,seed,'RAW')/'final.pt',map_location='cpu',weights_only=False)['state'];oldstate=torch.load(oldroot/'final.pt',map_location='cpu',weights_only=False)['state'];raw['weights']=g.statehash(state)==g.statehash(oldstate)
    assert shared['pass'] and (raw is None or all(raw.values())),'CRM_BASELINE_REPRODUCTION_FAILURE';return {'dataset':ds,'seed':seed,'SHARED':shared,'RAW':raw,'pass':True}

def finalize():
    data={'state':'COMPLETE','datasets':{},'test_opened':False};reproduction=[];comparisons=[('SHARED','RAW'),*[('MOM2',a) for a in ('RAW','SHARED','MEAN','CONTEXT','CAPACITY','SHUFFLE')]]
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{a:read(job('A',ds,s,a)/'result.json') for a in ARMS}} for s in range(3)]
        for row in rows:reproduction.append(baseline('A',ds,row['seed']));assert all(a['training_trace']==row['arms']['RAW']['training_trace'] for a in row['arms'].values())
        effects={f'{a}_vs_{b}':v.comparison(rows,a,b) for a,b in comparisons};data['datasets'][ds]={'seed_results':rows,'effects':effects,'metrics':{a:{k:v.stat([r['arms'][a]['validation'][k] for r in rows]) for k in v.METRICS} for a in ARMS}}
    gates={b:all(d['effects'][f'MOM2_vs_{b}']['ce']['mean']>0 and (d['effects'][f'MOM2_vs_{b}']['ce']['wins']>=2 if b in ('RAW','SHARED') else True) for d in data['datasets'].values()) for b in ('RAW','SHARED','MEAN','CONTEXT','CAPACITY','SHUFFLE')};statuses={'RAW':'CRM_REJECTED_NO_GAIN','SHARED':'CRM_REJECTED_DUP_BASELINE','MEAN':'CRM_REJECTED_SECOND_MOMENT','CONTEXT':'CRM_REJECTED_ENDPOINT_RELATIVITY','CAPACITY':'CRM_REJECTED_CAPACITY_EXPLANATION','SHUFFLE':'CRM_REJECTED_MEMBER_STRUCTURE'};rank=all(d['effects']['MOM2_vs_SHARED']['mrr']['mean']>0 for d in data['datasets'].values());status=next((statuses[k] for k,passed in gates.items() if not passed),'CRM_MOMENT_SIGNAL_WITH_RANKING_GAIN' if rank else 'CRM_MOMENT_SIGNAL_PROMISING');survivor='MOMENT_SIGNAL' if all(gates.values()) else 'NONE';decision={'final_status':status,'gates':gates,'ranking_gain_both_datasets':rank,'surviving_structure':survivor,'meta_conclusion_for_review':'CHRI_DERIVED_STRUCTURAL_SEARCH_EXHAUSTED' if survivor=='NONE' else None,'no_rescue':True};data['decision']=decision;artifact('09_PHASE_A_RESULTS.json',data);artifact('10_PAIRED_CONTRASTS.json',{ds:d['effects'] for ds,d in data['datasets'].items()});artifact('04_BASELINE_REPRODUCTION.json',{'state':'PASS','records':reproduction})
    diag={ds:[read(OUT/'diagnostics'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')}
    for name,key in (('11_MOMENT_DIAGNOSTICS.json','moments'),('12_NONREDUNDANCY_PROBES.json','probes'),('13_RAW_COLLISION_DIAGNOSTIC.json','raw_collision')):artifact(name,{ds:[{'seed':r['seed'],key:r[key]} for r in rr] for ds,rr in diag.items()})
    artifact('16_COMPUTE_AUDIT.json',{ds:{a:[r['arms'][a]['compute'] for r in d['seed_results']] for a in ('RAW','SHARED','MOM2')} for ds,d in data['datasets'].items()});lines=['| Dataset | Contrast | Mean DeltaCE | CE wins | Mean DeltaMRR |','|---|---|---:|---:|---:|']
    for ds,d in data['datasets'].items():
        for name,ef in d['effects'].items():lines.append(f"| {ds} | {name} | {ef['ce']['mean']:.10g} | {ef['ce']['wins']}/3 | {ef['mrr']['mean']:.10g} |")
    table='\n'.join(lines);md('15_RANKING_ANALYSIS.md','# V26 paired CE/ranking\n\n'+table);md('17_DECISION.md','# V26 decision\n\n'+json.dumps(decision,indent=2));sections=['# V26 final report',f'FINAL_STATUS: {status}',json.dumps(decision,indent=2),table]
    for name in ('01_SOURCE_PRECONDITION_AUDIT.md','06_LEAKAGE_AUDIT.md'):sections.append((ART/name).read_text())
    for name in ('02_CONTEXT_VALIDITY.json','03_MOMENT_SANITY.json','04_BASELINE_REPRODUCTION.json','05_PARAMETER_AUDIT.json','07_SWAP_INVARIANCE.json','08_DETERMINISM_PRECHECK.json','11_MOMENT_DIAGNOSTICS.json','12_NONREDUNDANCY_PROBES.json','13_RAW_COLLISION_DIAGNOSTIC.json','14_SHUFFLE_CONTROL_AUDIT.json','16_COMPUTE_AUDIT.json'):sections.extend([name,json.dumps(read(ART/name),indent=2)])
    sections.extend(['Complete validation metrics',json.dumps({ds:d['metrics'] for ds,d in data['datasets'].items()},indent=2),'q is endpoint-relative second raw moment, not variance. Low probeR2 or geometric separation is not predictive success. No novelty/causal claims. No test, PhaseB, rescue or automatic V26.1.','TEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO']);md('FINAL_REPORT.md','\n\n'.join(sections));md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: CRM_V26_CANDIDATE_RELATIVE_MOMENT_VALIDATION\nWORKSPACE: DCDLP-main\nCANONICAL_PROTOCOL: {PROTO}\nSOURCE_PRECONDITION: PASS\nCANONICAL_H_ALREADY_HAS_MOM2: NO\nMOMENT_SANITY: PASS\nBASELINE_REPRODUCTION: PASS\nDETERMINISM: PASS\nFINAL_STATUS: {status}\nSURVIVING_STRUCTURE: {survivor}\n{table}\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nHISTORICAL_RESULTS_MODIFIED: NO\nPRIMARY_ARTIFACT: result/innovation2/CRM_V26/FINAL_REPORT.md\nNEXT: Return evidence and stop. No V26.1, rescue or test.\n'+json.dumps(decision,indent=2));v.OUT=ROOT/'CHRI_V18_1';e.frozen_check();e.cache_check();st={'state':'COMPLETE','final_status':status,'ended_at':time.time(),'test_opened':False};artifact('RUN_STATUS.json',st);write(OUT/'RUN_STATUS.json',st);print('V26_COMPLETE',status,flush=True)

def supervise():
    try:
        freeze();batch([('prepare',ds) for ds in ('cora','pubmed')],'MOMENT_CACHE_PREPARATION',2);batch([('donors',ds,s) for ds in ('cora','pubmed') for s in range(3)],'MEMBER_COMPOSITION_DONORS');ready={ds:read(path(ds)/'READY.json') for ds in ('cora','pubmed')};audits={ds:[read(OUT/'donor_audits'/ds/f'seed_{s}.json') for s in range(3)] for ds in ('cora','pubmed')};artifact('02_CONTEXT_VALIDITY.json',{'state':'PASS','datasets':audits});artifact('03_MOMENT_SANITY.json',{'state':'PASS','datasets':ready,'same_member_zero_case':'direct zero displacements, exact zero mu/q','permutation':'sorted unique member IDs ensure exact order-invariant aggregation'});artifact('14_SHUFFLE_CONTROL_AUDIT.json',{'state':'PASS','datasets':audits,'same_endpoints_Z_RAW_counts_parameters_split':True,'composition_changed':True,'exact_size_required':True})
        counts={a:sum(p.numel() for p in make_net('pubmed',0,e.MAP.get(a,a),'A').parameters() if p.requires_grad) for a in ARMS};assert counts['Z']==26385 and counts['RAW']==28481 and all(counts[a]==30529 for a in ARMS[2:]),'CRM_IMPLEMENTATION_ERROR_PARAMETER_MATCH';artifact('05_PARAMETER_AUDIT.json',{'state':'PASS','counts':counts,'psi':[96,4,16],'CRM_decoder':[385,58,66,1],'historical_SHARED_decoder':[385,64,32,1],'user_approved_exact_matching':True,'canonical_encoder_relation_unchanged':True})
        for ds in ('cora','pubmed'):sanity(ds)
        artifact('07_SWAP_INVARIANCE.json',{'state':'PASS','datasets':{ds:read(OUT/'sanity'/f'{ds}.json') for ds in ('cora','pubmed')}});frozen=read(ART/'SOURCE_HASHES.json');frozen['moment_cache_hashes']={str(p.relative_to(REPO)):sha(p) for p in (OUT/'moment_cache').rglob('*') if p.is_file()};artifact('SOURCE_HASHES.json',frozen);print('V26_PREFLIGHT_PASS',counts,flush=True)
        batch([('run','D','pubmed',0,a,rep) for a in ('SHARED','CAPACITY','MOM2','SHUFFLE') for rep in (1,2)],'DETERMINISM_PRECHECK');pairs=[]
        for arm in ('SHARED','CAPACITY','MOM2','SHUFFLE'):
            rows=[read(job('D','pubmed',0,arm,rep)/'result.json') for rep in (1,2)];checks={k:rows[0][k]==rows[1][k] for k in ('checkpoint_sha256','score_vector_sha256','training_trajectory_sha256','history','training_trace')};pairs.append({'arm':arm,'pass':all(checks.values()),'checks':checks})
        ok=all(p['pass'] for p in pairs);artifact('08_DETERMINISM_PRECHECK.json',{'state':'PASS' if ok else 'FAIL','pairs':pairs});assert ok,'DETERMINISTIC_PROTOCOL_FAILURE';artifact('04_BASELINE_REPRODUCTION.json',{'state':'PASS','spot':baseline('D','pubmed',0)})
        for arm in ('SHARED','CAPACITY','MOM2','SHUFFLE'):
            dest=job('A','pubmed',0,arm);dest.parent.mkdir(parents=True,exist_ok=True);dest.symlink_to(job('D','pubmed',0,arm),target_is_directory=True)
        batch([('run','A',ds,s,a,1) for s in range(3) for ds in ('cora','pubmed') for a in ARMS if not(ds=='pubmed' and s==0 and a in ('SHARED','CAPACITY','MOM2','SHUFFLE'))],'PHASE_A');batch([('diagnose',ds,s) for ds in ('cora','pubmed') for s in range(3)],'DIAGNOSTICS',3)
        for p,h in read(ART/'SOURCE_HASHES.json')['moment_cache_hashes'].items():assert sha(REPO/p)==h,'CRM_IMPLEMENTATION_ERROR_CACHE_CHANGED'
        finalize()
    except BaseException as error:
        for p in e.CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        status=next((s for s in ('CRM_BASELINE_REPRODUCTION_FAILURE','DETERMINISTIC_PROTOCOL_FAILURE','TEST_SEAL_VIOLATION') if s in str(error)),'CRM_IMPLEMENTATION_ERROR');err={'state':'EXECUTION_FAILED','final_status':status,'error':repr(error),'traceback':traceback.format_exc(),'test_opened':False};artifact('RUN_STATUS.json',err);write(OUT/'RUN_STATUS.json',err);artifact('ERROR.json',err);md('FINAL_REPORT.md','# V26 failure\n\n'+json.dumps(err,indent=2));print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='supervise':supervise()
    elif cmd=='prepare':prepare(sys.argv[2])
    elif cmd=='donors':donors(sys.argv[2],int(sys.argv[3]))
    elif cmd=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif cmd=='diagnose':diagnose(sys.argv[2],int(sys.argv[3]))
    else:raise ValueError(cmd)
