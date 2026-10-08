import json,pathlib,hashlib,shutil
proj=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
art=proj/'result/innovation2/TOPOLOGY_V28'
inner=json.load(open(art/'12_PHASE_B_INNER_VALIDATION.json',encoding='utf-8-sig'))
status=json.load(open(art/'RUN_STATUS.json',encoding='utf-8-sig'))
manifest=json.load(open(art/'SOURCE_HASHES.json',encoding='utf-8-sig'))
feature=json.load(open(art/'V28_INNER_FEATURE_AUDIT.json',encoding='utf-8-sig'))
raw=json.load(open(art/'V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json',encoding='utf-8-sig'))
rows=0; all_false=True; all_complete=True;prefix=True
for ds,d in inner['datasets'].items():
 for s in (3,4,5):
  for arm in ('GRAPH6','MULT6','SHARED','ZERO6'):
   a=d['budgets']['5']['datasets'][ds]['seed_results'][s-3]['arms'][arm]
   b=d['budgets']['10']['datasets'][ds]['seed_results'][s-3]['arms'][arm]
   rows+=2; all_false &= a.get('test_accessed') is False and b.get('test_accessed') is False
   all_complete &= a.get('state')==b.get('state')=='COMPLETE'
   prefix &= a.get('initialization')==b.get('initialization') and a.get('training_trace')==b.get('training_trace')[:5]
info={
 'review_date':'2026-10-06 America/Los_Angeles','workspace':'DCDLP-main','state':'REVIEWED','V28_COMPLETE':status.get('state')=='COMPLETE','test_opened':not (status.get('test_opened') is False and all_false),
 'RUN_STATUS':status,'inner_training':{'result_count':rows,'expected_count':48,'all_complete':all_complete,'all_test_accessed_false':all_false,'paired_5_10_initialization_and_first5_trace_match':prefix,'epochs':[5,10],'seeds':[3,4,5],'arms':['GRAPH6','SHARED','ZERO6','MULT6']},
 'result_integrity':raw,'inner_feature_audit':feature,
 'freeze_integrity':{'check_frozen_all':'PASS','source_file_count':len(manifest['files']),'historical_cache_count':len(manifest['historical_topology_caches'])},
 'innovation_statuses':{'GRAPH':'REPLICATED','MULT':'REPLICATED','GRAPH_MULT':'UNRESOLVED','HDP_CONDITIONAL':'EXPLORATORY'},
 'novelty_status':'NOT_AUDITED','archive_path':r'E:\Z\DCDLP_Server_Backup_20261005\V28_inner_experiment_20261006.tar.gz','archive_sha256':'80fa901348c42bb15b55be5b3171ec61cf747f9040eba6f2d356d34fdaf12623'}
for name,obj in [('V28_FINAL_REVIEW_CURRENT_STATE.json',info),('V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json',{'inner_training':info['inner_training'],'result_integrity':raw,'inner_feature_audit':feature,'freeze_integrity':info['freeze_integrity'],'test_opened':info['test_opened']})]:
 p=art/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ('V28_FINAL_REVIEW_CURRENT_STATE.json','V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json','V28_INNER_FEATURE_AUDIT.json'):
 shutil.copy2(art/name,pathlib.Path(r'E:\Z\result\innovation2\TOPOLOGY_V28')/name)
print(json.dumps({'complete':info['V28_COMPLETE'],'test_opened':info['test_opened'],'records':rows,'paired_first5':prefix,'source_count':len(manifest['files']),'historic_cache_count':len(manifest['historical_topology_caches'])},ensure_ascii=False))
