# 04 — quick experiments

## Execution environment and traceability

- Local interpreter: `D:\anaconda\envs\Z\python.exe`, Python 3.10.20, PyTorch 2.0.0+cpu; CUDA unavailable.
- Source state: `git_commit=untracked`; the workspace has no Git metadata.
- `D:\DCDLP_DATA` is a junction to the existing workspace data directory `results/regime_gradient_audit_v1/data`; `D:\DCDLP_OUTPUT` is a junction to `HYPERGRAPH_RESEARCH/results`. The ASCII aliases were necessary because the installed Windows PyTorch writer failed on nested paths containing the Chinese workspace name. The target artifacts remain inside this workspace.
- Fixed model configuration: dataset-specific standard split, seed 0, `ablation=A5`, uniform training negatives, one pretraining epoch, zero disentanglement epochs, hidden 16, branch 8, 2 GCN layers, dropout 0, batch 4096 for Cora / 256 for smoke, CPU, 20 generated negatives per Cora positive / 10 per smoke positive.
- Selection: best validation MRR at epoch 0. Test metrics were not used to select any mode.

Representative command (mode substituted for each B0–B4):

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONPATH='src'
& 'D:\anaconda\envs\Z\python.exe' -m dcdlp.cli train `
  --dataset cora --data-root 'D:\DCDLP_DATA' --protocol standard `
  --protocol-train uniform --seed 0 --ablation A5 `
  --pretrain-epochs 1 --disentangle-epochs 0 --hidden-dim 16 `
  --branch-dim 8 --num-layers 2 --dropout 0 --batch-size 4096 `
  --device cpu --output-dir 'D:\DCDLP_OUTPUT\cora2_B1_raw' `
  --hypergraph-mode raw negatives_per_positive_eval=20
```

## Cora standard, seed 0

| ID | Mode | Validation MRR | Test MRR | Validation AUC | Test AUC | Validation AP | Test AP | Validation Hits@10 | Test Hits@10 | Train sec | Params |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B0 | disabled | 0.143932 | 0.136209 | 0.331071 | 0.338874 | 0.038426 | 0.036869 | 0.262357 | 0.288425 | 7.529 | 24,478 |
| B1 | raw | 0.164542 | 0.157838 | 0.415067 | 0.407205 | 0.043853 | 0.042603 | 0.403042 | 0.373814 | 15.565 | 24,734 |
| B2 | complement | 0.138576 | 0.123553 | 0.311225 | 0.311942 | 0.036228 | 0.035450 | 0.250951 | 0.284630 | 16.104 | 24,734 |
| B3 | shuffled | 0.127815 | 0.128608 | 0.365386 | 0.347407 | 0.036623 | 0.034976 | 0.346008 | 0.301708 | 16.319 | 24,734 |
| B4 | pairwise | 0.147698 | 0.146744 | 0.392640 | 0.382316 | 0.041432 | 0.039831 | 0.376426 | 0.349146 | 15.591 | 24,734 |

Artifacts are the JSON, checkpoint and prediction files below `HYPERGRAPH_RESEARCH/results/cora2_B*`.

## Built-in smoke, seed 0

The smoke graph has only 4 validation and 9 test positives, so these values are shape/contract evidence, not model evidence.

| Mode | Validation MRR | Test MRR | Validation AUC | Test AUC | Train sec | Params |
|---|---:|---:|---:|---:|---:|---:|
| disabled | 0.441964 | 0.171344 | 0.625000 | 0.446914 | 0.274 | 1,806 |
| raw | 0.269048 | 0.186468 | 0.525000 | 0.448148 | 0.326 | 2,062 |
| complement | 0.431250 | 0.172270 | 0.593750 | 0.474074 | 0.295 | 2,062 |
| shuffled | 0.264583 | 0.162394 | 0.518750 | 0.428395 | 0.701 | 2,062 |
| pairwise | 0.271825 | 0.181445 | 0.518750 | 0.449383 | 0.320 | 2,062 |

## Interpretation

The raw branch has a positive one-seed Cora signal (+0.020610 validation MRR versus B0), but the pairwise-equivalent control also improves (+0.003766), and the proposed complement is worse than B0 (-0.005356). The raw branch therefore does not establish an independent PCHR gain. No three-seed or LPShift run was authorized after this mechanism falsifier.

