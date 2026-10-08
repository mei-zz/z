from pathlib import Path
b=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\HYPERGRAPH_RESEARCH')
files=[p for p in b.rglob('*.py') if '__pycache__' not in p.parts]
print('python files',len(files),'bytes',sum(p.stat().st_size for p in files))
for p in files:
 if p.parent.name=='scripts' and p.name in ('experiment_v71.py','run_negative_v6_1.py','train_hardness_v7.py','run_codns_v6_2.py','hspe_v17.py','hspe_v17_1.py','hspe_v17_2.py','benchmark173.py','strong174.py'): print(p.relative_to(b),p.stat().st_size)
