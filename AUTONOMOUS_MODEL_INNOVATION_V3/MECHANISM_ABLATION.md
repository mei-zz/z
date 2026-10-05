# CDPT Deepening V3 — Mechanism Ablation

## Protocol lock

All B0–B4 models use the same Cora HeaRT split, uniform training negatives, official HeaRT validation/test candidates, target-edge masking, optimizer, four epochs, hidden/branch dimensions, and paired seed. Checkpoint selection uses validation MRR only. Every V3 JSON records `test_used_for_selection=false`.

The V2 test-based promotion remains a historical selection-bias caveat. It is not used as a V3 decision rule.

## Model controls

| ID | Decoder change | Total parameters | Trainable parameters | Purpose |
|---|---|---:|---:|---|
| B0 | Original DCDLP Parent | 112,486 | 112,486 | baseline |
| B1 | Early pair state × learned operator × late pair state | 119,751 | 119,751 | CDPT candidate |
| B2 | Late pair state × learned operator × late pair state | 119,751 | 119,751 | parameter-matched late-only control |
| B3 | Concatenated early/late pair states + small MLP | 119,718 | 119,718 | ordinary multi-scale fusion control |
| B4 | CDPT path with one fixed random operator | 119,751 | 118,727 | learned-operator necessity control |

B3 differs from B1 by 33 parameters, about 0.028% of the full model. B4 samples its operator once at construction and never resamples it at evaluation.

## Static mechanism checks

The audit found finite outputs, nonzero changed-path gradients, and nonzero score-path magnitudes. In the locked configuration, the CDPT path has a nonzero learned scale and nonzero operator norm. The five Cora runs have mean absolute changed-path score 0.733040, mean scale 0.146844, and mean operator norm 5.884240. This rejects an implementation-level collapse explanation, but nonzero activity is not proof that the activity is the source of ranking gains.

The fixed random control is also active, with mean absolute path score 0.418043 and no trainable operator. This is important: CDPT's path is used, but the Cora results do not show that learning the cross-depth operator is required.

## Cora HeaRT five-seed aggregate

The table reports mean ± sample SD over seeds 0–4. The Cora test column is a frozen report, but its historical V2 selection caveat remains attached.

| Model | Validation MRR | Test MRR | Validation Hits@10 | Test Hits@10 |
|---|---:|---:|---:|---:|
| B0 Parent | 0.097386 ± 0.007889 | 0.096769 ± 0.009089 | 0.236502 | 0.228083 |
| B1 CDPT | 0.104627 ± 0.008476 | 0.105725 ± 0.006771 | 0.264639 | 0.257685 |
| B2 Late-only | 0.102943 ± 0.005666 | 0.107691 ± 0.005925 | 0.259316 | 0.250474 |
| B3 Concat MLP | 0.099892 ± 0.008964 | 0.098340 ± 0.009196 | 0.242586 | 0.231879 |
| B4 Fixed random | 0.106771 ± 0.007665 | 0.102052 ± 0.003052 | 0.256274 | 0.235294 |

Paired MRR deltas versus B0:

| Model | Validation ΔMRR | Approx. 95% t interval | Test ΔMRR | Approx. 95% t interval | Validation wins | Test wins |
|---|---:|---:|---:|---:|---:|---:|
| B1 CDPT | +0.007241 | [-0.002395, +0.016876] | +0.008956 | [-0.005378, +0.023290] | 5/5 | 4/5 |
| B2 Late-only | +0.005557 | [+0.000288, +0.010826] | +0.010922 | [-0.000918, +0.022761] | 4/5 | 4/5 |
| B3 Concat MLP | +0.002506 | [+0.000852, +0.004159] | +0.001571 | [-0.002250, +0.005391] | 5/5 | 3/5 |
| B4 Fixed random | +0.009384 | [+0.002122, +0.016646] | +0.005283 | [-0.008084, +0.018651] | 5/5 | 3/5 |

The five-seed intervals are descriptive, not a claim of statistical significance. The strongest direct mechanism challenge is that B4 has the highest validation MRR delta, while B2 has a higher mean Cora test MRR than B1.

## Shuffle controls

The legacy V2 shuffled control is preserved, but audited precisely: it rolls the early pair-state rows relative to the late pair-state rows. It is therefore a **pair-alignment shuffle**, not a pure permutation of encoder-depth order. The two timings are reported separately.

On Cora seed 0:

| Control | Validation MRR | Test MRR | Interpretation |
|---|---:|---:|---|
| aligned B1 CDPT | 0.110618 | 0.093889 | normal training and evaluation |
| train-time pair-alignment shuffle | 0.102912 | 0.107561 | shuffle applied during learning |
| eval-time pair-alignment shuffle | — | 0.087382 | shuffle applied only after aligned training |

On CiteSeer seed 0, aligned B1 test MRR is 0.131765, train-time shuffled B1 is 0.120901, and eval-time pair-alignment shuffle is 0.174799. The opposite Cora/CiteSeer behavior makes the shuffle result a diagnostic control, not a standalone proof.

## Mechanism verdict

The evidence supports a weaker statement: the CDPT path is implemented, active, and can improve MRR under the locked protocol. It does not support the stronger statement that a **learned cross-depth tensor interaction** is responsible for the main gain. Late-only, concat fusion, and especially a fixed random operator reproduce much of the Cora improvement; CiteSeer supports CDPT in MRR but leaves a small Hits@10 advantage to Late-only. No CDPT V3 structure is justified by this ablation.

