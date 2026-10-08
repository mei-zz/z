# V28 FINAL RESEARCH REVIEW — 创新点2决策审查

STATUS: REVIEWED  
REVIEW_COMPLETE: YES  
REVIEW_UPDATED: 2026-10-06 (America/Los_Angeles)  
WORKSPACE: DCDLP-main  
V28_COMPLETE: YES  
TEST_OPENED: NO  
NOVELTY_STATUS: NOT_AUDITED

## 1. 决策摘要与完成状态

| 对象 | 评审状态 | 结论 |
| --- | --- | --- |
| GRAPH | REPLICATED | CE 主指标在新种子和独立训练池 inner-5 划分中，双数据集均超过 SHARED 与 ZERO6；inner-5/10 的 MRR 均值也为正。复现的是由共同邻居构成的预测信号，不代表新颖机制成立。 |
| MULT | REPLICATED | CE 主指标在新种子和 inner-5 划分中，双数据集均超过 SHARED 与 ZERO6；但 Cora inner-5 MRR 均值为负，排序收益的复现弱于 CE。 |
| GRAPH+MULT | UNRESOLVED | 原始 Phase A 有正向性能，但未稳定超过重复特征控制；未进入 Phase B top-2 的 inner 验证，不能确认条件互补。 |
| HDP CONDITIONAL | EXPLORATORY | 仅有早期三种子 CE 增量；HDP 身份打乱辨别力弱，H>0 子群不稳定，且未获得新种子或 inner 复验。 |

这里的 **REPLICATED** 仅表示 V28 预设的 CE 主指标在新种子与 inner-5 训练池留出中满足正向门槛；它不等于机制独立、统计显著或创新成立。GRAPH 的 MRR 证据也稳定，MULT 的 Cora inner-5 MRR 则不支持排序改善。V28 的新颖性仍为 `NOT_AUDITED`，没有证据证明 GRAPH、MULT、融合或 HDP 是超越经典拓扑统计的独立创新。

### 1.1 工作区身份

本会话可调用工具中不存在 workspace_info，不能声称已调用该工具。已读取 WORKSPACE_AUDIT.json，确认逻辑工作区 DCDLP-main、服务器历史检出 /home/ubuntu/lchr_v2、CHRI_DETERMINISTIC_CANONICAL_PROTOCOL_V1；冻结源码哈希复核无失败。本地项目目录为 E:/我的资料库/Documents/Downloads/DCDLP-main，E:/Z为会话辅助目录。

### 1.2 实验完成与恢复记录

此前的 inner 恢复尝试先遇到共享结构并发写入，随后 PubMed 特征写入因磁盘空间不足失败；这些早期错误日志和 `ERROR.json` 保留为历史记录。恢复脚本改为单一监督进程先构建并核验每个数据集的结构与上下文，再并发执行 seed 任务，未改模型、优化器、split、特征或采样定义。

本次恢复后的实验已完成：`RUN_STATUS.json` 为 `COMPLETE`，`12_PHASE_B_INNER_VALIDATION.json` 与 `13_EPOCH_STABILITY.json` 均为 `COMPLETE`。GRAPH 与 MULT 均满足新种子 CE 门槛，因此在 Cora、PubMed 各运行 seed 3–5、inner 5 与 10 epoch；合计 48 个融合方法训练单元。初始可用空间恢复后约 13 GiB，训练过程未再发生磁盘错误。

### 1.3 最终审查完成确认（2026-10-06）

**REVIEW_COMPLETE: YES；V28_COMPLETE: YES；TEST_OPENED: NO。** 本次已补齐预先指定的 inner 5/10 epoch 实验并重新审查 Phase A、Phase B、新种子、内部划分、机制对照和科学有效性。

内部训练共 48 个方法单元（2 个数据集 × 2 个预算 × 3 个种子 × 4 个 arm），48/48 有完成日志、原始 `result.json`、checkpoint 与验证分数文件；checkpoint 和 score-vector 哈希、报告与原始 JSON 一致性均通过。全部 48 条记录标记 `test_accessed=false`。六个 inner 特征缓存 READY 文件逐一哈希并可加载；Cora/PubMed 结构缓存的 `target_mask_oracle` 均为 PASS。5 与 10 epoch 使用相同初始化，10 epoch 的前 5 个负采样和排列轨迹与 5 epoch 逐项一致。训练日志中没有 traceback 或空间错误。

`topology28.check_frozen_all()` 在服务器上通过；V28 冻结清单内源码及 112 个历史拓扑缓存均无哈希差异。V28 机器生成的 `FINAL_REPORT.md` 保留原样；本人工审查按原协议把它的 `MECHANISM_SUPPORTED` 机器标签限定解释为受控性能信号，不能替代创新性论证。此前运行中断的错误文件也保留，恢复过程通过 `RECOVERY_AUDIT.json` 单独记录。

新增实验包已备份至 [V28_inner_experiment_20261006.tar.gz](E:/Z/DCDLP_Server_Backup_20261005/V28_inner_experiment_20261006.tar.gz)，服务器 SHA-256：`80fa901348c42bb15b55be5b3171ec61cf747f9040eba6f2d356d34fdaf12623`。新增执行审计见 [V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json](E:/Z/V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json) 与 [V28_INNER_FEATURE_AUDIT.json](E:/Z/V28_INNER_FEATURE_AUDIT.json)。`workspace_info` 工具在当前环境中不可用；逻辑工作区身份由现存审计文件、工作区路径和服务器检出路径交叉核对。

