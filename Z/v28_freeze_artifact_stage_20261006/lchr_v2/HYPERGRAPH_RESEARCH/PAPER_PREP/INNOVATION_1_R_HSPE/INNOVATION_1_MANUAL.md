# R-HSPE 创新点 1 手册

状态：DOCUMENTATION_ONLY 已完成  
冻结状态：FINAL_FROZEN  
整理日期：2026-10-04  
规范协议：R-HSPE-PAPER-V17.5

## 创新点 1 一页式总结

**名称：R-HSPE。** 正式英文展开全称未在 FINAL_FROZEN 工件中定义；依任务规则保留 R-HSPE 作为冻结名称/working full name，不另行创造。

**解决的问题。** 常见图链路预测器围绕候选端点的图结构邻域打分，但没有显式保留共享支持节点两侧关联超边如何成对出现的候选级超图上下文。R-HSPE 为每个候选节点对构造 incident-hyperedge-pair token 多重集，将这一上下文编码成可学习的 decoder correction。

**插入位置。** 它是已有 pairwise link predictor 的解码端轻量插件：原 backbone 先产生 logit，R-HSPE 产生一个标量残差并相加。独立评估时 backbone 是 frozen Raw-HG DCDLP B0；互补性主张来自 V17.4 的 NCN/NCNC 插件评估。

**输入与输出。** 输入是候选对 (u,v)、只使用训练图关系得到的 raw-star hypergraph、其 target-masked shared support，以及每个支持节点两侧的关联超边组合。每个 token 只编码两条关联超边的训练集 ECDF 大小秩组合，另外将 token 数与 shared-support 数显式拼接。输出是一个初始为零的标量 logit 残差；刚初始化时不改变原 backbone 分数。

**为何不是普通 CN、motif 或 HRA 标量。** 普通 CN 只计共同图邻居或聚合其节点表示，不枚举支持节点两侧的 incident hyperedge-pair 多重集。全局 motif/order 聚合通常先在全图/超图上编码模式，不等于针对每个查询候选对重建的 token 集合。HRA-like scalar 将结构压缩为标量；R-HSPE 保留候选条件化的 token 集合并学习 permutation-invariant pooling。不过 V17.1/V17.2 的控制结果不支持“大小内容本身带来提升”的机制归因，因此不能宣称 R-HSPE 在机制控制上胜过标量或 constant-set 对照。

**为何最终定位为 lightweight hypergraph-context plug-in，而不是 standalone SOTA。** V17.3 standalone benchmark 中 R-HSPE 排名为 Cora 4、PubMed 4、Citeseer 3，冻结结论为 standalone competitiveness WEAK。相反，V17.4 固定 10 epoch / final checkpoint 的 paired test 中，NCNC+R-HSPE 对 NCNC 的 MRR 增益在 Cora 为 0.025852682660934833（5/5 seeds），在 PubMed 为 0.007136914679784767（5/5）；NULL75 对照不能解释该增益。该证据支持把它作为互补插件来写，而不是替换 backbone。

| 冻结证据 | Cora | PubMed | Citeseer |
|---|---:|---:|---:|
| V17.2 standalone test：R-HSPE − B0 mean ΔMRR | 0.14411309043713388 | 0.01294802474118606 | 0.0887476626284336 |
| V17.4 NCNC plug-in paired test mean ΔMRR | 0.025852682660934833 | 0.007136914679784767 | 不适用：只做 validation，失败后 test 未运行 |
| 最终解释 | 有互补增益 | 有互补增益 | 强 backbone transfer 不支持 |

完整逐指标、配对对照及测量成本见 [METRIC_TABLES.md](METRIC_TABLES.md)。

## 精确方法定义

### 1. 候选条件化 hyperedge-pair token 多重集

所有结构只从 training-visible raw-star hypergraph 构造；基图使用训练正边，不将 held-out 边加入 message graph，也不做 clique expansion。对候选节点对 (u,v)，先在目标边移除规则下求 shared support 集合 \(\mathcal S(u,v)\)。训练正样本在构造 token 前移除被预测的目标关系，并对对应的有效超边大小作调整；验证/测试候选使用训练可见结构。

