# Limitations and claim boundaries

- Citeseer transfer is not supported: validation mean ΔMRR −0.027379, median −0.031435, 0/3. The predeclared gate stopped evaluation; no Citeseer test result exists.
- V17.3 NCN/NCNC use 100 epochs and best-validation checkpoints; V17.4 uses 10 epochs and the final checkpoint. Do not combine absolute scores in one ranking.
- Positive plug-in evidence covers Cora and PubMed under this protocol, not universal transfer.
- NULL75 does not account for the observed gains, but this control does not isolate causal contribution of each statistic.
- Mechanism remains CONTEXT_DRIVEN; hyperedge-size causality is NOT_SUPPORTED.
- Evaluation uses 20 negatives per query, not all-node ranking.
- The recorded Cora raw-data directory is incomplete; both runs share the same hash-identified processed input and exact split. Archive the canonical upstream raw source/preprocessing recipe for public reproduction.
