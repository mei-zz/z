# Attempt 006 — Source and protocol audit

- Training graph uses `train_pos` only.
- The role alignment profile is computed from endpoint-internal neighborhood statistics; no test positives enter adjacency construction.
- Stage1 uses Base, DangerousControls, stratified ShuffledAlign, and same-width scalar Proxy.
- The candidate is rejected if it is supported only by a single seed or if AUC/AP do not both beat the controls.
