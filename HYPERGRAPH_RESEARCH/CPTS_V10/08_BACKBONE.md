# Backbone generalization

Cora, fixed epoch 10, seeds 0–2. Frozen Graph-hard baselines reused from V7.1/V8; CPTS uses the unchanged local BIC selector.

| Backbone | Method | Seed 0 | Seed 1 | Seed 2 | Mean ± sample SD |
|---|---|---:|---:|---:|---:|
| GCN | GRAPH_HARD | 0.532759 | 0.328583 | 0.500069 | 0.453804 ± 0.109669 |
| GCN | CPTS | 0.494901 | 0.530459 | 0.585776 | 0.537045 ± 0.045794 |
| SAGE | GRAPH_HARD | 0.319458 | 0.391520 | 0.302562 | 0.337846 ± 0.047244 |
| SAGE | CPTS | 0.413666 | 0.492015 | 0.401331 | 0.435671 ± 0.049184 |
| GAT | GRAPH_HARD | 0.556319 | 0.446894 | 0.461373 | 0.488195 ± 0.059439 |
| GAT | CPTS | 0.542822 | 0.546529 | 0.536309 | 0.541887 ± 0.005174 |

| Backbone | CPTS − Graph-hard paired delta | Mean delta | Wins/3 |
|---|---|---:|---:|
| GCN | [-0.037858, 0.201876, 0.085707] | +0.083242 | 2/3 |
| SAGE | [0.094209, 0.100495, 0.098769] | +0.097824 | 3/3 |
| GAT | [-0.013496, 0.099635, 0.074936] | +0.053692 | 2/3 |