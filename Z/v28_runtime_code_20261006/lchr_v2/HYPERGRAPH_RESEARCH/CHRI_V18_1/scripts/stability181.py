"""V18.1: read-only historical V18, new reproduction/stability outputs, no test IO."""
from __future__ import annotations

import os
for _name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):
    os.environ.setdefault(_name,'4')
os.environ.setdefault('PYTHONDONTWRITEBYTECODE','1')
import sys
sys.dont_write_bytecode=True
import hashlib
import importlib.util
import json
import shutil
import subprocess
import time
import traceback
from pathlib import Path

import numpy as np
import torch
from torch import nn

OUT=Path(__file__).resolve().parents[1]
ROOT=OUT.parent
REPO=ROOT.parent
OLD=ROOT/'CHRI_V18'
sys.path.insert(0,str(OLD/'scripts'))
spec=importlib.util.spec_from_file_location('historical_chri18',OLD/'scripts/chri_v18.py')
v=importlib.util.module_from_spec(spec);sys.modules[spec.name]=v;spec.loader.exec_module(v)
v.OUT=OUT  # All inherited write helpers, job paths and caches now use the NEW root.
torch.set_num_threads(int(os.environ['OMP_NUM_THREADS']))
read,write,sha=v.read,v.write,v.sha
original_make_net=v.make_net
original_input=v.sealed_input


def validation_only(ds,test=False):
    assert ds in ('cora','pubmed'), 'V18_1_NO_THIRD_DATASET'
    assert test is False, 'V18_1_TEST_PERMANENTLY_SEALED'
    return v.s.input_data(ds,False)


v.sealed_input=validation_only


class StablePredictor(v.RelationPredictor):
    def __init__(self,structure,seed,name,mean,std):
        super().__init__(structure,seed,'A2',mean,std)
        self.variant=name.split('_')[0]
        self.control='NULL' if name.endswith('_NULL') else 'SHUFFLE' if name.endswith('_SHUFFLE') else 'TRUE'
        assert self.variant in ('V1','V2','V3')
        self.arm=name
        # The inherited trainer adds the returned nuisance loss when is_module is true.
        self.is_module=True
        self.nuisance.requires_grad_(True)
        self.correction.requires_grad_(self.variant in ('V2','V3'))
        with torch.random.fork_rng():
            torch.manual_seed(18700+seed)
            self.gate=nn.Linear(353,1)
            nn.init.zeros_(self.gate.weight);nn.init.constant_(self.gate.bias,-2.)
        self.gate.requires_grad_(self.variant=='V3')

    def components(self,pairs,b,donor=None):
        need=self.control=='TRUE'
        z,r=self.representation(pairs,b,need)
        if self.control=='NULL':
            latent=self.relation(b.new_zeros((len(pairs),48)))
            r=torch.cat((latent,latent),1)
        elif self.control=='SHUFFLE':
            assert donor is not None
            _,r=self.representation(donor,b,True)
        # No supervised gradient, encoder gradient, or label goes into the nuisance fit.
        m=self.nuisance(z.detach())
        residual=r-m.detach()
        zero=b.new_zeros((len(pairs),32))
        base=b[:,0]+self.decoder(torch.cat((z,zero),1)).flatten()
        alpha=torch.ones(len(pairs),device=b.device)
        if self.variant=='V1':
            score=b[:,0]+self.decoder(torch.cat((z,residual),1)).flatten()
            correction=score-base
        else:
            raw_correction=self.correction(residual).flatten()
            if self.variant=='V3':alpha=torch.sigmoid(self.gate(torch.cat((z,residual),1))).flatten()
            correction=alpha*raw_correction
            score=base+correction
        nuisance_loss=(m-r.detach()).square().mean()
        return {'score':score,'base':base,'correction':correction,'gate':alpha,
                'z':z,'r':r,'m':m,'residual':residual,'nuisance_loss':nuisance_loss}

    def forward(self,pairs,b,donor=None):
        part=self.components(pairs,b,donor)
        return part['score'],part['nuisance_loss'],b.new_zeros(())


def make_net(ds,seed,arm,phase,structure=None):
    if arm.startswith(('V1','V2','V3')):
        stats=read(v.cache(ds,seed)/'normalization.json')
        structure=structure or v.Structure(v.cache(ds)/'structure.npz')
        return StablePredictor(structure,seed,arm,np.asarray(stats['mean']),np.asarray(stats['std'])).to('cuda')
    return original_make_net(ds,seed,arm,phase,structure)


v.make_net=make_net


def job(phase,ds,seed,arm):return v.job(phase,ds,seed,arm)


def history_snapshot():
    files={}
    folders=(OLD,ROOT/'R_HSPE_FINAL_FROZEN',ROOT/'PAPER_PREP/INNOVATION_1_R_HSPE',REPO/'result/innovation2/CHRI_V18')
    for folder in folders:
        if not folder.exists():continue
        paths=list(folder.glob('*')) if folder==OLD else list(folder.rglob('*'))
        for p in paths:
            if p.is_file() and p.suffix in ('.json','.md','.py'):
                files[str(p.relative_to(REPO))]=sha(p)
    for p in (OLD/'scripts').glob('*.py'):files[str(p.relative_to(REPO))]=sha(p)
    for p in (OLD/'runs/A').glob('*/*/*/result.json'):files[str(p.relative_to(REPO))]=sha(p)
    return files


def check_history():
    manifest=read(OUT/'SOURCE_HASHES.json')
    for path,expected in manifest['historical_files'].items():
        assert sha(REPO/path)==expected,'HISTORICAL_ARTIFACT_MODIFIED '+path
    v.check_frozen()


def clone_caches():
    ready=OUT/'CACHE_CLONE_READY.json'
    if ready.exists():return
    hashes={}
    for ds in ('cora','pubmed'):
        source=OLD/'cache'/ds;target=v.cache(ds)
        assert source.is_dir()
        for file in source.glob('*'):
            if file.is_file():
                shutil.copy2(file,target/file.name)
                assert sha(file)==sha(target/file.name)
                hashes[str(file.relative_to(OLD))]=sha(file)
        for seed in range(3):
            original=source/f'seed_{seed}';copy=v.cache(ds,seed)
            for file in original.glob('*'):
                if file.is_file():
                    shutil.copy2(file,copy/file.name)
                    assert sha(file)==sha(copy/file.name)
                    hashes[str(file.relative_to(OLD))]=sha(file)
            assert read(copy/'B_READY_5.json')['state']=='COMPLETE'
            assert read(copy/'MATCH_READY_5.json')['state']=='COMPLETE'
    write(ready,{'state':'PASS','copy_kind':'independent regular files, no hardlinks or symlinks',
                'original_cache_file_sha256':hashes,'created_at':time.time()})


