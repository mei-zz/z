# Paper evidence matrix

| Claim | Required evidence | Current status | File | Ready? |
|---|---|---|---|---|
| QTHS > Graph-hard on Cora | Frozen Cora test; paired seeds | PASS | 01_CORA_FULL_RESULTS.md / V7.1 | YES |
| QTHS generalizes to PubMed | 3-seed test mean and wins/3 | SUPPORTED | 01_PUBMED.md | YES |
| Citeseer behavior | paired seed deltas and 95% bootstrap CI | CITESEER_NEUTRAL: CI [-0.0222,+0.0198] | 02_CITESEER_STATISTICS.md | YES |
| QTHS > random veto | Cora frozen test paired comparison | PASS | 01_CORA_FULL_RESULTS.md / V7.1 | YES |
| QTHS > semi-hard | Cora SH75, 3 seed paired validation | QTHS25_NOT_ABOVE_SH75 | 05_SEMIHARD_CONTROL.md | YES |
| Backbone generalization | 3 encoders; 2/3 positive with 2/3 seed wins | YES | 03_BACKBONE_GENERALIZATION.md | YES |
| Zero parameter overhead | same backbone parameter-count audit | PASS | 06_EFFICIENCY.md | YES |
| Runtime overhead | selection/scoring/training timing and GPU memory | MEASURED | 06_EFFICIENCY.md | YES |
| Trim sensitivity | Cora seed0 five ratios and association | MEASURED | 04_TRIM_SENSITIVITY.md | YES |
| Novelty status | focused primary-source overlap check | EXACT_RULE_UNVERIFIED | 07_NOVELTY.md | PARTIAL |
