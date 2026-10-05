# Attempt 007 — Stage1 probe

Status: STOP at Stage1.

Five-seed aggregate probe:

| Variant | AUC | AP |
|---|---:|---:|
| DangerousControls | 0.4528546 | 0.4962229 |
| TrueSpectral | 0.4571036 | 0.4971599 |
| ShuffledSpectral | 0.4528040 | 0.4952607 |
| Proxy | 0.4598303 | 0.4908741 |

TrueSpectral beats DangerousControls and ShuffledSpectral on AUC/AP, but loses to Proxy on AUC (0.45710 < 0.45983). Since `True <= Proxy` is an explicit STOP condition, Stage2 was not authorized despite the small AP gain.
