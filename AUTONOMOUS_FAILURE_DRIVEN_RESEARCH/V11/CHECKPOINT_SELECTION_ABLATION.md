# Checkpoint Selection Ablation

所有数值为 repaired V11 test candidate 上的结果，使用小数表示；每个均值和标准差来自 seeds 1–3。完整逐 epoch、逐 seed 的 MRR/Hits@10/20/50 保存在 `raw/formal_repaired/*.json`。

## 1. 四种规则

- A：old–old validation + Hits@20；
- B：old–old validation + MRR；
- C：old–old + validation-new + Hits@20；
- D：old–old + validation-new + MRR。

## 2. Overall test results

| 数据集 | 模型 | 规则 | MRR | Hits@10 | Hits@20 |
|---|---|---|---:|---:|---:|
| Cora | GraphSAGE | A | .19067±.01227 | .36284 | .49531 |
| Cora | GraphSAGE | B | .32438±.00219 | .55332 | .65124 |
| Cora | GraphSAGE | C | .30650±.02726 | .53253 | .63749 |
| Cora | GraphSAGE | D | .32929±.01170 | .56338 | .65459 |
| Cora | NodeDup | A | .20235±.13027 | .35446 | .45372 |
| Cora | NodeDup | B | .32813±.00342 | .55399 | .66901 |
| Cora | NodeDup | C | .28273±.08733 | .49229 | .61100 |
| Cora | NodeDup | D | .32843±.00618 | .55734 | .67438 |
| CiteSeer | GraphSAGE | A | .24720±.07334 | .42970 | .54147 |
| CiteSeer | GraphSAGE | B | .26632±.02408 | .47156 | .58373 |
| CiteSeer | GraphSAGE | C | .28996±.03862 | .50750 | .62401 |
| CiteSeer | GraphSAGE | D | .32386±.06165 | .53831 | .65087 |
| CiteSeer | NodeDup | A | .27666±.03492 | .48855 | .61809 |
| CiteSeer | NodeDup | B | .27796±.02785 | .48618 | .61414 |
| CiteSeer | NodeDup | C | .28734±.03613 | .48855 | .62243 |
| CiteSeer | NodeDup | D | .26695±.03424 | .46130 | .58768 |

## 3. Per-seed test MRR

| 数据集/模型 | seed 1 A/B/C/D | seed 2 A/B/C/D | seed 3 A/B/C/D |
|---|---|---|---|
| Cora GraphSAGE | .20290/.32687/.33433/.33352 | .19074/.32349/.30533/.33830 | .17837/.32278/.27985/.31607 |
| Cora NodeDup | .19861/.32668/.33183/.33195 | .33446/.33204/.33446/.33204 | .07399/.32568/.18190/.32129 |
| CiteSeer GraphSAGE | .32133/.25272/.30833/.34970 | .24559/.25210/.24559/.25349 | .17468/.29413/.31597/.36838 |
| CiteSeer NodeDup | .31536/.30496/.29103/.30496 | .26710/.27958/.32149/.25737 | .24752/.24933/.24951/.23853 |

## 4. 选择规则影响

- 只改指标、保持 old–old validation：A→B 的 MRR 增量为 Cora GraphSAGE `+0.13371`、Cora NodeDup `+0.12578`、CiteSeer GraphSAGE `+0.01912`、CiteSeer NodeDup `+0.00130`。Cora 上 Hits@20 选择存在明显早期/噪声敏感性。
- 只增加 new-node validation、保持 Hits@20：A→C 的 MRR 增量为 `+0.11583`、`+0.08038`、`+0.04276`、`+0.01068`，四种数据集/模型组合均为正。
- 只增加 new-node validation、保持 MRR：B→D 为 `+0.00491`、`+0.00030`、`+0.05754`、`−0.01101`。因此 new-node validation 的影响真实存在，但不是对所有模型都保证 test 提升。

## 5. 分组结果

采用 new-node validation 的 C/D 规则下，test MRR 按边类型的均值如下；完整 A/B/C/D 分组结果见 raw JSON。

| 数据集/模型/规则 | old–old | old–new | new–new |
|---|---:|---:|---:|
| Cora GraphSAGE C | .3050 | .3152 | .4321 |
| Cora GraphSAGE D | .3274 | .3445 | .4551 |
| Cora NodeDup C | .2824 | .2638 | .4421 |
| Cora NodeDup D | .3267 | .3407 | .4573 |
| CiteSeer GraphSAGE C | .2901 | .2923 | .1814 |
| CiteSeer GraphSAGE D | .3251 | .3052 | .2169 |
| CiteSeer NodeDup C | .2875 | .2796 | .3944 |
| CiteSeer NodeDup D | .2652 | .3005 | .2573 |

## 6. 结论

验证协议和 checkpoint 指标都会改变选择出的 epoch，并且这种变化会传递到冻结 test。new-node validation 对 Hits@20 选择的影响在两个数据集、两个模型上方向一致；MRR 选择较稳定，但 NodeDup/CiteSeer 仍出现下降。因此协议影响得到支持，但不能把它解释为某个新模型结构的收益。

