import tarfile,pathlib
p=pathlib.Path(r'E:\Z\DCDLP_Server_Backup_20261005\lchr_v2_full_server_backup.tar.gz')
t=tarfile.open(p,'r:gz')
print(t, type(next(iter(t))))
t.close()
