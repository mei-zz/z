# CDPT Deepening V3 — Five-Seed Results

## Locked protocol

Cora HeaRT, seeds 0–4, four epochs, shared Parent initialization, reset Python/NumPy/PyTorch seed before each model construction and training, validation-MRR checkpoint selection, and frozen official test report. Seed 1 is retained even though the historical V2 result was a failure; no seed was removed.

## Test metrics by seed

Each cell is `MRR / Hits@10 / Hits@20 / Hits@50 / Hits@100`. B2–B4 are shown with MRR and Hits@10 to keep the paired mechanism table readable; their complete metrics remain in the raw JSON files.

| Seed | B0 Parent | B1 CDPT | B2 Late-only | B3 Concat MLP | B4 Fixed random |
|---:|---|---|---|---|---|
| 0 | 0.100207 / 0.242884 / 0.368121 / 0.595825 / 0.774194 | 0.093889 / 0.237192 / 0.354839 / 0.518027 / 0.715370 | 0.107616 / 0.263757 | 0.104053 | 0.096757 |
| 1 | 0.104982 / 0.227704 / 0.354839 / 0.531309 / 0.713472 | 0.110229 / 0.267552 / 0.409867 / 0.609108 / 0.779886 | 0.113919 / 0.233397 | 0.102819 | 0.102542 |
| 2 | 0.092927 / 0.225806 / 0.356736 / 0.538899 / 0.732448 | 0.106854 / 0.273245 / 0.385199 / 0.593928 / 0.789374 | 0.113244 / 0.280835 | 0.098369 | 0.103308 |
| 3 | 0.082718 / 0.195446 / 0.297913 / 0.407970 / 0.584440 | 0.107712 / 0.259962 / 0.383302 / 0.609108 / 0.785579 | 0.102905 / 0.259962 | 0.082428 | 0.104570 |
| 4 | 0.103012 / 0.248577 / 0.362429 / 0.590133 / 0.759013 | 0.109941 / 0.250474 / 0.368121 / 0.616698 / 0.757116 | 0.100771 / 0.214421 | 0.104029 | 0.103084 |

CDPT's paired test MRR deltas versus Parent are `-0.006318, +0.005248, +0.013928, +0.024994, +0.006929` for seeds 0–4. Thus 4/5 test MRR differences are positive, while seed 0 remains a visible failure and is not hidden.

## Aggregate paired differences

| Model | Mean validation ΔMRR ± SD | Mean test ΔMRR ± SD | Validation wins | Test wins |
|---|---:|---:|---:|---:|
| B1 CDPT | +0.007241 ± 0.007760 | +0.008956 ± 0.011544 | 5/5 | 4/5 |
| B2 Late-only | +0.005557 ± 0.004244 | +0.010922 ± 0.009535 | 4/5 | 4/5 |
| B3 Concat MLP | +0.002506 ± 0.001332 | +0.001571 ± 0.003077 | 5/5 | 3/5 |
| B4 Fixed random | +0.009384 ± 0.005849 | +0.005283 ± 0.010766 | 5/5 | 3/5 |

Approximate t intervals with df=4 are descriptive only. For CDPT, validation ΔMRR is `[-0.002395, +0.016876]` and test ΔMRR is `[-0.005378, +0.023290]`.

## Runtime, parameters, and GPU memory

| Model | Total params | Trainable params | Runtime recording | Peak GPU recording |
|---|---:|---:|---|---|
| B0 | 112,486 | 112,486 | saved in every seed JSON | 55.438 MiB in every seed |
| B1 | 119,751 | 119,751 | saved in every seed JSON | 59.245 MiB in every seed |
| B2 | 119,751 | 119,751 | saved in every seed JSON | 59.294 MiB in every seed |
| B3 | 119,718 | 119,718 | saved in every seed JSON | 59.303 MiB in every seed |
| B4 | 119,751 | 118,727 | saved in every seed JSON | 59.341 MiB in every seed |

Peak memory was measured by `torch.cuda.max_memory_allocated` inside the runner. The original Cora seed0–2 metric files predate the instrumentation and are preserved. The separate `cora_measured/` outputs are resource-complete reruns; they do not replace the original performance files.

The measured reruns are not silently merged into the performance aggregate: CUDA execution is not bitwise deterministic in this graph path. Across the original versus measured reruns, the largest test-MRR difference was 0.013950 (B4, seed2), while most differences were small. The five-seed performance tables above therefore use the first complete five-seed batch consistently; the measured files are used for resource auditing only.

## Raw artifacts

- `phase2_seed0/` — original seed0 five-model run and separate train-time shuffle control.
- `cora_five_seeds/seed1/` through `seed4/` — original five-model seed runs.
- `cora_measured/seed0/` through `seed2/` — resource-instrumented reruns for the missing peak-memory fields.
