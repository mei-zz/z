import hashlib,json,pathlib,subprocess,sys,tempfile
import numpy as np
REPO=pathlib.Path('/home/ubuntu/lchr_v2');OLD=REPO/'HYPERGRAPH_RESEARCH/CHRI_V18';NEW=REPO/'HYPERGRAPH_RESEARCH/CHRI_V18_1';OUT=REPO/'HYPERGRAPH_RESEARCH/CHRI_V18_1R';OUT.mkdir(parents=True,exist_ok=True)
CHILD=r'''import hashlib,json,pathlib,sys,numpy as np
repo=pathlib.Path('/home/ubuntu/lchr_v2');old=repo/'HYPERGRAPH_RESEARCH/CHRI_V18';new=repo/'HYPERGRAPH_RESEARCH/CHRI_V18_1';sys.path.insert(0,str(old/'scripts'));import chri_v18 as v
phase,arm,out=sys.argv[1],sys.argv[2],pathlib.Path(sys.argv[3]);v.OUT=old if phase=='old' else new;net=v.load_net('A' if phase=='old' else 'R','pubmed',0,arm);p=out.with_suffix('.npz');v.evaluate(net,'pubmed',0,save=p)
with np.load(p) as z:
 s=np.r_[z['positive'].ravel(),z['negative'].ravel()].astype(np.float32);q=len(z['positive']);neg=z['negative'].shape[1]
np.save(out,s)
print(json.dumps({'sha256':hashlib.sha256(s.tobytes()).hexdigest(),'metrics':v.metrics(s,q,neg),'q':q,'negatives':neg,'score_min':float(s.min()),'score_max':float(s.max())}))
'''
def run_eval(phase,arm,tag):
 tmp=pathlib.Path(tempfile.mkstemp(prefix='chri18_1r_',suffix='.npy',dir='/tmp')[1]);tmp.unlink()
 if tag=='fresh':rec=json.loads(subprocess.check_output([sys.executable,'-c',CHILD,phase,arm,str(tmp)],text=True,stderr=subprocess.DEVNULL).strip().splitlines()[-1]);scores=np.load(tmp)
 else:
  import sys as _sys;_sys.path.insert(0,str(OLD/'scripts'));import chri_v18 as v;v.OUT=OLD if phase=='old' else NEW
  if not hasattr(run_eval,'nets'):run_eval.nets={}
  key=(phase,arm)
  if key not in run_eval.nets:run_eval.nets[key]=v.load_net('A' if phase=='old' else 'R','pubmed',0,arm)
  v.evaluate(run_eval.nets[key],'pubmed',0,save=tmp.with_suffix('.npz'))
  with np.load(tmp.with_suffix('.npz')) as z:scores=np.r_[z['positive'].ravel(),z['negative'].ravel()].astype(np.float32);q=len(z['positive']);neg=z['negative'].shape[1]
  rec={'sha256':hashlib.sha256(scores.tobytes()).hexdigest(),'metrics':v.metrics(scores,q,neg),'q':q,'negatives':neg,'score_min':float(scores.min()),'score_max':float(scores.max())}
 for q in (tmp,tmp.with_suffix('.npz')):
  try:q.unlink()
  except OSError:pass
 return rec,scores
result={'state':'COMPLETE','dataset':'pubmed','seed':0,'test_accessed':False,'arms':{}}
for phase in ('old','new'):
 for arm in ('A1','A2','A3'):
  row={}
  for mode,tag in (('same_process','same'),('fresh_process','fresh')):
   entries=[];vectors=[]
   for _ in range(10):rec,score=run_eval(phase,arm,tag);entries.append(rec);vectors.append(score)
   ref=vectors[0]
   row[mode]={'runs':entries,'unique_score_hashes':len(set(x['sha256'] for x in entries)),'max_abs_score_difference_from_first':[float(np.max(np.abs(x-ref))) for x in vectors],'max_abs_score_difference_any_pair':float(max(np.max(np.abs(x-y)) for i,x in enumerate(vectors) for y in vectors[i+1:])),'metrics_max_ce_range':max(x['metrics']['ce'] for x in entries)-min(x['metrics']['ce'] for x in entries),'metrics_max_mrr_range':max(x['metrics']['mrr'] for x in entries)-min(x['metrics']['mrr'] for x in entries)}
  result['arms'][phase+'_'+arm]=row
(OUT/'02_CHECKPOINT_EVAL_REPEATABILITY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:{m:{'unique_hashes':v[m]['unique_score_hashes'],'max_score_abs':v[m]['max_abs_score_difference_any_pair'],'ce_range':v[m]['metrics_max_ce_range'],'mrr_range':v[m]['metrics_max_mrr_range']} for m in v} for k,v in result['arms'].items()},indent=2))
