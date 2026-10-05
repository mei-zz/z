from __future__ import annotations
import argparse, ast, gc, hashlib, importlib.util, json, multiprocessing as mp, os, subprocess, sys, time, traceback
from pathlib import Path
import numpy as np

OUT=Path(__file__).resolve().parents[1]
PARENT=OUT.parent/'HSPE_V17_1'
sp=importlib.util.spec_from_file_location('frozen_v171',PARENT/'scripts/hspe_v17_1.py')
m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
torch=m.torch
FROZEN=OUT.parent/'R_HSPE_FROZEN'
METRICS=('mrr','hits10','hits20','mean_positive_rank')
DS=('cora','pubmed')

def safe(v):
    if isinstance(v,np.generic):return v.item()
    if isinstance(v,dict):return {k:safe(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [safe(x) for x in v]
    return v
def write(p,v):m.write_json(p,safe(v))
def read(p):return m.read_json(p)
def digest(v):return hashlib.sha256(json.dumps(safe(v),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def status(state,**kw):write(OUT/'status.json',{'state':state,'updated_at':time.time(),**kw})
def stat(v):return m.stat(v)
def paired(rows,a,b):
    d=[r['arms'][a]['metrics']['mrr']-r['arms'][b]['metrics']['mrr'] for r in rows]
    return {**stat(d),'wins':sum(x>0 for x in d)}

def parent_row(ds,seed,arm):
    phase='phase_rank' if arm=='H2_R_HSPE' else 'phase_a'
    return read(PARENT/'experiments'/phase/ds/f'seed_{seed}'/'results.json')['arms'][arm]

def normalized_config(c):return {k:v for k,v in c.items() if k not in ('dataset','seed','output_dir')}

def preflight():
    result=read(PARENT/'results.json')
    assert result['state']=='HSPE_VALIDATION_CONFIRMED' and result['final_variant']=='R_HSPE'
    assert result['mechanism']['interpretation']=='HSPE_CONTEXT_DRIVEN'
    src=m.sources(); text=(PARENT/'scripts/hspe_v17_1.py').read_text()
    before=text.replace('        # CUDA message aggregation can vary by one float32 ULP across forward\n        # calls even with bit-identical parameters and a zero residual head.\n        # 5e-7 accepts that round-off while still checking the initial function.\n','').replace('err<=5e-7','err<=2e-7').replace("'logit_roundoff_tolerance':5e-7,",'')
    oldhash=hashlib.sha256(before.encode()).hexdigest()
    assert oldhash=='94eae10a845b3f4930edc776d0e9b18c104c9f40e0ae7dc7d93b6fe875cab4c3'
    def method_ast(t):
        tree=ast.parse(t);tree.body=[x for x in tree.body if not isinstance(x,ast.FunctionDef) or x.name!='zero_audit'];return ast.dump(tree,include_attributes=False)
    assert method_ast(text)==method_ast(before)
    source_variants={src['v171'],oldhash}; controls={ds:max(('C0_COUNT_LINEAR','C1_COUNT_PARAM_MATCHED','C2_CONSTANT_SET'),key=lambda a:result['phase_a']['datasets'][ds]['metrics'][a]['mrr']['mean']) for ds in DS}
    refs=[]; configs={}; common=None
    for ds in DS:
        for seed in range(5):
            for arm in ('B0_BASELINE','H2_R_HSPE',controls[ds]):
                row=parent_row(ds,seed,arm); assert row['state']=='COMPLETE' and row['epochs']==10 and not row['test_evaluated']
                assert row['execution_sources']['v171'] in source_variants
                for k,v in src.items():
                    if k!='v171': assert row['execution_sources'][k]==v,(ds,seed,arm,k,'STOP_SOURCE_MISMATCH')
                path=Path(row['checkpoint']);assert path.is_file() and m.p.sha256_file(path)==row['checkpoint_sha256']
                checkpoint=torch.load(path,map_location='cpu',weights_only=False);config=checkpoint['config'];n=sum(x.numel() for x in checkpoint['model'].values());assert n==row['trainable_parameters']
                if common is None:common=normalized_config(config)
                assert normalized_config(config)==common,(ds,seed,arm,'STOP_CONFIG_MISMATCH')
                assert config['pretrain_epochs']==10 and config['hidden_dim']==16 and config['branch_dim']==8 and config['batch_size']==4096
                configs[f'{ds}/{seed}/{arm}']={'config':config,'config_sha256':digest(config),'normalized_config_sha256':digest(common)}
                refs.append({k:row[k] for k in ('dataset','seed','arm','checkpoint','checkpoint_sha256','execution_sources','trainable_parameters','added_parameters','train_pool_hash','selected_negative_hash','validation_candidate_hash')})
                del checkpoint
        meta=read(PARENT/'features'/ds/'metadata.json')
        for f in meta['files']:assert m.p.sha256_file(Path(f['path']))==f['sha256'],('STOP_FEATURE_MISMATCH',ds,f['path'])
    manifest={'state':'PASS','parent_status':result['state'],'final_variant':'R_HSPE','mechanism':'HSPE_CONTEXT_DRIVEN','size_causal_claim':'NOT_SUPPORTED','sources':src,'historical_source_variants':sorted(source_variants),'source_variant_difference':'only zero_audit tolerance 2e-7 -> 5e-7 and audit metadata; all other AST nodes identical','configurations':configs,'common_config':common,'common_config_sha256':digest(common),'controls':controls,'control_selection':'highest V17.1 five-seed validation MRR among C0/C1/C2; selected before test','checkpoint_references':refs,'no_method_or_training_change':True,'test_candidate_policy':'frozen QTHS V7.1 standard test candidates, seed999/group1000, 20 negatives, full positives filtered only during evaluation','evaluator':'frozen score_pairs batch8192, ranking_metrics; train message graph only; target masking True','runner_sha256':m.p.sha256_file(Path(__file__))}
    write(OUT/'SOURCE_HASHES.json',manifest);write(OUT/'FINAL_CONFIG.json',{'common':common,'common_sha256':digest(common),'datasets':DS,'test_seeds':list(range(5)),'third_dataset':'citeseer','third_seeds':[0,1,2],'epochs':10,'qths25':.25,'controls':controls,'parent_checkpoints':refs,'configs':configs,'no_further_tuning':True})
    (OUT/'METHOD_DEFINITION.md').write_text('''# Frozen R-HSPE method

R-HSPE uses the exact V17.1 H2 model. In the training-visible raw-star hypergraph, each candidate node pair (u,v) defines tokens (w,e,f) where w is a common projected support node, e contains u,w, and f contains v,w. Identity multiplicities and token topology are preserved; the predicted training edge is removed before token construction.

Training-only ECDF F(s)=#{training-visible active hyperedges with size <=s}/#active hyperedges maps effective |e|,|f| into ranks a,b. Each token is [a+b, abs(a-b), a*b, 0,0,0]. The frozen Linear(6,8)+ReLU encoder is pooled by mean and max. Two explicit descriptors log1p(token_count), log1p(support_count) are appended; a zero-initialized Linear(18,1) residual is added to the frozen Raw-HG DCDLP logit. Added parameter count is 75.

Optimizer, learning rate 0.001, weight decay 0.0001, dimensions16/8, two GCN layers, dropout0, batch4096, QTHS25, loss, and fixed final epoch10 remain identical to V17.1. Evaluator is score_pairs(batch8192), target removal True, ranking_metrics with 20 negative candidates. Test graph features use training-visible structure, and test ECDF uses only training-visible hyperedges. All parent checkpoints and source/config hashes are recorded before test.

Primary candidate claim: candidate-specific hyperedge-pair context encoding. Secondary component: training-only rank-normalized cardinality descriptors. Mechanism: context-driven. Size causal claim: NOT_SUPPORTED. Rank normalization alone is not the primary innovation. Cross-graph scale invariance is algebraic under strictly increasing size transforms, but reduced empirical cross-graph sensitivity has not been isolated causally.
''',encoding='utf8')
    return manifest

G=None
def feature_piece(bounds):
    struct=G['struct'];pairs=G['pairs'];targets=G['targets'];dist=G['dist'];sizes=struct['degree'].astype(np.int64)+1
    rows=[]
    for row in range(*bounds):
        u,v=map(int,pairs[row]);mask=(u*struct['n']+v) in targets
        shared,mu,mv,_,_,_,expected=m.p.v16.stage0._pair_projection(struct,u,v,mask)
        raw=[];rank=[]
        for w,nu,nv in zip(shared.tolist(),mu.tolist(),mv.tolist()):
            e=struct['incident'][u].intersection(struct['incident'][w]);f=struct['incident'][v].intersection(struct['incident'][w])
            if mask:e.discard(v);f.discard(u)
            assert len(e)==nu and len(f)==nv
            ee=np.asarray(sorted(e),dtype=np.int64);ff=np.asarray(sorted(f),dtype=np.int64)
            se=sizes[ee]-((ee==u)|(ee==v))*int(mask);sf=sizes[ff]-((ff==u)|(ff==v))*int(mask)
            se=se[se>1];sf=sf[sf>1];aa=np.repeat(se,len(sf));bb=np.tile(sf,len(se))
            raw.append(m.descriptor(np.log1p(aa),np.log1p(bb)));rank.append(m.descriptor(np.searchsorted(dist,aa,side='right')/len(dist),np.searchsorted(dist,bb,side='right')/len(dist)))
        raw=np.concatenate(raw) if raw else np.zeros((0,6),np.float32);rank=np.concatenate(rank) if rank else np.zeros((0,6),np.float32)
        assert len(raw)==expected
        rows.append((row,raw,rank,len(shared)))
    return rows

def make_features(ds,split,view,pairs,targets,workers):
    dest=OUT/'features'/ds/split;dest.mkdir(parents=True,exist_ok=True);path=dest/'cache.npz';meta_path=dest/'metadata.json'
    canonical=m.p.v16.stage0.canonical_pairs(np.asarray(pairs,np.int64));unique=np.unique(canonical,axis=0)
    target=m.p.v16.stage0.canonical_pairs(np.asarray(targets,np.int64));struct=m.p.v16.stage0.build_structure(m.p.v16.stage0.build_adjacency(view.num_nodes,np.asarray(view.train_pos,np.int64)))
    sizes=struct['degree'].astype(np.int64)+1;dist=np.sort(sizes[sizes>1]);keys=unique[:,0]*view.num_nodes+unique[:,1]
    identity={'dataset':ds,'split':split,'keys_sha256':m.p.v16.v61.array_hash(keys),'train_positive_sha256':m.p.v16.v61.array_hash(view.train_pos),'target_mask_sha256':m.p.v16.v61.array_hash(target),'ecdf_sha256':m.p.v16.v61.array_hash(dist),'method_source':read(OUT/'SOURCE_HASHES.json')['sources']['v171']}
    if path.exists() and meta_path.exists():
        old=read(meta_path)
        if old['identity']==identity and m.p.sha256_file(path)==old['archive_sha256']:
            with np.load(path,allow_pickle=False) as z:return {k:z[k].copy() for k in z.files},old
    global G
    G={'struct':struct,'pairs':unique,'targets':set((target[:,0]*view.num_nodes+target[:,1]).tolist()),'dist':dist}
    started=time.perf_counter();pieces=[None]*len(unique);done=0
    with mp.get_context('fork').Pool(workers) as pool:
        for block in pool.imap_unordered(feature_piece,[(i,min(i+128,len(unique))) for i in range(0,len(unique),128)]):
            for row,raw,rank,support in block:pieces[row]=(raw,rank,support)
            done+=len(block)
            if done%4096<128:write(dest/'progress.json',{'completed_pairs':done,'total_pairs':len(unique),'state':'RUNNING'})
    counts=np.asarray([len(x[0]) for x in pieces],np.int64);offsets=np.r_[0,np.cumsum(counts)]
    cache={'keys':keys,'offsets':offsets,'tokens_real':np.concatenate([x[0] for x in pieces]),'tokens_rank':np.concatenate([x[1] for x in pieces]),'support':np.asarray([x[2] for x in pieces],np.float32)}
    # Independently compare the frozen token constructor on nonempty rows.
    checked=0;maxerr=0.
    for row in np.flatnonzero(counts)[:16]:
        u,v=map(int,unique[row]);mask=(u*view.num_nodes+v) in G['targets'];tok=list(m.p.v16.stage0._iter_native_tokens(struct,u,v,mask));expected=np.asarray([x[0] for x in tok],np.float32)
        part=cache['tokens_real'][offsets[row]:offsets[row+1],:3];assert part.shape==expected.shape
        err=float(np.max(np.abs(part-expected)));assert err<=2e-6;maxerr=max(maxerr,err);checked+=1
    np.savez(path,**cache)
    meta={'state':'COMPLETE','identity':identity,'archive_sha256':m.p.sha256_file(path),'pair_count':len(keys),'token_count':int(offsets[-1]),'ecdf_fit':'training-visible active hyperedges only','ecdf_values':dist.tolist(),'native_token_constructor_audit_rows':checked,'max_token_descriptor_error':maxerr,'construction_seconds':time.perf_counter()-started,'target_mask':'training positive candidates masked; heldout candidates absent from train graph'}
    write(meta_path,meta);G=None;del pieces;gc.collect();return cache,meta

def new_store(cache,view,arm):
    st=m.p.Store(cache,view.num_nodes,torch.device('cuda'))
    st.counts=torch.as_tensor(np.column_stack((np.log1p(np.diff(cache['offsets'])),np.log1p(cache['support']))),dtype=torch.float32,device='cuda')
    if arm=='H2_R_HSPE':st.real=torch.as_tensor(cache['tokens_rank'],device='cuda')
    if arm=='C2_CONSTANT_SET':
        constant=np.zeros_like(cache['tokens_real']);constant[:,:3]=1.;st.real=torch.as_tensor(constant,device='cuda')
    return st

def evaluate(view,pos,neg,cache,row,split,seed):
    from dcdlp.train import edge_index_from_graph,score_pairs
    from dcdlp.evaluation.ranking import ranking_metrics
    arm=row['arm'];st=new_store(cache,view,arm);model=m.make_model(m.model_class(arm,st,st),view,view.name.lower());ckpt=Path(row['checkpoint']);assert m.p.sha256_file(ckpt)==row['checkpoint_sha256']
    model.load_state_dict(torch.load(ckpt,map_location='cuda',weights_only=False)['model'],strict=True);model.eval();n=sum(p.numel() for p in model.parameters());assert n==row['trainable_parameters']
    x=torch.as_tensor(view.features,dtype=torch.float32,device='cuda');edge=edge_index_from_graph(view.train_graph(),torch.device('cuda'));start=time.perf_counter();torch.cuda.reset_peak_memory_stats()
    with torch.no_grad():
        ps=score_pairs(model,x,edge,pos,batch_size=8192)['logit'];ns=score_pairs(model,x,edge,neg.reshape(-1,2),batch_size=8192)['logit']
    metrics=ranking_metrics(ps,ns.reshape(len(pos),neg.shape[1]))
    result={'state':'COMPLETE','arm':arm,'seed':seed,'dataset':view.name.lower(),'split':split,'metrics':metrics,'checkpoint':str(ckpt),'checkpoint_sha256':row['checkpoint_sha256'],'parameters':n,'scoring_seconds':time.perf_counter()-start,'peak_gpu_allocated_mb':torch.cuda.max_memory_allocated()/1024**2,'evaluator_sources':m.p._source_hashes(),'fixed_final_epoch':10,'test_guided_change':False}
    del model,st,x,edge;gc.collect();torch.cuda.empty_cache();return result,ps,ns

def prepare_test(ds,workers):
    manifest=read(OUT/'SOURCE_HASHES.json');ctx=m.p.build_context(ds);full,view=m.p.v16.base.init_dataset(ds)
    for seed in range(5):
        for arm in ('B0_BASELINE','H2_R_HSPE',manifest['controls'][ds]):
            ref=parent_row(ds,seed,arm);assert ref['train_pool_hash']==ctx['pool_hash'] and ref['selected_negative_hash']==ctx['selected_hash'] and ref['validation_candidate_hash']==ctx['valid_hash']
    # Validate checkpoint loading and frozen evaluator before opening test.
    audit_path=OUT/'diagnostics'/f'{ds}_evaluator_audit.json'
    if not audit_path.exists():
        meta=read(PARENT/'features'/ds/'metadata.json');cache={**ctx['valid_cache'],'tokens_rank':np.load(meta['splits']['valid']['rank_path'])};audit={}
        for arm in ('B0_BASELINE','H2_R_HSPE',manifest['controls'][ds]):
            row=parent_row(ds,0,arm);val,_,_=evaluate(view,ctx['valid_pos'],ctx['valid_neg'],cache,row,'valid_reproduction',0)
            errors={k:abs(val['metrics'][k]-row['validation_metrics'][k]) for k in METRICS};assert max(errors.values())<1e-6,(ds,arm,errors,'STOP_EVALUATOR_MISMATCH');audit[arm]=errors
        write(audit_path,{'state':'PASS','errors':audit,'test_accessed':False})
    pos,neg,h=m.p.v16.base.make_eval_candidates(full,'test');path=OUT/'candidates'/f'{ds}_test.npz';path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        with np.load(path) as z:assert np.array_equal(z['positive'],pos) and np.array_equal(z['negative'],neg)
    else:np.savez(path,positive=pos,negative=neg)
    write(path.with_suffix('.json'),{'dataset':ds,'split':'test','positive_hash':m.p.v16.v61.array_hash(pos),'negative_hash':h,'seed':999,'grouping_seed':1000,'negatives_per_positive':20,'frozen_before_scoring':True,'message_graph':'train only','heldout_positives_filter_only_during_test_sampling':True,'train_positive_hash':m.p.v16.v61.array_hash(view.train_pos)})
    make_features(ds,'test',view,np.vstack((pos,neg.reshape(-1,2))),np.empty((0,2),np.int64),workers)

def test_seed(ds,seed):
    manifest=read(OUT/'SOURCE_HASHES.json');_,view=m.p.v16.base.init_dataset(ds);path=OUT/'candidates'/f'{ds}_test.npz'
    with np.load(path) as z:pos=z['positive'];neg=z['negative']
    with np.load(OUT/'features'/ds/'test/cache.npz') as z:cache={k:z[k].copy() for k in z.files}
    rows={};job=OUT/'test'/ds/f'seed_{seed}';job.mkdir(parents=True,exist_ok=True)
    for arm in ('B0_BASELINE','H2_R_HSPE',manifest['controls'][ds]):
        dest=job/f'{arm}.json'
        if dest.exists():
            rows[arm]=read(dest);assert rows[arm]['checkpoint_sha256']==parent_row(ds,seed,arm)['checkpoint_sha256'];continue
        write(job/'status.json',{'state':'RUNNING','current_arm':arm,'completed_arms':list(rows)})
        ref=parent_row(ds,seed,arm);r,ps,ns=evaluate(view,pos,neg,cache,ref,'test',seed)
        r['candidate_metadata']=read(path.with_suffix('.json'));np.savez_compressed(job/f'{arm}_scores.npz',positive=ps,negative=ns);write(dest,r);rows[arm]=r
    write(job/'results.json',{'state':'COMPLETE','dataset':ds,'seed':seed,'arms':rows});write(job/'status.json',{'state':'COMPLETE'})

def third_context():
    ds='citeseer';_,view=m.p.v16.base.init_dataset(ds);path=OUT/'third/citeseer/context.npz'
    with np.load(path) as z:info={k:z[k].copy() for k in z.files}
    caches={}
    for split in ('train','valid'):
        with np.load(OUT/'features'/ds/split/'cache.npz') as z:caches[split]={k:z[k].copy() for k in z.files}
    return {'view':view,'train_pos':info['train_pos'],'selected':info['selected'],'pool':info['pool'],'valid_pos':info['valid_pos'],'valid_neg':info['valid_neg'],'pool_hash':m.p.v16.v61.array_hash(info['pool']),'selected_hash':m.p.v16.v61.array_hash(info['selected']),'valid_hash':m.p.v16.v61.array_hash(info['valid_neg']),'train_cache':caches['train'],'valid_cache':caches['valid'],'baseline_params':9807}

def third_prepare(workers):
    ds='citeseer';full,view=m.p.v16.base.init_dataset(ds);oldout=m.p.v16.OUT;m.p.v16.OUT=OUT
    try:pool,ph,scores,teacher=m.p.v16._fixed_train_pool(ds,view)
    finally:m.p.v16.OUT=oldout
    train=m.p.v16.stage0.canonical_pairs(np.asarray(view.train_pos,np.int64));qids,qmeta=m.p.v16.v7.make_ids(pool,scores,train,.25);selected=pool[np.arange(len(train)),qids].copy();pos=m.p.v16.stage0.canonical_pairs(np.asarray(full.valid_pos,np.int64));neg,sampling=m.p.v16.make_validation_candidates(view,pos)
    _,forbidden=m.p.v16.v61.make_train_forbidden(view);assert not any(m.p.v16.v61.canonical_edge(x) in forbidden for x in selected)
    job=OUT/'third/citeseer';job.mkdir(parents=True,exist_ok=True);np.savez(job/'context.npz',train_pos=train,pool=pool,selected=selected,valid_pos=pos,valid_neg=neg)
    write(job/'input_audit.json',{'teacher':teacher,'qths25':qmeta,'validation_sampling':sampling,'train_hash':m.p.v16.v61.array_hash(train),'pool_hash':ph,'selected_hash':m.p.v16.v61.array_hash(selected),'valid_pos_hash':m.p.v16.v61.array_hash(pos),'valid_neg_hash':m.p.v16.v61.array_hash(neg),'test_accessed':False})
    make_features(ds,'train',view,np.vstack((train,selected)),train,workers);make_features(ds,'valid',view,np.vstack((pos,neg.reshape(-1,2))),np.empty((0,2),np.int64),workers)

def third_seed(seed):
    ctx=third_context();ds='citeseer';ts=new_store(ctx['train_cache'],ctx['view'],'H2_R_HSPE');vs=new_store(ctx['valid_cache'],ctx['view'],'H2_R_HSPE')
    # Frozen model initialization and training engine; ranks are the only H2 inputs.
    base=m.make_model(m.model_class('B0_BASELINE',ts,vs),ctx['view'],ds);ctx['baseline_params']=sum(p.numel() for p in base.parameters());del base
    oldout=m.OUT;m.OUT=OUT
    try:
        job=OUT/'third/citeseer'/f'seed_{seed}';st=job/'status.json';arms={}
        for arm in ('B0_BASELINE','H2_R_HSPE'):
            ranks={'H2_R_HSPE':(ts.real,vs.real)}
            arms[arm]=m.run_arm(ctx,ds,seed,arm,ts,vs,ranks,job,st)
        write(job/'results.json',{'state':'COMPLETE','dataset':ds,'seed':seed,'arms':arms,'test_evaluated':False});write(st,{'state':'COMPLETE'})
    finally:m.OUT=oldout

def third_test_seed(seed):
    ds='citeseer';_,view=m.p.v16.base.init_dataset(ds)
    with np.load(OUT/'candidates/citeseer_test.npz') as z:pos=z['positive'];neg=z['negative']
    with np.load(OUT/'features/citeseer/test/cache.npz') as z:cache={k:z[k].copy() for k in z.files}
    job=OUT/'third/citeseer'/f'seed_{seed}';rows={}
    for arm in ('B0_BASELINE','H2_R_HSPE'):
        dest=job/f'{arm}_test.json'
        if dest.exists():rows[arm]=read(dest);continue
        ref=read(job/'results.json')['arms'][arm];r,ps,ns=evaluate(view,pos,neg,cache,ref,'test',seed);np.savez_compressed(job/f'{arm}_test_scores.npz',positive=ps,negative=ns);write(dest,r);rows[arm]=r
    write(job/'test_results.json',{'state':'COMPLETE','dataset':ds,'seed':seed,'arms':rows})

def schedule(tasks,limit=4):
    active={};done=[];fail=[];tasks=list(tasks);env=os.environ.copy()
    while tasks or active:
        while tasks and len(active)<limit and not fail:
            task=tasks.pop(0);log=OUT/'logs'/('_'.join(map(str,task))+'.log');log.parent.mkdir(parents=True,exist_ok=True);f=log.open('ab',buffering=0)
            proc=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*map(str,task)],stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,env=env,start_new_session=True);active[proc.pid]=(proc,task,f)
        for pid,(proc,task,f) in list(active.items()):
            code=proc.poll()
            if code is not None:f.close();(done if code==0 else fail).append({'task':task,'pid':pid,'code':code});del active[pid]
        write(OUT/'diagnostics/worker_status.json',{'state':'FAILED' if fail else 'RUNNING' if tasks or active else 'COMPLETE','active':[{'pid':pid,'task':task} for pid,(_,task,_) in active.items()],'pending':tasks,'completed':done,'failed':fail,'updated_at':time.time()})
        if fail and not active:raise RuntimeError(f'Worker failed: {fail}')
        if active:time.sleep(5)

def summarize_tests():
    control=read(OUT/'SOURCE_HASHES.json')['controls'];out={}
    for ds in DS:
        rows=[read(OUT/'test'/ds/f'seed_{s}/results.json') for s in range(5)];arms=('B0_BASELINE','H2_R_HSPE',control[ds]);delta=paired(rows,'H2_R_HSPE','B0_BASELINE');passes=delta['wins']>=(4 if ds=='cora' else 3) and delta['mean']>0 and delta['median']>0
        out[ds]={'seed_results':rows,'metrics':{a:{k:stat([r['arms'][a]['metrics'][k] for r in rows]) for k in METRICS} for a in arms},'R_HSPE_minus_B0':delta,'R_HSPE_minus_context':paired(rows,'H2_R_HSPE',control[ds]),'context_arm':control[ds],'test_supported':passes}
    return out

def finalize():
    tests=summarize_tests();third=read(OUT/'THIRD_DATASET.json');novelty=read(OUT/'NOVELTY_STATUS.json');support=all(x['test_supported'] for x in tests.values());collision=novelty['exact_collision'];decision='NOVELTY_CONFLICT' if collision else 'TEST_GENERALIZATION_FAIL' if not support else 'INNOVATION_1_FROZEN'
    data={'state':'COMPLETE','final_decision':decision,'final_variant':'R_HSPE','method_frozen':decision=='INNOVATION_1_FROZEN','test_results':tests,'third_dataset':third,'novelty':novelty,'mechanism':'CONTEXT_DRIVEN','size_causal_claim':'NOT_SUPPORTED','next_expected_step':'Begin Innovation 2 search on the frozen R-HSPE backbone; user-triggered only.' if decision=='INNOVATION_1_FROZEN' else 'Review failure without rescue.','innovation2_started':False}
    write(OUT/'results.json',data);write(OUT/'TEST_RESULTS.json',tests)
    lines=['# V17.2 final confirmation',f'FINAL_DECISION: {decision}',f'FINAL_VARIANT: R-HSPE','MECHANISM: CONTEXT_DRIVEN','SIZE_CAUSAL_CLAIM: NOT_SUPPORTED','','Frozen final epoch10; one-shot test; shared candidates for all arms; context controls selected by V17.1 validation only.','']
    for ds,block in tests.items():
        lines += [f'## {ds}',f'TEST_SUPPORTED: {block["test_supported"]}','| Arm | MRR mean±std | Hits10 mean±std | Hits20 mean±std | Mean rank±std |','|---|---|---|---|---|']
        for arm,metrics in block['metrics'].items():lines.append('| '+arm+' | '+' | '.join(f'{metrics[k]["mean"]:.6f} ± {metrics[k]["std"]:.6f}' for k in METRICS)+' |')
        lines.extend([f'R_HSPE_MINUS_B0: {json.dumps(block["R_HSPE_minus_B0"])}',f'R_HSPE_MINUS_CONTEXT: {json.dumps(block["R_HSPE_minus_context"])}',''])
    lines.extend(['## Third dataset',json.dumps(third,indent=2),'## Novelty',json.dumps(novelty,indent=2),'NEXT_EXPECTED_STEP: '+data['next_expected_step']])
    (OUT/'FINAL_REPORT.md').write_text('\n'.join(lines),encoding='utf8')
    if decision=='INNOVATION_1_FROZEN':
        FROZEN.mkdir(parents=True,exist_ok=True)
        import shutil
        for name in ('METHOD_DEFINITION.md','NOVELTY_MATRIX.md','TEST_RESULTS.json','FINAL_CONFIG.json','SOURCE_HASHES.json'):
            shutil.copy2(OUT/name,FROZEN/name)
        parent=read(PARENT/'results.json');manifest=read(OUT/'SOURCE_HASHES.json')
        freeze={'INNOVATION_1':'R-HSPE','STATUS':'FROZEN','PRIMARY_CLAIM':'candidate-specific hyperedge-pair context encoding','SECONDARY_COMPONENT':'training-only rank-normalized hyperedge cardinality','MECHANISM_STATUS':'CONTEXT_DRIVEN','SIZE_CAUSAL_CLAIM':'NOT_SUPPORTED','CORA_VALIDATION':parent['final_validation']['cora'],'PUBMED_VALIDATION':parent['final_validation']['pubmed'],'CORA_TEST':tests['cora']['R_HSPE_minus_B0'],'PUBMED_TEST':tests['pubmed']['R_HSPE_minus_B0'],'THIRD_DATASET':third,'PARAMETER_OVERHEAD':75,'NOVELTY_STATUS':novelty['status'],'CODE_HASH':manifest['sources'],'CONFIG_HASH':manifest['common_config_sha256'],'NO_FURTHER_TUNING':True,'SECOND_INNOVATION_BASELINE_ARMS':{'B0':'frozen original baseline','B1':'frozen R-HSPE','B2':'Innovation2 only','B3':'R-HSPE+Innovation2'},'INNOVATION2_STARTED':False}
        (FROZEN/'R_HSPE_FROZEN.md').write_text('# Innovation 1 freeze\n\n'+json.dumps(safe(freeze),indent=2),encoding='utf8');write(FROZEN/'checkpoint_references.json',manifest['checkpoint_references'])
        snapshots=FROZEN/'source_snapshot';snapshots.mkdir(exist_ok=True)
        for label,path in [('v171',PARENT/'scripts/hspe_v17_1.py'),('v17',m.PARENT/'scripts/hspe_v17.py'),('v16_stage1',Path(m.p.v16.__file__)),('stage0',Path(m.p.v16.stage0.__file__)),('qths_v71',Path(m.p.v16.base.__file__)),('negative_v61',Path(m.p.v16.v61.__file__)),('codns_engine',Path(m.p.v16.engine.__file__)),('dcdlp_train',Path(m.p.v16.ROOT)/'src/dcdlp/train.py'),('baseline_config',m.p.v16.v61.BASELINE/'H/config.json')]:shutil.copy2(path,snapshots/(label+path.suffix))
    (OUT/'C2C_HANDOFF.md').write_text('STATUS: EXECUTED\nR_HSPE_METHOD: '+('FROZEN' if data['method_frozen'] else 'NOT_FROZEN')+'\nCORA_TEST: '+str(tests['cora']['test_supported'])+'\nPUBMED_TEST: '+str(tests['pubmed']['test_supported'])+'\nTHIRD_DATASET: '+third['status']+'\nNOVELTY: '+novelty['status']+'\nCLAIM_SCOPE: candidate-specific hyperedge-pair context encoding\nSIZE_CAUSAL_CLAIM: NOT_SUPPORTED\nINNOVATION_1: '+decision+'\nFREEZE_ARTIFACT: '+(str(FROZEN) if data['method_frozen'] else 'NONE')+'\nNEXT_EXPECTED_STEP: '+data['next_expected_step']+'\n',encoding='utf8');status('COMPLETE',final_decision=decision)

def run_all():
    try:
        if not (OUT/'SOURCE_HASHES.json').exists():preflight()
        status('PREPARING_FROZEN_TEST')
        schedule([('prepare-test',ds) for ds in DS],2)
        status('FROZEN_TEST_RUNNING')
        schedule([('test-seed',ds,s) for s in range(5) for ds in DS],4)
        write(OUT/'TEST_RESULTS.json',summarize_tests());status('THIRD_DATASET_PREPARING')
        schedule([('third-prepare',)],1);status('THIRD_DATASET_VALIDATION_RUNNING')
        schedule([('third-seed',s) for s in range(3)],3)
        rows=[read(OUT/'third/citeseer'/f'seed_{s}/results.json') for s in range(3)];d=[r['arms']['H2_R_HSPE']['validation_metrics']['mrr']-r['arms']['B0_BASELINE']['validation_metrics']['mrr'] for r in rows];third={'dataset':'citeseer','validation_delta':{**stat(d),'wins':sum(x>0 for x in d)},'validation_seed_results':rows,'test_evaluated':False,'status':'THIRD_DATASET_NOT_SUPPORTED'}
        if np.mean(d)>0:
            status('THIRD_DATASET_FROZEN_TEST_PREPARING');full,view=m.p.v16.base.init_dataset('citeseer');pos,neg,h=m.p.v16.base.make_eval_candidates(full,'test');(OUT/'candidates').mkdir(exist_ok=True);np.savez(OUT/'candidates/citeseer_test.npz',positive=pos,negative=neg);write(OUT/'candidates/citeseer_test.json',{'negative_hash':h,'positive_hash':m.p.v16.v61.array_hash(pos),'seed':999,'grouping_seed':1000,'negatives_per_positive':20,'gate':'validation mean >0'})
            make_features('citeseer','test',view,np.vstack((pos,neg.reshape(-1,2))),np.empty((0,2),np.int64),24);schedule([('third-test-seed',s) for s in range(3)],3)
            tests=[read(OUT/'third/citeseer'/f'seed_{s}/test_results.json') for s in range(3)];third.update({'status':'THIRD_DATASET_VALIDATION_SUPPORTED','test_evaluated':True,'test_delta':paired(tests,'H2_R_HSPE','B0_BASELINE'),'test_seed_results':tests})
        write(OUT/'THIRD_DATASET.json',third)
        finalize()
    except Exception as e:status('FAILED',error=str(e),traceback=traceback.format_exc());raise

def main():
    torch.set_num_threads(int(os.environ.get('OMP_NUM_THREADS','4')));torch.set_num_interop_threads(1)
    ap=argparse.ArgumentParser();ap.add_argument('command',choices=['preflight','all','prepare-test','test-seed','third-prepare','third-seed','third-test-seed','finalize']);ap.add_argument('rest',nargs='*');a=ap.parse_args()
    if a.command=='preflight':print(json.dumps(preflight(),indent=2))
    elif a.command=='all':run_all()
    elif a.command=='prepare-test':prepare_test(a.rest[0],12)
    elif a.command=='test-seed':test_seed(a.rest[0],int(a.rest[1]))
    elif a.command=='third-prepare':third_prepare(24)
    elif a.command=='third-seed':third_seed(int(a.rest[0]))
    elif a.command=='third-test-seed':third_test_seed(int(a.rest[0]))
    else:finalize()
if __name__=='__main__':main()
