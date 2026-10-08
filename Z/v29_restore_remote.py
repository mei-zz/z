import tarfile,json,hashlib,os,uuid
from pathlib import Path
repo=Path('/home/ubuntu/lchr_v2');records=[]
with tarfile.open('/tmp/v29_prerequisites.tar.gz','r:gz') as arc:
 for m in arc:
  assert m.isfile() and m.name.startswith('lchr_v2/')
  out=repo/Path(m.name).relative_to('lchr_v2');out=out.resolve()
  assert out.is_relative_to(repo.resolve())
  contents=arc.extractfile(m).read();digest=hashlib.sha256(contents).hexdigest()
  if out.exists():
   assert hashlib.sha256(out.read_bytes()).hexdigest()==digest,'Existing historical content differs: '+str(out)
   restored=False
  else:
   out.parent.mkdir(parents=True,exist_ok=True);temp=out.with_name(out.name+'.restore-'+uuid.uuid4().hex);temp.write_bytes(contents);os.replace(temp,out);restored=True
  records.append({'path':str(out.relative_to(repo)),'bytes':len(contents),'sha256':digest,'restored_from_verified_local_backup':restored})
p=repo/'result/innovation2/HDP_ZERO_V29/PREREQUISITE_RESTORE_AUDIT.json'
old=json.loads(p.read_text()) if p.exists() else []
merged={x['path']:x for x in old}
merged.update({x['path']:x for x in records});p.write_text(json.dumps(list(merged.values()),indent=2))
print('RESTORED_VERIFIED',len(records),'files',sum(x['bytes'] for x in records),'bytes')
# Archive is only a transport duplicate; local source/backup and restored copies retained.
Path('/tmp/v29_prerequisites.tar.gz').unlink()
import sys
sys.path.insert(0,str(repo/'HYPERGRAPH_RESEARCH/TOPOLOGY_V28/scripts'))
import topology28 as t
missing=[]
for ds in ('cora','pubmed'):
 for seed in range(3):
  for arm in ('SHARED','GM','GMH','GMS','GMP','GMG','GDUP'):
   ref=json.loads((repo/'result/innovation2/TOPOLOGY_V28/06_PHASE_A_METRICS.json').read_text())
   path=Path(ref['datasets'][ds]['seed_results'][seed]['arms'][arm]['checkpoint']).parent if arm=='SHARED' else t.dest('A',ds,seed,arm)
   for name in ('final.pt','valid_epoch5_scores.npz','result.json'):
    f=path/name
    if not f.exists():missing.append(str(f.relative_to(repo)))
print('MISSING_HISTORICAL',json.dumps(missing))
