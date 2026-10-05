# CPTS V10 final report

**Status: EXECUTED — all gated stages complete.** The server reports no active training jobs; the Tesla V100 is idle. Protocol remained `STRICT_TRAIN_ONLY`, K=1, M=20, three seeds, 10 epochs, fixed epoch-10 checkpoint. No test candidates were opened before the Cora validation gate passed. PubMed and Citeseer results below are validation results; only Cora was evaluated on the frozen test candidates, as specified by the staged plan.

## Final decision

**GO (not STRONG_GO).** CPTS passed the registered Cora validation gates and the Cora test support gate. It improved over Graph-hard in validation on Cora, PubMed and Citeseer and on all three Cora backbones. Results are mixed against the strongest hardness-region baselines: QTHS25 beats CPTS on PubMed, SH75 beats CPTS on Citeseer, and Matched-Q is 0.002 MRR above CPTS on the Cora test set. The evidence supports CPTS as a viable adaptive selector, but not a universal winner or an established first method.

**Paper story: PARTIAL.** The train-only audit confirms heterogeneous local tail sizes, and validation supports the local rule over Global-CPTS, Matched-Q and Random-Matched. Cora test supports CPTS against Graph-hard, QTHS25 and SH75, but not against Matched-Q by mean. Keep the held-out matched-quantile caveat and the dataset-specific baseline reversals in the paper.

## Protocol and method

For each positive, CPTS sorts its 20 frozen graph-teacher scores and compares a one-segment Gaussian model with every permitted two-contiguous-segment model using the registered BIC formulas in `01_METHOD.md`. If BIC selects two segments, CPTS removes the inferred upper tail and selects the hardest candidate below its boundary; otherwise it selects Graph-hard. No percentile, trim ratio, trainable parameter or extra neural forward was added. Sorting costs O(M log M); the prefix-sum split scan costs O(M) per positive.

## Tail structure audit

| Dataset | Positives × candidates | Tail detected | Mean / median / p90 tail size | Exact tail-size buckets >10% | Modal tail size / share |
|---|---:|---:|---:|---:|---:|
| Cora | 4,488 × 20 | 100% | 6.826 / 7 / 11 | 5 | 2 / 19.1% |
| PubMed | 37,676 × 20 | 100% | 5.753 / 6 / 9 | 5 | 5 / 14.1% |
| Citeseer | 3,870 × 20 | 100% | 7.432 / 7 / 10 | 4 | 7 / 17.5% |

All three datasets pass the registered anti-collapse gate: at least three tail-size buckets exceed 10%, and no single tail size exceeds 80%. No positive was classified as no-tail under this BIC rule. Full 0–20 bin counts, hashes and score diagnostics are in `results.json` and `tail_audit.json`.

Cora selection overlap was 0% with Graph-hard, 0% with QTHS25, and 4.23–4.68% with SH75 across seeds. CPTS selected mean rank 7.83 from hardest (median 8), compared with rank 1 for Graph-hard, rank 1.5 for QTHS25, and about rank 13 for SH75. The Cora train-only mean tail fraction was 0.3413; Matched-Q therefore removed seven candidates uniformly and selected rank 8.

## Cora validation

| Method | Seed 0 | Seed 1 | Seed 2 | Mean MRR |
|---|---:|---:|---:|---:|
| Graph-hard | 0.532759 | 0.328583 | 0.500069 | 0.453804 |
| QTHS25 | 0.530263 | 0.383612 | 0.510112 | 0.474662 |
| SH75 | 0.494523 | 0.552162 | 0.556404 | 0.534363 |
| CPTS | 0.494901 | 0.530459 | 0.585776 | 0.537045 |
| Global-CPTS | 0.454645 | 0.345047 | 0.530634 | 0.443442 |
| Matched-Q | 0.499867 | 0.515114 | 0.569308 | 0.528096 |
| Random-Matched | 0.535604 | 0.357739 | 0.530796 | 0.474713 |

