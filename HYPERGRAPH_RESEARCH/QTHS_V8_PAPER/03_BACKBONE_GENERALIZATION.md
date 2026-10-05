# Cora backbone generalization

All runs use the same Cora split, frozen graph-teacher 20-candidate pool, raw-star hypergraph mode, decoder, optimizer settings, negative count, 10 epochs and seed list. The only model change is the graph encoder backbone. GCN rows reuse V7.1 checkpoints; SAGE and GAT are new V8 runs.

| Backbone | Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD | QTHS−Graph-hard paired mean | Wins/3 |
|---|---|---:|---:|---:|---:|---:|---:|
| GCN | UNIFORM | 0.485973 | 0.591476 | 0.569234 | 0.548894 ± 0.055615 |  |  |
| GCN | GRAPH_HARD | 0.532759 | 0.328583 | 0.500069 | 0.453804 ± 0.109669 |  |  |
| GCN | QTHS25 | 0.530263 | 0.383612 | 0.510112 | 0.474662 ± 0.079493 | +0.020859 | 2/3 |
| SAGE | UNIFORM | 0.445986 | 0.508822 | 0.443569 | 0.466126 ± 0.036996 |  |  |
| SAGE | GRAPH_HARD | 0.319458 | 0.391520 | 0.302562 | 0.337846 ± 0.047244 |  |  |
| SAGE | QTHS25 | 0.320283 | 0.392616 | 0.344540 | 0.352479 ± 0.036814 | +0.014633 | 3/3 |
| GAT | UNIFORM | 0.535054 | 0.551363 | 0.529232 | 0.538550 ± 0.011472 |  |  |
| GAT | GRAPH_HARD | 0.556319 | 0.446894 | 0.461373 | 0.488195 ± 0.059439 |  |  |
| GAT | QTHS25 | 0.579761 | 0.482530 | 0.495491 | 0.519261 ± 0.052794 | +0.031066 | 3/3 |

- Positive backbones passing both mean and paired-win gates: 3/3.
- BACKBONE_GENERALIZATION: **YES**.
