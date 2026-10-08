import json,pathlib
r=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
h=json.load(open(r/'result/innovation2/TOPOLOGY_V28/SOURCE_HASHES.json'))
out=pathlib.Path(r'E:\Z\v28_tar_paths.txt')
out.write_text('\n'.join('lchr_v2/'+p for p in h['historical_topology_caches']),encoding='utf-8')
print('wrote',len(h['historical_topology_caches']),out.stat().st_size)
