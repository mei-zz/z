import json
from pathlib import Path
R=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\result\innovation2\TOPOLOGY_V28')
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
A=read('06_PHASE_A_METRICS.json');B=read('11_PHASE_B_NEW_SEED_RESULTS.json');S=read('09_HDP_SUBGROUP_ANALYSIS.json');D=read('01_FEATURE_DEPENDENCY_AUDIT.json');P=read('05_CONDITIONAL_TOPOLOGY_DIAGNOSTICS.json');C=read('08_CONDITIONAL_SHUFFLE_AUDIT.json');audit=json.loads(Path(r'E:\Z\v28_review_audit.json').read_text(encoding='utf-8-sig'))
lines=[]
def add(s=''):lines.append(s)
def table(headers,rows):
 add('| '+' | '.join(headers)+' |');add('| '+' | '.join(['---']*len(headers))+' |')
 for row in rows:add('| '+' | '.join(str(v) for v in row)+' |')
 add()
def f(x):return f'{x:.9f}'
def eff(data,ds,a,b):return data['datasets'][ds]['effects'][a+'_vs_'+b]
add('# V28 FINAL RESEARCH REVIEW — 创新点2决策审查')
add();add('STATUS: REVIEWED  \nWORKSPACE: DCDLP-main  \nV28_COMPLETE: NO  \nTEST_OPENED: NO  \nNOVELTY_STATUS: NOT_AUDITED')
add();add('## 1. 决策摘要与完成状态');add()
table(['对象','评审状态','结论'],[
 ['GRAPH','EXPLORATORY','当前跨数据集 CE/MRR 最稳定；新种子延续正收益，但内部划分、10epoch及重复输入控制的扩展复验缺失。'],
 ['MULT','EXPLORATORY','CE在两个数据集的新种子延续；Cora新种子MRR下降，未证实GRAPH之外独立信息。'],
 ['GRAPH+MULT','UNRESOLVED','优于MULT-DUP，但未超过GRAPH-DUP的双数据集平均CE；正向性能保留，互补机制未支持。'],
 ['HDP CONDITIONAL','EXPLORATORY','GMH对GM有3/3种子双数据集CE改善；没有新种子复验，Cora的GRAPH复用与HDP打乱控制未通过，活跃子群也未稳定获益。']])
