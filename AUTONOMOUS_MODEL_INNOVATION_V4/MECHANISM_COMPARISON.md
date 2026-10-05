# CDPT V4 — Mechanism Comparison

Date: 2026-09-16  
Primary decision metric: validation MRR  
Dataset: Cora HeaRT  
Formal batch: `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_cora_v4run3/`

## Locked comparison

All five models use the same two-layer GCN encoder, target-edge masking, candidate edges, uniform training-negative protocol, four training epochs, optimizer, batch size, seeds 0–4, and fixed HeaRT evaluation candidates. Checkpoints are selected by validation MRR. Test MRR is reported only after selection and was not used to choose a model, structure, seed, or direction.

| ID | Mechanism | Total parameters | Trainable parameters | Runtime mean (s) | Peak GPU mean (MB) |
|---|---|---:|---:|---:|---:|
| A | Early × Early | 119,751 | 119,751 | 173.395 | 58.363 |
| B | Late × Late | 119,751 | 119,751 | 173.379 | 59.303 |
| C | Early × Late (CDPT) | 119,751 | 119,751 | 173.446 | 59.303 |
| D | Early + Late Concat MLP | 119,718 | 119,718 | 174.064 | 59.341 |
| E | Early × Fixed Random × Late | 119,751 | 118,727 | 165.335 | 59.294 |

D is 33 parameters below the tensor models. E has the same total parameter shape but its 1,024-parameter random operator is frozen. The fixed random operator is sampled once at model construction and is not resampled during evaluation.

## Cora per-seed MRR

These are the complete paired values used by the aggregate; seed 1 is retained.

| Seed | A val | B val | C val | D val | E val | A test | B test | C test | D test | E test |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.109144 | 0.102946 | 0.108074 | 0.099213 | 0.103463 | 0.117642 | 0.107618 | 0.095360 | 0.103863 | 0.096271 |
| 1 | 0.123529 | 0.108194 | 0.109233 | 0.111796 | 0.113321 | 0.111905 | 0.113924 | 0.107407 | 0.102187 | 0.102858 |
| 2 | 0.108305 | 0.097084 | 0.104519 | 0.089358 | 0.102896 | 0.113630 | 0.113242 | 0.114523 | 0.097743 | 0.104843 |
| 3 | 0.102785 | 0.102541 | 0.097153 | 0.093335 | 0.098492 | 0.109583 | 0.105795 | 0.100285 | 0.082425 | 0.106430 |
| 4 | 0.103521 | 0.106106 | 0.100206 | 0.101181 | 0.110560 | 0.104152 | 0.108455 | 0.102758 | 0.104236 | 0.108790 |

## Cora aggregate metrics

Values are mean ± sample SD over five seeds.

| Model | Validation MRR | Validation H@10 | Validation H@20 | Validation H@50 | Validation H@100 | Test MRR | Test H@10 | Test H@20 | Test H@50 | Test H@100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0.109457 ± 0.008355 | 0.260076 ± 0.012203 | 0.387072 ± 0.028882 | 0.603802 ± 0.044699 | 0.771863 ± 0.044505 | 0.111382 ± 0.005001 | 0.267173 ± 0.013105 | 0.390133 ± 0.021325 | 0.604934 ± 0.034741 | 0.778368 ± 0.040150 |
| B | 0.103374 ± 0.004217 | 0.261597 ± 0.004958 | 0.379468 ± 0.010888 | 0.597719 ± 0.039551 | 0.771863 ± 0.020476 | 0.109807 ± 0.003587 | 0.257306 ± 0.017422 | 0.386717 ± 0.019647 | 0.593548 ± 0.031905 | 0.772676 ± 0.030134 |
| C | 0.103837 ± 0.005133 | 0.260837 ± 0.021272 | 0.384030 ± 0.025788 | 0.594677 ± 0.038739 | 0.768821 ± 0.029624 | 0.104067 ± 0.007286 | 0.253510 ± 0.020419 | 0.374194 ± 0.019509 | 0.574194 ± 0.042358 | 0.763188 ± 0.039699 |
| D | 0.098977 ± 0.008568 | 0.245627 ± 0.020227 | 0.359696 ± 0.035117 | 0.520913 ± 0.065140 | 0.717110 ± 0.088300 | 0.098091 ± 0.009129 | 0.231879 ± 0.016780 | 0.343454 ± 0.029549 | 0.541556 ± 0.076640 | 0.722201 ± 0.084377 |
| E | 0.105747 ± 0.006052 | 0.259316 ± 0.019830 | 0.368061 ± 0.016661 | 0.562738 ± 0.050443 | 0.731559 ± 0.049474 | 0.103838 ± 0.004756 | 0.234535 ± 0.016575 | 0.358634 ± 0.019398 | 0.544213 ± 0.046177 | 0.737381 ± 0.050962 |

