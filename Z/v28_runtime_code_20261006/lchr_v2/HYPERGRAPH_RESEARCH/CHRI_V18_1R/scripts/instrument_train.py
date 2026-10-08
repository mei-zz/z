import argparse,hashlib,json,pathlib,sys,time
import numpy as np
import torch

parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);args=parser.parse_args()
OUT=pathlib.Path(args.out);OUT.mkdir(parents=True,exist_ok=True)
REPO=pathlib.Path('/home/ubuntu/lchr_v2');OLD=REPO/'HYPERGRAPH_RESEARCH/CHRI_V18';NEW=REPO/'HYPERGRAPH_RESEARCH/CHRI_V18_1';AUDIT=REPO/'HYPERGRAPH_RESEARCH/CHRI_V18_1R'
if not (OUT/'SOURCE_HASHES.json').exists(): (OUT/'SOURCE_HASHES.json').symlink_to(NEW/'SOURCE_HASHES.json')
if not (OUT/'cache').exists(): (OUT/'cache').symlink_to(NEW/'cache',target_is_directory=True)
if not (AUDIT/'CHRI_V18').exists(): (AUDIT/'CHRI_V18').symlink_to(OLD,target_is_directory=True)
sys.path.insert(0,str(OLD/'scripts'));import chri_v18 as v
v.OUT=OUT

def tensorhash(t):
 x=t.detach().contiguous().cpu()
 return hashlib.sha256(str((tuple(x.shape),str(x.dtype))).encode()+x.numpy().tobytes()).hexdigest()
def modulehash(net):
 h=hashlib.sha256()
 for k,t in sorted(net.state_dict().items()): h.update(k.encode());h.update(tensorhash(t).encode())
 return h.hexdigest()
def optimizerhash(opt):
 h=hashlib.sha256(); names={id(p):n for n,p in current['model'].named_parameters()}
 for group_index,group in enumerate(opt.param_groups):
  for param_index,param in enumerate(group['params']):
   h.update(names.get(id(param),str((group_index,param_index))).encode())
   state=opt.state.get(param,{})
   for key,val in sorted(state.items()):
    h.update(str(key).encode())
    if torch.is_tensor(val): h.update(tensorhash(val).encode())
    else: h.update(repr(val).encode())
 return h.hexdigest()
def gradient_info(net):
 h=hashlib.sha256();sq=0.0;count=0
 for name,p in net.named_parameters():
  if p.grad is not None:
   h.update(name.encode());h.update(tensorhash(p.grad).encode());sq+=float(p.grad.detach().float().pow(2).sum().cpu());count+=p.grad.numel()
 return {'sha256':h.hexdigest(),'l2_norm':sq**0.5,'elements':count,'tensor_hashes':{name:tensorhash(p.grad) for name,p in net.named_parameters() if p.grad is not None}}
AUDIT_DS=__import__('os').environ.get('CHRI_FORENSIC_DATASET','pubmed');AUDIT_ARM=__import__('os').environ.get('CHRI_FORENSIC_ARM','A2')
TRACE={'state':'RUNNING','run_label':OUT.name,'dataset':AUDIT_DS,'seed':0,'arm':AUDIT_ARM,'test_accessed':False,'init':{},'optimizer_steps':[],'epoch_end':[]}
current={'model':None,'optimizer':None,'bucket':{'inputs':[],'outputs':[],'losses':[],'activations':[]}}

class FirstStepComplete(Exception):pass
OriginalAdam=torch.optim.Adam
class AuditAdam(OriginalAdam):
 def __init__(self,*a,**kw):
  super().__init__(*a,**kw);current['optimizer']=self
  TRACE['init']['optimizer_empty_state_sha256']=optimizerhash(self)
 def step(self,*a,**kw):
  net=current['model'];before_grad=gradient_info(net)
  row={'step':len(TRACE['optimizer_steps'])+1,'inputs_sha256':hashlib.sha256(''.join(current['bucket']['inputs']).encode()).hexdigest(),'input_microbatches':current['bucket']['inputs'],'logits_sha256':hashlib.sha256(''.join(current['bucket']['outputs']).encode()).hexdigest(),'logit_microbatches':current['bucket']['outputs'],'loss_sha256':hashlib.sha256(''.join(current['bucket']['losses']).encode()).hexdigest(),'loss_microbatches':current['bucket']['losses'],'gradient':before_grad,'activation_events':current['bucket']['activations']}
  result=super().step(*a,**kw)
  row['model_after_sha256']=modulehash(net);row['model_tensor_hashes']={name:tensorhash(value) for name,value in net.state_dict().items()};row['optimizer_after_sha256']=optimizerhash(self);TRACE['optimizer_steps'].append(row)
  if len(TRACE['optimizer_steps'])==1 and __import__('os').environ.get('CHRI_FORENSIC_STOP_AFTER_FIRST')=='1':
   (OUT/'state_trace.json').write_text(json.dumps(TRACE,indent=2)+'\n');raise FirstStepComplete()
  current['bucket']={'inputs':[],'outputs':[],'losses':[],'activations':[]}
  return result
