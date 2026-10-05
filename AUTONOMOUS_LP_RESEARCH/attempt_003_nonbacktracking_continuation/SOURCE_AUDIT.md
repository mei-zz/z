# Attempt 003 — Source and protocol audit

- Training graph only; no held-out positives enter the adjacency.
- Train negatives are deterministic and exclude all positives.
- Validation uses the first fixed official negative candidate per positive.
- Base controls are CN/AA/RA/degree/L3/Local Path/CH2-L3/CH3-L3.
- TrueNB, stratified ShuffledNB and scalar Proxy are compared by logistic regression before any model integration.
