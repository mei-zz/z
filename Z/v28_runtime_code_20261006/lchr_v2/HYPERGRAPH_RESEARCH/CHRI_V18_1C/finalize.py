"""Validate duplicates, compute preregistered paired contrasts, and write V18.1C artifacts."""
import hashlib,json,math,pathlib,statistics,sys

REPO=pathlib.Path('/home/ubuntu/lchr_v2');R=REPO/'HYPERGRAPH_RESEARCH';A=R/'CHRI_V18_1C';OUT=REPO/'result/innovation2/CHRI_V18_1C'
CANONICAL_ARMS=('A0','A1','A2','A3'); METRICS=('ce','mrr','hits10','hits20','auc')
MAPPING={'A0':'A1','A1':'A2','A2':'A3','A3':'A4'}
def read(p):return json.loads(pathlib.Path(p).read_text())
def write(n,x):(OUT/n).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def sha(p):
 h=hashlib.sha256()
 with pathlib.Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def stat(vals):
 vals=[float(x) for x in vals]
 return {'mean':statistics.mean(vals),'median':statistics.median(vals),'sample_std':statistics.stdev(vals) if len(vals)>1 else None,
         'wins':sum(x>0 for x in vals),'per_seed':vals}

status=read(A/'RUN_STATUS.json');pairs=status['completed_pairs']
assert status['state']=='COMPLETE' and len(pairs)==24 and all(p['pair_pass'] for p in pairs), 'DUPLICATE_GATE_FAILED'
canonical={};dup=[];exact=True
for p in pairs:
 ds,seed,arm=p['dataset'],p['seed'],p['canonical_arm']; reps=[]
 for rr in p['replicates']:
  rec=read(rr['result_path']); checkpoint_ok=sha(rr['checkpoint_path'])==rr['checkpoint_sha256']
  score_ok=rec['score_vector_sha256']==rr['score_vector_sha256']
  reps.append({'replicate':rr['replicate'],'checkpoint_sha256':rr['checkpoint_sha256'],'checkpoint_file_hash_verified':checkpoint_ok,
    'score_vector_sha256':rr['score_vector_sha256'],'score_vector_hash_verified':score_ok,'validation':rr['validation'],
    'result_path':rr['result_path'],'checkpoint_path':rr['checkpoint_path'],'score_path':rr['score_path'],'wall_seconds':rr['wall_seconds']})
  exact=exact and checkpoint_ok and score_ok
 pair_ok=p['checkpoint_hash_equal'] and p['score_vector_hash_equal'] and p['validation_metrics_equal'] and all(x['checkpoint_file_hash_verified'] and x['score_vector_hash_verified'] for x in reps)
 exact=exact and pair_ok
 dup.append({'dataset':ds,'seed':seed,'canonical_arm':arm,'implementation_arm':MAPPING[arm],'replicates':reps,
   'checkpoint_hash_equal':p['checkpoint_hash_equal'],'score_vector_hash_equal':p['score_vector_hash_equal'],
   'validation_metrics_equal':p['validation_metrics_equal'],'pair_pass':pair_ok,'test_accessed':False})
 canonical.setdefault(ds,{}).setdefault(seed,{})[arm]=read(p['replicates'][0]['result_path'])

trace_checks=[]
for ds,seeds in canonical.items():
 for seed,arms in seeds.items():
  traces={a:json.dumps(r['training_trace'],sort_keys=True) for a,r in arms.items()}
  inits={a:r['initialization'] for a,r in arms.items()}
  trace_checks.append({'dataset':ds,'seed':seed,'training_trace_identical_across_arms':len(set(traces.values()))==1,
    'encoder_initialization_identical':len({x['encoder'] for x in inits.values()})==1,
    'relation_initialization_identical':len({x['relation'] for x in inits.values()})==1,
    'decoder_initialization_identical':len({x['decoder'] for x in inits.values()})==1})
