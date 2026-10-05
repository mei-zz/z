# Attempt 005 — Source and protocol audit

- Data source: remote `/home/ubuntu/DCDLP-main/data/processed/cora_heart_seed{0..4}.npz`.
- Training graph contains `train_pos` only.
- Stage0 support is descriptive after the candidate was fixed; Stage1 idea selection uses train/validation pairs only.
- Controls: Base, DangerousControls, stratified ShuffledExpand, and the same-width scalar Proxy.
- No edge count between exclusive neighborhoods, maximum matching, attention, gate, extra depth, or loss change is included.
