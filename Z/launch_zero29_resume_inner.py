import subprocess
from pathlib import Path
repo=Path('/home/ubuntu/lchr_v2')
script=repo/'HYPERGRAPH_RESEARCH/HDP_ZERO_V29/scripts/zero29.py'
root=repo/'HYPERGRAPH_RESEARCH/HDP_ZERO_V29'
with (root/'supervisor.log').open('a') as log:
    p=subprocess.Popen(['/home/ubuntu/anaconda3/envs/mei_env/bin/python','-B','-u',str(script),'resume_inner'],cwd=repo,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
print('DETACHED_V29_INNER_SUPERVISOR_PID',p.pid,flush=True)
