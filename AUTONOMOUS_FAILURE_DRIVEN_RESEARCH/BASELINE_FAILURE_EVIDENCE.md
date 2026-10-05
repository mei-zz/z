# Baseline Failure Evidence

## Remote execution boundary

All experiments in this document were executed on the server specified by `.env`, in conda environment `mei_env`, using the remote project `/home/ubuntu/DCDLP-main`. No model training was run locally. Raw JSON is preserved under [`raw/cora_heart_baselines`](raw/cora_heart_baselines).

Fixed Cora HeaRT facts:

- 4,488 train positives, 263 validation positives, 527 test positives.
- Official grouped candidate tensor shape `[527, 500, 2]`; 500 negatives per test positive.
- Candidate hash: `3d3960e42cbae3befddb666195eff1b66ef1a473813eb21ff99bdb41311ce1cc`.
- Split hash: `4d52b749074b`.
- All three Parent seeds used the same split and candidate hash; only training seed changed.
- Checkpoint selection used validation MRR inside the existing training code. Test values below were read only after the fixed runs and were not used to choose a model or direction.

## Parent validation results

| Seed | Validation MRR | Hits@10 | AUC | Best epoch |
|---:|---:|---:|---:|---:|
| 0 | 0.09867394 | 0.25475285 | 0.85591052 | from checkpoint |
| 1 | 0.10889872 | 0.24714829 | 0.81348478 | from checkpoint |
| 2 | 0.09119153 | 0.22433460 | 0.84762895 | from checkpoint |
| **Mean ± SD** | **0.09958806 ± 0.00888892** | — | — | — |

## Parent held-out test results

| Seed | Test MRR | Hits@10 | Hits@20 | Hits@50 | Hits@100 | AUC | AP | Train seconds | Peak GPU MB | Parameters |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.09986684 | 0.24478178 | 0.36812144 | 0.59582543 | 0.77419355 | 0.85820358 | 0.00852881 | 95.7562 | 55.46 | 112,486 |
| 1 | 0.10529825 | 0.22770398 | 0.35483871 | 0.53130930 | 0.71347249 | 0.81820749 | 0.00762849 | 96.3092 | 55.46 | 112,486 |
| 2 | 0.09326480 | 0.22580645 | 0.35673624 | 0.54079696 | 0.73244782 | 0.84253025 | 0.00772846 | 98.6473 | 55.46 | 112,486 |
| **Mean ± SD** | **0.09947663 ± 0.00602621** | **0.23276407 ± 0.01045080** | **0.35989880 ± 0.00718394** | **0.55597723 ± 0.03483408** | **0.74003795 ± 0.03106396** | **0.83964710 ± 0.02015332** | **0.00796192 ± 0.00049348** | **96.9042** | **55.46** | **112,486** |

## Predeclared proxy results on the same official candidates

These are fixed, non-learned classical proxies computed from the train graph. They were not tuned on test data. Validation is the decision-side comparison; test is shown only as a held-out descriptive check.

| Proxy | Validation MRR | Validation Hits@10 | Test MRR | Test Hits@10 | Test AUC |
|---|---:|---:|---:|---:|---:|
| CN | 0.11612312 | 0.25855513 | 0.09776815 | 0.20113852 | 0.66331122 |
| Adamic–Adar | **0.13417046** | **0.29277567** | **0.11913903** | **0.24098672** | 0.66991216 |
| Resource Allocation | 0.13236648 | 0.28517110 | 0.11808347 | 0.24288425 | 0.66976853 |
| Jaccard | 0.12461346 | 0.22053232 | 0.10182839 | 0.21062619 | 0.66471178 |
| Feature cosine | 0.09836496 | 0.18631179 | **0.12471537** | 0.23719165 | **0.77774809** |

The validation comparison is already enough to reject a claim that the current Parent is the strongest explanation of the Cora HeaRT signal: Adamic–Adar exceeds the Parent validation mean by `+0.03458240`, and CN exceeds it by `+0.01653505`. The test-side feature-cosine result is not used to select a model; it is reported because it demonstrates a second alternative explanation based on the supplied node features.

## Stable error subgroup

The existing evaluation partitions positives using a train-only median degree score and a train-fitted symmetric conditional-CN residual. It is not based on test performance or endpoint order. Parent test MRR by group:

| Seed | HH | HL | LH | LL | Worst group | Group gap |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.17338837 | 0.02096635 | 0.23758215 | 0.03128245 | 0.02096635 | 0.21661580 |
| 1 | 0.19701596 | 0.01814839 | 0.20456586 | 0.02685708 | 0.01814839 | 0.18641748 |
| 2 | 0.16426109 | 0.01898421 | 0.22058686 | 0.02363194 | 0.01898421 | 0.20160265 |
| **Mean** | **0.17822181** | **0.01936631** | **0.22091170** | **0.02725716** | — | — |

The HL/LL weakness repeats in all three seeds. However, AA/RA and feature similarity change the ranking of several groups, so the observation is a reproducible failure pattern, not evidence of a new propagation mechanism.

## What this evidence proves and does not prove

**Directly supported:** Parent is unstable at the seed level; it has a large, repeatable low-MRR subgroup on Cora HeaRT; fixed local and feature proxies provide credible alternative explanations; the hard-negative scenario is worth documenting.

**Not supported:** A new neural architecture, a causal claim that message passing is the bottleneck, or a claim that a new structure should be added. To make that claim, a candidate must beat AA/RA, feature controls, and a protocol-aligned strong pair-aware baseline on validation without relying on test selection.
