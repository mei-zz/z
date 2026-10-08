from pathlib import Path
r=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\HYPERGRAPH_RESEARCH')
for rel in ['R_HSPE_FROZEN','R_HSPE_FINAL_FROZEN','PAPER_PREP/INNOVATION_1_R_HSPE','CHRI_V18','R_HSPE_BENCHMARK_V17_3','HSPE_V17_2','HSPE_V17_1','HSPE_V17']:
 p=r/rel; fs=[x for x in p.rglob('*') if x.is_file()] if p.exists() else []
 print(rel,'exists',p.exists(),'files',len(fs),'GB',sum(x.stat().st_size for x in fs)/1e9)
 if rel in ['R_HSPE_FROZEN','R_HSPE_FINAL_FROZEN','PAPER_PREP/INNOVATION_1_R_HSPE']:print('  sample',[str(x.relative_to(p)) for x in fs[:8]])
