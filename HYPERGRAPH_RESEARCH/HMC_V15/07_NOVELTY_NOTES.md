# Focused Novelty Notes

**Status: `EXACT_RULE_UNVERIFIED`** (focused search, 2026-10-03). No exact collision was established in the sources checked. This is not an exhaustive priority search; several full texts are paywalled or available only as abstracts, so do not claim “first.”

## Closest prior work checked

- [HMNE: link prediction using hypergraph motifs and network embedding in social networks](https://link.springer.com/article/10.1007/s10115-024-02255-8) uses hypergraph motifs/hyper-nodes, local motif random walks, and skip-gram node embeddings for link prediction. Its accessible description does not show an encoder of the candidate pair's support-wise joint incidence multiplicities.
- [HMRLH: Research on a Link Prediction Algorithm Based on Hypergraph Representation Learning](https://www.mdpi.com/2079-9292/12/23/4842) represents open/closed hypermotifs as supernodes, then uses motif random walks and skip-gram to learn node embeddings. This is a close hypergraph-motif link-prediction neighbor, but the described prediction path is node-embedding based rather than the tested pair-specific joint-support encoder.
- [Link prediction in social networks using hyper-motif representation on hypergraph](https://doi.org/10.1007/s00530-024-01324-w) is another close prior: it uses hyper-motif representations and motif-guided walks for node embeddings. Its accessible abstract does not establish the exact HMC rule below.
- [Hypergraph Motif Representation Learning (KDD 2025)](https://doi.org/10.1145/3690624.3709274) predicts higher-order h-motifs using hypergraph and graph convolutions. The prediction target is h-motifs, not an ordinary candidate node pair.
- [Simplicial closure and higher-order link prediction](https://pmc.ncbi.nlm.nih.gov/articles/PMC6275482/) and the [simplicial motif predictor method](https://www.sciencedirect.com/science/article/pii/S0957417424031518) study closure/prediction of higher-order simplices or motifs, a related but different target from ordinary pairwise links.
- [Directed Hypergraph Representation Learning for Link Prediction](https://proceedings.mlr.press/v238/ma24b.html) performs pairwise link prediction with a directed-hypergraph neural representation. [Heterogeneous Hypergraph Variational Autoencoder for Link Prediction](https://doi.org/10.1109/TPAMI.2021.3059313) learns node/hyperedge representations for heterogeneous link prediction. These are relevant HGNN link-prediction baselines; their accessible descriptions do not establish HMC's support-wise joint multiplicity decoder.

## Exact-collision test

The correction requires one method to combine all of: ordinary pairwise link prediction; a hypergraph; candidate-pair shared support nodes; multiplicity from each endpoint to each same support; a permutation-invariant encoding of the resulting joint multiset; and use of that encoding as pair-decoder/residual input. The sources above establish nearby combinations of hypergraph motifs and link prediction, but the accessible methods descriptions do not establish all six elements together. Exact collision therefore remains **unverified**, not ruled out.

Preferred positioning if revisited: **support-wise co-incidence multiplicity encoding** or **multiplicity-aware pair-specific hypergraph closure**. Do not claim that these counts are unrecoverable from a weighted 2-section; the corrected hypothesis is about explicitly exposing their pair-specific joint pattern to the decoder.