paired_inputs_ok=all(all(v for k,v in q.items() if k not in ('dataset','seed')) for q in trace_checks)
identity=read(A/'01_CANONICAL_IMPLEMENTATION.json')
report_generator='HYPERGRAPH_RESEARCH/CHRI_V18_1C/scripts/finalize.py'
source_unchanged={name:sha(REPO/name)==digest for name,digest in identity['source_sha256'].items() if name!=report_generator}
report_generator_hash={'pre_run_sha256':identity['source_sha256'].get(report_generator),
 'post_run_sha256':sha(REPO/report_generator),'changed_after_training':identity['source_sha256'].get(report_generator)!=sha(REPO/report_generator),
 'scope':'post-run report aggregation only; not imported by canonical_run.py or supervise.py during training'}
cache_unchanged={}
for ds,seeds in identity['feature_caches'].items():
 for seed,record in seeds.items():
  root=pathlib.Path(record['cache_root'])
  for rel,digest in record['cache_file_sha256'].items():
   cache_unchanged[f'{ds}/seed_{seed}/{rel}']=sha(root/rel)==digest
source_stable=all(source_unchanged.values()) and all(cache_unchanged.values())
exact=exact and paired_inputs_ok and source_stable
write('02_DUPLICATE_REPRODUCIBILITY.json',{'state':'PASS' if exact else 'DETERMINISTIC_PROTOCOL_FAILURE',
 'protocol_pairs':len(dup),'independent_executions':2*len(dup),'duplicates':dup,
 'all_checkpoint_hashes_equal_within_pair':all(x['checkpoint_hash_equal'] for x in dup),
 'all_final_score_vector_hashes_equal_within_pair':all(x['score_vector_hash_equal'] for x in dup),
 'all_final_validation_metrics_equal_within_pair':all(x['validation_metrics_equal'] for x in dup),
 'paired_arm_input_initialization_checks':trace_checks,'paired_traces_and_initializations_all_equal':paired_inputs_ok,
 'frozen_sources_unchanged_after_runs':source_unchanged,'cached_feature_files_unchanged_after_runs':cache_unchanged,
 'report_generator_post_run_change':report_generator_hash,
 'all_preflight_sources_and_caches_unchanged':source_stable,
 'test_accessed':False})

def result_for(ds):
 rows=[]
 for seed in (0,1,2):
  row={'seed':seed,'arms':{a:{'validation':canonical[ds][seed][a]['validation'],
    'checkpoint_sha256':canonical[ds][seed][a]['checkpoint_sha256'],
    'score_vector_sha256':canonical[ds][seed][a]['score_vector_sha256'],
    'duplicate_exact':True,'implementation_arm':MAPPING[a]} for a in CANONICAL_ARMS}}
  rows.append(row)
 summary={a:{m:stat([canonical[ds][s][a]['validation'][m] for s in (0,1,2)]) for m in METRICS} for a in CANONICAL_ARMS}
 return {'state':'COMPLETE','dataset':ds,'epochs':5,'seeds':[0,1,2],'arms':rows,'metrics_across_seeds':summary,'duplicate_gate_pass':exact,'test_accessed':False}

cora=result_for('cora');pubmed=result_for('pubmed')
write('03_CORA_RESULTS.json',cora);write('04_PUBMED_RESULTS.json',pubmed)

def contrasts(ds):
 rows=[]
 for seed in (0,1,2):
  m={a:canonical[ds][seed][a]['validation'] for a in CANONICAL_ARMS}
  def contrast(reference):
   return {'delta_CE':m[reference]['ce']-m['A1']['ce'],
           'delta_MRR':m['A1']['mrr']-m[reference]['mrr'],
           'raw_better_on_CE':m['A1']['ce']<m[reference]['ce']}
  rows.append({'seed':seed,'RAW_vs_Z':contrast('A0'),'RAW_vs_SHUFFLE':contrast('A2'),'RAW_vs_NULL':contrast('A3')})
 aggregate={key:{metric:stat([r[key][metric] if metric!='raw_better_on_CE' else float(r[key][metric]) for r in rows])
     for metric in ('delta_CE','delta_MRR','raw_better_on_CE')} for key in ('RAW_vs_Z','RAW_vs_SHUFFLE','RAW_vs_NULL')}
 return {'dataset':ds,'per_seed':rows,'aggregate':aggregate}
