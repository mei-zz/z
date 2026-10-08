from __future__ import annotations
import argparse, gc, hashlib, importlib.util, json, multiprocessing as mp, os, subprocess, sys, time, traceback
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parents[1]
PARENT = OUT.parent / 'HSPE_V17'
SPEC = importlib.util.spec_from_file_location('hspe_v171_parent', PARENT / 'scripts' / 'hspe_v17.py')
p = importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name] = p; SPEC.loader.exec_module(p)
p.OUT = OUT
import torch
from torch import nn
ARMS = ('B0_BASELINE','C0_COUNT_LINEAR','C1_COUNT_PARAM_MATCHED','C2_CONSTANT_SET','C3_GLOBAL_SIZE_SHUFFLE','H1_HSPE_REAL')
DATASETS = ('cora','pubmed')
SEEDS = tuple(range(5))
FEATURE_VERSION = 'identity_permutation_mask_before_label_permutation_v1'
write_json, read_json = p.write_json, p.read_json

def sources():
    return {'v171':p.sha256_file(Path(__file__)), 'v17':p.sha256_file(PARENT/'scripts'/'hspe_v17.py'), **p._source_hashes()}

def descriptor(a,b):
    out=np.zeros((len(a),6),dtype=np.float32)
    out[:,0]=a+b; out[:,1]=np.abs(a-b); out[:,2]=a*b
    return out

_G = None
def feature_chunk(bounds):
    g=_G; struct=g['structure']; cache=g['cache']; sizes=g['sizes']; perm=g['perm']; dist=g['distribution']
    c3=np.load(g['shuffle_path'],mmap_mode='r+'); rank=np.load(g['rank_path'],mmap_mode='r+')
    changed=nonempty=0; maxerr=0.
    for row in range(*bounds):
        key=int(cache['keys'][row]); u,v=divmod(key,struct['n']); mask=key in g['targets']
        shared,mu,mv,_,_,_,expected=p.v16.stage0._pair_projection(struct,u,v,mask)
        lo,hi=map(int,cache['offsets'][row:row+2]); cursor=lo
        if hi-lo != expected or int(cache['support'][row]) != len(shared): raise RuntimeError('Frozen topology/count mismatch')
        anychange=False
        for w,nu,nv in zip(shared.tolist(),mu.tolist(),mv.tolist()):
            es=struct['incident'][u].intersection(struct['incident'][w]); fs=struct['incident'][v].intersection(struct['incident'][w])
            if mask: es.discard(v); fs.discard(u)
            if len(es)!=nu or len(fs)!=nv: raise RuntimeError('Frozen hyperedge identity mismatch')
            e=np.asarray(sorted(es),dtype=np.int64); f=np.asarray(sorted(fs),dtype=np.int64)
            se=sizes[e]-((e==u)|(e==v))*int(mask); sf=sizes[f]-((f==u)|(f==v))*int(mask)
            e=e[se>1]; f=f[sf>1]
            ee=np.repeat(e,len(f)); ff=np.tile(f,len(e)); count=len(ee)
            ae=sizes[ee]-((ee==u)|(ee==v))*int(mask); bf=sizes[ff]-((ff==u)|(ff==v))*int(mask)
            original=descriptor(np.log1p(ae),np.log1p(bf)); stop=cursor+count
            err=float(np.max(np.abs(original[:,:3]-cache['tokens_real'][cursor:stop,:3]))) if count else 0.
            maxerr=max(maxerr,err)
            if err>2e-6: raise RuntimeError(f'Token order/descriptor mismatch: {err}')
            # Mask effective size labels before permuting identities, preserving
            # the complete masked graph label multiset for each candidate.
            de,df=perm[ee],perm[ff]
            ae_s=sizes[de]-((de==u)|(de==v))*int(mask); bf_s=sizes[df]-((df==u)|(df==v))*int(mask)
            shuffled=descriptor(np.log1p(ae_s),np.log1p(bf_s))
            anychange |= not np.array_equal(original[:,:3],shuffled[:,:3])
            c3[cursor:stop]=shuffled
            ar=np.searchsorted(dist,ae,side='right')/len(dist); br=np.searchsorted(dist,bf,side='right')/len(dist)
            rank[cursor:stop]=descriptor(ar,br); cursor=stop
        if cursor!=hi: raise RuntimeError('Candidate token topology changed')
        changed+=int(anychange); nonempty+=int(hi>lo)
    c3.flush(); rank.flush()
    return {'changed':changed,'nonempty':nonempty,'max_token_difference':maxerr}

