import csv,json,math,shutil,hashlib
from pathlib import Path
ROOT=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main'); OUT=ROOT/'PAPER_PREP/R_HSPE_DSR_MANUSCRIPT_V2'; STAGE=Path(r'E:\Z\dsr_v32_audit_sources'); AD=OUT/'audit_sources/DSR_V32'; T=OUT/'tables'
assert ROOT.name=='DCDLP-main' and OUT.is_dir()
FILES=['FINAL_REPORT.md','DECISION_CORRECTION.md','SOURCE_AUDIT.json','RUN_STATUS.json','FINAL_INTEGRITY.json','FINALIZATION_FAILURE_EVIDENCE.json','POSTPROCESS_RECOVERY.md','02_PARAMETER_AUDIT.json','03_ROUTER_SANITY.json','04_DETERMINISM.json','05_PHASE_A_RESULTS.json','07_ROUTER_DIAGNOSTICS.json','08_PHASE_B_RESULTS.json','09_CITESEER_TRANSFER.json','10_INNER_VALIDATION.json','11_DECISION.md']
for f in FILES: shutil.copy2(STAGE/f,AD/f)
phases={k:json.loads((AD/f).read_text(encoding='utf-8')) for k,f in {'phase_a':'05_PHASE_A_RESULTS.json','phase_b':'08_PHASE_B_RESULTS.json','citeseer_transfer':'09_CITESEER_TRANSFER.json','inner_validation':'10_INNER_VALIDATION.json'}.items()}
params=json.loads((AD/'02_PARAMETER_AUDIT.json').read_text(encoding='utf-8')); diag=json.loads((AD/'07_ROUTER_DIAGNOSTICS.json').read_text(encoding='utf-8')); sanity=json.loads((AD/'03_ROUTER_SANITY.json').read_text(encoding='utf-8')); run=json.loads((AD/'RUN_STATUS.json').read_text(encoding='utf-8')); integrity=json.loads((AD/'FINAL_INTEGRITY.json').read_text(encoding='utf-8'))
assert all(d['state']=='COMPLETE' and d['test_opened'] is False for d in phases.values()) and params['state']=='PASS' and params['verified_jobs']==156 and sanity['state']=='PASS' and integrity['state']=='PASS' and run['state']=='COMPLETE'
M=['ce','mrr','hits10','hits20','auc']
def st(x):
 m=sum(x)/len(x); sd=math.sqrt(sum((v-m)**2 for v in x)/(len(x)-1)) if len(x)>1 else 0
 return {'mean':m,'sd':sd,'n':len(x),'wins':sum(v>0 for v in x),'per_seed':x}
def contrasts(phase,ds):
 recs=phases[phase]['datasets'][ds]['seed_results']; out={}
 for arm in sorted(set.intersection(*(set(r['arms']) for r in recs))-{'A6'}):
  vals={m:[] for m in M}
  for r in recs:
   a=r['arms']['A6']['validation'];b=r['arms'][arm]['validation']
   vals['mrr'].append(a['mrr']-b['mrr']);vals['ce'].append(b['ce']-a['ce'])
   for m in ('hits10','hits20','auc'): vals[m].append(a[m]-b[m])
  out[arm]={m:st(v) for m,v in vals.items()}
 return out
