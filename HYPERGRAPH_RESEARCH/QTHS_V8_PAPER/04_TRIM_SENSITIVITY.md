# QTHS trim sensitivity

Cora seed 0 validation only. This is a sensitivity analysis, not a model-selection step; QTHS25 remains frozen as the main rule. Because the frozen V7.1 rule trims from a two-candidate prepool, alpha counts candidate occurrences (2N); effective replaced-positive fractions are capped at 100%.

| Nominal trim ratio | Effective runner-up fraction | Validation MRR | Mean selected Rg | p95 Rg | Extreme-hard fraction |
|---:|---:|---:|---:|---:|---:|
| 0% | 0.000 | 0.532759 | 1.000000 | 1.000000 | 1.0000 |
| 10% | 0.200 | 0.538266 | 0.989469 | 1.000000 | 0.7999 |
| 25% | 0.500 | 0.530263 | 0.973684 | 1.000000 | 0.5000 |
| 40% | 0.800 | 0.530898 | 0.957899 | 1.000000 | 0.2001 |
| 60% | 1.000 | 0.529140 | 0.947368 | 0.947368 | 0.0000 |

- Spearman(alpha, validation MRR): -0.8000.
- Spearman(mean selected Rg, validation MRR): 0.8000.
- Correlations are descriptive associations over five settings, not causal estimates.
