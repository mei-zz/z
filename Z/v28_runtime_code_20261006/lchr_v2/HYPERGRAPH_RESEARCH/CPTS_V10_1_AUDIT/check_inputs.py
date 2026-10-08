"""Validate prerequisite references without scoring held-out test candidates."""
from pathlib import Path
import run_audit as a
r=a.readj(a.OUT/'results.json'); v8=a.readj(a.V8/'results.json'); v71=a.readj(a.V71/'results.json')
assert r['five_seed_gate']['triggered']
for ds in ('cora','pubmed','citeseer'):
 for m in ('CPTS','SH75'):
  for s in range(3):
   if ds=='cora' and m=='SH75': continue
   x=a.trainrec(ds,'gcn',m,s)
   assert x['state']=='COMPLETE'
   assert Path(x['training_record']['checkpoint']).is_file()
for s in range(3):
 for m in ('CPTS','MATCHED_Q'):
  assert a.testrec('cora',m,s)['state']=='COMPLETE'
  assert a.trainrec('cora','gcn',m,s)['state']=='COMPLETE'
for b in ('sage','gat'):
 assert Path(a.trainrec('cora',b,'CPTS',0)['training_record']['checkpoint']).is_file()
for m in ('GRAPH_HARD','QTHS25'):
 x=v8['pubmed']['test'][m]['by_seed']; assert len(x)==3
for s in range(3):
 assert isinstance(v71['citeseer']['test']['by_method_seed']['C1_GRAPH_HARD'][str(s)]['mrr'],float)
for ds in ('cora','pubmed','citeseer'):
 ev=(a.V71 if ds=='citeseer' else a.V8)/'EVALUATION'
 assert (ev/f'{ds}_test_candidates.npz').is_file()
print('PREFLIGHT_INPUT_REFERENCES_OK',flush=True)
