# Attempt 004 — Stage1 probe

Status: STOP at Stage1.

Five-seed aggregate balanced feature-only probe:

| Variant | AUC | AP |
|---|---:|---:|
| Base | 0.4157701 | 0.4658437 |
| DangerousControls | 0.4528546 | 0.4962229 |
| TrueMatch | 0.4707976 | 0.4911869 |
| ShuffledMatch | 0.4611069 | 0.4964072 |
| Proxy | 0.4598303 | 0.4908741 |

TrueMatch AUC exceeded DangerousControls by +0.017943, ShuffledMatch by +0.009691, and Proxy by +0.010967. However, TrueMatch AP was -0.005036 below DangerousControls and -0.005220 below ShuffledMatch. The candidate therefore fails the locked AUC+AP incremental gate and is not authorized for Stage2. No architecture rescue is allowed.
