import sys
import numpy as np
sys.path.insert(0, r'E:\\我的资料库\\Documents\\Downloads\\DCDLP-main\\HYPERGRAPH_RESEARCH\\QTHS_V7_1')
import experiment_v71 as e
rng=np.random.default_rng(1); n=18; nodes=60
pool=np.empty((n,20,2),dtype=np.int64)
for i in range(n):
    pairs=set()
    while len(pairs)<20:
        a,b=map(int,rng.choice(nodes,2,replace=False)); pairs.add(tuple(sorted((a,b))))
    pool[i]=np.array(sorted(pairs),dtype=np.int64)
scores=rng.random((n,20)).astype(np.float32)
pos=np.array([[i,(i+30)%nodes] for i in range(n)],dtype=np.int64)
degree=rng.integers(0,12,size=nodes)
ids,_=e.v7.make_ids(pool,scores,pos,.25); q=pool[np.arange(n),ids]
h,hm=e.build_hmc(pool,scores,pos,ids,0)
d,dm=e.build_dmc(pool,scores,pos,q,degree,0)
stats=e.v7.summarize(pool,scores,q,degree)
counts=np.bincount(q.ravel(),minlength=nodes)
print('gini',e.gini_from_histogram(np.bincount(counts),nodes,2*n),e.v7.gini(counts))
print('hmc',hm['absolute_quantile_error_sum'],'dmc',dm['matched_diversity_and_hardness'],'target',stats['unique_endpoint_ratio'],stats['endpoint_gini'],stats['hub_endpoint_ratio'])
high=np.arange(n)%2==1; sel,meta=e.adaptive_selector(pool,scores,pos,high,'test',0)
print('adaptive',sel.shape,meta['groups'])