def preflight():
    assert REPO.name in ('DCDLP-main','lchr_v2')
    historical=read(OLD/'status.json')
    assert historical['state']=='COMPLETE' and historical['decision']=='CHRI_KILL'
    assert 'CHRI_TRANSFER_WEAK' in historical['reason']
    assert 'FINAL_FROZEN' in (ROOT/'R_HSPE_FINAL_FROZEN/INNOVATION_1_FINAL.md').read_text()
    old_manifest=read(OLD/'SOURCE_HASHES.json')
    for ds in ('cora','pubmed'):
        a=validation_only(ds)
        for name in ('x','train','valid_pos','valid_neg'):
            assert v.s.ah(a[name])==old_manifest['datasets'][ds]['input_hashes'][name]
    sources={str(p.relative_to(OUT)):sha(p) for p in (OUT/'scripts').glob('*.py')}
    for p in (OLD/'scripts').glob('*.py'):
        sources['../CHRI_V18/scripts/'+p.name]=sha(p)
    write(OUT/'SOURCE_HASHES.json',{'state':'FROZEN_BEFORE_EXECUTION','workspace':'DCDLP-main',
        'innovation1_files':old_manifest['innovation1_files'],'v18_source_files':sources,
        'historical_files':history_snapshot(),'V18_final_status_preserved':historical,
        'protocol_sha256':sha(OUT/'00_PROTOCOL.md')})
    write(OUT/'RUN_MANIFEST.json',{'state':'REGISTERED','task':'CHRI_V18_1_STABILITY','created_at':time.time(),
        'reproduction':{'seeds':[0,1,2],'datasets':['cora','pubmed'],'epochs':5,'arms':{'R0':'A1','R1':'A2','R2':'A3'},
                        'ce_absolute_tolerance':1e-5,'mrr_absolute_tolerance':1e-4,'max_score_absolute_tolerance':5e-5},
        'phase_a':{'seeds':[0,1,2],'epochs':5,'primary_arms':['Z','RAW','V1','V2','V3','V3_NULL','V3_SHUFFLE'],
                   'additional_controls':'Only architecture-matched V1/V2 shuffle if that variant passes preliminary stability gates.'},
        'phase_b':{'seeds':list(range(5)),'epochs':10,'arms':['Z','RAW','SELECTED','SELECTED_NULL','SELECTED_SHUFFLE']},
        'nuisance':[321,32,32],'correction':[32,32,1],'gate':[353,1],
        'gate_initial_weight':0,'gate_initial_bias':-2,'gate_initial_value':float(1/(1+np.exp(2))),
        'lambda_nuisance':1,'conditional_null_regularization':False,
        'training_loss':'same V18 balanced positive+negative BCE sum, plus lambda1 nuisance MSE on detached Z/r',
        'optimizer':'same V18 Adam, dataset predictor LR, weight_decay=0',
        'base_head':'same V18 qZ decoder 353->64->32->1, reserved relation slots zero for V2/V3 base',
        'raw_diagnostic_nuisance':'321->32->32, five epochs, train-only epoch1 candidates, no label inputs, same predictor LR',
        'selection_order':['minimum paired CE improvement across all six seeds','total CE wins',
                           'mean paired CE improvement across datasets','mean paired MRR improvement','fewer added parameters'],
        'phase_a_promising':'both CE>=2/3, meanCE>0, meanMRR>=0; minimum dataset win count improves over RAW; true beats architecture-matched shuffle in meanCE on both datasets',
        'phase_b_gate':'both meanCE>0, medianCE>0, CE>=3/5, meanMRR>=0, true meanCE beats matched NULL and SHUFFLE',
        'parallel_workers':3,'test_opened':False,'citeseer':'NOT_RUN','I1_I2_complementarity':'NOT_RUN',
        'innovation1':'FINAL_FROZEN','innovation3':'NOT_STARTED'})
    clone_caches();check_history()
    for name in ('01_V18_REPRODUCTION.json','02_INSTABILITY_DIAGNOSIS.json','03_PHASE_A_RESULTS.json',
                 '05_PHASE_B_RESULTS.json','06_TRUE_VS_SHUFFLE.json'):
        if not (OUT/name).exists():write(OUT/name,{'state':'NOT_RUN','reason':'Prerequisite stage pending.'})
    for name in ('02_INSTABILITY_DIAGNOSIS.md','04_VARIANT_SELECTION.md','07_CORRECTION_BEHAVIOR.md','08_SUBGROUP_ANALYSIS.md'):
        if not (OUT/name).exists():(OUT/name).write_text('# '+name+'\n\nNOT_RUN: prerequisite stage pending.\n')
    write(OUT/'01_LEAKAGE_AUDIT.json',{'state':'PASS','inherited_from_V18':sha(OLD/'01_LEAKAGE_AUDIT.json'),
        'structure':'exact independent copies of audited V18 structures; target removal unchanged',
        'matching':'same training-only donors and initial-Z kNN32; no heldout fitting',
        'nuisance':'detached Z/r only, no label inputs or prediction-loss gradients',
        'test_accessed':False,'citeseer_accessed':False})
    print('V18_1_PREFLIGHT_PASS',flush=True)


def run(phase,ds,seed,arm,epochs):
    check_history()
    v.run(phase,ds,seed,arm,epochs)
    path=job(phase,ds,seed,arm)/'result.json';row=read(path)
    net=v.load_net(phase,ds,seed,arm)
    groups={name:sum(p.numel() for p in getattr(net,name).parameters() if p.requires_grad)
            for name in ('encoder','relation','decoder','nuisance','correction')}
    groups['gate']=sum(p.numel() for p in net.gate.parameters() if p.requires_grad) if hasattr(net,'gate') else 0
    assert sum(groups.values())==row['trainable_parameters']
    row['parameter_groups']=groups
    row['added_parameters_vs_Z']=row['trainable_parameters']-26385
    row['conditional_null_regularization']=False
    row['nuisance_labels_used']=False
    row['actual_shared_decoder_initialization']='same V18 seed18200 decoder; inherited unused z_decoder hash is not used for inference'
    write(path,row)