def prepare(ds,workers=8):
    t=time.perf_counter(); ctx=p.build_context(ds); hashes=sources(); dest=OUT/'features'/ds; dest.mkdir(parents=True,exist_ok=True)
    meta_path=dest/'metadata.json'
    expected={'version':FEATURE_VERSION,'parent_sources':hashes,'selected_hash':ctx['selected_hash'],'valid_hash':ctx['valid_hash']}
    if meta_path.exists():
        old=read_json(meta_path)
        if old.get('identity')==expected and all(Path(f['path']).is_file() and p.sha256_file(Path(f['path']))==f['sha256'] for f in old['files']): return old
    structure=p.v16.stage0.build_structure(p.v16.stage0.build_adjacency(ctx['view'].num_nodes,ctx['train_pos']))
    sizes=structure['degree']+1; active=np.flatnonzero(structure['degree']>0); distribution=np.sort(sizes[active])
    targets={p.v16.pair_key(pair,ctx['view'].num_nodes) for pair in ctx['train_pos']}
    result={'state':'COMPLETE','identity':expected,'input_audit':ctx['audit'],'hyperedge_count':len(active),'training_size_distribution':{'min':int(distribution.min()),'max':int(distribution.max()),'mean':float(distribution.mean())},'ecdf_fit':'train-visible hyperedges only; right-continuous ECDF','splits':{},'files':[],'test_evaluated':False}
    global _G
    for split,cache in (('train',ctx['train_cache']),('valid',ctx['valid_cache'])):
        seed=17110000+({'cora':1,'pubmed':2}[ds])*100+({'train':1,'valid':2}[split])
        perm=np.arange(len(sizes)); perm[active]=np.random.default_rng(seed).permutation(active)
        assert np.array_equal(np.sort(sizes[perm[active]]),distribution)
        shuffle_path=dest/f'{split}_global_shuffle.npy'; rank_path=dest/f'{split}_rank.npy'
        for path in (shuffle_path,rank_path):
            a=np.lib.format.open_memmap(path,mode='w+',dtype=np.float32,shape=cache['tokens_real'].shape); a.flush(); del a
        _G={'structure':structure,'cache':cache,'sizes':sizes,'perm':perm,'distribution':distribution,'targets':targets if split=='train' else set(),'shuffle_path':str(shuffle_path),'rank_path':str(rank_path)}
        chunks=[(i,min(i+256,len(cache['keys']))) for i in range(0,len(cache['keys']),256)]
        with mp.get_context('fork').Pool(workers) as pool: pieces=list(pool.imap_unordered(feature_chunk,chunks))
        changed=sum(x['changed'] for x in pieces); nonempty=sum(x['nonempty'] for x in pieces); fraction=changed/max(1,len(cache['keys']))
        result['splits'][split]={'permutation_seed':seed,'permutation_sha256':hashlib.sha256(perm.tobytes()).hexdigest(),'global_size_multiset_exact':True,'target_mask_policy':'effective labels masked first, then permuted by fixed donor identity; token topology follows true target-masked graph','pair_count':len(cache['keys']),'token_count':int(cache['offsets'][-1]),'token_count_support_incidence_unchanged':True,'informative_pair_count':changed,'informative_fraction':fraction,'nonempty_candidate_fraction':nonempty/max(1,len(cache['keys'])),'power':'ADEQUATE_HIGH_POWER_SHUFFLE' if fraction>=.5 else 'LOW_SHUFFLE_POWER','max_original_token_difference':max(x['max_token_difference'] for x in pieces),'shuffle_path':str(shuffle_path),'rank_path':str(rank_path)}
        for path in (shuffle_path,rank_path): result['files'].append({'path':str(path),'sha256':p.sha256_file(path)})
    result['feature_construction_seconds']=time.perf_counter()-t; write_json(meta_path,result); _G=None
    print(f'PREPARED {ds} '+json.dumps(result['splits']),flush=True)
    return result

def count_class(ts,vs,matched):
    from dcdlp.models.dcdlp import DCDLP as Base
    class CountModel(Base):
        def __init__(self,*a,**kw):
            super().__init__(*a,**kw)
            with torch.random.fork_rng(devices=[]):
                if matched:
                    self.count_encoder=nn.Linear(6,8); self.count_head=nn.Linear(18,1)
                else: self.count_head=nn.Linear(2,1)
                nn.init.zeros_(self.count_head.weight); nn.init.zeros_(self.count_head.bias)
        def forward(self,x,edge_index,pairs,remove_target_edges=True,support_edge_index=None):
            out=super().forward(x,edge_index,pairs,remove_target_edges=remove_target_edges,support_edge_index=support_edge_index)
            store=ts if self.training else vs; rows=store.lookup(pairs); c=store.counts[rows]
            if matched:
                h=torch.relu(self.count_encoder(torch.cat((c,torch.zeros((len(c),4),device=c.device)),dim=1)))
                rep=torch.cat((h,h,c),dim=1)
            else: rep=c
            delta=self.count_head(rep).squeeze(-1); out['logit']=out['logit']+delta; out['nhmc_delta']=delta
            return out
    return CountModel

