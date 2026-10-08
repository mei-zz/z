"""V18.1S detached, validation-only canonical stability experiment."""
import os
for k in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'): os.environ.setdefault(k,'2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1')
os.environ.setdefault('DGLBACKEND','pytorch')
import sys, json, hashlib, time, shutil, subprocess, concurrent.futures, traceback
from pathlib import Path
import numpy as np
import torch

ROOT=Path(__file__).resolve().parents[2]
REPO=ROOT.parent
OUT=ROOT/'CHRI_V18_1S'
ART=REPO/'result/innovation2/CHRI_V18_1S'
PROTO='CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1'
AGG_SHA='831570b9a4b9ebbb1d52096d832d99033d17c2853dfe812d4738d9e7a5e6adc1'
sys.path.insert(0,str(ROOT/'CHRI_V18_1/scripts'))
import stability181 as st
v=st.v
sys.path.insert(0,str(ROOT/'CHRI_V18_1R/scripts'))
from deterministic_aggregation import install
torch.set_num_threads(2)
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.deterministic=True
torch.backends.cudnn.benchmark=False
torch.backends.cuda.matmul.allow_tf32=False
torch.backends.cudnn.allow_tf32=False
torch.set_float32_matmul_precision('highest')
ORIGINAL_MAKE=v.make_net
MAP={'V0':'A1','VRAW':'A2'}

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def read(p): return json.loads(Path(p).read_text())
def write(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    tmp=p.with_name(p.name+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');tmp.replace(p)
def artifact(name,obj): write(ART/name,obj)
def md(name,text):
    ART.mkdir(parents=True,exist_ok=True);(ART/name).write_text(text+'\n')

def check():
    manifest=read(ART/'SOURCE_HASHES.json')
    for path,h in manifest['files'].items(): assert sha(REPO/path)==h, 'SOURCE_CHANGED '+path
    v.check_frozen()

def deterministic_make(*args,**kwargs):
    net=install(ORIGINAL_MAKE(*args,**kwargs))
    # The original stable heads use the actual canonical decoder, not the unused z_decoder.
    return net
v.make_net=deterministic_make

def score_hash(p):
    h=hashlib.sha256()
    with np.load(p) as z:
        for key in ('positive','negative'):
            a=np.ascontiguousarray(z[key]);h.update(key.encode());h.update(str(a.shape).encode());h.update(str(a.dtype).encode());h.update(a.tobytes())
    return h.hexdigest()

def sandbox(phase,ds,seed,arm,rep):
    out=OUT/'executions'/phase/ds/f'seed_{seed}'/arm/f'rep_{rep}'
    out.mkdir(parents=True,exist_ok=True)
    links=[(out.parent/'CHRI_V18',ROOT/'CHRI_V18',True),
           (out/'scripts',ROOT/'CHRI_V18_1/scripts',True),
           (out/'SOURCE_HASHES.json',ROOT/'CHRI_V18_1/SOURCE_HASHES.json',False),
           (out/'cache',OUT/'cache_B' if phase=='B' else ROOT/'CHRI_V18_1/cache',True)]
    for p,target,d in links:
        if not p.exists(): p.symlink_to(target,target_is_directory=d)
    return out

def job(phase,ds,seed,arm,rep=1):
    return OUT/'executions'/phase/ds/f'seed_{seed}'/arm/f'rep_{rep}'/'runs'/phase/ds/f'seed_{seed}'/MAP.get(arm,arm)

def run(phase,ds,seed,arm,epochs,rep):
    assert ds in ('cora','pubmed')
    assert arm in ('V0','VRAW','V1','V2','V3','V1_NULL','V1_SHUFFLE','V2_NULL','V2_SHUFFLE','V3_NULL','V3_SHUFFLE')
    assert epochs in (5,10)
    v.OUT=sandbox(phase,ds,seed,arm,rep);check()
    actual=MAP.get(arm,arm)
    net=v.make_net(ds,seed,actual,phase)
    # Assert zero-init additive heads exactly equal the canonical q0 at initialization.
    initial_decoder=v.hash_state(net.decoder)
    if arm.startswith(('V2','V3')):
        assert torch.count_nonzero(net.correction[-1].weight)==0
        assert torch.count_nonzero(net.correction[-1].bias)==0
        zero=torch.zeros((3,32),device='cuda')
        assert torch.count_nonzero(net.correction(zero))==0
    del net
    original_step=torch.optim.Adam.step
    first_step=[True]
    def logged_step(optimizer,*args,**kwargs):
        answer=original_step(optimizer,*args,**kwargs)
        if first_step[0]:
            first_step[0]=False
            print('FIRST_OPTIMIZER_STEP_OK',phase,ds,seed,arm,rep,flush=True)
        return answer
    torch.optim.Adam.step=logged_step
    print('TRAINING_START',phase,ds,seed,arm,rep,flush=True)
    v.run(phase,ds,seed,actual,epochs)
    dest=v.job(phase,ds,seed,actual);row=read(dest/'result.json')
    row.update(variant=arm,replicate=rep,canonical_protocol=PROTO,
        score_vector_sha256=score_hash(dest/f'valid_epoch{epochs}_scores.npz'),
        actual_decoder_initial_sha256=initial_decoder,zero_init_asserted=arm.startswith(('V2','V3')),
        nuisance_labels_used=False,nuisance_encoder_gradients=False,conditional_null_regularization=False)
    write(dest/'result.json',row)
    # Diagnostics are descriptive heldout evaluations; they never fit nuisance on validation labels.
    if arm in ('VRAW','V1','V2','V3'):
        net=v.load_net(phase,ds,seed,actual)
        parts=st.validation_components(net,ds,seed)
        q=len(v.sealed_input(ds)['valid_pos']);labels=np.r_[np.ones(q),np.zeros(len(parts['score'])-q)]
        stats=st.behavior_statistics(parts,labels,parts['base'])
        stats['residual_norm_mean']=float(np.linalg.norm(parts['residual'],axis=1).mean()) if 'residual' in parts else None
        stats['gate_quantiles']=np.quantile(parts['gate'],[0,.25,.5,.75,1]).tolist()
        stats['reference_note']='same-model zero-relation-slot base; separately fitted Z contrasts are in phase results'
        write(dest/'diagnostics.json',stats)
    print('V18_1S_JOB_COMPLETE',phase,ds,seed,arm,rep,flush=True)

def prepare(ds,seed):
    assert ds in ('cora','pubmed') and seed in range(5)
    out=OUT/'preparation'/ds/f'seed_{seed}';out.mkdir(parents=True,exist_ok=True)
    for p,target,d in [(out.parent/'CHRI_V18',ROOT/'CHRI_V18',True),
            (out/'scripts',ROOT/'CHRI_V18_1/scripts',True),
            (out/'SOURCE_HASHES.json',ROOT/'CHRI_V18_1/SOURCE_HASHES.json',False),
            (out/'cache',OUT/'cache_B',True)]:
        if not p.exists():p.symlink_to(target,target_is_directory=d)
    v.OUT=out;check()
    target=OUT/'cache_B'/ds/f'seed_{seed}';target.mkdir(parents=True,exist_ok=True)
    original=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}'
    before={}
    if seed<3:
        for p in original.iterdir():
            if p.is_file():
                dst=target/p.name
                if not dst.exists():shutil.copy2(p,dst)
                before[p.name]=sha(p)
                assert sha(dst)==before[p.name], 'CACHE_CLONE_CHANGED'
    # Cache transport of the frozen NCNC retains its original numerical path.
    # Strict canonical reductions apply to all CHRI training and Z matching.
    # Cached tensors are generated once and paired across every Phase-B arm.
    torch.use_deterministic_algorithms(False)
    v.prepare_backbone(ds,seed,10)
    torch.use_deterministic_algorithms(True)
    v.prepare_matching(ds,seed,10)
    if seed<3:
        for name,h in before.items():
            if name in ('negative_schedule.npy','progress.json','normalization.json'):continue
            assert sha(target/name)==h, 'CANONICAL_PREFIX_CHANGED '+name
        oldneg=np.load(original/'negative_schedule.npy');newneg=np.load(target/'negative_schedule.npy')
        assert np.array_equal(oldneg,newneg[:5]), 'NEGATIVE_PREFIX_CHANGED'
        assert read(original/'B_READY_5.json')['trace']==read(target/'B_READY_10.json')['trace'][:5]
        assert sha(original/'normalization.json')==sha(target/'normalization.json')
    write(target/'V18_1S_READY.json',{'state':'PASS','seed':seed,'dataset':ds,
        'canonical_first5_preserved':seed<3,'all_files':{p.name:sha(p) for p in target.iterdir() if p.is_file()},'test_accessed':False})

CHILDREN=[]
def batch(tasks,stage,workers=6):
    active=[];queue=list(tasks);completed=0
    logdir=OUT/'logs';logdir.mkdir(exist_ok=True)
    while active or queue:
        for item in list(active):
            p,args,log=item
            if p.poll() is not None:
                active.remove(item)
                if p.returncode:raise RuntimeError(f'JOB_FAILED {args}: {log}')
                completed+=1
        while queue and len(active)<workers:
            args=queue.pop(0);log=logdir/('_'.join(map(str,args))+'.log')
            with log.open('a') as f:
                p=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*map(str,args)],
                    stdout=f,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL,env=os.environ.copy(),start_new_session=True)
            active.append((p,args,log));CHILDREN.append(p)
        status={'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'queued':len(queue),
            'completed_stage_jobs':completed,'active':[{'pid':p.pid,'arguments':a,'log':str(l)} for p,a,l in active],
            'updated_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',status)
        if active:time.sleep(3)

