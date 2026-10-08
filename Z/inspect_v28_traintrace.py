import json
x=json.load(open(r'E:\Z\v28_results_complete\12_PHASE_B_INNER_VALIDATION.json',encoding='utf-8-sig'))
for ds in x['datasets']:
 for ep in ('5','10'):
  r=x['datasets'][ds]['budgets'][ep]['datasets'][ds]['seed_results'][0]['arms']['GRAPH6']
  print(ds,ep,'train_trace type',type(r['training_trace']).__name__,'len',len(r['training_trace']) if hasattr(r['training_trace'],'__len__') else None,'sample',str(r['training_trace'])[:300])
  print('history len',len(r['history']),'init',r['initialization'])
  if ep=='5':break
