import importlib.util, json, os, pathlib, subprocess, sys, time

def json_safe(value):
    if hasattr(value, 'item'):
        return value.item()
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return value

script = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('hspe_v17_1', script)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
out = m.OUT
datasets, seeds = m.DATASETS, m.SEEDS
phase = out / 'diagnostics' / 'phase_rank_resume_status.json'
queue = []
for seed in seeds:
    for ds in datasets:
        result = out / 'experiments' / 'phase_rank' / ds / f'seed_{seed}' / 'results.json'
        try:
            item = json.loads(result.read_text())
            if item.get('state') == 'COMPLETE' and 'H2_R_HSPE' in item.get('arms', {}):
                continue
        except Exception:
            pass
        queue.append((ds, seed))
active, completed, failed = {}, [], []
logs = out / 'logs'; logs.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
limit = 4
while queue or active:
    while queue and len(active) < limit and not failed:
        ds, seed = queue.pop(0)
        f = (logs / f'phase_rank_resume_{ds}_seed{seed}.log').open('ab', buffering=0)
        p = subprocess.Popen([sys.executable, '-u', str(script), 'run-one', ds, str(seed), 'phase_rank'], stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        active[p.pid] = (p, ds, seed, f)
    for pid, (p, ds, seed, f) in list(active.items()):
        code = p.poll()
        if code is not None:
            f.close(); (completed if code == 0 else failed).append({'dataset': ds, 'seed': seed, 'pid': pid, 'exit_code': code}); del active[pid]
    m.write_json(phase, {'state': 'FAILED' if failed else 'RUNNING' if queue or active else 'FINALIZING', 'completed_jobs': completed, 'failed_jobs': failed, 'active_jobs': [{'pid': pid, 'dataset': ds, 'seed': seed} for pid, (_, ds, seed, _) in active.items()], 'pending_jobs': queue, 'updated_at': time.time(), 'test_evaluated': False})
    if failed and not active:
        raise SystemExit('rank recovery jobs failed: ' + repr(failed))
    if active: time.sleep(5)

a = m.summarize_a()
rank = m.summarize_rank(a)
rank = json_safe(rank)
data = m.read_json(out / 'results.json')
data.update({'state': 'RANK_SCREEN_COMPLETE', 'phase_a': a, 'rank_screen': rank, 'primary_efficacy': 'HSPE_EFFICACY_CONFIRMED', 'final_variant': rank['final_variant'], 'error': None, 'traceback': None})
final = {ds: rank['datasets'][ds]['H2_minus_B0'] if rank['promoted'] else a['datasets'][ds]['effects']['TotalGain'] for ds in datasets}
data['final_validation'] = {ds: {'delta': d, 'passed': bool(m.efficacy(d))} for ds, d in final.items()}
data['mechanism'] = m.mechanism_summary(a)
data['state'] = 'HSPE_VALIDATION_CONFIRMED' if all(x['passed'] for x in data['final_validation'].values()) else 'HSPE_EFFICACY_CONFIRMED'
data['final_decision'] = data['state']
data['variant_decision'] = 'R_HSPE_SELECTED' if rank['promoted'] else 'ORIGINAL_HSPE_SELECTED'
data['next_expected_step'] = 'User reviews frozen method version and mechanism claims; test OFF.'
data = json_safe(data)
m.save(data)
(out / '06_NOVELTY_SCOPE.md').write_text(json.dumps({'claim_scope': 'candidate-specific hyperedge-pair context representation preserving the local incident hyperedge cardinality distribution for link decoding', 'distinction': 'pair-specific local hyperedge-size sets versus global order weighting', 'mechanism': data['mechanism'], 'no_first_size_claim': True, 'novelty_priority_not_independently_established': True, 'test_evaluated': False}, indent=2), encoding='utf-8')
m.write_json(phase, {'state': 'COMPLETE', 'completed_jobs': completed, 'failed_jobs': [], 'active_jobs': [], 'pending_jobs': [], 'updated_at': time.time(), 'test_evaluated': False})
print(json.dumps({'state': data['state'], 'final_variant': rank['final_variant'], 'promoted': rank['promoted'], 'final_validation': data['final_validation']}, indent=2))
