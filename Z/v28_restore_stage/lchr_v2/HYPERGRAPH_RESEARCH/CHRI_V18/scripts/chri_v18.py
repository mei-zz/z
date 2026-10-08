from __future__ import annotations

import os
for _key in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_key, '4')
os.environ.setdefault('DGLBACKEND', 'pytorch')

import copy
import gc
import hashlib
import importlib.util
import json
import random
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import torch
from scipy.spatial import cKDTree
from sklearn.decomposition import PCA
from sklearn.metrics import roc_auc_score

from chri_features import Structure, RelationPredictor, build_structure, heuristic_rows, array_hash

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parent
REPO = ROOT.parent
STRONG = ROOT / 'R_HSPE_STRONG_BACKBONE_V17_4'
CANONICAL = ROOT / 'R_HSPE_FINAL_FROZEN'
spec = importlib.util.spec_from_file_location('chri_frozen174', STRONG / 'scripts/strong174.py')
s = importlib.util.module_from_spec(spec); sys.modules[spec.name] = s; spec.loader.exec_module(s)
b = s.b
torch.set_num_threads(int(os.environ['OMP_NUM_THREADS']))
ARMS = ('A1', 'A2', 'A3', 'A4')
MODULE_ARMS = ('M0', 'M1', 'M2', 'M3', 'M4')
METRICS = ('ce', 'mrr', 'hits10', 'hits20', 'auc')
ARTIFACTS = ('03_PHASE_A_RESULTS.json', '04_PHASE_B_RESULTS.json',
             '05_CONDITIONAL_RELATION_DIAGNOSTIC.json', '06_MATCHED_HARD_DIAGNOSTIC.json',
             '08_CRIB_RESULTS.json', '09_I1_I2_ORTHOGONALITY.json', '10_TEST_RESULTS.json', '11_THIRD_DATASET.json')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, indent=2, allow_nan=False), encoding='utf-8')
    os.replace(temporary, path)


def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def hash_state(module):
    h=hashlib.sha256()
    for key,value in module.state_dict().items():
        h.update(key.encode()); h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def cache(ds, seed=None):
    p=OUT/'cache'/ds
    if seed is not None:p=p/f'seed_{seed}'
    p.mkdir(parents=True, exist_ok=True)
    return p


def job(phase, ds, seed, arm):
    return OUT/'runs'/phase/ds/f'seed_{seed}'/arm


def base_job(ds, seed, arm='C0'):
    phase='third' if ds=='citeseer' else 'B'
    return STRONG/'phases'/phase/ds/f'seed_{seed}'/arm


def sealed_input(ds, test=False):
    if test:
        gate=read(OUT/'TEST_UNSEAL.json')
        assert gate['allowed'] and gate['phenomenon'] and gate['i2_complement_to_i1']
        if ds=='citeseer':assert read(OUT/'11_THIRD_DATASET.json')['validation_pass']
    return s.input_data(ds, test)


def frozen_snapshot():
    files={}
    for folder in (CANONICAL, ROOT/'PAPER_PREP/INNOVATION_1_R_HSPE', ROOT/'R_HSPE_FROZEN'):
        assert folder.is_dir(), f'MISSING_FROZEN_FOLDER: {folder}'
        for p in folder.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                files[str(p.relative_to(REPO))]=sha(p)
    return files


def check_frozen():
    s.assert_frozen()
    expected=read(OUT/'SOURCE_HASHES.json')['innovation1_files']
    for p,h in expected.items():assert sha(REPO/p)==h, f'INNOVATION1_MODIFIED: {p}'
    for p,h in read(OUT/'SOURCE_HASHES.json')['v18_source_files'].items():
        assert sha(OUT/p)==h, f'V18_PREREGISTERED_SOURCE_CHANGED: {p}'


def preflight():
    assert REPO.name in ('DCDLP-main','lchr_v2'), 'WORKSPACE_MISMATCH'
    # The historical server checkout is named lchr_v2; identity uses the same audited sources.
    definition=(CANONICAL/'INNOVATION_1_FINAL.md').read_text()
    for text in ('FINAL_FROZEN','75','CONTEXT_DRIVEN','NOT_SUPPORTED'):
        assert text in definition
    s.assert_frozen()
    files=frozen_snapshot()
    source={str(p.relative_to(OUT)):sha(p) for p in (OUT/'scripts').glob('*.py')}
    manifest={'state':'FROZEN_BEFORE_RUN','workspace':'DCDLP-main', 'server_checkout':str(REPO),
              'innovation1_files':files,'v18_source_files':source,
              'protocol_sha256':sha(OUT/'00_PROTOCOL.md'),
              'backbone_adapter_sha256':sha(STRONG/'scripts/strong174.py'),
              'official_model_sha256':sha(next((b.OUT/'vendor').glob('NeuralCommonNeighbor-*'))/'model.py')}
    datasets={}
    for ds in ('cora','pubmed'):
        a=sealed_input(ds); truth=set(map(tuple,np.sort(a['train'],axis=1)))
        assert not any(tuple(p) in truth for p in np.sort(a['valid_pos'],axis=1))
        canonical=read(CANONICAL/'CANONICAL_PROTOCOL.json')['datasets'][ds]['arrays']
        for field in ('x','train','valid_pos','valid_neg'):
            # V17.5 canonical arrays use raw-byte SHA256, whereas the older array_hash
            # includes dtype/shape metadata. Preserve both conventions without mixing them.
            assert hashlib.sha256(np.ascontiguousarray(a[field]).tobytes()).hexdigest()==canonical[field], f'CANONICAL_INPUT_MISMATCH {ds} {field}'
        checkpoints={}
        for seed in range(5):
            p=base_job(ds,seed)/'final.pt'; ref=read(base_job(ds,seed)/'result.json')
            assert ref['epochs']==10 and ref['arm']=='C0' and ref['test_accessed'] is False
            assert sha(p)==ref['checkpoint_sha256']
            checkpoints[str(seed)]={'path':str(p),'sha256':sha(p),'epochs':10,'parameters':ref['base_parameters']}
        datasets[ds]={'n':len(a['x']), 'train_pairs':len(a['train']),
                      'valid_queries':len(a['valid_pos']), 'negatives_per_query':int(a['valid_neg'].shape[1]),
                      'input_hashes':{k:s.ah(a[k]) for k in a}, 'base_checkpoints':checkpoints,
                      'validation_edges_absent_from_train':True,'test_arrays_loaded':False}
    manifest['datasets']=datasets
    write(OUT/'SOURCE_HASHES.json',manifest)
    write(OUT/'RUN_MANIFEST.json',{'state':'REGISTERED','task':'CHRI_V18','created_at':time.time(),
        'datasets':['cora','pubmed'],'phase_a':{'seeds':[0,1,2],'epochs':5,'arms':['A0',*ARMS]},
        'phase_b':{'seeds':list(range(5)),'epochs':10,'arms':['A0',*ARMS]},
        'backbone':'frozen, seed-paired V17.4 C0 NCNC fixed-final-10 checkpoints; never optimized',
        'matching':'train-only normalized B/P; block PCA; kNN32; candidate-key self exclusion; labels not used',
        'hyperedge_encoder':[33,32,16],'relation_encoder':[48,32,16],
        'decoder':[353,64,32,1], 'module_z_decoder':[321,64,32,1],
        'module_nuisance':[321,32,32], 'module_correction':[32,32,1],
        'lambda_nuisance':1.0,'lambda_conditional_null':1.0,'permutations':500,
        'heuristic_subset':'closest one of original 20 negatives/query; lowest 25% matching distances; no replacement',
        'heuristic_disappearance_epsilon_ce':1e-4,'heuristic_disappearance_epsilon_mrr':1e-4,
        'training':'official 1:1 sum log-sigmoid loss; official batch/floor iterator policy; fixed final epoch',
        'primary_ce':'ordinary binary CE over frozen 1 positive+20 negatives/query; balanced CE also reported',
        'auxiliary_optimizer':'Adam, canonical predictor learning rate per dataset, weight_decay=0',
        'concurrency':{'backbone_cache_workers':2,'auxiliary_training_workers':3,'matching_cpu_threads':24},
        'test_accessed':False,'innovation1':'FINAL_FROZEN','innovation3':'NOT_STARTED'})
    for name in ARTIFACTS:
        if not (OUT/name).exists():write(OUT/name,{'state':'NOT_RUN','reason':'Awaiting prerequisite validation stage gate; task just registered.'})
    write(OUT/'01_LEAKAGE_AUDIT.json',{'state':'PENDING_STRUCTURE_ORACLE','datasets':datasets,
        'target_rule':'remove training target before incident memberships and descriptors; star centers u/v lose opposite endpoint',
        'test_accessed':False})
    write(OUT/'LEAKAGE_AUDIT.json',read(OUT/'01_LEAKAGE_AUDIT.json'))
    print('PREFLIGHT_PASS',flush=True)


