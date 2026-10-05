# Phase-2 Selective Routing 决策报告

决策：`PIVOT_TO_CALIBRATION`

本报告仅用于 Cora 5-seed 路线筛选，不构成确认性显著性结论。

## 配对完整性

- 合法配对：5
- 完整性通过：True
- 配对审计：`[{"dataset": "cora", "seed": 0, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed0_c40448cb28a0.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M2/raw/cora_uniform_seed0_11ee10e110ae.json"}, {"dataset": "cora", "seed": 1, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed1_24d10e7de783.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M2/raw/cora_uniform_seed1_25044ef578c4.json"}, {"dataset": "cora", "seed": 2, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed2_b02221ef63fb.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M2/raw/cora_uniform_seed2_d44d1125a6c1.json"}, {"dataset": "cora", "seed": 3, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed3_49fafa05d116.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M2/raw/cora_uniform_seed3_e15a1f5bd187.json"}, {"dataset": "cora", "seed": 4, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed4_5ed175dca270.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M2/raw/cora_uniform_seed4_08eb1afb48dd.json"}]`

## 冻结门槛

- MRR 相对下降不超过 1%：{'passed': True, 'relative_drop': 0.0, 'mean_delta': 0.004915030593602429}
- Routing selectivity：{'cn': {'passed': False, 'mean_delta': -0.029902846486090123, 'improved_seeds': 2, 'seed_count': 5}, 'degree': {'passed': False, 'mean_delta': -0.007784099274917589, 'improved_seeds': 1, 'seed_count': 5}}
- Target response：{'cn': {'passed': True, 'mean_delta': 0.15001030694457548}, 'degree': {'passed': True, 'mean_delta': 0.039418458223342896}}
- Cross/probe leakage：{'passed': True, 'cross_sensitivity': False, 'probe_r2': True}
- Audited interaction：{'passed': True, 'mean_share': 0.018518565953138853, 'cap': 0.2, 'audited_mode': True}
- Group robustness（支持证据）：{'passed': False, 'worst_group_mean_delta': 0.002383704656677815, 'group_gap_mean_delta': 0.015055862181948532}

所有统计检验均为探索性辅助；不会仅凭 5-seed t-test 宣称显著。
