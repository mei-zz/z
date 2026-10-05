# Attempt 001 — Stage1 feature-only probe

Status: PASS for feature-only screening; not sufficient for final acceptance.

Aggregate validation probe across Cora HeaRT seeds 0–4:

| variant | AUC mean ± sd | AP mean ± sd |
|---|---:|---:|
| DangerousControls | 0.45207 ± 0.00225 | 0.49468 ± 0.00326 |
| TrueRole | 0.46350 ± 0.00418 | 0.50130 ± 0.00505 |
| ShuffledRole | 0.45825 ± 0.00450 | 0.49769 ± 0.00457 |

TrueRole minus DangerousControls: AUC `+0.01144`, AP `+0.00661`.

TrueRole minus ShuffledRole: AUC `+0.00526`, AP `+0.00360`.

The improvement was positive in multiple L3 regimes, but this probe used a balanced validation view. Stage2 remained mandatory.

Required evidence for Stage1 GO:

- TrueRole improves over DangerousControls on at least two meaningful regimes/seeds;
- TrueRole is better than ShuffledRole in aggregate;
- TrueRole is not explained by the scalar proxy;
- the result is not a one-seed artifact and extraction cost remains reasonable.

If any decisive condition fails, mark this attempt STOP and do not add a GNN module.
