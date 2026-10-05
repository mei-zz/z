# Official LPShift Baseline Results

## 1. 配置

官方 GCN 命令等价于 `gcn.sh` 的有效配置：GCN encoder、3 层、hidden 128、3 层 MLP predictor、dropout 0.1、learning rate 0.01、100 epochs、evaluation every 20 epochs、seed 1、batch/validation/test batch size 65,536、1 run。模型选择只按 validation MRR；test 只在选中的 epoch 进行描述性打印。

## 2. Smoke test

1 epoch smoke test exit 0，确认数据加载、forward/backward、validation/test ranking 和显存均正常。其 validation MRR 为 0.0220，test MRR 为 0.0252。该结果只用于运行检查，不用于性能结论。

## 3. 默认 `(valid=1,test=2)` 完整 seed=1

| metric | Highest validation | test at selected validation epoch |
|---|---:|---:|
| MRR | 0.0712 | 0.0578 |
| Hits@1 | 0.0208 | 0.0120 |
| Hits@3 | 0.0551 | 0.0402 |
| Hits@10 | 0.1553 | 0.1243 |
| Hits@20 | 0.2628 | 0.2423 |
| Hits@50 | 0.5038 | 0.4646 |
| Hits@100 | 0.7802 | 0.7449 |

训练侧在最佳点 MRR 约 99.98%，说明这个配置在 train random negatives 上几乎饱和，但在官方困难候选上的 ranking 明显较低。这是基线失败/分布偏移证据，不是模型创新证据。

资源：wall `234.87 s`，maximum RSS `2,543,920 KB`，GPU 峰值约 `10.852 GB`，exit status 0。只有一个 seed，日志中 `± nan` 是官方统计代码在 runs=1 下使用无偏标准差的自然结果，不能解释为稳定性。

## 4. 同配置扩展 `(valid=2,test=4)`

该组用于固定流程的难度敏感性核查，不参与模型/阈值选择。官方 GCN 100 epoch、seed=1 已完成，原始日志为 `raw/gcn_2_4_seed1.log`。

| metric | Highest validation | test at selected validation epoch |
|---|---:|---:|
| MRR | 0.1173 | 0.0579 |
| Hits@1 | 0.0482 | 0.0141 |
| Hits@3 | 0.1093 | 0.0416 |
| Hits@10 | 0.2457 | 0.1213 |
| Hits@20 | 0.3704 | 0.2162 |
| Hits@50 | 0.6120 | 0.4522 |
| Hits@100 | 0.8609 | 0.7482 |

该组 wall `169.74 s`，maximum RSS `2,483,444 KB`，exit status 0。它不是“更强模型”的证据；它说明不同 CN 阈值会同时改变候选难度和 GCN 的 validation/test gap。

## 5. 可重复性边界

已证明：同一远程环境、同一数据 hash、同一源码 commit、同一 seed 下可以完整运行。尚未证明：多个随机 seed 的均值/方差、不同机器的 bitwise determinism、以及 DCDLP 与官方 GCN 的 apples-to-apples 对比。因此本报告不宣称 LPShift 上的论文级稳定提升。
