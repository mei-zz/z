# Deepening Mode — CDPT

Broad candidate search is closed after `FOUND_PROMISING_INNOVATION`.

## Focused next checks

1. Mechanism ablation: compare cross-depth contraction with a parameter-matched late-only pair decoder.
2. Operator ablation: compare the learned depth operator with fixed identity and randomized frozen operators.
3. Reproducibility: rerun the locked 4-epoch protocol with the existing Cora seeds 0--4 and retain every seed, including regressions.
4. Generalization: repeat only after a second official dataset is available; do not substitute a synthetic or uniform-candidate score for the unavailable benchmark.
5. Reporting: preserve official candidate hashes, masking rules, parameter counts, peak memory, runtime, and all seed-wise MRR/Hits.

No optimizer, learning-rate, hidden-size, loss, or generic gating sweep is part of deepening.