add('这里 EXPLORATORY 不否认 GRAPH/MULT 的新种子复验：该较窄证据已成立。但V28原协议的 REPLICATED_SIGNAL 还要求独立训练池划分及容量控制，不能把未执行的验证视为通过。没有方法获得已确认的创新点2资格。')
add();add('### 1.1 工作区身份');add()
add('本会话可调用工具中不存在 workspace_info，不能声称已调用该工具。已读取 WORKSPACE_AUDIT.json，确认逻辑工作区 DCDLP-main、服务器历史检出 /home/ubuntu/lchr_v2、CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1；冻结源码哈希复核无失败。本地项目目录为 E:/我的资料库/Documents/Downloads/DCDLP-main，E:/Z为会话辅助目录。')
add();add('### 1.2 停止事实优先于过期状态');add()
add('Phase A、四组独立确定性预检查、新种子3–7的GRAPH6/MULT6及SHARED/ZERO6复验已完成。恢复后的六个inner-only NCNC backbone也已完成10epoch训练，但其结果不是GRAPH/MULT融合方法的内部验证结果。')
add();add('恢复监督日志显示，PubMed内部特征准备因磁盘不足失败：`OSError: Not enough free space to write 66481592 bytes`，随后异常记录也因 `OSError: [Errno 28] No space left on device` 写入失败。服务器根分区219G、可用0、占用100%。因此RUN_STATUS.json仍停在INNER_FEATURES/RUNNING，是过期状态；当前没有topology28.py或resume_inner28.py进程，GPU0%、14MiB。现存训练已停止，但计划实验没有全部完成。')
add();add('12_PHASE_B_INNER_VALIDATION.json、13_EPOCH_STABILITY.json均为NOT_RUN；FINAL_REPORT.md、10_RANKING_CALIBRATION_ANALYSIS.md、14_SIGNAL_LEDGER.md、15_DECISION.md均仅有PENDING占位。没有可读取的最终融合方法内部验证或5/10epoch稳定性结论。本次审查没有修复服务器、清理磁盘、续跑训练或改写这些状态。')
add();add('## 2. 已完成的Phase A：全部方法');add()
add('Cora/PubMed，种子0–2，固定final5epoch；均为原规范验证集。CE越低越好，MRR越高越好。所有融合方法同为6→8→1头，总30594参数；SHARED30529。')
table(['方法','Cora CE','Cora MRR','PubMed CE','PubMed MRR'],[[a,*[f(A['datasets'][ds]['metrics'][a][m]['mean']) for ds in ('cora','pubmed') for m in ('ce','mrr')]] for a in A['arms']])
add('GDUP=[G,G,0]；MDUP=[M,M,0]；GM=[G,M,0]；GP=[G,P,0]；GMH=[G,M,H]；GMS=[G,M,Hshuffle]；GMP=[G,M,P]；GMG=[G,M,G]；GMC=[G,M条件打乱,0]。V27的2D未归一化分支与本轮6D训练归一化分支属于不同实验配置，不能将绝对分数混成同一个方法的种子集合。')
add();add('## 3. GRAPH与MULT：完整八种子配对结果');add()
add('ΔCE=CE(SHARED)−CE(候选)，ΔMRR=MRR(候选)−MRR(SHARED)。种子0–2参与选择，3–7为新种子独立复验；验证候选集本身没有变化。以下逐种子表同时列同容量ZERO6的CE对照。')
for ds in ('cora','pubmed'):
 for arm in ('GRAPH6','MULT6'):
  add('### '+ds+' — '+arm);add()
  rr=B['all_eight_seeds']['datasets'][ds]['seed_results']
  table(['seed','SHARED CE','候选CE','ΔCE','SHARED MRR','候选MRR','ΔMRR','ΔCE vs ZERO6'],[[r['seed'],f(r['arms']['SHARED']['validation']['ce']),f(r['arms'][arm]['validation']['ce']),f(r['arms']['SHARED']['validation']['ce']-r['arms'][arm]['validation']['ce']),f(r['arms']['SHARED']['validation']['mrr']),f(r['arms'][arm]['validation']['mrr']),f(r['arms'][arm]['validation']['mrr']-r['arms']['SHARED']['validation']['mrr']),f(r['arms']['ZERO6']['validation']['ce']-r['arms'][arm]['validation']['ce'])] for r in rr])
add('### 3.1 新种子与八种子汇总分别报告');add()
for section in ('new_seeds_only','all_eight_seeds'):
 data=B[section];n=len(data['seeds']);add('#### '+section+'，种子'+str(data['seeds']));add()
 rows=[]
 for ds in ('cora','pubmed'):
  for arm in ('GRAPH6','MULT6'):
   for control in ('SHARED','ZERO6'):
    e=eff(data,ds,arm,control);interval=e['ce']['paired_bootstrap']['percentile95'];rows.append([ds,arm,control,f(e['ce']['mean']),f(e['ce']['median']),str(e['ce']['wins'])+'/'+str(n),f(e['mrr']['mean']),str(e['mrr']['wins'])+'/'+str(n),'['+f(interval[0])+', '+f(interval[1])+']'])
 table(['数据集','候选','对照','平均ΔCE','中位ΔCE','CE胜出','平均ΔMRR','MRR胜出','配对seed bootstrap95%区间'],rows)
