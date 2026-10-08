"""Stop only this chat's V30B supervisor and its descendants on old deployment."""
import os,signal,time,json
from pathlib import Path
root=Path('/home/ubuntu/lchr_v2')
pid=int((root/'HYPERGRAPH_RESEARCH/PBD_V30B/supervisor.pid').read_text())
cmd=Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0',b' ')
assert b'PBD_V30B/scripts/run30b.py supervise' in cmd
children={}
for proc in Path('/proc').iterdir():
    if not proc.name.isdigit():continue
    try:
        stat=(proc/'stat').read_text();ppid=int(stat[stat.rfind(')')+2:].split()[1])
        children.setdefault(ppid,[]).append(int(proc.name))
    except (FileNotFoundError,ProcessLookupError):pass
owned=[]
def visit(parent):
    for child in children.get(parent,[]):visit(child);owned.append(child)
visit(pid)
os.kill(pid,signal.SIGSTOP)
for child in owned:
    try:os.kill(child,signal.SIGTERM)
    except ProcessLookupError:pass
os.kill(pid,signal.SIGTERM);os.kill(pid,signal.SIGCONT)
time.sleep(1)
for child in owned:
    try:os.kill(child,signal.SIGKILL)
    except ProcessLookupError:pass
art=root/'result/innovation2/PBD_V30B'
(art/'RUN_STATUS.json').write_text(json.dumps({'state':'STOPPED_RELOCATING','reason':'Wrong old deployment selected; user requested10.16.15.66, now moving execution','terminated_supervisor':pid,'terminated_descendants':owned,'test_opened':False},indent=2)+'\n')
(root/'HYPERGRAPH_RESEARCH/PBD_V30B/SUPERVISOR_LOCK').unlink(missing_ok=True)
print('ONLY_MISROUTED_V30B_STOPPED',pid,owned)
