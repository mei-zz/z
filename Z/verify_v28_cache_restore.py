import json,pathlib,hashlib
r=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
h=json.load(open(r/'result/innovation2/TOPOLOGY_V28/SOURCE_HASHES.json'))
base=pathlib.Path(r'E:\Z\v28_cache_extract\lchr_v2')
missing=[];bad=[];total=0
for p,x in h['historical_topology_caches'].items():
 q=base/p
 if not q.exists():missing.append(p);continue
 total+=q.stat().st_size
 if hashlib.sha256(q.read_bytes()).hexdigest()!=x:bad.append(p)
print('restored',len(h['historical_topology_caches'])-len(missing),'missing',len(missing),'bad',len(bad),'bytes',total)
print('examples',missing[:3],bad[:3])
