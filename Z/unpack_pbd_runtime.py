import tarfile,json,hashlib
from pathlib import Path
root=Path('/home/zhoulihui/DCDLP-main');prior=Path('/home/zhoulihui/lchr_v2')
assert not root.exists(),'ISOLATED_DEPLOYMENT_ALREADY_EXISTS'
manifest=json.loads(Path('/home/zhoulihui/PBD_V30B_TRANSPORT_MANIFEST.json').read_text())
differences=[];matches=0
for rel,h in manifest.items():
    old=prior/rel
    if old.is_file():
        actual=hashlib.sha256(old.read_bytes()).hexdigest()
        if actual!=h:differences.append({'path':rel,'existing_sha256':actual,'required_sha256':h})
        else:matches+=1
root.mkdir()
with tarfile.open('/home/zhoulihui/PBD_V30B_RUNTIME.tar.gz','r:gz') as archive:
    for m in archive.getmembers():
        assert m.isfile() and (root/m.name).resolve().is_relative_to(root)
    archive.extractall(root,filter='data')
for rel,h in manifest.items():assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==h,rel
art=root/'result/innovation2/PBD_V30B';art.mkdir(parents=True)
(art/'DEPLOYMENT_RECONCILIATION.json').write_text(json.dumps({'state':'PASS','server':'10.16.15.66','root':str(root),'logical_workspace':'DCDLP-main','existing_deployment':str(prior),'existing_source_differences':differences,'existing_matching_files':matches,'transport_files_verified':len(manifest),'existing_files_overwritten':False,'test_members_transferred':False,'input_seal':'Onlyx/train/valid_pos/valid_neg extracted from archived input, never test members'},indent=2))
print('ISOLATED_DEPLOYMENT_VERIFIED',len(manifest),'existing_differences',len(differences))
