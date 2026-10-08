# Table A — V17.3 standalone/fair benchmark

V17.3 settings: NCN/NCNC 100 epochs, first best validation-MRR checkpoint; NSLR-HMANN 5000 epochs/final checkpoint; frozen R-HSPE/B0/control results reused. Mean ± sample SD. This table is not equal-compute and is not ranked against Table B.

| Dataset | Method | MRR | Hits@10 | Hits@20 | n |
|---|---|---:|---:|---:|---:|
| Cora | B0 frozen baseline | 0.465940 ± 0.129872 | 0.793548 ± 0.108669 | 0.979127 ± 0.031035 | 5 |
| Cora | R-HSPE standalone | 0.610054 ± 0.083963 | 0.910436 ± 0.030697 | 0.991651 ± 0.011113 | 5 |
| Cora | C1 count/parameter-matched | 0.624237 ± 0.085967 | 0.909677 ± 0.030140 | 0.991651 ± 0.011113 | 5 |
| Cora | NSLR-HMANN | 0.390938 ± 0.034778 | 0.752562 ± 0.039316 | 0.980645 ± 0.010514 | 5 |
| Cora | NCN, 100e/best validation | 0.848105 ± 0.006706 | 0.989374 ± 0.002164 | 1.000000 ± 0.000000 | 5 |
| Cora | NCNC, 100e/best validation | 0.843495 ± 0.006660 | 0.993169 ± 0.002164 | 1.000000 ± 0.000000 | 5 |
| Pubmed | B0 frozen baseline | 0.843116 ± 0.012572 | 0.992780 ± 0.000575 | 0.999865 ± 0.000202 | 5 |
| Pubmed | R-HSPE standalone | 0.856064 ± 0.021902 | 0.991110 ± 0.001552 | 0.999729 ± 0.000489 | 5 |
| Pubmed | C2 constant-set control | 0.857205 ± 0.025185 | 0.991200 ± 0.001162 | 0.999729 ± 0.000371 | 5 |
| Pubmed | NSLR-HMANN | 0.522645 ± 0.021630 | 0.877843 ± 0.061886 | 0.974007 ± 0.034520 | 5 |
| Pubmed | NCN, 100e/best validation | 0.930320 ± 0.001863 | 0.999143 ± 0.000189 | 1.000000 ± 0.000000 | 5 |
| Pubmed | NCNC, 100e/best validation | 0.937093 ± 0.001874 | 0.999278 ± 0.000189 | 1.000000 ± 0.000000 | 5 |
| Citeseer | B0 frozen baseline | 0.438572 ± 0.091925 | 0.729670 ± 0.085996 | 0.980220 ± 0.024768 | 3 |
| Citeseer | R-HSPE standalone | 0.527320 ± 0.071749 | 0.829304 ± 0.053940 | 0.993407 ± 0.004396 | 3 |
| Citeseer | NSLR-HMANN | 0.363857 ± 0.014862 | 0.705495 ± 0.021646 | 0.978901 ± 0.005938 | 5 |
| Citeseer | NCN, 100e/best validation | 0.869390 ± 0.007841 | 0.989890 ± 0.001204 | 1.000000 ± 0.000000 | 5 |
| Citeseer | NCNC, 100e/best validation | 0.885873 ± 0.004042 | 0.996484 ± 0.003333 | 1.000000 ± 0.000000 | 5 |

V17.3 is complete (45/45 jobs, zero failures). Citeseer frozen R-HSPE/B0 have n=3; third-party NCN/NCNC n=5. Candidate set uses 20 negatives/query.
