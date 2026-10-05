# Cora train graph: star hyperedge structure

## Protocol and construction

The diagnostic uses the Cora standard seed-0 split and constructs the same closed-neighborhood star hyperedges as the raw hypergraph branch: `e_c = {c} U N(c)`. The graph contains 2,708 nodes and 4,488 training/message edges; it yields 2,620 non-empty star hyperedges. All counts and structural features come from `train_pos` only. Validation/test links are not inserted into the graph.

For each hyperedge, the report computes total induced-pair density, off-center leaf density, number of leaf-leaf training edges (equivalently center-containing triangles), and mean top-3 Jaccard overlap among hyperedges sharing at least one node. Shared-node overlap candidates are generated with an inverted incidence index, avoiding all-pairs hyperedge comparison.

## Distributions

| Measure | Mean | SD | P25 | Median | P75 | P90 | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hyperedge size | 4.426 | 4.561 | 3 | 4 | 5 | 7 | 151 |
| Center degree | 3.426 | 4.561 | 2 | 3 | 4 | 6 | 150 |
| Full induced pair density | 0.690 | 0.248 | 0.500 | 0.667 | 1.000 | 1.000 | 1.000 |
| Off-center density `rho_e` | 0.187 | 0.300 | 0 | 0 | 0.333 | 0.667 | 1.000 |
| Leaf-leaf edges / center triangles | 1.146 | 2.902 | 0 | 0 | 1 | 3 | 96 |
| Shared-node top-3 mean Jaccard | 0.392 | 0.174 | 0.283 | 0.349 | 0.433 | 0.583 | 1.000 |

Node hyperdegree has mean 4.282, SD 4.554, median 4, P90 7, and maximum 151.

## Associations

Off-center cohesion is almost uncorrelated with hyperedge size under Pearson (`r=-0.006`), though rank correlation is positive (`rho=0.469`); size control is therefore necessary. Full induced density falls as size grows (Pearson `r=-0.537`, Spearman `rho=-0.866`). The count of leaf edges grows with size (Pearson `r=0.843`). Top-3 overlap redundancy has weak size association (Pearson `r=-0.170`, Spearman `rho=0.007`). Cohesion and redundancy are moderately associated (Pearson `r=0.293`, Spearman `rho=0.471`), so Candidate A must be compared against the separate redundancy hypothesis rather than interpreted in isolation.

Full precision and reproducible calculation are in `structure_diagnostics.json` and `structure_diagnostics.py`.
