# V9 Final Decision

## Decision

**NO_INDEPENDENT_GAP**

## What was tested

V9 kept the V8 LPShift protocol and hashes fixed and compared the original DCDLP Parent against:

- deterministic FeatureCosine;
- deterministic TopologyRA;
- FeatureMLP;
- TopologyMLP;
- a linear feature/topology fusion;
- a parameter-matched ordinary MLP fusion.

All learned controls used paired seeds 1–3, the same four-epoch budget, optimizer, batch size, negative-sampling schedule, and training-order hashes as the V8 DCDLP runs. Validation MRR was the decision metric. No V9 choice used test MRR or test Hits.

## Why the independent-gap claim failed

1. In setting A, FeatureCosine alone gives validation MRR `0.5270`, above DCDLP `0.5237±0.0034`; it also gives much stronger validation Hits@10 (`0.8352` vs `0.7508`).
2. In setting B, TopologyRA alone gives validation MRR `0.8866`, above DCDLP `0.8740±0.0048`.
3. The parameter-matched fusion does not recover a stable advantage: A `0.5149±0.0110`, B `0.8070±0.0193`.
4. The learned linear fusion is unstable rather than mechanistically informative: A `0.2393±0.1986`, B `0.3036±0.2182`.
5. FeatureMLP is close to the deterministic feature proxy but does not improve it; TopologyMLP is high-variance and does not outperform RA where RA is strong.
6. Validation subgroup results, including CN-zero candidates, are already explained by simple proxies. No subgroup shows a stable residual advantage unique to DCDLP or to feature–topology fusion.

Therefore the current evidence does not support the statement that DCDLP's LPShift behavior requires an independent feature–topology interaction. It also does not support designing a V10 module to rescue this claim.

## What this decision does and does not mean

This is not a theorem that no feature–topology architecture can ever help link prediction. It means that the frozen LPShift A/B validation environment, the tested candidate statistics, and the paired controls do not reveal a defensible structural information gap. The residual differences in encoder target masking and representation basis are documented in `MATCHED_PROTOCOL_RESULTS.md`; they are limitations, not positive evidence.

The historical V8 test values are retained for auditability but are not treated as independent confirmation because that test behavior had already been viewed during V8. The decision is validation-based.

## Research action

Close the current LPShift feature–topology structure-search branch. Do not add attention, gates, a new loss, extra width, or another fusion module merely to manufacture a positive result. Preserve the raw JSON, prediction paths, logs, data hashes, and scripts for reproducibility.

If research continues, it must begin with a newly preregistered problem setting or an actually independent benchmark and a new failure audit. It must not reuse the present control failure as a reason to rename or extend DCDLP.

## Deliverables

- [FEATURE_TOPOLOGY_ABLATION.md](FEATURE_TOPOLOGY_ABLATION.md)
- [MATCHED_PROTOCOL_RESULTS.md](MATCHED_PROTOCOL_RESULTS.md)
- [INFORMATION_GAP_ANALYSIS.md](INFORMATION_GAP_ANALYSIS.md)
- [V9 raw aggregate](raw/v9_results_summary.json)
- [V9 control runner](scripts/run_feature_topology_controls.py)
- [V9 subgroup analyzer](scripts/analyze_v9_subgroups.py)

The result is a legitimate negative attribution result: the benchmark protocol is usable, the controls are reproducible, and no independent information gap was found under the stated V9 scope.
