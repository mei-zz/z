# Problem Gap Audit

## Fixed scope

The three pre-registered problem scenarios were:

| Scenario | Research question | Public evidence checked | Remote feasibility | Current status |
|---|---|---|---|---|
| A. Incomplete/noisy graph | Does message passing amplify missing or spurious observed edges? | PULL (AAAI 2025) and CORE (TKDD 2026) | The current repository has no Cora-full/PULL data; remote CoraFull acquisition from the official PyG URL stalled and was interrupted after more than 90 seconds | NOT_EXECUTED; no result is claimed |
| B. Inductive/new nodes | Does the Parent rely on training-node topology and fail when test endpoints are unseen? | LEAP (2025 preprint), OGB link benchmarks, official NCN code | Current DCDLP supports OGB loaders, but the remote cache has no OGB data and the available NCN Cora loader uses its own random split, not an inductive split | NOT_EXECUTED; no result is claimed |
| C. Hard negatives/distribution shift | Does Parent fail on fixed structurally difficult candidate sets? | LPShift (KDD 2025 Datasets & Benchmarks), HeaRT official candidates | Fully feasible on remote Cora HeaRT; fixed 500 negatives per positive and existing train/validation/test artifacts were available | AUDITED; failure is real but currently explained by existing proxies |

## Literature and protocol implications

### A: incomplete/noisy graph

PULL explicitly treats observed edges as positive and nonedges as unlabeled rather than assuming the observed graph is complete. CORE is a later topology-completion/noise-handling line. These are not merely decoder changes: they alter the data-generating assumption and the graph used by propagation. Consequently, a future candidate in this space would need an explicit missing-edge/noise protocol and must beat PULL/CORE-like controls. It cannot be evaluated by simply masking one target pair in ordinary HeaRT.

### B: inductive/new nodes

LEAP is a direct precedent for learnable topology augmentation in an inductive link-prediction setting. Official NCN code was inspected, but its Planetoid Cora path creates a random link split and is not a clean new-node benchmark. Running it beside HeaRT would be a protocol error. A future B experiment requires a predeclared node-disjoint split, feature availability for held-out nodes, and a strong inductive baseline such as GraphSAGE/NCN under the same split.

### C: hard negatives/distribution shift

LPShift provides a modern benchmark framing in which the split controls structural distribution shift. The available Cora HeaRT artifacts are not LPShift and are retained under their original HeaRT identity. This audit therefore calls the result “hard-negative failure on Cora HeaRT,” not “LPShift validation.”

## Decision from the gap audit

Only C has an executable, protocol-valid baseline failure in the current remote workspace. It is not yet a model gap: fixed classical proxies already outperform Parent on validation MRR, and their failure pattern is itself informative. A new model would need to improve over those proxies and established pair-aware methods while using only the train graph. No such independent state/propagation rule was identified without entering an existing collision family.

## Sources

- [PULL official repository](https://github.com/snudatalab/PULL)
- [CORE DOI record](https://doi.org/10.1145/3789200)
- [LPShift official repository](https://github.com/revolins/LPShift)
- [LPShift arXiv record](https://arxiv.org/abs/2406.08788)
- [LEAP arXiv record](https://arxiv.org/abs/2503.03331)
- [Neural Common Neighbor official repository](https://github.com/GraphPKU/NeuralCommonNeighbor)