def model_class(arm,ts,vs):
    from dcdlp.models.dcdlp import DCDLP
    if arm=='B0_BASELINE': return DCDLP
    if arm in ('C0_COUNT_LINEAR','C1_COUNT_PARAM_MATCHED'): return count_class(ts,vs,arm=='C1_COUNT_PARAM_MATCHED')
    return p.v16.make_model_class('C1_NHMC_SIZE',ts,vs)

def make_model(cls,view,ds):
    from dcdlp.train import ablation_profile
    cfg=p.v16.make_config(ds,OUT/'zero_init_probe',10); profile=ablation_profile(cfg.ablation)
    return cls(view.features.shape[1],cfg.hidden_dim,cfg.branch_dim,cfg.num_layers,cfg.dropout,cfg.backbone,
        use_interaction=profile['interaction'],active_branches=profile['active'],decoder_mode=profile['decoder'],
        cn_feature_mode=cfg.cn_feature_mode,cn_regressor=None,interaction_mode=cfg.interaction_mode,cn_input_schema=cfg.cn_input_schema,
        hypergraph_mode=cfg.hypergraph_mode,hypergraph_construction=cfg.hypergraph_construction,ghhr_enabled=False,
        complementarity_fusion_mode='none',fusion_gate_hidden_dim=cfg.fusion_gate_hidden_dim,
        fusion_margin_graph_threshold=cfg.fusion_margin_graph_threshold,fusion_margin_hypergraph_threshold=cfg.fusion_margin_hypergraph_threshold).to('cuda')

def stores(ctx):
    ts,vs=[p.Store(ctx[k],ctx['view'].num_nodes,torch.device('cuda')) for k in ('train_cache','valid_cache')]
    for st,cache in ((ts,ctx['train_cache']),(vs,ctx['valid_cache'])):
        st.counts=torch.as_tensor(np.column_stack((np.log1p(np.diff(cache['offsets'])),np.log1p(np.maximum(0,cache['support'])))),dtype=torch.float32,device='cuda')
    return ts,vs

def zero_audit(ctx,ds,ts,vs):
    from dcdlp.train import edge_index_from_graph
    torch.manual_seed(0); torch.cuda.manual_seed_all(0); base=make_model(model_class('B0_BASELINE',ts,vs),ctx['view'],ds).eval()
    state=base.state_dict(); base_params=sum(x.numel() for x in base.parameters()); audits={}
    x=torch.as_tensor(ctx['view'].features,dtype=torch.float32,device='cuda'); edge=edge_index_from_graph(ctx['view'].train_graph(),torch.device('cuda'))
    pair=torch.as_tensor(ctx['valid_pos'][:4],dtype=torch.long,device='cuda')
    with torch.no_grad(): logits=base(x,edge,pair,remove_target_edges=True)['logit']
    for arm in (*ARMS[1:],'H2_R_HSPE'):
        torch.manual_seed(0); torch.cuda.manual_seed_all(0); model=make_model(model_class(arm,ts,vs),ctx['view'],ds).eval()
        equal=all(torch.equal(v,model.state_dict()[k]) for k,v in state.items())
        with torch.no_grad(): err=float(torch.max(torch.abs(model(x,edge,pair,remove_target_edges=True)['logit']-logits)).cpu())
        n=sum(x.numel() for x in model.parameters()); expected=3 if arm=='C0_COUNT_LINEAR' else 75
        # CUDA message aggregation can vary by one float32 ULP across forward
        # calls even with bit-identical parameters and a zero residual head.
        # 5e-7 accepts that round-off while still checking the initial function.
        assert equal and err<=5e-7 and n-base_params==expected, (ds,arm,equal,err,n-base_params)
        audits[arm]={'initial_baseline_weights_equal':equal,'initial_logit_max_difference':err,'logit_roundoff_tolerance':5e-7,'trainable_parameters':n,'added_parameters':n-base_params}
        del model
    del base; torch.cuda.empty_cache()
    return {'baseline_parameters':base_params,'arms':audits}

