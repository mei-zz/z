# LCHR mechanism analysis

Validation candidates were rescored with the frozen B4 checkpoint. Entropy tertiles were formed from validation-positive router entropy (88 / 88 / 87 positives); B1, B3 and B4 were compared on the same positives and grouped uniform negatives.

| Entropy group | B1 MRR | B3 MRR | B4 MRR |
|---|---:|---:|---:|
| Low | 0.262725 | 0.228016 | 0.227784 |
| Mid | 0.119283 | 0.101848 | 0.101881 |
| High | 0.105724 | 0.064865 | 0.064662 |

Router diagnostics across 5,523 validation candidates (positives plus negatives):

- Mean candidate-pool size: 9.068 hyperedges; Top-K=8.
- Empty-pool fraction: 0.000724 (0.072%).
- Mean entropy: 1.8778; mean top-1 weight: 0.1634.
- Mean pairwise cosine similarity between positive-candidate routing vectors: 0.00645 across 34,453 pairs.

The low cross-candidate similarity indicates routing vectors are not collapsing to one shared weighting pattern. However, the entropy-stratified MRRs show no useful advantage over B3; the small route variation did not translate into link-prediction gain. Detailed values and exact bin cut points are in `results.json`.
