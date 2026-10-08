import tarfile,json,hashlib,pathlib,time
backup=pathlib.Path(r'E:\Z\DCDLP_Server_Backup_20261005\lchr_v2_full_server_backup.tar.gz')
dest=pathlib.Path(r'E:\Z\v29_prerequisite_restore')
prefixes=(
 'lchr_v2/HYPERGRAPH_RESEARCH/CHRI_V18_1/cache/pubmed/seed_0/',
 'lchr_v2/HYPERGRAPH_RESEARCH/R_HSPE_STRONG_BACKBONE_V17_4/phases/B/pubmed/seed_0/C0/',
 'lchr_v2/HYPERGRAPH_RESEARCH/ERDR_V21/context_cache/',
)
found=[];last=time.time()
with tarfile.open(backup,'r|gz') as arc:
 for member in arc:
  if member.isfile() and member.name.startswith(prefixes):
   # Only first five scheduled epochs are needed; retain normalization/donors.
   leaf=pathlib.PurePosixPath(member.name).name
   if leaf.startswith('epoch_'):
    try:
     epoch=int(leaf.split('_')[1].split('.')[0])
     if epoch>5:continue
    except ValueError:pass
   if member.name.endswith('.npz') and '/context_cache/' not in member.name and '/C0/' not in member.name:
    continue
   out=dest/pathlib.PurePosixPath(member.name);out.parent.mkdir(parents=True,exist_ok=True)
   with arc.extractfile(member) as src,out.open('wb') as sink:
    for chunk in iter(lambda:src.read(1024*1024),b''):sink.write(chunk)
   found.append({'path':member.name,'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
  if time.time()-last>30:print('scan ongoing; restored files',len(found),flush=True);last=time.time()
dest.mkdir(parents=True,exist_ok=True)
(dest/'MANIFEST.json').write_text(json.dumps(found,indent=2))
print('RESTORED',len(found),'BYTES',sum(x['bytes'] for x in found),flush=True)
output=pathlib.Path(r'E:\Z\v29_prerequisites.tar.gz')
with tarfile.open(output,'w:gz',compresslevel=1) as arc:
 for record in found:arc.add(dest/record['path'],arcname=record['path'],recursive=False)
print('ARCHIVE',output.stat().st_size,flush=True)
