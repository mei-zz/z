import json,pathlib
p=pathlib.Path(r'E:\Z\v28_results_complete\12_PHASE_B_INNER_VALIDATION.json')
x=json.load(open(p,encoding='utf-8-sig'))
for ds,d in x['datasets'].items():
 for ep,b in d['budgets'].items():
  c=b['datasets'][ds]
  print(ds,ep,'dataset keys',list(c.keys()),'budget keys',list(b.keys()))
  row=c['seed_results'][0]
  print('row keys',list(row.keys()),'arm keys',list(row['arms']['GRAPH6'].keys()),'arm result keys',list(row['arms']['GRAPH6'].keys()))
  print('effect keys',list(c.get('effects',{}).keys())[:8])
  break
