# Attempt 005 — Stage1 probe

Status: PASS to one minimal Stage2 test.

Five-seed aggregate balanced probe:

| Variant | AUC | AP |
|---|---:|---:|
| Base | 0.4157701 | 0.4658437 |
| DangerousControls | 0.4528546 | 0.4962229 |
| TrueExpand | 0.4685452 | 0.5008576 |
| ShuffledExpand | 0.4547037 | 0.4948872 |
| Proxy | 0.4598303 | 0.4908741 |

TrueExpand beats DangerousControls, ShuffledExpand, and Proxy on both AUC and AP in aggregate, with deltas of +0.015691/+0.004635, +0.013841/+0.005970, and +0.008715/+0.009983 respectively. The object therefore earned one locked Stage2 integration run.
