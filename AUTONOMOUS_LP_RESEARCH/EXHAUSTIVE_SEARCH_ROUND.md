# Exhaustive search round — final audit

Date: 2026-09-16

The loop did not find a validated GO/STRONG GO. Ten new candidates reached executable probes or minimal integrations after the imported blacklist was applied:

| Candidate | Highest stage | Result |
|---|---|---|
| R1-03 Internally Vertex-Disjoint Short-Path Profile | Stage2 | STOP: ranking AUC below Parent/Proxy; AP below shuffled |
| R1-07 Neighbor-Role Transition Matrix | Stage2 | STOP: integration collapsed below Parent/Shuffled |
| R2-01 Block-Cut Route Profile | Stage2 | STOP: weak AUC gain did not transfer to AP/MRR/Hits |
| R3-01 Non-Backtracking Continuation Profile | Stage2 | STOP: below Parent/Shuffled and far below Proxy |
| R4-01 Boundary Matching/Cover Profile | Stage1 | STOP: AUC gain but AP below controls/shuffled |
| R4-03 Boundary Expansion Deficit | Stage2 | STOP: mixed ranking; lost Parent/Proxy on key metrics |
| R4-07 Neighbor Signature Alignment Profile | Stage1 | STOP: below controls and shuffled |
| R4-08 Fixed Laplacian Spectral Band Profile | Stage1 | STOP: AUC below Proxy |
| R4-12 Exclusive-Neighborhood Cohesion Profile | Stage2 | STOP: lost Proxy on every aggregate ranking metric |
| R4-13 Multi-Scale Community Boundary Profile | Stage2 | STOP: below Parent on all aggregate ranking metrics |

Remaining queued ideas were removed from execution for one of two reasons:

- direct literature collision: common-neighbor witness graphs, enclosing-subgraph distance coupling, cycle-space/persistent-homology objects, line-graph edge incidence, motif/CN distribution summaries, community/flow similarity, and spectral/diffusion profiles;
- empirical family collision: separator/bridge/cut candidates after R2-01, path-redundancy candidates after R1-03/R3-01, matching/cover candidates after R4-01, cohesion/expansion candidates after R4-03/R4-12, and endpoint-role/homophily candidates after R1-07/R4-07/R4-13.

This is the permitted hard-stop condition `NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH` for the current static undirected Cora HeaRT environment. It is not a validated scientific idea and must not be presented as GO.