def run_arm(ctx,ds,seed,arm,ts,vs,modes,job,status):
    from dcdlp import train as tm
    from dcdlp.train import edge_index_from_graph,score_pairs
    from dcdlp.evaluation.ranking import ranking_metrics
    path=job/f'{arm}.json'; code=sources()
    if path.exists():
        old=read_json(path)
        if old.get('state')=='COMPLETE' and old.get('execution_sources')==code and old.get('epochs')==10 and old.get('seed')==seed and old.get('selected_negative_hash')==ctx['selected_hash'] and old.get('validation_candidate_hash')==ctx['valid_hash'] and Path(old.get('checkpoint','')).is_file():
            if p.sha256_file(Path(old['checkpoint']))==old.get('checkpoint_sha256'): return old
    real_t,real_v=ts.real,vs.real
    if arm in modes: ts.real,vs.real=modes[arm]
    cls=model_class(arm,ts,vs); captured=[]
    old_cls,old_train,old_loss=tm.DCDLP,tm.train_model,tm.link_prediction_loss
    old_ep,old_out=p.v16.engine.EPOCHS,p.v16.engine.OUT
    def capture(*a,**kw):
        model,result=old_train(*a,**kw); captured.append(model); return model,result
    progress={'samples':0,'epoch':0}; epoch_samples=2*len(ctx['train_pos'])
    def loss_progress(logits,labels,*a,**kw):
        result=old_loss(logits,labels,*a,**kw); progress['samples']+=int(labels.numel())
        if progress['samples']==epoch_samples:
            progress['epoch']+=1; progress['samples']=0
            write_json(status,{'state':'RUNNING','dataset':ds,'seed':seed,'epochs':10,'current_arm':arm,'training_epoch_completed':progress['epoch'],'test_evaluated':False})
            print(f'{ds} seed{seed} {arm} epoch {progress["epoch"]}/10 complete',flush=True)
        return result
    tm.DCDLP=cls; tm.train_model=capture; tm.link_prediction_loss=loss_progress
    p.v16.engine.EPOCHS=10; p.v16.engine.OUT=job/'engine_state'; p.v16.engine.candidate_pool=ctx['pool']; p.v16.engine.candidate_pool_hash=ctx['pool_hash']; p.v16.engine.validation_candidate_hash=ctx['valid_hash']
    arm_dir=job/'arms'/arm; torch.cuda.reset_peak_memory_stats(); started=time.perf_counter()
    try:
        rec=p.v16.engine.train_one(ctx['view'],f'HSPE_V17_1_{arm}',seed,ctx['selected'],str(arm_dir),ctx['valid_pos'],ctx['valid_neg'],initialize_from_v6=False,dataset_name=ds,hypergraph_mode='raw')
    finally:
        tm.DCDLP=old_cls; tm.train_model=old_train; tm.link_prediction_loss=old_loss; p.v16.engine.EPOCHS=old_ep; p.v16.engine.OUT=old_out
    try:
        ckpt=Path(rec['checkpoint'])
        if captured: model=captured[0]
        else:
            # The frozen engine may resume a completed checkpoint without
            # calling train_model. Load it instead of requiring a capture.
            model=make_model(cls,ctx['view'],ds); model.load_state_dict(torch.load(ckpt,map_location='cuda',weights_only=False)['model'],strict=True)
        model.eval(); x=torch.as_tensor(ctx['view'].features,dtype=torch.float32,device='cuda'); edge=edge_index_from_graph(ctx['view'].train_graph(),torch.device('cuda')); t=time.perf_counter()
        with torch.no_grad():
            pos=score_pairs(model,x,edge,ctx['valid_pos'],batch_size=8192)['logit']; neg=score_pairs(model,x,edge,ctx['valid_neg'].reshape(-1,2),batch_size=8192)['logit']
        infer=time.perf_counter()-t; metrics=ranking_metrics(pos,neg.reshape(len(pos),ctx['valid_neg'].shape[1])); n=sum(x.numel() for x in model.parameters())
        row={'state':'COMPLETE','dataset':ds,'seed':seed,'epochs':10,'arm':arm,'test_evaluated':False,'validation_only':True,'validation_metrics':metrics,'checkpoint':str(ckpt),'checkpoint_sha256':p.sha256_file(ckpt),'execution_sources':code,'train_pool_hash':ctx['pool_hash'],'selected_negative_hash':ctx['selected_hash'],'validation_candidate_hash':ctx['valid_hash'],'trainable_parameters':n,'added_parameters':n-ctx['baseline_params'],'train_seconds':rec.get('train_seconds'),'validation_scoring_seconds':infer,'wall_seconds':time.perf_counter()-started,'peak_gpu_allocated_mb':torch.cuda.max_memory_allocated()/1024**2,'checkpoint_rule':'fixed final epoch 10; no validation selection','engine_cache_resumed':not bool(captured)}
        if arm=='H1_HSPE_REAL': row['definition']='exact frozen V17 H1 = V16 C1_NHMC_SIZE'
        if arm=='C2_CONSTANT_SET': row['definition']='exact frozen V17 C3: constant [1,1,1] size descriptors; real counts'
        if arm=='C1_COUNT_PARAM_MATCHED': row['definition']='2 log-counts padded by 4 zeros; Linear(6,8), ReLU, hidden duplicated to 16; append 2 counts; zero-init Linear(18,1); 75 params'
        write_json(path,row); print(f'COMPLETE {ds} seed{seed} {arm} MRR={metrics["mrr"]:.6f}',flush=True)
        del model,captured; torch.cuda.empty_cache(); return row
    finally: ts.real,vs.real=real_t,real_v