C={f'{p}/{ds}':contrasts(p,ds) for p,d in phases.items() for ds in d['datasets']}
assert abs(C['phase_b/pubmed']['A4']['mrr']['mean']-.00440995)<5e-9 and C['phase_b/pubmed']['A4']['mrr']['wins']==4
assert abs(C['phase_b/pubmed']['A7']['mrr']['mean']+.00137762)<5e-9 and C['phase_b/pubmed']['A7']['mrr']['wins']==2
assert abs(C['phase_b/cora']['A4']['mrr']['mean']-.00046272)<5e-9 and abs(C['phase_b/cora']['A7']['mrr']['mean']-.00190467)<5e-9
assert abs(C['citeseer_transfer/citeseer']['A0']['mrr']['mean']-.006628526066852047)<1e-12
assert abs(C['inner_validation/pubmed']['A7']['mrr']['mean']-.00161579)<5e-9
A={'workspace':'DCDLP-main','local_git_root':str(ROOT),'git_commit':'5da7af3d282f4378b128a0ef8fb7f2e3503a9c74','experiment':'DSR_V32','status':'COMPLETE','verified_jobs':156,'phases':{},'arms':{'A0':'NCNC','A1':'NCNC+R','A2':'NCNC+GRAPH','A3':'NCNC+PBD','A4':'fixed equal 1/3 R/G/P; disconnected 83-parameter pad','A5':'global learned 3-logit R/G/P; disconnected 80-parameter pad','A6':'candidate-routed R/G/P','A7':'candidate-routed G/G/G repeated-GRAPH control','A8':'candidate-routed R/R/R','A9':'R/G/P with stratified shuffled candidate context','A10':'R/G/P with zero router context'},'paired_contrasts_recomputed':C,'router_diagnostics':diag,'router_sanity':sanity,'parameter_audit':params,'integrity':{'all_training_finished':True,'test_opened':False,'innovation1_modified':False,'historical_results_modified':False,'router_collapse':run['decision']['ROUTER_COLLAPSE']},'postprocessing':'Initial aggregation failed with KeyError(A6) after training; recovery reran reporting from existing scalar JSON; no retraining.'}
for p,d in phases.items():
 A['phases'][p]={}
 for ds,x in d['datasets'].items():
  A['phases'][p][ds]={'seeds':[r['seed'] for r in x['seed_results']],'metrics_mean_sd':x['metrics'],'per_seed':[{'seed':r['seed'],'arms':{a:r['arms'][a]['validation'] for a in r['arms']}} for r in x['seed_results']],'A6_minus_control_recomputed':C[f'{p}/{ds}']}
