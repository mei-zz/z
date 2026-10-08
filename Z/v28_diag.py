import json, pathlib, shutil
root=pathlib.Path('/home/ubuntu/lchr_v2')
art=root/'result/innovation2/TOPOLOGY_V28'
h=json.load(open(art/'SOURCE_HASHES.json'))
print('manifest keys',list(h.keys()))
print('historical cache count',len(h.get('historical_topology_caches',{})))
for p,x in h.get('historical_topology_caches',{}).items():
 q=root/p
 print(('OK' if q.exists() else 'MISSING'),p, q.stat().st_size if q.exists() and q.is_file() else '')
for p in ['HYPERGRAPH_RESEARCH/HDP2_V27/scripts/hdp27.py','HYPERGRAPH_RESEARCH/CHRI_V18/scripts/chri_features.py','HYPERGRAPH_RESEARCH/ERDR_V21/scripts/erdr21.py','HYPERGRAPH_RESEARCH/CHRI_V18_1R/scripts/deterministic_aggregation.py']:
 print(('OK' if (root/p).exists() else 'MISSING'),p)
print('disk',shutil.disk_usage(root))
