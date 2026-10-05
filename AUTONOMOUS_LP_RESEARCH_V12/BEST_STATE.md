# Best validated state

- Current status: STOPPED — NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH (all 14 ideas rejected across six mechanism families; no Phase 2).
- Innovation 1: none confirmed.
- Innovation 2: not applicable.
- Baseline: DCDLP A5 / Raw-HG, seed 0, Cora standard, fixed QTHS25 negative sampler and BCE, matched 5 epochs.
- Fresh validation MRR: 0.525620 (QTHS25+BCE, seed 0, five epochs).
- Phase 1: 39/40 Stage-1-equivalent model runs used; one equivalent remains unused because a complete candidate/control pair needs two arms. Total actual training jobs including five Stage 2 confirmations: 44.
- Test status: disabled; test labels/candidates unopened by V12.
- Candidate artifacts: experiment-local hooks only; no repository source/evaluation changes.
- Git: no .git directory exists locally or remotely; no branch/commit can truthfully be created. Source hashes and candidate patch files are the provenance record.

- Latest falsification: Stage 1H D2 scored 0.527136 MRR (+0.001515) against the 0.525620 baseline and 0.524867 within-side control. It beat its control by 0.002268, but missed the registered +0.003 / +1% promotion gate; no innovation is promoted.
- Stage 1I tested excess cross-closure density against the raw D2 arm using the exact same cached baseline, split, validation candidates, and selected negatives: candidate 0.525869 (+0.000249), raw-density control 0.527136. The contrast removed rather than explained the earlier subthreshold signal; reject it.
- Stage 1J tested raw endpoint-feature cosine: candidate 0.526290 (+0.000669) vs same-parameter score-rescaling control 0.525717 (+0.000573); neither clears the +0.003 / +1% gate.
- Stop condition: six orthogonal mechanism families were searched; no candidate survived formal promotion against fixed QTHS25. Provisional SH75-only F1/D1 signals failed matched confirmation, so no candidate entered Phase 2. Queue is complete, GPU idle, and test remains unopened.