def preflight():
    assert REPO.name in ('DCDLP-main','lchr_v2') and (ROOT/'CHRI_V18/scripts/chri_v18.py').exists()
    ART.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    assert sha(ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py')==AGG_SHA
    histories={}
    for folder,word in [('CHRI_V18','CHRI_KILL'),('CHRI_V18_1','V18_1_REPRODUCTION_MISMATCH'),
            ('CHRI_V18_1R','HISTORICAL_ROOT_CAUSE_IDENTIFIED'),('CHRI_V18_1C','CANONICAL_SIGNAL_PRESENT')]:
        base=REPO/'result/innovation2'/folder
        # V18.1R's server evidence lives at its research root; the result copy is local only.
        if not base.exists():base=ROOT/folder
        texts='\n'.join(p.read_text(errors='replace') for p in base.glob('*.md'))
        assert word in texts, 'HISTORY_MISMATCH '+folder
        histories[folder]={str(p.relative_to(REPO)):sha(p) for p in base.glob('*') if p.is_file() and p.suffix in ('.md','.json')}
    v.check_frozen()
    canonical=read(ROOT/'CHRI_V18_1C/01_CANONICAL_IMPLEMENTATION.json')
    # V18.1C records source/cache hashes and duplicate evidence, all checked below.
    dup=read(REPO/'result/innovation2/CHRI_V18_1C/02_DUPLICATE_REPRODUCIBILITY.json')
    assert dup['state']=='PASS' and all(d['pair_pass'] for d in dup['duplicates'])
    files={str(p.relative_to(REPO)):sha(p) for p in (OUT/'scripts').glob('*.py')}
    for path in [ROOT/'CHRI_V18/scripts/chri_v18.py',ROOT/'CHRI_V18/scripts/chri_features.py',
            ROOT/'CHRI_V18_1/scripts/stability181.py',ROOT/'CHRI_V18_1R/scripts/deterministic_aggregation.py']:
        files[str(path.relative_to(REPO))]=sha(path)
    for hist in histories.values():files.update(hist)
    caches={}
    for ds in ('cora','pubmed'):
        for seed in range(3):
            source=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}'
            expected=canonical['feature_caches'][ds][str(seed)]['cache_file_sha256']
            actual={str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file()}
            assert actual==expected, 'CANONICAL_CACHE_CHANGED'
            caches[f'{ds}/{seed}']=actual
        cb=OUT/'cache_B'/ds;cb.mkdir(parents=True,exist_ok=True)
        for p in (ROOT/'CHRI_V18_1/cache'/ds).glob('*'):
            if p.is_file() and not (cb/p.name).exists():shutil.copy2(p,cb/p.name)
    artifact('SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','files':files,'canonical_cache_hashes':caches,
        'canonical_protocol':PROTO,'deterministic_aggregation_sha256':AGG_SHA,'innovation1_modified':False})
    artifact('RUN_MANIFEST.json',{'state':'REGISTERED','canonical_protocol':PROTO,'created_at':time.time(),
        'precheck':{'dataset':'pubmed','seed':0,'variants':['V1','V2','V3'],'replicates':2,'epochs':5,'gate':'exact checkpoint and score-vector hashes'},
        'phase_A':{'datasets':['cora','pubmed'],'seeds':[0,1,2],'epochs':5,'arms':['V0','VRAW','V1','V2','V3','V3_NULL','V3_SHUFFLE']},
        'phase_B':{'conditional_on_phase_A_pass':True,'datasets':['cora','pubmed'],'seeds':list(range(5)),'epochs':10},
        'heads':{'nuisance':[321,32,32],'correction':[32,32,1],'gate':[353,1],'gate_initial_bias':-2,'gate_initial_weight':0},
        'nuisance_loss_weight':1,'prediction_loss':'canonical balanced positive/negative BCE sum','nuisance_input':'Z.detach()','nuisance_target':'R.detach()',
        'encoder_policy':'canonical architecture, feature definitions, initialization and end-to-end supervised training unchanged; nuisance does not update encoders',
        'base_head':'canonical decoder 353->64->32->1, relation slots zero for q0',
        'NULL':'canonical learned constant via relation MLP at zero 48d input; architecture and parameter count matched',
        'SHUFFLE':'unchanged cached kNN32 train-only matched donors; original donor_choices',
        'controls_for_V1_V2':'run only if preliminary per-dataset RAW/Z/MRR gates pass, before final selection',
        'phase_B_backbone_cache':'original frozen NCNC inference path, generated once; fixed caches across all paired arms; canonical first five epochs preserved',
        'optimizer':'canonical Adam, weight_decay=0','learning_rate':{ds:v.b.NCFG[ds]['prelr'] for ds in ('cora','pubmed')},
        'batch_size':{ds:v.b.NCFG[ds]['batch'] for ds in ('cora','pubmed')},'training_microbatch':256,
        'parallel_training_jobs':6,'cpu_threads_per_job':2,'test_opened':False,'citeseer_run':False,'innovation1_modified':False,'CRIB':False})
    for name in ['01_DETERMINISM_PRECHECK.json','02_NUISANCE_DIAGNOSTICS.json','03_PHASE_A_RESULTS.json','05_SELECTED_VARIANT.json','07_PHASE_B_RESULTS.json']:
        if not (ART/name).exists():artifact(name,{'state':'NOT_RUN','reason':'Prerequisite pending.'})
    for name in ['04_VARIANT_COMPARISON.md','06_RANKING_SPECIFICITY.md','08_CORRECTION_ANALYSIS.md','FINAL_REPORT.md']:
        if not (ART/name).exists():md(name,'# V18.1S\n\nPENDING: detached execution registered; no efficacy conclusion yet.')
    print('V18_1S_PREFLIGHT_PASS',flush=True)

