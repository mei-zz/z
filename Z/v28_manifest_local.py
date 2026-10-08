import json,pathlib,hashlib
r=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
h=json.load(open(r/'result/innovation2/TOPOLOGY_V28/SOURCE_HASHES.json'))
missing=[];bad=[];tot=0
for p,x in h['files'].items():
 q=r/p
 if not q.exists(): missing.append(p)
 elif q.is_file():
  d=hashlib.sha256(q.read_bytes()).hexdigest()
  if d!=x: bad.append(p)
  tot+=q.stat().st_size
print('files',len(h['files']),'missing',len(missing),'bad',len(bad),'bytes existing',tot)
print('missing sample',missing[:40]);print('bad',bad[:5])
