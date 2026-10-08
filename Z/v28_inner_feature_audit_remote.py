import pathlib,hashlib,json,numpy as np
exp=pathlib.Path('/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/TOPOLOGY_V28')
out={'ready_count':0,'missing':[],'hash_errors':[],'load_errors':[],'structures':{}}
for ready in sorted((exp/'features/inner').rglob('READY.json')):
 out['ready_count']+=1;obj=json.load(open(ready))
 for name,h in obj['hashes'].items():
  p=ready.parent/name
  if not p.is_file():out['missing'].append(str(p));continue
  if hashlib.sha256(p.read_bytes()).hexdigest()!=h:out['hash_errors'].append(str(p))
  if p.suffix=='.npy':
   try:np.load(p,mmap_mode='r',allow_pickle=False)
   except Exception as e:out['load_errors'].append([str(p),repr(e)])
for ds in ('cora','pubmed'):
 p=exp/'data/inner/cache'/ds/'STRUCTURE_READY.json';x=json.load(open(p));out['structures'][ds]={'state':x.get('state'),'target_mask_oracle':x.get('target_mask_oracle')}
json.dump(out,open('/tmp/v28_inner_feature_audit.json','w'),indent=2)
print(json.dumps({k:v for k,v in out.items() if k not in ('hash_errors','load_errors','missing')},indent=2));print('missing',len(out['missing']),'hash_errors',len(out['hash_errors']),'load_errors',len(out['load_errors']))
