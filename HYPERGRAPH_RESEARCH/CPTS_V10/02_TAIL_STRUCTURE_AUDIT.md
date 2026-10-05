# Tail structure audit

All calculations use frozen, train-only graph-teacher scores. No validation/test arrays enter CPTS selection or BIC fitting.

## BIC rule

M*ln(SSE1/M) + 2*ln(M); Gaussian mean and shared variance

M*ln(SSE2/M) + 4*ln(M); two segment means, shared variance, and discrete breakpoint

if min BIC2 < BIC1, remove upper tail h_(b+1)...h_(M) and select h_(b); else select h_(M)

## Dataset summaries

| Dataset | Positives | Tail present | Mean tail | Median | p90 | Modal tail share | 3 sizes >10% | >80% same size | Adaptive gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| cora | 4488 | 1.0000 | 6.8258 | 7.0 | 11.0 | 0.1905 | 5 | False | True |
| pubmed | 37676 | 1.0000 | 5.7528 | 6.0 | 9.0 | 0.1406 | 5 | False | True |
| citeseer | 3870 | 1.0000 | 7.4323 | 7.0 | 10.0 | 0.1752 | 4 | False | True |

## Cora tail-size counts

| Tail size | Count | Fraction |
|---:|---:|---:|
| 0 | 0 | 0.000000 |
| 1 | 0 | 0.000000 |
| 2 | 855 | 0.190508 |
| 3 | 139 | 0.030971 |
| 4 | 250 | 0.055704 |
| 5 | 328 | 0.073084 |
| 6 | 472 | 0.105169 |
| 7 | 472 | 0.105169 |
| 8 | 493 | 0.109848 |
| 9 | 459 | 0.102273 |
| 10 | 364 | 0.081105 |
| 11 | 259 | 0.057709 |
| 12 | 180 | 0.040107 |
| 13 | 109 | 0.024287 |
| 14 | 61 | 0.013592 |
| 15 | 28 | 0.006239 |
| 16 | 9 | 0.002005 |
| 17 | 8 | 0.001783 |
| 18 | 2 | 0.000446 |
| 19 | 0 | 0.000000 |
| 20 | 0 | 0.000000 |

## Cora cached selection overlap

| Seed | CPTS = Graph-hard | CPTS = QTHS25 | CPTS = SH75 |
|---:|---:|---:|---:|
| 0 | 0.0000 | 0.0000 | 0.0457 |
| 1 | 0.0000 | 0.0000 | 0.0423 |
| 2 | 0.0000 | 0.0000 | 0.0468 |

## Cora selected hardness

Rank 1 is hardest; rank 20 is easiest. Percentile is 100 at the hardest candidate and 0 at the easiest.

| Selector | Mean rank | Median rank | Mean teacher score | Mean score percentile | Mean gap to hardest |
|---|---:|---:|---:|---:|---:|
| CPTS | 7.826 | 8.0 | -0.051370 | 64.07 | 0.209977 |
| GRAPH_HARD | 1.000 | 1.0 | 0.158607 | 100.00 | 0.000000 |
| QTHS25 | 1.500 | 1.5 | 0.090044 | 97.37 | 0.068563 |
| SH75 | 12.992 | 13.0 | -0.084991 | 36.88 | 0.243598 |

## Gate

Cora fixed-quantile collapse: **False**. Adaptive structure confirmed: **True**.
Training remains disabled until this gate is evaluated. See `figures/tail_size_distribution.png` and `figures/representative_score_profiles.png`.
