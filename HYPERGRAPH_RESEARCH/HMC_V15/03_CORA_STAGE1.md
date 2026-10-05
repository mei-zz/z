# Cora Stage 1

Status: NOT RUN — corrected Stage-0 decision was SCALAR_SUFFICIENT, so GPU Stage 1 was not authorized. No arm was trained.

The planned arms were B0 baseline, B1 + support count, B2 + MS, B3 + HRA, C1 HMC-FLAT, C2 HMC-SHUFFLE, and H1 HMC-REAL; Cora seed 0, 5 epochs, QTHS25, BCE, validation only, test disabled. C1/C2/H1 would share 49 added parameters and a zero-initialized residual head.

Promotion would require H1−B0 ≥0.003 MRR; H1−best(B1,B2,B3) ≥0.002; H1−C1 ≥0.002; H1−C2 ≥0.002. These comparisons were not run.