contrast_data={ds:contrasts(ds) for ds in ('cora','pubmed')}
write('05_PAIRED_CONTRASTS.json',{'state':'COMPLETE' if exact else 'NOT_INTERPRETED_DUPLICATE_FAILURE',
 'sign_convention':'DeltaCE=CE(comparator)-CE(RAW); DeltaMRR=MRR(RAW)-MRR(comparator); positive means RAW is better.',
 'datasets':contrast_data,'test_accessed':False})

def classify(ds):
 c=contrast_data[ds]['aggregate'];z=c['RAW_vs_Z']['delta_CE'];sh=c['RAW_vs_SHUFFLE']['delta_CE']
 z_wins=c['RAW_vs_Z']['raw_better_on_CE']['wins'];sh_wins=c['RAW_vs_SHUFFLE']['raw_better_on_CE']['wins']
 if z_wins>=2 and z['mean']>0 and sh_wins>=2:return 'STRONG_SIGNAL'
 if z_wins>=1 and sh['mean']>0:return 'WEAK_SIGNAL'
 return 'NO_SIGNAL'

v18=read(REPO/'result/innovation2/CHRI_V18/03_PHASE_A_RESULTS.json')
v181=read(REPO/'result/innovation2/CHRI_V18_1/01_V18_REPRODUCTION.json')
v18_rows={}
for ds in ('cora','pubmed'):
 v18_rows[ds]={}
 for sr in v18['datasets'][ds]['seed_results']:
  v18_rows[ds][sr['seed']]={a:sr['arms'][old]['validation'] for a,old in MAPPING.items()}
v181_rows={}
for ds in ('cora','pubmed'):
 v181_rows[ds]={}
 for sr in v181.get('seed_results',{}).get(ds,[]):
  v181_rows[ds][sr['seed']]={'A0':sr['arms']['R0']['validation'],'A1':sr['arms']['R1']['validation'],'A2':sr['arms']['R2']['validation']}
history={'state':'COMPLETE','V18_state':'CHRI_KILL / CHRI_TRANSFER_WEAK',
 'V18_1_state':'V18_1_REPRODUCTION_MISMATCH','V18_1_reproduction_state':v181.get('state'),
 'V18_1_Phase_A':'NOT_RUN; V18.1 stopped before optimization variants after material V18 reproduction mismatch.',
 'V18_1C_state':'DETERMINISTIC_CANONICAL_REBASELINE','arm_mapping':{'V18 A1/V18.1 R0/V18.1C A0':'Z',
  'V18 A2/V18.1 R1/V18.1C A1':'RAW','V18 A3/V18.1 R2/V18.1C A2':'SHUFFLE','V18 A4/V18.1C A3':'parameter-matched NULL'},
 'datasets':{},'old_atomic_reduction_trajectories_are_historical_not_canonical':True,'test_accessed':False}
for ds in ('cora','pubmed'):
 history['datasets'][ds]={}
 for seed in (0,1,2):
  history['datasets'][ds][str(seed)]={}
  for arm in CANONICAL_ARMS:
   history['datasets'][ds][str(seed)][arm]={'V18':v18_rows[ds][seed][arm],
    'V18_1_reproduction':v181_rows[ds].get(seed,{}).get(arm),
    'V18_1C':canonical[ds][seed][arm]['validation']}
write('HISTORICAL_COMPARISON.json',history)

def mean(ds,arm,metric):return statistics.mean(canonical[ds][s][arm]['validation'][metric] for s in (0,1,2))
lines=['# Historical comparison: V18 vs V18.1 reproduction vs V18.1C','',
       'All rows are validation-only means across seeds 0, 1, 2. CE lower is better; MRR higher is better.',
       'V18.1 reproduction values are the single reproduction-attempt outputs, not a completed Phase-A optimization run.',
       'V18.1 has no NULL replay (`—`). Canonical A0/A1/A2/A3 correspond to Z/RAW/SHUFFLE/NULL.','']
