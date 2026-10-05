# Attempt 003 — Stage1 probe

Status: CONDITIONAL PASS to one minimal Stage2 test; not a final pass.

Five-seed aggregate balanced feature-only probe:

| Variant | AUC | AP |
|---|---:|---:|
| Base | 0.4520667 | 0.4946832 |
| TrueNB | 0.4611011 | 0.4886848 |
| ShuffledNB | 0.4535558 | 0.4909258 |
| Proxy | 0.4583412 | 0.4910135 |

TrueNB minus Base was +0.009034 AUC; TrueNB minus ShuffledNB was +0.007545 AUC; TrueNB minus Proxy was +0.002760 AUC. The positive signal was present in the L3=0 and L3=1–3 regimes, but not stable for L3>=4, and TrueNB AP was lower than every control. Because two meaningful L3 regimes showed an AUC increment, one locked minimal parent-integration test was permitted. No architecture rescue was permitted.
