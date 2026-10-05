# Attempt 004 — Literature audit

Working name: Boundary Matching/Cover Profile (BMCP)

## Candidate object

For a candidate pair `(u,v)`, construct the bipartite graph induced by the exclusive neighborhoods `A=N(u)\\N(v)` and `B=N(v)\\N(u)`, with original training-graph edges between `A` and `B`. The object is the local maximum-matching/deficiency profile: matching size, unmatched mass on each side, matching saturation, perfect-boundary indicator, and side-size imbalance.

This is structurally different from the blacklisted CECG mechanism, which counts cross-neighborhood edges / L3 witnesses. BMCP asks whether the boundary can be covered by distinct representatives; it does not use the raw cross-edge count as a feature.

## Novelty-kill result

- Searches covered 2022–2026 homogeneous link prediction, graph matching, matching-based link prediction, neighborhood matching, Hall deficiency, exclusive-neighborhood matching, and CECG-adjacent terms.
- Matching is a known primitive in bipartite and anchor-link prediction, so the collision level is `L2`; the candidate is not claimed as a new matching algorithm or a new GNN architecture.
- Recent matching/link-prediction results found in the search were for bipartite recommendation, anchor alignment, or hypergraph/linkage settings rather than this pair-conditioned exclusive-boundary object on undirected homogeneous Cora HeaRT.
- The candidate is retained only for an inexpensive incremental probe. If it fails, the matching/cover object is blacklisted and will not be rescued with CECG-style edge counts, attention, gates, or extra modules.

## Sources checked

- [Link Prediction in Bipartite Networks (2024)](https://doi.org/10.1016/j.procs.2024.09.567) — matching/recommendation setting, not this homogeneous boundary object.
- [GCN-ALP: Addressing Matching Collisions in Anchor Link Prediction](https://arxiv.org/abs/2103.10600) — anchor-link alignment, not candidate-edge prediction in a homogeneous graph.
- [Beyond Link Prediction: Predicting Hyperlinks in Adjacency Space](https://ojs.aaai.org/index.php/AAAI/article/view/11780) — hyperlink prediction, not pairwise exclusive-boundary matching.
- [Complete-Tree Space Favors Data-Efficient Link Prediction (ICML 2025)](https://proceedings.mlr.press/v267/gao25g.html) — a different global representation and search object.
