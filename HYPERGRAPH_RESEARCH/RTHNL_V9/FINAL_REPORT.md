# V9 final report

- Study status: **COMPLETE_EARLY_STOP** at the preregistered Cora validation gate.
- Final decision: **RTHNL_REJECT**; **MECHANISM_UNSUPPORTED**; **SH75_DOMINATES**.
- Actual frozen training count: **K=1**, although the train-only teacher candidate pool has 20 candidates per positive.
- RTHNL vs Graph-hard Cora validation: implied paired deltas `[0,0,0]`, mean `0`, wins `0/3`; required mean gain was greater than `0.002` and at least 2/3 wins.
- RTHNL vs Shuffled-RTHNL: exact identity for each positive at K=1; no possible within-positive reordering or tail attenuation.
- RTHNL vs SH75: implied mean delta `-0.080559`; SH75 wins 2/3. RTHNL is materially below SH75 under the `0.005` margin.
- Training jobs launched: **0**. V8 epoch-10 Graph-hard validation records were reused under the exact loss/gradient identity, avoiding three redundant runs. Test evaluations: **0**. PubMed, Citeseer and backbone expansions: **not run** after the validation gate.
- Machine: remote Tesla V100-PCIE-16GB; idle after CUDA formula preflight. No persistent monitoring process remains.
- Novelty: **EXACT_RULE_UNVERIFIED**. No positive novelty or performance claim is supported.

The completed finding is that V9's mechanism cannot operate under the frozen V8 K=1 training protocol. A new study with K>1 would be a protocol change and would require matched baselines; it is outside this frozen-protocol result.
