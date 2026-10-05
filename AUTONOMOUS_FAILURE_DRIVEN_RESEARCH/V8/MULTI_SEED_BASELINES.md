# V8 Multi-Seed Baselines

## Locked protocol

Two already-generated LPShift datasets were frozen before model training:

- A: `ogbl-collab_CN_2_1_0_seed1` (`valid=1, test=2, inverse`)
- B: `ogbl-collab_CN_4_2_0_seed1` (`valid=2, test=4, inverse`)

Only the model seed changed: `1, 2, 3`. Validation MRR was the only selection quantity for DCDLP. Test metrics were computed after the checkpoint was selected and were not used for structure, hyperparameter, or subgroup decisions.

## Model configurations

| Model | Parameters | Training setting | Important protocol notes |
|---|---:|---|---|
| Official GCN | 83,201 | official 3-layer GCN + 3-layer MLP scorer, hidden 128, lr `1e-2`, 100 epochs | original LPShift runner; no DCDLP target-mask path |
| DCDLP Parent | 28,966 | existing GCN backbone, hidden 64, branch 32, 2 layers, lr `1e-3`, 4 epochs | message-graph-only negatives; current target batch masked |
| CN / AA / RA / PA | fixed | deterministic message-graph heuristics | computed once per setting; no seed variance |

The comparison is valid as a benchmark audit, but it is not a perfectly compute-matched claim: the official GCN uses its original 100-epoch training schedule while DCDLP uses the locked four-epoch V8 setting. This difference is reported rather than tuned away.

DCDLP formal runs recorded approximately 3.58–3.63 GB peak GPU memory and 28,966 parameters. The official GCN source runner did not instrument CUDA peak memory; the V7 seed-1 observation was approximately 10.85 GB, while V8 seed-2/3 logs provide CPU RSS only. No GPU value is invented for those runs.

## Setting A per-seed results

Values are `validation MRR / Hits@10 / Hits@20 / Hits@50 / Hits@100` and then the corresponding frozen-test values.

### DCDLP Parent

| Seed | Validation | Test |
|---:|---|---|
| 1 | `0.525546 / 0.751785 / 0.831383 / 0.921458 / 0.974143` | `0.240739 / 0.596706 / 0.724801 / 0.867706 / 0.956676` |
| 2 | `0.519806 / 0.750264 / 0.833326 / 0.923275 / 0.974228` | `0.227772 / 0.576481 / 0.725575 / 0.874558 / 0.960544` |
| 3 | `0.525830 / 0.750475 / 0.835566 / 0.926064 / 0.975411` | `0.237234 / 0.581012 / 0.723475 / 0.870579 / 0.958444` |
| Mean ± SD | `0.523727 ± 0.003399` MRR | `0.235248 ± 0.006708` MRR |

Hits means ± SD: validation `0.750841±0.000824 / 0.833425±0.002093 / 0.923599±0.002320 / 0.974594±0.000709`; test `0.584733±0.010614 / 0.724617±0.001062 / 0.870948±0.003440 / 0.958554±0.001936`.

### Official GCN

| Seed | Validation | Test |
|---:|---|---|
| 1 | `0.071200 / 0.155300 / 0.262800 / 0.503800 / 0.780200` | `0.057800 / 0.124300 / 0.242300 / 0.464600 / 0.744900` |
| 2 | `0.070000 / 0.150700 / 0.258300 / 0.491400 / 0.771100` | `0.054400 / 0.121700 / 0.217400 / 0.440800 / 0.722600` |
| 3 | `0.071100 / 0.152000 / 0.261600 / 0.494900 / 0.773000` | `0.052400 / 0.127500 / 0.224800 / 0.453600 / 0.727500` |
| Mean ± SD | `0.070767 ± 0.000666` MRR | `0.054867 ± 0.002730` MRR |

### Setting-A fixed heuristics

| Heuristic | Validation MRR | Test MRR |
|---|---:|---:|
| CN | `0.3845` | `0.0079` |
| AA | `0.4026` | `0.0079` |
| RA | `0.4057` | `0.0079` |
| PA | `0.0391` | `0.0399` |

## Setting B per-seed results

### DCDLP Parent

| Seed | Validation | Test |
|---:|---|---|
| 1 | `0.879472 / 0.968793 / 0.979998 / 0.991285 / 0.997178` | `0.486710 / 0.728855 / 0.815254 / 0.916371 / 0.972470` |
| 2 | `0.870965 / 0.938208 / 0.952982 / 0.978213 / 0.994564` | `0.377999 / 0.514414 / 0.636482 / 0.831789 / 0.950394` |
| 3 | `0.871458 / 0.937005 / 0.953604 / 0.981076 / 0.996307` | `0.370601 / 0.504026 / 0.634231 / 0.856982 / 0.976452` |
| Mean ± SD | `0.873965 ± 0.004775` MRR | `0.411770 ± 0.065005` MRR |

Hits means ± SD: validation `0.948002±0.018016 / 0.962194±0.015421 / 0.983525±0.006871 / 0.996016±0.001331`; test `0.582432±0.126912 / 0.695322±0.103870 / 0.868381±0.043427 / 0.966439±0.014037`.

### Official GCN

| Seed | Validation | Test |
|---:|---|---|
| 1 | `0.117300 / 0.245700 / 0.370400 / 0.612000 / 0.860900` | `0.057900 / 0.121300 / 0.216200 / 0.452200 / 0.757400` |
| 2 | `0.117200 / 0.244000 / 0.368600 / 0.612900 / 0.862100` | `0.057700 / 0.122700 / 0.217100 / 0.453200 / 0.747400` |
| 3 | `0.114500 / 0.239100 / 0.363800 / 0.608700 / 0.864000` | `0.058600 / 0.121500 / 0.220900 / 0.456500 / 0.761300` |
| Mean ± SD | `0.116333 ± 0.001589` MRR | `0.058067 ± 0.000473` MRR |

### Setting-B fixed heuristics

| Heuristic | Validation MRR | Test MRR |
|---|---:|---:|
| CN | `0.8638` | `0.2991` |
| AA | `0.8866` | `0.3150` |
| RA | `0.8866` | `0.3176` |
| PA | `0.0600` | `0.0592` |

## Interpretation

DCDLP is consistently far above the official GCN under both settings and all three seeds, but this is not evidence for a new V8 architecture. It shows that the existing Parent can exploit this particular protocol more effectively than the official GCN implementation. In B validation, AA/RA slightly exceed DCDLP (`0.8866` versus `0.8740` mean MRR), while DCDLP is higher on the frozen test set (`0.4118` versus `0.3176`). The validation-to-test reversal is itself evidence of a severe shift and a reason not to use test performance for model decisions.

## Raw artifacts

Per-seed DCDLP JSONs and logs are under `raw/v8_dcdlp_pred_2_1_seed{1,2,3}.*` and `raw/v8_dcdlp_pred_2_4_seed{1,2,3}.*`. Official GCN logs are `raw/gcn_saved_2_1_seed{1,2,3}.log` and `raw/gcn_saved_2_4_seed{1,2,3}.log`. The machine-readable aggregation is `raw/v8_results_summary.json`.
