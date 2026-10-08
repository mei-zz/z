import json, pathlib, os, tarfile
root=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
art=root/'result/innovation2/TOPOLOGY_V28'
h=json.load(open(art/'SOURCE_HASHES.json'))
print('historical entries',len(h['historical_topology_caches']))
for p in list(h['historical_topology_caches'])[:8]:
 q=root/p
 print('local',q.exists(), q.stat().st_size if q.is_file() and q.exists() else 0,p)
arc=pathlib.Path(r'E:\Z\DCDLP_Server_Backup_20261005\lchr_v2_full_server_backup.tar.gz')
print('archive exists,size',arc.exists(),arc.stat().st_size)
if arc.exists():
 total=0; miss=[]; n=0
 want=set(h['historical_topology_caches'])
 with tarfile.open(arc,'r:gz') as t:
  for m in t:
   name=m.name[2:] if m.name.startswith('./') else m.name
   if name in want or name.startswith('lchr_v2/') and name.split('lchr_v2/',1)[1] in want:
    total+=m.size;n+=1;want.discard(name.split('lchr_v2/',1)[-1])
 print('archive matched',n,'bytes',total,'unmatched',len(want),list(want)[:4])