def prepare_structure(ds):
    destination=cache(ds)/'structure.npz'
    if (cache(ds)/'STRUCTURE_READY.json').exists():return
    a=sealed_input(ds)
    started=time.perf_counter()
    try:
        meta=build_structure(a['x'],a['train'],destination)
    except BaseException as error:
        invalid={'state':'INVALID_EXPERIMENT','dataset':ds,'reason':'Target-mask reconstruction audit failed',
                 'error':repr(error),'test_accessed':False}
        write(OUT/'01_LEAKAGE_AUDIT.json',invalid);write(OUT/'LEAKAGE_AUDIT.json',invalid)
        raise
    assert meta['target_mask_oracle']=='PASS'
    meta.update(state='PASS',dataset=ds,seconds=time.perf_counter()-started,
                train_only=True,training_targets_removed_before_encoder=True,
                descriptor_file_sha256=sha(destination),test_accessed=False)
    write(cache(ds)/'STRUCTURE_READY.json',meta)
    print('STRUCTURE_READY',ds,meta['seconds'],flush=True)


def load_backbone(ds,seed):
    model,pred,_,optimizer,data,train,scope,a,initial=s.make_models(ds,seed,'C0')
    ref=read(base_job(ds,seed)/'result.json')
    assert ref['epochs']==10 and ref['arm']=='C0'
    assert sha(base_job(ds,seed)/'final.pt')==ref['checkpoint_sha256']
    checkpoint=torch.load(base_job(ds,seed)/'final.pt',map_location='cuda',weights_only=False)
    model.load_state_dict(checkpoint['model']);pred.load_state_dict(checkpoint['predictor'])
    model.eval();pred.eval();model.requires_grad_(False);pred.requires_grad_(False)
    return model,pred,data,train,scope,a


@torch.no_grad()
def backbone_representations(pred,h,adj,pairs,batch=512):
    captured=[]
    def capture(_module,arguments):
        captured[:] = [arguments[0].detach()]
    handle=pred.lin.register_forward_pre_hook(capture)
    chunks=[]
    try:
        for begin in range(0,len(pairs),batch):
            part=torch.as_tensor(pairs[begin:begin+batch],dtype=torch.long,device='cuda')
            captured.clear();logit=pred(h,adj,part.T).flatten()
            assert len(captured)==1 and captured[0].shape==(len(part),256)
            # NCNC completion recursion also visits lin; the final call is the root candidate.
            assert torch.allclose(pred.lin(captured[0]).flatten(),logit,atol=1e-6,rtol=1e-6)
            chunks.append(torch.cat((logit[:,None],captured[0]),1).cpu().numpy())
    finally:handle.remove()
    return np.concatenate(chunks).astype(np.float32)


