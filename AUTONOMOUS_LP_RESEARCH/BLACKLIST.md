# Empirical Blacklist and Lessons

This file is cumulative. A STOP candidate remains here even when a later name sounds different.

## Permanent blacklist

- DCDLP Degree/CN Disentanglement: degree/CN/residual disentanglement, targeted degree/CN intervention, causal separation, conditional-CN residual.
- MPLP-VC: variance feature, uncertainty feature, confidence readout, estimator disagreement, reliability calibration, unless the structural object is genuinely different.
- NCN-CNDP: CN variance, second-moment pooling, mean/max/variance summaries, simple distribution pooling, adding one CN summary.
- HL-GNN-PDG: soft residual gate, pair-conditioned soft gate, adaptive hop gate, soft routing, mixtures of existing representations.
- CECG: exclusive-neighborhood L3 interaction, candidate-edge 4-cycle closure, L3 witness interaction graph, CECG and direct renamings.
- R1-07 Neighbor-Role Transition Matrix: degree-shell role-transition histograms on length-3 paths, unless a future candidate changes the structural object itself rather than the bucketization/decoder.
- R2-01 Block-Cut Route Profile: pair descriptors from biconnected blocks/articulation routes, unless a future candidate uses a genuinely different connectivity object.
- R3-01 Non-Backtracking Continuation Profile: continuation-count distributions over legal `u-a-b-c-v` non-backtracking paths, including total count, active continuation states, concentration, and count buckets; do not retry as a renamed non-backtracking, Hashimoto, or line-graph feature.
- R4-01 Boundary Matching/Cover Profile: maximum matching size, saturation, unmatched-side mass, perfect-boundary indicator, and side imbalance for the exclusive-neighborhood bipartite boundary; do not retry as a renamed CECG cross-edge count or cover statistic.
- R4-03 Boundary Expansion Deficit: two-sided frontier sizes, frontier overlap, exclusive frontier masses, normalized one-step growth, and side imbalance outside the exclusive-neighborhood boundary; do not retry as a renamed neighborhood-expansion or boundary-overlap feature.
- R4-07 Neighbor Signature Alignment Profile: endpoint-internal neighbor degree-shell/within-side-connectivity role alignment histogram, aligned mass, and side imbalance; do not retry as a renamed neighborhood-role similarity or histogram.
- R4-08 Fixed Laplacian Spectral Band Profile: fixed low-frequency squared endpoint differences and resistance-weighted spectral bands from a training-graph Laplacian basis; do not retry as a renamed spectral/diffusion-distance profile.
- R1-03 Internally Vertex-Disjoint Short-Path Profile: greedy mixed internally vertex-disjoint length-2/3 capacity, saturation ratios, and raw-to-disjoint gaps; do not retry as a renamed path-redundancy or separator-capacity feature.
- R4-12 Exclusive-Neighborhood Cohesion Profile: internal edge counts/densities, mean internal degree, dispersion, and side contrast within `N(u)\\N(v)` and `N(v)\\N(u)`; do not retry as a renamed clustering/cohesion feature.
- R4-13 Multi-Scale Community Boundary Profile: same-community status, within/outside neighborhood mass, boundary ratios, community-size contrast, and community coverage; do not retry as a renamed community or modular-flow feature.

## Empirical lessons

1. Reliability signal is not prediction gain.
2. Second-moment CN information is not automatically a stable incremental signal.
3. A soft pair gate may collapse to the parent.
4. A new-looking topology can reduce to known L3/graphlet signal.
5. True-vs-shuffled control is mandatory.
6. Mechanism subgroup support must be checked before large experiments.
7. Cora/CiteSeer Hits@100 can have insufficient headroom; inspect AUC/AP/MRR/Hits@10/50 as appropriate.
8. The next candidate must add a structural relation/object, not a scalar statistic or a gate over existing states.
9. A balanced train/validation feature probe can overestimate usefulness when the locked benchmark test uses many hard negatives; ranking-protocol alignment must be checked before treating a probe as model evidence.
10. A candidate object can have a positive logistic delta yet fail when the parent must learn it jointly; true-vs-shuffled must be checked after integration, not only before it.
11. Connectivity-decomposition features can dominate a balanced AUC probe but fail to transfer to locked 500-negative ranking; rare long-route subgroups cannot support a broad mechanism claim.
12. A continuation profile can beat a shuffled null in balanced classification while losing to both the parent and a scalar proxy under official ranking; AUC-only Stage1 evidence is insufficient when AP and ranking metrics move together in the wrong direction.
13. A matching/cover object can raise AUC while lowering AP against both controls; require both metrics before authorizing an integration run.
14. A feature-only AUC/AP pass can still yield a mixed ranking result: inspect MRR and Hits@10/50/100, seed-wise collapse, and proxy comparison before calling GO.
15. Endpoint-internal neighborhood role alignment can be worse than its shuffled null; role similarity is not automatically link-specific signal.
16. A fixed spectral profile can beat dangerous controls and shuffled null yet lose a simple scalar proxy; spectral-family novelty risk does not justify ignoring the proxy STOP rule.
17. A positive feature-only redundancy probe can disappear under ranking: disjoint capacity lost Parent/Proxy AUC and the shuffled null on AP.
18. A large Parent gain is not enough when a simple proxy wins every ranking metric; the proxy remains a hard control even when the parent itself is unstable.
19. Community-boundary features can separate balanced probes yet collapse under official ranking; community collision risk and ranking evidence both argue against retrying this family.

## Search constraints for the next candidates

- No candidate may proceed to GPU training without novelty audit, support audit, feature-only incremental probe, shuffled null, and simple-proxy control.
- A candidate is not rescued with attention, gating, extra depth, larger hidden size, new loss, optimizer changes, or repeated tuning after Stage1 failure.
