# Baseline and history audit

## Workspace and execution identity

- Local workspace folder basename: DCDLP-main; source root: E:\我的资料库\Documents\Downloads\DCDLP-main.
- The connected workspace-info service returned an MCP internal error. Identity was verified from the local folder name and the remote copy by SHA-256 equality of src/dcdlp/train.py, src/dcdlp/models/dcdlp.py, and HYPERGRAPH_RESEARCH/QTHS_V8_PAPER/experiment_v8.py.
- Remote project root: /home/zhoulihui/lchr_v2; its directory name differs, but its audited source hashes match the DCDLP-main workspace.
- Neither local nor remote copy has Git metadata. A branch cannot be created without inventing repository history; V12 isolates candidate code in experiment-local hooks and stores source and patch hashes. No evaluation/split file is edited.
- Server audit: Tesla V100-PCIE-16GB (16 GB), 40 CPU cores; idle GPU and no experiment process active. Server environment is offline and already has the Python environment.

## Frozen protocol / harness

- Dataset: Cora standard split, seed 0 in Stage 1; 5 fixed training epochs, fixed-final-epoch checkpoint, validation MRR primary; test evaluation disabled.
- Model: current DCDLP A5/raw hypergraph path unless an experiment-local decoder hook is registered.
- Training negatives: one per training positive (K=1), selected from the existing train-only candidate pool (M=20).
- Candidate pool source: HYPERGRAPH_RESEARCH/NEGATIVE_V6_1/strict_train_candidates_and_selections.npz. Recheck the frozen pool/split hashes before each run.
- Candidate pool hash from V10.1 frozen metadata: 3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba.
- Pool construction audit: sampled against only train positives / train message edges via TrainOnlyView; no validation or test identities enter training negative construction. Validation identities/candidates are used only by the fixed evaluator. Test labels/candidates remain unopened before LOCAL_GO.
- Existing evaluator: fixed ranking code under src/dcdlp/evaluation/ranking.py and src/dcdlp/evaluate.py; not modified.
- Metrics: MRR (gate), Hits@1/3/10, epoch/final validation curve, parameter count, runtime, peak GPU memory, split/pool/validation hashes, checkpoint SHA, and source/patch hashes.
- Stage 2/3 gates follow program.md; test access is gated behind Stage 3 LOCAL_GO.

## Historical findings

| Line | Verified finding | V12 consequence |
|---|---|---|
| LCHR / PCHR | LCHR one-epoch Cora screen: candidate-specific routing MRR 0.131696 vs global hypergraph 0.162793; below parameter-matched router 0.131830 and random Top-K 0.132367. PCHR is marked rejected in V3/V4 task history; no separate auditable metric row was found. | Do not revive candidate hyperedge routing / selection; keep PCHR metric uncertainty explicit. |
| V2 SSHC | Corrected 5-epoch A4 MRR 0.163446; only +0.000653 vs raw and below shuffled cohesion control 0.163983. | No hyperedge cohesion weighting. |
| V2 RAHC | True redundancy 0.162889; size control 0.163352 and shuffled redundancy 0.166308 were higher. | No redundancy weighting. |
| V2 HSA | Best true arm 0.164475, +0.001681 over raw and +0.001022 over shuffled control; missed +0.003 / +2% gate. | No auxiliary support-alignment rerun. |
| V3 ARHC | 5-epoch A3 0.487407 vs raw 0.487678; symmetric control also below raw. | No anchor/member operator variants. |
| V3 PMHE | 0.487705 vs raw 0.487678, but mean / second-moment controls were higher and gain gate failed. | No pair-moment hypergraph operator. |
| V3 ARPM | 0.487629 vs raw and below raw / moment / anchor-conditioned controls. | No anchor-conditioned pair-moment operator. |
| V4 ECPH | True component construction 0.488175 vs raw 0.487678 (+0.000497; +0.102%), below +0.001 screen; +39% runtime. | Do not subdivide ego stars into components. |
| V4 ECNH | 0.487562 vs raw 0.487678 (−0.000115). | Do not construct common-neighbor hyperedges. |
| V4 OWH | 0.485423 vs raw 0.487678 (−0.002255); 5.2x hyperedges and +139% runtime. | Do not add open-wedge hyperedges. |
| V5 GHHR | 0.493500 below raw, uniform-residual, and shuffled-difficulty controls. | Do not reweight HG residual by graph hardness. |
| V5 CVHNM | 0.532693 vs Graph-hard-only 0.533445; failed all-control gate. | Do not balance graph/HG hardness regions. |
| V5 DAF | 0.496903 vs raw 0.503012 (−0.006109). | No disagreement attention gate. |
| V6 HG-verified veto | Validation strong, but test A4 0.550652 vs shuffled veto A3 0.562830; causal false-negative veto did not transfer. | No false-negative HG veto mechanism claim. |
| V6.1 strict audit | Performance remained promising, but MECHANISM_SUPPORTED=NO; future-positive enrichment did not establish false-negative identification. | Separate predictive performance from the rejected mechanism. |
| V6.2 CODNS | Matched disagreement controls fail; M1−M3 = −0.001412 (2/3 wins), M1−M4 = −0.002760 (1/3). | Do not re-run cross-order disagreement sampling. |
| V7.1 AQTHS | QTHS remained a supported frozen baseline; AQTHS was rejected on Cora validation and test was not opened. | Keep QTHS25 only as a baseline. |
| V8 QTHS25 | Cora 5-seed test +0.017435 vs Graph-hard (4/5); PubMed +0.045911 (5/5); Citeseer neutral; SH75 is a strong control. | Use QTHS25 / SH75 as baselines, not a new contribution. |
| V9 RTHNL | With K=1, within-positive tail weighting is identical to Graph-hard; exact degeneracy. | No RTHNL or equivalent within-row weighting at K=1. |
| V10 CPTS | Reported gains vs Graph-hard were mixed against QTHS25, SH75 and Matched-Q; not a universal winner. | CPTS is a historical comparator, not assumed strongest. |
| V10.1 audit | Detector fires on 100% of real and null rows; CPTS vs shuffle and Matched-Q fail to validate local adaptivity. | No change-point/tail mechanism claim, fixed-percentile or SH75 micro-tuning. |
| Prior static-feature search | Ten structural feature candidates were screened; some rose on AUC/proxy metrics but lost on ranking or matched proxy controls. | MRR and mechanism controls take priority over proxy gains. |

