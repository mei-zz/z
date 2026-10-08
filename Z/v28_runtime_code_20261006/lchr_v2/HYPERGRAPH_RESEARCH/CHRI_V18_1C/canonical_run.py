"""One fresh deterministic Phase-A V18.1C run; underlying V18 arm labels are mapped here."""
import hashlib, json, os, pathlib, sys
import numpy as np
import torch

REPO = pathlib.Path('/home/ubuntu/lchr_v2')
RESEARCH = REPO / 'HYPERGRAPH_RESEARCH'
AUDIT = RESEARCH / 'CHRI_V18_1C'
V18R = RESEARCH / 'CHRI_V18_1R'
EXPECTED_AGGREGATION_SHA256 = '831570b9a4b9ebbb1d52096d832d99033d17c2853dfe812d4738d9e7a5e6adc1'
CANONICAL_TO_V18 = {'A0':'A1', 'A1':'A2', 'A2':'A3', 'A3':'A4'}

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()

def score_hash(path):
    with np.load(path) as z:
        h=hashlib.sha256()
        for key in ('positive','negative'):
            x=np.ascontiguousarray(z[key])
            h.update(key.encode());h.update(str(x.shape).encode());h.update(str(x.dtype).encode());h.update(x.tobytes())
        return h.hexdigest()

assert len(sys.argv)==5, 'usage: canonical_run.py DATASET SEED CANONICAL_ARM OUTPUT_DIR'
ds,seed_text,canonical_arm,out_text=sys.argv[1:]
seed=int(seed_text);out=pathlib.Path(out_text)
assert ds in ('cora','pubmed') and seed in (0,1,2) and canonical_arm in CANONICAL_TO_V18
assert sha(V18R/'scripts/deterministic_aggregation.py')==EXPECTED_AGGREGATION_SHA256, 'DETERMINISTIC_AGGREGATION_HASH_MISMATCH'
os.environ.setdefault('OMP_NUM_THREADS','2');os.environ.setdefault('MKL_NUM_THREADS','2');os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('CUBLAS_WORKSPACE_CONFIG',':4096:8')
torch.set_num_threads(int(os.environ['OMP_NUM_THREADS']))
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False
torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False
torch.set_float32_matmul_precision('highest')
assert torch.cuda.is_available(), 'CUDA_REQUIRED'
assert out.is_dir() and (out/'cache').exists() and (out/'scripts').exists() and (out/'SOURCE_HASHES.json').is_file()
sys.path.insert(0,str(RESEARCH/'CHRI_V18/scripts'))
import chri_v18 as v
sys.path.insert(0,str(V18R/'scripts'))
from deterministic_aggregation import install
v.OUT=out
original_make=v.make_net
def deterministic_make(*args,**kwargs):
    return install(original_make(*args,**kwargs))
v.make_net=deterministic_make
v.run('A',ds,seed,CANONICAL_TO_V18[canonical_arm],5)
run_dir=v.job('A',ds,seed,CANONICAL_TO_V18[canonical_arm])
result=v.read(run_dir/'result.json')
scores_path=run_dir/'valid_epoch5_scores.npz'
result.update({'canonical_protocol':'CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1',
               'canonical_arm':canonical_arm,'implementation_arm':CANONICAL_TO_V18[canonical_arm],
               'deterministic_aggregation_sha256':EXPECTED_AGGREGATION_SHA256,
               'strict_deterministic_algorithms':True,
               'CUBLAS_WORKSPACE_CONFIG':os.environ['CUBLAS_WORKSPACE_CONFIG'],
               'torch_version':torch.__version__,'torch_cuda_version':torch.version.cuda,
               'score_vector_sha256':score_hash(scores_path),'test_accessed':False})
v.write(run_dir/'result.json',result)
print(json.dumps({'state':'COMPLETE','dataset':ds,'seed':seed,'canonical_arm':canonical_arm,
                  'implementation_arm':CANONICAL_TO_V18[canonical_arm],
                  'checkpoint_sha256':result['checkpoint_sha256'],
                  'score_vector_sha256':result['score_vector_sha256'],
                  'validation':result['validation'],'test_accessed':False},sort_keys=True),flush=True)