add('区间来自10000次配对训练种子重采样；不能覆盖同一验证图反复选择、候选方法多重比较或数据划分不确定性，也不能作未经调整的显著性声明。全部八种子混有选择用种子0–2，新种子3–7是更重要的证据。')
add();add('### 3.2 同容量ZERO与重复特征控制');add()
table(['数据集','对比','平均ΔCE','CE胜出','平均ΔMRR'],[[ds,a+' vs '+b,f(eff(A,ds,a,b)['ce']['mean']),str(eff(A,ds,a,b)['ce']['wins'])+'/3',f(eff(A,ds,a,b)['mrr']['mean'])] for ds in ('cora','pubmed') for a,b in (('GRAPH6','ZERO6'),('GRAPH6','GDUP'),('MULT6','ZERO6'),('MULT6','MDUP'),('MULT6','GRAPH6'))])
add('GRAPH6/MULT6对ZERO6的新种子平均CE均正，故现有证据不支持“全由增加65参数且零输入就能解释”。但重复G或M在Phase A进一步改善CE；单特征没有超过各自重复输入对照，说明输入槽占用、参数化及优化轨迹仍影响收益。GDUP/MDUP没有运行种子3–7，也没有inner5/10结果；不能写成八种子通过重复特征控制。')
add();add('GRAPH最稳定的依据是新种子在双数据集对SHARED的CE、MRR均5/5获胜；MULT的CE同样5/5，但Cora新种子MRR平均下降。新种子MULT相对GRAPH可能有更低CE，而排序更弱，属于校准/排序差异，不能据此推断独立结构信息。')
add();add('## 4. GRAPH+MULT：性能与互补机制分开');add()
table(['数据集','GM对照','平均ΔCE','CE胜出','平均ΔMRR'],[[ds,b,f(eff(A,ds,'GM',b)['ce']['mean']),str(eff(A,ds,'GM',b)['ce']['wins'])+'/3',f(eff(A,ds,'GM',b)['mrr']['mean'])] for ds in ('cora','pubmed') for b in ('GDUP','MDUP','GRAPH6','MULT6','GP','ZERO6','SHARED','GMC')])
add('GM超过SHARED、ZERO6、单槽G/M并不自动说明互补。它对MDUP双数据集3/3改善CE，但对GDUP平均CE在两者均负：Cora0/3、PubMed1/3获胜。因此“G与M融合优于重复已知拓扑”尚未成立；不能简单判成只有容量，因为所有融合头同参数量，而重复输入改变有效参数化和特征几何。GP与GMC结果也让通用计数或条件校准解释继续可行。')
add();add('### 4.1 特征依赖与条件打乱的辨别力');add()
for ds in ('cora','pubmed'):
 x=D['datasets'][ds][0]['splits']['validation'];y=C['datasets'][ds][0]['audit']['validation'];add(f'- {ds}: GRAPH计数与MULT支持计数相等率{x["exact_equality_rate"]:.4%}，Pearson={x["Pearson"]:.6f}，Spearman={x["Spearman"]:.6f}，top10%重叠={x["top10pct_rank_overlap"]:.4%}；条件M打乱匹配率{y["matched_fraction"]:.4%}，实际M变化仅{y["actual_change_fraction"]:.4%}，状态{y["control_status"]}。')
add();add('两项统计数值确有不同，但大量零值/相同值使秩相关很高。条件打乱约96%匹配不等于有效破坏信息：仅约4%候选的M改变，按原规则为CONTROL_WEAK，不能将GM与GMC的接近或胜负当作决定性机制证据。MULT可由端点独占的加权关联投影重构；单个完整加权2-section是否足够，现有审计没有证明。所有raw-star特征都由原训练图确定，不能宣称native-hypergraph独占。')
add();add('训练拟合、验证评估的小型OLS探针只描述可恢复性，不进入模型训练，也不能直接证明有用的剩余信息。')
rows=[]
for ds in ('cora','pubmed'):
 for name in ('MULT','HDP','PAIR'):
  for j in range(2):
   vals=[r['probes'][name]['validation'][j]['R2'] for r in P['datasets'][ds]];rows.append([ds,name,j,f(min(vals)),f(max(vals))])
