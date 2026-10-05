# Attempt 008 — Source and protocol audit

- Training graph uses `train_pos` only.
- Candidate paths are restricted to short paths and are computed deterministically; test labels are not used for feature construction or Stage1 fitting.
- Stage1 controls: Base, DangerousControls, stratified ShuffledDisjoint, and same-width scalar Proxy.
