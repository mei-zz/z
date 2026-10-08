# -*- coding: utf-8 -*-
import json, pathlib, shutil, statistics, re
project=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main')
report_dir=project/'result/innovation2/TOPOLOGY_V28'
mirror=pathlib.Path(r'E:\Z\result\innovation2\TOPOLOGY_V28')
res=pathlib.Path(r'E:\Z\v28_results_complete')
review=report_dir/'V28_FINAL_RESEARCH_REVIEW.md'
t=review.read_text(encoding='utf-8')
inner=json.load(open(res/'12_PHASE_B_INNER_VALIDATION.json',encoding='utf-8-sig'))
new=json.load(open(res/'11_PHASE_B_NEW_SEED_RESULTS.json',encoding='utf-8-sig'))['new_seeds_only']
audit=json.load(open(r'E:\Z\V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json',encoding='utf-8-sig'))
feat=json.load(open(r'E:\Z\V28_INNER_FEATURE_AUDIT.json',encoding='utf-8-sig'))

def between(text,start,end,repl):
 i=text.index(start);j=text.index(end,i);return text[:i]+repl+'\n\n'+text[j:]
def set_line_prefix(text,prefix,newline):
 lines=text.splitlines(); found=False
 for i,line in enumerate(lines):
  if line.startswith(prefix):lines[i]=newline;found=True;break
 assert found,prefix
 return '\n'.join(lines)+'\n'

t=set_line_prefix(t,'V28_COMPLETE:','V28_COMPLETE: YES  ')
t=between(t,'| 对象 | 评审状态 | 结论 |','这里 EXPLORATORY', '''| 对象 | 评审状态 | 结论 |
| --- | --- | --- |
| GRAPH | REPLICATED | CE 主指标在新种子和独立训练池 inner-5 划分中，双数据集均超过 SHARED 与 ZERO6；inner-5/10 的 MRR 均值也为正。复现的是由共同邻居构成的预测信号，不代表新颖机制成立。 |
| MULT | REPLICATED | CE 主指标在新种子和 inner-5 划分中，双数据集均超过 SHARED 与 ZERO6；但 Cora inner-5 MRR 均值为负，排序收益的复现弱于 CE。 |
| GRAPH+MULT | UNRESOLVED | 原始 Phase A 有正向性能，但未稳定超过重复特征控制；未进入 Phase B top-2 的 inner 验证，不能确认条件互补。 |
| HDP CONDITIONAL | EXPLORATORY | 仅有早期三种子 CE 增量；HDP 身份打乱辨别力弱，H>0 子群不稳定，且未获得新种子或 inner 复验。 |''')
t=t.replace('这里 EXPLORATORY 不否认 GRAPH/MULT 的新种子复验：该较窄证据已成立。但V28原协议的 REPLICATED_SIGNAL 还要求独立训练池划分及容量控制，不能把未执行的验证视为通过。没有方法获得已确认的创新点2资格。',
'''这里的 **REPLICATED** 仅表示 V28 预设的 CE 主指标在新种子与 inner-5 训练池留出中满足正向门槛；它不等于机制独立、统计显著或创新成立。GRAPH 的 MRR 证据也稳定，MULT 的 Cora inner-5 MRR 则不支持排序改善。V28 的新颖性仍为 `NOT_AUDITED`，没有证据证明 GRAPH、MULT、融合或 HDP 是超越经典拓扑统计的独立创新。''')