def results(phase,seeds,arms):
    data={'state':'COMPLETE','phase':phase,'seeds':list(seeds),'datasets':{},'test_accessed':False}
    for ds in ('cora','pubmed'):
        rows=[{'seed':s,'arms':{a:read(job(phase,ds,s,a)/'result.json') for a in arms}} for s in seeds]
        for row in rows:
            ref=row['arms']['V0']
            for a,r in row['arms'].items():
                assert ref['training_trace']==r['training_trace'], 'PAIRED_TRACE_MISMATCH'
                assert ref['actual_decoder_initial_sha256']==r['actual_decoder_initial_sha256'], 'BASE_INIT_MISMATCH'
                assert ref['initialization']['encoder']==r['initialization']['encoder'], 'ENCODER_INIT_MISMATCH'
        effects={}
        for a in arms:
            if a in ('V0','VRAW') or '_' in a:continue
            for comp in ('V0','VRAW',a+'_NULL',a+'_SHUFFLE'):
                if comp in arms:effects[a+'_vs_'+comp]=v.comparison(rows,a,comp)
        data['datasets'][ds]={'seed_results':rows,'effects':effects,
            'RAW_vs_Z':v.comparison(rows,'VRAW','V0'),
            'metrics':{a:{m:v.stat([r['arms'][a]['validation'][m] for r in rows]) for m in v.METRICS} for a in arms}}
    return data

