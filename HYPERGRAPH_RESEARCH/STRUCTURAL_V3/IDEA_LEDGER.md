# Structural innovation ledger — V3

| Candidate | State | Decision | Gate / reason |
|---|---|---|---|
| A — ARHC | Implemented; server unit tests passed (6/6); F0/F1 complete | REJECT | F1: raw 0.487678, symmetric 0.487579, role-only 0.487406, full 0.487407; A3 did not lead, so A4 was not run. |
| B — PMHE | Implemented; server unit tests passed (8/8); F0/F1 complete | REJECT | F1: raw 0.487678, mean 0.487893, second moment 0.487971, pair moment 0.487705; B3 missed both controls and gain threshold. |
| C — ARPM | Implemented; server unit tests passed (10/10); F0/F1/C4 complete | REJECT | F1: raw 0.487678, PMHE 0.487705, anchor mean 0.487655, ARPM 0.487629, shuffled-anchor 0.487465; C3 did not lead the primary controls. |

Maximum candidates: 3. A GO ends the search immediately. A/B/C F0/F1 test evaluation is disabled; F1 decisions use validation-best checkpoints. No fourth module follows three rejections.
