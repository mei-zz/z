# V8 Researcher–Critic–Experimentalist–Judge Debate

## Researcher

The LPShift data create a real input shift: training positives are dominated by common neighbors, while A test positives have CN zero and B test positives mostly have CN zero. DCDLP is substantially better than the official GCN and topology-only heuristics on several held-out comparisons. A plausible research question is whether a link predictor should separate stable node-feature evidence from topology statistics when the topology distribution changes.

This is a useful empirical problem statement, but it is not yet a new network-structure result. The current DCDLP Parent already contains a feature/residual branch, and a direct feature-cosine proxy is often as good as or better than DCDLP.

## Critic

### Alternative explanation 1: simple feature similarity explains the apparent gain

Feature cosine is high for positives and lower for negatives in both settings. On validation, the feature-cosine proxy obtains MRR `0.5270` in A versus DCDLP mean `0.5237`, and `0.5565` in B versus DCDLP mean `0.8740` (B remains dominated by AA/RA, so this proxy does not explain every B result). On frozen test, feature cosine is `0.5384` in A and `0.5428` in B, exceeding the DCDLP means `0.2352` and `0.4118`. It is therefore impossible to attribute the DCDLP result to a unique topological computation from these experiments.

Control: freeze a feature-only score, a topology-only score, and their parameter-matched learned combination before any further architecture work.

### Alternative explanation 2: protocol and optimization are not identical

Official GCN uses its original 100-epoch optimization, negative sampling, and no DCDLP target-mask path; DCDLP uses four epochs, message-graph-only negatives, and target masking. The DCDLP comparison is protocol-preserving with respect to the LPShift data, but not an identical-training-budget causal ablation. A performance difference can therefore include optimizer, masking, and training-schedule effects.

Control: run a no-new-structure matched-budget baseline matrix with identical optimizer, negative sampling, masking policy, and epoch budget, while retaining the official GCN as a separate reproduction baseline.

### Alternative explanation 3: candidate ties and split construction dominate the ranking change

Most negative candidates have CN zero. A and B therefore have large tie groups, and the positive CN distribution changes sharply between train, validation, and test. A model can appear to improve because it breaks ties using feature or degree information, not because it learns a new propagation state.

Control: report per-tie-group metrics and compare against deterministic feature, degree, and topology score combinations under the official average-rank evaluator.

### Alternative explanation 4: small hard subgroups are seed-sensitive

B validation CN-zero MRR is `0.2794 / 0.1028 / 0.0922` over only 2,002 positives, while all-validation MRR is `0.8795 / 0.8710 / 0.8715`. This is not a stable mechanism effect. A subgroup cannot be used to motivate a new module until its definition and effect survive matched repetitions.

Control: pre-register subgroup thresholds from train data, report all seeds, and require the subgroup effect to exceed execution and optimization variance.

## Experimentalist

The cheapest falsification sequence is:

1. Reuse the frozen LPShift artifacts and compare feature-cosine, CN/AA/RA, degree-product, and a parameter-matched fixed linear combination.
2. Equalize the training budget and masking/sampling policy for official GCN and DCDLP Parent.
3. Evaluate validation MRR and the already frozen test set across additional paired seeds.
4. Only if DCDLP retains an improvement over the feature-only and matched-protocol controls should a new state or propagation rule be designed.

This sequence is cheaper and more diagnostic than adding attention, gating, a loss term, or width to DCDLP.

## Judge

The benchmark adapter and the official data protocol are ready. The failure phenomenon is real, but the present evidence does not isolate a missing message-passing capability. A simple feature proxy can reproduce or exceed the observed DCDLP ranking on the frozen test sets, and B's hardest subgroup is not seed-stable.

**Judgment: `BENCHMARK_READY_NO_GAP`.**

V8 does not authorize a V9 architecture. If research continues, the next task should be a baseline/protocol control matrix for feature-vs-topology evidence under LPShift. That is an audit of the current explanation, not a new GNN proposal.
