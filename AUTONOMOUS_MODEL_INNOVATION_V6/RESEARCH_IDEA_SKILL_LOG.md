# Research Idea Skill 使用日志

状态：`SKILL_LOADED`

## 已读取文件

已完整读取已安装的 Research Ideation Skill 及直接引用文件：

1. `E:/CodexStorage/Home/skills/research-ideation/SKILL.md`
2. `references/literature-search-strategies.md`
3. `references/gap-analysis-guide.md`
4. `references/research-question-formulation.md`
5. `references/method-selection-guide.md`
6. `references/research-planning.md`

同时读取了 `E:/CodexStorage/Home/skills/stop-that-shit/SKILL.md`，用于执行用户规定的候选数量、最小验证和硬停止边界。

## 实际采用的方法

- 先从 V1–V5 建立问题边界和永久黑名单。
- 将候选写成明确的状态对象、传播算子和可证伪的输入场景。
- 对候选的结构 primitive、公式和官方代码做碰撞审查，而不只检索名字。
- 先做最便宜的代理等价性审查；若数学上已能被简单方法复现，则不进入 GPU。
- 只有通过 novelty、机制、泄漏和资源门槛后才允许 Cora HeaRT 训练。

## 本轮 Skill 决策

Skill 产生的结论是：静态同构无向 Cora 方向已经高度拥挤；补图传播、边空间传播和可学习拓扑增广分别落入已有论文或历史黑名单。没有一个候选同时满足独立结构差异和最小机制验证条件，因此没有启动训练。

