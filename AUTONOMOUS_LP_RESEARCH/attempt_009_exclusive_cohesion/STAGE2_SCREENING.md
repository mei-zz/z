# Attempt 009 — Stage2 minimal parent integration

Status: STOP.

Three-seed locked ranking screen:

| Variant | AUC | AP | MRR | Hits@10 | Hits@50 | Hits@100 |
|---|---:|---:|---:|---:|---:|---:|
| Parent | 0.5344010 | 0.0037705 | 0.0426685 | 0.0702087 | 0.1941809 | 0.2928526 |
| TrueCohesion | 0.6643247 | 0.0064690 | 0.0966684 | 0.1872233 | 0.3118280 | 0.4098672 |
| ShuffledCohesion | 0.6411261 | 0.0067999 | 0.0926848 | 0.1771031 | 0.3175206 | 0.4149273 |
| Proxy | 0.6890884 | 0.0068484 | 0.1006691 | 0.2080961 | 0.4528779 | 0.5698925 |

TrueCohesion beats Parent and ShuffledCohesion on AUC, MRR, Hits@10, and is competitive on Hits@50/100, but it loses Proxy on every aggregate metric. The proxy STOP condition is decisive; this candidate is not a GO.
