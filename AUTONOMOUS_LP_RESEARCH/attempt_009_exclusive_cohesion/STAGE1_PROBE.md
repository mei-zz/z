# Attempt 009 — Stage1 probe

Status: PASS to one minimal Stage2 test.

Five-seed aggregate probe:

| Variant | AUC | AP |
|---|---:|---:|
| DangerousControls | 0.4528546 | 0.4962229 |
| TrueCohesion | 0.4865344 | 0.4991221 |
| ShuffledCohesion | 0.4574275 | 0.4945495 |
| Proxy | 0.4598303 | 0.4908741 |

TrueCohesion beat all controls on both AUC and AP, so one locked Stage2 test was authorized.
