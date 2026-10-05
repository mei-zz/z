# Attempt 002 — Source and protocol audit

- Source: remote `/home/ubuntu/DCDLP-main/data/processed/cora_heart_seed{0..4}.npz`.
- Training graph: `train_pos` only; no validation or test positive is inserted into the structural decomposition.
- Train negatives: deterministic uniform negatives excluding all positives.
- Validation probe: fixed first official negative candidate per validation positive, matching the prior feature-probe protocol.
- Controls: Base scalar controls, TrueRoute, stratified ShuffledRoute, and scalar Proxy.
- The route index is computed once per seed; pair extraction is deterministic.
