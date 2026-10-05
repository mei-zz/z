# Matched10-epoch transfer test main table

V17.3 rows use100 epochs; those results remain separately labeled reference anchors. Direct plug-in contrasts below are matched10-epoch final checkpoints, same seeds/splits/candidates. No ranking mixes5/10/100-epoch results.

| Dataset | Arm | MRR mean±SD | Hits@10 mean±SD | Hits@20 mean±SD | Mean rank mean±SD | Rank (matched arms) |
|---|---|---:|---:|---:|---:|---:|
| cora | NCN + R-HSPE | 0.731171 ± 0.040107 | 0.949526 ± 0.026855 | 0.999241 ± 0.001697 | 2.624288 ± 0.480561 | 1 |
| cora | NCN | 0.714230 ± 0.045021 | 0.938899 ± 0.035838 | 0.999241 ± 0.001697 | 2.831879 ± 0.613769 | 2 |
| cora | NCNC + R-HSPE | 0.705090 ± 0.040646 | 0.909677 ± 0.041802 | 0.989374 ± 0.006920 | 3.259203 ± 0.736747 | 3 |
| cora | NCNC | 0.679237 ± 0.052239 | 0.897533 ± 0.048933 | 0.987097 ± 0.009620 | 3.537002 ± 0.841426 | 4 |
| cora | NCNC + NULL75 | 0.677102 ± 0.053210 | 0.898672 ± 0.050251 | 0.987476 ± 0.009159 | 3.537381 ± 0.840637 | 5 |
| pubmed | NCN + R-HSPE | 0.907232 ± 0.012258 | 0.999413 ± 0.000202 | 1.000000 ± 0.000000 | 1.270442 ± 0.041434 | 1 |
| pubmed | NCNC + R-HSPE | 0.905804 ± 0.013693 | 0.998962 ± 0.000342 | 1.000000 ± 0.000000 | 1.269856 ± 0.043340 | 2 |
| pubmed | NCN | 0.900870 ± 0.015410 | 0.999458 ± 0.000202 | 1.000000 ± 0.000000 | 1.290523 ± 0.055319 | 3 |
| pubmed | NCNC | 0.898667 ± 0.015801 | 0.998917 ± 0.000294 | 1.000000 ± 0.000000 | 1.287906 ± 0.051694 | 4 |
| pubmed | NCNC + NULL75 | 0.898600 ± 0.017778 | 0.998782 ± 0.000303 | 1.000000 ± 0.000000 | 1.289170 ± 0.054678 | 5 |
