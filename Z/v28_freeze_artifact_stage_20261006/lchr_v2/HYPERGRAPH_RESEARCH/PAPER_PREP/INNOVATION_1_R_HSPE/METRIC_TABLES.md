# METRIC TABLES — R-HSPE

All numeric values below are read from the frozen JSON/CSV results or recomputed from the stored per-seed values where noted. Mean ± SD uses sample SD. Paired deltas are computed within matching seeds. Full experiment protocol is repeated beside every group so validation and test evidence remain separate.

## Table 1 — Frozen standalone test: R-HSPE vs B0

Protocol: V17.2 frozen one-shot test; final epoch 10 checkpoint; target removal enabled; test candidates frozen before scoring; 20 negatives per query; Cora and PubMed seeds 0–4, Citeseer seeds 0–2. No test-guided selection.

| Dataset | Method | n | MRR mean ± SD | Hits@10 mean ± SD | Hits@20 mean ± SD | Mean positive rank mean ± SD |
|---|---|---:|---:|---:|---:|---:|
| Cora | B0 | 5 | 0.46594045724371885 ± 0.1298717019678676 | 0.7935483870967742 ± 0.10866919369944075 | 0.9791271347248577 ± 0.031034966288038167 | 5.868690702087287 ± 1.7031364238656599 |
| Cora | R-HSPE | 5 | 0.6100535476808527 ± 0.0839628360024447 | 0.9104364326375711 ± 0.03069666863566326 | 0.991650853889943 ± 0.011113131282236297 | 3.775332068311195 ± 0.7100687411100163 |
| Pubmed | B0 | 5 | 0.8431156367354253 ± 0.012571941194017468 | 0.9927797833935019 ± 0.0005752503963890859 | 0.9998646209386282 ± 0.00020181118930503804 | 1.6321750902527075 ± 0.06006434657528178 |
| Pubmed | R-HSPE | 5 | 0.8560636614766113 ± 0.02190243205516568 | 0.9911101083032492 ± 0.0015517823884521338 | 0.9997292418772563 ± 0.0004891580186976332 | 1.6078068592057762 ± 0.10648210790663187 |
| Citeseer | B0 | 3 | 0.43857193059090305 ± 0.09192491741595124 | 0.7296703296703297 ± 0.08599559361104991 | 0.9802197802197802 ± 0.024767972900186074 | 6.745421245421245 ± 0.7975935407620519 |
| Citeseer | R-HSPE | 3 | 0.5273195932193366 ± 0.07174903286223369 | 0.8293040293040294 ± 0.053939516876776436 | 0.9934065934065934 ± 0.00439560439560438 | 5.0025641025641026 ± 0.261793054893648 |

Paired MRR deltas (R-HSPE minus comparator):

| Dataset | Contrast | Mean Δ | Median Δ | Seed wins |
|---|---|---:|---:|---:|
| Cora | R-HSPE − B0 | 0.14411309043713388 | 0.08275489536680869 | 5/5 |
| Cora | R-HSPE − C1 count/parameter-matched | -0.014183763816094675 | -0.01652164249412813 | 0/5 |
| Pubmed | R-HSPE − B0 | 0.01294802474118606 | 0.015533443089421395 | 4/5 |
| Pubmed | R-HSPE − C2 constant-set | -0.0011416533382728744 | -0.0013888022718222537 | 2/5 |
| Citeseer | R-HSPE − B0 | 0.0887476626284336 | 0.051092264685382194 | 3/3 |

Citeseer aggregates are recomputed from the three stored test seed records in HSPE_V17_2/THIRD_DATASET.json. The R-HSPE-minus-context comparator is not uniform across datasets: Cora uses the count/parameter-matched C1 arm; PubMed uses the constant-set C2 arm.

## Table 2 — Strong-backbone plug-in test

Protocol: V17.4 Phase B; test split; fixed final epoch 10; five paired seeds (0–4); same per-seed initialization, negative-sampling trace, permutation, and CUDA RNG trace within V17.4; 20 negatives per query. These are the canonical primary plug-in results.

