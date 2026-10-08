from pathlib import Path
import tarfile,shutil
proj=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main');rel=Path('HYPERGRAPH_RESEARCH/CHRI_V18_1/SOURCE_HASHES.json')
stage=Path(r'E:\Z\v28_chri_manifest_20261006');dst=stage/'lchr_v2'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(proj/rel,dst)
with tarfile.open(r'E:\Z\v28_chri_manifest_20261006.tar.gz','w:gz') as t:t.add(stage/'lchr_v2',arcname='lchr_v2')
