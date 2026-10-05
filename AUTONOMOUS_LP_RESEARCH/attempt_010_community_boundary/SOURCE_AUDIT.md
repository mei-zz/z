# Attempt 010 — Source and protocol audit

- Communities are inferred from `train_pos` only with a fixed seeded label-propagation procedure.
- No test labels, attention, gating, or extra model module is used in Stage1.
- Controls: Base, DangerousControls, stratified ShuffledCommunity, and same-width scalar Proxy.
