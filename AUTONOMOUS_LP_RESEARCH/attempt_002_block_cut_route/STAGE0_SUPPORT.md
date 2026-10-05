# Attempt 002 — Stage0 support

Status: PASS.

Across five Cora HeaRT seeds (the train graph structure is identical across these processed splits):

| label | total | reachable in block-cut forest | shared block | articulation incident | route >=2 | route >=4 |
|---|---:|---:|---:|---:|---:|---:|
| positive | 2,635 | 2,250 | 1,515 | 1,200 | 215 | 15 |
| negative | 1,317,500 | 1,133,215 | 773,330 | 494,585 | 121,435 | 14,720 |

The route object was non-constant and extraction cost was below one second per seed. It proceeded to Stage1.

Kill if the block-cut route is nearly constant, if positive or negative informative support is below 200 pairs, or if extraction is not cheap enough for the benchmark.