sec12='''### 1.2 实验完成与恢复记录

此前的 inner 恢复尝试先遇到共享结构并发写入，随后 PubMed 特征写入因磁盘空间不足失败；这些早期错误日志和 `ERROR.json` 保留为历史记录。恢复脚本改为单一监督进程先构建并核验每个数据集的结构与上下文，再并发执行 seed 任务，未改模型、优化器、split、特征或采样定义。

本次恢复后的实验已完成：`RUN_STATUS.json` 为 `COMPLETE`，`12_PHASE_B_INNER_VALIDATION.json` 与 `13_EPOCH_STABILITY.json` 均为 `COMPLETE`。GRAPH 与 MULT 均满足新种子 CE 门槛，因此在 Cora、PubMed 各运行 seed 3–5、inner 5 与 10 epoch；合计 48 个融合方法训练单元。初始可用空间恢复后约 13 GiB，训练过程未再发生磁盘错误。'''
t=between(t,'### 1.2 停止事实优先于过期状态','### 1.3 最终审查完成确认',sec12)
sec13='''### 1.3 最终审查完成确认（2026-10-06）

**REVIEW_COMPLETE: YES；V28_COMPLETE: YES；TEST_OPENED: NO。** 本次已补齐预先指定的 inner 5/10 epoch 实验并重新审查 Phase A、Phase B、新种子、内部划分、机制对照和科学有效性。

内部训练共 48 个方法单元（2 个数据集 × 2 个预算 × 3 个种子 × 4 个 arm），48/48 有完成日志、原始 `result.json`、checkpoint 与验证分数文件；checkpoint 和 score-vector 哈希、报告与原始 JSON 一致性均通过。全部 48 条记录标记 `test_accessed=false`。六个 inner 特征缓存 READY 文件逐一哈希并可加载；Cora/PubMed 结构缓存的 `target_mask_oracle` 均为 PASS。5 与 10 epoch 使用相同初始化，10 epoch 的前 5 个负采样和排列轨迹与 5 epoch 逐项一致。训练日志中没有 traceback 或空间错误。

`topology28.check_frozen_all()` 在服务器上通过；V28 冻结清单内源码及 112 个历史拓扑缓存均无哈希差异。V28 机器生成的 `FINAL_REPORT.md` 保留原样；本人工审查按原协议把它的 `MECHANISM_SUPPORTED` 机器标签限定解释为受控性能信号，不能替代创新性论证。此前运行中断的错误文件也保留，恢复过程通过 `RECOVERY_AUDIT.json` 单独记录。

新增实验包已备份至 [V28_inner_experiment_20261006.tar.gz](E:/Z/DCDLP_Server_Backup_20261005/V28_inner_experiment_20261006.tar.gz)，服务器 SHA-256：`80fa901348c42bb15b55be5b3171ec61cf747f9040eba6f2d356d34fdaf12623`。新增执行审计见 [V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json](E:/Z/V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json) 与 [V28_INNER_FEATURE_AUDIT.json](E:/Z/V28_INNER_FEATURE_AUDIT.json)。`workspace_info` 工具在当前环境中不可用；逻辑工作区身份由现存审计文件、工作区路径和服务器检出路径交叉核对。'''
t=between(t,'### 1.3 最终审查完成确认','## 2. 已完成的Phase A：全部方法',sec13)

# Add an exact inner result summary generated from the paired raw per-seed results.
rows=[]
for ds in ('cora','pubmed'):
 for ep in ('5','10'):
  data=inner['datasets'][ds]['budgets'][ep]['datasets'][ds]['seed_results']
  for cand in ('GRAPH6','MULT6'):
   vals={}
   for ctrl in ('SHARED','ZERO6'):
    ce=[r['arms'][ctrl]['validation']['ce']-r['arms'][cand]['validation']['ce'] for r in data]
    mr=[r['arms'][cand]['validation']['mrr']-r['arms'][ctrl]['validation']['mrr'] for r in data]
    vals[ctrl]=(statistics.mean(ce),sum(v>0 for v in ce),statistics.mean(mr),sum(v>0 for v in mr))
   s,z=vals['SHARED'],vals['ZERO6']
   rows.append(f"| {ds} | {ep} | {cand} | {s[0]:+.5f} ({s[1]}/3) | {s[2]:+.5f} ({s[3]}/3) | {z[0]:+.5f} ({z[1]}/3) | {z[2]:+.5f} ({z[3]}/3) |")
inner_section='''### 3.1 补齐的 inner 训练池留出与 5/10 epoch 稳定性

表中 ΔCE 定义为“对照 CE − 候选 CE”，ΔMRR 定义为“候选 MRR − 对照 MRR”；正值表示候选更好。每格报告 3 个配对种子的均值及候选胜出数。

| 数据集 | epoch | 候选 | ΔCE vs SHARED (wins) | ΔMRR vs SHARED (wins) | ΔCE vs ZERO6 (wins) | ΔMRR vs ZERO6 (wins) |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
'''+ '\n'.join(rows)+'''

GRAPH 在四个数据集×预算组合中对 SHARED 与 ZERO6 的 CE/MRR 均值全部为正；Cora inner-10 对 SHARED 的 CE 为 2/3 种子胜出，但均值仍为正。MULT 的 CE 在四组中均为正；MRR 在 PubMed 两个预算均 3/3 胜出，Cora inner-5 均值为负且仅 1/3 胜出，inner-10 均值转正但仅 2/3 胜出。因此 MULT 按预注册 CE 主指标达到 `REPLICATED_SIGNAL`，其排序效应不能描述为跨数据集、跨预算稳定复现。

候选与 ZERO6 均为 30,594 个可训练参数；SHARED 为 30,529 个。故 ZERO6 是同参数量的零结构输入对照，SHARED 是原冻结强基线且少 65 个参数。以上数值属于独立 inner 训练池划分，不与原验证池结果合并；每组仅 3 个种子，均值/胜出数不构成经多重比较校正的显著性证据。'''
t=t.replace('## 4. GRAPH+MULT：性能与互补机制分开',inner_section+'\n\n## 4. GRAPH+MULT：性能与互补机制分开',1)

