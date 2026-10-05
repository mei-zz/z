# Attempt 001 — Stage2 minimal parent integration

Status: STOP.

Parent: a deterministic scalar structural pair decoder trained on the real Cora HeaRT train split. It consumes CN/AA/RA/degree/L3/Local-Path/CH2-L3/CH3-L3 controls.

TrueRole: the same decoder with one appended 10-dimensional Neighbor-Role Transition Matrix.

Controls: same-width ShuffledRole and Proxy variants, using exact same pair lists, negative candidates, optimizer, learning rate, epochs and validation-selection rule.

GO criteria: TrueRole must beat Parent and ShuffledRole in aggregate, beat Proxy, show at least 4/6 paired seed/regime improvements when applicable, and avoid a material efficiency failure. Otherwise STOP and blacklist the mechanism.

## Locked screening result

Three Cora HeaRT seeds were run with the exact same train negatives, validation negatives, 500 test negatives per positive, optimizer, learning rate, 80-epoch budget, and validation-selection rule.

| seed | Parent AUC | TrueRole AUC | ShuffledRole AUC | Proxy AUC | TrueRole Hits@10 | Parent Hits@10 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.67492 | 0.67513 | 0.68362 | 0.68374 | 0.27135 | 0.24099 |
| 1 | 0.67037 | 0.64906 | 0.65576 | 0.66029 | 0.20683 | 0.24478 |
| 2 | 0.68058 | 0.47078 | 0.47250 | 0.64806 | 0.13662 | 0.25996 |
| mean | 0.67529 | 0.59832 | 0.60396 | 0.66403 | 0.20493 | 0.24858 |

TrueRole mean AUC delta versus Parent was `-0.07697`, versus ShuffledRole it was `-0.00564`, and versus Proxy it was `-0.06571`. MRR and Hits@50/100 also declined in aggregate. The feature-only probe did not survive the locked ranking protocol.
