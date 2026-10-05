# Final Verdict — Attempt 001

## Candidate

`R1-07 Neighbor-Role Transition Matrix`

## Verdict

**STOP**

## Evidence

- Stage0 support passed on five Cora HeaRT seeds.
- Stage1 balanced train/validation probe passed against dangerous scalar controls and a stratified shuffled null.
- Stage2 failed on the locked real benchmark screening: TrueRole was below Parent in mean AUC, below the same-width Proxy, and not above ShuffledRole.
- The candidate showed a sharp seed-dependent collapse, with seed 2 AUC `0.47078` versus Parent `0.68058`.

## Failure reason

The degree-shell role-transition object has a feature-only signal under a balanced validation probe, but the signal does not transfer to official 500-negative ranking when integrated into the minimal parent decoder. It is not a validated link-prediction innovation under this protocol.

## Action

The exact mechanism is blacklisted in `BLACKLIST.md`. Raw code and results are retained in this directory. No attention, gate, extra loss, larger model, or hyperparameter rescue was attempted.
