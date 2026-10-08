import json,pathlib,hashlib,importlib.util,sys
root=pathlib.Path('/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH');out=root/'HSPE_V17_2'
sp=importlib.util.spec_from_file_location('v172',out/'scripts/hspe_v17_2.py');m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
manifest=m.read(out/'SOURCE_HASHES.json');runtime=m.m.p.v16.ROOT
files={str(p):m.m.p.sha256_file(p) for p in (runtime/'src').rglob('*.py')}
manifest['runtime_python_source_hashes']=files
manifest['runtime_source_manifest_sha256']=m.digest(files)
splits={}
for ds in ('cora','pubmed','citeseer'):
 full,view=m.m.p.v16.base.init_dataset(ds)
 rec={'train_positive':m.m.p.v16.v61.array_hash(view.train_pos),'valid_positive':m.m.p.v16.v61.array_hash(full.valid_pos),'training_view_split_hash':m.m.p.v16.base.split_hash(view)}
 if ds!='citeseer':rec['test_positive']=m.m.p.v16.v61.array_hash(full.test_pos)
 else:rec['test_identities_opened']=False
 splits[ds]=rec
manifest['dataset_split_hashes']=splits
m.write(out/'SOURCE_HASHES.json',manifest)
print(json.dumps({'runtime_source_files':len(files),'dataset_splits':splits},indent=2))
