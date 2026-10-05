# PROBE V2 Protocol Fix Report

本报告由 `aggregate_posthoc_probe_v2.py` 基于现有 checkpoint 的 Probe V2 输出生成。没有重新训练模型，也没有修改 Step 12。

## A. Changed files

- `src/dcdlp/evaluation/posthoc_probe.py`: 增加 canonical context graph、单 pair target-edge removal、context hash，以及 Ridge scaler/target diagnostics。
- `scripts/run_posthoc_leakage_audit.py`: 改为逐 pair context graph，X/y 使用同一图，probe seed 控制 pair sampling，统一 eval/no-grad，并增加协议断言和逐边输出。
- `tests/test_posthoc_probe_v2.py`: 增加 per-pair masking、valid/test no-op、X/y context hash、sampling reproducibility 测试。
- `scripts/aggregate_posthoc_probe_v2.py`: 汇总 model-seed 与 probe-sample-seed 两类变异，并审计跨模型 pair hash。

## B. Root cause

旧 probe 的 train representation 使用了整个 batch 的 target-edge masking，而 valid/test representation 没有相同的图上下文；同时 train target 使用完整 train_graph。近常数 latent 维度在跨 split 偏移后使 StandardScaler 产生极小 scale，Ridge 测试输入发生外推，导致 M0 seed0 出现 R²≈-340。

## C. Old vs New protocol

| 项目 | Old | Probe V2 |
| --- | --- | --- |
| train masking | 一次移除整个 pair batch | 每个 pair 只移除自身 target edge |
| valid masking | 基本 no-op，但未统一显式验证 | 统一 remove-if-present；存在则报错 |
| test masking | 基本 no-op，但未统一显式验证 | 统一 remove-if-present；存在则报错 |
| X graph | train/valid/test 不一致 | 每个 pair 的 per-pair context graph |
| y graph | 完整 train_graph | 与 X 完全相同的 context graph |
| probe seed | Ridge deterministic，重复相同 | 真正控制 train/test pair sampling |
| scaler | StandardScaler+Ridge | 保持 StandardScaler+Ridge，新增 diagnostics |

## D. M0 seed0 diagnostic

旧值来自上一轮对旧 checkpoint/probe 的只读诊断；新值来自 Probe V2 输出。

| 指标 | Old | New Probe V2 |
| --- | ---: | ---: |
| z_cn→degree test R² | ≈ -340.55 | seed0: 0.238700; seed1: 0.029152; seed2: 0.215565 |
| standardized max abs | ≈ 10210 | seed0: 30.767585; seed1: 275.856714; seed2: 29.549389 |
| scaler min scale | ≈ 6.96e-6 | seed0: 0.0023080536; seed1: 0.00025769508; seed2: 0.0024030875 |

M0 seed0 V2 的三个 probe sample seed 的 z_cn→degree R²、test standardized max abs、min scaler scale 由 `posthoc_probe.csv` 与 `posthoc_probe_diagnostics.json` 保存；报告不对 R² 设正值门槛。

## E. Full M0-M3 probe results

完整逐 checkpoint、逐 probe sample seed 结果见 `posthoc_probe_v2_all_rows.csv`；按 model seed 聚合结果见 `posthoc_probe_v2_model_seed_summary.csv`；按 probe sample seed 聚合结果见 `posthoc_probe_v2_probe_seed_summary.csv`。以下为所有五类 probe 的整体均值±标准差（15 个 model-seed/sample-seed 组合）：

| Model | Probe | R² | MAE | Spearman |
| --- | --- | ---: | ---: | ---: |

| M0 | z_cn_to_degree | 0.1545±0.1442 | 0.9549±0.0199 | 0.3702±0.0174 |
| M0 | z_residual_to_degree | 0.1874±0.1183 | 0.9421±0.0544 | 0.4405±0.1090 |
| M0 | z_degree_to_cn_residual | 0.0187±0.0165 | 0.3426±0.0037 | 0.0506±0.0225 |
| M0 | z_degree_to_degree | 0.9984±0.0006 | 0.0311±0.0047 | 0.9992±0.0003 |
| M0 | z_cn_to_cn_residual | 0.7141±0.2585 | 0.1484±0.0096 | 0.8279±0.0165 |
| M1 | z_cn_to_degree | 0.5188±0.0541 | 0.6922±0.0336 | 0.7397±0.0260 |
| M1 | z_residual_to_degree | 0.1417±0.1658 | 0.9502±0.0573 | 0.4397±0.0965 |
| M1 | z_degree_to_cn_residual | 0.0160±0.0193 | 0.3430±0.0041 | 0.0557±0.0206 |
| M1 | z_degree_to_degree | 0.9985±0.0004 | 0.0303±0.0029 | 0.9994±0.0002 |
| M1 | z_cn_to_cn_residual | 0.9531±0.0173 | 0.0460±0.0079 | 0.9783±0.0118 |
| M2 | z_cn_to_degree | 0.5089±0.0837 | 0.7009±0.0382 | 0.7455±0.0358 |
| M2 | z_residual_to_degree | 0.1329±0.0427 | 0.9648±0.0170 | 0.3951±0.0386 |
| M2 | z_degree_to_cn_residual | 0.0147±0.0247 | 0.3431±0.0047 | 0.0476±0.0231 |
| M2 | z_degree_to_degree | 0.9983±0.0006 | 0.0327±0.0051 | 0.9992±0.0003 |
| M2 | z_cn_to_cn_residual | 0.9292±0.0769 | 0.0494±0.0073 | 0.9791±0.0050 |
| M3 | z_cn_to_degree | 0.5250±0.0443 | 0.6860±0.0331 | 0.7430±0.0293 |
| M3 | z_residual_to_degree | -1.2006±4.4459 | 0.9923±0.1393 | 0.4263±0.0910 |
| M3 | z_degree_to_cn_residual | 0.0156±0.0190 | 0.3430±0.0038 | 0.0560±0.0210 |
| M3 | z_degree_to_degree | 0.9988±0.0003 | 0.0273±0.0050 | 0.9991±0.0005 |
| M3 | z_cn_to_cn_residual | 0.9483±0.0334 | 0.0458±0.0077 | 0.9798±0.0065 |

