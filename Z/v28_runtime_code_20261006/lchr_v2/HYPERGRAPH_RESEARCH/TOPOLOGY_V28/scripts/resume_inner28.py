"""Resume V28 after the shared inner-structure preparation race; no model changes."""
import topology28 as m
from pathlib import Path
import os,signal,time,traceback

def main():
    try:
        m.configure('canonical');m.e.ART=m.ART;m.check_frozen_all()
        frozen=m.read(m.ART/'SOURCE_HASHES.json');frozen['files'][str(Path(__file__).resolve().relative_to(m.REPO))]=m.sha(Path(__file__))
        m.artifact('SOURCE_HASHES.json',frozen)
        a=m.read(m.ART/'06_PHASE_A_METRICS.json');record=m.read(m.ART/'11_PHASE_B_NEW_SEED_RESULTS.json');b=record['new_seeds_only'];selected=record['selected_hypotheses']
        eligible={ds:[item for item in selected if all(b['datasets'][ds]['effects'][f'{item["candidate"]}_vs_{c}']['ce']['mean']>0 for c in m.PRIMARY[item['hypothesis']])] for ds in ('cora','pubmed')}
        audit=m.read(m.ART/'INNER_SPLIT_AUDIT.json');m.configure('inner')
        # One owner builds shared files before any seed workers start.
        structures={}
        for ds,items in eligible.items():
            if not items:continue
            a_inner=m.sealed(ds)
            for name,expected in audit['datasets'][ds]['hashes'].items():assert m.array_hash(a_inner[name])==expected,'INNER_INPUT_CHANGED'
            with m.threadpool_limits(limits=4,user_api='blas'):meta=m.build_structure(a_inner['x'],a_inner['train'],m.cache(ds)/'structure.npz')
            meta.update(state='PASS',dataset=ds);m.write(m.cache(ds)/'STRUCTURE_READY.json',meta);m.e.prepare_context(ds)
            structures[ds]={'structure_sha256':m.sha(m.cache(ds)/'structure.npz'),'context_sha256':m.sha(m.e.context_path(ds)),'target_mask_oracle':meta['target_mask_oracle']}
        m.artifact('RECOVERY_AUDIT.json',{'state':'RESUMED','reason':'Concurrent writers to per-dataset inner structure.npz caused EOFError before inner model training.','fix':'Single supervisor builds and audits each shared structure/context before launching seed workers.','structures':structures,'Phase_A_and_B_reused_unchanged':True,'model_optimizer_split_feature_definitions_changed':False,'test_opened':False})
        m.configure('canonical')
        m.batch([('data','inner',ds,s,10) for ds,items in eligible.items() if items for s in (3,4,5)],'INNER_TRAIN_BACKBONE_AND_CACHE_RECOVERED',workers=2)
        m.batch([('features','inner',ds,s,1) for ds,items in eligible.items() if items for s in (3,4,5)],'INNER_FEATURES')
        inner={}
        for ds,items in eligible.items():
            if not items:continue
            arms=tuple(dict.fromkeys(x for item in items for x in (item['candidate'],*item['controls'])))
            m.batch([('train','inner',f'I{epochs}',ds,s,arm,1,epochs) for epochs in (5,10) for s in (3,4,5) for arm in arms],f'INNER_VALIDATION_{ds.upper()}')
            m.configure('inner');inner[ds]={'eligible_hypotheses':items,'budgets':{str(epochs):m.add_bootstrap(m.summary(f'I{epochs}',(3,4,5),arms,(ds,))) for epochs in (5,10)}};m.configure('canonical')
        m.artifact('12_PHASE_B_INNER_VALIDATION.json',{'state':'COMPLETE','protocol':'V28_INNER_TRAIN_VALIDATION_V1','datasets':inner,'not_run_datasets':{ds:'No positive new-seed primary hypothesis on this dataset.' for ds,items in eligible.items() if not items}})
        m.artifact('13_EPOCH_STABILITY.json',{'state':'COMPLETE','datasets':inner,'budgets':[5,10],'checkpoint_selection':'final epoch only, no validation checkpoint optimization'})
        m.finish(a,selected,b,inner)
    except BaseException as err:
        for p in m.CHILDREN:
            if p.poll() is None:
                try:os.killpg(p.pid,signal.SIGTERM)
                except ProcessLookupError:pass
        failed={'state':'EXECUTION_FAILED','error':repr(err),'traceback':traceback.format_exc(),'test_opened':False};m.artifact('ERROR.json',failed);m.artifact('RUN_STATUS.json',failed);m.write(m.OUT/'RUN_STATUS.json',failed);print(traceback.format_exc(),flush=True);raise
if __name__=='__main__':main()
