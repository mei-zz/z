import json,time,traceback,hashlib
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parents[1];PARENT=OUT.parent/'R_HSPE_BENCHMARK_V17_3'
def read(p):return json.loads(Path(p).read_text())
def write(p,obj):
 p=Path(p);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2,allow_nan=False));tmp.replace(p)
def finish():
 r=read(OUT/'results.json');a=r.get('A');b=r.get('B');third=r.get('third');test=r.get('test');latest=b or a
 fields={'R_HSPE_FROZEN':True,'INNOVATION_1':r['INNOVATION_1'],'COMPLEMENTARY_SIGNAL':'SUPPORTED' if r['INNOVATION_1']=='PAPER_READY' else 'NOT_SUPPORTED','TEST':'COMPLETE' if test else 'OFF','NEXT_EXPECTED_STEP':'Retrieve evidence and decide next research steps. No automatic Innovation2.','MECHANISM':'CONTEXT_DRIVEN','SIZE_CAUSAL_CLAIM':'NOT_SUPPORTED','paired_rng_audit':'Recorded hash equality of base initialization, official negative samples, permutations and CUDA RNG states; checked before promotion'}
 costs={};validation={}
 if latest:
  for ds,rows in latest['seed_results'].items():
   validation[ds]={};costs[ds]={}
   for arm in rows[0]['arms']:
    values=[row['arms'][arm] for row in rows]
    validation[ds][arm]={k:{'mean':float(np.mean([v['validation'][k] for v in values])),'std':float(np.std([v['validation'][k] for v in values],ddof=1))} for k in ('mrr','hits10','hits20','mean_positive_rank')}
    costs[ds][arm]={'parameters':values[0]['parameters'],'added_parameters':values[0]['added_parameters'],'percentage_overhead':values[0]['percentage_overhead'],'mean_train_seconds':float(np.mean([v['train_seconds'] for v in values])),'mean_validation_inference_seconds_per_epoch':float(np.mean([v['validation_seconds']/v['epochs'] for v in values])),'mean_wall_seconds':float(np.mean([v['wall_seconds'] for v in values])),'max_peak_gpu_mb':max(v['peak_gpu_mb'] for v in values)}
  for name,arm in [('NCN_BASELINE','N0'),('NCN_PLUS_R_HSPE','N1'),('NCNC_BASELINE','C0'),('NCNC_PLUS_R_HSPE','C1'),('PARAM_NULL','C2')]:fields[name]={ds:item[arm] for ds,item in validation.items() if arm in item}
  for ds in ('cora','pubmed'):
   fields[ds.upper()+'_DELTA']=latest['effects'][ds]
  fields['SEED_WINS']={ds:{name:eff['wins'] for name,eff in item.items()} for ds,item in latest['effects'].items()}
  fields['BACKBONE_INDEPENDENT']='SUPPORTED_FORMAL_VALIDATION' if b and b['backbone_independent'] else 'POSITIVE_PHASE_A_ONLY' if a and a['backbone_independent'] else 'NOT_SUPPORTED'
 fields['CITESEER_DELTA']=third['effects']['citeseer'] if third else 'NOT_REACHED'
 fields['PARAMETER_OVERHEAD']={ds:{arm:{k:v[k] for k in ('parameters','added_parameters','percentage_overhead')} for arm,v in item.items()} for ds,item in costs.items()}
 fields['RUNTIME_OVERHEAD']=costs
 fields['FEATURE_CACHE_TIME']={}
 for p in (OUT/'phases').glob('*/*/FEATURE_READY.json'):
  row=read(p);fields['FEATURE_CACHE_TIME'][row['phase']+'/'+row['dataset']]=row['feature_cache_seconds']
 if latest:
  overhead={}
  for ds,c in costs.items():
   overhead[ds]={}
   for augmented,baseline in [('N1','N0'),('C1','C0'),('C2','C0')]:
    if augmented in c and baseline in c:overhead[ds][augmented+'_vs_'+baseline]={'train_seconds_delta':c[augmented]['mean_train_seconds']-c[baseline]['mean_train_seconds'],'train_time_ratio':c[augmented]['mean_train_seconds']/c[baseline]['mean_train_seconds'],'mean_validation_inference_seconds_delta':c[augmented]['mean_validation_inference_seconds_per_epoch']-c[baseline]['mean_validation_inference_seconds_per_epoch']}
  fields['RUNTIME_OVERHEAD_COMPARISONS']=overhead
 if test:
  fields['ONE_SHOT_TEST']=test;fields['TEST_SUPPORT']=test['passes']
  entries=read(PARENT/'results.json')['summary'];combined={};ranks={}
  for ds,rows in entries.items():
   combined[ds]={}
   for method,item in rows.items():
    combined[ds][method+' [V17.3]']={'metrics':item['metrics'],'n':item['n'],'epochs':100 if method in ('NCN','NCNC') else 5000 if method=='NSLR-HMANN' else 10,'source':'V17.3 exact frozen candidate/evaluator','parameters':item['parameters']}
   if ds in test['datasets']:
    item=test['datasets'][ds]
    for arm,m in item['metrics'].items():
     phase='third' if ds=='citeseer' else 'B';ref=read(OUT/'phases'/phase/ds/'seed_0'/arm/'result.json')
     label={'N0':'NCN','N1':'NCN + R-HSPE','C0':'NCNC','C1':'NCNC + R-HSPE','C2':'NCNC + NULL75'}[arm]+' [V17.4,10 epochs]'
     combined[ds][label]={'metrics':m,'n':len(item['seeds']),'epochs':10,'source':'V17.4 one-shot test final10epochs','parameters':ref['parameters']}
   order=sorted(combined[ds],key=lambda key:combined[ds][key]['metrics']['mrr']['mean'],reverse=True);ranks[ds]={key:i+1 for i,key in enumerate(order)}
  fields['MAIN_TABLE_RANK']=ranks
  write(OUT/'COMBINED_MAIN_TABLE.json',{'datasets':combined,'ranks':ranks,'caveat':'Same candidate/evaluator, different official training budgets as disclosed by epoch column; plug-in causal contrasts use matched10-epoch baseline. Ranking is descriptive, not a claim of equal compute or SOTA.'})
  lines=['# Combined publication audit table','','Frozen V17.3 rows plus V17.4 one-shot test rows. Epoch budgets are explicit; all share the frozen candidates/evaluator. Plug-in effects use matched10-epoch rows, and the matched table is retained in06_MATCHED_MAIN_TABLE.md. No SOTA claim.','','| Dataset | Method | Epochs | Seeds | MRR mean±SD | Params | Descriptive rank |','|---|---|---:|---:|---:|---:|---:|']
  for ds,items in combined.items():
   for name in sorted(items,key=lambda key:ranks[ds][key]):
    row=items[name];mm=row['metrics']['mrr'];lines.append('| '+ds+' | '+name+f" | {row['epochs']} | {row['n']} | {mm['mean']:.6f} ± {mm['std']:.6f} | {row['parameters']} | {ranks[ds][name]} |")
  p=OUT/'06_MAIN_TABLE.md';(OUT/'06_MATCHED_MAIN_TABLE.md').write_text(p.read_text());p.write_text('\n'.join(lines)+'\n')
 else:fields['MAIN_TABLE_RANK']='NOT_REACHED_TEST_OFF'
 r['final_fields']=fields;write(OUT/'results.json',r)
 original=(OUT/'FINAL_REPORT.md').read_text();(OUT/'FINAL_REPORT.md').write_text(original+'\n\n## Required final fields and cost audit\n\n'+json.dumps(fields,indent=2)+'\n')
 handoff=['STATUS: EXECUTED','DIRECTION: R_HSPE_STRONG_BACKBONE_TRANSFER','R_HSPE: FROZEN','PHASE_A: '+('PASS' if a and a['all_pass'] else 'FAIL' if a else 'NOT_REACHED'),'PHASE_B: '+('PASS' if b and b['all_pass'] else 'FAIL' if b else 'NOT_REACHED'),'CORA: '+json.dumps(fields.get('CORA_DELTA','NOT_REACHED')),'PUBMED: '+json.dumps(fields.get('PUBMED_DELTA','NOT_REACHED')),'CITESEER: '+json.dumps(fields['CITESEER_DELTA']),'NCN_TRANSFER: '+fields.get('BACKBONE_INDEPENDENT','NOT_REACHED'),'NCNC_TRANSFER: '+r['decision'],'NULL_CONTROL: '+json.dumps({ds:v.get('delta_null') for ds,v in (latest['effects'] if latest else {}).items()}),'TEST: '+fields['TEST'],'PARAMETER_COST: '+json.dumps(fields['PARAMETER_OVERHEAD']),'COMPETITIVENESS: '+r['decision'],'INNOVATION_1: '+r['INNOVATION_1'],'DECISION: '+r['decision'],'NEXT_EXPECTED_STEP: retrieve evidence; user decides next research steps; no Innovation2']
 (OUT/'C2C_HANDOFF.md').write_text('\n'.join(handoff)+'\n')
 write(OUT/'FINALIZATION_STATUS.json',{'state':'COMPLETE','finished_at':time.time(),'results_sha256':hashlib.sha256((OUT/'results.json').read_bytes()).hexdigest()})
if __name__=='__main__':
 try:
  while True:
   state=read(OUT/'status.json')['state'] if (OUT/'status.json').exists() else 'RUNNING'
   if state!='RUNNING':break
   time.sleep(5)
  finish()
 except Exception as e:write(OUT/'FINALIZATION_ERROR.json',{'error':repr(e),'traceback':traceback.format_exc()});raise
