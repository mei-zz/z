import json,pathlib,statistics
base=pathlib.Path(r'E:\Z\v28_results_complete')
b=json.load(open(base/'11_PHASE_B_NEW_SEED_RESULTS.json',encoding='utf-8-sig'))['new_seeds_only']
for ds in ('cora','pubmed'):
 d=b['datasets'][ds]['effects']
 print(ds)
 for c in ('GRAPH6','MULT6'):
  print(c,{x:round(d[f'{c}_vs_{x}']['ce']['mean'],6) for x in ('SHARED','ZERO6')})