torch.optim.Adam=AuditAdam
original_make=v.make_net
def tracked_make(*a,**kw):
 net=original_make(*a,**kw)
 if __import__('os').environ.get('CHRI_FORENSIC_SEGMENT_AGG')=='1':
  from deterministic_aggregation import install
  install(net)
 current['model']=net
 endpoint_method=getattr(net.endpoint,'__func__',net.endpoint)
 endpoint_globals=getattr(endpoint_method,'__globals__',{})
 for op_name in (('scatter_mean','scatter_max') if 'scatter_mean' in endpoint_globals else ()):
  original_op=endpoint_globals[op_name]
  def wrapper_factory(name,fn):
   def wrapped(*args,**kwargs):
    output=fn(*args,**kwargs);value=output[0] if isinstance(output,tuple) else output
    if __import__('os').environ.get('CHRI_FORENSIC_STOP_AFTER_FIRST')=='1' and not TRACE['optimizer_steps']:
     current['bucket']['activations'].append({'op':name,'output':tensorhash(value)})
    return output
   return wrapped
  endpoint_globals[op_name]=wrapper_factory(op_name,original_op)
 TRACE['init']['model_sha256']=modulehash(net)
 original_endpoint=net.endpoint
 def tracked_endpoint(pairs,side):
  result=original_endpoint(pairs,side)
  if __import__('os').environ.get('CHRI_FORENSIC_STOP_AFTER_FIRST')=='1' and not TRACE['optimizer_steps']:
   current['bucket']['activations'].append({'op':'endpoint','side':side,'latent':tensorhash(result[0]),'counts':tensorhash(result[1]),'pooled':tensorhash(result[2])})
  return result
 net.endpoint=tracked_endpoint
 original_representation=net.representation
 def tracked_representation(pairs,b,need_relation=True):
  result=original_representation(pairs,b,need_relation)
  if __import__('os').environ.get('CHRI_FORENSIC_STOP_AFTER_FIRST')=='1' and not TRACE['optimizer_steps']:
   current['bucket']['activations'].append({'op':'representation','z':tensorhash(result[0]),'r':tensorhash(result[1]) if result[1] is not None else None})
  return result
 net.representation=tracked_representation
 original_forward=net.forward
 def tracked_forward(pairs,b,donor=None):
  h=hashlib.sha256()
  for t in (pairs,b,donor):
   if t is not None:h.update(tensorhash(t).encode())
  current['bucket']['inputs'].append(h.hexdigest())
  out=original_forward(pairs,b,donor);current['bucket']['outputs'].append(tensorhash(out[0]));return out
 net.forward=tracked_forward
 return net
v.make_net=tracked_make
original_bce=torch.nn.functional.binary_cross_entropy_with_logits
def tracked_bce(input,target,*a,**kw):
 out=original_bce(input,target,*a,**kw)
 if torch.is_grad_enabled():current['bucket']['losses'].append(tensorhash(out))
 return out
torch.nn.functional.binary_cross_entropy_with_logits=tracked_bce
original_evaluate=v.evaluate
def tracked_evaluate(net,ds,seed,split='valid',save=None):
 metrics=original_evaluate(net,ds,seed,split,save)
 e=len(TRACE['epoch_end'])+1
 TRACE['epoch_end'].append({'epoch':e,'model_state_sha256':modulehash(net),'optimizer_state_sha256':optimizerhash(current['optimizer']),'validation':metrics,'optimizer_steps':len(TRACE['optimizer_steps']),'test_accessed':False})
 p=OUT/'state_trace.json';p.write_text(json.dumps(TRACE,indent=2)+'\n')
 return metrics
current['epoch_end']=TRACE['epoch_end']
v.evaluate=tracked_evaluate
started=time.time()
try:v.run('A',AUDIT_DS,0,AUDIT_ARM,5);TRACE['state']='COMPLETE'
except FirstStepComplete:TRACE['state']='FIRST_STEP_CAPTURED'
TRACE['wall_seconds']=time.time()-started
(OUT/'state_trace.json').write_text(json.dumps(TRACE,indent=2)+'\n')
print(json.dumps({'state':TRACE['state'],'run_label':OUT.name,'init':TRACE['init'],'epoch_end':TRACE['epoch_end'],'optimizer_steps':len(TRACE['optimizer_steps']),'wall_seconds':TRACE['wall_seconds'],'test_accessed':False},indent=2))














