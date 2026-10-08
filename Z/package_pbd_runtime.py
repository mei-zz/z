import tarfile,json,hashlib
from pathlib import Path
import numpy as np
root=Path('/home/ubuntu/lchr_v2');files=set()
for q in root.rglob('*.py'):
    rel=q.relative_to(root)
    if any(part in ('.git','__pycache__','numba_cache','wheelhouse') for part in rel.parts):continue
    files.add(q)
for folder in ('configs','HYPERGRAPH_RESEARCH/HMC_V15/runtime/configs','HYPERGRAPH_RESEARCH/R_HSPE_FROZEN','HYPERGRAPH_RESEARCH/R_HSPE_FINAL_FROZEN'):
    for q in (root/folder).rglob('*'):
        if q.is_file() and q.suffix in ('.json','.yaml','.yml','.md','.py'):files.add(q)
for q in root.rglob('config.json'):
    if '/H/' in str(q) or '/BASELINE/' in str(q):files.add(q)
for rel in ('HYPERGRAPH_RESEARCH/R_HSPE_STRONG_BACKBONE_V17_4/AUDIT.json','HYPERGRAPH_RESEARCH/R_HSPE_STRONG_BACKBONE_V17_4/SOURCE_HASHES.json'):
    if (root/rel).exists():files.add(root/rel)
for ds in ('cora','pubmed'):
    for rel in ('HYPERGRAPH_RESEARCH/PAPER_SPRINT_01/data/SCREEN/'+ds,'HYPERGRAPH_RESEARCH/DA_NBR_V30A/paths/SCREEN/'+ds):
        files.update(q for q in (root/rel).iterdir() if q.is_file())
    source=root/'HYPERGRAPH_RESEARCH/R_HSPE_BENCHMARK_V17_3/input_cache'/f'{ds}.npz'
    dest=root/'HYPERGRAPH_RESEARCH/PBD_V30B/sealed_inputs'/f'{ds}.npz';dest.parent.mkdir(parents=True,exist_ok=True)
    with np.load(source) as z:np.savez_compressed(dest,**{k:z[k] for k in ('x','train','valid_pos','valid_neg')})
    files.add(dest)
# Seal a complete transport manifest; archive only, no existing source writes.
manifest={str(q.relative_to(root)):hashlib.sha256(q.read_bytes()).hexdigest() for q in sorted(files)}
dest=Path('/tmp/PBD_V30B_RUNTIME.tar.gz')
with tarfile.open(dest,'w:gz') as tar:
    for q in sorted(files):tar.add(q,arcname=str(q.relative_to(root)),recursive=False)
manifest_path=Path('/tmp/PBD_V30B_TRANSPORT_MANIFEST.json');manifest_path.write_text(json.dumps(manifest,indent=2))
print('TRANSPORT_READY',len(files),dest.stat().st_size)
