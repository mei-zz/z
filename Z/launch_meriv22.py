import subprocess
from pathlib import Path
repo=Path('/home/ubuntu/lchr_v2')
script=repo/'HYPERGRAPH_RESEARCH/MERI_V22/scripts/meri22.py'
with (script.parents[1]/'supervisor.log').open('w') as logfile:
    p=subprocess.Popen(['/home/ubuntu/anaconda3/envs/mei_env/bin/python','-B','-u',str(script),'supervise'],cwd=repo,stdin=subprocess.DEVNULL,stdout=logfile,stderr=subprocess.STDOUT,start_new_session=True)
print('MERI_SUPERVISOR_PID',p.pid)
