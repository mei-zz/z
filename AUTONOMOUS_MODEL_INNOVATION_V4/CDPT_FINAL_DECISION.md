# CDPT V4 — Final Decision

Date: 2026-09-16  
Locked decision rule: the rule in the V4 task specification was fixed before reading the formal aggregate.

## Decision

**MECHANISM_UNSUPPORTED**

The CDPT claim is terminated. The key mechanism is not established as an independent source of improvement on the formal Cora HeaRT comparison. No CDPT V3 structure, attention module, gate, auxiliary loss, or width increase is authorized as a rescue.

## Why the locked rule fires

The primary metric is validation MRR, evaluated in paired seeds 0–4:

| Contrast | C minus comparator, mean ± SD | Paired wins | 95% descriptive interval |
|---|---:|---:|---:|
| C − Early×Early (A) | −0.005620 ± 0.005115 | 0/5 | [−0.011971, 0.000731] |
| C − Late×Late (B) | +0.000463 ± 0.006030 | 3/5 | [−0.007024, 0.007950] |
| C − Concat MLP (D) | +0.004861 ± 0.007286 | 3/5 | [−0.004187, 0.013908] |
| C − Fixed Random (E) | −0.001909 ± 0.005731 | 2/5 | [−0.009025, 0.005207] |

The decisive observations are:

- CDPT loses to A in every validation seed.
- CDPT is effectively tied with B within the five-seed execution/seed variation.
- CDPT is below E, whose cross-depth operator has the same total parameter shape but is frozen and sampled once.
- CDPT’s advantage over D is not an isolated mechanism result: D has 33 fewer total parameters and is itself below A and B.

This satisfies the V4 case-B condition: the apparent benefit is reproducible by a single-depth alternative and is not improved by learning the cross-depth operator over a fixed random operator.

## Researcher / Critic / Judge

**Researcher.** C is above D by 0.004861 validation MRR on average and wins 3/5 paired seeds. The score path is active: its recorded nonzero fraction is 1.0 and the cross-depth operator is trainable. This shows that the implemented tensor path executes and can be optimized; it does not show that it is the useful causal mechanism.

**Critic.** A is stronger than C, so the early representation can be used without cross-depth interaction. E is at least as good as C on average, so a learned operator is not needed. B is close enough that the cross-depth claim has no reliable incremental effect. D’s small parameter mismatch weakens—but does not reverse—the conclusion because the stronger A and E controls already defeat C. Historical V3 original/resource reruns also showed up to 0.013950 test-MRR execution difference in the non-strict path; this is reported as a reproducibility boundary, not pooled with the formal result. Five seeds are not treated as strong significance evidence.

**Judge.** The direct mechanism claim is rejected. The remaining supported statement is narrower: in this implementation and budget, different depth-specific pair decoders have heterogeneous performance, and CDPT is not the preferred one on Cora.

## CiteSeer extension (not an independent test)

CiteSeer was already used in V3 and was therefore not eligible to be called a fresh independent test. The V4 five-seed extension nevertheless ran the same A–E controls. CDPT’s validation MRR was `0.148169 ± 0.009131`, versus A `0.146353 ± 0.011668`, B `0.142708 ± 0.010163`, D `0.141888 ± 0.009208`, and E `0.147675 ± 0.012396`. The paired C−E validation difference was `+0.000494 ± 0.006974`, with 3/5 wins and interval `[−0.008166, 0.009153]`; C test MRR was `0.131765`, below A at `0.140002`. This is a weak extension signal, not a mechanism confirmation, and it cannot override the Cora case-B result. No third benchmark was acquired because the locked Cora prerequisite failed.

## Reproducibility and protocol boundary

The strict same-configuration seed-0 repeat was bitwise identical for initialization, negative arrays, batch order, selected checkpoint, final RNG states, validation MRR, and test MRR when deterministic algorithms and `CUBLAS_WORKSPACE_CONFIG=:4096:8` were enabled. The formal five-seed batch used the locked non-strict mode, with all training negatives and permutations recorded per seed. All five models used the same masked graph, official HeaRT candidate arrays, four-epoch budget, and validation-only checkpoint selection. Test results are descriptive only.

The complete comparison and all Cora/CiteSeer metric tables are in `MECHANISM_COMPARISON.md`. The raw formal batch is `raw/mechanism_cora_v4run3/`; the CiteSeer extension is `raw/mechanism_citeseer_v4/`; the two aborted implementation batches are retained in `raw/failed_mechanism_cora_v4run1/` and `raw/failed_mechanism_cora_v4run2/` and are excluded from the Cora result.

## Answers to the final questions

- **Is CDPT worth continued structural investment?** No, not as the current mechanism claim.
- **What explains the observed signal?** The data support task-dependent depth choice and ordinary decoder capacity; they do not isolate learned cross-depth tensor interaction. Fixed random interaction and Early×Early are viable alternative explanations.
- **What remains uncertain?** The five-seed budget is modest and the non-strict path has an execution-noise boundary. CiteSeer gives a weak positive validation signal but its learned-vs-random difference is effectively zero and it was already used in V3; it cannot revive the failed Cora mechanism gate.
- **Was a new CDPT-backed structure innovation found?** No. The candidate is stopped and the next search is restarted separately in `NEXT_INNOVATION_SEARCH.md`.