CPTS paired deltas: **+0.083242 vs Graph-hard (2/3 wins), +0.062383 vs QTHS25 (2/3), +0.002682 vs SH75 (2/3), +0.093604 vs Global-CPTS (3/3), +0.008949 vs Matched-Q (2/3), and +0.062333 vs Random-Matched (2/3).** The registered validation decision was GO; the local-adaptivity and matched-control gates passed.

## Cora test

| Method | Mean MRR ± sample SD |
|---|---:|
| Graph-hard | 0.472552 ± 0.093757 |
| QTHS25 | 0.493377 ± 0.094352 |
| SH75 | 0.541575 ± 0.034388 |
| CPTS | **0.549076 ± 0.048415** |
| Matched-Q | 0.551122 ± 0.049336 |
| Random-Matched | 0.484298 ± 0.101912 |

CPTS paired deltas were +0.076525 vs Graph-hard (2/3 wins), +0.055699 vs QTHS25 (2/3), +0.007501 vs SH75 (2/3), −0.002046 vs Matched-Q (1/3), and +0.064778 vs Random-Matched (2/3). The registered Cora test gate is **SUPPORTED**. The slight Matched-Q advantage is a meaningful limit on the held-out adaptivity claim.

## PubMed validation

| Method | Mean MRR ± sample SD |
|---|---:|
| Graph-hard | 0.803706 ± 0.029743 |
| QTHS25 | **0.844267 ± 0.009034** |
| CPTS | 0.836954 ± 0.007643 |
| SH75 | 0.774026 ± 0.021739 |

CPTS is +0.033249 over Graph-hard (3/3 wins), +0.062928 over SH75 (3/3), and −0.007313 against QTHS25 (0/3). The predeclared clear-reversal flag was false, so the Citeseer gate remained open. No PubMed test evaluation was run.

## Citeseer validation

| Method | Mean MRR ± sample SD |
|---|---:|
| Graph-hard | 0.417359 ± 0.106364 |
| CPTS | 0.469040 ± 0.035287 |
| SH75 | **0.482535 ± 0.041730** |

CPTS is +0.051681 over Graph-hard (2/3 wins), and −0.013495 against SH75 (0/3). This is a neutral-to-mixed result under the registered protocol; no selector rules were changed. No Citeseer test evaluation was run.

## Cora backbone generalization

| Backbone | Graph-hard mean MRR | CPTS mean MRR | CPTS − Graph-hard | Wins |
|---|---:|---:|---:|---:|
| GCN | 0.453804 | 0.537045 | +0.083242 | 2/3 |
| GraphSAGE | 0.337846 | 0.435671 | +0.097824 | 3/3 |
| GAT | 0.488195 | 0.541887 | +0.053692 | 2/3 |

CPTS improves the mean over Graph-hard on all three backbones. Results are validation-only.

## Novelty and paper claims

**Novelty status: EXACT_RULE_UNVERIFIED.** A focused search found adjacent approaches but no exact match for this complete rule. DMNS generates controllable hardness levels with conditional diffusion, while CPTS selects within a frozen candidate pool. ProGCL estimates true-negative probability in unsupervised graph contrastive learning with a mixture model. Adaptive hardness sampling also exists in collaborative filtering. These are important related works; the search does not establish priority, so do not claim “first.” See `09_NOVELTY.md` for sources and scope distinctions.

**Paper core innovation:** a training-only, per-positive BIC change-point selector that infers and suppresses an upper tail in a fixed teacher-scored candidate pool. Frame the contribution as a promising selector with validated gains over Graph-hard and generalization across Cora backbones; disclose the Cora held-out Matched-Q result and the PubMed/Citeseer baseline reversals.

**Next step:** freeze the V10 rule and artifacts. Before making a broad method claim, increase seed count or evaluate additional datasets under the same frozen protocol; do not tune the BIC rule to these results.
