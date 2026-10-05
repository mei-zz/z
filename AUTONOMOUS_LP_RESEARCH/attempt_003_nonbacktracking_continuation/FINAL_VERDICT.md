# Attempt 003 — Final verdict

Candidate: Non-Backtracking Continuation Profile (NBCP)

Verdict: STOP / BLACKLIST.

The continuation-distribution object had adequate support and a small balanced feature-only AUC increment, but the signal did not transfer to the locked parent integration. TrueNB was below Parent and ShuffledNB on the main ranking metrics and below the simple Proxy on all metrics. This is an integration failure, not a reason to add architecture or tune the candidate.

Evidence:

- `raw_results/nb_stage0_stage1.json`
- `raw_results/nb_stage2.json`
- `STAGE0_SUPPORT.md`
- `STAGE1_PROBE.md`
- `STAGE2_SCREENING.md`

The exact non-backtracking continuation profile, including continuation-count concentration/dispersion over `u-a-b-c-v` paths, must not be retried under a renamed feature or decoder.
