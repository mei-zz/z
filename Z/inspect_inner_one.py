import json
x=json.load(open(r'E:\Z\v28_results_complete\12_PHASE_B_INNER_VALIDATION.json',encoding='utf-8-sig'))
r=x['datasets']['cora']['budgets']['5']['datasets']['cora']['seed_results'][0]['arms']['GRAPH6']
print('checkpoint',r['checkpoint'],'score',r['score_vector_sha256'],'training trajectory',r['training_trajectory_sha256'],'params',r['trainable_parameters'],'steps',r['optimizer_steps'],'initialization',str(r['initialization'])[:180])
