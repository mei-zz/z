import json
from pathlib import Path
p=Path('/home/zhoulihui/DCDLP-main/result/innovation2/DSR_V32')
status=json.loads((p/'RUN_STATUS.json').read_text())
assert status.get('state')=='COMPLETE'
assert status['decision'].get('MULTI_SOURCE_GAIN')=='REPLICATED'
status['decision']['MULTI_SOURCE_GAIN']='EXPLORATORY'
(p/'RUN_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
for name in ('11_DECISION.md','FINAL_REPORT.md'):
    f=p/name;s=f.read_text();old='MULTI_SOURCE_GAIN: REPLICATED';assert old in s,name
    f.write_text(s.replace(old,'MULTI_SOURCE_GAIN: EXPLORATORY'))
(p/'DECISION_CORRECTION.md').write_text('''# V32 decision aggregation correction\n\nThe first generated summary incorrectly labeled `MULTI_SOURCE_GAIN` as replicated because its aggregation checked whether A7 was nominated for a dataset with any replicated contrast, rather than whether A6−A7 itself replicated. Raw paired results show PubMed Phase B A6−A7 mean MRR = −0.00137762 (2/5 wins), so this contrast did not replicate. Phase A had a small positive PubMed mean (+0.00172649, 2/3 wins), and inner validation was positive (+0.00161579, 3/3); therefore the status is `EXPLORATORY`, not `REPLICATED`. No model, metric, checkpoint, or training artifact was changed; only the derived decision status and report text were corrected. Test remained unopened.\n''')
print('MULTI_SOURCE_GAIN=EXPLORATORY')
print('TRAINING_ARTIFACTS_MODIFIED=NO')
