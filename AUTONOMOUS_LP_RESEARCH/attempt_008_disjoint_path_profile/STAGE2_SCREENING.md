# Attempt 008 — Stage2 minimal parent integration

Status: STOP.

Three-seed locked ranking screen:

| Variant | AUC | AP | MRR | Hits@10 | Hits@50 | Hits@100 |
|---|---:|---:|---:|---:|---:|---:|
| Parent | 0.6126239 | 0.0063051 | 0.1174649 | 0.1853257 | 0.3333333 | 0.4010120 |
| TrueDisjoint | 0.6076383 | 0.0069325 | 0.1118626 | 0.2144213 | 0.3959519 | 0.4718533 |
| ShuffledDisjoint | 0.6056566 | 0.0069366 | 0.1046138 | 0.2055661 | 0.3908918 | 0.4667932 |
| Proxy | 0.6667527 | 0.0067061 | 0.1015368 | 0.1865908 | 0.4225174 | 0.5319418 |

TrueDisjoint lost Parent and Proxy on AUC, lost Parent on MRR, and lost ShuffledDisjoint on AP. It also lost Proxy on AUC/Hits@50/Hits@100. The candidate is STOP; no rescue is allowed.
