"""Run all duplicate pairs; stop scheduling new pairs at first determinism failure."""
import concurrent.futures, hashlib, json, os, pathlib, subprocess, sys, threading, time

REPO=pathlib.Path('/home/ubuntu/lchr_v2'); RESEARCH=REPO/'HYPERGRAPH_RESEARCH'
AUDIT=RESEARCH/'CHRI_V18_1C'; RUNNER=AUDIT/'scripts/canonical_run.py'
CANONICAL_TO_V18={'A0':'A1','A1':'A2','A2':'A3','A3':'A4'}
DATASETS=('cora','pubmed'); SEEDS=(0,1,2); ARMS=('A0','A1','A2','A3')
MAX_WORKERS=6
status_path=AUDIT/'RUN_STATUS.json'; lock=threading.Lock()

def write_status(obj):
    tmp=status_path.with_suffix('.json.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n');tmp.replace(status_path)

def hash_file(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def prepare_output(out):
    out.parent.mkdir(parents=True,exist_ok=True)
    # Historical code resolves frozen-source paths through OUT/../CHRI_V18.
    base=out.parent; oldlink=base/'CHRI_V18'
    if not oldlink.exists():oldlink.symlink_to(RESEARCH/'CHRI_V18',target_is_directory=True)
    links=[('cache',RESEARCH/'CHRI_V18_1/cache',True),
           ('scripts',RESEARCH/'CHRI_V18_1/scripts',True),
           ('SOURCE_HASHES.json',RESEARCH/'CHRI_V18_1/SOURCE_HASHES.json',False)]
    out.mkdir(parents=True,exist_ok=True)
    for name,target,is_dir in links:
        dest=out/name
        if not dest.exists():dest.symlink_to(target,target_is_directory=is_dir)

def run_one(ds,seed,arm,rep):
    parent=AUDIT/'runs'/ds/f'seed_{seed}'/arm;out=parent/f'rep_{rep}'
    prepare_output(out)
    env=os.environ.copy();env.update({'CHRI_CANONICAL_OUT':str(out),
        'OMP_NUM_THREADS':'2','MKL_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'2',
        'CUBLAS_WORKSPACE_CONFIG':':4096:8','DGLBACKEND':'pytorch'})
    logdir=AUDIT/'logs';logdir.mkdir(exist_ok=True)
    log=logdir/f'{ds}_seed{seed}_{arm}_rep{rep}.log'
    with log.open('w') as f:
        p=subprocess.run([sys.executable,str(RUNNER),ds,str(seed),arm,str(out)],
                         cwd=REPO,env=env,stdout=f,stderr=subprocess.STDOUT)
    if p.returncode:raise RuntimeError({'dataset':ds,'seed':seed,'arm':arm,'rep':rep,'returncode':p.returncode,'log':str(log)})
    job=out/'runs/A'/ds/f'seed_{seed}'/CANONICAL_TO_V18[arm]
    rec=json.loads((job/'result.json').read_text())
    return {'replicate':rep,'checkpoint_sha256':rec['checkpoint_sha256'],
            'score_vector_sha256':rec['score_vector_sha256'],'validation':rec['validation'],
            'result_path':str(job/'result.json'),'checkpoint_path':str(job/'final.pt'),
            'score_path':str(job/'valid_epoch5_scores.npz'),'wall_seconds':rec['wall_seconds']}

def run_pair(key):
    ds,seed,arm=key
    a=run_one(ds,seed,arm,1);b=run_one(ds,seed,arm,2)
    return {'dataset':ds,'seed':seed,'canonical_arm':arm,'implementation_arm':CANONICAL_TO_V18[arm],
            'replicates':[a,b], 'checkpoint_hash_equal':a['checkpoint_sha256']==b['checkpoint_sha256'],
            'score_vector_hash_equal':a['score_vector_sha256']==b['score_vector_sha256'],
            'validation_metrics_equal':a['validation']==b['validation'],
            'pair_pass':a['checkpoint_sha256']==b['checkpoint_sha256'] and a['score_vector_sha256']==b['score_vector_sha256'],
            'test_accessed':False}

pairs=[(ds,seed,arm) for ds in DATASETS for seed in SEEDS for arm in ARMS]
status={'state':'RUNNING','workspace':'DCDLP-main','protocol':'CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1',
        'total_pairs':len(pairs),'total_independent_runs':2*len(pairs),'max_workers':MAX_WORKERS,
        'completed_pairs':[],'active_pairs':[],'queued_pairs':len(pairs),'test_accessed':False,
        'started_at':time.time()};write_status(status)
failed=False
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    queue=iter(pairs);active={}
    for _ in range(min(MAX_WORKERS,len(pairs))):
        key=next(queue);active[pool.submit(run_pair,key)]=key
    while active:
        done,_=concurrent.futures.wait(active,timeout=2,return_when=concurrent.futures.FIRST_COMPLETED)
        for fut in done:
            key=active.pop(fut)
            try: result=fut.result()
            except Exception as e:
                status.update(state='FAILED',error=str(e),failed_pair=key,ended_at=time.time());failed=True
            else:
                status['completed_pairs'].append(result)
                if not result['pair_pass']:
                    status.update(state='DETERMINISTIC_PROTOCOL_FAILURE',failed_pair=key,ended_at=time.time());failed=True
            if failed:
                for pending in active:pending.cancel()
                break
            try:
                nxt=next(queue);active[pool.submit(run_pair,nxt)]=nxt
            except StopIteration:pass
        status['active_pairs']=[list(k) for k in active.values()]
        status['queued_pairs']=max(0,len(pairs)-len(status['completed_pairs'])-len(status['active_pairs']))
        write_status(status)
        if failed:break
if not failed:
    status.update(state='COMPLETE',ended_at=time.time(),active_pairs=[],queued_pairs=0)
write_status(status)
print(json.dumps({'state':status['state'],'completed_pairs':len(status['completed_pairs']),
                  'total_pairs':len(pairs),'test_accessed':False},indent=2),flush=True)
if failed:sys.exit(2)