def prepare_backbone(ds,seed,epochs):
    check_frozen();prepare_structure(ds)
    destination=cache(ds,seed)
    if (destination/f'B_READY_{epochs}.json').exists():return
    started=time.perf_counter();model,pred,data,train,scope,a=load_backbone(ds,seed)
    from torch_sparse import SparseTensor
    n=len(a['x']);count=len(train);cfg=b.NCFG[ds];batch=cfg['batch']
    keep=(count//batch)*batch
    # Official negative sampling calls use Python random. No heldout-label filtering.
    random.seed(seed);negative=[]
    for epoch in range(epochs):
        negative.append(scope['negative_sampling'](data.edge_index,data.num_nodes).T.cpu().numpy())
    np.save(destination/'negative_schedule.npy',np.stack(negative))
    if not (destination/'valid_b.npy').exists():
        with torch.no_grad():
            h=model(data.x,data.adj_t)
            pairs=np.vstack((a['valid_pos'],a['valid_neg'].reshape(-1,2)))
            vb=backbone_representations(pred,h,data.adj_t,pairs)
        # Bit-level transport is retained (float32 cache, no mixed precision).
        previous=base_job(ds,seed)/'valid_epoch10_scores.npz'
        with np.load(previous) as z:
            old=np.r_[z['positive'],z['negative'].ravel()]
        error=float(np.max(np.abs(old-vb[:,0])))
        assert error<1e-4, f'FROZEN_NCNC_VALID_LOGIT_PARITY {ds} {seed} {error}'
        np.save(destination/'valid_b.npy',vb);np.save(destination/'valid_pairs.npy',pairs)
        write(destination/'BASE_VALID_PARITY.json',{'state':'PASS','max_abs_error':error,'test_accessed':False})
    traces=[]
    for epoch in range(1,epochs+1):
        stem=destination/f'epoch_{epoch}'
        torch.manual_seed(18400+seed*100+epoch);torch.cuda.manual_seed_all(18400+seed*100+epoch)
        perm=torch.randperm(count,device='cuda')[:keep].cpu().numpy()
        neg=negative[epoch-1]
        assert len(neg)>=count
        p=a['train'][perm];q=neg[perm]
        trace={'epoch':epoch,'official_negative_hash':s.ah(neg), 'permutation_hash':s.ah(perm),
               'retained_train_pairs':keep,'official_floor_batch_tail':count-keep,
               'mask':'all positives in this minibatch removed from NCNC message graph; own target removed from raw-star views'}
        traces.append(trace)
        if (stem.with_suffix('.npy')).exists():continue
        features=[]
        for begin in range(0,keep,batch):
            removed=perm[begin:begin+batch]
            mask=torch.ones(count,dtype=torch.bool,device='cuda');mask[torch.as_tensor(removed,device='cuda')]=False
            edge=train[mask].T
            adj=SparseTensor.from_edge_index(edge,sparse_sizes=(n,n)).to_symmetric().coalesce()
            with torch.no_grad():
                h=model(data.x,adj)
                bp=backbone_representations(pred,h,adj,p[begin:begin+batch])
                bn=backbone_representations(pred,h,adj,q[begin:begin+batch])
            features.append((bp,bn))
        bp=np.concatenate([v[0] for v in features]);bn=np.concatenate([v[1] for v in features])
        np.save(stem.with_suffix('.npy'),np.stack((bp,bn)))
        np.save(destination/f'epoch_{epoch}_pairs.npy',np.stack((p,q)))
        write(destination/'progress.json',{'state':'PREPARING_B','dataset':ds,'seed':seed,
              'epoch':epoch,'epochs':epochs,'seconds':time.perf_counter()-started,'test_accessed':False})
        print('B_CACHE',ds,seed,epoch,epochs,flush=True)
        del features,bp,bn,h;gc.collect();torch.cuda.empty_cache()
    manifest={'state':'COMPLETE','dataset':ds,'seed':seed,'epochs':epochs,
              'frozen_checkpoint':str(base_job(ds,seed)/'final.pt'), 'checkpoint_sha256':sha(base_job(ds,seed)/'final.pt'),
              'B_definition':'[frozen NCNC logit, 256-dimensional root lin input]; C absorbed by B_NCNC',
              'NCNC_parameters_frozen':True,'trace':traces,'seconds':time.perf_counter()-started,'test_accessed':False}
    write(destination/f'B_READY_{epochs}.json',manifest)


def extract_matching_features(net,pairs,features):
    result=[]
    net.eval()
    with torch.no_grad():
        for begin in range(0,len(pairs),512):
            p=torch.tensor(pairs[begin:begin+512],dtype=torch.long,device='cuda')
            x=torch.tensor(features[begin:begin+512],device='cuda')
            z,_=net.representation(p,x,False)
            result.append(z.cpu().numpy())
    return np.concatenate(result)


class Matcher:
    """Approximate Z conditioning fitted only on unlabeled training candidates."""
    def __init__(self,train_z):
        self.mean=train_z.mean(0);self.std=train_z.std(0).clip(1e-5)
        standardized=(train_z-self.mean)/self.std
        self.b=PCA(n_components=8,random_state=18020,svd_solver='randomized').fit(standardized[:,1:257])
        self.p=PCA(n_components=4,random_state=18021,svd_solver='randomized').fit(standardized[:,257:])
        self.tree=cKDTree(self.transform(train_z))

    def transform(self,z):
        a=(z-self.mean)/self.std
        return np.column_stack((a[:,0],self.b.transform(a[:,1:257])/np.sqrt(8),
                                self.p.transform(a[:,257:])/2)).astype(np.float32)

    def query(self,z,query_keys=None,donor_keys=None):
        distance,index=self.tree.query(self.transform(z),k=40,workers=24)
        if query_keys is None:return index[:,:32].astype(np.int32),distance[:,:32]
        valid=donor_keys[index]!=query_keys[:,None]
        order=np.argsort(~valid,axis=1,kind='stable')[:,:32]
        index=np.take_along_axis(index,order,axis=1)
        distance=np.take_along_axis(distance,order,axis=1)
        assert not np.any(donor_keys[index]==query_keys[:,None]), 'SHUFFLE_SELF_KEY_LEAKAGE'
        return index.astype(np.int32),distance


def make_net(ds,seed,arm,phase,structure=None):
    destination=cache(ds,seed)
    stats=read(destination/'normalization.json')
    structure=structure or Structure(cache(ds)/'structure.npz')
    fixed=None;i1=None
    if phase in ('M','O','CM','CO'):
        parent_phase='C' if ds=='citeseer' else 'B'
        parent=torch.load(job(parent_phase,ds,seed,'A2')/'final.pt',map_location='cpu',weights_only=False)['state']
        fixed={'encoder':{k.removeprefix('encoder.'):v for k,v in parent.items() if k.startswith('encoder.')},
               'relation':{k.removeprefix('relation.'):v for k,v in parent.items() if k.startswith('relation.')}}
    if phase in ('O','CO') and arm in ('O1','O3_RAW','O3_CRIB'):
        _,view=s.f.m.p.v16.base.init_dataset(ds)
        i1=s.Residual(view,ds).to('cuda')
        cp=torch.load(base_job(ds,seed,'C1')/'final.pt',map_location='cuda',weights_only=False)
        rs={k.removeprefix('residual.'):v for k,v in cp['predictor'].items() if k.startswith('residual.')}
        i1.load_state_dict(rs,strict=True);i1.requires_grad_(False)
        assert sum(p.numel() for p in i1.parameters())==75
    net=RelationPredictor(structure,seed,arm,np.array(stats['mean']),np.array(stats['std']),fixed,i1).to('cuda')
    return net


def prepare_matching(ds,seed,epochs):
    destination=cache(ds,seed)
    if (destination/f'MATCH_READY_{epochs}.json').exists():return
    started=time.perf_counter()
    # Epoch1 donor pool is fixed before observing any outcome, labels are not inspected.
    ep=np.load(destination/'epoch_1.npy',mmap_mode='r')
    pp=np.load(destination/'epoch_1_pairs.npy')
    train_b=np.concatenate((ep[0],ep[1]));pool=np.concatenate((pp[0],pp[1]))
    mean=train_b.mean(0);std=train_b.std(0).clip(1e-5)
    write(destination/'normalization.json',{'mean':mean.tolist(),'std':std.tolist(),
          'fit':'epoch1 training candidates only, label-free','test_accessed':False})
    net=make_net(ds,seed,'A1','A')
    train_z=extract_matching_features(net,pool,train_b)
    matcher=Matcher(train_z);n=net.structure.n
    donor_keys=np.sort(pool,axis=1)@np.array([n,1])
    np.save(destination/'donor_pairs.npy',pool)
    distances=[]
    for split in [f'epoch_{e}' for e in range(1,epochs+1)]+['valid']:
        if (destination/f'{split}_knn.npy').exists():continue
        if split=='valid':
            pairs=np.load(destination/'valid_pairs.npy');features=np.load(destination/'valid_b.npy',mmap_mode='r')
        else:
            pairs=np.load(destination/f'{split}_pairs.npy').reshape(-1,2)
            features=np.load(destination/f'{split}.npy',mmap_mode='r').reshape(-1,257)
        z=extract_matching_features(net,pairs,features)
        keys=np.sort(pairs,axis=1)@np.array([n,1])
        indexes,d=matcher.query(z,keys,donor_keys)
        np.save(destination/f'{split}_knn.npy',indexes)
        selected=indexes[:,0]
        std_z=(z-matcher.mean)/matcher.std
        std_d=(train_z[selected]-matcher.mean)/matcher.std
        diagnostics={'split':split,'nearest_projected_distance_mean':float(d[:,0].mean()),
                     'top32_distance_mean':float(d.mean()),'top32_distance_q95':float(np.quantile(d,.95)),
                     'nearest_full_Z_rms_distance':float(np.sqrt(np.mean((std_z-std_d)**2,axis=1)).mean()),
                     'self_candidate_keys_excluded':True, 'queries':len(pairs)}
        distances.append(diagnostics)
        write(destination/f'{split}_matching_diagnostics.json',diagnostics)
        print('MATCH_READY',ds,seed,split,flush=True)
    diagnostics=[read(destination/f'{split}_matching_diagnostics.json') for split in [f'epoch_{e}' for e in range(1,epochs+1)]+['valid']]
    write(destination/f'MATCH_READY_{epochs}.json',{'state':'COMPLETE','seconds':time.perf_counter()-started,
        'matching_encoder':'seed-shared initial DeepSets encoder frozen for matching; predictor encoders subsequently trained',
        'rule':'train-only StandardScaler; PCA8 on NCNC structural representation + PCA4 on P_u/P_v; standardized logit; kNN32 of 40; exclude identical candidate keys',
        'donor_pool_candidates':len(pool),'donor_pairs_hash':s.ah(pool),
        'labels_used':False,'heldout_donors':False,'test_accessed':False,'diagnostics':diagnostics,
        'conditioning_limit':'finite-dimensional PCA/kNN approximation; not exact conditional independence sampling',
        'marginal_preservation':'local donors preserve support approximately; empirical learned-R diagnostics written per arm after training'})


def metrics(scores,queries,negatives=20):
    scores=np.asarray(scores,dtype=np.float64)
    positive=scores[:queries];negative=scores[queries:].reshape(queries,negatives)
    y=np.r_[np.ones(queries),np.zeros(queries*negatives)]
    losses=np.logaddexp(0,scores)-y*scores
    rr=b.ranking_metrics(positive,negative)
    return {'ce':float(losses.mean()),'balanced_ce':float((losses[:queries].mean()+losses[queries:].mean())/2),
            'auc':float(roc_auc_score(y,scores)),**{key:float(rr[key]) for key in ('mrr','hits10','hits20','mean_positive_rank')},
            'queries':queries,'negatives_per_query':negatives}


def setup_i1(net,ds,split):
    if net.i1 is None:return
    phase='third' if ds=='citeseer' else 'B'
    net.i1.store=s.feature_store(phase,ds,split)


def donor_choices(knn,seed,epoch):
    rng=np.random.RandomState(18500+seed*100+epoch)
    column=rng.randint(knn.shape[1],size=len(knn))
    return np.asarray(knn)[np.arange(len(knn)),column]


@torch.no_grad()
def evaluate(net,ds,seed,split='valid',save=None):
    destination=cache(ds,seed)
    net.eval();setup_i1(net,ds,split)
    pairs=np.load(destination/f'{split}_pairs.npy')
    features=np.load(destination/f'{split}_b.npy',mmap_mode='r')
    neighbors=np.load(destination/f'{split}_knn.npy',mmap_mode='r')
    donors=np.load(destination/'donor_pairs.npy')
    selected=donor_choices(neighbors,seed,0)
    outputs=[]
    for begin in range(0,len(pairs),512):
        stop=begin+512
        p=torch.tensor(pairs[begin:stop],dtype=torch.long,device='cuda')
        bf=torch.tensor(features[begin:stop],device='cuda')
        d=torch.tensor(donors[selected[begin:stop]],dtype=torch.long,device='cuda')
        outputs.append(net(p,bf,d)[0].cpu().numpy())
    scores=np.concatenate(outputs)
    a=sealed_input(ds,split=='test');q=len(a[f'{split}_pos']);nc=int(a[f'{split}_neg'].shape[1])
    result=metrics(scores,q,nc)
    if save is not None:np.savez_compressed(save,positive=scores[:q],negative=scores[q:].reshape(q,nc))
    return result


def relation_marginals(net,ds,seed):
    destination=cache(ds,seed);pairs=np.load(destination/'valid_pairs.npy')
    features=np.load(destination/'valid_b.npy',mmap_mode='r')
    donors=np.load(destination/'donor_pairs.npy')
    indexes=donor_choices(np.load(destination/'valid_knn.npy'),seed,0)
    arrays=[[],[]];net.eval()
    with torch.no_grad():
        for begin in range(0,len(pairs),512):
            bf=torch.tensor(features[begin:begin+512],device='cuda')
            for which,part in enumerate((pairs[begin:begin+512],donors[indexes[begin:begin+512]])):
                _,r=net.representation(torch.tensor(part,dtype=torch.long,device='cuda'),bf,True)
                arrays[which].append(r.cpu().numpy())
    a,c=[np.concatenate(v) for v in arrays]
    scale=a.std(0).clip(1e-6)
    return {'true_mean':a.mean(0).tolist(),'shuffled_mean':c.mean(0).tolist(),
            'true_std':a.std(0).tolist(),'shuffled_std':c.std(0).tolist(),
            'mean_absolute_standardized_mean_shift':float(np.mean(np.abs(a.mean(0)-c.mean(0))/scale)),
            'changed_candidate_fraction':float(np.mean(np.any(np.abs(a-c)>1e-6,axis=1))),
            'marginals_exactly_preserved':False,'donors':'matched training candidates; no labels used',
            'quantiles_true':np.quantile(a,[.1,.5,.9],axis=0).tolist(),
            'quantiles_shuffled':np.quantile(c,[.1,.5,.9],axis=0).tolist()}


def run(phase,ds,seed,arm,epochs):
    check_frozen();destination=job(phase,ds,seed,arm);destination.mkdir(parents=True,exist_ok=True)
    if (destination/'result.json').exists():return
    torch.manual_seed(seed);np.random.seed(seed);random.seed(seed)
    net=make_net(ds,seed,arm,phase)
    initial={'encoder':hash_state(net.encoder),'relation':hash_state(net.relation),
             'decoder':hash_state(net.z_decoder if net.is_module else net.decoder)}
    optimizer=torch.optim.Adam([p for p in net.parameters() if p.requires_grad],lr=b.NCFG[ds]['prelr'],weight_decay=0)
    baseline_b=np.load(cache(ds,seed)/'valid_b.npy',mmap_mode='r')
    a=sealed_input(ds);baseline=metrics(baseline_b[:,0],len(a['valid_pos']))
    donor_pool=np.load(cache(ds,seed)/'donor_pairs.npy');history=[]
    torch.cuda.reset_peak_memory_stats();started=time.perf_counter();batch=b.NCFG[ds]['batch']
    for epoch in range(1,epochs+1):
        features=np.load(cache(ds,seed)/f'epoch_{epoch}.npy',mmap_mode='r')
        pairs=np.load(cache(ds,seed)/f'epoch_{epoch}_pairs.npy',mmap_mode='r')
        neighbors=np.load(cache(ds,seed)/f'epoch_{epoch}_knn.npy',mmap_mode='r').reshape(2,len(pairs[0]),32)
        chosen=donor_choices(neighbors.reshape(-1,32),seed,epoch).reshape(2,-1)
        net.train();setup_i1(net,ds,'train');losses=[];nuisance=[];null=[]
        for begin in range(0,len(pairs[0]),batch):
            stop=begin+batch;optimizer.zero_grad(set_to_none=True)
            sample=np.concatenate((pairs[0,begin:stop],pairs[1,begin:stop]))
            bf=np.concatenate((features[0,begin:stop],features[1,begin:stop]))
            d=donor_pool[np.concatenate((chosen[0,begin:stop],chosen[1,begin:stop]))]
            size=len(sample)//2
            # Microbatches preserve the exact canonical optimizer minibatch and class weights.
            loss_value=nuis_value=null_value=0.
            for offset in range(0,len(sample),256):
                end=min(offset+256,len(sample));weight=(end-offset)/len(sample)
                p=torch.tensor(sample[offset:end],dtype=torch.long,device='cuda')
                x=torch.tensor(bf[offset:end],device='cuda')
                donor=torch.tensor(d[offset:end],dtype=torch.long,device='cuda')
                score,nl,cl=net(p,x,donor)
                label=torch.tensor(np.arange(offset,end)<size,dtype=score.dtype,device='cuda')
                predictive=2*torch.nn.functional.binary_cross_entropy_with_logits(score,label)
                total=predictive
                if net.is_module and arm not in ('M0','O0','O1'):
                    total=total+nl
                    if arm in ('M3','O3_CRIB','O2_CRIB'):total=total+cl
                assert torch.isfinite(total), 'NONFINITE_LOSS'
                (weight*total).backward()
                loss_value+=weight*float(total.detach());nuis_value+=weight*float(nl.detach());null_value+=weight*float(cl.detach())
            optimizer.step();losses.append(loss_value);nuisance.append(nuis_value);null.append(null_value)
        result=evaluate(net,ds,seed,save=destination/f'valid_epoch{epoch}_scores.npz')
        history.append({'epoch':epoch,'loss':float(np.mean(losses)), 'nuisance_loss':float(np.mean(nuisance)),
                        'null_loss':float(np.mean(null)), 'validation':result})
        write(destination/'progress.json',{'state':'RUNNING','phase':phase,'dataset':ds,'seed':seed,
              'arm':arm,'epoch':epoch,'epochs':epochs,'validation':result,
              'elapsed_seconds':time.perf_counter()-started,'updated_at':time.time(),'test_accessed':False})
        print('TRAIN',phase,ds,seed,arm,epoch,history[-1]['loss'],result['ce'],result['mrr'],flush=True)
    torch.save({'state':net.state_dict(),'phase':phase,'dataset':ds,'seed':seed,'arm':arm,'epochs':epochs},destination/'final.pt')
    rr={'state':'COMPLETE','phase':phase,'dataset':ds,'seed':seed,'arm':arm,'epochs':epochs,
        'validation':result,'A0_frozen_NCNC':baseline,'history':history,
        'checkpoint':str(destination/'final.pt'),'checkpoint_sha256':sha(destination/'final.pt'),
        'initialization':initial,'training_trace':read(cache(ds,seed)/f'B_READY_{epochs}.json')['trace'],
        'trainable_parameters':sum(p.numel() for p in net.parameters() if p.requires_grad),
        'encoder_trainable':any(p.requires_grad for p in net.encoder.parameters()),
        'relation_parameters':sum(p.numel() for p in net.relation.parameters()),
        'downstream_decoder_capacity_matched':True,'frozen_NCNC_parameters':read(base_job(ds,seed)/'result.json')['base_parameters'],
        'frozen_I1_parameters':75 if net.i1 is not None else 0,
        'peak_gpu_mb':torch.cuda.max_memory_allocated()/1024**2,'wall_seconds':time.perf_counter()-started,
        'checkpoint_selection':'fixed final epoch; no best-validation selection','test_accessed':False}
    if arm in ('A2','A3'):
        rr['relation_shuffle_marginal_diagnostics']=relation_marginals(net,ds,seed)
    write(destination/'result.json',rr)
    write(destination/'progress.json',{'state':'COMPLETE','epoch':epochs,'epochs':epochs,'validation':result,'test_accessed':False})


def stat(values):
    values=np.array(values,float)
    return {'mean':float(values.mean()),'median':float(np.median(values)),
            'std':float(values.std(ddof=1)) if len(values)>1 else None,
            'wins':int((values>0).sum()),'per_seed':values.tolist()}


def comparison(rows,left,right,field='validation'):
    # Positive CE effect means improvement; positive rank/AUC effect means improvement.
    return {metric:stat([(r['arms'][right][field][metric]-r['arms'][left][field][metric]) if metric=='ce'
                        else (r['arms'][left][field][metric]-r['arms'][right][field][metric]) for r in rows])
            for metric in METRICS}


def summarize(phase,datasets,seeds,arms):
    output={'state':'COMPLETE','phase':phase,'seeds':seeds,'datasets':{},'test_accessed':False}
    for ds in datasets:
        rows=[{'seed':seed,'arms':{arm:read(job(phase,ds,seed,arm)/'result.json') for arm in arms}} for seed in seeds]
        for row in rows:
            for arm in arms:
                assert row['arms'][arm]['training_trace']==row['arms'][arms[0]]['training_trace'], 'PAIR_TRACE_MISMATCH'
                assert row['arms'][arm]['initialization']['decoder']==row['arms'][arms[0]]['initialization']['decoder'], 'PAIR_DECODER_INIT_MISMATCH'
                assert row['arms'][arm]['initialization']['encoder']==row['arms'][arms[0]]['initialization']['encoder'], 'PAIR_ENCODER_INIT_MISMATCH'
        if phase in ('A','B','C'):
            effects={name:comparison(rows,left,right) for name,left,right in (
                ('true_vs_Z','A2','A1'),('true_vs_shuffle','A2','A3'),('true_vs_null','A2','A4'))}
            main=effects['true_vs_Z'];required=(2 if len(seeds)==3 else (4 if ds=='cora' else 3))
            gates={'mean_ce_positive':main['ce']['mean']>0, 'ce_seed_wins':main['ce']['wins']>=required,
                   'mean_mrr_positive':main['mrr']['mean']>0,
                   'true_vs_shuffle_ce':effects['true_vs_shuffle']['ce']['mean']>0,
                   'true_vs_null_ce':effects['true_vs_null']['ce']['mean']>0}
            if phase!='A':gates['median_ce_positive']=main['ce']['median']>0
        else:
            effects={f'{left}_vs_{right}':comparison(rows,left,right) for left,right in
                     (('M1','M0'),('M2','M1'),('M3','M1'),('M3','M2'),('M1','M4'))}
            gates={'CRIB_mean_ce_over_raw':effects['M3_vs_M1']['ce']['mean']>0,
                   'CRIB_mean_mrr_over_raw':effects['M3_vs_M1']['mrr']['mean']>0}
        output['datasets'][ds]={'seed_results':rows,'effects':effects,'gates':gates,'pass':all(gates.values()),
            'metrics':{arm:{metric:stat([r['arms'][arm]['validation'][metric] for r in rows]) for metric in METRICS} for arm in arms}}
    output['all_pass']=all(d['pass'] for d in output['datasets'].values())
    return output


def load_net(phase,ds,seed,arm):
    net=make_net(ds,seed,arm,phase)
    cp=job(phase,ds,seed,arm)/'final.pt'
    assert sha(cp)==read(job(phase,ds,seed,arm)/'result.json')['checkpoint_sha256']
    net.load_state_dict(torch.load(cp,map_location='cuda',weights_only=False)['state'])
    net.eval();return net


@torch.no_grad()
def latent_arrays(net,pairs,features):
    zz=[];rr=[]
    for begin in range(0,len(pairs),512):
        pp=torch.tensor(pairs[begin:begin+512],dtype=torch.long,device='cuda')
        bb=torch.tensor(features[begin:begin+512],device='cuda')
        z,r=net.representation(pp,bb,True)
        zz.append(z.cpu().numpy());rr.append(r.cpu().numpy())
    return np.concatenate(zz),np.concatenate(rr)


def scores_file(path):
    with np.load(path) as z:return np.r_[z['positive'],z['negative'].ravel()]


def conditional_diagnostic(ds,seed):
    destination=OUT/'diagnostics'/ds/f'seed_{seed}';destination.mkdir(parents=True,exist_ok=True)
    if (destination/'conditional.json').exists():return
    net=load_net('B',ds,seed,'A2');pool=np.load(cache(ds,seed)/'donor_pairs.npy')
    ep=np.load(cache(ds,seed)/'epoch_1.npy',mmap_mode='r');pool_b=ep.reshape(-1,257)
    pool_z,pool_r=latent_arrays(net,pool,pool_b)
    vp=np.load(cache(ds,seed)/'valid_pairs.npy');vb=np.load(cache(ds,seed)/'valid_b.npy',mmap_mode='r')
    vz,vr=latent_arrays(net,vp,vb)
    # Refit the same train-only matching rule using the final learned conditioning representation.
    matcher=Matcher(pool_z);n=net.structure.n
    keys=np.sort(vp,axis=1)@np.array([n,1]);dkeys=np.sort(pool,axis=1)@np.array([n,1])
    knn,distance=matcher.query(vz,keys,dkeys)
    q=len(sealed_input(ds)['valid_pos']);ref=read(job('B',ds,seed,'A1')/'result.json')['validation']['ce']
    observed=ref-read(job('B',ds,seed,'A2')/'result.json')['validation']['ce']
    statistics=[];rng=np.random.RandomState(18600+seed)
    labels=torch.tensor(np.r_[np.ones(q),np.zeros(len(vp)-q)],dtype=torch.float64,device='cuda')
    z=torch.tensor(vz,device='cuda');baseline=torch.tensor(vb[:,0].copy(),device='cuda')
    donor_r=torch.tensor(pool_r,device='cuda')
    knn_t=torch.tensor(knn,dtype=torch.long,device='cuda');rows=torch.arange(len(vp),device='cuda')
    with torch.no_grad():
        for permutation in range(500):
            cols=torch.tensor(rng.randint(32,size=len(vp)),dtype=torch.long,device='cuda')
            indexes=knn_t[rows,cols];loss=0.
            for begin in range(0,len(vp),8192):
                score=net.prediction(z[begin:begin+8192],donor_r[indexes[begin:begin+8192]],baseline[begin:begin+8192]).double()
                ll=torch.nn.functional.binary_cross_entropy_with_logits(score,labels[begin:begin+8192],reduction='sum')
                loss+=float(ll)
            statistics.append(ref-loss/len(vp))
            if (permutation+1)%100==0:print('CONDITIONAL_PERM',ds,seed,permutation+1,flush=True)
    statistics=np.array(statistics)
    result={'state':'COMPLETE','dataset':ds,'seed':seed,'permutations':500,
        'observed_delta_ce':float(observed),'null_mean':float(statistics.mean()),
        'null_std':float(statistics.std(ddof=1)),
        'empirical_p_value':float((1+(statistics>=observed).sum())/501),
        'shuffled_delta_ce_distribution':statistics.tolist(),
        'matching_rule':'same block-PCA/kNN32, refit on final q1 Z from training donor pool only; no heldout donors or labels',
        'matching_distance_mean':float(distance.mean()),
        'interpretation':'approximate matched conditional permutation support diagnostic; neither an exact conditional test nor an exact CMI estimator',
        'test_accessed':False}
    write(destination/'conditional.json',result)


def matched_hard_diagnostic(ds,seeds):
    a=sealed_input(ds);q=len(a['valid_pos']);pairs=np.vstack((a['valid_pos'],a['valid_neg'].reshape(-1,2)))
    h=heuristic_rows(a['train'],len(a['x']),pairs)
    pool=np.load(cache(ds,seeds[0])/'donor_pairs.npy')
    train_h=heuristic_rows(a['train'],len(a['x']),pool)
    mean=train_h.mean(0);std=train_h.std(0).clip(1e-5)
    hh=(h-mean)/std
    pos=hh[:q];neg=hh[q:].reshape(q,20,-1)
    distances=np.sqrt(((neg-pos[:,None,:])**2).mean(2))
    choice=distances.argmin(1);best=distances[np.arange(q),choice]
    chosen=np.argsort(best,kind='stable')[:max(16,int(np.ceil(q*.25)))]
    positive_rows=chosen;negative_rows=q+chosen*20+choice[chosen]
    rows=[]
    for seed in seeds:
        arm_results={}
        for arm in ('A1','A2','A3'):
            scores=scores_file(job('B',ds,seed,arm)/'valid_epoch10_scores.npz')
            restricted=np.r_[scores[positive_rows],scores[negative_rows]]
            arm_results[arm]={'validation':metrics(restricted,len(chosen),1)}
        rows.append({'seed':seed,'arms':arm_results})
    effects={'true_vs_Z':comparison(rows,'A2','A1'), 'true_vs_shuffle':comparison(rows,'A2','A3')}
    disappeared=effects['true_vs_Z']['ce']['mean']<=1e-4 and effects['true_vs_Z']['mrr']['mean']<=1e-4
    result={'state':'COMPLETE','dataset':ds,'seed_results':rows,'effects':effects,
        'heuristics':['degree_u','degree_v','Eu_count','Ev_count','incident_overlap','size_u_mean','size_u_std',
                      'size_v_mean','size_v_std','CN','AA','RA','length3_shared_support'],
        'normalization':'training donor candidates only','selection':'one closest original negative/query, lowest-distance 25% query subset, labels identify positive/negative only; scores not used',
        'positive_query_indexes':chosen.tolist(),'negative_within_query_indexes':choice[chosen].tolist(),
        'queries':len(chosen),'negative_count':1,'main_split_modified':False,
        'matching_distance_mean':float(best[chosen].mean()),'matching_distance_q95':float(np.quantile(best[chosen],.95)),
        'remaining_standardized_mean_imbalance':np.abs(hh[positive_rows].mean(0)-hh[negative_rows].mean(0)).tolist(),
        'signal_completely_disappeared':bool(disappeared),
        'limitations':'approximate feature matching; subset uses one negative/query and is not numerically comparable to the main 20-negative MRR',
        'test_accessed':False}
    write(OUT/'diagnostics'/ds/'matched_hard.json',result)
    return result


def orthogonality_summary(datasets,seeds,crib,phase='O',module_phase='M'):
    o3='O3_CRIB' if crib else 'O3_RAW';selected='M3' if crib else 'M1'
    result={'state':'COMPLETE','selected_method':'CRIB' if crib else 'raw R_CAT phenomenon probe',
            'datasets':{},'test_accessed':False}
    for ds in datasets:
        rows=[]
        for seed in seeds:
            arms={'O0':read(job(module_phase,ds,seed,'M0')/'result.json'),
                  'O1':read(job(phase,ds,seed,'O1')/'result.json'),
                  'O2':read(job(module_phase,ds,seed,selected)/'result.json'),
                  'O3':read(job(phase,ds,seed,o3)/'result.json')}
            assert all(v['epochs']==10 for v in arms.values())
            assert all(v['training_trace']==arms['O0']['training_trace'] for v in arms.values())
            rows.append({'seed':seed,'arms':arms})
        effects={name:comparison(rows,left,right) for name,left,right in (
            ('I2_complement_to_I1','O3','O1'),('I1_effect','O1','O0'),('I2_effect','O2','O0'))}
        effect=effects['I2_complement_to_I1']
        result['datasets'][ds]={'seed_results':rows,'effects':effects,
            'pass':effect['ce']['mean']>0 and effect['mrr']['mean']>0}
    result['I2_COMPLEMENT_TO_I1']='YES' if all(d['pass'] for d in result['datasets'].values()) else 'NO'
    return result


def prepare_test(ds,seed):
    a=sealed_input(ds,True);destination=cache(ds,seed)
    if (destination/'TEST_READY.json').exists():return
    model,pred,data,_,_,_=load_backbone(ds,seed)
    pairs=np.vstack((a['test_pos'],a['test_neg'].reshape(-1,2)))
    forbidden=set(map(tuple,np.sort(a['train'],axis=1)))
    assert not any(tuple(x) in forbidden for x in np.sort(a['test_pos'],axis=1))
    with torch.no_grad():
        h=model(data.x,data.adj_t)
        features=backbone_representations(pred,h,data.adj_t,pairs)
    np.save(destination/'test_pairs.npy',pairs);np.save(destination/'test_b.npy',features)
    # Fit matching on the same pre-training seed-shared training representation, never on test.
    net=make_net(ds,seed,'A1','A');pool=np.load(destination/'donor_pairs.npy')
    pool_b=np.load(destination/'epoch_1.npy',mmap_mode='r').reshape(-1,257)
    train_z=extract_matching_features(net,pool,pool_b);matcher=Matcher(train_z)
    tz=extract_matching_features(net,pairs,features)
    n=len(a['x']);indexes,distance=matcher.query(tz,np.sort(pairs,axis=1)@np.array([n,1]),np.sort(pool,axis=1)@np.array([n,1]))
    np.save(destination/'test_knn.npy',indexes)
    write(destination/'TEST_READY.json',{'state':'COMPLETE','dataset':ds,'seed':seed,
          'test_positive_hash':s.ah(a['test_pos']),'test_negative_hash':s.ah(a['test_neg']),
          'matching_train_only':True,'matching_distance_mean':float(distance.mean()),'target_overlap_audit':'PASS'})


def test_run(ds,seed,label,phase,arm):
    sealed_input(ds,True);net=load_net(phase,ds,seed,arm)
    destination=OUT/'test'/ds/f'seed_{seed}'/label;destination.mkdir(parents=True,exist_ok=True)
    if (destination/'result.json').exists():return
    ref=read(job(phase,ds,seed,arm)/'result.json')
    result=evaluate(net,ds,seed,'test',destination/'scores.npz')
    write(destination/'result.json',{'state':'COMPLETE','dataset':ds,'seed':seed,'arm':label,
        'model_phase':phase,'model_arm':arm,'epochs':10,'metrics':result,
        'checkpoint_sha256':ref['checkpoint_sha256'],'checkpoint_selection':'frozen final epoch10',
        'no_test_training_or_selection':True})


def test_summary(datasets,seeds_by_ds):
    output={'state':'COMPLETE','datasets':{},'test_accessed':True}
    for ds in datasets:
        rows=[{'seed':seed,'arms':{arm:read(OUT/'test'/ds/f'seed_{seed}'/arm/'result.json') for arm in ('T0','T1','T2','T3','T4')}} for seed in seeds_by_ds[ds]]
        effects={name:comparison(rows,left,right,'metrics') for name,left,right in (
            ('I2_vs_Z','T2','T0'),('I1_I2_vs_I1','T3','T1'),('true_vs_shuffle','T2','T4'))}
        output['datasets'][ds]={'seed_results':rows,'effects':effects,
            'pass':all(effects[e][m]['mean']>0 for e in effects for m in ('ce','mrr'))}
    output['all_pass']=all(d['pass'] for d in output['datasets'].values())
    return output


CHILDREN=[]


def launch(arguments):
    (OUT/'logs').mkdir(exist_ok=True)
    log=OUT/'logs'/('_'.join(map(str,arguments))+'.log')
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):env[key]='4'
    with log.open('a') as stream:
        proc=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*map(str,arguments)],
                              stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,
                              env=env,start_new_session=True)
    item={'proc':proc,'arguments':arguments,'log':str(log)};CHILDREN.append(item)
    return item


