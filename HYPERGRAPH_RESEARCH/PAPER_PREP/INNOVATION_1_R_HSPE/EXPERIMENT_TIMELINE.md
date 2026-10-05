# EXPERIMENT TIMELINE — R-HSPE

| 版本 | 研究问题 | 结果 | 决策 |
|---|---|---|---|
| HMC V15 | 固定摘要下的 hypergraph motif/set 信号是否超过 HRA-like scalar，是否值得启动神经 Stage 1？ | Cora zero-GPU gate 得到 SCALAR_SUFFICIENT；real joint summary 未达到预设增益，Stage 1 GPU 未运行；test sealed。 | 停止 HMC；不把诊断性摘要失败外推成所有可学习编码器均无效。 |
| NHMC V16 | learned native hypergraph set encoder 能否超过 scalar、SIZE 与 SHUFFLE 对照并跨数据集迁移？ | Cora seed0×5 epoch validation Stage 1 GO；PubMed transfer screen reject，H1 未过 B2/C1/C2 gates；test OFF。Stage0 按 override 只作 diagnostic。 | 不支持跨数据集推广；没有 Stage 2 或 test。 |
| HSPE V17 | 去掉 native overlap 后，size-token set encoder 是否足以带来早期信号？ | Cora/PubMed 5E×3 seeds 早期 screen 对 B0 有信号，但 Cora 的 parameter-matched gate 未过，且 shuffle power 低；overall HSPE_EARLY_REJECT。 | 不直接推广早期 H1；进入更严格的机制与 rank normalization audit。 |
| V17.1 | 多种 scalar/set controls 下，候选 pair token pathway 与 rank-normalized variant 能否通过 validation？ | 10 epochs×5 seeds，validation only。H1 对 B0 有效，但 Cora H1 未超过 count-matched、constant-set 或 global-size-shuffle；两数据集 size-content 解释均不成立。一个 ECDF rank variant H2 被选为 R-HSPE；mechanism 为 CONTEXT_DRIVEN。 | 冻结候选方法和边界为 R-HSPE；controls 只限制机制解释，test 保持到 V17.2。 |
| V17.2 | 冻结 R-HSPE 是否在 one-shot test 保留 standalone 增益，并能在第三数据集复现？ | Cora/PubMed 五 seed test 相对 B0 mean ΔMRR 分别 +0.14411309043713388、+0.01294802474118606；Citeseer 三 seed +0.0887476626284336。Cora 对 count-matched C1、PubMed 对 constant-set C2 的 paired 差值为负/近零。 | standalone predictive efficacy 有支持；size-specific causal explanation 仍不支持；进入 publication benchmark 与插件验证。 |
| V17.3 | R-HSPE 单独与公开/强 link predictors 的排名竞争力如何？ | Standalone competitiveness WEAK：R-HSPE rank Cora 4、PubMed 4、Citeseer 3；NCN/NCNC 通常排名更高。训练预算/选点规则不同。 | 不再把 R-HSPE 定位成 standalone backbone；转向 complementary plug-in claim。 |
| V17.4 | R-HSPE 作为 NCN/NCNC decoder plug-in 是否在强 backbone 上提供可重复互补增益？ | Fixed-final-10 paired test：NCNC+R-HSPE 在 Cora/PubMed 为 +0.025852682660934833/+0.007136914679784767，均 5/5 wins；对 NULL75 也均 5/5。Citeseer validation Δ−0.02737937803369254、0/3，test 未运行。 | 冻结支持 Cora/PubMed strong-backbone complementarity；Citeseer transfer NOT_SUPPORTED。 |
| V17.5 | V17.3 与 V17.4 的协议差异是否意味着必须重跑或混合排名？ | 核实为 INTENTIONAL_PROTOCOL_DIFFERENCE：数据、split、candidate set、adapter、evaluator 相同；V17.3 NCN/NCNC 100e best-validation，V17.4 10e fixed-final。无 unresolved code mismatch。 | 无需 rerun；Table A 与 Table B 分开；R-HSPE FINAL_FROZEN；Innovation 2 未启动。 |

## V17.3 / V17.4 protocol reconciliation

| 项目 | V17.3 | V17.4 |
|---|---|---|
| NCN/NCNC budget | 100 epochs | fixed 10 epochs |
| checkpoint | first best validation MRR | final epoch 10 |
| data / split / candidate set / adapter / evaluator | 与 V17.4 对齐 | 与 V17.3 对齐 |
| 主要用途 | standalone publication benchmark / ranks | paired strong-backbone plug-in test |
| 能否共用绝对 ranking table | 不可以 | 不可以 |

V17.5 冻结 artifact 将此认定为 INTENTIONAL_PROTOCOL_DIFFERENCE，而非尚待消除的实现冲突。不能从某一版本绝对 MRR 推出跨版本强弱排名。V17.3 表里的 R-HSPE/B0/control 是冻结 standalone 结果复用，NCN/NCNC 则使用 100-epoch best-validation protocol，因此对比也不是 equal-compute。

## 实验终点

FINAL_FROZEN 工件、方法定义、hash 与协议表均已存在；没有剩余 R-HSPE 实验门槛需要本手册触发。本任务只整理文档，不启动任何新的训练、测试、调参、方法搜索或 Innovation 2。
