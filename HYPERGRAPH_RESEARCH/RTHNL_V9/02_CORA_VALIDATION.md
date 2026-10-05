# Cora validation gate

The registered rule requires RTHNL to beat Graph-hard and both Shuffled-RTHNL and Score-SoftWeight. The singleton identity proves that RTHNL is the same training objective as Graph-hard and Shuffled-RTHNL in float32. The V8 fixed-epoch-10 Graph-hard validation scores are reused under this exact identity; no RTHNL training job was necessary.

| Seed | Graph-hard | RTHNL implied by identity | Shuffled-RTHNL implied | RTHNL − Graph-hard | RTHNL − Shuffled |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.532759 | 0.532759 | 0.532759 | 0.000000 | 0.000000 |
| 1 | 0.328583 | 0.328583 | 0.328583 | 0.000000 | 0.000000 |
| 2 | 0.500069 | 0.500069 | 0.500069 | 0.000000 | 0.000000 |
| Mean | 0.453804 | 0.453804 | 0.453804 | 0.000000 | 0.000000 |

Gate 1 fails: RTHNL beats Graph-hard in 0/3 seeds and the mean gain is 0, below +0.002. Gate 2 also fails by identity: RTHNL cannot beat its within-positive shuffled control in any seed. Decision: **RTHNL_REJECT; MECHANISM_UNSUPPORTED**. Later comparison jobs are stopped at this validation gate.

For context, the V8 fixed-epoch-10 SH75 validation MRRs were 0.494523, 0.552162, and 0.556404 (mean 0.534363). RTHNL implied by identity is lower by 0.080559 on average and wins 1/3 seeds. This exceeds the registered 0.005 material-dominance margin; **SH75_DOMINATES**. V8 QTHS25 validation mean was 0.474662, also above the RTHNL implied mean by 0.020858.

These are gate calculations from cached V8 Graph-hard results and algebraic identity, not independently trained RTHNL measurements. V9 test was not opened.
