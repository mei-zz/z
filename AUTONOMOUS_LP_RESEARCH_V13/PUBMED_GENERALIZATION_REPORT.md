# PubMed generalization result — V13 ECR

**Decision:** GENERALIZATION_REJECT  
**Protocol:** PubMed, seeds 0/1/2, 10 epochs, Raw-HG DCDLP + QTHS25 + BCE. Each seed used matched split, training candidate pool, validation candidates, and selected negatives for baseline, ECR, and shuffled-evidence control. Test evaluation was disabled. All 9 jobs completed.

## Paired validation MRR

| Seed | Baseline | ECR | Shuffled evidence | ECR − baseline | ECR − shuffled |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.8472040922 | 0.8595802312 | 0.8452447234 | +0.0123761390 | +0.0143355078 |
| 1 | 0.8231326007 | 0.8423909495 | 0.8314169789 | +0.0192583488 | +0.0109739706 |
| 2 | 0.8467487761 | 0.8232693549 | 0.8497296168 | −0.0234794212 | −0.0264602619 |
| **Mean** | **0.8390284897** | **0.8417468452** | **0.8421304397** | **+0.0027183555** | **−0.0003835945** |

ECR beat baseline and shuffled control in 2/3 seeds. It met the positive mean-gain requirement against baseline but missed the required positive mean margin against the matched control by 0.0003835945. Therefore ECR did not pass the cross-dataset gate and is not confirmed as Innovation 1.

T1 and L1 have since completed their Phase B Stage 1 comparisons; both were rejected. No next experiment is selected. The complete cross-family summary is in INNOVATION_RESULTS_SUMMARY.md.

Archive SHA-256: 91494ee85c8b9f4f58fc31681a78c3cf5f7bac86d4604ab32c45add75353ffd4  
Driver SHA-256: ee5a913bb75d738300ae9c5a22931d792d38c49d677e0fad6ea834937c85aedb
