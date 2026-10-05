# Cora Stage 1: six-arm validation-only screen

**Decision: NHMC_STAGE1_GO** under the frozen gate. Seed 0, five epochs, V100, 263 validation positives × 20 candidates, test OFF. All six arms used the same train-only QTHS25 selected-negative hash and validation candidate hash. Zero-initialization audit confirmed baseline logits matched exactly (maximum absolute difference 0).

|Arm|Validation MRR|H1−arm|
|---|---:|---:|
|B0_BASELINE|0.503991|0.089560|
|B1_HRA|0.504136|0.089415|
|B2_NATIVE_SCALAR|0.532451|0.061099|
|C1_NHMC_SIZE|0.590748|0.002803|
|C2_NHMC_SHUFFLE|0.589727|0.003823|
|H1_NHMC_REAL|0.593551|—|

|Gate|Required|Observed|Pass|
|---|---:|---:|---|
|H1−B0|≥0.003|0.089560|YES|
|H1−best scalar|≥0.002|0.061099|YES|
|H1−C1 SIZE|≥0.002|0.002803|YES|
|H1−C2 SHUFFLE|≥0.002 (train shuffle power 0.4535)|0.003823|YES|

Baseline trainable parameters: 24735. H1 adds 75 (0.3032%); below the 2% cap. Cora wall time: 206.6 s; summed arm training time: 191.94 s.

The legacy trainer read empty `TrainOnlyView` compatibility sentinels. They contain zero validation/test edges; actual test identities were not exposed and test scoring remained disabled. The first audit misclassified these sentinel reads and lacked the baseline parameter count. The result was reconciled from the completed checkpoints and validation metrics. Original failure/status and pre-reconciliation snapshots remain under diagnostics.
