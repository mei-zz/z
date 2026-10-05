# Attempt 002 — Stage2 minimal parent integration

Status: STOP.

Parent: the deterministic scalar structural pair decoder used in the prior locked screening.

TrueRoute: Parent plus the fixed block-cut route object.

Controls: same-width ShuffledRoute and scalar Proxy variants, with exact same train/validation/test pair lists and 500 test negatives per positive.

No attention, gate, extra loss, larger hidden layer, or optimizer rescue is allowed.

## Locked screening result

Three Cora HeaRT seeds used identical train negatives, validation negatives, 500 test negatives per positive, optimizer, learning rate, 80-epoch budget and validation-selection rule.

| variant | AUC mean | AP mean | MRR mean | Hits@10 mean | Hits@50 mean | Hits@100 mean |
|---|---:|---:|---:|---:|---:|---:|
| Parent | 0.57989 | 0.00675 | 0.09050 | 0.17584 | 0.30930 | 0.38077 |
| TrueRoute | 0.58291 | 0.00518 | 0.06012 | 0.12460 | 0.28906 | 0.38836 |
| ShuffledRoute | 0.57843 | 0.00426 | 0.05055 | 0.10436 | 0.24605 | 0.38204 |
| Proxy | 0.67453 | 0.00779 | 0.10621 | 0.21695 | 0.45225 | 0.54396 |

TrueRoute had only a `+0.00302` mean AUC delta versus Parent, was below Proxy by `-0.09162` AUC, and had negative aggregate AP/MRR/Hits@10/Hits@50 deltas. It does not meet GO or STRONG GO.
