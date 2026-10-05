# Attempt 002 — Literature audit

Working name: Block-Cut Route Profile (BCRP)

## New object

Using training positives only, decompose the graph into biconnected blocks and articulation vertices. For a candidate pair, expose the relation of its endpoints in this block-cut forest: shared block membership, route length, articulation incidence, and block-membership multiplicity.

## Collision search

- Exact and synonym searches: `block-cut tree link prediction`, `block-cutpoint route link prediction`, `biconnected-component pair representation`, `articulation-aware graph link prediction`, and the same primitives with KGE, recommender, graph classification, and graph matching.
- The search found graph-algorithm definitions and bridge/community work, but no complete link-prediction method using this pair-conditioned block-cut route object in this round.
- Collision level: `L2/L3`. It is adjacent to SEAL/NBFNet/path reasoning and bridge-link prediction, but it is a connectivity-decomposition object rather than a generic enclosing subgraph, path count, community label, or confidence score.
- Novelty wording: “In this round’s search scope, no complete isomorphic work was found.”

## Parent sees / misses

- Parent sees node embeddings, CN/AA/RA, degree, L3 and related local path summaries.
- Parent misses whether a pair is connected through articulation bottlenecks and how its endpoints are situated in the block-cut decomposition.

## Cheap-kill rationale

The block-cut forest is computed once per training graph, and pair descriptors are table lookups. Support and logistic incremental signal can therefore kill the idea without any GPU training.