def reproduction_summary():
    rows={};discrepancies=[]
    for ds in ('cora','pubmed'):
        rows[ds]=[]
        for seed in range(3):
            arms={}
            for name,arm in (('R0','A1'),('R1','A2'),('R2','A3')):
                new=read(job('R',ds,seed,arm)/'result.json')
                old=read(OLD/'runs/A'/ds/f'seed_{seed}'/arm/'result.json')
                trace_match=new['training_trace']==old['training_trace']
                init_match=new['initialization']==old['initialization']
                if not trace_match or not init_match:
                    discrepancies.append({'dataset':ds,'seed':seed,'arm':name,
                        'training_trace_match':trace_match,'initialization_match':init_match})
                checks=[]
                for epoch,(current,prior) in enumerate(zip(new['history'],old['history']),1):
                    delta_ce=current['validation']['ce']-prior['validation']['ce']
                    delta_mrr=current['validation']['mrr']-prior['validation']['mrr']
                    score=v.scores_file(job('R',ds,seed,arm)/f'valid_epoch{epoch}_scores.npz')
                    previous=v.scores_file(OLD/'runs/A'/ds/f'seed_{seed}'/arm/f'valid_epoch{epoch}_scores.npz')
                    error=float(np.max(np.abs(score-previous)))
                    passed=abs(delta_ce)<=1e-5 and abs(delta_mrr)<=1e-4 and error<=5e-5
                    checks.append({'epoch':epoch,'ce_difference':delta_ce,'mrr_difference':delta_mrr,
                                   'score_max_abs_error':error,'pass':passed})
                    if not passed:discrepancies.append({'dataset':ds,'seed':seed,'arm':name,**checks[-1]})
                arms[name]={'validation':new['validation'],'original_validation':old['validation'],
                            'history':new['history'],'epoch_tolerance_checks':checks,
                            'training_trace_match':trace_match,'initialization_match':init_match}
            rows[ds].append({'seed':seed,'arms':arms})
    effects={ds:{'RAW_vs_Z':v.comparison(rr,'R1','R0'),'RAW_vs_SHUFFLE':v.comparison(rr,'R1','R2')} for ds,rr in rows.items()}
    result={'state':'PASS' if not discrepancies else 'REPRODUCTION_MISMATCH','reproduced':not discrepancies,
            'seed_results':rows,'effects':effects,'discrepancies':discrepancies,
            'tolerance':{'ce':1e-5,'mrr':1e-4,'score_abs':5e-5},'historical_V18_gate':'CHRI_KILL / CHRI_TRANSFER_WEAK',
            'training_traces_and_initialization_identical':all(a['training_trace_match'] and a['initialization_match'] for rr in rows.values() for item in rr for a in item['arms'].values()),
            'test_accessed':False}
    write(OUT/'01_V18_REPRODUCTION.json',result)
    return result


def safe_correlation(a,b):
    a=np.asarray(a,float);b=np.asarray(b,float)
    if a.std()<1e-12 or b.std()<1e-12:return None
    return float(np.corrcoef(a,b)[0,1])


def nuisance_statistics(r,prediction):
    r=np.asarray(r,np.float64);m=np.asarray(prediction,np.float64)
    residual=r-m;variance=float(np.mean(np.var(r,axis=0)))
    mse=float(np.mean(residual**2))
    norm=np.linalg.norm(r,axis=1)*np.linalg.norm(m,axis=1)
    cosine=np.sum(r*m,axis=1)/np.maximum(norm,1e-12)
    return {'mse':mse,'R2':float(1-mse/variance) if variance>1e-12 else None,
            'relation_mean_component_variance':variance,'residual_mean_component_variance':float(np.var(residual,axis=0).mean()),
            'cosine_mean':float(cosine.mean()),'residual_norm_mean':float(np.linalg.norm(residual,axis=1).mean())}


def behavior_statistics(parts,labels,reference):
    c=parts['correction'];r=parts['r'];base=parts['base'];score=parts['score'];gate=parts['gate']
    tol=1e-6;benefit=(2*labels-1)*c
    result={'relation_norm_mean':float(np.linalg.norm(r,axis=1).mean()),
        'relation_norm_std':float(np.linalg.norm(r,axis=1).std()),
        'correction_norm':float(np.linalg.norm(c)), 'correction_rms':float(np.sqrt(np.mean(c**2))),
        'correction_mean':float(c.mean()),'correction_std':float(c.std()),'correction_variance':float(c.var()),
        'correction_sign_distribution':{'positive':float(np.mean(c>tol)),'negative':float(np.mean(c<-tol)), 'zero':float(np.mean(np.abs(c)<=tol))},
        'correlation_correction_baseline_logit':safe_correlation(c,base),'correlation_correction_label':safe_correlation(c,labels),
        'score_changed_fraction':float(np.mean(np.abs(c)>tol)),
        'hard_prediction_changed_fraction':float(np.mean((score>0)!=(base>0))),
        'beneficial_correction_fraction':float(np.mean(benefit>tol)),
        'harmful_correction_fraction':float(np.mean(benefit<-tol)),
        'prediction_difference_from_separately_trained_Z_rms':float(np.sqrt(np.mean((score-reference)**2))),
        'gate_mean':float(gate.mean()),'gate_std':float(gate.std()),
        'gate_positive_mean':float(gate[labels==1].mean()),'gate_negative_mean':float(gate[labels==0].mean()),
        'gate_correlation_abs_baseline_margin':safe_correlation(gate,np.abs(base))}
    if 'm' in parts:result['nuisance']=nuisance_statistics(r,parts['m'])
    return result


@torch.no_grad()
def validation_components(net,ds,seed):
    destination=v.cache(ds,seed);pairs=np.load(destination/'valid_pairs.npy')
    features=np.load(destination/'valid_b.npy',mmap_mode='r');pool=np.load(destination/'donor_pairs.npy')
    indexes=v.donor_choices(np.load(destination/'valid_knn.npy'),seed,0)
    net.eval();parts={}
    for begin in range(0,len(pairs),512):
        p=torch.tensor(pairs[begin:begin+512],dtype=torch.long,device='cuda')
        b=torch.tensor(features[begin:begin+512],device='cuda')
        d=torch.tensor(pool[indexes[begin:begin+512]],dtype=torch.long,device='cuda')
        if isinstance(net,StablePredictor):
            item=net.components(p,b,d)
        else:
            z,r=net.representation(p,b,True)
            score=net.prediction(z,r,b[:,0]);base=net.prediction(z,torch.zeros_like(r),b[:,0])
            item={'z':z,'r':r,'score':score,'base':base,'correction':score-base,'gate':torch.ones(len(p),device='cuda')}
        for name,value in item.items():
            if name=='nuisance_loss':continue
            parts.setdefault(name,[]).append(value.cpu().numpy())
    return {name:np.concatenate(chunks) for name,chunks in parts.items()}