def progress(stage,active,queued):
    write(OUT/'status.json',{'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),
        'updated_at':time.time(),'queued_jobs':queued,
        'active':[{'pid':v['proc'].pid,'arguments':v['arguments'],'log':v['log']} for v in active],
        'test_unsealed':(OUT/'TEST_UNSEAL.json').exists()})


def batch(arguments,stage,parallel=3):
    queue=list(arguments);active=[]
    while queue or active:
        for item in list(active):
            if item['proc'].poll() is not None:
                active.remove(item)
                if item['proc'].returncode:
                    raise RuntimeError(f"JOB_FAILED {item['arguments']} log={item['log']}")
        while queue and len(active)<parallel:active.append(launch(queue.pop(0)))
        progress(stage,active,len(queue))
        if active:time.sleep(3)


def execute_phase(phase,datasets,seeds,epochs,arms):
    # Streaming preparation: early Cora arms start while PubMed/other seed caches are built.
    queue=[(ds,seed) for seed in seeds for ds in datasets]
    preparing=[];training=[];waiting=[]
    while queue or preparing or training or waiting:
        for item in list(preparing):
            if item['proc'].poll() is not None:
                preparing.remove(item)
                if item['proc'].returncode:raise RuntimeError(f"PREP_FAILED {item['arguments']} {item['log']}")
                ds,seed=item['arguments'][1:3]
                waiting.extend([('run',phase,ds,int(seed),arm,epochs) for arm in arms])
        for item in list(training):
            if item['proc'].poll() is not None:
                training.remove(item)
                if item['proc'].returncode:raise RuntimeError(f"TRAIN_FAILED {item['arguments']} {item['log']}")
        while waiting and len(training)+len(preparing)<3:
            training.append(launch(waiting.pop(0)))
        while queue and len(preparing)<2 and len(training)+len(preparing)<3:
            ds,seed=queue.pop(0)
            ready=cache(ds,seed)/f'MATCH_READY_{epochs}.json'
            if ready.exists():
                waiting.extend([('run',phase,ds,seed,arm,epochs) for arm in arms]);continue
            preparing.append(launch(('prepare',ds,seed,epochs)))
        progress('PHASE_'+phase,preparing+training,len(queue)*len(arms)+len(waiting))
        if preparing or training:time.sleep(3)