## 2. 已完成的Phase A：全部方法

Cora/PubMed，种子0–2，固定final5epoch；均为原规范验证集。CE越低越好，MRR越高越好。所有融合方法同为6→8→1头，总30594参数；SHARED30529。
| 方法 | Cora CE | Cora MRR | PubMed CE | PubMed MRR |
| --- | --- | --- | --- | --- |
| SHARED | 0.339870371 | 0.737686808 | 0.127129717 | 0.921859533 |
| ZERO6 | 0.337741158 | 0.735432644 | 0.130896788 | 0.920679870 |
| GRAPH6 | 0.332671683 | 0.737178515 | 0.122627813 | 0.929120288 |
| MULT6 | 0.334024684 | 0.736884259 | 0.124549528 | 0.926803310 |
| GDUP | 0.328784334 | 0.740484355 | 0.119680506 | 0.931859133 |
| MDUP | 0.330053206 | 0.735957656 | 0.123023488 | 0.928576325 |
| GM | 0.329444745 | 0.739287089 | 0.119748983 | 0.931385987 |
| GP | 0.329242133 | 0.739523255 | 0.119896944 | 0.932289934 |
| GMH | 0.327350246 | 0.740041130 | 0.117817637 | 0.932603320 |
| GMS | 0.327225986 | 0.740041130 | 0.118614949 | 0.933237611 |
| GMP | 0.327455318 | 0.739301798 | 0.118005057 | 0.932700553 |
| GMG | 0.327181991 | 0.739518317 | 0.117951172 | 0.932893588 |
| GMC | 0.329318146 | 0.738872738 | 0.120165658 | 0.931007770 |

GDUP=[G,G,0]；MDUP=[M,M,0]；GM=[G,M,0]；GP=[G,P,0]；GMH=[G,M,H]；GMS=[G,M,Hshuffle]；GMP=[G,M,P]；GMG=[G,M,G]；GMC=[G,M条件打乱,0]。V27的2D未归一化分支与本轮6D训练归一化分支属于不同实验配置，不能将绝对分数混成同一个方法的种子集合。

## 3. GRAPH与MULT：完整八种子配对结果

ΔCE=CE(SHARED)−CE(候选)，ΔMRR=MRR(候选)−MRR(SHARED)。种子0–2参与选择，3–7为新种子独立复验；验证候选集本身没有变化。以下逐种子表同时列同容量ZERO6的CE对照。
### cora — GRAPH6

| seed | SHARED CE | 候选CE | ΔCE | SHARED MRR | 候选MRR | ΔMRR | ΔCE vs ZERO6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.402660125 | 0.388897157 | 0.013762968 | 0.712718567 | 0.712104891 | -0.000613677 | 0.007369879 |
| 1 | 0.263901580 | 0.262218844 | 0.001682736 | 0.773519209 | 0.773973370 | 0.000454161 | 0.002183120 |
| 2 | 0.353049407 | 0.346899048 | 0.006150358 | 0.726822647 | 0.725457283 | -0.001365365 | 0.005655426 |
| 3 | 0.365252408 | 0.359726044 | 0.005526363 | 0.714191790 | 0.714641424 | 0.000449635 | 0.001774955 |
| 4 | 0.320132958 | 0.318737720 | 0.001395238 | 0.721886281 | 0.722868152 | 0.000981871 | 0.001805427 |
| 5 | 0.256175059 | 0.255379600 | 0.000795459 | 0.794104106 | 0.795667498 | 0.001563392 | 0.001103702 |
| 6 | 0.340289097 | 0.336677869 | 0.003611227 | 0.744595109 | 0.746052650 | 0.001457541 | 0.003873764 |
| 7 | 0.441416086 | 0.439194556 | 0.002221530 | 0.703370687 | 0.704004400 | 0.000633714 | 0.001711334 |

### cora — MULT6

| seed | SHARED CE | 候选CE | ΔCE | SHARED MRR | 候选MRR | ΔMRR | ΔCE vs ZERO6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.402660125 | 0.393912334 | 0.008747791 | 0.712718567 | 0.712679664 | -0.000038903 | 0.002354701 |
| 1 | 0.263901580 | 0.261749487 | 0.002152093 | 0.773519209 | 0.771755373 | -0.001763836 | 0.002652478 |
| 2 | 0.353049407 | 0.346412231 | 0.006637176 | 0.726822647 | 0.726217739 | -0.000604908 | 0.006142243 |
| 3 | 0.365252408 | 0.356788993 | 0.008463415 | 0.714191790 | 0.713126779 | -0.001065010 | 0.004712007 |
| 4 | 0.320132958 | 0.318280951 | 0.001852006 | 0.721886281 | 0.724008837 | 0.002122555 | 0.002262196 |
| 5 | 0.256175059 | 0.255864584 | 0.000310475 | 0.794104106 | 0.792202965 | -0.001901141 | 0.000618718 |
| 6 | 0.340289097 | 0.338652579 | 0.001636518 | 0.744595109 | 0.746179393 | 0.001584284 | 0.001899055 |
| 7 | 0.441416086 | 0.439544952 | 0.001871134 | 0.703370687 | 0.698617835 | -0.004752852 | 0.001360938 |

### pubmed — GRAPH6

