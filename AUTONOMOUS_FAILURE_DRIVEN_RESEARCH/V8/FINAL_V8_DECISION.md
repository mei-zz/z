# V8 Final Decision

## Status

**`BENCHMARK_READY_NO_GAP`**

## Why the benchmark is ready

- Both fixed LPShift settings were loaded from official generated artifacts.
- The adapter passed 10/10 protocol tests on both settings.
- Message graph, split tensors, candidate order, negative grouping, and file/tensor hashes were checked.
- DCDLP optimized decoding was numerically equivalent to the direct implementation on the retained equivalence test.
- Official GCN and DCDLP were trained on model seeds 1, 2, and 3 for both settings.
- Validation-only model selection was respected; test values were reported after freezing.
- Raw JSON, prediction files, logs, configurations, hashes, and remote paths were retained.

## What was learned

The LPShift shift is substantial and reproducible:

- Setting A train-positive CN mean `11.7676`, validation `0.4329`, test `0.0000`.
- Setting B train-positive CN mean `15.5509`, validation `1.7015`, test `0.3409`.
- Most negative candidates have CN zero in every split.
- Positive feature cosine is comparatively stable and separates positives from negatives.

DCDLP Parent is much stronger than the reproduced official GCN under the two locked settings:

- A validation MRR: DCDLP `0.5237 ± 0.0034`, GCN `0.0708 ± 0.0007`.
- A test MRR: DCDLP `0.2352 ± 0.0067`, GCN `0.0549 ± 0.0027`.
- B validation MRR: DCDLP `0.8740 ± 0.0048`, GCN `0.1163 ± 0.0016`.
- B test MRR: DCDLP `0.4118 ± 0.0650`, GCN `0.0581 ± 0.0005`.

However, this does not identify a new structural information gap:

- A validation feature-cosine MRR is `0.5270`, slightly above DCDLP `0.5237`.
- A test feature-cosine MRR is `0.5384`, above DCDLP's three-seed mean `0.2352`.
- B test feature-cosine MRR is `0.5428`, above DCDLP's three-seed mean `0.4118`.
- In B validation, AA/RA (`0.8866`) are slightly above DCDLP (`0.8740`).
- B CN-zero subgroup MRR varies from `0.2794` to `0.0922` across DCDLP seeds.

The evidence supports a distribution-shift and candidate-tie failure scenario, but the observed gains can be explained by existing feature evidence, topology statistics, and protocol/training differences. It does not support claiming a missing propagation state or a new GNN structure.

## Required V8 questions

### Is the DCDLP adapter legal?

Yes for the LPShift data protocol. It preserves official message context edges, separates train/validation/test tensors, masks DCDLP training targets, and does not use held-out labels in training negative sampling. The official GCN's own masking and negative-sampling behavior differs and is explicitly documented.

### Is there a stable failure mechanism?

Yes: positive topology statistics shift sharply and topology-only heuristics can collapse. But the mechanism is not independent of simple feature cosine, and the hardest B subgroup is not seed-stable.

### Is a new structure justified now?

No. V8 must stop before architectural development. A feature-only and matched-protocol control matrix is required before any V9 structure can be motivated.

## Preserved failure records

- Initial B hash assertion typo, corrected without changing data.
- Unoptimized DCDLP full run stopped after CPU neighbor-set reconstruction bottleneck.
- Two sparse decoder in-place-autograd failures before equivalence validation.
- Initial official GCN `--save_test` attempt failed because its output directory did not exist; reruns completed after creating the intended directory.
- Official GCN CUDA peak memory was not instrumented for seeds 2/3; no fabricated values are reported.

## Artifact index

- `ADAPTER_IMPLEMENTATION.md`
- `PROTOCOL_UNIT_TESTS.md`
- `MULTI_SEED_BASELINES.md`
- `SHIFT_DISTRIBUTION_AUDIT.md`
- `FAILURE_SUBGROUP_ANALYSIS.md`
- `RESEARCHER_CRITIC_DEBATE.md`
- `raw/v8_results_summary.json`
- `raw/v8_adapter_tests_2_1.json`, `raw/v8_adapter_tests_2_4.json`
- `raw/v8_shift_distribution_2_1.json`, `raw/v8_shift_distribution_2_4.json`
- `raw/v8_failure_subgroups_2_1.json`, `raw/v8_failure_subgroups_2_4.json`

The authoritative large prediction tensors and official GCN score checkpoints remain on the remote V100 workspace under `/home/ubuntu/AFDR_V7/raw/`; their corresponding JSON/log paths are recorded in the baseline report.
