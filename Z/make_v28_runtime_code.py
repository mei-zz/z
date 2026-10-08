from pathlib import Path
import shutil,tarfile
proj=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
stage=Path(r'E:\Z\v28_runtime_code_20261006')
root=stage/'lchr_v2'
root.mkdir(parents=True,exist_ok=False)
base=proj/'HYPERGRAPH_RESEARCH'
files=list(base.rglob('*.py'))
for src in files:
 rel=src.relative_to(proj);dst=root/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
arc=Path(r'E:\Z\v28_runtime_code_20261006.tar.gz')
with tarfile.open(arc,'w:gz') as t:t.add(root,arcname='lchr_v2')
print('py',len(files),'raw',sum(x.stat().st_size for x in root.rglob('*.py')),'archive',arc.stat().st_size)
