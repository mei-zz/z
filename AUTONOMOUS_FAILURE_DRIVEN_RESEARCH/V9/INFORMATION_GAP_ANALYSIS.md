# V9 Information-Gap Analysis

## 1. Question and preregistered interpretation

The question was not whether DCDLP can score LPShift candidates. It was whether the observed behavior exposes a stable information bottleneck that requires a new interaction between node features and topology.

The analysis therefore tested four progressively stronger explanations:

- feature-only information is insufficient;
- topology-only information is insufficient;
- an interaction is needed beyond additive fusion;
- an ordinary parameter-matched MLP is insufficient.

The final decision is based on validation MRR and Hits under the frozen A/B settings and paired seeds 1–3. Test results are descriptive only.

## 2. Direct evidence

### Setting A

The deterministic feature-only cosine score obtains validation MRR `0.5270`, compared with DCDLP `0.5237±0.0034`. Its validation Hits@10 is `0.8352`, compared with DCDLP `0.7508±0.0008`. The feature MLP is close to DCDLP (`0.5228±0.0033`), while the parameter-matched fusion is lower (`0.5149±0.0110`).

On the validation CN-zero subgroup, FeatureCosine obtains `0.5041` MRR while DCDLP obtains approximately `0.2218` averaged over the three seeds. On the low-feature-cosine subgroup, neither the feature-only proxy nor DCDLP is strong, but the parameter-matched fusion does not provide a stable or uniquely superior solution.

### Setting B

The deterministic topology-only RA score obtains validation MRR `0.8866`, compared with DCDLP `0.8740±0.0048`. The parameter-matched fusion is lower at `0.8070±0.0193`; the feature-only proxy is `0.5565` and the topology MLP is unstable (`0.4992±0.1709`).

On the validation CN-zero subgroup, FeatureCosine obtains approximately `0.5357` averaged over seeds, while DCDLP obtains approximately `0.1581`. On the low-feature-cosine subgroup, RA remains strong and the learned fusion again does not become uniquely necessary.

The complete MRR, Hits@10/20/50/100, per-seed values, and frozen descriptive test values are in `FEATURE_TOPOLOGY_ABLATION.md` and `raw/v9_results_summary.json`.

## 3. Hypothesis-by-hypothesis decision

| Hypothesis | Evidence | Decision |
|---|---|---|
| H1: features alone cannot explain the ranking | FeatureCosine beats DCDLP on A validation and FeatureMLP is nearly equal; it also dominates DCDLP in the A CN-zero subgroup | Not supported |
| H2: topology alone cannot explain the ranking | RA beats DCDLP on B validation, although it fails badly on A test and B test; TopologyMLP is unstable | Not supported as a general claim |
| H3: feature–topology interaction is necessary | No setting shows a stable fusion gain over the strongest single-family proxy; LinearFusion is highly variable | Not supported |
| H4: extra ordinary capacity explains the previous DCDLP signal | ParameterMatchedFusion does not beat the strongest fixed proxy and does not produce a consistent gain | Not supported as the sole explanation, but no independent DCDLP mechanism remains |

The key point is not that one proxy wins every split. The key point is that no control family leaves a reproducible residual that specifically requires feature–topology interaction. A feature-only proxy dominates the A validation failure mode; a topology-only proxy dominates B validation; and the fusion controls do not add a stable improvement on top of them.

## 4. Stability and variance

- FeatureCosine and RA are deterministic on each frozen message graph, so their across-training-seed SD is zero.
- FeatureMLP is comparatively stable but never improves on the strongest deterministic proxy: A `0.5228±0.0033`, B `0.5543±0.0024`.
- TopologyMLP is unstable: A `0.1512±0.0607`, B `0.4992±0.1709`.
- LinearFusion is extremely seed-sensitive: A `0.2393±0.1986`, B `0.3036±0.2182`.
- ParamMatchedFusion is more stable than LinearFusion but remains below DCDLP in both validation settings and below the strongest simple proxy: A `0.5149±0.0110`, B `0.8070±0.0193`.

This pattern is inconsistent with a clean, independently useful interaction mechanism. It is more consistent with the dataset regimes being dominated by different simple signals and with the learned low-budget fusion being poorly conditioned.

## 5. Subgroup interpretation

The subgroup results do not justify a new model structure:

1. CN-zero candidates are not a unique DCDLP failure that needs a learned interaction. FeatureCosine already gives high validation MRR in both settings.
2. Low feature-cosine candidates are hard for the feature proxy, but topology or DCDLP can sometimes rank them better; this is a disagreement between observable proxies, not evidence that a new interaction is causally required.
3. A subgroup with low MRR is not automatically an information bottleneck. The control results show that candidate difficulty, distribution shift, and heuristic ties can create large differences without requiring a new message-passing rule.
4. No subgroup was selected from test performance. Subgroup thresholds were defined from training-positive statistics and applied to validation; test subgroup numbers were frozen descriptive output only.

## 6. Alternative explanations and limits

The following caveats prevent a stronger claim than `NO_INDEPENDENT_GAP`:

- The ten controls are engineered pair statistics, not a full learned raw-feature encoder. A future study could still ask whether a different feature representation adds information.
- The control target masking is necessarily weaker than DCDLP's full target-masked message encoder because the controls do not propagate node states.
- Only three paired training seeds were required for this V9 attribution audit.
- V8 had already inspected the same LPShift test outputs. V9 does not call them independent test evidence; the final choice uses validation only.
- The observed A/B regime dependence means no universal statement about all link-prediction datasets follows from this audit.

These limitations support a cautious closure of the current LPShift structure-search branch, not a request to add attention, gates, losses, width, or another unplanned module.

## 7. Researcher–Critic–Judge synthesis

**Researcher.** The strongest reproducible observation is that LPShift ranking is often already predictable from a single observable family: feature cosine in A and RA in B. A feature–topology interaction could still be useful in another benchmark, but this protocol has not exposed a necessity for it.

**Critic.** The apparent DCDLP signal could be confounded by target-masking differences, the limited statistic basis, training instability, candidate distribution shift, and the historically viewed test set. A parameter-matched ordinary fusion does not remove every confound, but it fails to produce the positive residual that would be needed to justify a new structure.

**Judge.** The validation evidence is sufficient to close the present LPShift information-gap claim. A new architecture would be speculative under the current evidence and would violate the V9 stopping rule.
