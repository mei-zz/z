import subprocess
from pathlib import Path
repo=Path('/home/ubuntu/lchr_v2');root=repo/'HYPERGRAPH_RESEARCH/CRM_V26'
with (root/'supervisor.log').open('a') as log:
    p=subprocess.Popen(['/home/ubuntu/anaconda3/envs/mei_env/bin/python','-B','-u',str(root/'scripts/crm26.py'),'supervise'],cwd=repo,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
print('DETACHED_SUPERVISOR_PID',p.pid,flush=True)
