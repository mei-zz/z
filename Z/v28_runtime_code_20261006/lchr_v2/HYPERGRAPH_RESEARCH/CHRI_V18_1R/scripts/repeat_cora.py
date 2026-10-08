import os,pathlib,subprocess,sys,time,json
repo=pathlib.Path('/home/ubuntu/lchr_v2');audit=repo/'HYPERGRAPH_RESEARCH/CHRI_V18_1R';logdir=audit/'cora_repeat_logs';logdir.mkdir(exist_ok=True)
env=os.environ.copy();env.update({'CHRI_CORRECTED_OUT':str(audit/'runB'),'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','CUBLAS_WORKSPACE_CONFIG':':4096:8'})
active=[]
for arm in ['A1','A2','A3']:
 f=(logdir/f'cora_0_{arm}.log').open('w');p=subprocess.Popen([sys.executable,str(audit/'scripts/corrected_run.py'),'cora','0',arm],cwd=repo,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True);active.append((arm,p,f))
while active:
 for item in list(active):
  arm,p,f=item
  if p.poll() is not None:
   f.close();active.remove(item)
   if p.returncode:raise RuntimeError((arm,p.returncode))
print('CORA_REPEAT_COMPLETE',flush=True)