| Dataset | Arm | n | Test MRR mean ± SD |
|---|---|---:|---:|
| Cora | NCNC | 5 | 0.6792374307372457 ± 0.05223880121690982 |
| Cora | NCNC + R-HSPE | 5 | 0.7050901133981805 ± 0.04064610118279473 |
| Cora | NCNC + NULL75 | 5 | 0.6771019108806603 ± 0.05320967799178234 |
| Cora | NCN | 5 | 0.7142296611223624 ± 0.04502090786008005 |
| Cora | NCN + R-HSPE | 5 | 0.7311714358935324 ± 0.040107195095352745 |
| Pubmed | NCNC | 5 | 0.8986670808884256 ± 0.015801355884384145 |
| Pubmed | NCNC + R-HSPE | 5 | 0.9058039955682103 ± 0.01369273569585237 |
| Pubmed | NCNC + NULL75 | 5 | 0.8985998390398209 ± 0.017777986285503634 |
| Pubmed | NCN | 5 | 0.9008697976336739 ± 0.015410381244272232 |
| Pubmed | NCN + R-HSPE | 5 | 0.9072316916245431 ± 0.012257892407511888 |

Paired MRR effects:

| Dataset | Contrast | Mean Δ | Median Δ | Seed wins |
|---|---|---:|---:|---:|
| Cora | NCNC + R-HSPE − NCNC | 0.025852682660934833 | 0.03415585230049967 | 5/5 |
| Cora | NCNC + R-HSPE − NULL75 | 0.02798820251752021 | 0.03432863265492614 | 5/5 |
| Cora | NCN + R-HSPE − NCN | 0.016941774771170048 | 0.018560811421342693 | 5/5 |
| Pubmed | NCNC + R-HSPE − NCNC | 0.007136914679784767 | 0.007610820161587428 | 5/5 |
| Pubmed | NCNC + R-HSPE − NULL75 | 0.007204156528389394 | 0.006713329039592653 | 5/5 |
| Pubmed | NCN + R-HSPE − NCN | 0.006361893990869061 | 0.007418718841327165 | 5/5 |

## Table 3 — Citeseer strong-backbone transfer limitation

Protocol: V17.4 third-dataset phase; validation split only; fixed final epoch 10; seeds 0–2; paired arms; 20 negatives per query. The gate failed and the Citeseer test was not accessed.

| Validation arm | n | Validation MRR mean ± SD |
|---|---:|---:|
| NCNC | 3 | 0.8574180332926121 ± 0.006765440081717476 |
| NCNC + R-HSPE | 3 | 0.8300386552589196 ± 0.014543053533630293 |
| NCNC + NULL75 | 3 | 0.8629748188668893 ± 0.008232566617255549 |

| Paired validation contrast | Mean Δ | Median Δ | Seed wins |
|---|---:|---:|---:|
| NCNC + R-HSPE − NCNC | -0.02737937803369254 | -0.03143486469477641 | 0/3 |
| NCNC + R-HSPE − NULL75 | -0.03293616360796969 | -0.04053546795837537 | 0/3 |

Status: CITESEER_TRANSFER_NOT_SUPPORTED. This is a validation failure; no Citeseer strong-backbone test result exists.

## Table 4 — V17.3 standalone publication benchmark

Protocol: V17.3 benchmark artifact; test metrics as recorded in PAPER_MAIN_TABLE.csv; Cora/PubMed NCN and NCNC trained 100 epochs and selected by first best validation MRR; NSLR-HMANN trained 5000 epochs/final checkpoint; frozen R-HSPE, B0 and controls reused. Seeds and n are shown per row. “Rank” is the within-dataset benchmark rank in that artifact. The declared baseline comparison is not equal-compute.

| Dataset | Method | n | V17.3 MRR rank | MRR mean ± SD |
|---|---|---:|---:|---:|
| Cora | B0_BASELINE | 5 | 5 | 0.46594045724371885 ± 0.1298717019678676 |
| Pubmed | B0_BASELINE | 5 | 5 | 0.8431156367354253 ± 0.012571941194017468 |
| Citeseer | B0_BASELINE | 3 | 4 | 0.43857193059090305 ± 0.09192491741595124 |
| Cora | C1_COUNT_PARAM_MATCHED | 5 | 3 | 0.6242373114969475 ± 0.08596665308300691 |
| Pubmed | C2_CONSTANT_SET | 5 | 3 | 0.8572053148148843 ± 0.0251851648804989 |
| Cora | NCN | 5 | 1 | 0.848105048019659 ± 0.006706340864332814 |
| Pubmed | NCN | 5 | 2 | 0.9303195120346786 ± 0.0018628734079999781 |
| Citeseer | NCN | 5 | 2 | 0.86939014930831 ± 0.007841451227825801 |
| Cora | NCNC | 5 | 2 | 0.8434945922168268 ± 0.006660096129259056 |
| Pubmed | NCNC | 5 | 1 | 0.9370930995022826 ± 0.0018743531595511681 |
| Citeseer | NCNC | 5 | 1 | 0.8858734836591979 ± 0.0040417688791567295 |
| Cora | NSLR-HMANN | 5 | 6 | 0.3909376011546719 ± 0.034777595652838764 |
| Pubmed | NSLR-HMANN | 5 | 6 | 0.5226451617001289 ± 0.021630450968215004 |
| Citeseer | NSLR-HMANN | 5 | 5 | 0.36385716579885263 ± 0.01486236066424293 |
| Cora | R-HSPE | 5 | 4 | 0.6100535476808527 ± 0.0839628360024447 |
| Pubmed | R-HSPE | 5 | 4 | 0.8560636614766113 ± 0.02190243205516568 |
| Citeseer | R-HSPE | 3 | 3 | 0.5273195932193366 ± 0.07174903286223369 |

