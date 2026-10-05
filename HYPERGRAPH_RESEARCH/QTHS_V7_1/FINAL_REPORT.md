# V7.1 final report

- QTHS_LOCKED_REPRODUCTION: **PASS**
- ENVIRONMENT_REPRO_BLOCKED: **False**
- INNOVATION_1: **QTHS** (frozen rule; predefined alpha=0.25)
- INNOVATION_2: **AQTHS REJECTED**
- MECHANISM_CLASS: **INCONCLUSIVE**
- NOVELTY_STATUS: **NO_EXACT_MATCH_IDENTIFIED_IN_FOCUSED_SEARCH** (not a priority claim)
- FINAL_DECISION: **QTHS_ONLY_PAPER_READY**

## Cora test

- C1_GRAPH_HARD: 0.472552 ± 0.093757; seeds=0.555629, 0.370896, 0.491130
- C2_RANDOM_VETO: 0.490064 ± 0.093377; seeds=0.549985, 0.382473, 0.537733
- C3_QTHS25: 0.493377 ± 0.094352; seeds=0.554033, 0.384672, 0.541427

## Cross-dataset status

- Cora locked gate details: `{'QTHS25_mean_mrr': 0.4933770849310061, 'Graph_hard_mean_mrr': 0.4725515619217042, 'Random_veto_mean_mrr': 0.4900635446840087, 'QTHS25_wins_vs_graph_hard': 2, 'QTHS25_wins_vs_random_veto': 3, 'QTHS25_beats_graph_hard_mean': True, 'QTHS25_beats_random_veto_mean_or_ties': True}`.
- Citeseer: `{'positive_mean_on_validation': True, 'positive_mean_on_test': False, 'validation_wins_vs_graph_hard': 2, 'test_wins_vs_graph_hard': 2, 'supported': True, 'fully_reverse': False, 'rule': 'positive if validation OR test mean beats Graph-hard; report both without tuning'}`.
- PubMed: `THIRD_DATASET_POSITIVE_SIGNAL`; details in `03_PUBMED_SCREEN.md`.
- AQTHS Cora validation: `AQTHS_REJECT`.
- AQTHS Cora test: `NOT_RUN_VALIDATION_GATE_CLOSED`.
- AQTHS Citeseer transfer: `NOT_RUN_AQTHS_TEST_NOT_CONFIRMED`.

NEXT_EXPECTED_STEP: Benchmark expansion, ablations, runtime, paper writing