| seed | SHARED CE | 候选CE | ΔCE | SHARED MRR | 候选MRR | ΔMRR | ΔCE vs ZERO6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.119889471 | 0.121915315 | -0.002025844 | 0.925167987 | 0.931117502 | 0.005949516 | 0.008185893 |
| 1 | 0.120831027 | 0.114899272 | 0.005931756 | 0.925220097 | 0.932929182 | 0.007709085 | 0.007128325 |
| 2 | 0.140668653 | 0.131068852 | 0.009599801 | 0.915190514 | 0.923314181 | 0.008123667 | 0.009492707 |
| 3 | 0.120680758 | 0.120542198 | 0.000138560 | 0.924680355 | 0.929614170 | 0.004933815 | 0.002498880 |
| 4 | 0.168735573 | 0.167100888 | 0.001634685 | 0.898149629 | 0.915129343 | 0.016979714 | -0.000164847 |
| 5 | 0.157847782 | 0.150727282 | 0.007120500 | 0.911007238 | 0.920210176 | 0.009202939 | 0.006002548 |
| 6 | 0.158367738 | 0.144299944 | 0.014067794 | 0.905977321 | 0.925623011 | 0.019645690 | 0.012691342 |
| 7 | 0.125885719 | 0.120391011 | 0.005494708 | 0.924392243 | 0.932842495 | 0.008450252 | 0.006391527 |

### pubmed — MULT6

| seed | SHARED CE | 候选CE | ΔCE | SHARED MRR | 候选MRR | ΔMRR | ΔCE vs ZERO6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0.119889471 | 0.124530128 | -0.004640657 | 0.925167987 | 0.930526876 | 0.005358890 | 0.005571080 |
| 1 | 0.120831027 | 0.117513559 | 0.003317468 | 0.925220097 | 0.930131348 | 0.004911252 | 0.004514037 |
| 2 | 0.140668653 | 0.131604897 | 0.009063757 | 0.915190514 | 0.919751706 | 0.004561192 | 0.008956663 |
| 3 | 0.120680758 | 0.120494599 | 0.000186159 | 0.924680355 | 0.928275421 | 0.003595066 | 0.002546478 |
| 4 | 0.168735573 | 0.161347041 | 0.007388532 | 0.898149629 | 0.908455271 | 0.010305642 | 0.005589000 |
| 5 | 0.157847782 | 0.151174760 | 0.006673022 | 0.911007238 | 0.918781506 | 0.007774268 | 0.005555070 |
| 6 | 0.158367738 | 0.144226027 | 0.014141711 | 0.905977321 | 0.920332288 | 0.014354967 | 0.012765259 |
| 7 | 0.125885719 | 0.122164065 | 0.003721654 | 0.924392243 | 0.931879799 | 0.007487556 | 0.004618473 |

### 3.1 新种子与八种子汇总分别报告

#### new_seeds_only，种子[3, 4, 5, 6, 7]

| 数据集 | 候选 | 对照 | 平均ΔCE | 中位ΔCE | CE胜出 | 平均ΔMRR | MRR胜出 | 配对seed bootstrap95%区间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cora | GRAPH6 | SHARED | 0.002709964 | 0.002221530 | 5/5 | 0.001017231 | 5/5 | [0.001320585, 0.004204430] |
| cora | GRAPH6 | ZERO6 | 0.002053837 | 0.001774955 | 5/5 | 0.001214088 | 5/5 | [0.001378298, 0.003027611] |
| cora | MULT6 | SHARED | 0.002826710 | 0.001852006 | 5/5 | -0.000802433 | 2/5 | [0.000930913, 0.005775754] |
| cora | MULT6 | ZERO6 | 0.002170583 | 0.001899055 | 5/5 | -0.000605575 | 2/5 | [0.001130853, 0.003479203] |
| pubmed | GRAPH6 | SHARED | 0.005691250 | 0.005494708 | 5/5 | 0.011842482 | 5/5 | [0.001808240, 0.009899418] |
| pubmed | GRAPH6 | ZERO6 | 0.005483890 | 0.006002548 | 4/5 | 0.011234927 | 5/5 | [0.001966134, 0.009392887] |
| pubmed | MULT6 | SHARED | 0.006422216 | 0.006673022 | 5/5 | 0.008703500 | 5/5 | [0.002780904, 0.010563962] |
| pubmed | MULT6 | ZERO6 | 0.006214856 | 0.005555070 | 5/5 | 0.008095945 | 5/5 | [0.003756701, 0.009693864] |

#### all_eight_seeds，种子[0, 1, 2, 3, 4, 5, 6, 7]

| 数据集 | 候选 | 对照 | 平均ΔCE | 中位ΔCE | CE胜出 | 平均ΔMRR | MRR胜出 | 配对seed bootstrap95%区间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cora | GRAPH6 | SHARED | 0.004393235 | 0.002916379 | 8/8 | 0.000445159 | 6/8 | [0.002102934, 0.007446203] |
| cora | GRAPH6 | ZERO6 | 0.003184701 | 0.001994274 | 8/8 | 0.001413506 | 7/8 | [0.001851671, 0.004716551] |
| cora | MULT6 | SHARED | 0.003958826 | 0.002011614 | 8/8 | -0.000802476 | 2/8 | [0.001884984, 0.006203781] |
| cora | MULT6 | ZERO6 | 0.002750292 | 0.002308448 | 8/8 | 0.000165871 | 4/8 | [0.001689718, 0.003988497] |
| pubmed | GRAPH6 | SHARED | 0.005245245 | 0.005713232 | 7/8 | 0.010124334 | 8/8 | [0.001903232, 0.008739452] |
| pubmed | GRAPH6 | ZERO6 | 0.006528297 | 0.006759926 | 7/8 | 0.010186986 | 8/8 | [0.003830455, 0.009044401] |
| pubmed | MULT6 | SHARED | 0.004981456 | 0.005197338 | 7/8 | 0.007293604 | 8/8 | [0.001165725, 0.008666263] |
| pubmed | MULT6 | ZERO6 | 0.006264507 | 0.005563075 | 8/8 | 0.007356256 | 8/8 | [0.004439284, 0.008552211] |