for ds in ('cora','pubmed'):
 lines += [f'## {ds.title()}','', '| Arm | V18 CE / MRR | V18.1 reproduction CE / MRR | V18.1C CE / MRR |','|---|---:|---:|---:|']
 for arm in CANONICAL_ARMS:
  oldvals=[v18_rows[ds][s][arm] for s in (0,1,2)]
  newvals=[v181_rows[ds].get(s,{}).get(arm) for s in (0,1,2)]
  canon=[canonical[ds][s][arm]['validation'] for s in (0,1,2)]
  fmt=lambda arr,key:'—' if not arr or arr[0] is None else f"{statistics.mean(x[key] for x in arr):.6f} / {statistics.mean(x['mrr'] for x in arr):.6f}"
  lines.append(f"| {arm} ({ {'A0':'Z','A1':'RAW','A2':'SHUFFLE','A3':'NULL'}[arm] }) | {fmt(oldvals,'ce')} | {fmt(newvals,'ce')} | {fmt(canon,'ce')} |")
 lines.append('')
lines += ['Historical V18 remains unchanged as prior evidence. V18.1 reports `V18_1_REPRODUCTION_MISMATCH` and its Phase-A optimization variants were not run. V18.1C starts a fresh canonical validation-only baseline with deterministic segment reductions; it does not claim numerical reproduction of the old atomic-reduction trajectories.']
(OUT/'06_HISTORICAL_COMPARISON.md').write_text('\n'.join(lines)+'\n')

if not exact:
 final='DETERMINISTIC_PROTOCOL_FAILURE';cora_signal=pubmed_signal='NOT_INTERPRETED'
else:
 cora_signal=classify('cora');pubmed_signal=classify('pubmed')
 signals={'STRONG_SIGNAL','WEAK_SIGNAL'}
 if cora_signal in signals and pubmed_signal in signals and all(contrast_data[d]['aggregate']['RAW_vs_SHUFFLE']['delta_CE']['mean']>0 for d in ('cora','pubmed')):final='CANONICAL_SIGNAL_PRESENT'
 elif (cora_signal in signals) != (pubmed_signal in signals):final='CANONICAL_ONE_DATASET_ONLY'
 else:final='CANONICAL_NO_SIGNAL'
decision={'FINAL_STATUS':final,'Cora':cora_signal,'PubMed':pubmed_signal,
 'Cora_raw_vs_shuffle_mean_delta_CE':contrast_data['cora']['aggregate']['RAW_vs_SHUFFLE']['delta_CE']['mean'],
 'PubMed_raw_vs_shuffle_mean_delta_CE':contrast_data['pubmed']['aggregate']['RAW_vs_SHUFFLE']['delta_CE']['mean'],
 'resume_V18_1_residualization':final=='CANONICAL_SIGNAL_PRESENT','test_accessed':False,
 'innovation1_modified':False,'new_method_variants_run':False}
write('DECISION.json',decision)
def contrast_text(ds,name):
 q=contrast_data[ds]['aggregate'][name]
 return f"DeltaCE={q['delta_CE']['per_seed']} (mean {q['delta_CE']['mean']:.6f}; wins {q['delta_CE']['wins']}/3), DeltaMRR={q['delta_MRR']['per_seed']} (mean {q['delta_MRR']['mean']:.6f})"
decision_md=f'''# Canonical decision

**Status: `{final}`**

- Cora: **{cora_signal}**.
- PubMed: **{pubmed_signal}**.
- Cora RAW vs Z: {contrast_text('cora','RAW_vs_Z')}.
- Cora RAW vs SHUFFLE: {contrast_text('cora','RAW_vs_SHUFFLE')}.
- Cora RAW vs NULL: {contrast_text('cora','RAW_vs_NULL')}.
- PubMed RAW vs Z: {contrast_text('pubmed','RAW_vs_Z')}.
- PubMed RAW vs SHUFFLE: {contrast_text('pubmed','RAW_vs_SHUFFLE')}.
- PubMed RAW vs NULL: {contrast_text('pubmed','RAW_vs_NULL')}.

Deterministic duplicate gate: **{'PASS' if exact else 'FAIL'}**. Test accessed: **NO**. Innovation 1 modified: **NO**.

{'The deterministic signal meets the two-dataset V18.1C continuation rule. V18.1 residualization/stability optimization may resume under `CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1`, but it is not started by this task.' if final=='CANONICAL_SIGNAL_PRESENT' else 'The V18.1C cross-dataset continuation rule is not met. Do not start residualization under this decision.'}
'''
(OUT/'07_CANONICAL_DECISION.md').write_text(decision_md)

