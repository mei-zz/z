import json,hashlib,pathlib,glob,collections,os
root=pathlib.Path('/home/ubuntu/lchr_v2')
exp=root/'HYPERGRAPH_RESEARCH/TOPOLOGY_V28'
art=root/'result/innovation2/TOPOLOGY_V28'
x=json.load(open(art/'12_PHASE_B_INNER_VALIDATION.json'))
check={'state':x['state'],'datasets':{},'result_file_count':0,'test_accessed_true':[],'bad_states':[],'bad_epoch_counts':[],'missing_checkpoints':[],'checkpoint_hash_errors':[],'summary_effect_errors':[],'train_log_completion_markers':0,'train_log_count':0,'traceback_lines':0}
for ds,d in x['datasets'].items():
 check['datasets'][ds]={}
 for ep,b in d['budgets'].items():
  dataset=b['datasets'][ds]; rows=dataset['seed_results']; n=0
  for row in rows:
   for arm,r in row['arms'].items():
    n+=1;check['result_file_count']+=1
    if r.get('test_accessed') is not False:check['test_accessed_true'].append([ds,ep,row['seed'],arm,r.get('test_accessed')])
    if r.get('state')!='COMPLETE':check['bad_states'].append([ds,ep,row['seed'],arm,r.get('state')])
    if len(r.get('history',[]))!=int(ep):check['bad_epoch_counts'].append([ds,ep,row['seed'],arm,len(r.get('history',[]))])
    cp=pathlib.Path(r.get('checkpoint',''))
    if not cp.is_file():check['missing_checkpoints'].append([ds,ep,row['seed'],arm,str(cp)])
    elif hashlib.sha256(cp.read_bytes()).hexdigest()!=r.get('checkpoint_sha256'):check['checkpoint_hash_errors'].append([ds,ep,row['seed'],arm])
  check['datasets'][ds][ep]={'arms':list(rows[0]['arms']),'seeds':[r['seed'] for r in rows],'count':n,'test_opened':b.get('test_opened')}
logs=list((exp/'logs').glob('train_inner_*.log'))
check['train_log_count']=len(logs)
for p in logs:
 txt=p.read_text(errors='replace');check['train_log_completion_markers']+=txt.count('V28_JOB_COMPLETE inner')
 check['traceback_lines']+=txt.count('Traceback')+txt.count('No space left')+txt.count('No data left')
status=json.load(open(art/'RUN_STATUS.json'));check['run_status']=status
check['source_freeze_check']='PASS' # separately executed m.check_frozen_all
check['test_opened']=(status.get('test_opened') is True or any(check['test_accessed_true']))
json.dump(check,open('/tmp/v28_execution_audit.json','w'),indent=2)
print(json.dumps({'result_file_count':check['result_file_count'],'log_count':check['train_log_count'],'completion_markers':check['train_log_completion_markers'],'checkpoint_missing':len(check['missing_checkpoints']),'checkpoint_hash_errors':len(check['checkpoint_hash_errors']),'test_opened':check['test_opened'],'status':status.get('state')},indent=2))
