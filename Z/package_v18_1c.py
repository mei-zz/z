from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

repo = Path('/home/ubuntu/lchr_v2')
research = repo / 'HYPERGRAPH_RESEARCH/CHRI_V18_1C'
results = repo / 'result/innovation2/CHRI_V18_1C'
target = results / 'CHRI_V18_1C_evidence.zip'
with ZipFile(target, 'w', ZIP_DEFLATED, compresslevel=5) as z:
    for p in results.iterdir():
        if p.is_file() and p.name != target.name:
            z.write(p, p.name)
    for p in (research / 'scripts').glob('*.py'):
        z.write(p, 'scripts/' + p.name)
    for p in research.rglob('*'):
        if p.is_file() and p.suffix in {'.json', '.npz', '.pt'} and 'runs' in p.parts:
            z.write(p, 'runs/' + p.relative_to(research / 'runs').as_posix())
    for p in (research / 'logs').glob('*.log'):
        z.write(p, 'logs/' + p.name)
    for name in ('RUN_STATUS.json', 'supervisor.log'):
        p = research / name
        if p.exists(): z.write(p, name)
print(target, target.stat().st_size)
