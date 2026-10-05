# Attempt 001 — Stage0 support

Status: PASS.

Remote Cora HeaRT seeds 0–4, using the train graph for extraction and official test candidates for support:

| label | total | nonzero role object | at least 2 role paths | at least 5 role paths | multiple role states | mean role paths |
|---|---:|---:|---:|---:|---:|---:|
| positive | 2,635 | 1,455 | 950 | 370 | 785 | 2.0057 |
| negative | 1,317,500 | 205,800 | 120,485 | 35,725 | 97,845 | 0.4815 |

Support was sufficient, so the candidate proceeded to Stage1.

Kill rules:

- positive or negative informative support below 200 pairs;
- fewer than 200 pairs with at least two role-transition paths in either label;
- the object is nearly constant or almost exactly reducible to the scalar controls;
- extraction cost is clearly disproportionate to the Cora protocol.
