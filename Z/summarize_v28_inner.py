import json,pathlib,statistics
base=pathlib.Path(r'E:\Z\v28_results_complete')
x=json.load(open(base/'12_PHASE_B_INNER_VALIDATION.json',encoding='utf-8-sig'))
for ds,d in x['datasets'].items():
 print('\nDATASET',ds,'eligible',[(z['hypothesis'],z['candidate'],z['controls']) for z in d['eligible_hypotheses']])
 for ep,b in d['budgets'].items():
  print(' EPOCH',ep,'seeds',b['datasets'][ds]['seeds'] if 'seeds' in b['datasets'][ds] else [q['seed'] for q in b['datasets'][ds]['seed_results']])
  rows=b['datasets'][ds]['seed_results']
  arms=rows[0]['arms'].keys();print(' arms',list(arms))
  candidates=[z['candidate'] for z in d['eligible_hypotheses']]
  for cand in candidates:
   for ctrl in ['SHARED','ZERO6','GRAPH6','MULT6']:
    if ctrl==cand or ctrl not in rows[0]['arms']:continue
    ce=[r['arms'][ctrl]['validation']['ce']-r['arms'][cand]['validation']['ce'] for r in rows]
    mr=[r['arms'][cand]['validation']['mrr']-r['arms'][ctrl]['validation']['mrr'] for r in rows]
    if ctrl not in (cand,):print(f'  {cand}-{ctrl}: dCE mean {statistics.mean(ce):+.6f} {ce}; dMRR mean {statistics.mean(mr):+.6f} {mr}')
  # candidate raw means
  for arm in candidates+['SHARED','ZERO6']:
   if arm not in rows[0]['arms']:continue
   ce=[r['arms'][arm]['validation']['ce'] for r in rows];mr=[r['arms'][arm]['validation']['mrr'] for r in rows]
   print(f'  {arm} mean CE={statistics.mean(ce):.6f}, MRR={statistics.mean(mr):.6f}')
