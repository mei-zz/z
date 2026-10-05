# Attempt 007 — Source and protocol audit

- Spectral basis is computed from `train_pos` only for each seed.
- The candidate is fixed-dimensional and deterministic; no test labels, learnable spectral filter, attention, gate, or extra loss is used.
- Stage1 compares Base, DangerousControls, TrueSpectral, ShuffledSpectral, and same-width scalar Proxy.