对于每个共享支持点 \(w\)，定义 \(I_u(w)\) 为同时与 u 和 w 关联的有效训练可见超边集合，\(I_v(w)\) 同理。token 枚举是 endpoint-role 有序的笛卡尔积：对每个 \(e\in I_u(w)\) 和 \(f\in I_v(w)\) 各产生一个 token。若不同的 \((w,e,f)\) 产生相同描述符，仍按原次数保留，因此是 multiset；没有学习超边 ID embedding。

设 \(M\) 为训练可见 active hyperedges 数量，训练集右连续经验 CDF 为：

\[
F_{\mathrm{train}}(s)=rac{1}{M}\sum_{h\in H_{\mathrm{train}}^{\mathrm{active}}}\mathbf{1}[|h|\leq s].
\]

对 target-masked 后有效大小 \(|e|,|f|\)，计算：

\[
r_e=F_{\mathrm{train}}(|e|),\qquad r_f=F_{\mathrm{train}}(|f|),
\]

并构造冻结的六维 token：

\[
\mathbf{x}_{w,e,f}=
[r_e+r_f,\ |r_e-r_f|,\ r_e r_f,\ 0,\ 0,\ 0]\in\mathbb{R}^{6}.
\]

末三维固定为零；R-HSPE 冻结版本没有将超边交叠描述、node features 或 learned hyperedge identity embedding 输入该 token encoder。ECDF 只用训练可见 active hyperedges 拟合。

### 2. 共享 token encoder、pooling 与计数特征

对每个 token 使用共享 Linear(6,8) 和 ReLU：

\[
\mathbf{h}_{t}=\operatorname{ReLU}(W_e\mathbf{x}_{t}+\mathbf{b}_e)\in\mathbb{R}^{8}.
\]

令 token 数 \(T=|\mathcal T(u,v)|\)，shared-support 数 \(S=|\mathcal S(u,v)|\)。池化采用逐维 mean 与逐维 max：

\[
\mathbf{h}_{\mathrm{mean}}=
egin{cases}
T^{-1}\sum_{t=1}^{T}\mathbf{h}_t,&T>0\
\mathbf{0},&T=0
\end{cases},
\qquad
\mathbf{h}_{\mathrm{max}}=
egin{cases}
\max_{t=1,\ldots,T}\mathbf{h}_t,&T>0\
\mathbf{0},&T=0.
\end{cases}
\]

按代码，空集合的 mean/max 都是 8 维零向量。随后拼接两个显式结构计数：

\[
\mathbf{c}(u,v)=
[\mathbf{h}_{\mathrm{mean}};\mathbf{h}_{\mathrm{max}};
\log(1+T);\log(1+S)]\in\mathbb{R}^{18}.
\]

这一表示对 token 顺序置换不变；token 的多重性由池化输入中的重复项及 T 保留。

### 3. 零初始化残差打分

\[
\Delta_{\mathrm{R	ext{-}HSPE}}(u,v)=W_r\mathbf{c}(u,v)+b_r,\qquad
s_{\mathrm{final}}(u,v)=s_{\mathrm{backbone}}(u,v)+\Delta_{\mathrm{R	ext{-}HSPE}}(u,v).
\]

\(W_r,b_r\) 均零初始化，因此初始残差严格为零。Encoder 参数为 \(6	imes8+8=56\)；residual head 参数为 \(18+1=19\)；总计 75 个新增可训练参数。

### 数据流

候选对 (u,v)  
→ 只含训练关系的 training-visible raw-star hypergraph  
→ target masking 后的 shared supports w  
→ 逐个枚举 incident hyperedge pairs (e,f)，保留多重性  
→ 训练可见 active hyperedges 上拟合的 ECDF  
→ [r_e+r_f, |r_e-r_f|, r_e*r_f, 0, 0, 0]  
→ 共享 Linear(6,8)+ReLU  
→ 逐候选 mean pooling + max pooling  
→ 拼接 log1p(token_count) 与 log1p(support_count)  
→ Linear(18,1) zero-init residual  
→ frozen backbone logit + residual  
→ final pair score

