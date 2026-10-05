# V2-002 CDPT — Stage 0 audit

- Parent equivalence with cross-depth scale set to zero: max logit error `0.0`.
- Exchange symmetry error: `0.0`.
- Finite output: yes; six cross-depth parameter tensors received nonzero gradients in the toy audit.
- Cora HeaRT seed 0, 8192 candidates: Parent 112,486 parameters and 42.99 MB peak GPU memory; CDPT 119,751 parameters and 46.75 MB peak GPU memory.
- Candidate/Parent parameter ratio: `1.0646`; forward-time ratio: `1.0812`; peak memory delta: `+3.75 MB`.
- Leakage audit: early and late states use the same target-edge-masked message graph as Parent; no valid/test labels or candidates are used during fitting.

Static verdict: PASS. The exact structure is retained in `scripts/candidate_models.py`.
