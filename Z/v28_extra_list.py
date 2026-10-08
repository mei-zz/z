import json,pathlib
r=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
h=json.load(open(r/'result/innovation2/TOPOLOGY_V28/SOURCE_HASHES.json'))
out=pathlib.Path(r'E:\Z\v28_extra_archive_paths.txt')
missing=[p for p in h['files'] if not (r/p).is_file()]
out.write_text('\n'.join('lchr_v2/'+p for p in missing),encoding='utf-8')
print(len(missing),*missing,sep='\n')
