# V12 Blacklist

| Method / family | Disposition | Failure evidence / reason |
|---|---|---|
| PCHR | BLACKLISTED | Prior V3/V4 task history says REJECT; no separate metric file found. Candidate-conditioned hyperedge/routing family has direct LCHR failure; no PCHR metrics are invented. |
| LCHR | BLACKLISTED | Validation 0.131696 < parameter-matched global router 0.131830, random Top-K 0.132367, and global hypergraph 0.162793. |
| SSHC | BLACKLISTED | Corrected true-cohesion arm lost to shuffled-cohesion control and missed effect-size gate. |
| RAHC | BLACKLISTED | True redundancy lost to size and shuffled controls. |
| HSA | BLACKLISTED | Best true arm did not reach minimum effect-size gate. |
| ARHC | BLACKLISTED | Role-aware propagation did not beat Raw-HG in 5-epoch screen. |
| PMHE | BLACKLISTED | Pair-moment arm lost to simpler mean / second-moment controls; subthreshold gain. |
| ARPM | BLACKLISTED | Anchor-conditioned pair moment lost to Raw, PMHE and anchor-mean controls. |
| ECPH | BLACKLISTED | +0.000497 MRR / +0.102%, below gate; increased runtime. |
| ECNH | BLACKLISTED | −0.000115 MRR against Raw-HG. |
| OWH | BLACKLISTED | −0.002255 MRR and 5.2x hyperedges / +139% runtime. |
| GHHR | BLACKLISTED | Below Raw-HG and the uniform / shuffled controls. |
| CVHNM | BLACKLISTED | Lost to Graph-hard-only control. |
| DAF | BLACKLISTED | −0.006109 MRR against Raw-HG. |
| False-negative HG veto mechanism | BLACKLISTED | Validation performance did not establish mechanism; on test true veto lost to shuffled veto by 0.012178 MRR. |
| CODNS | BLACKLISTED | Graph-hardness-matched disagreement controls were negative or subthreshold. |
| AQTHS | BLACKLISTED | Validation gate failed; test was not run. |
| RTHNL under K=1 | BLACKLISTED | Mathematically degenerates to Graph-hard because one negative per positive leaves no within-row reordering. |
| CPTS true-tail / change-point detector | BLACKLISTED | Detected tails in all real and null rows; local adaptivity mechanism not supported. |
| Per-positive CPTS adaptivity claim | BLACKLISTED | CPTS did not beat shuffled / Matched-Q controls consistently; retain only empirical performance as historical. |
| Fixed percentile trimming | BLACKLISTED | QTHS25 remains a strong baseline, but ordinary threshold changes are hyperparameter search without an independent mechanism claim. |
| SH75 window tweaks | BLACKLISTED | SH75 is a strong empirical control; moving fixed window boundaries is parameter tuning, not a mechanism. |
| V12-F1 global batch-top-10 standalone ranking loss | BLACKLISTED | Under matched QTHS25 training negatives, Stage 2 MRR 0.235394 vs QTHS25+BCE 0.530263 and random-ten pairwise control 0.385148. Do not repeat unchanged. |
| V12-D1 one-hop target-masked ego-context residual | BLACKLISTED | Under matched QTHS25 training negatives, Stage 2 MRR 0.365654 vs 0.530263 baseline and 0.521947 node-permuted-context control. Do not repeat unchanged. |
| V12-F2 BCE-anchored batch-hard ranking residual | BLACKLISTED | Stage 1B MRR 0.523925 vs QTHS25+BCE 0.525620; random-ten pairwise control 0.515801. It failed the required improvement gate. |
| V12-H1 train-edge-dropout pair-score consistency | BLACKLISTED | Stage 1B MRR 0.523719 vs baseline 0.525620 and shuffled-pair consistency control 0.525116. It failed the required improvement gate. |
| V12-X1 orthogonalized Raw-HG pair-representation residual | BLACKLISTED | Stage 1C MRR 0.523703 vs QTHS25+BCE 0.525620 and raw-feature MLP control 0.527652. The orthogonal residual did not isolate a helpful component. |
| V12-G2 persistent positive-difficulty weighting | BLACKLISTED | Stage 1D MRR 0.525049 vs QTHS25+BCE 0.525620 and shuffled-history control 0.525135; instantaneous-difficulty control matched the candidate. No persistent-history mechanism signal. |
| V12-X2 aligned Graph/Raw-HG bilinear residual | BLACKLISTED | Stage 1E candidate MRR 0.527739 (+0.002119) vs QTHS25+BCE 0.525620; the parameter-matched self-moment control scored 0.527742. The effect missed the gate and the proposed cross-view product had no measurable advantage over self moments. |
| V12-B2 residual-structural branch coactivation | BLACKLISTED | Stage 1F candidate MRR 0.526513 (+0.000892) vs QTHS25+BCE 0.525620; the same-parameter degree/CN branch-calibration control scored 0.527789 (+0.002169). The bilinear interactions failed both the effect and control gates. Keep the calibration control as an unconfirmed diagnostic only. |
| Hyperparameter-only changes | BLACKLISTED | Learning rate, dropout, dimension, weight decay, batch size, epochs, seed, negative count, activation, generic normalization or residual changes are not innovations. |
| PCHR exact numeric diagnosis | NOT RECOVERED | Explicitly blacklisted by prior task; no separate PCHR result artifact found. Do not infer or recreate its metric. |
