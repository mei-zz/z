import json,pathlib,hashlib,os
r=pathlib.Path('/home/ubuntu/lchr_v2'); a=r/'result/innovation2/TOPOLOGY_V28'
h=json.load(open(a/'SOURCE_HASHES.json'))
missing=[];bad=[];sizes=0
for group in ('files','historical_topology_caches'):
 for p,x in h[group].items():
  q=r/p
  if not q.is_file():missing.append((group,p));continue
  if hashlib.sha256(q.read_bytes()).hexdigest()!=x:bad.append((group,p))
print('missing',len(missing),'bad',len(bad))
for k,p in missing: print(k,p)
for k,p in bad: print('BAD',k,p)
