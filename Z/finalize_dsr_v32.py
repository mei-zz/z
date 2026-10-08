import sys, shutil
from pathlib import Path
sys.path.insert(0, '/home/zhoulihui/DCDLP-main/HYPERGRAPH_RESEARCH/DSR_V32/scripts')
import run32 as r
r.install_paths()
status=r.p.read(r.ART/'RUN_STATUS.json')
if status.get('state')!='EXECUTION_FAILED' or "KeyError('A6')" not in status.get('error',''):
    raise RuntimeError('Unexpected run status; refusing finalization recovery')
shutil.copy2(r.ART/'RUN_STATUS.json', r.ART/'FINALIZATION_FAILURE_EVIDENCE.json')
primary=r.p.read(r.ART/'05_PHASE_A_RESULTS.json')
rep=r.p.read(r.ART/'08_PHASE_B_RESULTS.json')
transfer=r.p.read(r.ART/'09_CITESEER_TRANSFER.json')
inner=r.p.read(r.ART/'10_INNER_VALIDATION.json')
gate=r.p.read(r.ART/'PHASE_A_GATE.json')['nominated']
diag=r.p.read(r.ART/'07_ROUTER_DIAGNOSTICS.json')
fixed={ds:{'A6':{'A6': arms['A6']}} for ds,arms in diag.items()}
r.finalize(primary,rep,transfer,inner,gate,fixed)
with open(r.ART/'POSTPROCESS_RECOVERY.md','w',encoding='utf-8') as f:
    f.write('# V32 post-processing recovery\n\nAll predeclared training jobs completed. The original supervisor failed only while assembling the final report due to a diagnostics dictionary key error (`KeyError: A6`). Original failure evidence is preserved in `FINALIZATION_FAILURE_EVIDENCE.json`. The existing Phase A, Phase B, Citeseer transfer, and inner-validation artifacts were reused without retraining. Finalization was rerun with the already recorded router-collapse fields mapped to the expected report shape. Test data remained unopened.\n')
print('POSTPROCESS_RECOVERY=PASS')
print('STATUS='+str(r.p.read(r.ART/'RUN_STATUS.json').get('state')))