def preliminary(data,a):
    for ds,item in data['datasets'].items():
        z=item['effects'][a+'_vs_V0'];raw=item['effects'][a+'_vs_VRAW']
        if not (raw['ce']['mean']>=0 if ds=='cora' else raw['ce']['mean']>0):return False
        if not (z['ce']['wins']>=2 and z['ce']['mean']>0 and z['mrr']['mean']>=0):return False
    return True

def eligible(data,a):
    if not preliminary(data,a):return False
    return all(item['effects'].get(a+'_vs_'+a+c,{}).get('ce',{}).get('mean',-np.inf)>0
        for item in data['datasets'].values() for c in ('_NULL','_SHUFFLE'))

def select(data):
    eligible_arms=[a for a in ('V1','V2','V3') if eligible(data,a)]
    def key(a):
        effects=[i['effects'][a+'_vs_VRAW'] for i in data['datasets'].values()]
        n=data['datasets']['cora']['seed_results'][0]['arms'][a]['trainable_parameters']
        return (min(e['ce']['mean'] for e in effects),sum(e['ce']['wins'] for e in effects),
            np.mean([e['ce']['mean'] for e in effects]),np.mean([e['mrr']['mean'] for e in effects]),-n,-int(a[1]))
    chosen=max(eligible_arms,key=key) if eligible_arms else None
    artifact('05_SELECTED_VARIANT.json',{'state':'SELECTED' if chosen else 'NONE','variant':chosen,
        'working_name':'CHRI-STABLE-v1' if chosen else None,'passing_variants':eligible_arms,
        'selection_keys':{a:list(key(a)) for a in eligible_arms},'architecture_frozen':bool(chosen),
        'selection_order':['min dataset CE vs RAW','total CE wins vs RAW','mean CE vs RAW','mean MRR vs RAW','fewer params','registry order'],
        'test_opened':False})
    return chosen

