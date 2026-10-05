# Benchmark Feasibility

## 1. 远程环境

所有实际训练和数据恢复均在 `.env` 指定的远程服务器 `mei_env` 中完成，未把凭据写入报告或代码。

- GPU：Tesla V100 PCIe 16 GB；CUDA 可用。
- PyTorch：`2.8.0+cu128`。
- 远程磁盘：约 219 GB 总量，运行前约 28 GB 可用；因此不适合直接下载 full IGB。
- 官方 NodeDup 仓库已克隆到 `/home/ubuntu/AFDR_V10/NodeDup`。
- 实验原始日志和结果保存在远程 `/home/ubuntu/AFDR_V10/NodeDup/results_v10/formal`，并同步到本地 `V10/raw/formal/`。

## 2. 数据集可行性

| 数据集 | 是否完成 | 规模/用途 | 结论 |
|---|---:|---|---|
| Cora | 是 | 官方 NodeDup inductive cache，500 negatives/source | 可低成本重复运行 |
| CiteSeer | 是 | 官方 Planetoid raw files 恢复后生成同一 NodeDup cache | 可低成本重复运行 |
| IGB tiny | 未训练 | 官方 tiny download 约 0.36 GB，需额外安装 IGB-Datasets | 下载和后续 smoke test 可行；不应在当前没有 gap 时扩展到 full IGB |
| IGB full/small | 否 | 大图和 mmap/磁盘需求明显更高 | 当前服务器余量不足以作为低成本默认基准 |

已使用两个真实数据集完成基线，不使用人工随机负样本冒充官方 benchmark。

## 3. 协议边界

NodeDup 的公开 split 固定为 split seed 234、每个 source 500 negatives，官方 average-rank 处理 ties。10% 节点划为新节点；训练图只使用 old–old train edges。validation 主要是 old–old link ranking，而 test 混合 old–old、old–new 和 new–new 候选，推理图还包含部分 new-node context。

因此，本轮准确称为 NodeDup 的 production-style semi-inductive protocol，而不是严格 isolated-node zero-shot。validation/test 的任务组成不同是实验解释中的关键限制。

## 4. 运行兼容性和修复记录

1. PyTorch 2.8 默认 `torch.load` 的 weights-only 行为与旧 PyG 缓存不兼容。使用仅针对可信本地数据读取的兼容 wrapper，未修改模型计算或数据内容。
2. CiteSeer 的 PyG/fsspec 下载超时；从 Planetoid 官方 raw GitHub 文件直接恢复 `x/y/tx/ty/allx/ally/graph/test.index`，再按官方 NodeDup 代码生成 cache。
3. Cora 与 CiteSeer 均完成一轮 smoke forward/backward 及正式运行；没有因 OOM 改变模型语义。

## 5. 正式预算

- 模型：官方 GraphSAGE `augment=none` 与官方 NodeDup `augment=duplicated`。
- 模型 seeds：1、2、3；数据 split 固定，不把 split seed 和模型 seed 混用。
- Cora 学习率 `5e-4`，CiteSeer `1e-4`；两层 SAGE，hidden 256，dropout 0.5，sum predictor，最多 100 epochs，patience 20。
- checkpoint 选择只使用 validation Hits@20；test 只在配置冻结后报告。
- 12 个正式训练均退出码 0；CiteSeer duplicated seed3 早停，其他记录完整保留。

## 6. 可复现性资产

- 锁定协议：[PROTOCOL_LOCK.md](PROTOCOL_LOCK.md)
- 原始 baseline 日志：[raw/formal](raw/formal)
- 结构化 baseline 汇总：[baseline_summary.json](raw/baseline_summary.json)
- Cora 代理结果：[cora_proxy.json](raw/cora_proxy.json)
- CiteSeer 代理结果：[citeseer_proxy.json](raw/citeseer_proxy.json)
- 代理脚本：[inductive_proxy_audit.py](scripts/inductive_proxy_audit.py)

结论：至少两个真实数据集和当前 V100 环境足以支撑低成本 baseline/proxy 审计；但大规模 IGB 只应在明确 gap 后再启用。

