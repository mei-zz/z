# V8 — Protocol-Preserving LPShift Adapter Audit

## Final status

```text
STATUS: EXECUTED
PROTOCOL_STATUS: PROTOCOL_PARTIALLY_READY
```

The adapter implementation, local protocol tests, archived official-data
checks, and archived official GCN baseline runs were audited. The status is
`PROTOCOL_PARTIALLY_READY` because the updated direction/multiplicity check
has not been rerun against the remote `.pt` files after the final adapter
patch; those official data files are not present in this workspace and the
remote password channel was unavailable. No PCHR experiment was run.

## 1. Workspace and audit boundary

The local path is `D:\我的资料库\Documents\Downloads\DCDLP-main` and contains
`pyproject.toml`, `src\dcdlp`, and the DCDLP test suite. The requested
`workspace_info` MCP check failed with an MCP internal error; the local path
and Python project metadata were used as the fallback evidence. The directory
is not a Git checkout (`git status` reports “not a git repository”), so no
commit hash is claimed here.

This audit is restricted to LPShift data adaptation and the frozen official
GCN reproduction. PCHR, hypergraph tuning, and new module search are outside
the scope and were not executed.

## 2. Protocol path and original failure

The official recovery artifacts identify the LPShift source as commit
`cd916a4daaf060530326b5a7c43a99d7d4ab294c` in the remote checkout
`/home/ubuntu/AFDR_V7/repo/LPShift-main`, environment `mei_env`. The official
default generator command was:

```text
python gen_synth.py --data_name ogbl-collab --valid_rat 1 --test_rat 2 --inverse
```

The extension was generated with `--valid_rat 2 --test_rat 4`.

The data flow is:

```text
official SynthDataset .pt files
  -> LPShift split edge / edge_neg tensors
  -> independent LPShiftData adapter
  -> raw official message_edge_index + train/valid/test tensors
  -> DCDLP target mask and encoder/decoder
  -> official grouped candidates -> ranking_metrics
```

The old DCDLP path was:

```text
load_dataset()
  -> GraphDataset
  -> GraphDataset.train_graph()
  -> edge_index_from_graph()
  -> DCDLP.forward()
```

The concrete loss occurs at:

- `src/dcdlp/data/loaders.py:70-74`, where `GraphDataset.train_graph()` adds
  only `self.train_pos`.
- `src/dcdlp/train.py:114-116`, where NetworkX edges are converted back to a
  single-orientation tensor.
- `src/dcdlp/models/node_encoder.py:8-11`, where DCDLP then adds the reverse
  orientation and self-loops.
- `src/dcdlp/data/loaders.py:11-21`, where the generic loader canonicalizes,
  uniques, and removes self-loops; this is not allowed for the official
  grouped candidates.

The generic loader also does not recognize the custom LPShift dataset
directories. Passing raw `ogbl-collab` to it would select the OGB split rather
than `ogbl-collab_CN_2_1_0_seed1` or `ogbl-collab_CN_4_2_0_seed1`.

### What the official message graph contains

The official generator removes the final validation/test target edges but
keeps the remaining training and context edges. The audited default graph has
`[2, 1,733,096]` directed rows and `866,548` canonical undirected pairs. The
training positives contain `848,668` canonical pairs, so rebuilding the graph
from training positives deterministically discards `17,880` allowed context
pairs. The extension has `[2, 1,597,130]` rows and `798,565` canonical pairs;
its audited training-graph overlap is `596,728` canonical pairs.

The official graph is already represented as a directionally symmetric edge
list. This matters because the unchanged DCDLP GCN layer itself adds reverse
rows. Sending the raw official tensor directly to that layer would double the
message multiplicity. This was an additional protocol incompatibility found
during this audit.

The official split sizes are:

| setting | train positive | valid positive | test positive | message graph |
|---|---:|---:|---:|---:|
| `(1,2)` | 1,697,336 | 23,669 | 9,048 | `[2,1,733,096]` |
| `(2,4)` | 1,193,456 | 24,097 | 11,551 | `[2,1,597,130]` |

