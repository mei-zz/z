# T1 Phase B Stage 1 result

**Decision: `STAGE1_REJECT`.** The server completed the T1 teacher trajectory and all seven registered Cora Stage 1 jobs. The T1 selector did not pass either the baseline-gain or mechanism-control gate. Test data were not evaluated.

## Validation MRR

| Arm | MRR | Difference from QTHS25 |
|---|---:|---:|
| QTHS25 baseline | 0.5256204672 | — |
| T1 persistent hardness | 0.3362255062 | −0.1893949609 |
| Final snapshot | 0.3202629917 | −0.2053574755 |
| Mean rank | 0.3157074960 | −0.2099129712 |
| Trajectory shuffled | 0.4923756435 | −0.0332448237 |
| Final-rank-matched | 0.4848878243 | −0.0407326429 |
| SH75 | 0.4840758807 | −0.0415445864 |

T1's relative change against QTHS25 was −36.03%. It exceeded final-snapshot by +0.0159625145 and mean-rank by +0.0205180103, but fell below trajectory-shuffled by −0.1561501372, final-rank-matched by −0.1486623180, and SH75 by −0.1478503745. Since the registered mechanism gate requires T1 to exceed both trajectory-shuffled and final-rank-matched, the candidate is rejected regardless of its small gains over two weaker summaries.

## Execution integrity

- The Graph-hard teacher completed 10 epochs and recorded every epoch 1–10 over the frozen train-only pool `[4488, 20, 2]`.
- All 7 Stage 1 jobs completed 5/5 epochs; each had 24,735 trainable parameters.
- Split hash: `c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a`.
- Train-pool hash: `3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba`.
- Validation-candidate hash: `aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455`.
- The common QTHS25 selected-negative hash was checked for all arms. Every result records `test_evaluated: false`.
- Driver SHA-256: `cc468f74531d66ea373090de83721741138925a10d6cfddbbedd5b57032d39cc`.
- Downloaded archive SHA-256: `75b76db3fa6d535749365675f599fcc7b78392be977ea3c5695a61bf166a78b1` (matches the server archive).

## Artifacts

- Local archive and extracted records: `remote_results/phaseb_t1_completed/`.
- Main Stage 1 JSON: `remote_results/phaseb_t1_completed/AUTONOMOUS_LP_RESEARCH_V13/t1_phaseb_stage1_results.json`.
- Final status JSON: `remote_results/phaseb_t1_completed/AUTONOMOUS_LP_RESEARCH_V13/t1_phaseb_status.json`.
- Teacher metadata/trajectory: `t1_phaseb_teacher_trajectory_cora.json` and `.npz` in the same extracted directory.
- Exact driver: `run_v13_t1_phaseb.py`.

## Research consequence

T1 is closed as a candidate and is not an Innovation 2 result. ECR remains unconfirmed after its PubMed matched-control rejection. L1 has since completed all five Stage 1 jobs and was rejected; see L1_PHASEB_STAGE1_PLAN.md for its final metrics and audit. No next experiment is selected.

