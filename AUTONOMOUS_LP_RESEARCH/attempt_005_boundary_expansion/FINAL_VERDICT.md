# Attempt 005 — Final verdict

Candidate: Boundary Expansion Deficit (BED)

Verdict: STOP / weak mixed Stage2 result.

BED passed Stage1 strongly, but the parent integration did not produce a robust ranking win. It improves aggregate AUC and Hits@50/100, yet loses on MRR and Hits@10 versus Parent, loses to Proxy on four ranking metrics, and collapses on seed 0. The single-dataset result cannot satisfy the requested GO threshold. The exact two-sided frontier-growth/overlap profile is blacklisted and must not be rescued by architecture changes or tuning.