def update_leakage():
    audit=read(OUT/'01_LEAKAGE_AUDIT.json')
    for ds in ('cora','pubmed'):
        meta=read(cache(ds)/'STRUCTURE_READY.json')
        assert meta['state']=='PASS' and meta['target_mask_oracle']=='PASS'
        audit['datasets'][ds]['target_mask']=meta
    audit.update(state='PASS',train_only_structure=True,matching_fit='train-only, label-free',
                 validation_test_relations_in_encoder=False,test_accessed=False)
    write(OUT/'01_LEAKAGE_AUDIT.json',audit);write(OUT/'LEAKAGE_AUDIT.json',audit)


def report(state,decision,reason):
    check_frozen()
    if state=='COMPLETE':
        for artifact in ARTIFACTS:
            item=read(OUT/artifact)
            if item.get('state')=='NOT_RUN':
                write(OUT/artifact,{'state':'NOT_RUN','reason':reason,'prerequisite_final_decision':decision})
    def result(name):
        return read(OUT/name) if (OUT/name).exists() else {'state':'NOT_RUN','reason':reason}
    a=result('03_PHASE_A_RESULTS.json');formal=result('04_PHASE_B_RESULTS.json')
    conditional=result('05_CONDITIONAL_RELATION_DIAGNOSTIC.json');hard=result('06_MATCHED_HARD_DIAGNOSTIC.json')
    modules=result('08_CRIB_RESULTS.json');orth=result('09_I1_I2_ORTHOGONALITY.json')
    tests=result('10_TEST_RESULTS.json');third=result('11_THIRD_DATASET.json')
    phase_a='PASS' if a.get('all_pass') else ('FAIL' if a.get('state')=='COMPLETE' else 'NOT_RUN')
    phase_b='PASS' if formal.get('all_pass') else ('FAIL' if formal.get('state')=='COMPLETE' else 'NOT_RUN')
    crib='SUPPORTED' if modules.get('all_pass') else ('NOT_SUPPORTED' if modules.get('state')=='COMPLETE' else 'NOT_RUN')
    complement=orth.get('I2_COMPLEMENT_TO_I1','NOT_RUN')
    lines=['# CHRI V18 — Innovation 2', '',f'STATE: {state}',f'FINAL_INNOVATION_2_STATUS: {decision}',f'REASON: {reason}', '',
        '## Definitions', '',
        'Z = [frozen NCNC logit and 256d root decoder representation, P_u, P_v]. C is absorbed by the NCNC candidate-conditioned representation. Each P is mean/max pooling of the SAME shared two-layer hyperedge encoder, independently applied to its target-masked incident hyperedge set.',
        '', 'R_CAT = mean/max pooling of MLP([z_e+z_f, |z_e-z_f|, z_e*z_f]) over all pairs e in Eu, f in Ev. B/C never enter this encoder; no interaction pairs are truncated. This is a generic prior-art-style phenomenon probe.',
        '', 'The backbone is frozen at its existing seed-paired V17.4 fixed-final-10 checkpoint. Phase A/B epochs count auxiliary-predictor learning (5/10), not additional NCNC tuning. All arms share that same backbone, canonical candidates, training negatives, permutations, optimizer batches, and decoder initialization.',
        '', 'PRIMARY: ordinary binary log loss over the frozen 1:20 validation candidate population. Delta_CE = CE(control)-CE(true). Positive is improvement. This is finite-model predictive evidence, not exact conditional mutual information.',
        '', f'## 1. CHRI hypothesis\n\n{decision}. {reason}',
        '', '## 2–4. Exact controls, relation, and measured gains', '',
        '| Stage | Dataset | Contrast | Delta CE mean | Delta MRR mean | CE wins |',
        '|---|---|---|---:|---:|---:|']
    for stage,payload in (('A',a),('B',formal)):
        for ds,item in payload.get('datasets',{}).items():
            for name,effect in item['effects'].items():
                lines.append(f"| {stage} | {ds} | {name} | {effect['ce']['mean']:.10g} | {effect['mrr']['mean']:.10g} | {effect['ce']['wins']}/{len(effect['ce']['per_seed'])} |")
    lines.extend(['','## 5. True versus matched shuffle','',
        'See the paired contrasts above and per-seed learned-R marginal diagnostics. Matching uses only training donors and unlabeled training-fitted Z normalization/PCA. The finite-neighbor approximation does not guarantee exact conditional marginals.',
        '',f"## 6. Degree/motif matched diagnostic\n\n{json.dumps({k:{'effects':v.get('effects'),'signal_completely_disappeared':v.get('signal_completely_disappeared')} for k,v in hard.get('datasets',{}).items()},indent=2) if hard.get('state')=='COMPLETE' else hard}",
        '',f'## 7. CRIB versus generic relation\n\n{crib}.',
        '',f'## 8. Complementarity with FINAL_FROZEN R-HSPE\n\nI2_COMPLEMENT_TO_I1: {complement}',
        '',f"## 9. Citeseer\n\n{third.get('decision',third.get('state'))}. {third.get('reason','')}",
        '',f'## 10. Innovation 2 status\n\n{decision}',
        '', '## Test', '',json.dumps(tests,indent=2) if tests.get('state')=='COMPLETE' else f"NOT_RUN: {tests.get('reason',reason)}",
        '', '## Conditional relation support diagnostic', '',
        json.dumps({ds:[{'seed':r['seed'],'observed_delta_ce':r['observed_delta_ce'],'null_mean':r['null_mean'],'null_std':r['null_std'],'empirical_p_value':r['empirical_p_value']} for r in rr] for ds,rr in conditional.get('datasets',{}).items()},indent=2) if conditional.get('state')=='COMPLETE' else f"NOT_RUN: {conditional.get('reason',reason)}",
        '', 'Innovation 1 remains FINAL_FROZEN (75 parameters; CONTEXT_DRIVEN; size causal claim NOT_SUPPORTED). Innovation 3 is not started.'])
    (OUT/'FINAL_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    (OUT/'07_CHRI_DECISION.md').write_text(f'# CHRI decision\n\nSTATE: {state}\n\nDECISION: {decision}\n\n{reason}\n',encoding='utf-8')
    handoff=['STATUS: '+('EXECUTED' if state=='COMPLETE' else state),'TASK: CHRI_V18','WORKSPACE: DCDLP-main',
        f'PHASE_A: {phase_a}',f'PHASE_B: {phase_b}',
        'CHRI: '+('KILL' if decision=='CHRI_KILL' else 'CONFIRMED' if phase_b=='PASS' else 'PENDING'),
        'TRUE_VS_SHUFFLE: '+json.dumps({ds:v['effects']['true_vs_shuffle'] for ds,v in formal.get('datasets',a.get('datasets',{})).items()}),
        'MATCHED_HARD: '+json.dumps({ds:v.get('signal_completely_disappeared') for ds,v in hard.get('datasets',{}).items()}),
        f'CRIB: {crib}',f'I2_COMPLEMENT_TO_I1: {complement}',
        'CORA_TEST: '+json.dumps(tests.get('datasets',{}).get('cora',{'state':'NOT_RUN','reason':reason}).get('effects',{'state':'NOT_RUN','reason':reason})),
        'PUBMED_TEST: '+json.dumps(tests.get('datasets',{}).get('pubmed',{'state':'NOT_RUN','reason':reason}).get('effects',{'state':'NOT_RUN','reason':reason})),
        'CITESEER: '+str(third.get('decision',third.get('state'))),f'FINAL_INNOVATION_2_STATUS: {decision}',
        'PRIMARY_ARTIFACT: HYPERGRAPH_RESEARCH/CHRI_V18/FINAL_REPORT.md',
        'NEXT_EXPECTED_STEP: '+('freeze Innovation 2 and prepare handbook' if decision=='CHRI_AND_CRIB_VALIDATED' else
            'stop this direction and return to Innovation 2 search' if decision=='CHRI_KILL' else
            'review whether a new method contribution is still needed; do not freeze an unsupported module')]
    (OUT/'C2C_HANDOFF.md').write_text('\n'.join(handoff)+'\n',encoding='utf-8')
    if state=='COMPLETE':
        result_folder=REPO/'result/innovation2/CHRI_V18';result_folder.mkdir(parents=True,exist_ok=True)
        for p in OUT.glob('*'):
            if p.is_file() and p.suffix in ('.json','.md'):shutil.copy2(p,result_folder/p.name)
        write(OUT/'status.json',{'state':'COMPLETE','decision':decision,'reason':reason,'ended_at':time.time(),
              'test_accessed':tests.get('state')=='COMPLETE','innovation1_unchanged':True})
        print('V18_COMPLETE',decision,reason,flush=True)


def finish(decision,reason):
    report('COMPLETE',decision,reason)


def module_and_orth(ds,seeds,crib=None,third=False):
    module_phase='CM' if third else 'M';orth_phase='CO' if third else 'O'
    batch([('run',module_phase,d,seed,arm,10) for d in ds for seed in seeds for arm in MODULE_ARMS],
          'CRIB_THIRD' if third else 'CRIB_MODULE')
    result=summarize(module_phase,ds,seeds,MODULE_ARMS)
    if crib is None:crib=result['all_pass']
    arm='O3_CRIB' if crib else 'O3_RAW'
    batch([('run',orth_phase,d,seed,a,10) for d in ds for seed in seeds for a in ('O1',arm)],
          'ORTHOGONALITY_THIRD' if third else 'I1_I2_ORTHOGONALITY')
    orth=orthogonality_summary(ds,seeds,crib,orth_phase,module_phase)
    return result,orth,crib


def final_test(datasets,crib):
    candidates=[('test-prepare',ds,seed) for ds in datasets for seed in range(3 if ds=='citeseer' else 5)]
    batch(candidates,'ONE_SHOT_TEST_FEATURES',parallel=2)
    jobs=[]
    for ds in datasets:
        phase='CM' if ds=='citeseer' else 'M';op='CO' if ds=='citeseer' else 'O'
        refs={'T0':(phase,'M0'),'T1':(op,'O1'),'T2':(phase,'M3' if crib else 'M1'),
              'T3':(op,'O3_CRIB' if crib else 'O3_RAW'),'T4':(phase,'M4')}
        for seed in range(3 if ds=='citeseer' else 5):
            jobs.extend([('test',ds,seed,label,p,arm) for label,(p,arm) in refs.items()])
    batch(jobs,'ONE_SHOT_TEST',parallel=3)
    return test_summary(datasets,{ds:list(range(3 if ds=='citeseer' else 5)) for ds in datasets})


def supervise():
    try:
        check_frozen();report('RUNNING','PENDING','Phase A execution; test remains sealed.')
        execute_phase('A',('cora','pubmed'),[0,1,2],5,ARMS)
        update_leakage()
        a=summarize('A',('cora','pubmed'),[0,1,2],ARMS)
        write(OUT/'03_PHASE_A_RESULTS.json',a)
        if not a['all_pass']:
            passed=[ds for ds,item in a['datasets'].items() if item['pass']]
            subtype='CHRI_TRANSFER_WEAK' if len(passed)==1 else 'CHRI_EARLY_REJECT'
            finish('CHRI_KILL',f'{subtype}: strict dual-dataset Phase A gate failed; no rescue or test.');return
        execute_phase('B',('cora','pubmed'),list(range(5)),10,ARMS)
        formal=summarize('B',('cora','pubmed'),list(range(5)),ARMS)
        write(OUT/'04_PHASE_B_RESULTS.json',formal)
        if not formal['all_pass']:
            finish('CHRI_KILL','CHRI_NOT_CONFIRMED: Phase B primary CE/rank/control gate failed.');return
        batch([('conditional',ds,seed) for ds in ('cora','pubmed') for seed in range(5)],
              'CONDITIONAL_RELATION_DIAGNOSTIC',parallel=2)
        conditional={ds:[read(OUT/'diagnostics'/ds/f'seed_{seed}'/'conditional.json') for seed in range(5)] for ds in ('cora','pubmed')}
        write(OUT/'05_CONDITIONAL_RELATION_DIAGNOSTIC.json',{'state':'COMPLETE','datasets':conditional,'test_accessed':False})
        hard={ds:matched_hard_diagnostic(ds,list(range(5))) for ds in ('cora','pubmed')}
        write(OUT/'06_MATCHED_HARD_DIAGNOSTIC.json',{'state':'COMPLETE','datasets':hard,'test_accessed':False})
        if any(d['signal_completely_disappeared'] for d in hard.values()):
            finish('CHRI_KILL','CHRI_HEURISTIC_CONFOUND: CE and MRR signal disappears in matched-hard diagnostic.');return
        write(OUT/'PHENOMENON_CONFIRMED.json',{'state':'CHRI_PHENOMENON_CONFIRMED','test_accessed':False})
        modules,orth,crib=module_and_orth(('cora','pubmed'),list(range(5)))
        write(OUT/'08_CRIB_RESULTS.json',modules);write(OUT/'09_I1_I2_ORTHOGONALITY.json',orth)
        if orth['I2_COMPLEMENT_TO_I1']!='YES':
            finish('CHRI_SUPPORTED_BUT_NOT_COMPLEMENTARY_TO_I1','Validation phenomenon survives, but O3 does not exceed O1 in both datasets. Test remains sealed.');return
        # Citeseer is first accessed for V18 only after dual-dataset final validation succeeds.
        execute_phase('C',('citeseer',),[0,1,2],10,ARMS)
        third=summarize('C',('citeseer',),[0,1,2],ARMS)
        third_result={'state':'COMPLETE','validation':third,'validation_pass':False,
                      'decision':'CITESEER_CHRI_TRANSFER_NOT_SUPPORTED','reason':'Third-dataset pre-registered gate failed; no test.'}
        if third['all_pass']:
            cm,co,_=module_and_orth(('citeseer',),[0,1,2],crib,True)
            selected='M3_vs_M1' if crib else 'M1_vs_M0'
            effect=cm['datasets']['citeseer']['effects'][selected]
            method_pass=effect['ce']['mean']>0 and effect['mrr']['mean']>0
            third_result.update(module_results=cm,orthogonality=co,
                                validation_pass=method_pass and co['I2_COMPLEMENT_TO_I1']=='YES')
            if third_result['validation_pass']:
                third_result.update(decision='CITESEER_CHRI_VALIDATION_SUPPORTED',reason='Frozen-method transfer and complementarity gates passed.')
        write(OUT/'11_THIRD_DATASET.json',third_result)
        checkpoints={str(p.relative_to(OUT)):sha(p) for p in (OUT/'runs').rglob('final.pt')}
        write(OUT/'TEST_UNSEAL.json',{'allowed':True,'phenomenon':True,'i2_complement_to_i1':True,
            'selected_method':'CRIB' if crib else 'raw R_CAT','configuration_sha256':sha(OUT/'RUN_MANIFEST.json'),
            'v18_sources':read(OUT/'SOURCE_HASHES.json')['v18_source_files'],'checkpoints':checkpoints,
            'opened_at':time.time(),'test_epochs':10,'no_further_training_or_tuning':True})
        datasets=('cora','pubmed')+(('citeseer',) if third_result['validation_pass'] else ())
        tests=final_test(datasets,crib);write(OUT/'10_TEST_RESULTS.json',tests)
        if 'citeseer' in tests['datasets']:
            third_result['test']=tests['datasets']['citeseer'];write(OUT/'11_THIRD_DATASET.json',third_result)
        primary_pass=all(tests['datasets'][ds]['pass'] for ds in ('cora','pubmed'))
        if not primary_pass:
            finish('CHRI_KILL','Frozen final test failed the pre-registered directional CE/MRR and correspondence confirmation.');return
        if crib:
            finish('CHRI_AND_CRIB_VALIDATED','Both supported datasets pass validation, complementary frozen-I1 test, and true-vs-shuffle contrasts.')
        else:
            finish('CHRI_PHENOMENON_SUPPORTED\nMODULE_INNOVATION_NOT_ESTABLISHED','Generic relation phenomenon supported; CRIB failed to exceed raw relation in dual-dataset validation.')
    except BaseException as error:
        for item in CHILDREN:
            if item['proc'].poll() is None:
                try:os.killpg(item['proc'].pid,__import__('signal').SIGTERM)
                except ProcessLookupError:pass
        leakage=read(OUT/'01_LEAKAGE_AUDIT.json')
        failed={'state':'INVALID_EXPERIMENT' if leakage.get('state')=='INVALID_EXPERIMENT' else 'EXECUTION_FAILED',
                'error':repr(error),'traceback':traceback.format_exc(),'ended_at':time.time()}
        write(OUT/'ERROR.json',failed);write(OUT/'status.json',failed)
        print('V18_EXECUTION_FAILED',repr(error),flush=True);raise


if __name__=='__main__':
    command=sys.argv[1]
    if command=='preflight':preflight()
    elif command=='structure':prepare_structure(sys.argv[2])
    elif command=='prepare':
        ds,seed,epochs=sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
        prepare_backbone(ds,seed,epochs);prepare_matching(ds,seed,epochs)
    elif command=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif command=='conditional':conditional_diagnostic(sys.argv[2],int(sys.argv[3]))
    elif command=='test-prepare':prepare_test(sys.argv[2],int(sys.argv[3]))
    elif command=='test':test_run(sys.argv[2],int(sys.argv[3]),sys.argv[4],sys.argv[5],sys.argv[6])
    elif command=='supervise':supervise()
    else:raise ValueError(command)
