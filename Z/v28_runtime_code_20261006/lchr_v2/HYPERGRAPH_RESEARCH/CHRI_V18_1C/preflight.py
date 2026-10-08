"""Freeze identity, runtime and all Phase-A cache/backbone hashes before training."""
import ast, hashlib, json, os, pathlib, subprocess, sys, time

os.environ.setdefault('OMP_NUM_THREADS','2');os.environ.setdefault('MKL_NUM_THREADS','2');os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8');os.environ.setdefault('DGLBACKEND','pytorch')
import numpy as np
import torch

REPO=pathlib.Path('/home/ubuntu/lchr_v2');R=REPO/'HYPERGRAPH_RESEARCH';A=R/'CHRI_V18_1C'
OLD=R/'CHRI_V18';R181=R/'CHRI_V18_1';R18R=R/'CHRI_V18_1R'
def sha(p):
 h=hashlib.sha256()
 with pathlib.Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def funhash(path,container,name):
 text=path.read_text();tree=ast.parse(text)
 cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==container) if container else None
 nodes=cls.body if cls else tree.body
 node=next(n for n in nodes if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name)
 return hashlib.sha256(ast.get_source_segment(text,node).encode()).hexdigest()

torch.use_deterministic_algorithms(True);torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest')
sys.path.insert(0,str(OLD/'scripts'));import chri_v18 as v
v.check_frozen()
assert 'CHRI_KILL' in (REPO/'result/innovation2/CHRI_V18/07_CHRI_DECISION.md').read_text()
assert 'V18_1_REPRODUCTION_MISMATCH' in (REPO/'result/innovation2/CHRI_V18_1/FINAL_REPORT.md').read_text()
assert 'HISTORICAL_ROOT_CAUSE_IDENTIFIED' in (R18R/'FINAL_REPORT.md').read_text()
i1=R/'R_HSPE_FINAL_FROZEN/INNOVATION_1_FINAL.md';assert 'FINAL_FROZEN' in i1.read_text()
agg=R18R/'scripts/deterministic_aggregation.py'
expected='831570b9a4b9ebbb1d52096d832d99033d17c2853dfe812d4738d9e7a5e6adc1'
assert sha(agg)==expected,'V18_1R_AGGREGATION_HASH_MISMATCH'
datasets={};backbones={}
for ds in ('cora','pubmed'):
 datasets[ds]={}
 for seed in (0,1,2):
  src=R181/'cache'/ds/f'seed_{seed}';oldcache=OLD/'cache'/ds/f'seed_{seed}'
  ready=json.loads((src/'B_READY_5.json').read_text());assert ready['state']=='COMPLETE'
  hashes={str(p.relative_to(src)):sha(p) for p in sorted(src.rglob('*')) if p.is_file()}
  old_hashes={str(p.relative_to(oldcache)):sha(p) for p in sorted(oldcache.rglob('*')) if p.is_file()}
  assert hashes==old_hashes, f'V18_CACHE_CLONE_MISMATCH {ds} seed {seed}'
  datasets[ds][str(seed)]={'cache_root':str(src),'cache_file_sha256':hashes,
    'cache_files_identical_to_historical_V18':True,'B_READY_5':ready,
    'split_hashes':{k:v for k,v in hashes.items() if 'split' in k.lower() or 'pair' in k.lower() or 'negative' in k.lower()}}
  cp=v.base_job(ds,seed)/'final.pt';backbones[f'{ds}/seed_{seed}']={'checkpoint_path':str(cp),'sha256':sha(cp),
    'checkpoint_record':v.read(v.base_job(ds,seed)/'result.json')}
