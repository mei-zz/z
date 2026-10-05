# Attempt 001 — Source and protocol audit

- Data source: remote `/home/ubuntu/DCDLP-main/data/processed/cora_heart_seed{0..4}.npz`.
- Protocol: Cora HeaRT processed split; train graph contains training positives only.
- Training negatives: deterministic, sampled against the union of all positive edges with seed `10000 + seed`.
- Validation negatives: the first fixed official HeaRT negative candidate per validation positive, matching the prior feature-probe protocol.
- No test label or test metric is used in idea selection or feature construction.
- Variant controls: `Base`, `BasePlusL3`, `DangerousControls`, `TrueRole`, `ShuffledRole`.
- Shuffled null: role vectors are permuted within label-independent strata formed from rounded CN, L3, and log degree-product controls.
- Simple proxy: `DangerousControls` is the scalar proxy containing CN/AA/RA/degree/L3/Local Path/CH2-L3/CH3-L3.
- The candidate contains no trainable parameters and no architecture change.