manifest={'task':'CHRI_V18_1C_DETERMINISTIC_REBASELINE','state':final,'workspace':'DCDLP-main',
 'canonical_protocol':'CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1','datasets':['cora','pubmed'],'seeds':[0,1,2],
 'epochs':5,'arms':{'A0':'Z','A1':'Z+RAW R_CAT','A2':'Z+matched SHUFFLE R_CAT','A3':'Z+parameter-matched NULL'},
 'implementation_arm_mapping':MAPPING,'duplicate_executions_per_cell':2,'duplicate_gate':'PASS' if exact else 'FAIL',
 'test_accessed':False,'innovation1_modified':False,'historical_V18_modified':False,'historical_V18_1_modified':False,
 'method_optimization_run':False,'residualization_run':False,'run_status':status,'source_sha256':read(A/'01_CANONICAL_IMPLEMENTATION.json')['source_sha256']}
write('RUN_MANIFEST.json',manifest)
files={str(p.relative_to(REPO)):sha(p) for p in sorted(A.rglob('*')) if p.is_file() and p.name not in ('SOURCE_HASHES.json','RUN_MANIFEST.json') and '__pycache__' not in p.parts}
write('SOURCE_HASHES.json',{'state':'FROZEN_AFTER_CANONICAL_RUN','files':files,'test_accessed':False,
 'historical_artifacts_modified':False,'innovation1_modified':False})

