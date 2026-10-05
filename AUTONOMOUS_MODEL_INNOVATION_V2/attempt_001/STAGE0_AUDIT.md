# V2-001 PCDT — Stage 0 audit

- Parent equivalence with transport scale set to zero: max logit error `0.0`.
- Exchange symmetry error: `0.0`.
- Finite output: yes; transport parameters received nonzero gradients.
- Cora HeaRT seed 0, 8192 candidates: Parent 112,486 parameters and 43.22 MB peak GPU memory; PCDT 177,512 parameters and 631.13 MB peak GPU memory.
- Candidate/Parent parameter ratio: `1.5781`; forward-time ratio: `0.9659` in this measurement; peak memory delta: `+587.91 MB`.
- Leakage audit: transport uses the train graph only and removes the candidate edge itself; valid/test positives are not inserted into message passing.

Static verdict: PASS. Stage 1 control verdict: STOP, recorded in `STAGE1_FAILURE.md`.
