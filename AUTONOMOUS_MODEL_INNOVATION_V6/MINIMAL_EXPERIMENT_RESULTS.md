# V6 最小实验结果

状态：`NOT_EXECUTED`

## 预注册规则

只有在候选通过文献审查和机制单元测试后，才执行：seed 0 smoke，再执行 seeds 0/1/2 的 Parent/New/Simple/Frozen/Shuffled/Proxy 配对实验。GO 条件固定为：

1. New 在三个 seed 的 validation MRR 都超过 Parent；
2. 平均 validation ΔMRR ≥ +0.005；
3. New 超过最强简单替代和关键机制对照；
4. shuffled/frozen 不能复现核心收益；
5. Hits@10 没有明显一致退化；
6. 无泄漏、实现错误和异常资源消耗。

该阈值是初筛门槛，不是统计显著性或论文级证明。

## 实际运行记录

| 项目 | 结果 |
|---|---|
| 本机 GPU 训练 | 未执行；本机 PyTorch 为 CPU build |
| 服务器合成图实验 | 未执行；候选在 novelty gate 前停止 |
| 服务器 Cora seed 0 smoke | 未执行 |
| 服务器 Cora seeds 0/1/2 | 未执行 |
| Parent/New/Simple/Frozen/Shuffled/Proxy | 无原始指标，不能填 0 或 N/A 冒充结果 |
| test 指标选择 | 未发生 |
| 新代码/配置/JSON/日志 | 未生成；旧 V1–V5 文件未覆盖 |

## 远程环境

服务器已通过只读探测确认：`mei_env` 使用 PyTorch 2.8.0 + CUDA 12.8，CUDA 可用，检测到 Tesla V100 16 GB。之后若有合法候选，所有机制测试和训练都必须通过该解释器在远程执行；本机不得代跑。

远程项目 `/home/ubuntu/DCDLP-main` 已具备 `data/processed/cora_heart_seed0..4.npz`。五个文件的 SHA256 均为：`0fb69795489eff3b3a2067b29808bdff4c703974f309e5c5480c135627eb9e62`。本轮没有读取标签做模型选择，也没有启动训练进程。

## 为什么不训练

C1 的补图算子与 ECGN/UGCN 等双图传播碰撞，且 `A^cX=1(1^TX)-X-AX` 给出简单代理；C2 与 edge-space/line-graph/Hodge/非回溯家族碰撞；C3 与 LEAP/CORE 的 link-prediction topology augmentation 碰撞。GPU 训练只能比较实现和预算，不能修复结构独立性失败，所以按预注册规则停止。
