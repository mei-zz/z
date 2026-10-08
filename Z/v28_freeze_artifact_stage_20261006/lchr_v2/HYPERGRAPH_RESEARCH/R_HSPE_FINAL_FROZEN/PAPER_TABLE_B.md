# Table B — V17.4 strong-backbone R-HSPE plug-in

Matched five seeds, fixed final epoch 10; within-seed paired initialization/sampler/order/RNG. Mean ± sample SD. This is the primary complementarity table; do not mix ranks with Table A.

| Dataset | Arm | MRR | Hits@10 | Hits@20 | Mean rank |
|---|---|---:|---:|---:|---:|
| Cora | NCN | 0.714230 ± 0.045021 | 0.938899 ± 0.035838 | 0.999241 ± 0.001697 | 2.831879 ± 0.613769 |
| Cora | NCN + R-HSPE | 0.731171 ± 0.040107 | 0.949526 ± 0.026855 | 0.999241 ± 0.001697 | 2.624288 ± 0.480561 |
| Cora | NCNC | 0.679237 ± 0.052239 | 0.897533 ± 0.048933 | 0.987097 ± 0.009620 | 3.537002 ± 0.841426 |
| Cora | NCNC + R-HSPE | 0.705090 ± 0.040646 | 0.909677 ± 0.041802 | 0.989374 ± 0.006920 | 3.259203 ± 0.736747 |
| Cora | NCNC + NULL75 | 0.677102 ± 0.053210 | 0.898672 ± 0.050251 | 0.987476 ± 0.009159 | 3.537381 ± 0.840637 |
| Pubmed | NCN | 0.900870 ± 0.015410 | 0.999458 ± 0.000202 | 1.000000 ± 0.000000 | 1.290523 ± 0.055319 |
| Pubmed | NCN + R-HSPE | 0.907232 ± 0.012258 | 0.999413 ± 0.000202 | 1.000000 ± 0.000000 | 1.270442 ± 0.041434 |
| Pubmed | NCNC | 0.898667 ± 0.015801 | 0.998917 ± 0.000294 | 1.000000 ± 0.000000 | 1.287906 ± 0.051694 |
| Pubmed | NCNC + R-HSPE | 0.905804 ± 0.013693 | 0.998962 ± 0.000342 | 1.000000 ± 0.000000 | 1.269856 ± 0.043340 |
| Pubmed | NCNC + NULL75 | 0.898600 ± 0.017778 | 0.998782 ± 0.000303 | 1.000000 ± 0.000000 | 1.289170 ± 0.054678 |

## Paired MRR effects

| Dataset | Contrast | Mean Δ | Median Δ | Wins |
|---|---|---:|---:|---:|
| Cora | NCNC+R-HSPE − NCNC | 0.025853 | 0.034156 | 5/5 |
| Cora | NCNC+R-HSPE − NULL75 | 0.027988 | 0.034329 | 5/5 |
| Cora | NCN+R-HSPE − NCN | 0.016942 | 0.018561 | 5/5 |
| Pubmed | NCNC+R-HSPE − NCNC | 0.007137 | 0.007611 | 5/5 |
| Pubmed | NCNC+R-HSPE − NULL75 | 0.007204 | 0.006713 | 5/5 |
| Pubmed | NCN+R-HSPE − NCN | 0.006362 | 0.007419 | 5/5 |

Both Cora and PubMed pass the paired-transfer and NULL75 gates. PubMed NCN plugin effect is modest (+0.001003 mean MRR). Citeseer transfer is NOT_SUPPORTED: validation delta −0.027379, 0/3; test not run.