## Current strong baselines

- QTHS25 is the strongest relevant frozen negative-sampling baseline for general non-sampling candidates; SH75 is a strong fixed-region control, while Graph-hard and CPTS remain diagnostics. V10.1 invalidates the CPTS adaptivity claim.
- The first exploratory 5-epoch batch used SH75+BCE and produced provisional F1/D1 screens. These are not treated as valid promotions against the strongest baseline. Both candidates were rechecked with the same QTHS25 training negatives for treatment, control and baseline in Stage 2.
- Stage 2 exact matched results on Cora seed 0, fixed epoch 10: QTHS25+BCE MRR 0.530263; F1 batch-top-ten pairwise MRR 0.235394 vs random-ten pairwise control 0.385148; D1 ego-context MRR 0.365654 vs node-permuted context control 0.521947. Both rejected; their large drop under the stronger sampler is logged as a sampler-dependent failure, not a universal claim.
- Stage 1B used a fresh QTHS25+BCE baseline, Cora seed 0, five epochs: baseline MRR 0.525620; F2 BCE-anchored batch-hard residual 0.523925 vs random-ten auxiliary control 0.515801; H1 train-edge-dropout consistency 0.523719 vs shuffled-pair control 0.525116. Both failed the registered effect/control gate and were rejected.
- Stage 1C tested graph/Raw-HG pair-representation orthogonal residual with three matched controls against a fresh QTHS25+BCE baseline: baseline 0.525620; orthogonal residual 0.523703; raw-feature MLP 0.527652; random orthogonal rotation 0.525538; projected same-dimension concatenation 0.524026. The proposed orthogonal residual was rejected because it lost to baseline and the raw-feature parameter-matched control.
- Stage 1D tested training-only persistent positive-difficulty weighting for five epochs: QTHS25+BCE baseline 0.525620; EMA candidate 0.525049; instantaneous-difficulty control 0.525049; shuffled-history control 0.525135. Reject persistent positive-history weighting; no held-out labels were used.
- Stage 1E tested same-pair Graph/Raw-HG multiplicative branch interaction against a parameter-matched self-moment control: baseline 0.525620; cross-view candidate 0.527739 (+0.002119); self-moment control 0.527742. Reject the specific cross-view product mechanism: below the registered effect gate and indistinguishable from the matched control.
- Stage 1F tested degree×residual and CN×residual bilinear decoder terms against a two-parameter branch-score calibration control: baseline 0.525620; candidate 0.526513 (+0.000892); calibration control 0.527789 (+0.002169). Reject the bilinear coactivation; the control is a subthreshold diagnostic signal and does not meet the gate.
- Stage 1G tested BCE-anchored local pairwise ranking between each train positive and its own QTHS25-selected negative: baseline 0.525620; identity-aligned candidate 0.506463 (−0.019158); cyclic mismatch control 0.505986. Reject both auxiliary pairwise arms; the extra ranking term sharply degraded MRR regardless of pair identity.
- Stage 1H tested parameter-light, target-masked exclusive-neighborhood cross-edge density: baseline 0.525620; raw cross-density candidate 0.527136 (+0.001515); within-side density control 0.524867. Candidate-control separation was +0.002268, but candidate gain missed both +0.003 and 1% gates. Reject unchanged D2. A single contrastive revision (cross minus within density) is screened in Stage 1I against the raw cross-density arm; it is not a parameter sweep.
- Stage 1I tested the contrastive revision: 0.525869 (+0.000249) vs cached baseline 0.525620 and raw cross-density control 0.527136 (−0.001266 vs control). The subtraction removed the subthreshold Stage 1H signal; reject D2R without coefficient tuning.
- Stage 1J tested raw endpoint input-feature cosine as a one-scalar decoder residual against same-parameter residual-score recalibration: candidate 0.526290 (+0.000669), control 0.525717 (+0.000097), baseline 0.525620. The candidate-control gap was +0.000573; both the effect and matched-control promotion gates failed. The cached baseline was accepted only after checking dataset, seed, epochs, sampler, selected-negative hash, train-pool hash, validation-candidate hash, and all non-runner project source hashes against Stage 1H.
- Subsequent Stage 1 screens use QTHS25+BCE directly. Historical 10-epoch scores do not replace fresh matched baselines.

## Integrity checks

No split, evaluator, ranking code, positive/negative evaluation candidate construction, or test file is changed. V12 hooks are isolated inside each runner process and restored on exit. The runner fails closed if source/pool/split hashes mismatch or evaluate_test is true.