def run_one(ds,seed,phase):
    torch.set_num_threads(int(os.environ.get('OMP_NUM_THREADS','4')))
    torch.set_num_interop_threads(1)
    ctx=p.build_context(ds); meta=read_json(OUT/'features'/ds/'metadata.json'); ts,vs=stores(ctx)
    # The same input/cache hashes must hold for all seeds and both phases.
    if meta['identity']['selected_hash']!=ctx['selected_hash'] or meta['identity']['valid_hash']!=ctx['valid_hash']: raise RuntimeError('Prepared feature split mismatch')
    const=[]; shuffled=[]; ranked=[]
    for split,cache in (('train',ctx['train_cache']),('valid',ctx['valid_cache'])):
        a=np.zeros_like(cache['tokens_real']); a[:,:3]=1.; const.append(torch.as_tensor(a,device='cuda'))
        shuffled.append(torch.as_tensor(np.load(meta['splits'][split]['shuffle_path']),device='cuda'))
        ranked.append(torch.as_tensor(np.load(meta['splits'][split]['rank_path']),device='cuda'))
    modes={'C2_CONSTANT_SET':tuple(const),'C3_GLOBAL_SIZE_SHUFFLE':tuple(shuffled),'H2_R_HSPE':tuple(ranked)}
    audit=zero_audit(ctx,ds,ts,vs); ctx['baseline_params']=audit['baseline_parameters']
    job=OUT/'experiments'/phase/ds/f'seed_{seed}'; status=job/'status.json'; rows={}
    write_json(job/'input_audit.json',ctx['audit']); write_json(job/'zero_init_audit.json',audit)
    arms=ARMS if phase=='phase_a' else ('H2_R_HSPE',)
    for arm in arms:
        write_json(status,{'state':'RUNNING','dataset':ds,'seed':seed,'epochs':10,'current_arm':arm,'completed_arms':list(rows),'test_evaluated':False})
        rows[arm]=run_arm(ctx,ds,seed,arm,ts,vs,modes,job,status)
    write_json(job/'results.json',{'state':'COMPLETE','dataset':ds,'seed':seed,'epochs':10,'arms':rows,'mrr':{k:v['validation_metrics']['mrr'] for k,v in rows.items()},'feature_metadata_path':str(OUT/'features'/ds/'metadata.json'),'test_evaluated':False})
    write_json(status,{'state':'COMPLETE','dataset':ds,'seed':seed,'epochs':10,'completed_arms':list(rows),'test_evaluated':False})

def stat(values):
    a=np.asarray(values,dtype=float); return {'mean':float(a.mean()),'std':float(a.std(ddof=1)),'median':float(np.median(a)),'min':float(a.min()),'max':float(a.max()),'per_seed':a.tolist()}

def paired(rows,a,b):
    d=[r['arms'][a]['validation_metrics']['mrr']-r['arms'][b]['validation_metrics']['mrr'] for r in rows]
    return {**stat(d),'wins':int(np.sum(np.asarray(d)>0))}

def efficacy(delta): return delta['wins']>=4 and delta['mean']>=.005 and delta['median']>0

def mechanism_summary(a):
    supported={ds:a['datasets'][ds]['effects']['SizeContentGain']['mean']>=.002 and a['datasets'][ds]['effects']['SizeContentGain']['wins']>=3 and a['datasets'][ds]['effects']['H1_vs_CountMatched']['mean']>=.002 for ds in DATASETS}
    label='HSPE_SIZE_CONTENT_SUPPORTED' if all(supported.values()) else 'HSPE_SIZE_CONTENT_DATASET_DEPENDENT' if any(supported.values()) else 'HSPE_CONTEXT_DRIVEN'
    assignment=all(all(v['informative_fraction']>=.5 for v in a['datasets'][ds]['features']['splits'].values()) and a['datasets'][ds]['effects']['ShuffleAssignmentGain']['wins']>=3 and a['datasets'][ds]['effects']['ShuffleAssignmentGain']['mean']>0 for ds in DATASETS)
    return {'interpretation':label,'size_content_by_dataset':supported,'candidate_assignment_supported':assignment,'descriptive_size_effect_rule':'mean >=0.002 and >=3/5 wins versus constant-set, and mean >=0.002 versus count-matched; descriptive only','control_comparisons_are_diagnostic_only':True,'contrasts_are_not_causal_decomposition':True}

