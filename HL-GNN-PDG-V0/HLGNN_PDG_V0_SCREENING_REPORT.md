# HL-GNN-PDG V0 screening report

Final verdict: **STOP**

## 1. Source audit

See `HLGNN_PDG_SOURCE_AUDIT.md`. The official parent uses a global `(K+1,)` `self.temp`, streams hop states into one global hidden representation, and feeds the endpoint product to the original LinkPredictor.

## 2. Parent mathematical reconstruction

`X^(0)=Linear(X)`; `X^(k+1)=normalized_train_adjacency @ X^(k)`; `H=sum_k t_k X^(k)`. PDG keeps the same propagation and uses `w_k(u,v)=t_k+c*tanh(a)*tanh(G(profile_uv))`.

## 3. Seed and negative-sampling audit

The official split is generated with seed 234 before resetting the requested seed. Each variant×seed is a separate process. Training batch permutations use an independent deterministic generator, and random negative edges use a dedicated CPU generator shared by all four variants for the same dataset×seed.

## 4. Parent reproduction and initial equivalence

B0 is the unmodified parent model and original LinkPredictor. B1 appends the four profiles to the endpoint product. B2 is PDG; B3 has the same gate and parameterization with within-pool profile shuffling.

| Dataset | Seed | B2 max abs init logit diff |
| --- | ---: | ---: |
| cora | 0 | 0.000e+00 |
| cora | 1 | 0.000e+00 |
| cora | 2 | 0.000e+00 |
| citeseer | 0 | 0.000e+00 |
| citeseer | 1 | 0.000e+00 |
| citeseer | 2 | 0.000e+00 |

## 5. Seed-level metrics

| Dataset | Seed | Parent | Profile | PDG | Shuffled | ΔPDG |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| cora | 0 | 95.45 | 92.98 | 95.64 | 95.83 | +0.19 |
| cora | 1 | 94.50 | 92.98 | 94.69 | 95.07 | +0.19 |
| cora | 2 | 94.88 | 94.50 | 95.07 | 94.88 | +0.19 |
| citeseer | 0 | 97.36 | 97.36 | 97.58 | 97.36 | +0.22 |
| citeseer | 1 | 96.70 | 97.14 | 97.36 | 96.92 | +0.66 |
| citeseer | 2 | 97.80 | 97.58 | 97.58 | 97.80 | -0.22 |

## 6. Mean ± std

### cora
- Parent: Hits@10 61.04 ± 2.92; Hits@50 87.92 ± 0.29; Hits@100 94.94 ± 0.48
- Profile Direct: Hits@10 66.03 ± 1.19; Hits@50 88.36 ± 0.48; Hits@100 93.49 ± 0.88
- PDG: Hits@10 61.29 ± 1.81; Hits@50 87.41 ± 0.77; Hits@100 95.13 ± 0.48
- Shuffled PDG: Hits@10 60.28 ± 1.14; Hits@50 88.55 ± 0.96; Hits@100 95.26 ± 0.50
### citeseer
- Parent: Hits@10 65.42 ± 10.37; Hits@50 92.75 ± 0.79; Hits@100 97.29 ± 0.55
- Profile Direct: Hits@10 61.54 ± 2.12; Hits@50 91.36 ± 0.71; Hits@100 97.36 ± 0.22
- PDG: Hits@10 71.79 ± 11.75; Hits@50 93.41 ± 1.34; Hits@100 97.51 ± 0.13
- Shuffled PDG: Hits@10 64.84 ± 10.36; Hits@50 93.11 ± 0.55; Hits@100 97.36 ± 0.44

## 7. Expected-depth and gate diagnostics

- Mean expected depth across PDG runs: 4.3520
- Mean expected-depth within-run std: 0.0000
- Mean `mean|w-t|`: 0.000000
- Mean pairwise hop-weight std: 0.000000
- Mean subgroup depth range: 0.0000

The per-run JSON files contain depth quantiles, CN=0/1/>=2 groups, train-only degree thresholds, train-only feature-similarity thresholds, and subgroup depth statistics.

## 8. Parameters, runtime, and GPU memory

| Dataset | Variant | Params (mean) | Epoch sec (mean) | Peak allocated MB (mean) |
| --- | --- | ---: | ---: | ---: |
| cora | B0 | 80927520 | 1.254 | 2215.3 |
| cora | B1 | 80960288 | 1.244 | 2216.4 |
| cora | B2 | 80928374 | 1.309 | 2677.2 |
| cora | B3 | 80928374 | 1.310 | 2697.6 |
| citeseer | B0 | 44067294 | 1.407 | 2088.5 |
| citeseer | B1 | 44100062 | 1.406 | 2088.5 |
| citeseer | B2 | 44068148 | 1.463 | 3221.9 |
| citeseer | B3 | 44068148 | 1.463 | 3221.1 |

Mean PDG-vs-Parent epoch-runtime overhead: 4.21%
Mean PDG-vs-Parent peak-allocated-memory overhead: 37.56%

## 9. Interpretation

PDG > Parent on 5/6 paired seeds. Dataset mean ΔPDG (percentage points): cora +0.19; citeseer +0.22. PDG-vs-Shuffled means: cora -0.13; citeseer +0.15. PDG-vs-Profile means: cora +1.64; citeseer +0.15.

