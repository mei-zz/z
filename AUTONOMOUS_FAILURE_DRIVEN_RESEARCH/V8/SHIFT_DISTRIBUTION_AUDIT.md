# V8 Shift Distribution Audit

## Protocol

All structural quantities are computed on the official LPShift message graph, not on a graph rebuilt from train positives. The audit includes endpoint degree, CN, Adamic–Adar, Resource Allocation, and node-feature cosine similarity. The test distribution is shown only as a frozen descriptive report; no model or subgroup decision used it.

Training-negative summaries reproduce the V8 DCDLP rule: uniform candidates forbidden only when their canonical edge is in the message graph. Held-out labels are not read by this sampler.

Artifacts:

- `raw/v8_shift_distribution_2_1.json`
- `raw/v8_shift_distribution_2_4.json`
- script: `scripts/audit_shift_distributions.py`

## Structural distribution summary

The table reports CN mean, CN median, CN zero fraction, AA mean, RA mean, and feature-cosine mean.

| Setting / group | CN mean | CN median | CN=0 | AA mean | RA mean | feature cosine |
|---|---:|---:|---:|---:|---:|---:|
| A train positive | 11.7676 | 5 | 0.0034 | 3.6060 | 0.5449 | 0.9570 |
| A sampled train negative | 0.0005 | 0 | 0.9996 | 0.0001 | 0.0000 | 0.8043 |
| A validation positive | 0.4329 | 0 | 0.5671 | 0.1521 | 0.0275 | 0.9586 |
| A validation negative | 0.0019 | 0 | 0.9985 | 0.0005 | 0.0000 | 0.8535 |
| A test positive | 0.0000 | 0 | 1.0000 | 0.0000 | 0.0000 | 0.9599 |
| A test negative | 0.0019 | 0 | 0.9985 | 0.0005 | 0.0000 | 0.8548 |
| B train positive | 15.5509 | 8 | 0.0011 | 4.5580 | 0.6206 | 0.9606 |
| B sampled train negative | 0.0004 | 0 | 0.9997 | 0.0001 | 0.0000 | 0.8044 |
| B validation positive | 1.7015 | 2 | 0.0831 | 0.6916 | 0.1529 | 0.9617 |
| B validation negative | 0.0023 | 0 | 0.9982 | 0.0006 | 0.0001 | 0.8556 |
| B test positive | 0.3409 | 0 | 0.6591 | 0.1307 | 0.0263 | 0.9623 |
| B test negative | 0.0022 | 0 | 0.9983 | 0.0005 | 0.0001 | 0.8578 |

## What the shift mechanism changes

1. Positive-edge CN collapses from a high-CN training distribution to a mostly zero-CN held-out distribution. The collapse is strongest in A, where every test positive has CN zero.
2. The negative candidates are almost always CN zero in every split. Therefore a rule that ranks mainly by CN can look strong on validation when positive CN remains nonzero, then fail when the positive CN distribution collapses.
3. Feature cosine is comparatively stable for positives (`0.9570–0.9623`) but much lower for negatives (`about 0.804–0.858`). This makes feature similarity a plausible easy signal and a confounder for any claim that a model is solving a purely topological shift.
4. B is less severe than A on validation but still shifts strongly by test: positive CN mean falls from `1.7015` to `0.3409`.
5. A single statistic cannot explain all changes. Degree, CN/AA/RA, feature similarity, candidate multiplicity, and the official negative construction move together to different degrees.

## Ranking ties and heuristic limits

CN/AA/RA produce many exact ties because most negative candidates have zero common-neighbor score. On A validation, `56.71%` of positives have CN zero and only two distinct CN values occur among validation positives in the retained tie diagnostic. On B, `8.31%` of validation positives have CN zero. The official ranking evaluator's tie handling must therefore be respected; top-k values for heuristics can remain flat after the first nonzero score group.

The fixed heuristic results show both the usefulness and the limitation of these statistics:

- A: RA validation MRR `0.4057` but test MRR `0.0079`.
- B: RA validation MRR `0.8866` and test MRR `0.3176`.

This is evidence of a real distribution shift, not evidence that CN/AA/RA alone identify the complete missing mechanism.

## Leakage audit conclusion

The shift audit reads held-out candidates only for descriptive validation/test summaries. DCDLP training negative sampling uses only message-edge exclusion. The test distributions were not used to choose a new structure. The remaining methodological difference is that the official GCN's original sampler/masking behavior differs from DCDLP's protocol-preserving runner, which is explicitly disclosed in the baseline report.
