# Candidate C — HSA

**Decision: REJECT.** The best true-support arm beats every control, but misses both registered effect-size thresholds.

## Hypothesis and implementation

Hyperedge Support Alignment leaves raw global propagation unchanged and adds a small auxiliary scorer for sampled non-center leaf pairs. Positives are train/message-graph edges; negatives are non-edges. Center-leaf pairs are excluded, and validation/test edges do not provide supervision. Each star samples up to four examples per class. The shuffled-label control retains the same scorer and loss weight.

## Corrected Cora standard, seed 0 results

| Arm | Description | Validation MRR | Runtime (s) |
|---|---|---:|---:|
| C0 | Raw hypergraph | 0.162793 | 12.53 |
| C1 | Same-size auxiliary MLP, `lambda=0` | 0.162793 | 15.78 |
| C2 | Shuffled labels, `lambda=0.05` | 0.162891 | 16.59 |
| C2 | Shuffled labels, `lambda=0.10` | 0.163453 | 15.55 |
| C3 | True support, `lambda=0.05` | **0.164475** | 15.80 |
| C3 | True support, `lambda=0.10` | 0.162377 | 15.49 |

The C1 initialization-matched check is exact: C0 and C1 validation MRR are both 0.16279348007164107. The best true arm gains +0.001681 (+1.03%) over C0 and exceeds the strongest shuffled control by +0.001022, but it does not reach +0.003 or +2%. Therefore it is rejected and no three-seed confirmation is triggered. The true `lambda=0.10` arm is below raw. The six Cora runs took 91.73 seconds total.

Across each auxiliary training run, 4,398 leaf-pair examples were sampled over three batches (mean 1,466 per batch). The best true arm's mean unweighted auxiliary BCE was 0.6906. This confirms that the auxiliary path executed, but does not establish a downstream effect large enough to pass the registered rule.

## Initialization correction and test status

The first remote C batch was discarded because constructing the auxiliary MLP before the baseline decoder consumed RNG and changed the raw model's initialization. The MLP was moved after the base model layers; local checks then confirmed matching common parameters and identical raw/C1 output, and the corrected C0–C3 batch above was rerun. Exact corrected configs and metrics are in `../remote_evidence/C_HSA/`.

All V2 arms set `evaluate_test=false`. Since no candidate passed, Stage 2 and test evaluation were not run. The prior raw B1 test MRR of 0.158069 from the LCHR report is only a carried-forward baseline, not a C result.

## Command and novelty

The common command was `python -m dcdlp.cli train --dataset cora --protocol standard --protocol-train uniform --seed 0 --ablation A5 --pretrain-epochs 1 --disentangle-epochs 0 --hidden-dim 16 --branch-dim 8 --num-layers 2 --dropout 0 --batch-size 4096 --device cuda --hypergraph-mode <raw|hsa|hsa_shuffled> lambda_aux=<0|0.05|0.10> evaluate_test=false negatives_per_positive_eval=20`. Exact argv, config, and metrics are retained in `../remote_evidence/C_HSA/`.

Novelty status is `NOVELTY_CONFLICT`: sub-hyperedge self-supervision and incidence reconstruction are established ([S3Hyper](https://ojs.aaai.org/index.php/AAAI/article/view/39471), [DualCL](https://link.springer.com/article/10.1007/s44443-026-01156-w)); HSA's fixed-star leaf-edge supervision remains a narrow distinction, not a verified novelty claim.