(OUT/'DSR_NUMERICAL_AUDIT.json').write_text(json.dumps(A,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
T.mkdir(exist_ok=True)
rows=[]
for p,label in [('phase_a','Phase A, seeds 0-2'),('phase_b','Phase B, new seeds 3-7')]:
 for ds,x in phases[p]['datasets'].items():
  m=x['metrics'];c=C[f'{p}/{ds}']; row=[ds.capitalize(),label,m['A6']['mrr']['mean'],m['A6']['mrr']['std']]
  for arm in ['A4','A7','A5','A9']:
   e=c[arm]['mrr']; row += [e['mean'],e['sd'],e['wins'],e['n']]
  rows.append(row)
heads=['dataset','phase','A6_mrr_mean','A6_mrr_sd']+sum(([f'delta_vs_{a}',f'paired_sd_{a}',f'wins_{a}',f'n_{a}'] for a in ['A4','A7','A5','A9']),[])
with (T/'table7_dsr_primary.csv').open('w',newline='',encoding='utf-8-sig') as f: w=csv.writer(f);w.writerow(heads);w.writerows(rows)
lines=['**Table 7. Dynamic structural routing and matched validation controls**','','| Dataset | Phase | A6 MRR mean ± SD | Δ vs A4 fixed mixture | Δ vs A7 repeated GRAPH | Δ vs A5 global mixture | Δ vs A9 shuffle |','|---|---|---:|---:|---:|---:|---:|']
for r in rows:
 ds,label,am,asv,*e=r; cells=[]
 for i in range(0,len(e),4): cells.append(f'{e[i]:+.6f} ± {e[i+1]:.6f}; {e[i+2]}/{e[i+3]}')
 lines.append(f'| {ds} | {label} | {am:.6f} ± {asv:.6f} | '+' | '.join(cells)+' |')
lines+=['','ΔMRR is paired A6 minus comparator. A4 is fixed equal-weight R/G/P; A5 learns candidate-independent global weights; A7 routes among three independently initialized GRAPH experts; A9 shuffles candidate context. A4/A5 declared parameter counts include disconnected pads. Means and sample SDs are seed-level; all rows are validation-only.']
(T/'table7_dsr_primary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
metric_rows=[];pair_rows=[]
for p,d in phases.items():
 for ds,x in d['datasets'].items():
  seeds=[r['seed'] for r in x['seed_results']]
  for arm,v in x['metrics'].items(): metric_rows.append([p,ds,','.join(map(str,seeds)),arm]+[v[m]['mean'] for m in M]+[v[m]['std'] for m in M])
  for r in x['seed_results']:
   a=r['arms']['A6']['validation']
   for arm,q in r['arms'].items():
    if arm=='A6': continue
    b=q['validation'];pair_rows.append([p,ds,r['seed'],arm,a['mrr'],b['mrr'],a['mrr']-b['mrr'],b['ce']-a['ce'],a['hits10']-b['hits10'],a['hits20']-b['hits20'],a['auc']-b['auc']])
with (T/'tableS6_all_metrics.csv').open('w',newline='',encoding='utf-8-sig') as f: w=csv.writer(f);w.writerow(['phase','dataset','seeds','arm']+['mean_'+m for m in M]+['sd_'+m for m in M]);w.writerows(metric_rows)
with (T/'dsr_per_seed_contrasts.csv').open('w',newline='',encoding='utf-8-sig') as f: w=csv.writer(f);w.writerow(['phase','dataset','seed','control','A6_MRR','control_MRR','delta_MRR','delta_CE_control_minus_A6','delta_Hits10','delta_Hits20','delta_AUC']);w.writerows(pair_rows)
subgroups=[('R absent','R_token_count_zero'),('R present','R_token_count_positive'),('P3 = 0','P3_zero'),('P3 > 0','P3_positive'),('GRAPH low','projected_CN_low'),('GRAPH high','projected_CN_high')]
rr=[]
for ds in ['cora','pubmed']:
 for label,key in subgroups:
  s=diag[ds]['A6']['subgroups'][key]; rr.append([ds,label,s['n'],*s['mean'],*s['std'],*s['q05_q50_q95'][0],*s['q05_q50_q95'][1],*s['q05_q50_q95'][2]])
with (T/'tableS7_router_weights.csv').open('w',newline='',encoding='utf-8-sig') as f: w=csv.writer(f);w.writerow(['dataset','subgroup','n']+[f'mean_alpha_{x}' for x in 'RGP']+[f'sd_alpha_{x}' for x in 'RGP']+[f'q05_alpha_{x}' for x in 'RGP']+[f'q50_alpha_{x}' for x in 'RGP']+[f'q95_alpha_{x}' for x in 'RGP']);w.writerows(rr)
router=['**Table S7. Candidate-router weight distributions on validation candidates**','','Each weight cell reports mean [5th, 95th percentile]; full means, SDs, medians, and quantiles are in `tableS7_router_weights.csv`. GRAPH low/high is the projected common-neighbor median split. These are descriptive routing behavior, not causal attribution. Counts pool the fixed validation candidates across seeds.','']
for ds in ['cora','pubmed']:
 router += [f'**{ds.capitalize()}**','','| Subgroup | n | αR mean [p05,p95] | αG mean [p05,p95] | αP mean [p05,p95] |','|---|---:|---:|---:|---:|']
 for label,key in subgroups:
  s=diag[ds]['A6']['subgroups'][key];q=s['q05_q50_q95'];router.append(f"| {label} | {s['n']} | {s['mean'][0]:.3f} [{q[0][0]:.3f},{q[2][0]:.3f}] | {s['mean'][1]:.3f} [{q[0][1]:.3f},{q[2][1]:.3f}] | {s['mean'][2]:.3f} [{q[0][2]:.3f},{q[2][2]:.3f}] |")
 router.append('')
router.append(f"Router collapse was false for A6 on Cora and PubMed. The A9 context shuffle changed {diag['cora']['A9']['context_change_fraction']:.1%} of Cora and {diag['pubmed']['A9']['context_change_fraction']:.1%} of PubMed validation feature rows.")
(T/'tableS7_router_weights.md').write_text('\n'.join(router)+'\n',encoding='utf-8')
runtime=[]
for p in ['phase_a','phase_b']:
 for ds,x in phases[p]['datasets'].items():
  for arm in ['A0','A4','A6','A7']:
   z=[r['arms'][arm] for r in x['seed_results'] if arm in r['arms']]
   if z:
    times=[q['wall_seconds'] for q in z];mem=[q['peak_gpu_mb'] for q in z]
    runtime.append([p,ds,arm,len(z),sum(times)/len(times),st(times)['sd'],sum(mem)/len(mem),st(mem)['sd']])
with (T/'tableS8_runtime.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.writer(f);w.writerow(['phase','dataset','arm','n','wall_seconds_mean','wall_seconds_sd','peak_gpu_MiB_mean','peak_gpu_MiB_sd']);w.writerows(runtime)
print('DSR numerical audits and tables generated',len(metric_rows),'arm-rows',len(pair_rows),'paired rows')