table(['数据集','预测目标','通道','R2最小','R2最大'],rows)
add();add('## 5. HDP条件增量：正向线索与反例');add()
table(['数据集','GMH对照','平均ΔCE','CE胜出','平均ΔMRR'],[[ds,b,f(eff(A,ds,'GMH',b)['ce']['mean']),str(eff(A,ds,'GMH',b)['ce']['wins'])+'/3',f(eff(A,ds,'GMH',b)['mrr']['mean'])] for ds in ('cora','pubmed') for b in ('GM','GMP','GMG','GMS')])
add('GMH对GM的CE改善在两数据集都是3/3，值得保留为条件性能线索，不能因V27独立HDP弱于GRAPH就删除。GMH对GMP的平均CE也略正。但Cora对GMG与GMS都是0/3改善，PubMed两项虽有平均CE优势，MRR却略弱；超边分组身份的跨数据集解释未得到支持。GMG是第三槽GRAPH复用控制，不是GDUP；两者定义必须分清。GMH未入选最多两个Phase B假设，所以不存在HDP的八种子或内部验证结果。')
add();add('### 5.1 H活跃子群：逐种子证据');add()
rows=[]
for ds in ('cora','pubmed'):
 for r in S['datasets'][ds]:
  for name in ('H0','Hpositive','H2plus'):
   x=r['subgroups'][name];rows.append([ds,r['seed'],name,x['positives'],x['negatives'],f(x['positive_rate']),f(x['CE']['GM']),f(x['CE']['GMH']),f(x['per_candidate_DeltaCE_distribution']['mean']),f(x['average_score_GMH_minus_GM'])])
table(['数据集','seed','子群','正例','负例','正例率','GM CE','GMH CE','平均逐候选ΔCE','GMH−GM平均score'],rows)
add('关键反证：Cora H>0子群三个种子CE全部恶化；PubMed H>0仅seed0改善、seed1/2恶化。H≥2在两个数据集的所有三个种子均恶化。H=0子群反而全部改善。H≥2嵌套在H>0中，不能将两者计数相加。整体CE正向收益主要出现在多数的H=0候选，不能描述成“匹配资源瓶颈活跃群稳定获益”。共同训练与归一化后，H=0仍可产生常量特征状态、改变共享权重或决策校准；这是可检验的解释，不是已证实机制。')
add();add('值得进行有限的新种子反证性复验，但不值得直接扩展K=3、path-GNN或把H>0子群选成优化目标。当前没有已确认的、未被经典拓扑/输入参数化解释的结构增量。最值得澄清的剩余线索是HDP在GM条件下的全局CE增量及其H=0校准来源。')
add();add('## 6. 科学有效性与缺失证据');add()
table(['审查项','核验结果','边界'],[
 ['规范结果完整性',f'{audit["canonical_result_cells"]}个结果单元checkpoint/score哈希与重算CE全部通过','78个PhaseA单元+40个新种子单元；不是118次独立重新训练，含历史及D阶段复用。'],
 ['规范特征缓存',f'{len(audit["canonical_feature_caches"])}个READY缓存全部匹配各自文件与归一化哈希','原规范协议证据可用。'],
 ['冻结源码/历史缓存','哈希失败0','创新点1、历史源文件与V27特征未改动。'],
 ['配对训练轨迹','所有方法training_trace与initialization一致','参数值优化轨迹因方法不同应不同；重复同一方法才要求trajectory hash完全相同。'],
 ['确定性预检查','GM/GMH/GMS/GMP独立两次全部通过','特征、checkpoint、score、history、训练轨迹均一致。'],
 ['并发修复后共享结构','Cora/PubMed structure和context实际SHA均匹配RECOVERY_AUDIT','恢复日志为单监督进程先构建，再启动seed任务；target-mask oracle PASS。'],
 ['内部backbone','6个inner C0 final10 checkpoint匹配记录、test_accessed均false','它们不是GRAPH/MULT/SHARED/ZERO6融合训练的内部结果。'],
 ['内部融合方法结果','result.json数量0；5/10稳定性NOT_RUN','所有相关比较为UNRESOLVED，不得从canonical5推断inner10。'],
 ['内部特征完整性',f'{len(audit["invalid_inner_npy"])}个现存npy结构加载失败','不能将部分缓存、只有READY/文件名或已完成backbone视为整轮有效。'],
 ['test封存','所有规范结果及内部backbone test_accessed=false；源码只用sealed False分支','证据支持V28未开启test；这不是操作系统级全文件访问追踪。']])