## F. Cross leakage conclusion

以 R² 为主，较低表示从其他分支表征重建结构目标的能力较低。下表是 M1/M2/M3 相对 M0 的五个 model seed paired ΔR²；`direction` 使用 lower-is-better 规则。

| Candidate | Probe | ΔR² mean±std | Direction |
| --- | --- | ---: | --- |
| M1 | z_cn_to_degree | 0.3644±0.0966 | WORSE |
| M1 | z_residual_to_degree | -0.0457±0.0794 | MIXED |
| M1 | z_degree_to_cn_residual | -0.0027±0.0095 | UNCHANGED |
| M2 | z_cn_to_degree | 0.3544±0.0916 | WORSE |
| M2 | z_residual_to_degree | -0.0545±0.1126 | MIXED |
| M2 | z_degree_to_cn_residual | -0.0040±0.0212 | MIXED |
| M3 | z_cn_to_degree | 0.3706±0.0804 | WORSE |
| M3 | z_residual_to_degree | -1.3880±2.4716 | IMPROVED |
| M3 | z_degree_to_cn_residual | -0.0030±0.0112 | UNCHANGED |

## G. Target retention conclusion

target retention 的 R² 越高表示目标信息保留越强。下表使用 higher-is-better 方向；`z_degree→degree` 基本保持不变，而 `z_cn→cn_residual` 在 M1/M2/M3 相对 M0 整体提高。

| Candidate | Probe | ΔR² mean±std | Direction |
| --- | --- | ---: | --- |
| M1 | z_degree_to_degree | 0.0001±0.0003 | UNCHANGED |
| M1 | z_cn_to_cn_residual | 0.2389±0.1573 | IMPROVED |
| M2 | z_degree_to_degree | -0.0001±0.0004 | UNCHANGED |
| M2 | z_cn_to_cn_residual | 0.2151±0.1727 | IMPROVED |
| M3 | z_degree_to_degree | 0.0004±0.0006 | UNCHANGED |
| M3 | z_cn_to_cn_residual | 0.2341±0.1364 | IMPROVED |

## H. Scientific conclusion

Probe V2 修复了已确认的 protocol mismatch，使 M0 seed0 的极端负 R² 不再由 batch masking 与 X/y context mismatch 主导。修复后，`z_cn→degree` 的 R² 在 M1/M2/M3 相对 M0 均为正向增加（对 cross leakage 而言是 WORSE），MAE 虽下降但不能抵消 R²/Spearman 的方向；`z_residual→degree` 只有混合或高方差证据；`z_degree→cn_residual` 基本不变。因此当前不能声称 Conditional CN Residual 已经降低整体 cross leakage。可以客观报告的支持证据是：`z_cn→cn_residual` target retention 明显提高，且旧的 M0 seed0 极端 probe 异常被 protocol 修复后消失。

## I. Protocol and test status

- 已完成 20 个 checkpoint、300 条 probe 记录；V2 metadata 保存 per-pair context graph hash、split pair hash、model frozen/eval 状态和断言计数。
- `posthoc_probe_top20_errors.csv` 保存每个 probe/sample seed 的最大 20 个测试误差及 pair 结构信息。
- `posthoc_probe_v2_pair_hash_audit.csv` 检查相同 model seed/probe seed 下 M0-M3 的采样是否一致；当前 45 组均通过。
- V2 toy graph、sampling、X/y context 与既有 post-hoc 测试共 7 项通过；PyTorch 2.8 checkpoint load 使用 probe 进程级兼容设置。
- 不修改 routing loss、interaction、CN residualizer、checkpoint 或 Step 12。