def raw_diagnosis(ds,seed):
    output=OUT/'diagnostics'/ds/f'seed_{seed}';output.mkdir(parents=True,exist_ok=True)
    if (output/'raw_diagnosis.json').exists():return
    net=v.load_net('R',ds,seed,'A2')
    pool=np.load(v.cache(ds,seed)/'donor_pairs.npy')
    features=np.load(v.cache(ds,seed)/'epoch_1.npy',mmap_mode='r').reshape(-1,257)
    z,r=v.latent_arrays(net,pool,features)
    train_z=torch.tensor(z,device='cuda');train_r=torch.tensor(r,device='cuda')
    with torch.random.fork_rng():
        torch.manual_seed(18800+seed)
        nuisance=nn.Sequential(nn.Linear(321,32),nn.ReLU(),nn.Linear(32,32)).to('cuda')
    optimizer=torch.optim.Adam(nuisance.parameters(),lr=v.b.NCFG[ds]['prelr'],weight_decay=0)
    fit_history=[]
    for epoch in range(5):
        total=[]
        for begin in range(0,len(z),v.b.NCFG[ds]['batch']):
            target=train_r[begin:begin+v.b.NCFG[ds]['batch']]
            predicted=nuisance(train_z[begin:begin+v.b.NCFG[ds]['batch']])
            loss=(predicted-target).square().mean();optimizer.zero_grad(set_to_none=True);loss.backward();optimizer.step()
            total.append(float(loss.detach()))
        fit_history.append(float(np.mean(total)))
    nuisance.eval();parts=validation_components(net,ds,seed)
    with torch.no_grad():
        prediction=nuisance(torch.tensor(parts['z'],device='cuda')).cpu().numpy()
        training_prediction=nuisance(train_z).cpu().numpy()
    q=len(validation_only(ds)['valid_pos']);labels=np.r_[np.ones(q),np.zeros(len(parts['score'])-q)]
    reference=v.scores_file(job('R',ds,seed,'A1')/'valid_epoch5_scores.npz')
    raw=read(job('R',ds,seed,'A2')/'result.json');baseline=read(job('R',ds,seed,'A1')/'result.json')
    result={'state':'COMPLETE','dataset':ds,'seed':seed,'raw_CE_win':raw['validation']['ce']<baseline['validation']['ce'],
        'paired_delta_ce':baseline['validation']['ce']-raw['validation']['ce'],
        'paired_delta_mrr':raw['validation']['mrr']-baseline['validation']['mrr'],
        'trajectory':raw['history'],'correction_behavior':behavior_statistics(parts,labels,reference),
        'nuisance_validation':nuisance_statistics(parts['r'],prediction),
        'nuisance_training':nuisance_statistics(r,training_prediction), 'nuisance_training_mse_trajectory':fit_history,
        'nuisance_fit':'five epochs, epoch1 training candidates only, frozen raw encoder, no labels, same Adam LR',
        'raw_correction_definition':'q_RAW(Z,R)-q_RAW(Z,0) in the SAME fitted model; not an additive branch or causal attribution',
        'test_accessed':False}
    write(output/'raw_diagnosis.json',result)


def diagnosis_summary():
    data={ds:[read(OUT/'diagnostics'/ds/f'seed_{seed}'/'raw_diagnosis.json') for seed in range(3)] for ds in ('cora','pubmed')}
    output={'state':'COMPLETE','datasets':data,'test_accessed':False,
            'interpretation':'descriptive within-dataset seed associations only; three seeds cannot establish a causal failure mechanism'}
    write(OUT/'02_INSTABILITY_DIAGNOSIS.json',output)
    lines=['# RAW instability diagnosis','','V18 failed its original preregistered gate. These measurements diagnose the reproduced weak signal; they do not reinterpret that result.','',
           '| Dataset | Seed | CE win | Delta CE | R norm mean | Correction RMS | Harmful fraction | Nuisance validation R² | Residual variance |',
           '|---|---:|---|---:|---:|---:|---:|---:|---:|']
    for ds,rows in data.items():
        for item in rows:
            behavior=item['correction_behavior'];nuis=item['nuisance_validation']
            lines.append(f"| {ds} | {item['seed']} | {item['raw_CE_win']} | {item['paired_delta_ce']:.9g} | {behavior['relation_norm_mean']:.9g} | {behavior['correction_rms']:.9g} | {behavior['harmful_correction_fraction']:.9g} | {nuis['R2']} | {nuis['residual_mean_component_variance']:.9g} |")
        for field,source in (('R norm','correction_behavior'),('correction RMS','correction_behavior'),('redundancy R2','nuisance_validation')):
            name={'R norm':'relation_norm_mean','correction RMS':'correction_rms','redundancy R2':'R2'}[field]
            winners=[r[source][name] for r in rows if r['raw_CE_win'] and r[source][name] is not None]
            failures=[r[source][name] for r in rows if not r['raw_CE_win'] and r[source][name] is not None]
            lines.append(f"\n{ds}: {field}; CE-winning seeds mean={np.mean(winners) if winners else 'NA'}, failed seeds mean={np.mean(failures) if failures else 'NA'}.")
    lines+=['','Correction is a same-model zero-R counterfactual. Nuisance statistics use a label-free train-only fit and report heldout validation quality. Harmful/beneficial fractions include all candidates and are class-imbalance dependent. These are descriptive associations, not causal explanations.']
    (OUT/'02_INSTABILITY_DIAGNOSIS.md').write_text('\n'.join(lines)+'\n')
    return output


def phase_rows(phase,ds,seeds,selected=None):
    rows=[]
    for seed in seeds:
        if phase=='A':
            references={'Z':('R','A1'),'RAW':('R','A2'),
                        **{name:('A',name) for name in ('V1','V2','V3','V3_NULL','V3_SHUFFLE')}}
            for variant in ('V1','V2'):
                if (job('A',ds,seed,variant+'_SHUFFLE')/'result.json').exists():
                    references[variant+'_SHUFFLE']=('A',variant+'_SHUFFLE')
        else:
            references={'Z':('B','A1'),'RAW':('B','A2'),'STABLE':('B',selected),
                        'NULL':('B',selected+'_NULL'),'SHUFFLE':('B',selected+'_SHUFFLE')}
        arms={label:read(job(p,ds,seed,arm)/'result.json') for label,(p,arm) in references.items()}
        assert all(item['training_trace']==arms['Z']['training_trace'] for item in arms.values())
        rows.append({'seed':seed,'arms':arms})
    return rows


