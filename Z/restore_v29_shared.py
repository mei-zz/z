from pathlib import Path
import json,tarfile,hashlib,time
data=json.loads(Path(r'E:\Z\result\innovation2\TOPOLOGY_V28\06_PHASE_A_METRICS.json').read_text(encoding='utf-8-sig'))
want={};reference={}
for ds,values in data['datasets'].items():
 for row in values['seed_results']:
  record=row['arms']['SHARED'];folder=Path(record['checkpoint'].replace('/home/ubuntu/','')).parent.as_posix()
  for name in ('final.pt','valid_epoch5_scores.npz','result.json'):want[folder+'/'+name]=record
stage=Path(r'E:\Z\v29_shared_restore');found=[];last=time.time()
for ds in ('cora','pubmed'):
 want[f'lchr_v2/HYPERGRAPH_RESEARCH/R_HSPE_BENCHMARK_V17_3/input_cache/{ds}.npz']=None
with tarfile.open(r'E:\Z\DCDLP_Server_Backup_20261005\lchr_v2_full_server_backup.tar.gz','r|gz') as arc:
 for member in arc:
  if member.isfile() and member.name in want:
   content=arc.extractfile(member).read();record=want.pop(member.name)
   if member.name.endswith('/final.pt'):assert hashlib.sha256(content).hexdigest()==record['checkpoint_sha256']
   out=stage/member.name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(content);found.append(member.name)
   print('restored',len(found),'of18',flush=True)
  if not want:break
  if time.time()-last>30:print('archive scan',len(found),'of18',flush=True);last=time.time()
assert not want,'Missing '+str(list(want))
with tarfile.open(r'E:\Z\v29_shared_restore.tar.gz','w:gz') as arc:
 for path in found:arc.add(stage/path,arcname=path,recursive=False)
print('SHARED_RESTORE_COMPLETE',len(found),flush=True)