Both settings use grouped candidates with shape `[N,250,2]`. The official
candidate arrays intentionally retain duplicates and false-negative risks;
they are not cleaned by the adapter.

## 3. Minimal implementation

The independent adapter is:

`AUTONOMOUS_FAILURE_DRIVEN_RESEARCH/V8/scripts/lpshift_adapter.py`

It loads the two official `.pt` files directly with `weights_only=False` for
the trusted local artifacts and exposes separate fields:

| adapter field | source | used as a held-out label? |
|---|---|---:|
| `message_edge_index` | exact saved `data.edge_index` | no |
| `train_pos` | `split["train"]["edge"]` | no |
| `valid_pos` | `split["valid"]["edge"]` | yes, evaluation only |
| `test_pos` | `split["test"]["edge"]` | yes, evaluation only |
| `valid_neg` / `test_neg` | official `edge_neg` tensors | evaluation only |

The adapter never reconstructs the message graph from `train_pos`, never
filters official negative candidates, and never merges validation/test labels
into the training sampler. `training_view()` exposes only
`message_edge_index` and `train_pos`.

The final minimal fix is in:

- `lpshift_adapter.py:68-94`: strict `dcdlp_edge_index` construction checks
  that the saved directed multiset is symmetric and keeps exactly one
  orientation per multiplicity. Expanding it through the unchanged DCDLP GCN
  reproduces the exact raw directed edge multiset.
- `lpshift_adapter.py:96-101`: explicit expansion helper used by tests.
- `run_lpshift_dcdlp.py:265`: DCDLP receives the adapter's equivalent view;
  the raw official tensor remains the source for the message-graph audit and
  sparse adjacency.
- `test_dcdlp_fast_equivalence.py:35`: equivalence testing uses the same
  adapter view.

No DCDLP layer, decoder, loss, metric, split, candidate, or Cora loader was
changed.

## 4. Protocol tests

### Local tests executed in this workspace

Command:

```text
D:\anaconda\envs\Z\python.exe -m pytest tests/test_lpshift_adapter_protocol.py -q
```

Result: `3 passed`.

The local fixture verifies:

1. node count, feature identity, and index preservation;
2. direction and duplicate multiplicity equality after DCDLP expansion;
3. removal of both target directions while retaining non-target context;
4. positive row order, grouped negative shape/order, and held-out-label
   separation.

The four modified V8 scripts also passed `py_compile`.

The repository-wide `pytest` invocation was not used as a protocol result:
the selected local interpreter does not have the editable `dcdlp` package and
PyYAML on its import path. The adapter-specific test is self-contained and
passed in that interpreter.

### Archived official-data tests

The prior remote `mei_env` artifacts are:

- `AUTONOMOUS_FAILURE_DRIVEN_RESEARCH/V8/raw/v8_adapter_tests_2_1.json`
- `AUTONOMOUS_FAILURE_DRIVEN_RESEARCH/V8/raw/v8_adapter_tests_2_4.json`

Both archived runs passed their ten original checks: node/features, message
graph shape, train-positive retention, held-out-positive absence, target
masking, context retention, positive order, grouped negative order/shape,
official hashes, and the training-view label boundary.

Recorded fingerprints include:

| setting | message shape | message hash | valid negative hash | test negative hash |
|---|---|---|---|---|
| `(1,2)` | `[2,1,733,096]` | `9f7c3d699b039c5ce37c1c50aa53abfa464df6c897b18c8b79f5d3ad8b101eee` | `24ee3173d984974fd9c9fef4cb133a0e04722b6f8f28415b4fd7c2dafbf0f51d` | `10bd6bd21860ffd4a9b3c525205bfc6919be607e7b3534e1b8d135f575d313d4` |
| `(2,4)` | `[2,1,597,130]` | `e7139c7a780dc610d1032757007b933d32c1b92575cc8fa0fdb996da4445b71d` | `d3d53f225b54fa69a7f676a660949fdf607dfeaf85b0c92c90bbb18bd232940e` | `7d8ea1cca3641da1c21fba8a1a6d81e901bfae6931a7b07c9850eea53949ea19` |