R-HSPE standalone rank: Cora 4, PubMed 4, Citeseer 3. Frozen interpretation: standalone competitiveness WEAK. Do not merge these absolute scores/ranks with Table 2, which uses a different training/checkpoint protocol.

## Table 5 — Mechanism controls and claim limits

### V17.1 Phase A mechanism screen

Protocol: validation only; 10 epochs; seeds 0–4; H1_HSPE_REAL is the screen arm, not a synonym for every frozen test result. Controls are diagnostic rather than causal decomposition.

| Dataset | Arm | Validation MRR mean ± SD |
|---|---|---:|
| Cora | B0 baseline | 0.44543608768605536 ± 0.1282289058795747 |
| Cora | C0 count-linear | 0.5628302377370348 ± 0.08596771439530418 |
| Cora | C1 count/parameter-matched | 0.6023887112395807 ± 0.078817246319277 |
| Cora | C2 constant-set | 0.5936536391384888 ± 0.08395054779694142 |
| Cora | C3 global size-shuffle | 0.6246619918697282 ± 0.07233389788772464 |
| Cora | H1 HSPE-REAL | 0.574487622823183 ± 0.056905999371889684 |
| Pubmed | B0 baseline | 0.8501581741323319 ± 0.010773516116138618 |
| Pubmed | C0 count-linear | 0.8582153446453855 ± 0.01241401801095542 |
| Pubmed | C1 count/parameter-matched | 0.8630887583617171 ± 0.01834949648707041 |
| Pubmed | C2 constant-set | 0.8657654559399749 ± 0.01945989541470794 |
| Pubmed | C3 global size-shuffle | 0.8631131212056526 ± 0.023672704722857613 |
| Pubmed | H1 HSPE-REAL | 0.8632834624663822 ± 0.0193329934526118 |

| Dataset | Paired contrast | Mean ΔMRR | Median ΔMRR | Seed wins |
|---|---|---:|---:|---:|
| Cora | H1 − B0 | 0.12905153513712764 | 0.10650375556995995 | 5/5 |
| Cora | H1 − C1 count/parameter-matched | -0.027901088416397657 | -0.008986513890927195 | 1/5 |
| Cora | H1 − C2 constant-set | -0.019166016315305966 | -0.002459392212214473 | 1/5 |
| Cora | H1 − C3 global size-shuffle | -0.050174369046545285 | -0.021148559931829847 | 1/5 |
| Pubmed | H1 − B0 | 0.013125288334050179 | 0.017066618324515614 | 4/5 |
| Pubmed | H1 − C1 count/parameter-matched | 0.00019470410466515542 | 0.000275888695669968 | 3/5 |
| Pubmed | H1 − C2 constant-set | -0.002481993473592703 | -0.001404063534827249 | 0/5 |
| Pubmed | H1 − C3 global size-shuffle | 0.00017034126072950072 | 0.000813252170098866 | 3/5 |

### V17.2 final R-HSPE vs context control

Protocol: V17.2 one-shot test; fixed final epoch 10; Cora/PubMed seeds 0–4; 20 negatives/query. These are separate from the V17.1 validation screen.

| Dataset | Contrast | Mean ΔMRR | Median ΔMRR | Seed wins |
|---|---|---:|---:|---:|
| Cora | H2 − B0 | 0.14411309043713388 | 0.08275489536680869 | 5/5 |
| Cora | H2 − C1 count/parameter-matched | -0.014183763816094675 | -0.01652164249412813 | 0/5 |
| Pubmed | H2 − B0 | 0.01294802474118606 | 0.015533443089421395 | 4/5 |
| Pubmed | H2 − C2 constant-set | -0.0011416533382728744 | -0.0013888022718222537 | 2/5 |

