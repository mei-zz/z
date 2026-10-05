# V12 Final Report — Autonomous Link-Prediction Innovation Search

STATUS: EXECUTED  
WORKSPACE: DCDLP-main  
AUTORESEARCH: V12 + Paper-Core Continuation Mode  
FINAL_DECISION: `NO_EXECUTABLE_IDEA_AFTER_EXHAUSTIVE_SEARCH`  
STOP_CONDITION: six orthogonal mechanism families were tested; no idea passed formal promotion against the strongest fixed QTHS25 baseline. The initial SH75-only F1/D1 signals were provisional and failed their matched QTHS25 confirmation. The search stopped with 39/40 Phase 1 training equivalents used because the last equivalent could not fund a complete new candidate/control pair.

## Handoff

| Field | Result |
|---|---|
| PHASE1_EXPERIMENTS | 39/40 Stage-1-equivalent actual training runs; 14 ideas across dynamics/positive-side, pair/decoder, context, graph–hypergraph representation, ranking objective, and consistency regularization |
| PHASE1_CONFIRMATIONS | 5 additional 10-epoch Stage 2 runs for F1 and D1; both rejected against the QTHS25 baseline and matched controls |
| INNOVATION_1 | None confirmed |
| I1_FAMILY | N/A |
| I1_VALIDATION | No candidate survived the fixed-QTHS25 promotion/confirmation gates; provisional F1/D1 SH75 signals collapsed under matched QTHS25 confirmation |
| I1_TEST | Not run; test data and labels remained unopened |
| I1_CROSS_DATASET | Not run; no I1 was frozen |
| I1_MECHANISM | N/A |
| I1_NOVELTY | No I1 novelty claim. Focused checks for the earlier F1/D1 Stage 2 candidates found conceptual overlap; both failed performance confirmation |
| PHASE2_EXPERIMENTS | 0/25; not started because no Innovation 1 was frozen |
| INNOVATION_2 | Not searched; not applicable without I1 |
| I2_FAMILY / VALIDATION / TEST / CROSS_DATASET / MECHANISM / NOVELTY | N/A; no Phase 2 candidate was evaluated |
| I1_I2_ORTHOGONALITY | N/A |
| COMBINATION_VALIDATION / TEST | Not run |
| ADDITIVE_GAIN | N/A |
| PARAMETER_CONTROL | Candidate-specific controls were run as listed in the experiment ledger; none of the candidates cleared the registered promotion gate |
| COMPUTE_CONTROL | Training epochs, sampler, split, and validation protocol were held fixed within each screen; two independent arms were run in parallel where applicable |
| COMBINED_NOVELTY | Not applicable |
| PAPER_STORY_COHERENCE | Not established; no supported I1→I2 mechanism chain exists |
| TOTAL_EXPERIMENTS | 44 actual model-training jobs: 39 Phase 1 screens plus 5 Stage 2 confirmation runs. Cached identical 5-epoch baselines in Stage 1I/J are recorded as reuses, not new training jobs |
| TOTAL_GPU_TIME | 4,069.05 seconds (about 67 minutes 49 seconds, summed per-job training time; jobs overlapped). Sum of per-job wall times was 4,299.10 seconds |
| GPU / RUNTIME | Tesla V100-PCIE-16GB; locked Python 3.11.11 / Torch 2.3.1+cu121 / PyG 2.5.3. Stage 1I/J ran two arms concurrently; observed GPU load was 94–98%, with under 1.2 GiB total reported VRAM use |
| TEST_POLICY | Preserved: `test_evaluated=false` in all V12 results; no test set was loaded |
| SERVER_FINAL_STATE | Training processes exited; queue contains only completed jobs; GPU idle at 0% and 9 MiB reported use |
| NEXT_EXPECTED_STEP | End this V12 search. Any follow-up should start from a new falsifiable mechanism informed by the ledgers; do not retune rejected candidates or claim a paper contribution from these screens |

## Final Stage 1 outcomes

| Candidate | Validation MRR | Baseline | Matched control | Outcome |
|---|---:|---:|---:|---|
| D2 raw cross-closure density (Stage 1H) | 0.527136 | 0.525620 | 0.524867 | +0.001515 vs baseline and +0.002268 vs control; below +0.003 / +1% gate |
| D2R excess cross-closure contrast (Stage 1I) | 0.525869 | 0.525620 | 0.527136 | +0.000249 vs baseline; −0.001266 vs raw D2 control |
| C2 raw-feature cosine (Stage 1J) | 0.526290 | 0.525620 | 0.525717 | +0.000669 vs baseline and +0.000573 vs score-rescaling control; below gate |

The stronger historical outcomes and all other falsifications are recorded in [IDEA_LEDGER.md](IDEA_LEDGER.md), [EXPERIMENT_LEDGER.tsv](EXPERIMENT_LEDGER.tsv), [BASELINE_AUDIT.md](BASELINE_AUDIT.md), and [NOVELTY_LEDGER.md](NOVELTY_LEDGER.md). The strongest matched 5-epoch reference remained Cora seed 0 QTHS25+BCE at validation MRR 0.525620.