def phase_summary(phase,seeds,selected=None):
    result={'state':'COMPLETE','phase':phase,'seeds':seeds,'datasets':{},'test_accessed':False}
    for ds in ('cora','pubmed'):
        rows=phase_rows(phase,ds,seeds,selected)
        names=[arm for arm in rows[0]['arms'] if arm!='Z']
        effects={name+'_vs_Z':v.comparison(rows,name,'Z') for name in names}
        if phase=='A':
            controls=[(name,name+'_SHUFFLE') for name in ('V1','V2','V3') if name+'_SHUFFLE' in rows[0]['arms']]
            controls.append(('V3','V3_NULL'))
            for name,control in controls:effects[name+'_vs_'+control]=v.comparison(rows,name,control)
            gates={}
            for name in ('V1','V2','V3'):
                effect=effects[name+'_vs_Z']
                basic=effect['ce']['wins']>=2 and effect['ce']['mean']>0 and effect['mrr']['mean']>=0
                shuffle=effects.get(name+'_vs_'+name+'_SHUFFLE')
                gates[name]={'basic_stability':basic,
                             'architecture_matched_shuffle_run':shuffle is not None,
                             'true_beats_matched_shuffle':shuffle is not None and shuffle['ce']['mean']>0}
        else:
            effects['STABLE_vs_NULL']=v.comparison(rows,'STABLE','NULL')
            effects['STABLE_vs_SHUFFLE']=v.comparison(rows,'STABLE','SHUFFLE')
            main=effects['STABLE_vs_Z']
            gates={'positive_mean_ce':main['ce']['mean']>0,'positive_median_ce':main['ce']['median']>0,
                   'ce_wins_at_least_3':main['ce']['wins']>=3,'mean_mrr_nonnegative':main['mrr']['mean']>=0,
                   'true_beats_null':effects['STABLE_vs_NULL']['ce']['mean']>0,
                   'true_beats_shuffle':effects['STABLE_vs_SHUFFLE']['ce']['mean']>0}
        result['datasets'][ds]={'seed_results':rows,'effects':effects,'gates':gates,
            'metrics':{name:{metric:v.stat([r['arms'][name]['validation'][metric] for r in rows]) for metric in v.METRICS} for name in rows[0]['arms']}}
        if phase=='B':result['datasets'][ds]['pass']=all(gates.values())
    if phase=='B':result['all_pass']=all(item['pass'] for item in result['datasets'].values())
    return result


def needs_shuffle(phase_a):
    jobs=[]
    for variant in ('V1','V2'):
        if all(item['gates'][variant]['basic_stability'] for item in phase_a['datasets'].values()):
            jobs.extend([('run','A',ds,seed,variant+'_SHUFFLE',5) for ds in ('cora','pubmed') for seed in range(3)])
    return jobs


def select_variant(phase_a):
    candidates=[];raw_min=min(d['effects']['RAW_vs_Z']['ce']['wins'] for d in phase_a['datasets'].values())
    for variant in ('V1','V2','V3'):
        if not all(all(d['gates'][variant].values()) for d in phase_a['datasets'].values()):continue
        effects=[d['effects'][variant+'_vs_Z'] for d in phase_a['datasets'].values()]
        minimum_wins=min(e['ce']['wins'] for e in effects)
        if minimum_wins<=raw_min:continue
        improvements=[value for e in effects for value in e['ce']['per_seed']]
        params=phase_a['datasets']['cora']['seed_results'][0]['arms'][variant]['added_parameters_vs_Z']
        rank=[min(improvements),sum(e['ce']['wins'] for e in effects),
              float(np.mean([e['ce']['mean'] for e in effects])),
              float(np.mean([e['mrr']['mean'] for e in effects])),-params]
        candidates.append({'variant':variant,'selection_key':rank,'minimum_dataset_ce_wins':minimum_wins,
                           'added_parameters':params})
    candidates.sort(key=lambda item:item['selection_key'],reverse=True)
    selected=candidates[0]['variant'] if candidates else None
    result={'state':'SELECTED' if selected else 'NONE','variant':selected,'candidates':candidates,
            'selection_rule':read(OUT/'RUN_MANIFEST.json')['selection_order'],
            'raw_minimum_dataset_ce_wins':raw_min,'architecture_frozen_before_phase_b':bool(selected),
            'definition':{'V1':'q(Z, R-stopgrad(m(Z)))','V2':'qZ(Z)+zero-init g(R-stopgrad(m(Z)))',
                          'V3':'qZ(Z)+sigmoid(a([Z,R_delta]))*zero-init g(R_delta)'}.get(selected),
            'test_accessed':False}
    write(OUT/'SELECTED_VARIANT.json',result)
    (OUT/'04_VARIANT_SELECTION.md').write_text('# Frozen variant selection\n\n'+json.dumps(result,indent=2)+'\n')
    return selected


def correction_behavior(phase,ds,seed,arm,baseline_phase):
    destination=OUT/'behavior'/phase/ds/f'seed_{seed}';destination.mkdir(parents=True,exist_ok=True)
    if (destination/(arm+'.json')).exists():return
    net=v.load_net(phase,ds,seed,arm);parts=validation_components(net,ds,seed)
    epochs=read(job(phase,ds,seed,arm)/'result.json')['epochs']
    reference=v.scores_file(job(baseline_phase,ds,seed,'A1')/f'valid_epoch{epochs}_scores.npz')
    q=len(validation_only(ds)['valid_pos']);labels=np.r_[np.ones(q),np.zeros(len(parts['score'])-q)]
    result={'state':'COMPLETE','dataset':ds,'seed':seed,'arm':arm,
            'behavior':behavior_statistics(parts,labels,reference),'test_accessed':False,
            'correction_definition':'explicit relation residual for V2/V3; same-model zero-relation-slot counterfactual for V1/RAW'}
    write(destination/(arm+'.json'),result)


