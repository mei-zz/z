# V16 control audit — C1_NHMC_SIZE promoted to HSPE

## Frozen implementation

The V16 C1 path is the exact HSPE-REAL definition for V17. It starts from each candidate pair’s V16 shared-support hyperedge-pair tokens, keeps only the three size descriptors, and zeros the three overlap descriptors. For hyperedge sizes a and b, the retained symmetric values are log(1+a)+log(1+b), the absolute difference of the log sizes, and their product.

The six-wide input is processed by Linear(6,8), ReLU, permutation-invariant mean and max pooling. The pooled 16 values are concatenated with log(1+token_count) and log(1+shared_support_count); a zero-initialized Linear(18,1) adds the residual to the frozen baseline score. The added count is 56+19=75 trainable parameters. No overlap, CN, HRA, ECR, order attention, or extra feature enters this path.

## Frozen prediction context

Raw-HG DCDLP A5, raw-star construction, V16 QTHS25 selected negatives, the V6.1 baseline configuration, BCE, decoder, optimizer, and validation evaluator are reused. The audited baseline uses GCN, hidden size 16, two layers, dropout 0, branch size 8, learning rate 0.001, weight decay 0.0001, and batch size 4096. Each epoch uses the same fixed QTHS25 negative for each train positive. Stage 1 runs five epochs, validation only; the V17 confirmation stage is ten epochs only after both datasets pass the 5E gate.

V16 target masking removes a train-positive target edge before its raw-star token is formed. The V16 mask audit compared local masking with a full raw-star rebuild and checked endpoint symmetry on 100 train-positive samples per dataset; maximum difference was zero. V17 reuses the V16 train/validation pair-feature caches only after checksum and exact candidate-key validation. The test split remains unused.

## V16 seed-0 origin evidence (not V17 confirmation)

| Dataset | B0 MRR | V16 C1 size-only MRR | H1−B0 |
|---|---:|---:|---:|
| Cora | 0.503991 | 0.590748 | +0.086757 |
| PubMed | 0.826532 | 0.837051 | +0.010519 |

These observed V16 values motivate the candidate and are not counted as independent Cora confirmation. PubMed B0 and C1 may be reused for V17 seed 0 only when the V16 script, split/pool, selected-negative, validation-candidate, seed, epoch, feature-cache, and checkpoint checks all match. The Cora V16 script hash predates the final V16 audit patch and therefore its seed-0 arms are rerun.

## Source and artifact provenance

V16 Cora Stage 1 source hash: d15aa844e83fe021d6c0c3808026ea62c949dffdf3d80109ef20b5fb99756d83.

V16 PubMed Stage 1 and frozen implementation source hash: f3b19889afa236fd71eeaa6681efc31c845eb32c4a90df87ab8d40092c196982.

V16 Cora train-pool / selected-negative / validation-candidate hashes are retained in the Cora Stage 1 result JSON; the corresponding PubMed hashes are retained in the PubMed Stage 1 result JSON. V17 results.json records all current code hashes, input/cache hashes, and result/checkpoint hashes for any reused arm.