# Candidate Ledger

## Rule

No candidate is allowed to become a model merely because it sounds different. The candidate must have: an observed Parent failure; a missing information object; a non-equivalent propagation rule; a proxy control; a collision audit; and a minimum validation-only falsification experiment.

## Ledger

| ID | Scenario | Candidate | Failure it would target | Collision / proxy risk | Decision |
|---|---|---|---|---|---|
| C-A1 | Incomplete/noisy | Uncertainty-aware topology denoising | Parent may propagate missing/spurious edges | PULL, CORE, LEAP; no compatible public data available remotely | NOT_EXECUTED |
| C-B1 | Inductive | New-node topology induction | Parent may have no training topology for test endpoints | GraphSAGE/NCN/LEAP and standard inductive protocols; no fixed data available remotely | NOT_EXECUTED |
| C-C1 | Hard negatives | Hard-negative-conditioned local pair reranker | Parent HL/LL subgroup weakness | CN/AA/RA, feature proxy, SEAL, NCN/NCNC; repeats PCDT/CDPT decoder pattern | STOP before implementation |

No candidate passed the gate. Therefore no “selected architecture” is being claimed, no new module was trained, and no rescue modification was attempted.

## Why no random fourth candidate was added

Adding attention, a gate, a loss term, a wider hidden state, or a larger neighborhood would not distinguish whether the current failure is information loss, optimization, or a stronger existing proxy. That would recreate the V1–V4 search pattern and violate the fixed budget.
