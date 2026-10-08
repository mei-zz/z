from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path('/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/CHRI_V18_1R')
target = root / 'CHRI_V18_1R_evidence.zip'
with ZipFile(target, 'w', ZIP_DEFLATED, compresslevel=6) as z:
    def add(path):
        z.write(path, path.relative_to(root.parent))
    for p in root.iterdir():
        if p.is_file() and (p.suffix in {'.json', '.md', '.log'}): add(p)
    for p in (root / 'scripts').glob('*.py'): add(p)
    for name in ('runA/state_trace.json', 'runB/state_trace.json',
                 'runC_patch/state_trace.json', 'runD_patch/state_trace.json'):
        p = root / name
        if p.exists(): add(p)
    for name in ('runA/runs/A', 'runB/runs/A'):
        base = root / name
        if base.exists():
            for p in base.rglob('*'):
                if p.is_file() and p.suffix in {'.json', '.npz', '.pt'}: add(p)
    base = root / 'arm_order_runs'
    if base.exists():
        for p in base.rglob('*'):
            if p.is_file() and p.suffix in {'.json', '.npz', '.pt'}: add(p)
    for p in (root / 'arm_order_logs').glob('*.log'):
        add(p)
    for folder in ('corrected_logs', 'cora_repeat_logs'):
        base = root / folder
        if base.exists():
            for p in base.glob('*.log'): add(p)
print(target, target.stat().st_size)
