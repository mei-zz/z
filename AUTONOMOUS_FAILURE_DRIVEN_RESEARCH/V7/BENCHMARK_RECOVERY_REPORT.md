# V7 LPShift Benchmark Recovery Report

状态：`BENCHMARK_PARTIALLY_READY`

## 结论先行

官方 LPShift 已在 `.env` 指定的远程 V100 服务器、`mei_env` 中恢复并完成了数据生成、数据哈希审计、1 epoch smoke test 和 100 epoch 官方 GCN seed=1 完整运行。失败的根因不是 GitHub 仓库不可访问，而是 SNAP/OGB 数据下载速度过低，以及官方旧环境与当前 `mei_env` 的 PyTorch/SciPy 兼容性差异。

整体仍标记为 `BENCHMARK_PARTIALLY_READY`，原因是：

1. LPShift 官方 GCN 环境已经可复现；
2. AA/CN/RA 已在相同官方候选上完成固定代理审计；
3. 当前 DCDLP loader 不能直接读取 LPShift 的自定义 split，且其 message-passing 图定义与官方 LPShift 图不完全相同，因此本轮没有伪造一个“DCDLP LPShift 结果”；
4. 默认 `(valid=1,test=2)` 和扩展 `(valid=2,test=4)` 已完成基线退化核查，但尚未完成多 seed 的 LPShift 统计稳定性验证。

## 远程执行边界

所有下载、数据生成、启发式评估和 GCN 训练均在远程服务器完成：

- 项目：`/home/ubuntu/AFDR_V7/repo/LPShift-main`
- 环境：`mei_env`
- GPU：Tesla V100 16 GB
- 远程原始日志：`/home/ubuntu/AFDR_V7/logs/`
- 远程原始 JSON：`/home/ubuntu/AFDR_V7/raw/`

本机只保存报告、审计脚本和小型 JSON/日志副本；没有把 `.env` 凭证写入任何报告。

## 恢复结果

| 阶段 | 结果 | 证据 |
|---|---|---|
| GitHub 仓库访问 | 成功 | 官方 commit `cd916a4daaf060530326b5a7c43a99d7d4ab294c` |
| 官方源码归档 | 成功 | `/home/ubuntu/AFDR_V7/repo/LPShift-main` |
| OGB `collab.zip` | 成功 | 121,625,147 bytes；SHA256 `c5563198e041c338f0a78e11322bb2de76b68f0e9ae3e3b6d6af2d8ca64cc` |
| 官方数据生成 `(1,2)` | 成功 | dataset `ogbl-collab_CN_2_1_0_seed1` |
| 数据审计 | 成功 | `raw/lpshift_dataset_audit.json` |
| GCN smoke | 成功 | 1 epoch，exit 0 |
| GCN 完整 seed=1 | 成功 | 100 epochs，exit 0 |
| 扩展 `(2,4)` 数据生成 | 成功 | dataset `ogbl-collab_CN_4_2_0_seed1` |

## 初始失败与修复

第一次执行官方 `gen_synth.sh` 在约 5 分钟后只有约 7 MB 下载量，最终因人为停止而退出；这不是把普通 OGB 数据误标成 LPShift，也不是数据损坏。随后使用 8 路 HTTP range 下载完整官方 archive，并执行 ZIP 完整性测试。

当前环境的 PyTorch 为 2.8.0，而官方 `environment.yml` 针对 PyTorch 1.13/CUDA 11.6。第一次加载 OGB cache 时触发 PyTorch 2.6+ 默认 `torch.load(weights_only=True)` 的反序列化错误。随后又出现官方源码对旧版 SciPy/PyTorch 索引行为的假设不兼容。修复方式是远程 wrapper：对可信的官方本地数据显式使用 `weights_only=False`，并提供仅用于索引互操作的 edge-index compatibility view；没有改写 LPShift 的生成逻辑、模型或指标。

## 原始文件

- [数据审计 JSON](raw/lpshift_dataset_audit.json)
- [启发式审计 JSON](raw/lpshift_heuristics.json)
- [GCN smoke 日志](raw/gcn_smoke.log)
- [GCN seed=1 日志](raw/gcn_seed1.log)
- [扩展 `(2,4)` 启发式 JSON](raw/lpshift_heuristics_2_4.json)
- [扩展 `(2,4)` 数据审计 JSON](raw/lpshift_dataset_audit_2_4.json)
- [扩展 `(2,4)` GCN 日志](raw/gcn_2_4_seed1.log)

远程大文件 archive 没有复制到本地报告目录，权威副本仍在 `/home/ubuntu/AFDR_V7/collab.parallel.zip`，以节省本地空间；其大小和 SHA256 已记录在 `ENVIRONMENT_AUDIT.md`。