区间来自10000次配对训练种子重采样；不能覆盖同一验证图反复选择、候选方法多重比较或数据划分不确定性，也不能作未经调整的显著性声明。全部八种子混有选择用种子0–2，新种子3–7是更重要的证据。

### 3.2 同容量ZERO与重复特征控制

| 数据集 | 对比 | 平均ΔCE | CE胜出 | 平均ΔMRR |
| --- | --- | --- | --- | --- |
| cora | GRAPH6 vs ZERO6 | 0.005069475 | 3/3 | 0.001745871 |
| cora | GRAPH6 vs GDUP | -0.003887349 | 0/3 | -0.003305841 |
| cora | MULT6 vs ZERO6 | 0.003716474 | 3/3 | 0.001451615 |
| cora | MULT6 vs MDUP | -0.003971478 | 0/3 | 0.000926603 |
| cora | MULT6 vs GRAPH6 | -0.001353001 | 2/3 | -0.000294256 |
| pubmed | GRAPH6 vs ZERO6 | 0.008268975 | 3/3 | 0.008440419 |
| pubmed | GRAPH6 vs GDUP | -0.002947307 | 1/3 | -0.002738845 |
| pubmed | MULT6 vs ZERO6 | 0.006347260 | 3/3 | 0.006123441 |
| pubmed | MULT6 vs MDUP | -0.001526040 | 0/3 | -0.001773015 |
| pubmed | MULT6 vs GRAPH6 | -0.001921715 | 0/3 | -0.002316978 |

GRAPH6/MULT6对ZERO6的新种子平均CE均正，故现有证据不支持“全由增加65参数且零输入就能解释”。但重复G或M在Phase A进一步改善CE；单特征没有超过各自重复输入对照，说明输入槽占用、参数化及优化轨迹仍影响收益。GDUP/MDUP没有运行种子3–7，也没有inner5/10结果；不能写成八种子通过重复特征控制。

GRAPH最稳定的依据是新种子在双数据集对SHARED的CE、MRR均5/5获胜；MULT的CE同样5/5，但Cora新种子MRR平均下降。新种子MULT相对GRAPH可能有更低CE，而排序更弱，属于校准/排序差异，不能据此推断独立结构信息。

### 3.3 补齐的 inner 训练池留出与 5/10 epoch 稳定性

表中 ΔCE 定义为“对照 CE − 候选 CE”，ΔMRR 定义为“候选 MRR − 对照 MRR”；正值表示候选更好。每格报告 3 个配对种子的均值及候选胜出数。

| 数据集 | epoch | 候选 | ΔCE vs SHARED (wins) | ΔMRR vs SHARED (wins) | ΔCE vs ZERO6 (wins) | ΔMRR vs ZERO6 (wins) |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| cora | 5 | GRAPH6 | +0.00287 (2/3) | +0.00208 (3/3) | +0.00515 (3/3) | +0.00264 (3/3) |
| cora | 5 | MULT6 | +0.00448 (3/3) | -0.00096 (1/3) | +0.00676 (3/3) | -0.00040 (1/3) |
| cora | 10 | GRAPH6 | +0.02236 (2/3) | +0.00437 (3/3) | +0.02391 (3/3) | +0.00519 (3/3) |
| cora | 10 | MULT6 | +0.01024 (2/3) | +0.00190 (2/3) | +0.01179 (3/3) | +0.00273 (3/3) |
| pubmed | 5 | GRAPH6 | +0.01316 (3/3) | +0.00922 (3/3) | +0.01050 (3/3) | +0.00943 (3/3) |
| pubmed | 5 | MULT6 | +0.01392 (3/3) | +0.00739 (3/3) | +0.01126 (3/3) | +0.00759 (3/3) |
| pubmed | 10 | GRAPH6 | +0.02532 (3/3) | +0.01036 (3/3) | +0.02455 (3/3) | +0.01045 (3/3) |
| pubmed | 10 | MULT6 | +0.02298 (3/3) | +0.00817 (3/3) | +0.02220 (3/3) | +0.00826 (3/3) |

GRAPH 在四个数据集×预算组合中对 SHARED 与 ZERO6 的 CE/MRR 均值全部为正；Cora inner-10 对 SHARED 的 CE 为 2/3 种子胜出，但均值仍为正。MULT 的 CE 在四组中均为正；MRR 在 PubMed 两个预算均 3/3 胜出，Cora inner-5 均值为负且仅 1/3 胜出，inner-10 均值转正但仅 2/3 胜出。因此 MULT 按预注册 CE 主指标达到 `REPLICATED_SIGNAL`，其排序效应不能描述为跨数据集、跨预算稳定复现。

候选与 ZERO6 均为 30,594 个可训练参数；SHARED 为 30,529 个。故 ZERO6 是同参数量的零结构输入对照，SHARED 是原冻结强基线且少 65 个参数。以上数值属于独立 inner 训练池划分，不与原验证池结果合并；每组仅 3 个种子，均值/胜出数不构成经多重比较校正的显著性证据。

