from pathlib import Path
import hashlib,tarfile
for p in [Path(r'E:\Z\DCDLP_Server_Backup_20261005\V28_inner_experiment_20261006.tar.gz'),Path(r'E:\Z\DCDLP_Server_Backup_20261005\V28_final_review_update_20261006.tar.gz')]:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 print(p.name,h.hexdigest(),p.stat().st_size)
 with tarfile.open(p,'r:gz') as t:print('members',len(t.getmembers()))
