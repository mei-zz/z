# V6.1 False-Negative Enrichment

Future-positive labels were joined only after all training, candidate selection, validation gating, and test scoring completed. Rates below count candidate occurrences; unique-pair rates are also present in `enrichment_results.json`.

- True HG veto: 7/4488 = 0.00155971 (95% row-bootstrap CI [0.000445632798573975, 0.002896613190730838]).
- Shuffled veto, averaged across three seed-specific shuffles: 0.00074272.
- Random veto, averaged across three seed-specific draws: 0.00103981.
- Graph-hard prepool: 0.00089127.
- True veto / prepool enrichment: 1.7500000000000002 (95% row-bootstrap CI [1.2, 2.0]).
- True vs shuffled paired rate difference: 0.00081699, 95% CI [0.00014854426619132508, 0.0016339869281045752]; OR=1.958, CI [1.286000987528471, 3.0033470936070517]; seed-0 Fisher p=0.774263.
- True vs random paired rate difference: 0.00051990, 95% CI [-7.427213309566254e-05, 0.0012626262626262625]; OR=1.452, CI [0.918099353270804, 2.2197008291970524]; seed-0 Fisher p=0.343476.
- Mechanism support requires both paired bootstrap comparisons to exclude zero and both seed-0 Fisher tests to have p<0.05. Fisher tests are non-significant here, so the higher point estimates are not treated as confirmed enrichment.
- Q1 (Graph-hard/HG-high) vs Q2 (Graph-hard/HG-low): rates 0.00155971 vs 0.00022282; RR=7.000000000000001; absolute difference=0.00133690.
- HG percentile monotonicity: True; bucket rates=[0.0, 0.0, 0.0, 0.0, 0.004454342984409799].
- FILTERED_ALL_POSITIVE future-positive pool occurrences: 0/89760 (structurally forced to zero).

See `HG_PERCENTILE_VS_FUTURE_POSITIVE.csv` for publication-ready bucket counts and intervals.
