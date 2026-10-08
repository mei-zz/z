from pathlib import Path
import tarfile,shutil
src=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\result\innovation2\TOPOLOGY_V28')
stage=Path(r'E:\Z\v28_review_update_stage_20261006b');base=stage/'lchr_v2'/'result'/'innovation2'/'TOPOLOGY_V28';base.mkdir(parents=True,exist_ok=False)
files=['V28_FINAL_RESEARCH_REVIEW.md','V28_FINAL_REVIEW_CURRENT_STATE.json','V28_FINAL_REVIEW_EVIDENCE_AUDIT.json','V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json','V28_INNER_FEATURE_AUDIT.json','V28_FINAL_REVIEW_PRE_INNER_EVIDENCE_AUDIT_20261006.json','V28_FINAL_REVIEW_PRE_INNER_CURRENT_STATE_20261006.json']
for name in files:shutil.copy2(src/name,base/name)
readme=stage/'V28_REVIEW_UPDATE_README.txt';readme.write_text('Overlay this archive after V28_inner_experiment_20261006.tar.gz. It contains the final review and current audit snapshots. Restore under /home/ubuntu/lchr_v2 on the server or under the local DCDLP-main project root. The PRE_INNER audit is retained as historical snapshot.\n',encoding='utf-8')
arc=Path(r'E:\Z\DCDLP_Server_Backup_20261005\V28_final_review_update_20261006.tar.gz')
with tarfile.open(arc,'w:gz') as t:
 t.add(base,arcname='lchr_v2/result/innovation2/TOPOLOGY_V28')
 t.add(readme,arcname='V28_REVIEW_UPDATE_README.txt')
print('archive_bytes',arc.stat().st_size)