# Replace the old validity table and stale failure statements.
validity='''| 审查项 | 核验结果 | 边界 |
| --- | --- | --- |
| 规范结果完整性 | 既有 118 个规范结果单元的 checkpoint/score 哈希与重算 CE 通过；新 inner 阶段 48/48 原始结果与归档摘要一致 | 规范结果的历史复用单元不是新训练；inner 结果是 48 个新训练单元。 |
| 规范特征缓存 | 既有 17 个 READY 缓存哈希通过；本次 6 个 inner READY 缓存内每个数组哈希通过且可加载 | 前一次失败尝试产生的错误文件保留，但未被本次成功结果引用。 |
| 冻结源码/历史缓存 | 本次服务器 `check_frozen_all()` PASS；238 个源码/文件项和 112 个 V27 历史拓扑缓存无差异 | 历史文件由已校验本地归档恢复后核对；运行前不改源码定义。 |
| 配对训练轨迹 | 同 seed、arm、split 的 5/10 epoch 初始权重相同，前 5 个负采样及 permutation 轨迹逐项相同 | 不同 arm 的参数更新轨迹理应不同；不能要求跨方法参数状态相同。 |
| 内部分割和 target masking | 两数据集固定 inner split；结构 oracle PASS；6 个 READY 特征缓存哈希/加载全过 | 只证明这一个 seed=280016 的训练池留出，不是外部数据集复现。 |
| 内部结果与日志 | 48/48 结果 COMPLETE，checkpoint/score-vector SHA 匹配，48/48 完成标记；traceback/磁盘错误计数 0 | 6 个独立 inner-only C0 backbone 也完成 10 epoch，不与 48 个方法结果混计。 |
| test 封存 | 全部 inner 结果和 RUN_STATUS 均 `test_accessed/test_opened=false`；inner 输入只含 x/train/valid_pos/valid_neg | 源码审计和结果标记支持 test 未开启；不是操作系统级的文件访问追踪。 |'''
t=between(t,'| 审查项 | 核验结果 | 边界 |','### 6.1 split与target masking',validity)
inner_explain='''固定 seed=280016 将原训练池的 undirected 正例按 10% 留作 inner validation，剩余部分构成 inner-train。Cora 为 4,039 个 inner-train 正例、449 个 inner-validation 正例和 8,980 个负例；PubMed 分别为 33,908、3,768 和 75,360。每个 query 使用 20 个不重复的 uniform endpoint-corruption 负例，排除整个原训练池，不用原 validation/test 标签筛选。结构、raw-star、上下文、target mask 与归一化从 inner-train 重新构建，伪留出边不进入消息图或中心成员；每个数据集的 target-mask oracle 均 PASS。inner-only NCNC C0 backbone 从头训练 final-10 epoch，未复用 full-training checkpoint。由此 GRAPH/MULT 的内部预测信号有第二个边级划分来源；但只使用一个固定 inner split 与三个训练种子，不能等同独立外部数据复现。'''
t=between(t,'原训练池10%固定种子280016划分','### 6.2 选择偏差与优化限制',inner_explain)
select_bias='''V18–V28 多轮使用相同 Cora/PubMed 验证图设计和筛选方向；新种子 3–7 检验的是固定数据划分上的优化随机性。inner split 的留出正例来自原训练池、且在 V28 full-training 阶段未作为 validation target，因此为 GRAPH/MULT 增加了新的边级评价来源；候选先按 Phase B 全训练池的新种子 CE 规则筛选，inner 标签未用于候选筛选。它降低了对单一固定 validation edge set 的依赖，但只有一次固定 inner split、每格 3 seeds，仍不能抵消多轮方法探索、跨数据集比较和选择偏差，也不能给出未校正显著性结论。固定 final epoch 避免 best-checkpoint 挑选；5/10 epoch 轨迹配对一致。后续应把任何 V29 假设预登记，报告所有配对 seed 和每个控制，不访问 test。'''
t=between(t,'V18至V28多轮用相同Cora/PubMed验证集设计','## 7. 六个决策问题',select_bias)

