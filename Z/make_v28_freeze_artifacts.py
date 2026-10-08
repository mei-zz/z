from pathlib import Path
import tarfile,shutil,json
proj=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
paths=['HYPERGRAPH_RESEARCH/R_HSPE_FROZEN','HYPERGRAPH_RESEARCH/R_HSPE_FINAL_FROZEN','HYPERGRAPH_RESEARCH/PAPER_PREP/INNOVATION_1_R_HSPE','HYPERGRAPH_RESEARCH/CHRI_V18/SOURCE_HASHES.json']
stage=Path(r'E:\Z\v28_freeze_artifact_stage_20261006');root=stage/'lchr_v2';root.mkdir(parents=True,exist_ok=False)
for rel in paths:
 src=proj/rel;dst=root/rel
 if src.is_dir():shutil.copytree(src,dst)
 elif src.is_file():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
 else:raise FileNotFoundError(src)
arc=Path(r'E:\Z\v28_freeze_artifacts_20261006.tar.gz')
with tarfile.open(arc,'w:gz') as t:t.add(root,arcname='lchr_v2')
print('files',sum(1 for p in root.rglob('*') if p.is_file()),'raw',sum(p.stat().st_size for p in root.rglob('*') if p.is_file()),'archive',arc.stat().st_size)
