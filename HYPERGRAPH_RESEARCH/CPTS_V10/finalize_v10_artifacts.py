import json
from pathlib import Path
root=Path(__file__).resolve().parent
rp=root/'results.json'; sp=root/'status.json'
r=json.loads(rp.read_text(encoding='utf-8'))
s=json.loads(sp.read_text(encoding='utf-8'))
r['study_status']='ALL_GATED_STAGES_COMPLETE'
r['final_decision']='GO'
r['paper_story_supported']='PARTIAL'
r['novelty_status']='EXACT_RULE_UNVERIFIED'
r['test_evaluated']=True
r['test_accessed']=True
r['efficiency_summary']={
 'extra_trainable_parameters':0,
 'extra_neural_forwards':0,
 'sorting_complexity':'O(M log M)',
 'change_point_scan_complexity':'O(M) per positive after prefix sums',
 'M':20,
}
r['final_gate_summary']={
 'cora_validation':r['cora_validation']['final_decision_at_validation'],
 'cora_test_supported':r['cora_test']['supported'],
 'pubmed_clear_reversal':r['pubmed']['clear_reversal'],
 'pubmed_cpts_vs_graph_hard_wins':r['pubmed']['cpts_paired_delta']['GRAPH_HARD']['wins'],
 'citeseer_cpts_vs_graph_hard_wins':r['citeseer']['cpts_paired_delta']['GRAPH_HARD']['wins'],
 'positive_backbones':r['backbone_generalization']['positive_backbone_count'],
 'cora_test_cpts_minus_matched_q_mean':r['cora_test']['paired_cpts_delta']['MATCHED_Q']['mean_delta'],
 'interpretation':'Registered GO gates pass. The held-out Cora Matched-Q result and PubMed QTHS25 / Citeseer SH75 reversals limit the paper claim; do not claim universal superiority or priority.'
}
rp.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
s.update({'state':'COMPLETE','stage':'ALL_GATED_STAGES','decision':'GO','cora_test_supported':True,'validation_training_jobs':12,'downstream_jobs':30,'total_v10_stage_jobs':42,'final_report_ready':True,'final_decision':'GO','paper_story_supported':'PARTIAL','no_active_training_jobs':True})
sp.write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'study_status':r['study_status'],'final_decision':r['final_decision'],'paper_story_supported':r['paper_story_supported'],'final_gate_summary':r['final_gate_summary'],'status':s},indent=2))