def behavior_report(phase,selected=None):
    seeds=range(5) if phase=='B' else range(3)
    arms=('A2',selected) if phase=='B' else ('A2','V1','V2','V3')
    data={ds:{arm:[] for arm in arms} for ds in ('cora','pubmed')}
    for ds in data:
        for arm in arms:
            actual_phase='R' if phase=='A' and arm=='A2' else phase
            for seed in seeds:
                data[ds][arm].append(read(OUT/'behavior'/actual_phase/ds/f'seed_{seed}'/(arm+'.json')))
    payload={'state':'COMPLETE','phase':phase,'selected_variant':selected,'datasets':data,
             'interpretation':'descriptive correction behavior; performance, NULL and correspondence controls are needed for the mechanism claim',
             'test_accessed':False}
    write(OUT/'CORRECTION_BEHAVIOR.json',payload)
    lines=['# Correction behavior','','No causal claim is inferred from these descriptive statistics. Compare RAW with residualization and the frozen selected method when available.','',
           '| Dataset | Arm | Seed | Correction RMS | Harmful fraction | Beneficial fraction | Gate mean | Gate std | Residual variance |',
           '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for ds,by_arm in data.items():
        for arm,rows in by_arm.items():
            for row in rows:
                item=row['behavior'];residual=item.get('nuisance',{}).get('residual_mean_component_variance','NA')
                lines.append(f"| {ds} | {arm} | {row['seed']} | {item['correction_rms']:.9g} | {item['harmful_correction_fraction']:.9g} | {item['beneficial_correction_fraction']:.9g} | {item['gate_mean']:.9g} | {item['gate_std']:.9g} | {residual} |")
    lines+=['','RAW/V1 correction uses a fitted-model counterfactual and is not an isolated causal effect. V2/V3 have explicit additive correction. The separately fitted Z prediction difference is also included in JSON. Nuisance loss uses no labels; gate label strata are evaluation diagnostics only.']
    (OUT/'07_CORRECTION_BEHAVIOR.md').write_text('\n'.join(lines)+'\n')
    return payload


def subgroup_analysis(selected):
    freeze=read(OUT/'PHASE_B_FROZEN.json')
    assert freeze['state']=='FROZEN' and freeze['test_opened'] is False
    for path,h in freeze['result_files'].items():assert sha(OUT/path)==h
    output={}
    for ds in ('cora','pubmed'):
        rows=[]
        for seed in range(5):
            source=v.cache(ds,seed)
            train=np.load(source/'epoch_1.npy',mmap_mode='r').reshape(-1,257)
            cuts=np.quantile(np.abs(train[:,0]),[.25,.5,.75])
            q=len(validation_only(ds)['valid_pos'])
            confidence=np.abs(np.load(source/'valid_b.npy',mmap_mode='r')[:q,0])
            labels=np.digitize(confidence,cuts)
            baseline=v.scores_file(job('B',ds,seed,'A1')/'valid_epoch10_scores.npz')
            true=v.scores_file(job('B',ds,seed,selected)/'valid_epoch10_scores.npz')
            subgroups=[]
            for group in range(4):
                query=np.flatnonzero(labels==group)
                if not len(query):
                    subgroups.append({'group':group,'queries':0,'state':'EMPTY'});continue
                def subset(score):
                    return np.r_[score[:q][query],score[q:].reshape(q,20)[query].ravel()]
                m0=v.metrics(subset(baseline),len(query));m1=v.metrics(subset(true),len(query))
                subgroups.append({'group':group,'queries':len(query),'delta_ce':m0['ce']-m1['ce'],
                                 'delta_mrr':m1['mrr']-m0['mrr']})
            rows.append({'seed':seed,'training_confidence_quartile_cuts':cuts.tolist(),'subgroups':subgroups})
        output[ds]=rows
    write(OUT/'SUBGROUP_ANALYSIS.json',{'state':'COMPLETE','datasets':output,'selection_use':False,
          'definition':'frozen NCNC positive-query absolute logit, bins fitted on unlabeled training candidate logits',
          'after_all_phase_b_results_frozen':True,'test_accessed':False})
    (OUT/'08_SUBGROUP_ANALYSIS.md').write_text('# Descriptive confidence subgroups\n\n'+json.dumps(output,indent=2)+'\n\nUsed only after Phase B results were frozen. No feature engineering, model selection, or tuning uses these groups.\n')


CHILDREN=[]


def launch(arguments):
    directory=OUT/'logs';directory.mkdir(exist_ok=True)
    log=directory/('_'.join(map(str,arguments))+'.log')
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS'):env[key]='4'
    env['PYTHONDONTWRITEBYTECODE']='1'
    with log.open('a') as stream:
        process=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*map(str,arguments)],
             stdin=subprocess.DEVNULL,stdout=stream,stderr=subprocess.STDOUT,env=env,start_new_session=True)
    item={'proc':process,'arguments':arguments,'log':str(log)};CHILDREN.append(item)
    return item


def batch(arguments,stage,parallel=3):
    queue=list(arguments);active=[]
    while queue or active:
        for item in list(active):
            if item['proc'].poll() is not None:
                active.remove(item)
                if item['proc'].returncode:raise RuntimeError(f"JOB_FAILED {item['arguments']} {item['log']}")
        while queue and len(active)<parallel:active.append(launch(queue.pop(0)))
        write(OUT/'status.json',{'state':'RUNNING','stage':stage,'supervisor_pid':os.getpid(),'updated_at':time.time(),
            'queued_jobs':len(queue),'active':[{'pid':r['proc'].pid,'arguments':r['arguments'],'log':r['log']} for r in active],
            'test_opened':False,'historical_V18_status':'CHRI_KILL / CHRI_TRANSFER_WEAK'})
        if active:time.sleep(3)


def seal_skipped(reason):
    for name in ('01_V18_REPRODUCTION.json','02_INSTABILITY_DIAGNOSIS.json','03_PHASE_A_RESULTS.json',
                 '05_PHASE_B_RESULTS.json','06_TRUE_VS_SHUFFLE.json'):
        data=read(OUT/name)
        if data.get('state')=='NOT_RUN':write(OUT/name,{'state':'NOT_RUN','reason':reason})
    for name in ('02_INSTABILITY_DIAGNOSIS.md','04_VARIANT_SELECTION.md','07_CORRECTION_BEHAVIOR.md','08_SUBGROUP_ANALYSIS.md'):
        p=OUT/name
        if 'NOT_RUN: prerequisite stage pending.' in p.read_text():
            p.write_text('# '+name+'\n\nNOT_RUN: '+reason+'\n')