report=f'''# V18.1C deterministic canonical rebaseline

**FINAL_STATUS: `{final}`**

## Protocol and integrity

The canonical path uses the exact V18.1R-verified segment-reduction implementation (`torch.segment_reduce`, SHA-256 `{read(A/'01_CANONICAL_IMPLEMENTATION.json')['deterministic_implementation']['sha256']}`). PyTorch deterministic algorithms and deterministic cuDNN were enabled; TF32 was disabled. The frozen NCNC backbones, V18 feature caches/splits/candidate and negative schedules, model definitions, optimizer, learning rates, batch sizes, and five-epoch validation evaluator were held fixed. The underlying V18 implementation arm mapping is recorded in `01_CANONICAL_IMPLEMENTATION.json`.

The duplicate gate **{'PASS' if exact else 'FAIL'}**: {len(dup)} dataset/seed/arm cells, {2*len(dup)} independent executions. Checkpoint-file SHA-256 and final validation score-vector SHA-256 matched within every pair. Paired arms also share the same cached training traces and initialization streams. Test remained sealed; no residualization, gating, CRIB, architecture or hyperparameter change was run. Innovation 1 remains FINAL_FROZEN. A report-only `finalize.py` path reference was corrected after training; it was not used by training, and its before/after hashes are recorded in `02_DUPLICATE_REPRODUCIBILITY.json`.

## Deterministic Phase-A signal

Sign convention: `DeltaCE = CE(comparator) - CE(RAW)` and `DeltaMRR = MRR(RAW) - MRR(comparator)`; positive values favor RAW. The full per-seed metrics are in `03_CORA_RESULTS.json`, `04_PUBMED_RESULTS.json`, and `05_PAIRED_CONTRASTS.json`.

| Dataset | Signal class | RAW vs Z: mean ΔCE; CE wins | RAW vs SHUFFLE: mean ΔCE; CE wins | RAW vs NULL: mean ΔCE; CE wins |
|---|---|---:|---:|---:|
| Cora | {cora_signal} | {contrast_data['cora']['aggregate']['RAW_vs_Z']['delta_CE']['mean']:.6f}; {contrast_data['cora']['aggregate']['RAW_vs_Z']['delta_CE']['wins']}/3 | {contrast_data['cora']['aggregate']['RAW_vs_SHUFFLE']['delta_CE']['mean']:.6f}; {contrast_data['cora']['aggregate']['RAW_vs_SHUFFLE']['delta_CE']['wins']}/3 | {contrast_data['cora']['aggregate']['RAW_vs_NULL']['delta_CE']['mean']:.6f}; {contrast_data['cora']['aggregate']['RAW_vs_NULL']['delta_CE']['wins']}/3 |
| PubMed | {pubmed_signal} | {contrast_data['pubmed']['aggregate']['RAW_vs_Z']['delta_CE']['mean']:.6f}; {contrast_data['pubmed']['aggregate']['RAW_vs_Z']['delta_CE']['wins']}/3 | {contrast_data['pubmed']['aggregate']['RAW_vs_SHUFFLE']['delta_CE']['mean']:.6f}; {contrast_data['pubmed']['aggregate']['RAW_vs_SHUFFLE']['delta_CE']['wins']}/3 | {contrast_data['pubmed']['aggregate']['RAW_vs_NULL']['delta_CE']['mean']:.6f}; {contrast_data['pubmed']['aggregate']['RAW_vs_NULL']['delta_CE']['wins']}/3 |

RAW-vs-Z paired DeltaMRR means are Cora {contrast_data['cora']['aggregate']['RAW_vs_Z']['delta_MRR']['mean']:.6f} and PubMed {contrast_data['pubmed']['aggregate']['RAW_vs_Z']['delta_MRR']['mean']:.6f}. RAW-vs-SHUFFLE paired DeltaMRR means are Cora {contrast_data['cora']['aggregate']['RAW_vs_SHUFFLE']['delta_MRR']['mean']:.6f} and PubMed {contrast_data['pubmed']['aggregate']['RAW_vs_SHUFFLE']['delta_MRR']['mean']:.6f}. RAW-vs-NULL paired DeltaMRR means are Cora {contrast_data['cora']['aggregate']['RAW_vs_NULL']['delta_MRR']['mean']:.6f} and PubMed {contrast_data['pubmed']['aggregate']['RAW_vs_NULL']['delta_MRR']['mean']:.6f}.

## Historical context and next step

V18 remains `CHRI_KILL / CHRI_TRANSFER_WEAK`; V18.1 remains `V18_1_REPRODUCTION_MISMATCH` and did not run its Phase-A optimization variants. Their metrics are shown descriptively beside V18.1C in `06_HISTORICAL_COMPARISON.md`. V18 and V18.1 used the old atomic-reduction numerical path; those trajectories remain historical evidence and are not claimed to be reproduced numerically by V18.1C.

**Should V18.1 residualization resume?** {'Yes, as a separately authorized next task and only under `CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1`.' if final=='CANONICAL_SIGNAL_PRESENT' else 'No; the cross-dataset continuation criterion was not met.'} It is not started here.

**Test opened:** NO. **Innovation 1 modified:** NO. **Final C2C handoff status:** {final}.
'''
(OUT/'FINAL_REPORT.md').write_text(report)
# Include hashes of the final handoff artifacts after they are written.
hash_manifest=read(OUT/'SOURCE_HASHES.json')
hash_manifest['preflight_source_sha256']=identity['source_sha256']
hash_manifest['preflight_sources_unchanged_after_runs']=source_unchanged
hash_manifest['critical_result_artifact_sha256']={name:sha(OUT/name) for name in
 ['00_PROTOCOL.md','01_CANONICAL_IMPLEMENTATION.json','02_DUPLICATE_REPRODUCIBILITY.json',
  '03_CORA_RESULTS.json','04_PUBMED_RESULTS.json','05_PAIRED_CONTRASTS.json',
  '06_HISTORICAL_COMPARISON.md','07_CANONICAL_DECISION.md','RUN_MANIFEST.json','FINAL_REPORT.md']}
write('SOURCE_HASHES.json',hash_manifest)
print(json.dumps({'state':final,'duplicate_pairs':len(dup),'deterministic_duplicates_pass':exact,
 'Cora':cora_signal,'PubMed':pubmed_signal,'test_accessed':False,'artifacts':sorted(p.name for p in OUT.iterdir())},indent=2))
