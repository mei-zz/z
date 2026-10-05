# Phase-2 Selective Routing 决策报告

决策：`PIVOT_TO_CALIBRATION`

本报告仅用于 Cora 5-seed 路线筛选，不构成确认性显著性结论。

## 配对完整性

- 合法配对：5
- 完整性通过：True
- 配对审计：`[{"dataset": "cora", "seed": 0, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed0_c40448cb28a0.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M1/raw/cora_uniform_seed0_415e591ece66.json"}, {"dataset": "cora", "seed": 1, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed1_24d10e7de783.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M1/raw/cora_uniform_seed1_a86ca08c063e.json"}, {"dataset": "cora", "seed": 2, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed2_b02221ef63fb.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M1/raw/cora_uniform_seed2_9083d838c144.json"}, {"dataset": "cora", "seed": 3, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed3_49fafa05d116.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M1/raw/cora_uniform_seed3_3a6d721ab1ca.json"}, {"dataset": "cora", "seed": 4, "status": "AVAILABLE", "reason": "", "baseline_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M0/raw/cora_uniform_seed4_5ed175dca270.json", "candidate_result": "/home/ubuntu/DCDLP-main/results/phase2_selective_local/cora5/M1/raw/cora_uniform_seed4_f6727223606a.json"}]`

## 冻结门槛

- MRR 相对下降不超过 1%：{'passed': True, 'relative_drop': 0.0, 'mean_delta': 0.0017013409692488157}
- Routing selectivity：{'cn': {'passed': True, 'mean_delta': 0.00012970883169920012, 'improved_seeds': 3, 'seed_count': 5}, 'degree': {'passed': False, 'mean_delta': -0.05021389818872549, 'improved_seeds': 0, 'seed_count': 5}}
- Target response：{'cn': {'passed': False, 'mean_delta': -0.006116251996423619}, 'degree': {'passed': True, 'mean_delta': 0.006325654484331608}}
- Cross/probe leakage：{'passed': True, 'cross_sensitivity': False, 'probe_r2': True}
- Audited interaction：{'passed': True, 'mean_share': 0.019117394491136627, 'cap': 0.2, 'audited_mode': True}
- Group robustness（支持证据）：{'passed': False, 'worst_group_mean_delta': 0.00016498708682402536, 'group_gap_mean_delta': 0.010998644003745667}

所有统计检验均为探索性辅助；不会仅凭 5-seed t-test 宣称显著。