## Paired mechanism tests

Each row is C minus the named comparator, computed within the same seed. The interval is the five-seed t-based 95% interval with df=4; it is descriptive, not a claim of strong statistical significance.

| Contrast | Validation ΔMRR mean ± SD | Validation 95% interval | Validation wins | Test ΔMRR mean ± SD | Test 95% interval | Test wins |
|---|---:|---:|---:|---:|---:|---:|
| C − A | −0.005620 ± 0.005115 | [−0.011971, 0.000731] | 0/5 | −0.007316 ± 0.009196 | [−0.018735, 0.004103] | 1/5 |
| C − B | +0.000463 ± 0.006030 | [−0.007024, 0.007950] | 3/5 | −0.005740 ± 0.004807 | [−0.011709, 0.000229] | 1/5 |
| C − D | +0.004861 ± 0.007286 | [−0.004187, 0.013908] | 3/5 | +0.005976 ± 0.011443 | [−0.008232, 0.020184] | 3/5 |
| C − E | −0.001909 ± 0.005731 | [−0.009025, 0.005207] | 2/5 | +0.000228 ± 0.006876 | [−0.008309, 0.008766] | 2/5 |

The primary result is not a CDPT win: C loses to A in all five validation seeds, is effectively tied with B within the observed seed variation, and loses to E on average. C is better than the under-sized D on average, but that comparison does not isolate cross-depth interaction because A and E already provide stronger alternatives.

## CiteSeer extension evidence

CiteSeer was already used in V3, so this section is an extension validation, not a fresh independent test. It was run after the Cora mechanism gate had already failed, and it was not used to choose a structure, hyperparameter, or next direction. The official HeaRT data hash is `93b2480b3b56`; all five manifests agree on it.

| Seed | A val | B val | C val | D val | E val |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.148615 | 0.136771 | 0.151188 | 0.140781 | 0.152375 |
| 1 | 0.151055 | 0.159915 | 0.145983 | 0.134899 | 0.137931 |
| 2 | 0.136544 | 0.140378 | 0.151226 | 0.147936 | 0.161693 |
| 3 | 0.133335 | 0.133968 | 0.133920 | 0.131725 | 0.131767 |
| 4 | 0.162216 | 0.142509 | 0.158526 | 0.154102 | 0.154608 |

| Model | Validation MRR | Validation H@10 | Validation H@20 | Validation H@50 | Validation H@100 | Test MRR | Test H@10 | Test H@20 | Test H@50 | Test H@100 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0.146353 ± 0.011668 | 0.298678 ± 0.022333 | 0.433480 ± 0.026542 | 0.630837 ± 0.019303 | 0.814978 ± 0.006965 | 0.140002 ± 0.006225 | 0.343736 ± 0.019072 | 0.484396 ± 0.023290 | 0.695824 ± 0.018817 | 0.833407 ± 0.015416 |
| B | 0.142708 ± 0.010163 | 0.279295 ± 0.016659 | 0.400881 ± 0.011231 | 0.611454 ± 0.028104 | 0.783260 ± 0.025573 | 0.123145 ± 0.011211 | 0.312088 ± 0.016373 | 0.461538 ± 0.020441 | 0.679560 ± 0.013672 | 0.819341 ± 0.011142 |
| C | 0.148169 ± 0.009131 | 0.296916 ± 0.023017 | 0.426432 ± 0.027757 | 0.612335 ± 0.031305 | 0.778855 ± 0.015068 | 0.131765 ± 0.006391 | 0.322637 ± 0.021274 | 0.455824 ± 0.024256 | 0.669890 ± 0.033598 | 0.815824 ± 0.018995 |
| D | 0.141888 ± 0.009208 | 0.281938 ± 0.021805 | 0.411454 ± 0.024249 | 0.611454 ± 0.022763 | 0.786784 ± 0.022376 | 0.115703 ± 0.009401 | 0.281758 ± 0.021331 | 0.425934 ± 0.021103 | 0.652308 ± 0.019248 | 0.814945 ± 0.021945 |
| E | 0.147675 ± 0.012396 | 0.289868 ± 0.020043 | 0.433480 ± 0.026358 | 0.620264 ± 0.025950 | 0.794714 ± 0.030297 | 0.130787 ± 0.009823 | 0.324835 ± 0.013223 | 0.464615 ± 0.026171 | 0.673846 ± 0.035629 | 0.819780 ± 0.016225 |