## 4. GRAPH+MULT：性能与互补机制分开

| 数据集 | GM对照 | 平均ΔCE | CE胜出 | 平均ΔMRR |
| --- | --- | --- | --- | --- |
| cora | GDUP | -0.000660411 | 0/3 | -0.001197266 |
| cora | MDUP | 0.000608460 | 3/3 | 0.003329434 |
| cora | GRAPH6 | 0.003226938 | 3/3 | 0.002108575 |
| cora | MULT6 | 0.004579939 | 3/3 | 0.002402831 |
| cora | GP | -0.000202613 | 0/3 | -0.000236165 |
| cora | ZERO6 | 0.008296413 | 3/3 | 0.003854445 |
| cora | SHARED | 0.010425625 | 3/3 | 0.001600281 |
| cora | GMC | -0.000126599 | 0/3 | 0.000414351 |
| pubmed | GDUP | -0.000068477 | 1/3 | -0.000473146 |
| pubmed | MDUP | 0.003274505 | 3/3 | 0.002809662 |
| pubmed | GRAPH6 | 0.002878830 | 2/3 | 0.002265698 |
| pubmed | MULT6 | 0.004800545 | 3/3 | 0.004582677 |
| pubmed | GP | 0.000147961 | 2/3 | -0.000903947 |
| pubmed | ZERO6 | 0.011147805 | 3/3 | 0.010706117 |
| pubmed | SHARED | 0.007380734 | 3/3 | 0.009526454 |
| pubmed | GMC | 0.000416675 | 1/3 | 0.000378216 |

GM超过SHARED、ZERO6、单槽G/M并不自动说明互补。它对MDUP双数据集3/3改善CE，但对GDUP平均CE在两者均负：Cora0/3、PubMed1/3获胜。因此“G与M融合优于重复已知拓扑”尚未成立；不能简单判成只有容量，因为所有融合头同参数量，而重复输入改变有效参数化和特征几何。GP与GMC结果也让通用计数或条件校准解释继续可行。

### 4.1 特征依赖与条件打乱的辨别力

- cora: GRAPH计数与MULT支持计数相等率97.2479%，Pearson=0.242066，Spearman=0.998383，top10%重叠=97.1014%；条件M打乱匹配率94.9846%，实际M变化仅3.8204%，状态CONTROL_WEAK。
- pubmed: GRAPH计数与MULT支持计数相等率98.3797%，Pearson=0.910337，Spearman=0.999756，top10%重叠=100.0000%；条件M打乱匹配率96.9765%，实际M变化仅3.8916%，状态CONTROL_WEAK。

两项统计数值确有不同，但大量零值/相同值使秩相关很高。条件打乱约96%匹配不等于有效破坏信息：仅约4%候选的M改变，按原规则为CONTROL_WEAK，不能将GM与GMC的接近或胜负当作决定性机制证据。MULT可由端点独占的加权关联投影重构；单个完整加权2-section是否足够，现有审计没有证明。所有raw-star特征都由原训练图确定，不能宣称native-hypergraph独占。

训练拟合、验证评估的小型OLS探针只描述可恢复性，不进入模型训练，也不能直接证明有用的剩余信息。
| 数据集 | 预测目标 | 通道 | R2最小 | R2最大 |
| --- | --- | --- | --- | --- |
| cora | MULT | 0 | 0.693281994 | 0.693645169 |
| cora | MULT | 1 | 0.662028770 | 0.662988893 |
| cora | HDP | 0 | 0.908897717 | 0.909581467 |
| cora | HDP | 1 | 0.874692416 | 0.875363714 |
| cora | PAIR | 0 | 0.982672326 | 0.982734625 |
| cora | PAIR | 1 | 0.702360235 | 0.703501494 |
| pubmed | MULT | 0 | 0.953146873 | 0.953153864 |
| pubmed | MULT | 1 | 0.965764352 | 0.965770425 |
| pubmed | HDP | 0 | 0.943613046 | 0.943644691 |
| pubmed | HDP | 1 | 0.756499093 | 0.757059301 |
| pubmed | PAIR | 0 | 0.991008830 | 0.991015730 |
| pubmed | PAIR | 1 | 0.663481814 | 0.663562607 |


## 5. HDP条件增量：正向线索与反例

| 数据集 | GMH对照 | 平均ΔCE | CE胜出 | 平均ΔMRR |
| --- | --- | --- | --- | --- |
| cora | GM | 0.002094499 | 3/3 | 0.000754041 |
| cora | GMP | 0.000105071 | 3/3 | 0.000739332 |
| cora | GMG | -0.000168255 | 0/3 | 0.000522814 |
| cora | GMS | -0.000124261 | 0/3 | 0.000000000 |
| pubmed | GM | 0.001931346 | 3/3 | 0.001217333 |
| pubmed | GMP | 0.000187421 | 2/3 | -0.000097233 |
| pubmed | GMG | 0.000133536 | 2/3 | -0.000290268 |
| pubmed | GMS | 0.000797312 | 3/3 | -0.000634291 |