v18src=OLD/'scripts/chri_v18.py';features=OLD/'scripts/chri_features.py'
fix_functions={n:funhash(agg,None,n) for n in ('endpoint','representation','install')}
source_files=[v18src,features,agg,R18R/'scripts/corrected_run.py',A/'scripts/canonical_run.py',A/'scripts/supervise.py',A/'scripts/preflight.py',A/'scripts/finalize.py',A/'00_PROTOCOL.md']
source_hashes={str(p.relative_to(REPO)):sha(p) for p in source_files}
fn_hashes={'chri_v18.make_net':funhash(v18src,None,'make_net'),'chri_v18.run':funhash(v18src,None,'run'),
 'chri_v18.evaluate':funhash(v18src,None,'evaluate'),
 'RelationPredictor.endpoint':funhash(features,'RelationPredictor','endpoint'),
 'RelationPredictor.representation':funhash(features,'RelationPredictor','representation'),
 'RelationPredictor.forward':funhash(features,'RelationPredictor','forward'),**{f'deterministic_aggregation.{k}':x for k,x in fix_functions.items()}}
gpu=subprocess.run(['nvidia-smi','--query-gpu=name,uuid,memory.total,driver_version','--format=csv,noheader'],capture_output=True,text=True,check=True).stdout.strip()
data={'state':'FROZEN_BEFORE_TRAINING','canonical_protocol':'CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1',
 'workspace':'DCDLP-main','server_checkout':str(REPO),'historical_states':{'V18':'CHRI_KILL / CHRI_TRANSFER_WEAK','V18.1':'V18_1_REPRODUCTION_MISMATCH','V18.1R':'HISTORICAL_ROOT_CAUSE_IDENTIFIED'},
 'historical_artifacts_modified':False,'innovation1_status':'FINAL_FROZEN','test_accessed':False,
 'arm_mapping':{'A0':'V18 implementation A1: Z only','A1':'V18 implementation A2: Z + RAW R_CAT',
  'A2':'V18 implementation A3: Z + matched SHUFFLE R_CAT','A3':'V18 implementation A4: Z + parameter-matched NULL'},
 'epochs':5,'datasets':['cora','pubmed'],'seeds':[0,1,2],'duplicate_executions_per_cell':2,
 'paired_training_trace':'V18 B_READY_5 trace and epoch candidate/negative/permutation cache are shared across arms; arm-specific initialization streams are frozen in V18 code.',
 'deterministic_implementation':{'file':str(agg.relative_to(REPO)),'sha256':sha(agg),'matches_V18_1R_verified_hash':sha(agg)==expected,'functions':fix_functions},
 'source_sha256':source_hashes,'function_sha256':fn_hashes,
 'runtime':{'python':sys.version,'pytorch':torch.__version__,'torch_cuda':torch.version.cuda,'cudnn':torch.backends.cudnn.version(),
  'gpu':gpu,'deterministic_algorithms':torch.are_deterministic_algorithms_enabled(),'cudnn_deterministic':torch.backends.cudnn.deterministic,
  'cudnn_benchmark':torch.backends.cudnn.benchmark,'cuda_matmul_tf32':torch.backends.cuda.matmul.allow_tf32,
  'cudnn_tf32':torch.backends.cudnn.allow_tf32,'float32_matmul_precision':torch.get_float32_matmul_precision(),
  'CUBLAS_WORKSPACE_CONFIG':os.environ['CUBLAS_WORKSPACE_CONFIG'],'OMP_NUM_THREADS':os.environ['OMP_NUM_THREADS'],
  'MKL_NUM_THREADS':os.environ['MKL_NUM_THREADS'],'OPENBLAS_NUM_THREADS':os.environ['OPENBLAS_NUM_THREADS']},
 'training_config':{ds:{'learning_rate':v.b.NCFG[ds]['prelr'],'batch_size':v.b.NCFG[ds]['batch'],'optimizer':'Adam','weight_decay':0,'epochs':5} for ds in ('cora','pubmed')},
 'frozen_backbone_checkpoint_sha256':backbones,'feature_caches':datasets,
 'historical_V18_numerical_reproduction_claim':False}
(A/'01_CANONICAL_IMPLEMENTATION.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
print(json.dumps({'state':data['state'],'fix_sha256':sha(agg),'cache_seeds':12,'backbones':len(backbones),'test_accessed':False},indent=2))
