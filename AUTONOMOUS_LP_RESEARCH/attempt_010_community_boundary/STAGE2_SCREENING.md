# Attempt 010 — Stage2 minimal parent integration

Status: STOP.

Three-seed locked ranking screen:

| Variant | AUC | AP | MRR | Hits@10 | Hits@50 | Hits@100 |
|---|---:|---:|---:|---:|---:|---:|
| Parent | 0.6610492 | 0.0083594 | 0.1237833 | 0.2346616 | 0.4117647 | 0.5079064 |
| TrueCommunity | 0.6188304 | 0.0061032 | 0.0677266 | 0.1404175 | 0.2991777 | 0.4048071 |
| ShuffledCommunity | 0.6258490 | 0.0051780 | 0.0522099 | 0.1195446 | 0.3023403 | 0.4111322 |
| Proxy | 0.6736528 | 0.0069923 | 0.1112810 | 0.2182163 | 0.4471853 | 0.5426945 |

TrueCommunity loses Parent on every aggregate ranking metric and loses Proxy on AUC, AP, MRR, and Hits@10. STOP; the community object is not a validated incremental innovation.