GMH对GM的CE改善在两数据集都是3/3，值得保留为条件性能线索，不能因V27独立HDP弱于GRAPH就删除。GMH对GMP的平均CE也略正。但Cora对GMG与GMS都是0/3改善，PubMed两项虽有平均CE优势，MRR却略弱；超边分组身份的跨数据集解释未得到支持。GMG是第三槽GRAPH复用控制，不是GDUP；两者定义必须分清。GMH未入选最多两个Phase B假设，所以不存在HDP的八种子或内部验证结果。

### 5.1 H活跃子群：逐种子证据

| 数据集 | seed | 子群 | 正例 | 负例 | 正例率 | GM CE | GMH CE | 平均逐候选ΔCE | GMH−GM平均score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cora | 0 | H0 | 77 | 4788 | 0.015827338 | 0.319850592 | 0.319353452 | 0.000497140 | -0.002080905 |
| cora | 0 | Hpositive | 186 | 472 | 0.282674772 | 0.886962697 | 0.887366564 | -0.000403866 | 0.001121294 |
| cora | 0 | H2plus | 116 | 155 | 0.428044280 | 1.294888427 | 1.295713079 | -0.000824652 | 0.001520071 |
| cora | 1 | H0 | 77 | 4788 | 0.015827338 | 0.187316056 | 0.187149608 | 0.000166448 | -0.000884430 |
| cora | 1 | Hpositive | 186 | 472 | 0.282674772 | 0.795236667 | 0.796103223 | -0.000866556 | 0.002642459 |
| cora | 1 | H2plus | 116 | 155 | 0.428044280 | 1.035745017 | 1.036453151 | -0.000708134 | 0.002562244 |
| cora | 2 | H0 | 77 | 4788 | 0.015827338 | 0.269536991 | 0.262890096 | 0.006646895 | -0.022920580 |
| cora | 2 | Hpositive | 186 | 472 | 0.282674772 | 0.870850449 | 0.870889669 | -0.000039221 | 0.013242748 |
| cora | 2 | H2plus | 116 | 155 | 0.428044280 | 1.215335808 | 1.215808743 | -0.000472935 | 0.005529978 |
| pubmed | 0 | H0 | 712 | 41159 | 0.017004609 | 0.077327010 | 0.073492772 | 0.003834238 | 0.011620977 |
| pubmed | 0 | Hpositive | 1504 | 3161 | 0.322400857 | 0.469735317 | 0.466888855 | 0.002846461 | 0.066172541 |
| pubmed | 0 | H2plus | 1319 | 937 | 0.584663121 | 0.656840465 | 0.659085267 | -0.002244802 | 0.043491739 |
| pubmed | 1 | H0 | 712 | 41159 | 0.017004609 | 0.073668132 | 0.071806365 | 0.001861768 | -0.005914055 |
| pubmed | 1 | Hpositive | 1504 | 3161 | 0.322400857 | 0.496404165 | 0.504226717 | -0.007822552 | 0.073438459 |
| pubmed | 1 | H2plus | 1319 | 937 | 0.584663121 | 0.679155428 | 0.691617537 | -0.012462110 | 0.073375193 |
| pubmed | 2 | H0 | 712 | 41159 | 0.017004609 | 0.081718390 | 0.078172814 | 0.003545576 | 0.006446732 |
| pubmed | 2 | Hpositive | 1504 | 3161 | 0.322400857 | 0.528816083 | 0.548989586 | -0.020173504 | 0.157354256 |
| pubmed | 2 | H2plus | 1319 | 937 | 0.584663121 | 0.718256860 | 0.750887890 | -0.032631030 | 0.169994489 |

关键反证：Cora H>0子群三个种子CE全部恶化；PubMed H>0仅seed0改善、seed1/2恶化。H≥2在两个数据集的所有三个种子均恶化。H=0子群反而全部改善。H≥2嵌套在H>0中，不能将两者计数相加。整体CE正向收益主要出现在多数的H=0候选，不能描述成“匹配资源瓶颈活跃群稳定获益”。共同训练与归一化后，H=0仍可产生常量特征状态、改变共享权重或决策校准；这是可检验的解释，不是已证实机制。

值得进行有限的新种子反证性复验，但不值得直接扩展K=3、path-GNN或把H>0子群选成优化目标。当前没有已确认的、未被经典拓扑/输入参数化解释的结构增量。最值得澄清的剩余线索是HDP在GM条件下的全局CE增量及其H=0校准来源。

## 6. 科学有效性与缺失证据

| 审查项 | 核验结果 | 边界 |
| --- | --- | --- |
| 规范结果完整性 | 既有 118 个规范结果单元的 checkpoint/score 哈希与重算 CE 通过；新 inner 阶段 48/48 原始结果与归档摘要一致 | 规范结果的历史复用单元不是新训练；inner 结果是 48 个新训练单元。 |
| 规范特征缓存 | 既有 17 个 READY 缓存哈希通过；本次 6 个 inner READY 缓存内每个数组哈希通过且可加载 | 前一次失败尝试产生的错误文件保留，但未被本次成功结果引用。 |
| 冻结源码/历史缓存 | 本次服务器 `check_frozen_all()` PASS；238 个源码/文件项和 112 个 V27 历史拓扑缓存无差异 | 历史文件由已校验本地归档恢复后核对；运行前不改源码定义。 |
| 配对训练轨迹 | 同 seed、arm、split 的 5/10 epoch 初始权重相同，前 5 个负采样及 permutation 轨迹逐项相同 | 不同 arm 的参数更新轨迹理应不同；不能要求跨方法参数状态相同。 |
| 内部分割和 target masking | 两数据集固定 inner split；结构 oracle PASS；6 个 READY 特征缓存哈希/加载全过 | 只证明这一个 seed=280016 的训练池留出，不是外部数据集复现。 |
| 内部结果与日志 | 48/48 结果 COMPLETE，checkpoint/score-vector SHA 匹配，48/48 完成标记；traceback/磁盘错误计数 0 | 6 个独立 inner-only C0 backbone 也完成 10 epoch，不与 48 个方法结果混计。 |
| test 封存 | 全部 inner 结果和 RUN_STATUS 均 `test_accessed/test_opened=false`；inner 输入只含 x/train/valid_pos/valid_neg | 源码审计和结果标记支持 test 未开启；不是操作系统级的文件访问追踪。 |

