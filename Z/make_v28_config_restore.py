from pathlib import Path
import tarfile
proj=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
rel=Path('HYPERGRAPH_RESEARCH/COMPLEMENT_V5/A_GHHR/remote_evidence/baseline_10_epoch/H/config.json')
stage=Path(r'E:\Z\v28_config_restore_20261006');p=stage/'lchr_v2'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((proj/rel).read_bytes())
with tarfile.open(r'E:\Z\v28_config_restore_20261006.tar.gz','w:gz') as t:t.add(stage/'lchr_v2',arcname='lchr_v2')
print('archive ready')
