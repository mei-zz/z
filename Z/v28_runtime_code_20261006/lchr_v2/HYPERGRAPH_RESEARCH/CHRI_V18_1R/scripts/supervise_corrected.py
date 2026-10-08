import json,os,pathlib,subprocess,sys,time
repo=pathlib.Path('/home/ubuntu/lchr_v2');audit=repo/'HYPERGRAPH_RESEARCH/CHRI_V18_1R';script=audit/'scripts/corrected_run.py';out=audit/'runA';logdir=audit/'corrected_logs';logdir.mkdir(exist_ok=True)
jobs=[(ds,seed,arm) for ds,seeds in [('pubmed',[0,1,2]),('cora',[0])] for seed in seeds for arm in ['A1','A2','A3']]
env=os.environ.copy();env.update({'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','CUBLAS_WORKSPACE_CONFIG':':4096:8'})
status={'state':'RUNNING','jobs':jobs,'parallel':3,'test_accessed':False,'started_at':time.time()};(audit/'CORRECTED_REPRODUCTION_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
queue=list(jobs);active=[]
while queue or active:
 while queue and len(active)<3:
  ds,seed,arm=queue.pop(0);lp=(logdir/f'{ds}_{seed}_{arm}.log').open('w');p=subprocess.Popen([sys.executable,str(script),ds,str(seed),arm],cwd=repo,env=env,stdout=lp,stderr=subprocess.STDOUT,start_new_session=True);active.append((ds,seed,arm,p,lp))
 for item in list(active):
  ds,seed,arm,p,lp=item
  if p.poll() is not None:
   lp.close();active.remove(item)
   if p.returncode:
    status.update(state='FAILED',error={'job':[ds,seed,arm],'returncode':p.returncode,'log':str(logdir/f'{ds}_{seed}_{arm}.log')},ended_at=time.time());(audit/'CORRECTED_REPRODUCTION_STATUS.json').write_text(json.dumps(status,indent=2)+'\n');raise RuntimeError(status['error'])
   status['completed']=status.get('completed',[])+[[ds,seed,arm]]
 status.update(active=[[ds,seed,arm,p.pid] for ds,seed,arm,p,_ in active],queued=len(queue),updated_at=time.time());(audit/'CORRECTED_REPRODUCTION_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
 time.sleep(1)
status.update(state='COMPLETE',ended_at=time.time(),active=[],queued=0);(audit/'CORRECTED_REPRODUCTION_STATUS.json').write_text(json.dumps(status,indent=2)+'\n');print('CORRECTED_REPRODUCTION_COMPLETE',len(status['completed']),flush=True)
