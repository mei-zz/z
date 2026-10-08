from pathlib import Path
base=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\HYPERGRAPH_RESEARCH')
for n in ['R_HSPE_STRONG_BACKBONE_V17_4','R_HSPE_BENCHMARK_V17_3','HSPE_V17_2','NHMC_V16','R_HSPE_FROZEN','QTHS_V7_1','CHRI_V18']:
 p=base/n
 for sub in ['scripts','.deps']:
  q=p/sub
  if q.exists():print(n,sub,sum(x.stat().st_size for x in q.rglob('*') if x.is_file()),len([x for x in q.rglob('*') if x.is_file()]))
