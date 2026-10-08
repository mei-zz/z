# V6 blacklist

- Do not modify DCDLP, GNN/HGNN layers, features, decoder, optimizer, loss, graph split, or hypergraph construction.
- Do not tune veto ratio, prepool multiplier, disagreement lambda, or epoch schedule after seeing validation results.
- Do not use validation/test model scores or outcomes to build, rank, or select training negatives.
- Preserve the standard sampler's all-positive forbidden-edge filter and explicitly disclose its use of held-out positive identities.
- Do not call cross-view ambiguity a verified false negative.
- Do not run test unless Candidate A satisfies the specified 3-seed STRONG_SIGNAL gate; when authorized, evaluate only A1, A3, and A4.
- Do not proceed to B after Candidate A GO; do not proceed to C unless A and B reject and B0 remains >=0.53.
- Do not claim “first” or exact novelty based on this focused search.
