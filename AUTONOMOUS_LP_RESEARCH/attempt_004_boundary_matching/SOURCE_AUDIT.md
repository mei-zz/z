# Attempt 004 — Source and protocol audit

- Data source: remote `/home/ubuntu/DCDLP-main/data/processed/cora_heart_seed{0..4}.npz`.
- Training graph: `train_pos` only; no validation/test positives enter adjacency construction.
- Stage0 support uses official test pair lists only to measure coverage after the idea was fixed; no test labels are used to define the object or tune the probe.
- Stage1 uses deterministic train negatives and the first fixed official validation negative per positive.
- Controls: Base degree/CN/AA/RA and L3 scalars, DangerousControls with the full locked scalar set, stratified ShuffledMatch, and a same-width scalar Proxy.
- The new object is an eight-dimensional matching/deficiency profile. It excludes raw cross-boundary edge count to keep CECG blacklisted.
