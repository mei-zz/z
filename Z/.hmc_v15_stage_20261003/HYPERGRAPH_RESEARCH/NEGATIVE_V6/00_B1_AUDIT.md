# V5 B1 Graph-hard audit for V6

**Audit scope:** source code, saved configuration, metrics, candidate-pool metadata, and V5 final report. This audit distinguishes score-based selection from the standard sampler's forbidden-positive filter.

## B1 implementation

| Question | Finding | Evidence |
|---|---|---|
| Which model supplies Graph hardness? | The frozen V5 seed-0 Graph-only DCDLP checkpoint, under A_GHHR/remote_evidence/baseline_10_epoch/G. B1 selects only by that checkpoint's pair logit. | run_cvh_nm_candidate_b.py, make_candidate_pool and choose_negatives; B_CVHNM/candidate_runs/pool_metadata.json |
| Was an HG teacher also scored? | Yes, the matched frozen Raw-HG checkpoint was scored over the same pool for other V5 arms. It does not affect B1's argmax. | Same source and metadata |
| How is the candidate pool made? | Uniform negative sampling for 20 × 4,488 = 89,760 pairs with seed 20261002, then grouped to 20 candidates per training positive with seed 20261003. Pool hash: c3a31fd8ed188a81b4072c95f64fd2b882957649f85a3f97103c05db61531fae. | pool_metadata.json; V5 runner |
| How many candidates and selected negatives? | 20 candidates are scored for each positive; one training negative is selected per positive per epoch (K=1). | V5 runner constants and trainer sampler |
| Static or dynamic? | Static. The candidate pool and frozen teacher scores are generated once. B1 selects each row's Graph argmax; the selected-negative SHA-256 is identical across its 10 epochs: f7cfa686c835021c73c3636bcdef914b72ee9d1cb2bf3e2f463f7c7dc35fae1. No teacher refresh occurs within or between epochs. | B1 metrics.json; runner implementation |
| Is score selection differentiable? | No. Teacher inference scores are copied into NumPy arrays; argmax is outside the training graph. No gradient flows through teacher scoring or selection. | make_candidate_pool and choose_negatives |
| What model is trained? | Raw-HG DCDLP (A5, raw hypergraph branch enabled), not Graph-only. B1 is a sampler intervention on the Raw-HG trainer. | B1 config.json and metrics.json |
| What evaluation candidates are used? | Standard validation: 20 uniform negatives per validation positive, generated with seed 777 and grouped with seed 778. V5 recorded negative-matrix hash aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455 and positive-plus-negative candidate-tensor hash 197912d7397d8d8e118e2c985ff2a7948810c8b96ab5bed91e49c598aa481d48. B1's own metrics leave candidate_hash null; V6 recomputes and verifies both. Test evaluation was disabled. | V5 run_complementarity_audit.py and results.json; B1 metrics.json; train.evaluate_split |
| Which split? | Standard Cora seed 0; split hash 4ad9a114f501. Train-positive hash fd806089f2ddf34eed08e4ad63f611a0516977500964035338fb026eb0453cf8. | B1 metrics.json |
| Did validation/test information enter mining? | No validation/test model scores, ranking metrics, or labels were used to score or rank candidates. There is one protocol-level caveat: V5 calls uniform_negative_sampling with dataset.all_positive, which includes known positives from all splits, as a forbidden-edge filter when drawing the train pool. Thus held-out positive identities can affect candidate rejection, but never hardness scores or the selected-rank rule. V6 preserves this exact behavior for B1 reproduction and will state it explicitly. | V5 runner make_candidate_pool; src/dcdlp/data/negative_sampling.py |

## Reproduction gate

Stored B1 validation MRR is 0.5334445819888557 (best epoch 6), with 10 epochs, seed 0, and the exact B1 config. The matched Raw-HG initial-state hash is 966ac47231c28a65b16a18ae1638e4db4fefd8d7861f7ec105c6b0f942351c69. V6 first regenerates and verifies the pool, teacher-score rankings, selected-negative hash, split, and validation candidates, then reruns B1. Candidate A is blocked unless the reproduced validation MRR differs from 0.533445 by at most 0.003.

The V6 V100 preflight regenerated the exact training-pool and validation candidate hashes, matched the B1 selected-negative hash and the seed-0 initial-state hash, and found identical per-row Graph and HG teacher-score orderings (including every top-2 set). Floating score-array hashes differ across replays by less than 3.6e-7 maximum, consistent with tiny CUDA accumulation variation; ranking and selected examples are unchanged. The actual V6 B1 rerun reached MRR 0.5334445819888557 (absolute error 0.0), so the reproduction gate passed.

## Baseline references

- Raw-HG with original uniform negatives: 0.5030120048647342 (V5 matched seed-0, 10-epoch baseline).
- Graph-hard B1: 0.5334445819888557 (V5 seed-0, 10-epoch control).
- V5 final report explicitly says test was not evaluated and the server runner completed.

No model code or architecture is changed for V6. Only training-negative selection rules are varied.
