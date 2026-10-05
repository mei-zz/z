# Phase-2 Selective Routing 决策报告

决策：`PIVOT_TO_CALIBRATION`

本报告仅用于 Cora 5-seed 路线筛选，不构成确认性显著性结论。

## 配对完整性

- 合法配对：5
- 完整性通过：True
- 配对审计：`[{"dataset": "cora", "seed": 0, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed0_c40448cb28a0.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M3/raw/cora_uniform_seed0_36c81d7aab4e.json"}, {"dataset": "cora", "seed": 1, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed1_24d10e7de783.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M3/raw/cora_uniform_seed1_4d43ed49c208.json"}, {"dataset": "cora", "seed": 2, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed2_b02221ef63fb.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M3/raw/cora_uniform_seed2_8df3d221b8d4.json"}, {"dataset": "cora", "seed": 3, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed3_49fafa05d116.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M3/raw/cora_uniform_seed3_5734aa780c60.json"}, {"dataset": "cora", "seed": 4, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed4_5ed175dca270.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M3/raw/cora_uniform_seed4_cb4c9d211379.json"}]`

## 冻结门槛

- MRR 相对下降不超过 1%：{'passed': True, 'relative_drop': 0.0, 'mean_delta': 0.0017871823638036493}
- Routing selectivity：{'cn': {'passed': True, 'mean_delta': 0.057611867146010076, 'improved_seeds': 5, 'seed_count': 5}, 'degree': {'passed': False, 'mean_delta': -0.025685668408615324, 'improved_seeds': 1, 'seed_count': 5}}
- Target response：{'cn': {'passed': True, 'mean_delta': 0.08515692589026465}, 'degree': {'passed': True, 'mean_delta': 0.011787948779761793}}
- Cross/probe leakage：{'passed': True, 'cross_sensitivity': True, 'probe_r2': True}
- Audited interaction：{'passed': False, 'mean_share': 0.0, 'cap': 0.2, 'audited_mode': False}
- Group robustness（支持证据）：{'passed': False, 'worst_group_mean_delta': 0.00018628604290679593, 'group_gap_mean_delta': 0.012707242284856706}

所有统计检验均为探索性辅助；不会仅凭 5-seed t-test 宣称显著。
