import json,pathlib,hashlib
r=pathlib.Path('/home/ubuntu/lchr_v2'); a=r/'result/innovation2/TOPOLOGY_V28'; h=json.load(open(a/'SOURCE_HASHES.json'))
out={}
for group in ('files','historical_topology_caches'):
 out[group]=[]
 for p,x in h[group].items():
  q=r/p
  if not q.is_file() or hashlib.sha256(q.read_bytes()).hexdigest()!=x:out[group].append(p)
json.dump(out,open('/tmp/v28_missing_restore.json','w'))
print('missing by group', {k:len(v) for k,v in out.items()})
