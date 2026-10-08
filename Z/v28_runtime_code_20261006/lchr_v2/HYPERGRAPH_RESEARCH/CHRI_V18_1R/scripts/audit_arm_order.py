import json, os, pathlib, subprocess, sys, time

repo = pathlib.Path('/home/ubuntu/lchr_v2')
research = repo / 'HYPERGRAPH_RESEARCH'
audit = research / 'CHRI_V18_1R'
runner = audit / 'scripts/corrected_run.py'
sequences = [('R0_R1_R2', ['A1', 'A2', 'A3']),
             ('R2_R1_R0', ['A3', 'A2', 'A1']),
             ('R1_alone', ['A2'])]
order_base = audit / 'arm_order_runs'; order_base.mkdir(exist_ok=True)
old_link = order_base / 'CHRI_V18'
if not old_link.exists(): old_link.symlink_to(research / 'CHRI_V18', target_is_directory=True)
env = os.environ.copy()
env.update({'OMP_NUM_THREADS':'4', 'MKL_NUM_THREADS':'4',
            'OPENBLAS_NUM_THREADS':'4', 'CUBLAS_WORKSPACE_CONFIG':':4096:8'})
status = {'state':'RUNNING', 'sequences':{}, 'test_accessed':False,
          'started_at':time.time()}
(audit/'ARM_ORDER_STATUS.json').write_text(json.dumps(status, indent=2)+'\n')
for name, arms in sequences:
    out = audit / 'arm_order_runs' / name
    logs = audit / 'arm_order_logs'; logs.mkdir(exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    for link, target in [('cache', research / 'CHRI_V18_1/cache'),
                         ('scripts', research / 'CHRI_V18_1/scripts'),
                         ('SOURCE_HASHES.json', research / 'CHRI_V18_1/SOURCE_HASHES.json')]:
        dest = out / link
        if not dest.exists(): dest.symlink_to(target, target_is_directory=link != 'SOURCE_HASHES.json')
    status['sequences'][name] = {'state':'RUNNING','arms':arms}
    (audit/'ARM_ORDER_STATUS.json').write_text(json.dumps(status, indent=2)+'\n')
    for arm in arms:
        runenv = env.copy(); runenv['CHRI_CORRECTED_OUT'] = str(out)
        log = (logs / f'{name}_{arm}.log').open('w')
        p = subprocess.run([sys.executable, str(runner), 'pubmed', '0', arm],
                           cwd=repo, env=runenv, stdout=log,
                           stderr=subprocess.STDOUT)
        log.close()
        if p.returncode:
            status['state']='FAILED'; status['error']={'sequence':name,'arm':arm,'returncode':p.returncode}
            (audit/'ARM_ORDER_STATUS.json').write_text(json.dumps(status, indent=2)+'\n')
            raise RuntimeError(status['error'])
        status['sequences'][name]['completed_arms'] = arms[:arms.index(arm)+1]
        (audit/'ARM_ORDER_STATUS.json').write_text(json.dumps(status, indent=2)+'\n')
    status['sequences'][name]['state']='COMPLETE'
    (audit/'ARM_ORDER_STATUS.json').write_text(json.dumps(status, indent=2)+'\n')
status.update(state='COMPLETE', ended_at=time.time())
(audit/'ARM_ORDER_STATUS.json').write_text(json.dumps(status, indent=2)+'\n')
print('ARM_ORDER_COMPLETE', flush=True)
