# V10 Research Reset: Frozen Baseline Protocol

## Scope

This round audits inductive/cold-start link prediction only. It does not implement a new GNN module. The first executable setting is the public NodeDup inductive protocol on Cora and CiteSeer.

## Problem definition

The benchmark code creates a node split with 10% inference-time new nodes. Training uses the old-node subgraph and old-old training edges. Validation is an old-old link-ranking split. Test contains old-old, old-new, and new-new edges; most observed old-new/new-new context edges are available in the inference graph. Therefore this is an inductive/semi-cold-start protocol, not strict zero-shot link prediction with completely isolated new nodes. The distinction is preserved in all reports.

The official implementation uses 500 sampled negatives per source node and the average-rank MRR/Hits evaluator. The graph split seed is fixed by the repository at 234. Model seeds are run separately and are recorded independently.

## Locked models and settings

For each dataset, use the repository's published GraphSAGE settings: two SAGE layers, hidden size 256, dropout 0.5, sum predictor, Adam with the dataset-specific learning rate from `scripts/inductive.sh` (Cora `5e-4`, CiteSeer `1e-4`), 500 negatives, `metric=hits@20`, and validation-only checkpoint selection.

The low-cost audit uses 100 epochs and patience 20 for every learned method, with model seeds 1–3 and one run per process. This is a fixed screening budget, not a tuned setting. The existing published `augment=duplicated` method is included as a strong cold-start baseline; it is not proposed as a new contribution.

Fixed proxies are evaluated on exactly the same cached candidate groups and message/inference graphs:

- Feature cosine from original node features;
- Common-neighbor count;
- Resource Allocation score.

No proxy, model, subgroup, or direction is selected using test results. Test metrics are emitted only after validation checkpoint selection or as frozen proxy evaluation.

## Primary questions

1. Does the plain GraphSAGE baseline fail consistently on isolated/low-degree inference nodes?
2. Does the existing NodeDup baseline already explain or remove that failure on two real datasets?
3. Can a fixed feature or topology proxy reproduce the apparent cold-start gain?
4. Is there any residual, cross-dataset failure that cannot be explained by the existing methods and simple proxies?

An architecture is not allowed unless these controls leave a reproducible residual problem.
