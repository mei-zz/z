# Attempt 003 — Stage2 minimal parent integration

Status: STOP.

Parent: the locked scalar structural pair decoder. TrueNB appended the non-backtracking continuation profile; ShuffledNB and Proxy preserved the same input width and protocol. Seeds 0, 1, and 2 used the same 80-epoch protocol and official 500-negative ranking evaluation.

| Variant | AUC | AP | MRR | Hits@10 | Hits@50 | Hits@100 |
|---|---:|---:|---:|---:|---:|---:|
| Parent | 0.6571601 | 0.0081285 | 0.1173540 | 0.2251739 | 0.4123972 | 0.4990512 |
| TrueNB | 0.6437794 | 0.0056540 | 0.0959925 | 0.1777356 | 0.3706515 | 0.4813409 |
| ShuffledNB | 0.6452676 | 0.0060481 | 0.1128595 | 0.2043011 | 0.3896268 | 0.5167615 |
| Proxy | 0.6905335 | 0.0086206 | 0.1263572 | 0.2523720 | 0.4851360 | 0.5768501 |

TrueNB lost to Parent on every listed metric, lost to ShuffledNB on AUC/AP/MRR/Hits@10/Hits@50, and lost to the simple Proxy on every metric. Aggregate TrueNB minus Parent was -0.013381 AUC, -0.002474 AP, -0.021362 MRR, and -0.047438 Hits@10. The candidate is blacklisted; no extra module, gate, attention, loss, depth, or tuning is allowed.
