import json,pathlib,statistics,collections
base=pathlib.Path(r'E:\Z\v28_results_complete')
x=json.load(open(base/'12_PHASE_B_INNER_VALIDATION.json',encoding='utf-8-sig'))
checks={'test_false':True,'all_complete':True,'all_expected_epochs':True,'paired_first5_schedule_matches':True,'initializations_match':True,'parameters':{},'scores':[]}
for ds,d in x['datasets'].items():
 for s in (3,4,5):
  for arm in ('GRAPH6','MULT6','SHARED','ZERO6'):
   r5=d['budgets']['5']['datasets'][ds]['seed_results'][s-3]['arms'][arm]
   r10=d['budgets']['10']['datasets'][ds]['seed_results'][s-3]['arms'][arm]
   checks['test_false'] &= r5.get('test_accessed') is False and r10.get('test_accessed') is False
   checks['all_complete'] &= r5.get('state')==r10.get('state')=='COMPLETE'
   checks['all_expected_epochs'] &= len(r5['history'])==5 and len(r10['history'])==10
   checks['paired_first5_schedule_matches'] &= r5['training_trace']==r10['training_trace'][:5]
   checks['initializations_match'] &= r5['initialization']==r10['initialization']
   checks['parameters'].setdefault((ds,arm),set()).update([r5['trainable_parameters'],r10['trainable_parameters']])
   checks['scores'].append((ds,s,arm,r5['score_vector_sha256'],r10['score_vector_sha256']))
print({k:v for k,v in checks.items() if k!='scores'})
for ds,d in x['datasets'].items():
 print('\n',ds)
 for ep in ('5','10'):
  rows=d['budgets'][ep]['datasets'][ds]['seed_results'];print(' epochs',ep)
  for cand in ('GRAPH6','MULT6'):
   for ctrl in ('SHARED','ZERO6'):
    dce=[r['arms'][ctrl]['validation']['ce']-r['arms'][cand]['validation']['ce'] for r in rows]
    dmrr=[r['arms'][cand]['validation']['mrr']-r['arms'][ctrl]['validation']['mrr'] for r in rows]
    print(cand,'vs',ctrl,'dCE',round(statistics.mean(dce),6),'wins',sum(a>0 for a in dce),'perseed',[round(z,6) for z in dce], 'dMRR',round(statistics.mean(dmrr),6),'wins',sum(a>0 for a in dmrr),'perseed',[round(z,6) for z in dmrr])