### 6.1 split与target masking

| 数据集 | inner训练正例 | inner验证正例 | 验证负例 | undirected正例不相交 | 负例无inner训练冲突 |
| --- | --- | --- | --- | --- | --- |
| cora | 4039 | 449 | 8980 | True | True |
| pubmed | 33908 | 3768 | 75360 | True | True |

固定 seed=280016 将原训练池的 undirected 正例按 10% 留作 inner validation，剩余部分构成 inner-train。Cora 为 4,039 个 inner-train 正例、449 个 inner-validation 正例和 8,980 个负例；PubMed 分别为 33,908、3,768 和 75,360。每个 query 使用 20 个不重复的 uniform endpoint-corruption 负例，排除整个原训练池，不用原 validation/test 标签筛选。结构、raw-star、上下文、target mask 与归一化从 inner-train 重新构建，伪留出边不进入消息图或中心成员；每个数据集的 target-mask oracle 均 PASS。inner-only NCNC C0 backbone 从头训练 final-10 epoch，未复用 full-training checkpoint。由此 GRAPH/MULT 的内部预测信号有第二个边级划分来源；但只使用一个固定 inner split 与三个训练种子，不能等同独立外部数据复现。

### 6.2 选择偏差与优化限制

V18–V28 多轮使用相同 Cora/PubMed 验证图设计和筛选方向；新种子 3–7 检验的是固定数据划分上的优化随机性。inner split 的留出正例来自原训练池、且在 V28 full-training 阶段未作为 validation target，因此为 GRAPH/MULT 增加了新的边级评价来源；候选先按 Phase B 全训练池的新种子 CE 规则筛选，inner 标签未用于候选筛选。它降低了对单一固定 validation edge set 的依赖，但只有一次固定 inner split、每格 3 seeds，仍不能抵消多轮方法探索、跨数据集比较和选择偏差，也不能给出未校正显著性结论。固定 final epoch 避免 best-checkpoint 挑选；5/10 epoch 轨迹配对一致。后续应把任何 V29 假设预登记，报告所有配对 seed 和每个控制，不访问 test。

## 7. 六个决策问题

### 7.1 哪个方法跨数据集收益最稳定？

**GRAPH6。** 新种子对 SHARED 的 CE/MRR 均为双数据集正向；inner 5 epoch 与 10 epoch 中，对 SHARED 和同参数 ZERO6 的 CE/MRR 均值在 Cora、PubMed 四组全部为正。特别是 PubMed 两个预算里所有配对种子都改善；Cora inner-5 MRR 也对两个对照 3/3 改善。Cora inner-10 的 CE 对 SHARED 有一个种子负向，因此不把均值提升表述为每种子无例外。

### 7.2 哪个方法有尚未解释的结构增量？

**没有方法已证实拥有独立、非经典拓扑结构增量。** GRAPH 的预测信号现在达到 CE 复现标准，但它是常见邻居统计；MULT 的 CE 信号也达到复现标准，然而 Cora inner-5 MRR 不改善，而且 MULT 与 GRAPH 高度相关。GRAPH+MULT 的互补效应没有通过重复输入控制且没有 inner 结果。HDP 条件分支只有早期三种子正向 CE 线索，shuffle 辨别力和 H>0 子群证据不足。

### 7.3 哪些收益属于经典统计或容量效应？

GRAPH 是经典共同邻居/2-section 投影统计；MULT 是端点独占加权关联投影可恢复的多重性与支持数，不能主张 hypergraph-exclusive。GRAPH/MULT 对同容量 ZERO6 的 inner CE 均值改善，表明正向输入本身有用，不能把其提升简单归因于“多了 65 个参数”。但 GM 对 GDUP 的 Phase A 结果不佳，重复输入可能改变特征几何、优化或校准；现有对照未证明 GRAPH+MULT 独立互补。HDP 的全局增量也可能来自常量/二值闭包状态或共享权重校准，尚无证据区分。

### 7.4 若只允许一项V29，最值得验证的具体假设？

建议继续只检验一个机制问题：**在固定 GRAPH+MULT 表征后，HDP 的真实超边分组身份是否比二值闭包状态更能改善 inner-train 留出泛化？** V28 的 GMH 相对 GM 有三种子 CE 线索，但与 GMG/GMS 竞争结果不一致、H>0 子群没有稳定收益、shuffle 实际改变率仅约 4%，而且 HDP 未进入新种子或 inner 复验。V29 应采用新种子和预登记训练池 split，锁定特征、模型和 5/10 epoch，不按 validation 子群调参；如果控制有效而真实 HDP 仍无增益，就停止这条结构身份解释。这里仅给出建议，不执行 V29。

### 7.5 最重要的两个反证对照？

