# V8 Failure Subgroup Analysis

## Predeclared subgroup rules

Subgroups were defined from the message graph and train-positive distribution before interpreting model results:

- CN low/high: train-positive CN quartiles.
- degree-product low/high: train-positive degree-product quartiles.
- high degree-gap: the 75th percentile of a deterministic first-100,000 train-positive prefix.
- feature-cosine low/high: train-positive cosine quartiles.
- CN-zero: exact `CN == 0`.

The same frozen thresholds were applied to validation and, only after freezing, to test. The exact thresholds are stored in both `raw/v8_failure_subgroups_2_1.json` and `raw/v8_failure_subgroups_2_4.json`. The subgroup analysis uses the official candidate order and average-rank tie convention: `0.5 * ((1 + #neg>pos) + (1 + #neg>=pos))`.

## Validation results across seeds

The most relevant groups are shown as MRR. Full Hits values and all groups are in the raw JSON files.

### Setting A

| Group | n | DCDLP seed 1/2/3 | GCN seed 1/2/3 |
|---|---:|---|---|
| all | 23,669 | `0.5255 / 0.5198 / 0.5258` | `0.0707 / 0.0696 / 0.0708` |
| CN zero | 13,423 | `0.2243 / 0.2155 / 0.2257` | `0.0599 / 0.0540 / 0.0548` |
| feature cosine low | 3,783 | `0.4133 / 0.4062 / 0.4095` | `0.0435 / 0.0435 / 0.0450` |
| feature cosine high | 1,491 | `0.6929 / 0.6744 / 0.6791` | `0.1380 / 0.1265 / 0.1314` |
| high degree-gap | 9,277 | `0.5014 / 0.4745 / 0.4871` | `0.0778 / 0.0756 / 0.0786` |

The A CN-zero subgroup is a real and reproducible hard case for DCDLP: MRR is about `0.22`, much lower than its all-validation MRR. However, a simple feature-cosine ranking proxy obtains validation MRR `0.5041` on this same group, so this is not evidence that a new message-passing mechanism is required.

### Setting B

| Group | n | DCDLP seed 1/2/3 | GCN seed 1/2/3 |
|---|---:|---|---|
| all | 24,097 | `0.8795 / 0.8710 / 0.8715` | `0.1170 / 0.1168 / 0.1140` |
| CN zero | 2,002 | `0.2794 / 0.1028 / 0.0922` | `0.0681 / 0.0688 / 0.0635` |
| feature cosine low | 4,013 | `0.8478 / 0.8448 / 0.8518` | `0.1008 / 0.0995 / 0.0971` |
| feature cosine high | 1,032 | `0.9325 / 0.8919 / 0.8909` | `0.1872 / 0.1807 / 0.1711` |
| high degree-gap | 10,113 | `0.8492 / 0.8291 / 0.8343` | `0.1132 / 0.1118 / 0.1104` |

The B CN-zero subgroup is not stable across model seeds. Its small size and large DCDLP variation make it unsuitable as a claimed structural failure without a further controlled study. The all-validation result is much more stable than this subgroup, but it is partly explained by the easy feature and heuristic separation.

## Frozen-test descriptive results

The test group was not used to create the rules. It is reported only to show how the validation findings transfer.

| Setting / test group | n | DCDLP MRR by seed | GCN MRR by seed | Feature-cosine proxy | RA proxy |
|---|---:|---|---|---:|---:|
| A all (= CN zero) | 9,048 | `0.2407 / 0.2278 / 0.2372` | `0.0576 / 0.0545 / 0.0524` | `0.5384` | `0.0079` |
| B all | 11,551 | `0.4867 / 0.3780 / 0.3706` | `0.0578 / 0.0577 / 0.0586` | `0.5428` | `0.3176` |
| B CN zero | 7,613 | `0.2643 / 0.1053 / 0.0946` | `0.0520 / 0.0525 / 0.0542` | `0.5305` | not used for decision |

The feature-cosine proxy is a direct warning against attributing the DCDLP result to a new structural computation: it exceeds the DCDLP mean on A test and also exceeds the DCDLP mean on B test. It uses no learned parameters and is computed from the same node features already present in the benchmark.

## Error localization conclusion

1. GCN is weak on both validation and test; it does not isolate the LPShift failure mechanism.
2. CN/AA/RA are strong when the validation positive distribution still contains common neighbors, but they collapse when positive CN collapses.
3. DCDLP is better than GCN and the topology-only heuristics on several held-out groups, especially A test, but its gain is not independent of a simple feature-cosine ranking signal.
4. The most reproducible observable failure is distribution shift plus candidate-score ties, not a demonstrated missing message-passing state.
5. No validation evidence here justifies adding a new GNN module. Any next study would first need a frozen, compute-matched test of feature-only and feature-plus-topology baselines, not an architectural rescue.
