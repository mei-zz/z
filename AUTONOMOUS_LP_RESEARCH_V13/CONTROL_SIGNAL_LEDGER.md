# Control-derived signal ledger

All values below come from completed V12 Cora seed-0 five-epoch QTHS25 runs, except where explicitly stated. Frozen baseline MRR is 0.5256204671690727. Positive deltas are exploratory weak primitives only; none satisfies the registered Stage-1 promotion gate.

| Primitive | V12 arm | MRR | Δ baseline | Params | Runtime (s) | Independent information source | V12 matched treatment/control | Status |
|---|---|---:|---:|---:|---:|---|---|---|
| P1 raw-HG pair representation | S1C_X1_RAW | 0.5276520613 | +0.002032 | 24944 | 132.59 | 24-dimensional pair evidence from Raw-HG branch score representations; independent higher-order view | X1 orthogonalized candidate 0.523703; random rotation 0.525538; fixed projected concat 0.524026 | WEAK_PRIMITIVE; control-sourced |
| P2 within-view self-moment | S1E_X2_SELF | 0.5277424882 | +0.002122 | 25136 | 84.41 | Within-view second/self moments from branch pair states | X2 cross-view product 0.527739 | WEAK_PRIMITIVE; mechanism contrast is null |
| P3 structural scalar calibration | S1F_B2_SCALE | 0.5277890892 | +0.002169 | 24737 | 66.29 | Two train-structure score channels: degree and common-neighbor branch scores | B2 coactivation candidate 0.526513 | WEAK_PRIMITIVE; strongest weak control |
| P4 target-masked cross-neighborhood density | S1H_D2 | 0.5271357171 | +0.001515 | 24736 | 64.93 | Cross-edge density between exclusive endpoint neighborhoods after target masking | Within-side density 0.524867; excess-density candidate 0.525869 | WEAK_PRIMITIVE; beat matched within control by +0.002268, below absolute gate |
| P5 raw feature cosine | S1J_C2 | 0.5262899355 | +0.000669 | 24736 | 48.57 | Raw endpoint feature cosine | Same-parameter score rescaling 0.525717 | LOW_PRIORITY; below gate and weaker than P1–P4 |

## Composition decisions

- Do not concatenate all primitives. ECR tests one residual-calibration mechanism: separately standardized Raw-HG pair evidence, degree/CN scalar evidence, and target-masked cross-neighborhood density, with zero-initialized low-capacity corrections.
- ECR singles are ablations of a coherent hypothesis, not separate discoveries. The same-parameter shuffled arm breaks evidence-to-pair assignment while preserving dimensions, parameter count, and the calibration form.
- If ECR fails the registered additive gate, test one factorized semantic × structural calibration. Exact baseline/single results may be reused only if runner/source hashes, initializer, fixed sample, split hashes, validation candidate hashes, sampler, seed, and epoch count match.
- No test examples or labels were opened in V12 or V13 Stage 1.

