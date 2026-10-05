# Best state — V13 experiments

- Current status: all experiment families summarized here are complete; no Innovation 1 or Innovation 2 is confirmed.
- ECR: passed Cora single-seed screening, Stage 2, 3-seed local confirmation, and one-time Cora test. It failed the registered PubMed matched-control generalization gate: mean ECR MRR 0.8417468452 vs 0.8421304397 for shuffled evidence (margin −0.0003835945). It remains a Cora-local candidate, not a confirmed innovation.
- T1 Persistent Hardness Selection: all 7 Cora seed-0 Stage 1 arms completed; T1 MRR 0.3362255062 vs QTHS25 0.5256204672, trajectory shuffled 0.4923756435, and final-rank-matched 0.4848878243. Decision STAGE1_REJECT.
- L1 Setwise Rank Calibration: all 5 Cora seed-0 Stage 1 jobs completed; L1 MRR 0.3457115803 vs QTHS25 0.5256204672, independent BCE 0.4870842144, random listwise 0.5032648386, and repeated BCE 0.4844376842. Independent audit passed; scientific decision STAGE1_REJECT.
- No P1 training run or P1 metric is recorded.
- Full metric tables and protocol details: INNOVATION_RESULTS_SUMMARY.md.
