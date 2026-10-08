import importlib.util, sys, json, pathlib, hashlib
root=pathlib.Path('/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH')
spec=importlib.util.spec_from_file_location('v171',root/'HSPE_V17_1/scripts/hspe_v17_1.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
j=m.read_json(root/'HSPE_V17_1/results.json')
src=m.sources(); print('CURRENT_SOURCES',json.dumps(src))
variants={}
for ds in m.DATASETS:
 for phase in ('phase_a','phase_rank'):
  for seed in m.SEEDS:
   for arm,row in m.read_json(root/'HSPE_V17_1/experiments'/phase/ds/f'seed_{seed}/results.json')['arms'].items():
    variants.setdefault(row['execution_sources']['v171'],[]).append([ds,phase,seed,arm])
print('V171_VARIANTS',json.dumps(variants))
text=(root/'HSPE_V17_1/scripts/hspe_v17_1.py').read_text()
old=text.replace('        # CUDA message aggregation can vary by one float32 ULP across forward\n        # calls even with bit-identical parameters and a zero residual head.\n        # 5e-7 accepts that round-off while still checking the initial function.\n','').replace('err<=5e-7','err<=2e-7').replace("'logit_roundoff_tolerance':5e-7,",'')
print('RECONSTRUCTED_PRE_AUDIT_HASH',hashlib.sha256(old.encode()).hexdigest())
row=m.read_json(root/'HSPE_V17_1/experiments/phase_rank/cora/seed_0/results.json')['arms']['H2_R_HSPE']
ck=m.torch.load(row['checkpoint'],map_location='cpu',weights_only=False)
print('CHECKPOINT_KEYS',list(ck)); print('CHECKPOINT_CONFIG',json.dumps(ck.get('config'),default=str)); print('PARAMETERS',sum(v.numel() for v in ck['model'].values()))
print('BEST_CONTEXT',json.dumps({ds:max(('C0_COUNT_LINEAR','C1_COUNT_PARAM_MATCHED','C2_CONSTANT_SET'),key=lambda arm:j['phase_a']['datasets'][ds]['metrics'][arm]['mrr']['mean']) for ds in m.DATASETS}))
