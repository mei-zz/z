# DCDLP V6 最终决策

## 决策

**STOP — NO_VALID_NETWORK_INNOVATION_FOUND**

允许的状态枚举中，本轮状态为 `STOP`；附带原因码为 `NO_VALID_NETWORK_INNOVATION_FOUND`。

## 逐项回答

### 找到了什么候选？

审查了三个结构候选：补图上下文传播、边/cochain 非回溯传播、learned topology-residual propagation。它们分别在公式或状态对象层面碰撞 ECGN/补图 GNN、SLRGNN/Hodge/历史 non-backtracking、LEAP/CORE。

### 与已有论文有什么实质区别？

没有一个候选能在本轮审查后给出可防守的实质区别。补图候选还可由全局特征和普通邻居聚合形成简单代理；边空间候选直接改变状态对象为已有 edge-space primitive；拓扑残差候选直接改变为已有 learnable graph editing。

### 是否完成真实训练？

没有。原因不是资源不足，而是所有候选先于机制测试在 novelty gate 被停止。服务器资源已确认可用，但没有以 GPU 训练掩盖碰撞。

### 三个 seed 原始指标是多少？

没有 V6 seed 0/1/2 运行，故不存在可报告的三 seed 指标、ΔMRR、Hits@10、AUC、AP、参数量、运行时间或峰值显存。V1–V5 的旧指标仍在旧目录中，未被移入或重算为 V6 结果。

### Shuffled/Frozen 是否复现收益？

V6 没有执行这些控制。不能把历史 CDPT 的 frozen/random 结果冒充 V6 候选结果；V4 的 CDPT 机制结论仍是 `MECHANISM_UNSUPPORTED`。

### 当前结果是否支持独立机制？

不支持。当前证据支持的是“这三个候选不应作为独立结构继续训练”，不是它们性能失败的实验证据。

### 是否值得继续深入？

不值得在当前静态 Cora HeaRT 环境继续深入这三条路线。若继续自主搜索，必须先改变研究问题或找到未落入上述状态对象的新传播规则，并重新执行文献、代理等价和合成图门槛；禁止从补图、edge-space、topology-editing 或 CDPT 变体继续扩展。

## 代码与数据边界

本轮未修改 V1–V5。当前源码是非 Git 工作区，因此用 SHA256 记录审计边界：

| 文件 | SHA256 |
|---|---|
| `src/dcdlp/models/dcdlp.py` | `C1BBF8A86A798FE088D13E61D38053E8DC23D8ADFB4443DEA5C56EF3F5FEBBA3` |
| `src/dcdlp/models/node_encoder.py` | `EADA0A085994145AED9DAFA78AEB98215C027E329A931DDCCDEB8178C2272FA1` |
| `src/dcdlp/train.py` | `DF889AB13B374AE5AED517346F3F2DF8A97B5DB633854AD2F32C4CDCF0CDB1F4` |
| `AUTONOMOUS_MODEL_INNOVATION_V4/scripts/v4_models.py` | `A203C41DBE31C727D0183544F7B27C09D0EF50A049743F0AC4D998CB46D81588` |
| `AUTONOMOUS_MODEL_INNOVATION_V4/scripts/v4_runner.py` | `DF08127D16747325B506CACC092BF4F5F4BC82477CB4F4C7BDB1793B5A35FCA7` |

V4 历史 Cora HeaRT 数据/候选边界哈希为 `98e4aaaf07d4`。远程服务器的 `data/processed/cora_heart_seed0..4.npz` 均已存在且 SHA256 为 `0fb69795489eff3b3a2067b29808bdff4c703974f309e5c5480c135627eb9e62`；当前本地工作区没有这些 NPZ，因此没有宣称完成 V6 数据重跑。服务器上也没有 V6 训练进程。
