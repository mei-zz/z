# LCHR final decision

```text
STATUS: EXECUTED
CANDIDATE: LCHR — Link-Conditioned Hyperedge Routing
SERVER: remote experiment completed
DECISION: REJECT
TARGETED_REVISION: none
NEXT_EXPECTED_STEP: Stop LCHR and return evidence for designing the next hypergraph-link-prediction candidate.
```

B4 validation MRR is 0.131696, below B3 at 0.131830 and B2 at 0.132367. It is also below B1 at 0.162793. This meets the predefined rejection criteria R1 and R2, so no targeted revision or three-seed confirmation was run. Routing weights vary by candidate (mean positive-pair cosine 0.00645), but this selectivity does not improve validation MRR.

The evidence is one seed and one epoch. It is sufficient for the requested fast falsification screen, not for a final benchmark claim.