### 两种使用方式

- **Standalone B0：** frozen Raw-HG DCDLP 产生基础分数，R-HSPE H2 residual 插入其解码输出。V17.2 的测试采用 10 epoch fixed-final checkpoint。
- **NCN/NCNC plug-in：** 在强 pairwise graph predictor 的候选对分数上增加冻结 75 参数的 R-HSPE correction。V17.4 Phase B 使用各 backbone 官方配置、10 epoch、固定 final checkpoint；Table 2 才是插件互补主张的证据。
- 两种 protocol 的 backbone、训练日程和 checkpoint 规则不同，不能横向合并绝对 MRR。

### 冻结 standalone 关键训练/评估设置

Standalone 版本沿用 V17.1 H2：Adam，learning rate 0.001，weight decay 0.0001，hidden/branch dimensions 16/8，2 个 GCN layers，dropout 0，batch 4096，QTHS25 负采样规则，fixed final epoch 10。评估调用 score_pairs(batch 8192)，target removal=True，ranking_metrics 使用每条正边 20 个负候选。V17.4 NCN/NCNC 插件遵循独立冻结的官方 backbone protocol，细项见 CANONICAL_PROTOCOL.json。

## 创新点的真正核心

可防守的核心不是“使用超边大小”，也不是“首次使用超边大小”或“首次使用 candidate hyperedge context”。冻结边界描述的是一个联合构造：**candidate-specific hyperedge-pair context + permutation-invariant decoder residual**；training-only rank-normalized cardinality descriptors 是其中的实现组成。focused novelty audit 中的精确碰撞标准同时要求候选条件化 incident-pair multiset、训练 ECDF descriptors、可学习集合池化与 decoder residual。

这与几类已知结构不同：

- **Ordinary CN：** 共同邻居作为点或计数输入，未保留每个共享支持点两侧超边身份组合形成的候选 token 多重集。
- **Global hyperedge-order / motif aggregation：** 在超图或 motif 上按阶数聚合的全局/节点表示，不等同于为每个 pair query 构建 (w,e,f) 集合。
- **Node-level hypergraph encoder：** 基于 incidence 的节点/超边消息传递属于 encoder 表示学习；R-HSPE 是加在 link predictor 解码端的候选残差。
- **HRA-like scalar heuristic：** 单个标量压缩结构摘要；R-HSPE 显式建模一组候选条件化的 pair tokens。该表示形式上的区别不等于控制实验中 R-HSPE 已胜过 HRA scalar。
- **NCN/NCNC：** 已建立候选 common-neighbor 表示与 decoder structural pooling 的先例；R-HSPE 的差异落在 hyperedge-pair token 多重集与训练 ECDF rank descriptor 的组合上。

## Novelty matrix 摘要

下表是对 HSPE_V17_2/NOVELTY_MATRIX.md focused audit 的简述；NR/UNKNOWN 表示所检查材料未报告，不能当作方法不存在的证据。

