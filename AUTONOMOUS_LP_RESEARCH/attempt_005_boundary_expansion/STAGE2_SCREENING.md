# Attempt 005 — Stage2 minimal parent integration

Status: STOP / weak mixed result.

The three-seed locked ranking screen used identical 80-epoch protocols and 500 negatives per positive:

| Variant | AUC | AP | MRR | Hits@10 | Hits@50 | Hits@100 |
|---|---:|---:|---:|---:|---:|---:|
| Parent | 0.6478340 | 0.0075459 | 0.1119307 | 0.2131562 | 0.3902593 | 0.4807084 |
| TrueExpand | 0.6962465 | 0.0075851 | 0.1021668 | 0.1967109 | 0.4054396 | 0.5275142 |
| ShuffledExpand | 0.6403009 | 0.0052838 | 0.0701253 | 0.1302973 | 0.3308033 | 0.4408602 |
| Proxy | 0.6767536 | 0.0073683 | 0.1099339 | 0.2137887 | 0.4528779 | 0.5452245 |

TrueExpand beats Parent on aggregate AUC, AP, Hits@50, and Hits@100, and beats ShuffledExpand on every aggregate metric. However, it loses to Parent on aggregate MRR and Hits@10, and loses to Proxy on aggregate MRR, Hits@10, Hits@50, and Hits@100. Seed 0 is a clear collapse, while seed 1 supplies most of the gain. With only one dataset available and mixed primary ranking metrics, this is a weak result under the locked GO rules (`True > Proxy` is not satisfied across the ranking metrics). STOP; no rescue module or tuning is allowed.
