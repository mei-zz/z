import json,pathlib,hashlib,shutil,subprocess,sys
project=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
manifest=json.load(open(project/'result/innovation2/TOPOLOGY_V28/SOURCE_HASHES.json'))
missing=json.load(open(r'E:\Z\v28_missing_restore.json'))
stage=pathlib.Path(r'E:\Z\v28_restore_stage'); shutil.rmtree(stage,ignore_errors=True)
root=stage/'lchr_v2'; srcroot=pathlib.Path(r'E:\Z\v28_cache_extract\lchr_v2')
items=[]
for p in missing['files']:
 src=project/p
 if not src.is_file(): src=srcroot/p
 if not src.is_file(): raise FileNotFoundError(src)
 if hashlib.sha256(src.read_bytes()).hexdigest()!=manifest['files'][p]: raise ValueError('HASH '+p)
 items.append((p,src))
for p in missing['historical_topology_caches']:
 src=srcroot/p
 if not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest()!=manifest['historical_topology_caches'][p]: raise ValueError('CACHE '+p)
 items.append((p,src))
for p,src in items:
 dst=root/p; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
arc=pathlib.Path(r'E:\Z\v28_restore_missing.tar.gz')
if arc.exists():arc.unlink()
subprocess.run(['tar','-czf',str(arc),'-C',str(stage),'lchr_v2'],check=True)
print('files',len(items),'uncompressed',sum(x.stat().st_size for x in root.rglob('*') if x.is_file()),'archive',arc.stat().st_size)
