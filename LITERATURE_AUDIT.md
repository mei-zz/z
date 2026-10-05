# Literature Audit — V2

## Scope and result

The search covered recent primary/official sources on link prediction message passing, structural link representation, target-aware matching, and conditional message passing. The nearest established ideas are:

1. MPLP argues that ordinary node-level message passing misses joint link structure and uses message passing to estimate common-neighbor-like information.
2. SLRGNN transforms link prediction to node classification on a line graph; this is explicitly excluded by the inherited line-graph/edge-centric blacklist.
3. The conditional-message-passing theory describes pair-conditioned node representations and therefore creates a high collision risk for any generic target-conditioned GNN.
4. CRAFT uses target-aware matching for temporal link prediction; it is not a static homogeneous-graph implementation, but it reinforces the collision risk around generic pair matching.
5. Recent work on generalization cautions that link-level MPNN behavior depends on structural and architectural assumptions, supporting a controlled architecture audit rather than a feature-only probe.

## V2-001 boundary

PCDT is not claimed to be globally novel. Its testable distinction is narrower: a static DCDLP node encoder is augmented with a pair-token-generated low-rank transport operator that is applied separately to the two masked endpoint neighborhoods and then fed through a symmetric endpoint update. The audit must kill it if the implementation is reducible to known conditional message passing or if empirical behavior is equivalent to a late pair decoder.

## Sources

- Dong, Guo, and Chawla, “Pure Message Passing Can Estimate Common Neighbor for Link Prediction,” NeurIPS 2024: https://proceedings.neurips.cc/paper_files/paper/2024/hash/85970f7bbc821852c1d17052b88c2451-Abstract-Conference.html
- Lachi et al., “A Simple and Expressive Graph Neural Network Based Method for Structural Link Representation,” PMLR 251, 2024: https://proceedings.mlr.press/v251/lachi24a.html
- Huang et al., “A Theory of Link Prediction via Conditional Message Passing Neural Networks,” OpenReview: https://openreview.net/pdf?id=7hLlZNrkt5
- Yi et al., “Future Link Prediction Without Memory or Aggregation,” NeurIPS 2025: https://proceedings.neurips.cc/paper_files/paper/2025/hash/036912a83bdbb1fd792baf6532f1022d8-Abstract-Conference.html
- Vasileiou, Stoll, and Morris, “Understanding Generalization in Node and Link Prediction,” AISTATS 2026: https://proceedings.mlr.press/v300/vasileiou26a.html