| Contrast | Validation ΔMRR mean ± SD | Validation 95% interval | Validation wins | Test ΔMRR mean ± SD | Test 95% interval | Test wins |
|---|---:|---:|---:|---:|---:|---:|
| C − A | +0.001815 ± 0.007833 | [−0.007910, 0.011541] | 3/5 | −0.008237 ± 0.011709 | [−0.022775, 0.006301] | 1/5 |
| C − B | +0.005460 ± 0.012521 | [−0.010086, 0.021007] | 3/5 | +0.008620 ± 0.010927 | [−0.004948, 0.022188] | 3/5 |
| C − D | +0.006280 ± 0.004159 | [0.001116, 0.011444] | 5/5 | +0.016062 ± 0.013242 | [−0.000380, 0.032505] | 4/5 |
| C − E | +0.000494 ± 0.006974 | [−0.008166, 0.009153] | 3/5 | +0.000978 ± 0.008992 | [−0.010187, 0.012144] | 4/5 |

CiteSeer therefore provides a weak positive validation signal against A/B/D, but the C−E difference is near zero with an interval crossing zero, and C does not beat A on test MRR. Because CiteSeer was used in V3 and Cora already triggered case B, this is extension evidence, not confirmation of an independent CDPT mechanism.

## Direct answers to the mechanism questions

1. **Does Early contain information that Late cannot replace?** The result supports this as a task-level statement: A exceeds B by 0.006083 validation MRR on average (not a proof about representation mutual information). It does not show that Early–Late interaction is useful.
2. **Is cross-depth computation better than single-depth computation?** No. C does not beat A and only exceeds B by 0.000463 with a confidence interval crossing zero.
3. **Is tensor interaction better than ordinary concatenation?** C exceeds D by 0.004861 validation MRR, but D has 33 fewer parameters and is weaker than A/B. This is insufficient to attribute a main gain to tensor interaction.
4. **Is the learned operator better than a frozen random operator?** No. C is below E by 0.001909 validation MRR and wins only 2/5 paired seeds.
5. **Is the gap larger than execution noise?** The strict same-configuration repeat was bitwise identical for initialization, negative arrays, batch order, checkpoint, RNG state, validation MRR, and test MRR. Thus the Cora paired differences are not explained by non-determinism in that strict probe. The historical non-strict V3 resource rerun had up to 0.013950 test-MRR difference, so the non-strict run-to-run boundary remains reported separately.
6. **Direct evidence versus inference:** The paired metric outcomes, equal candidate hashes, parameter counts, score-path nonzero fraction, trainability flags, and strict repeat are direct evidence. Claims about “information” and why one depth helps are inferences and are not presented as established mechanisms.

## Path and integrity notes

- Formal JSON/checkpoints/manifests/logs: `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_cora_v4run3/`.
- CiteSeer extension JSON/checkpoints/manifests/logs: `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_citeseer_v4/`.
- CiteSeer aggregate: `AUTONOMOUS_MODEL_INNOVATION_V4/raw/mechanism_citeseer_v4/citeseer_v4_summary.json`.
- Aggregation code: `AUTONOMOUS_MODEL_INNOVATION_V4/scripts/aggregate_v4.py`.
- Failed first and second batches are retained under `raw/failed_mechanism_cora_v4run1/` and `raw/failed_mechanism_cora_v4run2/`; they are excluded from every table above.
- Cora data hash: `98e4aaaf07d4`.
