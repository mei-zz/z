# V6 选定网络结构

状态：`NONE_SELECTED`

本轮没有候选通过文献碰撞审查，因此不能把任一候选称为“选定架构”，也没有生成伪模型图、参数量或训练结果。

## 被停止候选的可审计定义

为避免只因改名而重复研究，保留三条候选的数学定义：

1. 补图传播：`A^c=J-I-A`，节点更新使用 `N(A^c)H^lW_l`。
2. 边空间传播：`e_{i→j}^{l+1}=φ(e_{i→j}^l, Σ_{k∈N(i)\{j}}e_{k→i}^l)`。
3. 拓扑残差：`A_θ=A+Δ_θ(X,A)`，再使用 `N(A_θ)H^lW_l`。

分别对应补图双传播、line-graph/Hodge/非回溯边状态和 learnable topology augmentation，均已有直接或结构等价先例，故不满足 V6 的“实质性差异”要求。

## 现有 Parent 仅作审计基线

源码中的 Parent 是 `DCDLP`：目标 pair 先经 `mask_pair_edges` 从 message-passing edge list 移除，再进入 `NodeEncoder`，之后使用 degree/CN/residual 分支和 pair interaction。该结构不是 V6 新贡献；V6 不修改它。

## 参数、形状和复杂度

由于没有选定架构，V6 不报告虚假的输入输出张量、参数量、显存和时间。候选层面的资源风险已记录：显式补图在稀疏 Cora 上为稠密 `O(n^2)` 候选关系；边空间状态至少按有向边存储；拓扑残差需要额外候选边生成和 masking 审计。这些风险也是未授权训练的原因之一。