def describe(data):
    lines=['# Paired variant comparison','','Positive DeltaCE = CE(comparator)-CE(method); positive DeltaMRR = MRR(method)-MRR(comparator).','',
        '| Dataset | Contrast | Mean DeltaCE | Median DeltaCE | CE wins | Mean DeltaMRR |','|---|---|---:|---:|---:|---:|']
    for ds,item in data['datasets'].items():
        for name,e in item['effects'].items():lines.append(f"| {ds} | {name} | {e['ce']['mean']:.10g} | {e['ce']['median']:.10g} | {e['ce']['wins']}/{len(e['ce']['per_seed'])} | {e['mrr']['mean']:.10g} |")
    md('04_VARIANT_COMPARISON.md','\n'.join(lines))

def diagnostics(phase,seeds,arms):
    rows={ds:{a:[read(job(phase,ds,s,a)/'diagnostics.json') for s in seeds] for a in arms} for ds in ('cora','pubmed')}
    artifact('02_NUISANCE_DIAGNOSTICS.json',{'state':'COMPLETE','phase':phase,
        'datasets':{ds:{a:[r.get('nuisance') for r in rr] for a,rr in item.items() if a!='VRAW'} for ds,item in rows.items()},
        'fit':'online train candidates only; detached Z and detached relation target; labels excluded',
        'measurement':'heldout validation representations; descriptive, no selection of nuisance hyperparameters'})
    artifact('CORRECTION_DIAGNOSTICS.json',{'state':'COMPLETE','phase':phase,'datasets':rows,'causal_claim':False})
    lines=['# Correction and residual diagnostics','','Associations only. RAW/V1 correction is a same-model zero-relation-slot counterfactual; V2/V3 is an explicit additive correction. Nuisance is fitted only on train representations.','',
        '| Dataset | Variant | Seed | R norm | Residual norm | Correction RMS | Harmful | Beneficial | Gate mean | Nuisance R2 |',
        '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for ds,item in rows.items():
        for a,rr in item.items():
            for s,r in zip(seeds,rr):lines.append(f"| {ds} | {a} | {s} | {r['relation_norm_mean']} | {r.get('residual_norm_mean')} | {r['correction_rms']} | {r['harmful_correction_fraction']} | {r['beneficial_correction_fraction']} | {r['gate_mean']} | {r.get('nuisance',{}).get('R2')} |")
    md('08_CORRECTION_ANALYSIS.md','\n'.join(lines))

def ranking(data):
    records={}
    # Same-epoch canonical RAW shuffle baseline for Phase A; Phase B has selected controls only.
    for a in ('V1','V2','V3'):
        item=data['datasets']['cora']['effects'].get(a+'_vs_'+a+'_SHUFFLE')
        if item:
            new=item['mrr']['mean']
            rows=[]
            for s in range(3):
                arms={}
                for name,canonical,actual in [('RAW','A1','A2'),('SHUFFLE','A2','A3')]:
                    path=ROOT/'CHRI_V18_1C/runs/cora'/f'seed_{s}'/canonical/'rep_1/runs/A/cora'/f'seed_{s}'/actual/'result.json'
                    arms[name]=read(path)
                rows.append({'seed':s,'arms':arms})
            raw=v.comparison(rows,'RAW','SHUFFLE')['mrr']['mean']
            label='RANKING_SPECIFICITY_RECOVERED' if new>=0 else 'RANKING_TENSION_REDUCED' if new>raw else 'RANKING_TENSION_PERSISTS'
            records[a]={'RAW_vs_SHUFFLE_mean_DeltaMRR':raw,'new_vs_own_SHUFFLE_mean_DeltaMRR':new,'classification':label}
    md('06_RANKING_SPECIFICITY.md','# Cora Phase-A ranking specificity\n\n'+json.dumps(records,indent=2)+'\n\nDescriptive; CE promotion gate is unchanged.')

def final(status,reason,selected=None):
    # History/source/cache checks close the audited execution without rewriting prior artifacts.
    v.OUT=ROOT/'CHRI_V18_1';check()
    manifest=read(ART/'SOURCE_HASHES.json')
    for ds in ('cora','pubmed'):
        for seed in range(3):
            base=ROOT/'CHRI_V18_1/cache'/ds/f'seed_{seed}'
            assert {str(p.relative_to(base)):sha(p) for p in base.rglob('*') if p.is_file()}==manifest['canonical_cache_hashes'][f'{ds}/{seed}']
    a=read(ART/'03_PHASE_A_RESULTS.json');b=read(ART/'07_PHASE_B_RESULTS.json')
    answers={'determinism':read(ART/'01_DETERMINISM_PRECHECK.json'),'nuisance':read(ART/'02_NUISANCE_DIAGNOSTICS.json'),
        'selected':read(ART/'05_SELECTED_VARIANT.json'),'phase_A':a,'phase_B':b}
    lines=['# V18.1S final report','',f'FINAL_STATUS: {status}',f'REASON: {reason}',f'SELECTED_VARIANT: {selected or "NONE"}',
        '', '## Determinism and nuisance predictability','',json.dumps(answers['determinism'],indent=2),
        '', 'Nuisance MSE, R2, cosine and residual variance: 02_NUISANCE_DIAGNOSTICS.json. Negative R2 means the fitted nuisance is worse than the validation mean predictor; residualization is not assumed successful.',
        '', '## Residualization, zero-init and gating','',
        'V1 tests residualized concat; V2 tests a zero-init additive correction; V3 tests the same correction with a conservative learned gate. All canonical encoders and supervised training rules are retained; nuisance fits detached Z/r without labels. See paired CE/MRR, every seed and all five requested metrics below.',
        '',(ART/'04_VARIANT_COMPARISON.md').read_text(),
        '', '## Selection, relation specificity and Phase B','',json.dumps(answers['selected'],indent=2),
        '',json.dumps(b,indent=2),
        '',(ART/'06_RANKING_SPECIFICITY.md').read_text(),
        '', '## Correction analysis','', (ART/'08_CORRECTION_ANALYSIS.md').read_text(),
        '', '## Method contribution','',status+'. '+reason,
        '', 'TEST_OPENED: NO','INNOVATION_1_MODIFIED: NO','CITESEER_RUN: NO','CRIB_RUN: NO','INNOVATION_3_STARTED: NO',
        '', '## Full Phase A evidence','',json.dumps(a,indent=2)]
    md('FINAL_REPORT.md','\n'.join(lines))
    write(OUT/'RUN_STATUS.json',{'state':'COMPLETE','final_status':status,'reason':reason,'selected':selected,'ended_at':time.time(),'test_opened':False})
    artifact('RUN_STATUS.json',read(OUT/'RUN_STATUS.json'))
    md('C2C_HANDOFF.md',f'STATUS: EXECUTED\nTASK: CHRI_V18_1S_RESIDUALIZATION_STABILITY\nCANONICAL_PROTOCOL: {PROTO}\nFINAL_STATUS: {status}\nSELECTED_VARIANT: {selected or "NONE"}\nTEST_OPENED: NO\nINNOVATION_1_MODIFIED: NO\nPRIMARY_ARTIFACT: result/innovation2/CHRI_V18_1S/FINAL_REPORT.md')
    print('V18_1S_COMPLETE',status,flush=True)

def supervise():
    try:
        preflight()
        tasks=[('run','D','pubmed',0,a,5,r) for a in ('V1','V2','V3') for r in (1,2)]
        batch(tasks,'DETERMINISM_PRECHECK')
        pairs=[]
        for a in ('V1','V2','V3'):
            rr=[read(job('D','pubmed',0,a,r)/'result.json') for r in (1,2)]
            pairs.append({'variant':a,'checkpoint_hashes':[r['checkpoint_sha256'] for r in rr],
                'score_hashes':[r['score_vector_sha256'] for r in rr],
                'pass':rr[0]['checkpoint_sha256']==rr[1]['checkpoint_sha256'] and rr[0]['score_vector_sha256']==rr[1]['score_vector_sha256']})
        passed=all(p['pass'] for p in pairs)
        artifact('01_DETERMINISM_PRECHECK.json',{'state':'PASS' if passed else 'FAIL','pairs':pairs,'epochs':5,'test_accessed':False})
        if not passed:
            artifact('07_PHASE_B_RESULTS.json',{'state':'NOT_RUN','reason':'Determinism failure.'})
            final('DETERMINISTIC_PROTOCOL_FAILURE','Exact independent checkpoint/score hashes differ. No efficacy study launched.');return
        arms=['V0','VRAW','V1','V2','V3','V3_NULL','V3_SHUFFLE']
        # Reuse only the just-completed independent precheck replicate1, not historical results.
        for a in ('V1','V2','V3'):
            dest=job('A','pubmed',0,a);dest.parent.mkdir(parents=True,exist_ok=True)
            if not dest.exists():dest.symlink_to(job('D','pubmed',0,a),target_is_directory=True)
        tasks=[('run','A',ds,s,a,5,1) for s in range(3) for ds in ('cora','pubmed') for a in arms
               if not (ds=='pubmed' and s==0 and a in ('V1','V2','V3'))]
        batch(tasks,'PHASE_A_SCREEN')
        aresults=results('A',range(3),arms)
        extras=[a+c for a in ('V1','V2') if preliminary(aresults,a) for c in ('_NULL','_SHUFFLE')]
        if extras:
            batch([('run','A',ds,s,a,5,1) for s in range(3) for ds in ('cora','pubmed') for a in extras],'MATCHED_CONTROLS')
            arms+=extras;aresults=results('A',range(3),arms)
        for a in ('V1','V2','V3'):
            aresults.setdefault('variant_gates',{})[a]={'preliminary_pass':preliminary(aresults,a),'all_gates_pass':eligible(aresults,a)}
        artifact('03_PHASE_A_RESULTS.json',aresults);describe(aresults);ranking(aresults)
        diagnostics('A',range(3),['VRAW','V1','V2','V3'])
        selected=select(aresults)
        if not selected:
            artifact('07_PHASE_B_RESULTS.json',{'state':'NOT_RUN','reason':'No variant passed strict Phase-A RAW, Z, NULL, SHUFFLE and MRR gates.'})
            final('CHRI_PHENOMENON_CONFIRMED_METHOD_NOT_IMPROVED','No preregistered residualized variant improves canonical RAW and survives all controls.');return
        batch([('prepare',ds,s) for ds in ('cora','pubmed') for s in range(5)],'PHASE_B_CACHE_PREPARATION',workers=2)
        barms=['V0','VRAW',selected,selected+'_NULL',selected+'_SHUFFLE']
        batch([('run','B',ds,s,a,10,1) for s in range(5) for ds in ('cora','pubmed') for a in barms],'PHASE_B_VALIDATION')
        bresults=results('B',range(5),barms);allpass=True;calibration=[]
        rawgains=[]
        for ds,item in bresults['datasets'].items():
            e=item['effects'];z=e[selected+'_vs_V0'];raw=e[selected+'_vs_VRAW']
            gates={'Z_mean_CE':z['ce']['mean']>0,'Z_median_CE':z['ce']['median']>0,'Z_CE_wins':z['ce']['wins']>=3,
                'RAW_mean_CE':raw['ce']['mean']>=0,'shuffle_CE':e[selected+'_vs_'+selected+'_SHUFFLE']['ce']['mean']>0,
                'null_CE':e[selected+'_vs_'+selected+'_NULL']['ce']['mean']>0,'Z_mean_MRR':z['mrr']['mean']>=0}
            item['gates']=gates;item['pass']=all(gates.values());allpass=allpass and item['pass'];rawgains.append(raw['ce']['mean'])
            calibration.append(z['ce']['mean']>0 and z['mrr']['mean']<0)
        allpass=allpass and max(rawgains)>0;bresults['all_pass']=allpass
        artifact('07_PHASE_B_RESULTS.json',bresults);diagnostics('B',range(5),['VRAW',selected])
        status='CHRI_STABLE_METHOD_SUPPORTED' if allpass else 'CALIBRATION_ONLY_GAIN' if all(calibration) else 'CHRI_STABILITY_IMPROVED'
        final(status,'Selected fixed architecture completed five-seed validation; see per-dataset gates and controls.',selected)
    except BaseException as err:
        for p in CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,__import__('signal').SIGTERM)
                except ProcessLookupError:pass
        failure={'state':'EXECUTION_FAILED','error':repr(err),'traceback':traceback.format_exc(),'ended_at':time.time(),'test_opened':False}
        write(OUT/'RUN_STATUS.json',failure);artifact('ERROR.json',failure)
        print(traceback.format_exc(),flush=True);raise

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='supervise':supervise()
    elif cmd=='preflight':preflight()
    elif cmd=='prepare':prepare(sys.argv[2],int(sys.argv[3]))
    elif cmd=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]),int(sys.argv[7]))
    else:raise ValueError(cmd)