add('截断文件（未修复、未使用）：')
for r in audit['invalid_inner_npy']:add('- '+r['path']+'：'+r['error'])
add();add('### 6.1 split与target masking');add()
table(['数据集','inner训练正例','inner验证正例','验证负例','undirected正例不相交','负例无inner训练冲突'],[[ds,r['train_count'],r['validation_count'],r['negative_count'],r['disjoint'],r['no_negative_training_collision']] for ds,r in audit['inner_split'].items()])
add('原训练池10%固定种子280016划分；每查询20个不重复端点腐蚀负例，过滤原训练池，未借原validation/test标签过滤。重建结构只用inner-train；候选训练目标从消息图/两中心成员中移除，HDP再排除共同含两端点超边。inner-only backbone从头训练，未复用观察过pseudo-heldout边的full-training checkpoint。输入与结构级隔离有通过证据，但未完成的融合训练不能得到内部泛化结论。')
add();add('### 6.2 选择偏差与优化限制');add()
add('V18至V28多轮用相同Cora/PubMed验证集设计、筛选方向；V28从13个方法观察多个对照，再选择GRAPH/MULT。新随机种子独立检验优化随机性，但同一固定验证图仍承受跨轮适应性选择。8seed/3–7 seed bootstrap均不能校正这种偏差；不应宣称统计显著的新机制。固定final epoch排除了best-checkpoint选择，但不消除方法/训练预算选择。inner划分本应提供第二来源，现阶段只有分割与backbone完成，尚无目标方法验证。因此对完整研究结论必须降级，而不是否认已核验的性能观察。')
add();add('## 7. 六个决策问题');add()
add('### 7.1 哪个方法跨数据集收益最稳定？');add();add('GRAPH6。新种子3–7对SHARED在Cora/PubMed的CE、MRR均5/5改善；八种子的排序也较MULT一致。它是当前最可靠的经典拓扑增强基线，不是已成立的新颖机制。内部划分及10epoch仍缺失。')
add();add('### 7.2 哪个方法有尚未解释的结构增量？');add();add('没有方法已证实独立结构增量。HDP条件分支有尚未充分解释的CE性能增量，但真实超边身份控制不一致、H活跃群普遍无益，可能是零闭包状态校准或额外输入参数化。GM未证明优于GDUP，MULT也未证明GRAPH之外的稳定预测增量。')
add();add('### 7.3 哪些收益属于经典统计或容量效应？');add();add('GRAPH使用经典投影共同邻居；MULT使用可由端点独占加权关联投影恢复的多重性与支持数。单特征对同容量ZERO的改善支持真实拓扑输入有用，不支持纯零输入容量解释。GDUP/MDUP及GMG的进一步改善提示输入复制、有效参数化、优化或校准也能解释部分组合收益；尚不能把它们定性为全部纯容量，更不能把经典统计融合重新命名为创新点2。')
add();add('### 7.4 若只允许一项V29，最值得验证的具体假设？');add();add('建议一个反证优先的“闭包状态 vs 超边匹配身份”实验：在固定G/M条件下，GMH的新增CE改善是否只由稀疏闭包零/非零状态与校准解释，而真实匹配数和超边分组还具有独立泛化价值。主对照GM保持不变；目标GMH保持原HDP定义。预期证据必须同时来自新种子、独立训练池划分，以及H=0/H>0预先定义子群。现有H>0反证使资源瓶颈机制的先验支持较弱，此实验目的应是排除错误解释，而不是rescue调参。')
add();add('### 7.5 最重要的两个反证对照？');add();add('1. **闭包状态对照**：GM第三槽使用两维 `[log1p(I(H>0)), I(H>0)]`，沿用同一个6→8→1分支、同参数量、训练期拟合归一化和共同初始化。若它与GMH等效或更好，连续最大匹配/资源瓶颈解释缺少支持。还应记录该指示变量与G>0是否逐候选等价；若等价，进一步回到经典图闭包信息。\n2. **度数保持的HDP-SHUFFLE对照**：沿用真实HDP所用G/M、超边行度数和支持节点列度数不变的打乱；必须同时报告实质重连率和H实际变化率。若控制弱或多数H未改变，就不能把未胜出写成决定性否定；若控制有辨别力且GMH不胜，则真实超边身份解释受反证。')
add();add('既有GMG/PAIR表现是不能删除的第三槽重复/通用计数证据；后续预算若允许，它们应保持为辅助对照。这里指定的两项主反证分别针对“只有零/非零状态”和“只有端点度数/多重性”，不是把已有Cora控制失败掩盖掉。')
add();add('### 7.6 不访问test，如何验证稳定性？');add();add('预登记新种子（例如8–12）和固定原训练池inner划分；只在inner-train构建raw-star、消息图、归一化和训练checkpoint。方法、控制、学习率、5/10epoch final预算事先固定，每预算从共同初始化训练，报告所有配对种子CE/MRR、校准指标及固定H子群；保留两数据集失败结果，不从validation标签选择阈值。新种子仍使用相同图时只检验优化稳定性；训练池第二划分检验另一评价来源，但还不等同独立外部数据。最好明确将这些方向当作V28后提出的新假设，而不是回溯声称原先预登记。报告paired bootstrap不作未经校正的显著性宣称。本次不执行任何这些建议。')
add();add('## 8. 原始证据索引');add()
add('以下均已读取或从原始结果重算核验；历史文件保持原样。')
for n in ('00_PROTOCOL.md','WORKSPACE_AUDIT.json','RUN_MANIFEST.json','RUN_STATUS.json','SOURCE_HASHES.json','02_BASELINE_REPRODUCTION.json','03_PARAMETER_AND_INITIALIZATION_AUDIT.json','04_DETERMINISM_PRECHECK.json','06_PHASE_A_METRICS.json','07_PHASE_A_PAIRED_CONTRASTS.json','11_PHASE_B_NEW_SEED_RESULTS.json','PHASE_B_SELECTION.json','01_FEATURE_DEPENDENCY_AUDIT.json','05_CONDITIONAL_TOPOLOGY_DIAGNOSTICS.json','08_CONDITIONAL_SHUFFLE_AUDIT.json','09_HDP_SUBGROUP_ANALYSIS.json','INNER_SPLIT_AUDIT.json','RECOVERY_AUDIT.json','12_PHASE_B_INNER_VALIDATION.json','13_EPOCH_STABILITY.json','recovery_supervisor.log'):add('- ['+n+']('+n+')')
add();add('服务器原始日志：HYPERGRAPH_RESEARCH/TOPOLOGY_V28/logs/，全部日志进行了完成标记、epoch行数和错误扫描；正常训练日志的116个独立运行各有5个epoch与完成标记。canonical结果单元118还包含6个历史SHARED与4个D/A结果复用，不能混同独立重复次数。恢复日志与PubMed特征日志用于磁盘失败判定，结构/输入/模型从服务器只读哈希或数组检查。当前没有完整最终报告或已执行内部5/10融合方法结果可供审查，不能用PENDING文件冒充最终报告。')
add();add('## 9. C2C HANDOFF');add()
add('```text\nSTATUS: REVIEWED\nWORKSPACE: DCDLP-main\nV28_COMPLETE: NO\nGRAPH_STATUS: EXPLORATORY\nMULT_STATUS: EXPLORATORY\nGRAPH_MULT_STATUS: UNRESOLVED\nHDP_CONDITIONAL_STATUS: EXPLORATORY\nMOST_STABLE_METHOD: GRAPH6 (canonical new-seed CE/MRR gains; inner/10epoch evidence missing)\nBEST_UNRESOLVED_MECHANISM: HDP conditional CE increment versus zero-closure calibration; no confirmed independent structural increment\nRECOMMENDED_V29_HYPOTHESIS: Does exact HDP add conditional generalization beyond G/M and a binary closure-state feature?\nMANDATORY_CONTROLS: capacity-matched binary closure-state third block; degree-preserving HDP-SHUFFLE with effective-power audit\nTEST_OPENED: NO\nNEXT_EXPECTED_STEP: WAIT_FOR_REVIEW\n```')
(R/'V28_FINAL_RESEARCH_REVIEW.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('REVIEW_WRITTEN',R/'V28_FINAL_RESEARCH_REVIEW.md')