q71='''### 7.1 哪个方法跨数据集收益最稳定？

**GRAPH6。** 新种子对 SHARED 的 CE/MRR 均为双数据集正向；inner 5 epoch 与 10 epoch 中，对 SHARED 和同参数 ZERO6 的 CE/MRR 均值在 Cora、PubMed 四组全部为正。特别是 PubMed 两个预算里所有配对种子都改善；Cora inner-5 MRR 也对两个对照 3/3 改善。Cora inner-10 的 CE 对 SHARED 有一个种子负向，因此不把均值提升表述为每种子无例外。'''
t=between(t,'### 7.1 哪个方法跨数据集收益最稳定？','### 7.2 哪个方法有尚未解释的结构增量？',q71)
q72='''### 7.2 哪个方法有尚未解释的结构增量？

**没有方法已证实拥有独立、非经典拓扑结构增量。** GRAPH 的预测信号现在达到 CE 复现标准，但它是常见邻居统计；MULT 的 CE 信号也达到复现标准，然而 Cora inner-5 MRR 不改善，而且 MULT 与 GRAPH 高度相关。GRAPH+MULT 的互补效应没有通过重复输入控制且没有 inner 结果。HDP 条件分支只有早期三种子正向 CE 线索，shuffle 辨别力和 H>0 子群证据不足。'''
t=between(t,'### 7.2 哪个方法有尚未解释的结构增量？','### 7.3 哪些收益属于经典统计或容量效应？',q72)
q73='''### 7.3 哪些收益属于经典统计或容量效应？

GRAPH 是经典共同邻居/2-section 投影统计；MULT 是端点独占加权关联投影可恢复的多重性与支持数，不能主张 hypergraph-exclusive。GRAPH/MULT 对同容量 ZERO6 的 inner CE 均值改善，表明正向输入本身有用，不能把其提升简单归因于“多了 65 个参数”。但 GM 对 GDUP 的 Phase A 结果不佳，重复输入可能改变特征几何、优化或校准；现有对照未证明 GRAPH+MULT 独立互补。HDP 的全局增量也可能来自常量/二值闭包状态或共享权重校准，尚无证据区分。'''
t=between(t,'### 7.3 哪些收益属于经典统计或容量效应？','### 7.4 若只允许一项V29，最值得验证的具体假设？',q73)
q74='''### 7.4 若只允许一项V29，最值得验证的具体假设？

建议继续只检验一个机制问题：**在固定 GRAPH+MULT 表征后，HDP 的真实超边分组身份是否比二值闭包状态更能改善 inner-train 留出泛化？** V28 的 GMH 相对 GM 有三种子 CE 线索，但与 GMG/GMS 竞争结果不一致、H>0 子群没有稳定收益、shuffle 实际改变率仅约 4%，而且 HDP 未进入新种子或 inner 复验。V29 应采用新种子和预登记训练池 split，锁定特征、模型和 5/10 epoch，不按 validation 子群调参；如果控制有效而真实 HDP 仍无增益，就停止这条结构身份解释。这里仅给出建议，不执行 V29。'''
t=between(t,'### 7.4 若只允许一项V29，最值得验证的具体假设？','### 7.5 最重要的两个反证对照？',q74)
q75='''### 7.5 最重要的两个反证对照？

1. **同容量二值闭包状态分支**：在相同 GM 上加入 `[I(H>0), log1p(I(H>0))]`，使用相同 6→8→1 残差分支、初始化、归一化、训练预算。若它与真实 HDP 表现相当或更好，则连续匹配数/超边身份增量解释不成立。
2. **有足够辨别力的度数保持 HDP-SHUFFLE**：保持超边行度数与支持节点列度数，预先规定实质重连率和 H 改变率最低门槛；达不到门槛的 shuffle 视为无效操纵，不得用作真实结构证据。若有效 shuffle 不输真实 HDP，身份机制不支持。

GM（不加 HDP）作为估计条件增量的基础参照始终保留。既有 GMG/PAIR 结果也应呈报，避免把第三槽重复输入解释遗漏；但最关键的两个机制反证分别是二值闭包和有效随机化。'''
t=between(t,'### 7.5 最重要的两个反证对照？','### 7.6 不访问test，如何验证稳定性？',q75)
q76='''### 7.6 不访问test，如何验证稳定性？

V28 已给出一种无 test 的执行方式：只从原训练正例固定抽出 10% inner validation；用剩余 90% 重建图、raw-star 和 target mask，过滤负例时只使用原训练池；inner-only C0 从头训练；5/10 epoch 从相同初始化出发并复用相同前五轮负采样/排列。V29 若执行，应在启动前冻结新 seeds、第二个独立 inner split、所有对照、模型预算和终止门槛，报告逐 seed CE/MRR 与 bootstrap 区间；test 分支继续封存。'''
t=between(t,'### 7.6 不访问test，如何验证稳定性？','## 8. 原始证据索引',q76)