def summarize_a():
    out={'datasets':{},'both_datasets_pass':False}
    for ds in DATASETS:
        rows=[read_json(OUT/'experiments'/'phase_a'/ds/f'seed_{s}'/'results.json') for s in SEEDS]
        metrics={a:{k:stat([r['arms'][a]['validation_metrics'][k] for r in rows]) for k in ('mrr','hits10','hits20','mean_positive_rank')} for a in ARMS}
        effects={name:paired(rows,a,b) for name,a,b in (('TotalGain','H1_HSPE_REAL','B0_BASELINE'),('CountLinearGain','C0_COUNT_LINEAR','B0_BASELINE'),('CountCapacityGain','C1_COUNT_PARAM_MATCHED','C0_COUNT_LINEAR'),('SetPathwayGain','C2_CONSTANT_SET','C1_COUNT_PARAM_MATCHED'),('SizeContentGain','H1_HSPE_REAL','C2_CONSTANT_SET'),('ShuffleAssignmentGain','H1_HSPE_REAL','C3_GLOBAL_SIZE_SHUFFLE'))}
        effects['H1_vs_CountMatched']=paired(rows,'H1_HSPE_REAL','C1_COUNT_PARAM_MATCHED')
        costs={a:{'parameters':rows[0]['arms'][a]['trainable_parameters'],'training_seconds':stat([r['arms'][a]['train_seconds'] for r in rows]),'inference_seconds':stat([r['arms'][a]['validation_scoring_seconds'] for r in rows]),'peak_GPU_MB':stat([r['arms'][a]['peak_gpu_allocated_mb'] for r in rows])} for a in ARMS}
        out['datasets'][ds]={'seed_results':rows,'metrics':metrics,'effects':effects,'efficacy_pass':efficacy(effects['TotalGain']),'costs':costs,'features':read_json(OUT/'features'/ds/'metadata.json')}
    out['both_datasets_pass']=all(x['efficacy_pass'] for x in out['datasets'].values()); return out

def summarize_rank(a):
    out={'datasets':{}}
    for ds in DATASETS:
        rows=[read_json(OUT/'experiments'/'phase_rank'/ds/f'seed_{s}'/'results.json') for s in SEEDS]
        originals=a['datasets'][ds]['seed_results']; d=[rows[s]['mrr']['H2_R_HSPE']-originals[s]['mrr']['H1_HSPE_REAL'] for s in SEEDS]
        baseline=[rows[s]['mrr']['H2_R_HSPE']-originals[s]['mrr']['B0_BASELINE'] for s in SEEDS]
        out['datasets'][ds]={'seed_results':rows,'H2_minus_H1':stat(d),'H2_minus_B0':{**stat(baseline),'wins':int(np.sum(np.asarray(baseline)>0))},'metrics':{k:stat([r['arms']['H2_R_HSPE']['validation_metrics'][k] for r in rows]) for k in ('mrr','hits10','hits20','mean_positive_rank')},'parameters':rows[0]['arms']['H2_R_HSPE']['trainable_parameters'],'costs':{k:stat([r['arms']['H2_R_HSPE'][k] for r in rows]) for k in ('train_seconds','validation_scoring_seconds','peak_gpu_allocated_mb')}}
    means=[out['datasets'][ds]['H2_minus_H1']['mean'] for ds in DATASETS]
    out['promoted']=all(x>=-.001 for x in means) and any(x>=.002 for x in means) and np.mean(means)>0
    out['final_variant']='R_HSPE' if out['promoted'] else 'ORIGINAL_HSPE'; return out

