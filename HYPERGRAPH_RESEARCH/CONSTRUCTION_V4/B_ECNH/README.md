# Candidate B — ECNH

**Status:** rejected after Candidate A's rejection; novelty search and validation-only screen complete.

ECNH creates one deterministic edge-centered group for every target-masked observed edge with at least one common neighbor, caps selected common neighbors at 16 (lowest message-graph degree first), and retains all Raw stars. The raw ECNH proposals are canonicalized. B1/B2 controls are matched one-to-one to unique non-Raw ECNH additions so their added edge count and exact size multiset match B3 after deduplication.

The operator and downstream model components remained fixed. The five-epoch validation MRRs were B0=0.487677542, B1=0.487055545, B2=0.485338383, and B3=0.487562378. B3 was 0.000115164 below Raw, so it was rejected without 10-epoch confirmation or test evaluation. `remote_evidence/status.json` records the gate result.
