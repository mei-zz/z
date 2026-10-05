# V13 preliminary novelty screen: ECR

Screen date: 2026-10-02 (local); primary-source search performed before Stage 2. This is a collision screen, not a systematic review or proof of priority.

## Candidate in scope

Evidence-Calibrated Residual (ECR) adds a zero-initialized, 28-parameter residual to the base Raw-HG DCDLP score. It combines a 24-dimensional pair-specific Raw-HG feature vector, separately standardized degree/CN scalars, target-masked cross-exclusive-neighborhood density, and one Raw-HG × structure interaction. The key empirical control is the same-parameter residual with evidence rows shuffled across pairs. The current Phase-A result is only a single-seed, five-epoch Cora screen.

## Closest primary literature checked

| Work | Primary source | Overlap | Difference / current collision judgment |
|---|---|---|---|
| HL-GNN, Zhang et al., KDD 2024 | [arXiv paper](https://arxiv.org/abs/2406.07979) | Learns graph link-prediction heuristics using a small number of parameters and combines local/global structural evidence. | Strong conceptual overlap in parameter-efficient learned structural heuristics. Its propagation/matrix formulation is not this post-score, pair-calibrated residual and does not use the ECR evidence set or shuffled-pair test. Not an exact algorithmic collision from the source reviewed. |
| SEAL, Zhang & Chen, NeurIPS 2018 | [NeurIPS proceedings paper](https://proceedings.neurips.cc/paper_files/paper/2018/hash/53f0d7c537d99b3824f0f99d62ea2428-Abstract.html) | Learns link heuristics from pair-enclosing subgraphs and structural labels. | Strong overlap at the broad level of learning pair-specific structural evidence. ECR uses a fixed hypergraph predictor plus a small additive evidence correction rather than an enclosing-subgraph classifier. |
| Neo-GNNs, Yun et al., NeurIPS 2021 | [NeurIPS proceedings paper](https://proceedings.neurips.cc/paper/2021/hash/71ddb91e8fa0541e426a54e538075a5a-Abstract.html) | Injects neighborhood-overlap and other structural heuristics into neural link prediction. | Close conceptual overlap in combining learned representations and explicit structural evidence. The reviewed method modifies neural aggregation/scoring through its Neo-GNN construction; it does not match the ECR multi-channel zero-start residual and pair-shuffle mechanism test. |
| NCN / NCNC, Wang et al., ICLR 2024 | [ICLR proceedings paper](https://proceedings.iclr.cc/paper_files/paper/2024/hash/3efb4bdc6bfe13e1ff95b4407c37961d-Abstract-Conference.html) | Uses structural common-neighbor information and link prediction to complete neighborhood structure; structural evidence enters prediction. | Broad overlap in topology-aware link scoring and explicit structural evidence. The method centers on neighborhood completion / structural feature aggregation, rather than ECR's low-capacity post-logit calibration. |
| BUDDY / ELPH, Chamberlain et al. | [arXiv paper](https://arxiv.org/abs/2209.15486) | Pair-level link representations use structural counts/sketches to scale subgraph link prediction. | Related in pair-specific structural evidence; different objective and structural representation. |
| HMANN / NSLR-HMANN, Chai et al., Pattern Recognition 2024 | [publisher paper](https://doi.org/10.1016/j.patcog.2024.110292) | Hypergraph model for link prediction with node- and hyperedge-level views. | Relevant hypergraph LP background. It fuses views in the representation learner, not as the ECR post-score residual. |

## Assessment

The general premise—learned graph/structural heuristics can improve neural link prediction—is established and must not be presented as novel. The narrower combination checked here (pair-specific Raw-HG evidence + standardized degree/CN + target-masked cross-neighborhood density, composed as a zero-initialized low-capacity residual with aligned-vs-shuffled evidence control) did not yield an exact match in the primary sources above. That is a limited negative search result. It does not support “first” or “novel” claims; a broader search for score calibration, residual adapters, heuristic fusion, and hypergraph link prediction is required if ECR reaches Stage 2/3.

## Decision

Preliminary collision screen: `RELATED_WORK_PRESENT; NO_EXACT_MATCH_FOUND_IN_SCREENED_SOURCES; NOVELTY_NOT_ESTABLISHED`. Stage 2 may proceed as validation of the registered candidate. Novelty status remains provisional until the broader review.

## Phase 2 pre-screen: Persistent Hardness Trajectory (T1)

Screen date: 2026-10-02 local. This was a preliminary pre-screen; no novelty claim was made. T1 has since completed its registered Stage 1 and was rejected.

### Closest primary literature checked

| Work | Primary source | Overlap | Difference / current collision judgment |
|---|---|---|---|
| MeBNS, Wang et al. (2023) | [arXiv preprint](https://arxiv.org/abs/2312.04815) | Directly studies easy/hard negative migration and uses a teacher-student design with meta-learned negative reweighting for link prediction. | Strong overlap in training-dynamics-aware negative selection. T1 instead ranks each fixed candidate at teacher epochs 1–10 and selects one candidate by its worst (minimum) hardness percentile across the trajectory. The reviewed abstract does not establish an exact match, but full method-level comparison remains necessary. |
| HeaRT, Li et al. (2023) | [arXiv preprint](https://arxiv.org/abs/2306.10453) | Establishes heuristic-related hard negatives as a more realistic link-prediction evaluation protocol. | Relevant hard-negative benchmark context; its reviewed description is a heuristic-based fixed evaluation sampler, not temporal persistence of the same training candidate across checkpoints. |
| Enhanced Negative Sampling for dynamic graphs (Gao et al., 2024) | [Neural Networks article](https://doi.org/10.1016/j.neunet.2024.106175) | Schedules negative difficulty during temporal graph training. | Conceptual overlap in varying hardness over training. The reported method targets temporal graphs and historical/temporal proximity; it does not appear to use maximin rank persistence for a fixed static candidate pool. |

### Assessment and experiment implication

Training-dynamics-aware hard-negative selection is established, so T1 cannot be described as the first dynamic or trajectory-aware negative sampler. The Cora Stage 1 result failed both its gain and mechanism gates: T1 MRR 0.3362255062 versus QTHS25 0.5256204672, trajectory-shuffled 0.4923756435, and final-rank-matched 0.4848878243. The candidate is rejected; no broader novelty claim is warranted.

For the next-family objective fallback, generic listwise ranking is also established: [Expected Reciprocal Rank for Graded Relevance](https://research.google/pubs/expected-reciprocal-rank-for-graded-relevance/), [Listwise Learning to Rank Based on Approximate Rank Indicators](https://ojs.aaai.org/index.php/AAAI/article/view/20826), and [PiRank](https://arxiv.org/abs/2012.06731). A generic expected-rank loss alone would therefore be weak novelty; any L-family candidate must be justified by the fixed one-positive/20-negative link-candidate protocol and beat compute-matched controls.

L1 Setwise Rank Calibration was subsequently completed and rejected. Its Cora Stage 1 comparison is summarized in the final status update below.

Final decisions: ECR_GENERALIZATION_REJECT; T1_STAGE1_REJECT; L1_STAGE1_REJECT. No innovation is confirmed; no next experiment is selected.




## Final status update — 2026-10-03

This update supersedes the earlier “L1 pending/running” statements in this ledger. L1 completed all five registered Cora seed-0 jobs and was rejected: MRR 0.34571158 versus 0.52562047 QTHS25 and below independent BCE (0.48708421), random listwise (0.50326484), and repeated BCE (0.48443768). Its standalone integrity audit passed; the raw infrastructure-failure label came from a summarizer key mismatch.

ECR passed local Cora confirmation but failed PubMed's positive-mean-margin requirement against the shuffled-evidence control (mean margin −0.00038359); novelty and generalization are not established. T1 and L1 are rejected. There is no confirmed Innovation 1 or Innovation 2, and no P1 training result.

