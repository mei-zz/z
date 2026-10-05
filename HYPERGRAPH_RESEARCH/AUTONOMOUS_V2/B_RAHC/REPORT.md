# Candidate B — RAHC

**Decision: REJECT.** The true overlap calibration failed against both registered controls.

## Hypothesis and implementation

Redundancy-Aware Hyperedge Calibration keeps the full incidence set and attenuates each raw star-hyperedge message using the z-scored mean of its top-three shared-node Jaccard overlaps: `w_e = 1 - beta * tanh(r_e)`, with `0 <= beta <= 0.5` and a near-identity initialization. Controls are size calibration and shuffled redundancy.

## Cora standard, seed 0

| Arm | Description | Validation MRR | Runtime (s) |
|---|---|---:|---:|
| B1 | Raw global hypergraph | 0.162793 | 13.38 |
| B2 | Size calibration | 0.163352 | 16.49 |
| B3 | Shuffled redundancy | 0.166308 | 14.54 |
| B4 | True redundancy | 0.162889 | 15.79 |

B4 is only +0.000096 (+0.06%) over raw, and is below B2 by 0.000463 and B3 by 0.003419. This fails the control comparison and both effect-size thresholds. The best arm is a shuffled control and is not a candidate win. No test split was evaluated.

## Command and configuration

The common command was `python -m dcdlp.cli train --dataset cora --protocol standard --protocol-train uniform --seed 0 --ablation A5 --pretrain-epochs 1 --disentangle-epochs 0 --hidden-dim 16 --branch-dim 8 --num-layers 2 --dropout 0 --batch-size 4096 --device cuda --hypergraph-mode <mode> evaluate_test=false negatives_per_positive_eval=20`, with modes `raw`, `size_calibration`, `shuffled_redundancy`, and `redundancy_calibration`; `top_m=3`. Exact argv, configuration, and metrics are retained in `../remote_evidence/B_RAHC/`.

The four Cora runs took 60.20 seconds total. Test evaluation was disabled.

## Novelty and mechanism evidence

Novelty status is `NOVELTY_CONFLICT`: overlap-weighted hyperedge line graphs, redundancy pruning, and degree-based message calibration are established ([DDEC](https://www.mdpi.com/1099-4300/28/7/729), [IJCAI hypergraph structure learning](https://www.ijcai.org/proceedings/2022/0267), [TF-MP](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ad9804eed175610302917a0c21ab9b52-Abstract-Conference.html)). The shuffled-control ranking argues against claiming a real-overlap-specific signal here.