These control comparisons leave the frozen interpretation CONTEXT_DRIVEN and SIZE_CAUSAL_CLAIM NOT_SUPPORTED. They do not negate the predictive gains against B0 or the plug-in gains against NCN/NCNC.

## Table 6 — Parameter efficiency and measured costs

### Added parameter ratios

Protocol/source: frozen R-HSPE addition is 75 parameters. Backbone counts are from the V17.3 PAPER_MAIN_TABLE.csv. Ratio is exactly 75 divided by the baseline parameter count shown, in percent; R-HSPE standalone totals are B0 + 75.

| Dataset | B0 params | R-HSPE standalone params | 75 / B0 | NCN params | 75 / NCN | NCNC params | 75 / NCNC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cora | 24735 | 24810 | 0.3032140691328078% | 764163 | 0.00981465996129098% | 830212 | 0.009033837140393056% |
| Pubmed | 9807 | 9882 | 0.7647598654022637% | 525315 | 0.014277147996916137% | 591364 | 0.012682544084523236% |
| Citeseer | 61055 | 61130 | 0.12284006223896486% | 1411587 | 0.005313168795122086% | 1477636 | 0.00507567492941428% |

### Standalone runtime records

Protocol/source: absolute per-seed mean measurements copied from V17.3 PAPER_MAIN_TABLE.csv for the frozen 10-epoch B0/R-HSPE standalone runs; peak GPU memory is the artifact’s recorded peak. These are measured arm totals, not a clean estimate of extra module-only training work.

| Dataset | Arm | n | Mean training seconds | Mean inference/scoring seconds | Peak GPU MB |
|---|---|---:|---:|---:|---:|
| Cora | B0_BASELINE | 5 | 149.02732985178008 | 8.042246694955974 | 58.923828125 |
| Cora | R-HSPE | 5 | 146.69851251831278 | 8.192751836031675 | 71.06689453125 |
| Pubmed | B0_BASELINE | 5 | 3504.83058542097 | 119.4033029725775 | 594.66259765625 |
| Pubmed | R-HSPE | 5 | 2791.0108207447456 | 121.27349124737084 | 762.68994140625 |
| Citeseer | B0_BASELINE | 3 | 95.5744325555861 | 6.719061622706552 | 80.15478515625 |
| Citeseer | R-HSPE | 3 | 93.99165083902578 | 6.199991205862413 | 96.31982421875 |

### V17.4 NCNC plug-in timing and memory

Protocol: Phase B fixed-final-epoch-10 training and paired test scoring; seeds 0–4. Arm values are mean ± sample SD. Paired delta is plug-in minus NCNC. Peak GPU values are mean reported peaks (MB) for the phase indicated.

| Dataset | Arm | Training seconds mean ± SD | Test scoring seconds mean ± SD | Training peak GPU MB | Test peak GPU MB |
|---|---|---:|---:|---:|---:|
| Cora | NCNC | 1.8009297982789576 ± 0.18746430539076944 | 0.45490769054740665 ± 0.04627645637274895 | 141.56083984375 | 69.56396484375 |
| Cora | NCNC + R-HSPE | 1.6091713070869447 ± 0.2931510967391692 | 0.5492455439642072 ± 0.02838376368345352 | 174.64443359375 | 70.45654296875 |
| Pubmed | NCNC | 11.633301165979356 ± 1.3760164712727816 | 2.6298323323950172 ± 0.680391229173743 | 542.853125 | 178.037109375 |
| Pubmed | NCNC + R-HSPE | 13.325316962227225 ± 0.2435800529046176 | 3.7329856202937663 ± 0.14197469368622917 | 857.02060546875 | 194.52783203125 |

| Dataset | Paired cost difference | Training seconds mean Δ ± SD | Test scoring seconds mean Δ ± SD | Training peak GPU MB mean Δ | Test peak GPU MB mean Δ |
|---|---|---:|---:|---:|---:|
| Cora | +R-HSPE − NCNC | -0.19175849119201302 ± 0.31310833835738866 | 0.0943378534168005 ± 0.040763264224624375 | 33.08359375 | 0.892578125 |
| Pubmed | +R-HSPE − NCNC | 1.6920157962478697 ± 1.536997878522019 | 1.1031532878987491 ± 0.7720223944370784 | 314.16748046875 | 16.49072265625 |

Feature-cache storage bytes and a cache-only latency breakdown: NOT REPORTED in the canonical result tables. Cache identities, hashes, pair counts and token counts are logged in run metadata. Runtime values are hardware/protocol measurements and should not be generalized to other systems.