The archived checks predate the final direction-view patch, so they are
evidence for the raw-file/split invariants, not evidence that the new
direction/multiplicity assertion has been executed on the official files.

## 5. Official GCN baseline reproduction

The baseline logs were checked before comparison. They use the official GCN
and scorer, 3 GCN layers, 3 predictor layers, hidden width 128, dropout 0.1,
learning rate `1e-2`, 100 epochs, seed 1, and batch sizes 65,536. Validation
MRR is the selection metric; the official candidate groups and metrics were
not changed.

### Default `(1,2)`

Log: `AUTONOMOUS_FAILURE_DRIVEN_RESEARCH/V8/raw/gcn_saved_2_1_seed1.log`

```text
best valid: 7.12%, best test: 5.78%
Exit status: 0
```

Thus `Validation MRR = 0.0712` and `Test MRR = 0.0578`, matching the handoff
reference without changing the protocol.

### Extension `(2,4)`

Log: `AUTONOMOUS_FAILURE_DRIVEN_RESEARCH/V8/raw/gcn_saved_2_4_seed1.log`

```text
best valid: 11.73%, best test: 5.79%
Exit status: 0
```

Thus `Validation MRR = 0.1173` and `Test MRR = 0.0579`.

The exact commands recorded in the logs were:

```text
timeout 1800 python /home/ubuntu/AFDR_V7/lpcompat_run.py main_gnn.py --data_name ogbl-collab_CN_2_1_0 --lr 1e-2 --dropout 0.1 --device 0 --epochs 100 --eval_steps 20 --log_steps 1 --runs 1 --seed 1 --batch_size 65536 --val_batch_size 65536 --test_batch_size 65536 --save_test --output_dir /home/ubuntu/AFDR_V7/raw/gcn_saved_2_1_seed1

timeout 1800 python /home/ubuntu/AFDR_V7/lpcompat_run.py main_gnn.py --data_name ogbl-collab_CN_4_2_0 --lr 1e-2 --dropout 0.1 --device 0 --epochs 100 --eval_steps 20 --log_steps 1 --runs 1 --seed 1 --batch_size 65536 --val_batch_size 65536 --test_batch_size 65536 --save_test --output_dir /home/ubuntu/AFDR_V7/raw/gcn_saved_2_4_seed1
```

These are official GCN reference runs, not DCDLP results. The official GCN
and DCDLP still differ in their training-negative sampler and target-masking
path; this is an explicit implementation difference, not silently folded
into the baseline comparison.

## 6. Stale results and remaining limits

The archived V8 DCDLP formal JSON/log files were produced before the final
direction-view correction and must not be cited as results of this patched
adapter. They are retained as history only. No PCHR result was generated.

Remaining limits:

1. Official LPShift `.pt`/`.npy` files are not stored locally.
2. The final direction/multiplicity test needs one remote rerun against both
   official datasets.
3. After that rerun, DCDLP formal runs must be regenerated through the patched
   `dcdlp_edge_index`; old V8 DCDLP metrics are not substitutes.
4. The official GCN and DCDLP have different optimization/sampling/masking
   implementations, so a future model comparison must report those differences
   rather than interpret the GCN number as a causal control for DCDLP.

## Final handoff

```text
STATUS: EXECUTED
PROTOCOL_STATUS: PROTOCOL_PARTIALLY_READY
TESTS: local adapter protocol 3/3 passed; archived official raw/split checks 10/10 for both (1,2) and (2,4); final official direction-view rerun pending
BASELINE_REPRODUCTION: official GCN (1,2) valid MRR 0.0712, test MRR 0.0578; (2,4) valid MRR 0.1173, test MRR 0.0579; both exit 0
NEXT_EXPECTED_STEP: rerun the updated adapter protocol test on the official remote files, then regenerate only the DCDLP Parent runs through the corrected direction-preserving adapter
```