def report(state,final_status,reason):
    check_history()
    if state=='COMPLETE':seal_skipped(reason)
    def artifact(name):return read(OUT/name) if (OUT/name).exists() else {'state':'NOT_RUN','reason':reason}
    reproduced=artifact('01_V18_REPRODUCTION.json')
    a=artifact('03_PHASE_A_RESULTS.json');b=artifact('05_PHASE_B_RESULTS.json')
    selected=artifact('SELECTED_VARIANT.json');correspondence=artifact('06_TRUE_VS_SHUFFLE.json')
    diagnosis=artifact('02_INSTABILITY_DIAGNOSIS.json')
    chosen=selected.get('variant')
    lines=['# V18.1 — CHRI stability continuation','',f'STATE: {state}',f'FINAL_STATUS: {final_status}',f'REASON: {reason}','',
        '**Historical integrity:** V18 failed its original preregistered gate: CHRI_KILL / CHRI_TRANSFER_WEAK. V18.1 is a user-authorized weak-signal stabilization continuation with a different research goal. V18 is not retroactively changed.',
        '',f'## 1. Was V18 reproduced?\n\n{reproduced.get("state")}. Exact traces/initialization are required; all five heldout trajectories must meet preregistered numerical tolerances.',
        '', '## 2–3. Why RAW was unstable; predictability of R from Z','',
        'See 02_INSTABILITY_DIAGNOSIS.md/json for per-seed trajectories, relation/correction norms, correction signs, harmful/beneficial fractions, train-only nuisance MSE/R²/cosine, and residual variance. Failed versus winning seed comparisons are descriptive; three seeds do not prove that redundancy causes instability.',
        '', '## 4–6. Residualization, zero initialization, and conservative gating','',
        'V1 uses q(Z,R-stopgrad(m(Z))); V2 uses qZ(Z)+zero-init g(R_delta); V3 uses qZ(Z)+sigmoid(a([Z,R_delta]))*zero-init g(R_delta). All use the original encoders and R operator; m fits detached Z/r without labels. Lambda_nuis=1; no conditional-null regularization. V18 RAW already zero-initializes its final concat decoder; V2 isolates a separately initialized additive relation head, so this is not a claim that RAW lacked all zero initialization.',
        '', '| Phase | Dataset | Method vs Z | Mean Delta CE | Median Delta CE | CE wins | Mean Delta MRR | MRR wins |',
        '|---|---|---|---:|---:|---:|---:|---:|']
    for phase,payload in (('A',a),('B',b)):
        for ds,item in payload.get('datasets',{}).items():
            for name,effect in item['effects'].items():
                if not name.endswith('_vs_Z'):continue
                ce=effect['ce'];mrr=effect['mrr']
                lines.append(f"| {phase} | {ds} | {name} | {ce['mean']:.10g} | {ce['median']:.10g} | {ce['wins']}/{len(ce['per_seed'])} | {mrr['mean']:.10g} | {mrr['wins']}/{len(mrr['per_seed'])} |")
    lines.extend(['',f'## 7. Selected variant\n\n{chosen or "NONE"}. {selected.get("definition","")}',
        '', '## 8–9. Cora and PubMed stability before/after','',
        'The table above contains paired CE/MRR and wins. Phase A requires a minimum dataset CE-win count higher than RAW, with both datasets meeting ≥2/3, positive mean CE and nonnegative mean MRR, plus architecture-matched shuffle advantage. Phase B requires ≥3/5, positive mean/median CE, nonnegative mean MRR, and true advantage over NULL and SHUFFLE.',
        '', '## 10–11. Relation correspondence and parameter capacity','',
        json.dumps(correspondence,indent=2),
        '', '## 12. Remaining signal','',final_status+'. '+reason,
        '', '## Correction behavior','',
        'See 07_CORRECTION_BEHAVIOR.md and CORRECTION_BEHAVIOR.json. Explicit V2/V3 relation residuals and same-model zero-slot RAW/V1 counterfactuals are reported separately from the difference to an independently trained Z model. NULL and correspondence contrasts are required before interpreting reduced harmful corrections as relation-specific stability.',
        '', 'TEST_OPENED: NO', 'CORA_TEST: NOT_RUN', 'PUBMED_TEST: NOT_RUN','CITESEER: NOT_RUN',
        'I1_I2_COMPLEMENTARITY: NOT_RUN','INNOVATION_1_MODIFIED: NO','INNOVATION_2_FINAL_FROZEN: NO','INNOVATION_3: NOT_STARTED'])
    (OUT/'FINAL_REPORT.md').write_text('\n'.join(lines)+'\n')
    phase_b='PASS' if b.get('all_pass') else 'FAIL' if b.get('state')=='COMPLETE' else 'NOT_RUN'
    fields=['STATUS: '+('EXECUTED' if state=='COMPLETE' else state),'TASK: CHRI_V18_1_STABILITY','WORKSPACE: DCDLP-main',
            'V18_REPRODUCED: '+('YES' if reproduced.get('reproduced') else 'NO' if reproduced.get('state')=='REPRODUCTION_MISMATCH' else 'PENDING')]
    for ds in ('cora','pubmed'):
        raw=reproduced.get('effects',{}).get(ds,{}).get('RAW_vs_Z')
        fields.append('RAW_'+ds.upper()+': '+(json.dumps(raw) if raw else 'NOT_RUN'))
    fields += ['SELECTED_VARIANT: '+(chosen or 'NONE'),'SELECTED_VARIANT_DEFINITION: '+str(selected.get('definition')),
               'CORA_STABILITY: '+json.dumps(b.get('datasets',a.get('datasets',{})).get('cora',{}).get('effects',{})),
               'PUBMED_STABILITY: '+json.dumps(b.get('datasets',a.get('datasets',{})).get('pubmed',{}).get('effects',{})),
               'TRUE_VS_SHUFFLE: '+json.dumps(correspondence),
               'TRUE_VS_NULL: '+json.dumps({ds:item.get('effects',{}).get('STABLE_vs_NULL',item.get('effects',{}).get('V3_vs_V3_NULL')) for ds,item in b.get('datasets',a.get('datasets',{})).items()}),
               f'PHASE_B: {phase_b}',f'FINAL_STATUS: {final_status}','TEST_OPENED: NO','INNOVATION_1_MODIFIED: NO',
               'NEXT_EXPECTED_STEP: '+('design V18.2 formal conditional-null/CRIB validation and I1-I2 complementarity audit' if final_status=='CHRI_STABILITY_CONFIRMED' else
                   'review stability evidence before formal module validation' if final_status=='CHRI_STABILITY_IMPROVED' else
                   'resolve reproduction mismatch' if final_status=='V18_1_REPRODUCTION_MISMATCH' else 'inspect candidate/seed failure mechanism; do not broad-search architectures')]
    (OUT/'C2C_HANDOFF.md').write_text('\n'.join(fields)+'\n')
    if state=='COMPLETE':
        write(OUT/'status.json',{'state':'COMPLETE','final_status':final_status,'reason':reason,'selected_variant':chosen,
             'phase_b':phase_b,'ended_at':time.time(),'test_opened':False,'innovation1_modified':False,'V18_modified':False})
        target=REPO/'result/innovation2/CHRI_V18_1';target.mkdir(parents=True,exist_ok=True)
        for p in OUT.glob('*'):
            if p.is_file() and p.suffix in ('.json','.md'):shutil.copy2(p,target/p.name)
        print('V18_1_COMPLETE',final_status,reason,flush=True)