# Add new evidence references and replace outdated log-completion paragraph.
t=t.replace('- [13_EPOCH_STABILITY.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/13_EPOCH_STABILITY.json)', '- [13_EPOCH_STABILITY.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/13_EPOCH_STABILITY.json)\n- [V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json)\n- [V28_INNER_FEATURE_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/V28_INNER_FEATURE_AUDIT.json)')
old='服务器原始日志：HYPERGRAPH_RESEARCH/TOPOLOGY_V28/logs/，全部日志进行了完成标记、epoch行数和错误扫描；正常训练日志的116个独立运行各有5个epoch与完成标记。canonical结果单元118还包含6个历史SHARED与4个D/A结果复用，不能混同独立重复次数。恢复日志与PubMed特征日志用于磁盘失败判定，结构/输入/模型从服务器只读哈希或数组检查。当前没有完整最终报告或已执行内部5/10融合方法结果可供审查，不能用PENDING文件冒充最终报告。'
newp='服务器 V28 原始训练日志保存在 `HYPERGRAPH_RESEARCH/TOPOLOGY_V28/logs/`。本次新增 48 个 inner 方法训练日志全部含 `V28_JOB_COMPLETE`，没有 traceback/空间错误；48 个 checkpoint、score-vector 和原始结果 JSON 哈希一致。6 个 inner READY 缓存均逐数组哈希通过并可加载；两数据集 structure/context 的 split 与 target-mask 审计 PASS。`RUN_STATUS.json`、`12_PHASE_B_INNER_VALIDATION.json`、`13_EPOCH_STABILITY.json` 均为 COMPLETE，且 `test_opened=false`。较早的磁盘失败与并发写入日志和 ERROR 文件作为尝试历史保留，不代表最终状态。V28 完整 inner 输入、特征、backbone、训练 checkpoint、分数和日志增量已归档到上述本地 tar.gz。既有规范结果的 118 单元统计仍含复用项，不与新增 48 次训练混计。'
assert old in t
t=t.replace(old,newp)
# Replace C2C block.
c2c='''```text
STATUS: REVIEWED
WORKSPACE: DCDLP-main
V28_COMPLETE: YES
GRAPH_STATUS: REPLICATED
MULT_STATUS: REPLICATED
GRAPH_MULT_STATUS: UNRESOLVED
HDP_CONDITIONAL_STATUS: EXPLORATORY
MOST_STABLE_METHOD: GRAPH6 (cross-dataset CE/MRR gains persist in new seeds and inner 5/10 budgets)
BEST_UNRESOLVED_MECHANISM: HDP grouping identity conditional on GRAPH+MULT versus binary closure-state/calibration
RECOMMENDED_V29_HYPOTHESIS: Does true HDP grouping improve a fixed GRAPH+MULT model on a pre-registered inner split beyond binary closure-state and effective degree-preserving shuffle?
MANDATORY_CONTROLS: matched binary closure-state branch; degree-preserving HDP-SHUFFLE with predeclared effective-power thresholds
TEST_OPENED: NO
NOVELTY_STATUS: NOT_AUDITED
NEXT_EXPECTED_STEP: WAIT_FOR_REVIEW
```'''
t=between(t,'```text\nSTATUS: REVIEWED','```',c2c)
t=t[:t.index('## 9. C2C HANDOFF')]+'## 9. C2C HANDOFF\n\n'+c2c+'\n'
# Check and write.
assert 'V28_COMPLETE: YES' in t and 'V28_COMPLETE: NO' not in t
assert 'result.json数量0' not in t and 'NOT_RUN' not in t and '没有可读取的最终融合' not in t
assert all(s in t for s in ['GRAPH_STATUS: REPLICATED','MULT_STATUS: REPLICATED','GRAPH_MULT_STATUS: UNRESOLVED','HDP_CONDITIONAL_STATUS: EXPLORATORY','TEST_OPENED: NO'])
review.write_text(t,encoding='utf-8')
for n in ('V28_FINAL_RESEARCH_REVIEW.md',):shutil.copy2(report_dir/n,mirror/n)
print('report written',len(t),'chars',review)