## 10. Final verdict

**STOP**


## 11. Gate-collapse diagnostics

| Dataset | Seed | mean|w-t| | mean pairwise std(w) | depth mean | depth std |
| --- | ---: | ---: | ---: | ---: | ---: |
| cora | 0 | 1.255e-09 | 3.971e-07 | 4.0636 | 0.000e+00 |
| cora | 1 | 1.167e-09 | 2.934e-07 | 4.0796 | 0.000e+00 |
| cora | 2 | 1.158e-09 | 3.249e-07 | 4.0714 | 4.768e-07 |
| citeseer | 0 | 8.278e-10 | 3.685e-07 | 4.7446 | 0.000e+00 |
| citeseer | 1 | 1.363e-09 | 3.037e-07 | 4.5759 | 0.000e+00 |
| citeseer | 2 | 1.196e-09 | 3.627e-07 | 4.5766 | 4.768e-07 |

## 12. CN subgroup

| Dataset | Seed | Group | Count | E[D_uv] | SD[D_uv] | mean|w-t| |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| cora | 0 | CN=0 | 808 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 0 | CN=1 | 171 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 0 | CN>=2 | 75 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 1 | CN=0 | 808 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 1 | CN=1 | 171 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 1 | CN>=2 | 75 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 2 | CN=0 | 808 | 4.0714 | 0.0000 | 1.158e-09 |
| cora | 2 | CN=1 | 171 | 4.0714 | 0.0000 | 1.158e-09 |
| cora | 2 | CN>=2 | 75 | 4.0714 | 0.0000 | 1.158e-09 |
| citeseer | 0 | CN=0 | 747 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 0 | CN=1 | 111 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 0 | CN>=2 | 52 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 1 | CN=0 | 747 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 1 | CN=1 | 111 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 1 | CN>=2 | 52 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 2 | CN=0 | 747 | 4.5766 | 0.0000 | 1.196e-09 |
| citeseer | 2 | CN=1 | 111 | 4.5766 | 0.0000 | 1.196e-09 |
| citeseer | 2 | CN>=2 | 52 | 4.5766 | 0.0000 | 1.196e-09 |

## 13. Degree subgroup

| Dataset | Seed | Group | Count | E[D_uv] | SD[D_uv] | mean|w-t| |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| cora | 0 | degree_low | 551 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 0 | degree_medium | 270 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 0 | degree_high | 233 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 1 | degree_low | 551 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 1 | degree_medium | 270 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 1 | degree_high | 233 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 2 | degree_low | 551 | 4.0714 | 0.0000 | 1.158e-09 |
| cora | 2 | degree_medium | 270 | 4.0714 | 0.0000 | 1.158e-09 |
| cora | 2 | degree_high | 233 | 4.0714 | 0.0000 | 1.158e-09 |
| citeseer | 0 | degree_low | 477 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 0 | degree_medium | 185 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 0 | degree_high | 248 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 1 | degree_low | 477 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 1 | degree_medium | 185 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 1 | degree_high | 248 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 2 | degree_low | 477 | 4.5766 | 0.0000 | 1.196e-09 |
| citeseer | 2 | degree_medium | 185 | 4.5766 | 0.0000 | 1.196e-09 |
| citeseer | 2 | degree_high | 248 | 4.5766 | 0.0000 | 1.196e-09 |

## 14. Feature-similarity subgroup

| Dataset | Seed | Group | Count | E[D_uv] | SD[D_uv] | mean|w-t| |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| cora | 0 | similarity_low | 359 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 0 | similarity_medium | 325 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 0 | similarity_high | 370 | 4.0636 | 0.0000 | 1.255e-09 |
| cora | 1 | similarity_low | 359 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 1 | similarity_medium | 325 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 1 | similarity_high | 370 | 4.0796 | 0.0000 | 1.167e-09 |
| cora | 2 | similarity_low | 359 | 4.0714 | 0.0000 | 1.158e-09 |
| cora | 2 | similarity_medium | 325 | 4.0714 | 0.0000 | 1.158e-09 |
| cora | 2 | similarity_high | 370 | 4.0714 | 0.0000 | 1.158e-09 |
| citeseer | 0 | similarity_low | 291 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 0 | similarity_medium | 307 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 0 | similarity_high | 312 | 4.7446 | 0.0000 | 8.278e-10 |
| citeseer | 1 | similarity_low | 291 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 1 | similarity_medium | 307 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 1 | similarity_high | 312 | 4.5759 | 0.0000 | 1.363e-09 |
| citeseer | 2 | similarity_low | 291 | 4.5766 | 0.0000 | 1.196e-09 |
| citeseer | 2 | similarity_medium | 307 | 4.5766 | 0.0000 | 1.196e-09 |
| citeseer | 2 | similarity_high | 312 | 4.5766 | 0.0000 | 1.196e-09 |

## 15. Interpretation note

The measured gate deltas and subgroup depth ranges above are the mechanism check. A near-zero value indicates that the zero-initialized residual gate stayed at the parent profile during training.

## 16. Final verdict

**STOP**