def supervise():
    try:
        check_history();report('RUNNING','PENDING','Reproduce historical V18 before running any optimization variant.')
        batch([('run','R',ds,seed,arm,5) for seed in range(3) for ds in ('cora','pubmed') for arm in ('A1','A2','A3')],
              'V18_REPRODUCTION')
        reproduced=reproduction_summary()
        if not reproduced['reproduced']:
            report('COMPLETE','V18_1_REPRODUCTION_MISMATCH','Reproduced trajectory differs materially from historical V18. No new variant was run.');return
        batch([('diagnose',ds,seed) for ds in ('cora','pubmed') for seed in range(3)],'RAW_INSTABILITY_DIAGNOSIS')
        diagnosis_summary()
        batch([('run','A',ds,seed,arm,5) for seed in range(3) for ds in ('cora','pubmed') for arm in ('V1','V2','V3','V3_NULL','V3_SHUFFLE')],
              'STABILITY_PHASE_A')
        a=phase_summary('A',[0,1,2]);control_jobs=needs_shuffle(a)
        if control_jobs:batch(control_jobs,'NECESSARY_ARCHITECTURE_MATCHED_SHUFFLE_CONTROLS')
        a=phase_summary('A',[0,1,2]);write(OUT/'03_PHASE_A_RESULTS.json',a)
        batch([('behavior','R' if arm=='A2' else 'A',ds,seed,arm,'R') for ds in ('cora','pubmed') for seed in range(3) for arm in ('A2','V1','V2','V3')],
              'PHASE_A_CORRECTION_BEHAVIOR')
        behavior_report('A')
        selected=select_variant(a)
        write(OUT/'06_TRUE_VS_SHUFFLE.json',{'state':'COMPLETE','phase':'A',
             'datasets':{ds:{name:effect for name,effect in item['effects'].items() if '_SHUFFLE' in name} for ds,item in a['datasets'].items()},
             'selected_variant':selected,'matching_rule':'unchanged V18 kNN32 matched training donors; no labels','test_accessed':False})
        if selected is None:
            report('COMPLETE','CHRI_WEAK_SIGNAL_ONLY','V18_1_STABILIZATION_FAILED: no new variant improves worst-dataset CE-win stability and survives architecture-matched correspondence controls.');return
        batch([('prepare',ds,seed,10) for ds in ('cora','pubmed') for seed in range(5)],'PHASE_B_FROZEN_CACHE_PREPARATION',parallel=2)
        batch([('run','B',ds,seed,arm,10) for seed in range(5) for ds in ('cora','pubmed') for arm in ('A1','A2',selected,selected+'_NULL',selected+'_SHUFFLE')],
              'STABILITY_PHASE_B')
        formal=phase_summary('B',list(range(5)),selected);write(OUT/'05_PHASE_B_RESULTS.json',formal)
        write(OUT/'PHASE_B_FROZEN.json',{'state':'FROZEN','selected_variant':selected,'test_opened':False,
            'result_files':{str(p.relative_to(OUT)):sha(p) for p in (OUT/'runs/B').glob('*/*/*/result.json')},
            'source_files':read(OUT/'SOURCE_HASHES.json')['v18_source_files'],'frozen_at':time.time()})
        write(OUT/'06_TRUE_VS_SHUFFLE.json',{'state':'COMPLETE','phase':'B','selected_variant':selected,
            'datasets':{ds:item['effects']['STABLE_vs_SHUFFLE'] for ds,item in formal['datasets'].items()},
            'matching_rule':'unchanged V18 train-only initial-Z kNN32 matched donors','test_accessed':False})
        batch([('behavior','B',ds,seed,arm,'B') for ds in ('cora','pubmed') for seed in range(5) for arm in ('A2',selected)],
              'PHASE_B_CORRECTION_BEHAVIOR')
        behavior_report('B',selected);subgroup_analysis(selected)
        if formal['all_pass']:
            report('COMPLETE','CHRI_STABILITY_CONFIRMED','STABILITY_IMPROVED: both datasets pass five-seed CE/MRR and true-vs-NULL/SHUFFLE validation gates. Test remains sealed.');return
        correspondence=all(d['gates']['true_beats_shuffle'] and d['gates']['true_beats_null'] for d in formal['datasets'].values())
        raw_min=min(d['effects']['RAW_vs_Z']['ce']['wins'] for d in formal['datasets'].values())
        stable_min=min(d['effects']['STABLE_vs_Z']['ce']['wins'] for d in formal['datasets'].values())
        overall_positive=all(d['effects']['STABLE_vs_Z']['ce']['mean']>0 and d['effects']['STABLE_vs_Z']['mrr']['mean']>=0 for d in formal['datasets'].values())
        if correspondence and overall_positive and stable_min>raw_min:
            report('COMPLETE','CHRI_STABILITY_IMPROVED','Reliability improves over paired RAW, but the full five-seed confirmation gate fails; review before formal module validation.')
        else:
            flag='STABILIZATION_NOT_RELATION_SPECIFIC_OR_NULL_EXPLAINS_GAIN' if not correspondence else 'WEAK_SIGNAL_PERSISTS'
            report('COMPLETE','CHRI_WEAK_SIGNAL_ONLY',flag+': full five-seed validation does not establish recovered stable relation-specific signal.')
    except BaseException as error:
        for item in CHILDREN:
            if item['proc'].poll() is None:
                try:os.killpg(item['proc'].pid,__import__('signal').SIGTERM)
                except ProcessLookupError:pass
        failure={'state':'EXECUTION_FAILED','error':repr(error),'traceback':traceback.format_exc(),'ended_at':time.time(),
                 'test_opened':False,'historical_V18_modified':False}
        write(OUT/'ERROR.json',failure);write(OUT/'status.json',failure)
        print('V18_1_EXECUTION_FAILED',repr(error),flush=True);raise


if __name__=='__main__':
    command=sys.argv[1]
    if command=='preflight':preflight()
    elif command=='run':run(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],int(sys.argv[6]))
    elif command=='prepare':
        ds,seed,epochs=sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
        v.prepare_backbone(ds,seed,epochs);v.prepare_matching(ds,seed,epochs)
    elif command=='diagnose':raw_diagnosis(sys.argv[2],int(sys.argv[3]))
    elif command=='behavior':correction_behavior(sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5],sys.argv[6])
    elif command=='supervise':supervise()
    else:raise ValueError(command)
