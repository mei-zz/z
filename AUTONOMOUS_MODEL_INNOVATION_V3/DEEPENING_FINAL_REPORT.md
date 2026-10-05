# CDPT Deepening V3 — Final Report

## Executive decision

**Final state: `WEAK_SIGNAL`.**

CDPT is implemented and active, and it improves MRR over the original Parent on Cora and on the independent CiteSeer run. The evidence does not establish that the improvement is caused specifically by learned cross-depth tensor interaction:

- On five Cora seeds, parameter-matched Late-only has higher mean test MRR than CDPT (`0.107691` vs `0.105725`).
- The fixed random operator has a higher mean Cora validation MRR delta than CDPT (`+0.009384` vs `+0.007241`).
- On CiteSeer, CDPT beats Late-only in test MRR (`0.131765` vs `0.122422`) but loses slightly in Hits@10 (`0.338462` vs `0.340659`) and is only one seed.

CDPT is worth limited attribution follow-up, not broad structure search. No CDPT V3 architecture is justified or implemented.

## Phase 0: audit outcome

The audit found two historical limitations and repaired the decision protocol:

1. V2 inspected Cora test metrics when promoting CDPT. That creates test-set selection bias. V2 results and failures are preserved as exploratory historical evidence only.
2. V2 Parent/Candidate training was sequential and did not fully reset random state before every training run. V3 resets Python/NumPy/PyTorch randomness before each constructor and training run, with the same Parent template state.

V3 selects checkpoints by validation MRR only, records `test_used_for_selection=false`, uses target-edge masking before node encoding, and keeps the fixed B0–B4 set unchanged before reading V3 test results. All Cora V3 results share data hash `98e4aaaf07d4`; CiteSeer uses an independent data hash `93b2480b3b56`.

The legacy “shuffled” control was also clarified: it rolls early pair-state rows against late pair-state rows, so it is a pair-alignment shuffle, not a pure encoder-depth permutation. Train-time and eval-time versions are reported separately and are not treated as interchangeable.

Peak GPU memory is now captured for every Cora seed/model by `torch.cuda.max_memory_allocated` (B0 55.438 MiB; B1 59.245 MiB; B2 59.294 MiB; B3 59.303 MiB; B4 59.341 MiB). The resource-complete reruns are kept separate because CUDA execution is not bitwise deterministic in this graph path; the largest original-versus-resource-rerun test-MRR difference was 0.013950. The performance aggregate consistently uses the first complete five-seed batch.

## Phase 1–3: Cora mechanism evidence

The five-model comparison uses the same encoder, data, optimizer, epochs, masking, and seed. Parameter counts are:

| Model | Total | Trainable |
|---|---:|---:|
| B0 Parent | 112,486 | 112,486 |
| B1 CDPT | 119,751 | 119,751 |
| B2 Late-only | 119,751 | 119,751 |
| B3 Concat MLP | 119,718 | 119,718 |
| B4 Fixed random | 119,751 | 118,727 |

Mean paired MRR deltas versus Parent over seeds 0–4:

| Model | Validation ΔMRR | Test ΔMRR | Validation wins | Test wins |
|---|---:|---:|---:|---:|
| B1 CDPT | +0.007241 ± 0.007760 | +0.008956 ± 0.011544 | 5/5 | 4/5 |
| B2 Late-only | +0.005557 ± 0.004244 | +0.010922 ± 0.009535 | 4/5 | 4/5 |
| B3 Concat MLP | +0.002506 ± 0.001332 | +0.001571 ± 0.003077 | 5/5 | 3/5 |
| B4 Fixed random | +0.009384 ± 0.005849 | +0.005283 ± 0.010766 | 5/5 | 3/5 |

The Cora seed0 CDPT test result is `0.093889` MRR, below Parent `0.100207`; this failure is retained. The full per-seed table is in `FIVE_SEED_RESULTS.md`.

Static checks found finite outputs, nonzero path gradients, and nonzero CDPT score contribution. Thus the mechanism is not dead code or a zero-scale collapse. However, a fixed random operator remains competitive, so activity alone does not establish causal attribution.

## Phase 4: independent CiteSeer evidence

The official CiteSeer HeaRT data were prepared from repository-provided difficult-negative files. The structure was locked before this run; test metrics were not used for selection.

| Model | Validation MRR | Test MRR | Test Hits@10 |
|---|---:|---:|---:|
| B0 Parent | 0.140228 | 0.108796 | 0.285714 |
| B1 CDPT | 0.145948 | 0.131765 | 0.338462 |
| B2 Late-only | 0.132304 | 0.122422 | 0.340659 |

CDPT improves test MRR over Parent by `+0.022969` and over Late-only by `+0.009344`. The small Hits@10 loss to Late-only, one-seed design, and reversed eval-shuffle behavior prevent a stronger claim.

## Researcher, Critic, Judge

### Researcher

CDPT has a real, nonzero cross-depth path and positive MRR evidence on two datasets. Its validation MRR advantage over Parent is reproducible on all five Cora seeds.

### Critic

Late-only preserves the parameter budget and matches or exceeds CDPT on Cora test MRR. A fixed random operator is competitive or better on Cora validation. The legacy shuffle is pair-alignment corruption rather than a pure depth permutation, and its effect reverses between Cora and CiteSeer. V2's test-based promotion remains a selection-bias caveat.

### Judge

The correct status is `WEAK_SIGNAL`: continue only with a cheap attribution test if needed; stop structure expansion. The evidence is insufficient for `CONFIRMED_PROMISING`, but it is not a total rejection because independent CiteSeer MRR supports CDPT over both Parent and Late-only.

## Final answers to the required questions

- **Is CDPT worth continued investment?** Limited verification investment only; not broad architecture investment.
- **What mechanism explains the gain?** A nonzero pair-decoder contribution is present, but current evidence cannot distinguish learned cross-depth interaction from late-only capacity or a generic/fixed quadratic operator.
- **What alternatives remain?** Parameterized late-only scoring, ordinary multi-scale fusion, fixed random operators, dataset-specific ranking behavior, training randomness, and historical test-selection bias.
- **Was an evidence-based new structure innovation found?** No. The evidence does not justify a CDPT V3 structure. The next falsifiable experiment is a true depth-order permutation control that preserves candidate-pair identity.
