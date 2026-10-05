# Attempt 002 — Stage1 probe

Status: PASS for feature-only screening; not sufficient for final acceptance.

Aggregate validation probe across five Cora HeaRT seeds:

| variant | AUC mean | AP mean |
|---|---:|---:|
| Base | 0.45207 | 0.49468 |
| TrueRoute | 0.52930 | 0.52801 |
| ShuffledRoute | 0.45589 | 0.49459 |
| Proxy | 0.45518 | 0.48781 |

TrueRoute minus Base AUC: `+0.07723`; TrueRoute minus ShuffledRoute AUC: `+0.07341`; TrueRoute minus Proxy AUC: `+0.07412`.

The apparent signal was concentrated in the route<2 regime (503 validation pairs per seed); longer-route regimes had too few pairs for a strong claim. Stage2 remained mandatory.

Required: TrueRoute > Base, TrueRoute > ShuffledRoute and TrueRoute > Proxy on aggregate and in at least two meaningful route regimes. Failure means STOP without architectural rescue.