def write_report(data):
    lines=['# HSPE V17.1','',f'STATUS: {data["state"]}','PARENT: HSPE_V17','PRIMARY_DIRECTION: HSPE','TEST_EVALUATED: FALSE',f'FINAL_DECISION: {data.get("final_decision","PENDING")}','',
        'Primary efficacy requires each dataset: >=4/5 positive H1−B0 seed deltas, mean >=0.005, median >0. Controls only scope mechanism claims. Test remains OFF.','']
    a=data.get('phase_a')
    if a:
        for ds,item in a['datasets'].items():
            lines += [f'## {ds.title()} — 10E / 5 seeds',f'Primary efficacy passed: {item["efficacy_pass"]}','', '| Seed | B0 | Count-linear | Count-matched | Constant-set | Global shuffle | H1 |','|---:|---:|---:|---:|---:|---:|---:|']
            lines.insert(len(lines)-3,f'{ds.upper()}_H1_VS_B0: {json.dumps(item["effects"]["TotalGain"])}; {ds.upper()}_5SEED_WINS: {item["effects"]["TotalGain"]["wins"]}/5')
            for r in item['seed_results']: lines.append('| '+str(r['seed'])+' | '+' | '.join(f'{r["mrr"][arm]:.6f}' for arm in ARMS)+' |')
            lines += ['','| Diagnostic | Mean delta | Std | Median | Min | Max | Wins |','|---|---:|---:|---:|---:|---:|---:|']
            for name,d in item['effects'].items(): lines.append(f'| {name} | {d["mean"]:+.6f} | {d["std"]:.6f} | {d["median"]:+.6f} | {d["min"]:+.6f} | {d["max"]:+.6f} | {d["wins"]}/5 |')
            lines += ['','These contrasts are empirical diagnostics, not a causal decomposition.','', '| Arm | MRR mean±std | Hits@10 mean±std | Hits@20 mean±std | Mean positive rank±std |','|---|---|---|---|---|']
            for arm in ARMS:
                lines.append('| '+arm+' | '+' | '.join(f'{item["metrics"][arm][k]["mean"]:.6f} ± {item["metrics"][arm][k]["std"]:.6f}' for k in ('mrr','hits10','hits20','mean_positive_rank'))+' |')
            lines += ['','| Arm / metric | Median | Min | Max | Per-seed values |','|---|---:|---:|---:|---|']
            for arm in ARMS:
                for metric,d in item['metrics'][arm].items(): lines.append(f'| {arm} / {metric} | {d["median"]:.6f} | {d["min"]:.6f} | {d["max"]:.6f} | '+', '.join(f'{v:.6f}' for v in d['per_seed'])+' |')
            lines += ['','| Arm | Parameters | Mean train seconds | Mean scoring seconds | Mean peak GPU MB |','|---|---:|---:|---:|---:|']
            for arm,c in item['costs'].items(): lines.append(f'| {arm} | {c["parameters"]} | {c["training_seconds"]["mean"]:.2f} | {c["inference_seconds"]["mean"]:.2f} | {c["peak_GPU_MB"]["mean"]:.2f} |')
            for split,s in item['features']['splits'].items(): lines.append(f'SHUFFLE_POWER {split}: {s["informative_fraction"]:.4%}; {s["power"]}; nonempty candidate ceiling {s["nonempty_candidate_fraction"]:.4%}.')
            lines += [f'RUNTIME feature construction seconds: {item["features"]["feature_construction_seconds"]:.2f}.','PARAMETERS: see per-arm cost table.','COUNT_LINEAR: C0−B0; COUNT_PARAM_MATCHED: C1−C0; CONSTANT_SET: C2−C1.','HIGH_POWER_SHUFFLE: C3 global hyperedge size-label permutation, not pair multiset swapping.','SIZE_CONTENT_EFFECT: H1−C2; CONTEXT_PATHWAY_EFFECT: C0/C1/C2 contrasts above.','']
    rank=data.get('rank_screen'); lines += ['## R-HSPE and freeze',f'R_HSPE: {"COMPLETED" if rank else "CONDITIONAL_OR_SKIPPED"}',f'FINAL_VARIANT: {data.get("final_variant","PENDING")}','']
    if rank:
        for ds,item in rank['datasets'].items(): lines += [f'{ds}: H2−H1 {json.dumps(item["H2_minus_H1"]) }; H2−B0 {json.dumps(item["H2_minus_B0"])}; parameters {item["parameters"]}.',f'H2 metrics: {json.dumps(item["metrics"])}',f'H2 runtime: {json.dumps(item["costs"])}','']
    lines += [f'FINAL_VARIANT_VS_B0: {json.dumps(data.get("final_validation",{}))}','','## Mechanism interpretation','MECHANISM_INTERPRETATION: '+json.dumps(data.get('mechanism',{}),indent=2,ensure_ascii=False),'','CLAIM_SCOPE: candidate-specific hyperedge-pair context representation preserving the incident hyperedge cardinality distribution for link decoding. Do not claim first use of hyperedge size or size as sole mechanism.','',f'NEXT_EXPECTED_STEP: {data.get("next_expected_step","Retrieve completed validation results; review frozen variant and mechanism before any test.")}','']
    if data.get('error'): lines += ['## Execution error',data['error']]
    (OUT/'FINAL_REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    if a: (OUT/'03_HSPE_10E_5SEED.md').write_text('\n'.join(lines[lines.index('## '+DATASETS[0].title()+' — 10E / 5 seeds'):]),encoding='utf-8')
    if rank: (OUT/'04_RANK_HSPE.md').write_text(json.dumps(rank,indent=2),encoding='utf-8')
    if data.get('final_variant'): (OUT/'05_FINAL_VALIDATION.md').write_text(json.dumps({'final_variant':data['final_variant'],'final_validation':data.get('final_validation'),'test_evaluated':False},indent=2),encoding='utf-8')

def save(data): write_json(OUT/'results.json',data); write_report(data)

def run_phase(phase,concurrency):
    pending=[(ds,seed) for seed in SEEDS for ds in DATASETS]; active={}; done=[]; failed=[]; env=os.environ.copy()
    status=OUT/'diagnostics'/f'{phase}_status.json'; (OUT/'logs').mkdir(parents=True,exist_ok=True)
    while pending or active:
        while pending and len(active)<concurrency and not failed:
            ds,seed=pending.pop(0); log=OUT/'logs'/f'{phase}_{ds}_seed{seed}.log'
            with log.open('ab',buffering=0) as f:
                proc=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),'run-one',ds,str(seed),phase],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,env=env,start_new_session=True)
            active[proc.pid]=(proc,ds,seed)
        for pid,(proc,ds,seed) in list(active.items()):
            code=proc.poll()
            if code is not None:
                (done if code==0 else failed).append({'dataset':ds,'seed':seed,'pid':pid,'exit_code':code}); del active[pid]
        write_json(status,{'state':'FAILED' if failed else 'RUNNING' if active or pending else 'COMPLETE','phase':phase,'completed_jobs':done,'failed_jobs':failed,'active_jobs':[{'pid':pid,'dataset':d,'seed':s} for pid,(_,d,s) in active.items()],'pending_jobs':pending,'test_evaluated':False,'updated_at':time.time()})
        if failed and not active: break
        if active: time.sleep(5)
    if failed: raise RuntimeError(f'{phase}: {failed}')