| 相关工作 | 工作内容 | 与 R-HSPE 的重叠 | 不同之处 / 非 exact collision 判断 |
|---|---|---|---|
| CCLPH（closest prior） | community-conditioned hypergraph similarity，对候选 node pair/triple 使用 incident hyperedge intersections 与大小项 | 候选条件化 hypergraph-pair/cardinality context，尤其大小乘积统计 | 分析式社区相似度求和；未见训练 ECDF rank token、learned permutation-invariant set encoder 与 decoder residual 的冻结联合构造 |
| NCN / NCNC（closest prior） | 候选 common-neighbor 节点表示与 decoder structural pooling | 候选条件化集合聚合、强 pairwise decoder precedent | 聚合对象为 graph common neighbors，不是 incident hyperedge-pair multiset；没有超边大小对/训练 ECDF |
| OFSH / OHAA | hyperedge prediction、order-specific node-neighborhood attention 与对比学习 | cardinality/order-aware hypergraph encoding | 所查方法按阶聚合，不是候选级 (e,f) token set 与 ECDF residual decoder |
| NSLR-HMANN | attribute-free link prediction，NSLR graph-to-HG 与节点/超边 attention | incidence/hyperedge结构用于 link prediction | 所查代码没有候选条件化超边对 tokens 或 ECDF descriptors |
| HMNE | hyper-motif/supernode、random-walk sequence 与 skip-gram node embeddings | hyper-motif 与超边关联结构 | 全局 motif/walk embedding；出版材料部分不可访问，相关字段保留 UNKNOWN/NR |
| HMRLH | open/closed hypermotifs 作为 supernodes 并做 motif random walk | motif / hyperedge intersection 结构 | 全局 motif 表示；所查方法未描述候选条件化 size-pair token decoder |
| HNHN / HGNN | incidence-based node-hyperedge message passing与 degree/cardinality normalization | cardinality-aware normalization | encoder侧归一化并非训练 ECDF，也不构造候选超边对多重集 |
| HP2PH | node-hyperedge weighted random walk，用超边大小调整 walk | hyperedge-size aware | walk/statistical scorer，不是 learned pair-token set residual |
| Hyperedge Copy Model | temporal hyperedge prediction，noisy-copy generative likelihood；边大小与交集统计 | 包含 edge-size/intersection 和 size-pair statistics 的先验 | 生成式 hyperedge likelihood，不是 pairwise node candidate 的神经 token-set decoder |

## 最终冻结结论

- Innovation 1：R-HSPE；Status：FINAL_FROZEN。
- Paper role：lightweight hypergraph-context plug-in。
- Primary evidence：V17.4 fixed-final-10 paired NCNC gains on Cora and PubMed。
- Supporting evidence：V17.2 standalone test gains over B0 on Cora、PubMed、Citeseer。
- Generalization limit：Citeseer strong-backbone transfer NOT_SUPPORTED；仅有 validation 失败结果，未运行 test。
- Mechanism：CONTEXT_DRIVEN；hyperedge-size causal claim：NOT_SUPPORTED。
- Novelty：focused audit 未识别 exact collision；这不是 priority proof。
- Standalone SOTA：NO；strong-backbone complementarity：在 Cora + PubMed 的冻结协议下 SUPPORTED。
- Further tuning：不进行；Innovation 2：本次未启动。
- Protocol audit：V17.3 与 V17.4 是 intentional protocol difference，分别保留排名表，不合并。

## 审计来源

首要冻结来源：R_HSPE_FINAL_FROZEN/INNOVATION_1_FINAL.md、CANONICAL_PROTOCOL.json、SOURCE_HASHES.json、FINAL_RESULTS.json、PAPER_TABLE_A.md、PAPER_TABLE_B.md、LIMITATIONS.md、NOVELTY_BOUNDARY.md。方法以 R_HSPE_FROZEN/METHOD_DEFINITION.md 及其中 source_snapshot/v171.py、v16_stage1.py、stage0.py 为准。历史实验来源：HSPE_V17_1、HSPE_V17_2、R_HSPE_BENCHMARK_V17_3、R_HSPE_STRONG_BACKBONE_V17_4、R_HSPE_PROTOCOL_AUDIT_V17_5。具体指标与 protocol 标注见 METRIC_TABLES.md。


## 数字与协议审计

数值审计通过：Table 1/2 的配对均值、中位数和 seed wins 与所存 per-seed 记录一致；Table 4 的 R-HSPE/NCN/NCNC ranks 与 V17.3 CSV 一致；Citeseer 插件条目明确标为 validation-only、test 未访问。V17.3 与 V17.4 保持两张协议表，没有跨协议混排。
