# Candidate A — SSHC

**Decision: REJECT.** The one permitted numerical initialization correction produced a smaller gain than the shuffled-cohesion control.

## Hypothesis and implementation

Structure-Supported Hyperedge Calibration preserves every raw global star hyperedge and calibrates its message using the z-scored off-center leaf density, `w_e = 1 + sigmoid(a) * tanh(z_e)`. The structural score is computed from the training/message graph only. The initialization is near identity. Controls replace cohesion with normalized size or a shuffled cohesion assignment.

## Cora standard, seed 0

| Arm | Description | Validation MRR | Runtime (s) |
|---|---|---:|---:|
| A0 | Graph baseline | 0.143932 | 9.86 |
| A1 | Raw global hypergraph | 0.162793 | 13.23 |
| A2 | Size calibration | 0.162515 | 14.17 |
| A3 | Shuffled cohesion | 0.163983 | 13.89 |
| A4, initial | True cohesion, `a=-5` | 0.164051 | 15.21 |
| A4, corrected | True cohesion, `a=-3` | 0.163446 | 14.93 |

Initial A4 exceeded the raw arm by 0.001258 (0.77%) and the shuffled control by only 0.000068, short of both the +0.003 and +2% thresholds. After the single allowed initialization correction, A4 exceeded raw by 0.000653 (0.40%) but trailed A3 by 0.000537. It therefore fails the required control comparison and is rejected. No test split was evaluated for these arms.

## Command and configuration

The common command was `python -m dcdlp.cli train --dataset cora --protocol standard --protocol-train uniform --seed 0 --ablation A5 --pretrain-epochs 1 --disentangle-epochs 0 --hidden-dim 16 --branch-dim 8 --num-layers 2 --dropout 0 --batch-size 4096 --device cuda --hypergraph-mode <mode> evaluate_test=false negatives_per_positive_eval=20`, with modes `raw`, `size_calibration`, `shuffled_cohesion`, and `sshc`. The corrected A4 run used `alpha_logit_init=-3`. Exact argv, configuration, and metrics are retained in `../remote_evidence/A_SSHC/`.

The six Cora runs took 81.30 seconds total. V2 test evaluation was disabled; the prior raw B1 test MRR (0.158069) is documented in the final report as a carried-forward baseline, not a new A result.

## Novelty and mechanism evidence

Novelty status is `NOVELTY_CONFLICT`: hyperedge weighting and within-hyperedge pairwise density are established directions ([hyperedge weighting](https://arxiv.org/abs/1410.6736), [hypergraph clustering coefficient](https://www.nature.com/articles/s41598-025-07869-8)). The corrected arm did not show a reliable cohesion-specific gain; no broader novelty claim is supported.
