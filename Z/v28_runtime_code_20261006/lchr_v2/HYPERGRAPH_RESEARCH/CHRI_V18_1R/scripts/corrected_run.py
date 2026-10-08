import json,pathlib,sys,torch
repo=pathlib.Path('/home/ubuntu/lchr_v2');research=repo/'HYPERGRAPH_RESEARCH';audit=research/'CHRI_V18_1R';out=pathlib.Path(__import__('os').environ.get('CHRI_CORRECTED_OUT',str(audit/'runA')));old=research/'CHRI_V18'
sys.path.insert(0,str(old/'scripts'));import chri_v18 as v
sys.path.insert(0,str(audit/'scripts'));from deterministic_aggregation import install
v.OUT=out;torch.set_num_threads(4);torch.use_deterministic_algorithms(True);torch.backends.cudnn.deterministic=True;torch.backends.cudnn.benchmark=False;torch.backends.cuda.matmul.allow_tf32=False;torch.backends.cudnn.allow_tf32=False;torch.set_float32_matmul_precision('highest')
original=v.make_net
def deterministic_make(*a,**kw):return install(original(*a,**kw))
v.make_net=deterministic_make
ds,seed,arm=sys.argv[1],int(sys.argv[2]),sys.argv[3]
assert ds in ('cora','pubmed') and seed in (0,1,2) and arm in ('A1','A2','A3')
v.run('A',ds,seed,arm,5)
p=v.job('A',ds,seed,arm)/'result.json';r=v.read(p);r.update({'corrected_aggregation':'V18_1R deterministic contiguous-segment sum/mean/max','strict_deterministic_algorithms':True,'CUBLAS_WORKSPACE_CONFIG':':4096:8','test_accessed':False});v.write(p,r)
print('CORRECTED_RUN_COMPLETE',ds,seed,arm,r['validation']['ce'],r['validation']['mrr'],r['checkpoint_sha256'],flush=True)

