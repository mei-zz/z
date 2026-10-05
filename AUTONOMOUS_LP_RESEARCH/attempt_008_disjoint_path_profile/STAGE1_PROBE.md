# Attempt 008 — Stage1 probe

Status: PASS to one minimal Stage2 test.

Five-seed aggregate probe:

| Variant | AUC | AP |
|---|---:|---:|
| DangerousControls | 0.4528546 | 0.4962229 |
| TrueDisjoint | 0.4688618 | 0.5035215 |
| ShuffledDisjoint | 0.4673293 | 0.5026784 |
| Proxy | 0.4598332 | 0.4908757 |

TrueDisjoint beat all three controls on aggregate AUC and AP, so one minimal Stage2 test was authorized. The True-vs-Shuffled margin was small and required ranking confirmation.
