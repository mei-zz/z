# Attempt 009 — Source and protocol audit

- Training graph uses `train_pos` only.
- Internal exclusive-neighborhood edges are counted only within each endpoint's own side; cross-boundary edges remain excluded.
- Stage1 uses Base, DangerousControls, stratified ShuffledCohesion, and same-width Proxy.
