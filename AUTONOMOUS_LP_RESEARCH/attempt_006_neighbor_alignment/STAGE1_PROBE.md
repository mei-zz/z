# Attempt 006 — Stage1 probe

Status: STOP at Stage1.

Five-seed aggregate probe:

| Variant | AUC | AP |
|---|---:|---:|
| DangerousControls | 0.4528546 | 0.4962229 |
| TrueAlign | 0.4467160 | 0.4881258 |
| ShuffledAlign | 0.4526204 | 0.4938984 |
| Proxy | 0.4598303 | 0.4908741 |

TrueAlign lost to DangerousControls, ShuffledAlign, and Proxy on both AUC and AP. Stage2 was not authorized.
