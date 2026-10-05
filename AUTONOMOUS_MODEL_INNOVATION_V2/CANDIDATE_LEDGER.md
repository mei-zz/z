# Candidate Ledger — V2

| ID | Candidate | Structural object | Closest literature / collision | Stage 0 | Stage 1 | Stage 2 | Stage 3 | Verdict |
|---|---|---|---|---|---|---|---|---|
| V2-001 | Pair-Conditioned Dynamic Transport (PCDT) | A candidate-pair token generates a low-rank linear transport operator; the operator re-aggregates each endpoint's masked neighborhood before a symmetric endpoint update and score. | High-risk adjacency to conditional message passing, NBFNet, and target-aware matching; not identical in the audited formulation because transport is a local endpoint-neighborhood operator added to DCDLP's late branches. | pass | pass, ΔMRR +0.01883 vs Parent | killed by shuffled-evaluation control; no Stage 2 promotion | not run | STOP (F9, with F4 risk) |
| V2-002 | Cross-Depth Pair Tensor Decoder (CDPT) | A symmetric pair state is formed at each encoder depth and coupled by a learned cross-depth tensor contraction rather than concatenation or a scalar gate. | Bilinear/low-rank link decoders, multi-scale pair representations, and layer aggregation; no exact isomorphism was found in the bounded audit, so the result is reported as promising rather than globally novel. | pass | pass, ΔMRR +0.00807 vs Parent | pass, ΔMRR +0.00800; trained shuffled control lower | pass: mean ΔMRR +0.00873, 2/3 seeds improved, Hits means positive | PROMISING; deepening mode |

## Researcher/Critic/Experimentalist/Judge — V2-001

### Researcher

The native DCDLP encoder is candidate-independent. A missing link can be supported by different endpoint neighborhoods even when the final endpoint states and late pair branches look similar. A pair-conditioned transport operator could expose compatibility between the candidate pair and the two endpoint neighborhoods before the final score, adding a structural computation rather than another hand-designed statistic.

### Critic

Conditional message passing is an established family, and a dynamic operator can collapse to a degree-sensitive scalar or to an ordinary pair decoder. The candidate risks high novelty collision, quadratic pair-neighborhood cost, and train/eval mismatch from masking a batch of target edges. It must pass an exact symmetry test, randomized-operator control, a simple-proxy control, and a non-collapse test before any long run.

### Experimentalist

Implement one extra local transport step after the existing encoder. Use the same masked edge list and the same training/evaluation candidates as the parent. Keep hidden and branch dimensions fixed; report exact parameter count, peak memory, wall time, transport norm, and score contribution. Stage 1 uses one Cora seed and short training; Stage 2 uses one seed with the official ranking protocol; Stage 3 uses seeds 0--2 only if Stage 2 passes.

### Judge

Proceed to static audit only. Do not claim novelty or promise improvement. Kill before training if the candidate is equivalent to a post-hoc pair feature, violates exchange symmetry, materially exceeds the resource cap, or is indistinguishable from the parent with the transport path disabled.

## Researcher/Critic/Experimentalist/Judge — V2-002

### Researcher

The Parent exposes only the final node state to its pair branches. CDPT preserves the same graph encoder but forms a link state at an early and a late propagation depth, then models their compatibility with a bilinear cross-depth operator. The hypothesis is that link evidence can depend on a transition between structural scales, not on a pooled multi-scale feature vector.

### Critic

Cross-depth interaction is adjacent to layer aggregation, multi-scale link prediction, and bilinear decoders. It could reduce to a late-only pair decoder, an extra parameterized score, or a depth-dependent gate. A positive result is therefore conditional and must be accompanied by parent-equivalence, shuffled-depth, proxy, parameter, and seed checks.

### Experimentalist

Use a shared pair encoder for early and late states, one learned cross-depth tensor, and one scalar score contribution. Keep the Parent initialization, optimizer, batch size, masking, official HeaRT candidates, and early validation selection identical. Train one short Stage 1 seed, one short Stage 2 seed with a trained shuffled-depth control, and three fixed Stage 3 seeds.

### Judge

Proceed because the structure is distinct from the inherited feature blacklist, has an exact zero-scale parent limit, is exchange invariant, and fits the resource budget. Promotion requires mean ΔMRR > 0, at least 2/3 MRR seed wins, no systematic Hits regression, and a control that does not reproduce the gain.
