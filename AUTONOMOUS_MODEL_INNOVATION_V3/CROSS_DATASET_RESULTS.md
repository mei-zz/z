# CDPT Deepening V3 — Cross-Dataset Results

## Dataset and protocol audit

| Dataset | Protocol | Split/candidate source | Selection rule | Test used for selection |
|---|---|---|---|---|
| Cora | HeaRT | repository processed HeaRT split, seeds 0–4 | validation MRR | No in V3; historical V2 promotion used test metrics |
| CiteSeer | HeaRT | official repository HeaRT files, seed 0 | validation MRR | No |

CiteSeer was prepared from the repository's official HeaRT files, not self-generated random negatives. Both datasets use target-edge masking before node encoding and official difficult-negative candidates for validation and test.

## Cora summary

Across five paired seeds, CDPT has validation ΔMRR `+0.007241 ± 0.007760` versus Parent and test ΔMRR `+0.008956 ± 0.011544`. Late-only has validation ΔMRR `+0.005557 ± 0.004244` and test ΔMRR `+0.010922 ± 0.009535`. Fixed random has validation ΔMRR `+0.009384 ± 0.005849`, larger than CDPT on the validation metric used for decisions.

The Cora test values are retained for transparency but are not treated as an unbiased final estimate of V2's historical promotion because V2 inspected test metrics while choosing CDPT.

## CiteSeer seed 0

| Model | Validation MRR | Test MRR | Test Hits@10 | Test Hits@20 | Test Hits@50 | Test Hits@100 |
|---|---:|---:|---:|---:|---:|---:|
| B0 Parent | 0.140228 | 0.108796 | 0.285714 | 0.435165 | 0.657143 | 0.821978 |
| B1 CDPT | 0.145948 | 0.131765 | 0.338462 | 0.483516 | 0.694505 | 0.841758 |
| B2 Late-only | 0.132304 | 0.122422 | 0.340659 | 0.474725 | 0.663736 | 0.821978 |

Relative to Parent, CiteSeer test ΔMRR is `+0.022969` for CDPT and `+0.013626` for Late-only. Relative to Late-only, CDPT gains `+0.009344` test MRR, but loses `0.002198` Hits@10. This is positive independent evidence for CDPT's ranking score on one second dataset, not sufficient evidence for a general mechanism claim because it is one seed and one metric family still shows a control advantage.

The CiteSeer train-time shuffle control has test MRR `0.120901`, below aligned CDPT. The eval-time pair-alignment shuffle has test MRR `0.174799`, above aligned CDPT. The latter is a strong warning that the legacy shuffled control is not monotonic and should not be read as a clean causal intervention.

## Cross-dataset interpretation

| Question | Evidence | Assessment |
|---|---|---|
| Does CDPT beat Parent somewhere independently? | Yes: CiteSeer test MRR +0.022969; Cora validation mean +0.007241. | Supported |
| Does CDPT beat parameter-matched Late-only everywhere? | Cora test: no; CiteSeer test MRR: yes, Hits@10: no. | Not established |
| Does learning the operator beat a fixed random operator? | Cora validation: no; B4 is higher. CiteSeer B4 was not run. | Not established |
| Is the effect stable across datasets? | Positive MRR on both, but control ordering and Hits behavior differ. | Weak signal only |
