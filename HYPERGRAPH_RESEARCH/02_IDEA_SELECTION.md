# 02 — idea selection and novelty screen

## Literature collision screen

The search was performed against primary paper pages where available. The following are established mechanisms, not novelty claims for this project:

- [Hypergraph Neural Networks (Feng et al., 2018)](https://arxiv.org/abs/1809.09401) already defines hyperedge convolution for high-order correlation and notes that ordinary graph convolution is a special case.
- [Hypergraph Convolution and Hypergraph Attention (Bai et al., 2019)](https://arxiv.org/abs/1901.08150) explicitly provides both hypergraph convolution and an attention operator. A learned hyperedge weight alone is therefore not a defensible new contribution.
- [A Hypergraph Neural Network Framework for Learning Hyperedge-Dependent Node Embeddings (Aponte et al., 2022)](https://arxiv.org/abs/2212.14077) learns hyperedge-dependent node embeddings and evaluates hyperedge prediction, so per-hyperedge adaptive representations are also prior art.
- [Link Prediction with Relational Hypergraphs (Huang et al., 2024)](https://arxiv.org/abs/2402.04062) studies link prediction directly on relational hypergraphs and its expressivity, making a generic “add hypergraph to link prediction” claim too broad.
- The [NSLR-HMANN hypergraph modeling and multi-view attention paper](https://www.sciencedirect.com/science/article/pii/S0031320324000438) combines structural hypergraph construction with node/hyperedge attention for link prediction. The page was accessible only through snippets in this environment; exact implementation-level overlap remains `NOVELTY_UNVERIFIED`.

## Candidate decisions

| Candidate | Problem / hypothesis | Mechanism | Main risk | Minimal falsifier | Decision |
|---|---|---|---|---|---|
| A. Adaptive Hyperedge Reliability | Some high-order sets are noisy under shift; training-only local evidence should downweight unreliable hyperedges. | Learned reliability from hyperedge size, overlap and local support. | Hyperedge attention, adaptive weights and reliability calibration are already common; the repository blacklist also blocks reliability/variance renamings. | Raw hypergraph vs learned reliability vs fixed and shuffled weights, with the same incidence. | `REJECT` as a primary idea; no distinct mechanism survived the collision screen. |
| B. Structural-role Hypergraph | Pairwise message passing may fail to distinguish nodes with different set-valued roles. | Motif/common-neighbor/role-defined hyperedges. | Existing CN, motif, enclosing-subgraph and structural-role searches already failed; triangles or common neighbors alone are not new. | Same information projected to an ordinary pairwise graph, plus shuffled hyperedges. | `INCONCLUSIVE` backup only; not implemented. |
| C. Shift-aware Hypergraph Fusion | The usefulness of pairwise and high-order messages changes by local regime. | A node/pair gate. | Collides with the blacklisted HL-GNN-PDG gate family and the V9 feature/topology fusion attribution failure. | Fixed, scalar-learned, proposed gate and shuffled gate under matched parameters. | `REJECT` before implementation. |
| Selected alternative: PCHR | A hypergraph may help only through information not already aligned with the pairwise encoder. | **Pairwise-Complementary Hypergraph Residual (PCHR):** build closed-neighborhood star hyperedges from the target-masked training message graph; subtract the per-node projection of the hypergraph message onto the pairwise node state; apply the same linear map as the raw hypergraph control. | It may remove useful signal, collapse to a generic residual layer, or be no better than an ordinary pairwise projection. | `B0` original, `B1` raw hypergraph, `B2` PCHR, `B3` shuffled assignment, `B4` pairwise co-membership projection, equal one-epoch budget. | Implemented and screened; `REJECT` after Cora seed-0 ranking. |

## Novelty status

PCHR is not claimed as a verified novel method. The search found standard hypergraph convolution, attention and hyperedge-dependent representations, but did not identify an exact paper using this particular per-node pairwise-complement projection as a link-prediction plug-in. That is only a gap in the search evidence, not proof of novelty. Status: `NOVELTY_UNVERIFIED`.

## Why PCHR was chosen for the minimal screen

It changes a measurable mechanism rather than adding a generic gate: the intervention is a geometric projection that predicts a concrete outcome. If the residual component is the useful part, PCHR should beat the raw hypergraph branch and the ordinary pairwise projection; if the hypergraph gain is merely extra two-hop information, `pairwise` should match it. Both predictions are directly testable without modifying the decoder, loss, candidate set or split.

