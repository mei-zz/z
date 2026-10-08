# Cora locked reproduction — V7.1

Frozen protocol: STRICT_TRAIN_ONLY, 20 train candidates per positive, one selected negative per train positive per epoch, fixed epoch 10, QTHS25 alpha=0.25. All arms share one runtime, split, train pool and evaluation candidate arrays.

- Runtime: {"python": "3.11.11", "torch": "2.3.1+cu121", "torch_cuda_build": "12.1", "cuda_available": true, "gpu": "Tesla V100-PCIE-16GB", "pyg": "2.5.3", "numpy": "1.26.4", "protocol": "STRICT_TRAIN_ONLY", "checkpoint_rule": "FIXED_EPOCH_10", "environment_route": "LOCKED_TORCH_2_3_1_CUDA_12_1", "environment_repro_blocked": false}
- Split hash: `c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a`; train-pool hash: `3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba`; validation candidates: `aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455`.
- Frozen Graph-teacher state hash: `30343bdf61b8fa38a7d9eecbd280a836ee81ef4dfeb63efeb1c74445337ad28b`; cached Graph-teacher score hash: `a1b01e0e2ad5cd287011862d65ade0681205d11ca99dc50cf1b763faf8a82d5c`.

## Validation MRR

| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |
|---|---:|---:|---:|---:|---:|
| C0_UNIFORM | 0.485973 | 0.591476 | 0.569234 | 0.548894 | 0.055615 |
| C1_GRAPH_HARD | 0.532759 | 0.328583 | 0.500069 | 0.453804 | 0.109669 |
| C2_RANDOM_VETO | 0.531053 | 0.361110 | 0.519806 | 0.470656 | 0.095036 |
| C3_QTHS25 | 0.530263 | 0.383612 | 0.510112 | 0.474662 | 0.079493 |

## Test MRR (opened once after validation freeze)

| Method | Seed 0 | Seed 1 | Seed 2 | Mean | Sample SD |
|---|---:|---:|---:|---:|---:|
| C0_UNIFORM | 0.496163 | 0.581666 | 0.566902 | 0.548244 | 0.045703 |
| C1_GRAPH_HARD | 0.555629 | 0.370896 | 0.491130 | 0.472552 | 0.093757 |
| C2_RANDOM_VETO | 0.549985 | 0.382473 | 0.537733 | 0.490064 | 0.093377 |
| C3_QTHS25 | 0.554033 | 0.384672 | 0.541427 | 0.493377 | 0.094352 |

- Locked reproduction: **PASS**.
- Test candidate hash: `ddbb4e92f8bedb8eafa0b9f04a6b75b5a121d8bc0af3a30a4f24588638fe7f92`.
- Paired test deltas: `{"C3_QTHS25_minus_C1_GRAPH_HARD_by_seed": [-0.0015961419048433623, 0.01377608488996035, 0.050296626042788506], "C3_QTHS25_minus_C2_RANDOM_VETO_by_seed": [0.004047862162974258, 0.0021989430935007714, 0.0036938154845169713], "C1_GRAPH_HARD_minus_C0_UNIFORM_by_seed": [0.05946577415902582, -0.21077072053853707, -0.07577205712930746], "C2_RANDOM_VETO_minus_C0_UNIFORM_by_seed": [0.0538217700912082, -0.1991935787420775, -0.029169246571035923], "C3_QTHS25_minus_C0_UNIFORM_by_seed": [0.05786963225418246, -0.19699463564857672, -0.02547543108651895]}`.
