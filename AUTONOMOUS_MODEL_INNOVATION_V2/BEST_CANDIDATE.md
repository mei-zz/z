# Best Candidate — V2

## V2-002 Cross-Depth Pair Tensor Decoder (CDPT)

CDPT retains DCDLP's masked global encoder and late branches, but exposes the pair representation at two propagation depths. For each depth it forms a symmetric pair state `[h_u*h_v, |h_u-h_v|, h_u+h_v]`, maps it into a shared pair space, and applies a learned cross-depth tensor contraction between the early and late pair states. The resulting scalar is added as a structural score. It is neither ordinary feature concatenation nor a scalar gate.

## Locked evidence

| Seed | Parent MRR | CDPT MRR | ΔMRR | ΔHits@10 | ΔHits@20 | ΔHits@50 | ΔHits@100 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.09987 | 0.10787 | +0.00800 | +0.01898 | +0.03226 | +0.01708 | +0.01898 |
| 1 | 0.10498 | 0.09933 | -0.00565 | -0.00380 | -0.01518 | -0.00380 | -0.00759 |
| 2 | 0.09267 | 0.11652 | +0.02385 | +0.05313 | +0.06452 | +0.09488 | +0.07590 |
| Mean Δ | — | — | **+0.00873** | **+0.02277** | **+0.02720** | **+0.03605** | **+0.02910** |

The locked gate is met: mean ΔMRR > 0, 2/3 seed MRR improvements, and no systematic Hits decline. Stage 2's trained shuffled structural-path control was below CDPT on MRR and all Hits on seed 0 (0.10756 vs 0.10787 MRR). The CN proxy MRR was 0.09777.

## Caveat and deepening mode

Only Cora HeaRT was executable in this environment and the runs used four short epochs. Seed 1 regressed, so this is `FOUND_PROMISING_INNOVATION`, not a general SOTA claim. Deepening should focus on a matched late-only pair decoder, fixed/random depth-operator controls, and broader datasets when available; it must not turn into hyperparameter rescue.
