import json,hashlib,pathlib,numpy as np
root=pathlib.Path('/home/ubuntu/lchr_v2'); exp=root/'HYPERGRAPH_RESEARCH/TOPOLOGY_V28'; art=root/'result/innovation2/TOPOLOGY_V28';x=json.load(open(art/'12_PHASE_B_INNER_VALIDATION.json'))
out={'files':0,'score_file_missing':[],'score_hash_errors':[],'raw_json_mismatch':[],'checkpoint_hash_errors':[],'logs':0,'completion_markers':0,'traceback_lines':0}
def scorehash(p):
 h=hashlib.sha256()
 with np.load(p) as z:
  for k in ('positive','negative'):
   a=np.ascontiguousarray(z[k]);h.update(k.encode());h.update(str(a.shape).encode());h.update(str(a.dtype).encode());h.update(a.tobytes())
 return h.hexdigest()
for ds,d in x['datasets'].items():
 for ep,b in d['budgets'].items():
  for row in b['datasets'][ds]['seed_results']:
   for arm,r in row['arms'].items():
    out['files']+=1; folder=pathlib.Path(r['checkpoint']).parent;p=folder/f'valid_epoch{ep}_scores.npz'
    if not p.is_file():out['score_file_missing'].append(str(p))
    elif scorehash(p)!=r['score_vector_sha256']:out['score_hash_errors'].append(str(p))
    q=folder/'result.json'
    if not q.is_file() or json.load(open(q))!=r:out['raw_json_mismatch'].append(str(q))
    cp=pathlib.Path(r['checkpoint'])
    if not cp.is_file() or hashlib.sha256(cp.read_bytes()).hexdigest()!=r['checkpoint_sha256']:out['checkpoint_hash_errors'].append(str(cp))
for p in (exp/'logs').glob('train_inner_*.log'):
 out['logs']+=1;t=p.read_text(errors='replace');out['completion_markers']+=t.count('V28_JOB_COMPLETE inner');out['traceback_lines']+=t.count('Traceback')+t.count('No space left')+t.count('No data left')
json.dump(out,open('/tmp/v28_execution_audit2.json','w'),indent=2);print(json.dumps(out,indent=2))