def run_all(concurrency):
    assert 2<=concurrency<=4
    data={'state':'PREFLIGHT','parent':'HSPE_V17','direction':'HSPE_V17_1','test_evaluated':False,'phase_a':None,'rank_screen':None,'final_variant':None,'final_decision':'PENDING','protocol':{'datasets':DATASETS,'seeds':SEEDS,'epochs':10,'arms':ARMS,'concurrency':concurrency,'primary_gate':'wins>=4/5; mean>=0.005; median>0 each dataset','controls':'claim scoping only','rank_variant':'one ECDF substitution only'}}; save(data)
    try:
        for ds in DATASETS: prepare(ds)
        data['state']='PHASE_A_RUNNING'; save(data); run_phase('phase_a',concurrency)
        a=summarize_a(); data['phase_a']=a; data['mechanism']=mechanism_summary(a)
        if not a['both_datasets_pass']:
            data['state']='HSPE_EFFICACY_REJECT'; data['final_decision']=data['state']; data['next_expected_step']='Review completed efficacy and mechanism evidence. No refinement or test.'; save(data); return
        data['state']='HSPE_EFFICACY_CONFIRMED'; data['primary_efficacy']='HSPE_EFFICACY_CONFIRMED'; save(data)
        data['state']='R_HSPE_SCREEN_RUNNING'; save(data); run_phase('phase_rank',concurrency)
        rank=summarize_rank(a); data['rank_screen']=rank; data['final_variant']=rank['final_variant']
        final={ds:rank['datasets'][ds]['H2_minus_B0'] if rank['promoted'] else a['datasets'][ds]['effects']['TotalGain'] for ds in DATASETS}
        data['final_validation']={ds:{'delta':d,'passed':efficacy(d)} for ds,d in final.items()}
        data['mechanism']=mechanism_summary(a)
        data['state']='HSPE_VALIDATION_CONFIRMED' if all(x['passed'] for x in data['final_validation'].values()) else 'HSPE_EFFICACY_CONFIRMED'
        data['final_decision']=data['state']; data['variant_decision']='R_HSPE_SELECTED' if rank['promoted'] else 'ORIGINAL_HSPE_SELECTED'; data['next_expected_step']='User reviews frozen method version and mechanism claims; test OFF.'; save(data)
        (OUT/'06_NOVELTY_SCOPE.md').write_text(json.dumps({'claim_scope':'candidate-specific hyperedge-pair context representation preserving the local incident hyperedge cardinality distribution for link decoding','distinction':'pair-specific local hyperedge-size sets versus global order weighting','mechanism':data['mechanism'],'no_first_size_claim':True,'novelty_priority_not_independently_established':True,'test_evaluated':False},indent=2),encoding='utf-8')
    except Exception as e:
        data['state']='FAILED'; data['error']=str(e); data['traceback']=traceback.format_exc(); save(data); raise

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('run-all'); a.add_argument('--concurrency',type=int,default=4)
    b=sub.add_parser('run-one'); b.add_argument('dataset',choices=DATASETS); b.add_argument('seed',type=int,choices=SEEDS); b.add_argument('phase',choices=('phase_a','phase_rank'))
    c=sub.add_parser('prepare'); c.add_argument('dataset',choices=DATASETS); c.add_argument('--workers',type=int,default=8)
    d=sub.add_parser('preflight'); d.add_argument('dataset',choices=DATASETS)
    args=ap.parse_args()
    if args.cmd=='run-all':run_all(args.concurrency)
    elif args.cmd=='run-one':run_one(args.dataset,args.seed,args.phase)
    elif args.cmd=='prepare':prepare(args.dataset,args.workers)
    else:
        torch.set_num_threads(4); ctx=p.build_context(args.dataset); ts,vs=stores(ctx); audit=zero_audit(ctx,args.dataset,ts,vs); write_json(OUT/'diagnostics'/f'{args.dataset}_model_preflight.json',audit);print(json.dumps(audit,indent=2))

if __name__=='__main__': main()