1. **同容量二值闭包状态分支**：在相同 GM 上加入 `[I(H>0), log1p(I(H>0))]`，使用相同 6→8→1 残差分支、初始化、归一化、训练预算。若它与真实 HDP 表现相当或更好，则连续匹配数/超边身份增量解释不成立。
2. **有足够辨别力的度数保持 HDP-SHUFFLE**：保持超边行度数与支持节点列度数，预先规定实质重连率和 H 改变率最低门槛；达不到门槛的 shuffle 视为无效操纵，不得用作真实结构证据。若有效 shuffle 不输真实 HDP，身份机制不支持。

GM（不加 HDP）作为估计条件增量的基础参照始终保留。既有 GMG/PAIR 结果也应呈报，避免把第三槽重复输入解释遗漏；但最关键的两个机制反证分别是二值闭包和有效随机化。

### 7.6 不访问test，如何验证稳定性？

V28 已给出一种无 test 的执行方式：只从原训练正例固定抽出 10% inner validation；用剩余 90% 重建图、raw-star 和 target mask，过滤负例时只使用原训练池；inner-only C0 从头训练；5/10 epoch 从相同初始化出发并复用相同前五轮负采样/排列。V29 若执行，应在启动前冻结新 seeds、第二个独立 inner split、所有对照、模型预算和终止门槛，报告逐 seed CE/MRR 与 bootstrap 区间；test 分支继续封存。

## 8. 原始证据索引

以下均已读取或从原始结果重算核验；既有 Phase A/B 指标文件保持不变，新增 inner 与审查状态另行同步。
- [00_PROTOCOL.md](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/00_PROTOCOL.md)
- [WORKSPACE_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/WORKSPACE_AUDIT.json)
- [RUN_MANIFEST.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/RUN_MANIFEST.json)
- [RUN_STATUS.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/RUN_STATUS.json)
- [SOURCE_HASHES.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/SOURCE_HASHES.json)
- [02_BASELINE_REPRODUCTION.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/02_BASELINE_REPRODUCTION.json)
- [03_PARAMETER_AND_INITIALIZATION_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/03_PARAMETER_AND_INITIALIZATION_AUDIT.json)
- [04_DETERMINISM_PRECHECK.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/04_DETERMINISM_PRECHECK.json)
- [06_PHASE_A_METRICS.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/06_PHASE_A_METRICS.json)
- [07_PHASE_A_PAIRED_CONTRASTS.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/07_PHASE_A_PAIRED_CONTRASTS.json)
- [11_PHASE_B_NEW_SEED_RESULTS.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/11_PHASE_B_NEW_SEED_RESULTS.json)
- [PHASE_B_SELECTION.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/PHASE_B_SELECTION.json)
- [01_FEATURE_DEPENDENCY_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/01_FEATURE_DEPENDENCY_AUDIT.json)
- [05_CONDITIONAL_TOPOLOGY_DIAGNOSTICS.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/05_CONDITIONAL_TOPOLOGY_DIAGNOSTICS.json)
- [08_CONDITIONAL_SHUFFLE_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/08_CONDITIONAL_SHUFFLE_AUDIT.json)
- [09_HDP_SUBGROUP_ANALYSIS.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/09_HDP_SUBGROUP_ANALYSIS.json)
- [INNER_SPLIT_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/INNER_SPLIT_AUDIT.json)
- [RECOVERY_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/RECOVERY_AUDIT.json)
- [12_PHASE_B_INNER_VALIDATION.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/12_PHASE_B_INNER_VALIDATION.json)
- [13_EPOCH_STABILITY.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/13_EPOCH_STABILITY.json)
- [FINAL_REPORT.md](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/FINAL_REPORT.md)
- [C2C_HANDOFF.md](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/C2C_HANDOFF.md)
- [V28_FINAL_REVIEW_CURRENT_STATE.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/V28_FINAL_REVIEW_CURRENT_STATE.json)
- [V28_FINAL_REVIEW_EVIDENCE_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/V28_FINAL_REVIEW_EVIDENCE_AUDIT.json)
- [V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/V28_FINAL_REVIEW_EXECUTION_AUDIT_FULL.json)
- [V28_INNER_FEATURE_AUDIT.json](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/V28_INNER_FEATURE_AUDIT.json)
- [recovery_supervisor.log](E:/我的资料库/Documents/Downloads/DCDLP-main/result/innovation2/TOPOLOGY_V28/recovery_supervisor.log)

服务器 V28 原始训练日志保存在 `HYPERGRAPH_RESEARCH/TOPOLOGY_V28/logs/`。本次新增 48 个 inner 方法训练日志全部含 `V28_JOB_COMPLETE`，没有 traceback/空间错误；48 个 checkpoint、score-vector 和原始结果 JSON 哈希一致。6 个 inner READY 缓存均逐数组哈希通过并可加载；两数据集 structure/context 的 split 与 target-mask 审计 PASS。`RUN_STATUS.json`、`12_PHASE_B_INNER_VALIDATION.json`、`13_EPOCH_STABILITY.json` 均为 COMPLETE，且 `test_opened=false`。较早的磁盘失败与并发写入日志和 ERROR 文件作为尝试历史保留，不代表最终状态。V28 完整 inner 输入、特征、backbone、训练 checkpoint、分数和日志增量已归档到上述本地 tar.gz。既有规范结果的 118 单元统计仍含复用项，不与新增 48 次训练混计。

## 9. C2C HANDOFF

```text
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
```

