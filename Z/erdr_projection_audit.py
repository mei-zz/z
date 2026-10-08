import os
os.environ['CUBLAS_WORKSPACE_CONFIG']=':4096:8'
import sys,json,hashlib
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits,threadpool_info
R=Path('/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH')
sys.path.insert(0,str(R/'ERDR_V21/scripts'));import erdr21 as e
for ds in ('cora','pubmed'):
 a=e.sealed(ds)
 with np.load(R/'CHRI_V18_1/cache'/ds/'structure.npz') as z:p=z['projection'];mu=z['normalization_mean'];std=z['normalization_std']
 target=e.read(R/'CHRI_V18_1/cache'/ds/'STRUCTURE_READY.json')['projected_node_hash']
 for threads in (1,2,4,8,16,24,32,40):
  with threadpool_limits(limits=threads,user_api='blas'):
   node=(np.asarray(a['x']@p,np.float32)-mu)/std
  from chri_features import array_hash
  print(ds,threads,str(a['x'].dtype),str(p.dtype),array_hash(node),array_hash(node)==target,flush=True)
