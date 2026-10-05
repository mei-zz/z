# V8 Adapter Implementation

## Scope

V8 only adapts the existing DCDLP Parent to the official LPShift artifacts. No new GNN module, loss, hidden width, or decoder was introduced.

Remote execution root: `/home/ubuntu/AFDR_V7/repo/LPShift-main`  
Remote V8 scripts: `/home/ubuntu/AFDR_V8_scripts/`  
Remote raw artifacts: `/home/ubuntu/AFDR_V7/raw/`  
Environment: `mei_env`, Python 3.11.11, PyTorch 2.8.0+cu128, PyG 2.5.3, Tesla V100-PCIE-16GB.

The official LPShift commit used for recovery is `cd916a4daaf060530326b5a7c43a99d7d4ab294c`. The adapter is implemented in `scripts/lpshift_adapter.py` and the protocol-preserving DCDLP runner in `scripts/run_lpshift_dcdlp.py`.

## Explicit data separation

The adapter keeps the following tensors separate:

| Object | Source | Used by training message passing? |
|---|---|---:|
| `message_edge_index` | official LPShift `.pt` | Yes |
| `train_pos` | official split | Yes, as positive targets |
| `valid_pos` | official split | No |
| `test_pos` | official split | No |
| `valid_neg` | official `heart_valid_samples.npy` / split | No |
| `test_neg` | official `heart_test_samples.npy` / split | No |

The message graph is never reconstructed from `train_pos`. This is important because LPShift contains additional context edges. Held-out positives are absent from the message graph in both fixed settings; non-target context edges remain available.

Training negatives are sampled only against canonical undirected edges in `message_edge_index`. The historical DCDLP helper used `all_positive` and therefore could read held-out labels; the V8 runner does not call that path. Duplicate official candidates and the recorded false-negative cases are retained and are not silently filtered.

## Target masking

For every DCDLP training batch, both directed representations of each current target pair are removed from the temporary message graph before encoding. Canonical edge keys use `(min(u,v), max(u,v))`, so endpoint order cannot bypass the mask. Validation and test use the unmodified official message graph because the adapter verifies that held-out positives are not present in it.

The official LPShift GCN code does not use this DCDLP target-edge masking path. Therefore the comparison is protocol-valid with respect to the LPShift split and candidate files, but it is not a claim that the two model implementations have identical target masking.

## Semantics-preserving performance work

The original DCDLP decoder repeatedly copied all neighbor sets and was stopped during an early full run after an excessive CPU bottleneck (exit 143). The V8 runner then used cached neighbor sets, a cached sparse adjacency, sparse common-neighbor aggregation, and cached held-out node encoding. `test_dcdlp_fast_equivalence.py` compared the optimized decoder with the direct implementation on 512 pairs:

| Quantity | Maximum absolute difference |
|---|---:|
| logit | `5.96e-7` |
| degree branch score | `0` |
| CN branch score | `4.32e-7` |
| residual branch score | `3.58e-7` |
| interaction score | `4.47e-8` |
| raw CN | `0` |

The optimization therefore changes execution strategy, not the model calculation.

## Dataset fingerprints

### Setting A: `ogbl-collab_CN_2_1_0_seed1`

- nodes: `235,868`
- features: `[235868, 128]`
- message graph: `[2, 1,733,096]`
- train/valid/test positives: `1,697,336 / 23,669 / 9,048`
- negatives per held-out positive: `250`
- message hash: `9f7c3d699b039c5ce37c1c50aa53abfa464df6c897b18c8bb79f5d3ad8b101eee`
- train hash: `5db0173da159b5e79b4a641786b127644d64bb2593b273e11e76b29521e49a4a`
- valid hash: `6c16deb8c6b39dd25f93b76798bcebd62704015c1e5729cd4102fc7371ca35c3`
- test hash: `8f8c0805601d73ee91da361d1c6e695d4a3bc74602c46ffa2886f6004d98bf3a`
- valid negative tensor hash: `24ee3173d984974fd9c9fef4cb133a0e04722b6f8f28415b4fd7c2dafbf0f51d`
- test negative tensor hash: `10bd6bd21860ffd4a9b3c525205bfc6919be607e7b3534e1b8d135f575d313d4`

### Setting B: `ogbl-collab_CN_4_2_0_seed1`

- message graph: `[2, 1,597,130]`
- train/valid/test positives: `1,193,456 / 24,097 / 11,551`
- message hash: `e7139c7a780dc610d1032757007b933d32c1b92575cc8fa0fdb996da4445b71d`
- train hash: `9e876f00d0da73d7bb1229a9aee50ecf8ff9f1f3221eb932fbb9ec5f2c62c048`
- valid hash: `f8ee3623440863545e162b38f4a6ff29cf35b8891ac49d81e8568e562895f42b`
- test hash: `cd34f4b513f4d581e64afa405f9df384031d7b5de960153af7b65317fc992ed9`
- valid negative tensor hash: `d3d53f225b54fa69a7f676a660949fdf607dfeaf85b0c92c90bbb18bd232940e`
- test negative tensor hash: `7d8ea1cca3641da1c21fba8a1a6d81e901bfae6931a7b07c9850eea53949ea19`

## Known implementation incidents

1. The first setting-B adapter check used a mistyped expected hash (`...9400e`); the official file was not changed. The expected value was corrected to the observed `...940e`, and the complete test suite then passed.
2. The first unoptimized DCDLP full attempt was stopped after the CPU neighbor-copy bottleneck. It is retained as a failed run and no metric from it is used.
3. The first sparse decoder implementation triggered two in-place-autograd errors. Those were fixed, then numerical equivalence was tested before formal runs.

These incidents are implementation history, not deleted negative results.
