# V10.1 启动状态

状态：**服务器后台实验已启动，短时健康检查通过。完整实验尚未完成。**

- 服务器 SSH 正常；工作区查询服务仍返回 Internal error。依用户“解决连接问题后开始实验”的要求，已直接核对本地 DCDLP-main 与服务器对应项目的 V10 工件，记录替代核验方式。
- 后台主进程 PID 352400，PPID=1，独立会话 SID=352400；SSH 退出后进程持续存在。
- 6 个工作进程均已开始实际训练：PubMed Matched-Q seeds0/1/2，以及 Cora TS-SHUFFLE seeds0/1/2。
- 两次短时检查 GPU 利用率均为99%，后次显存占用2839MiB/16384MiB；截至检查无训练失败记录或异常退出。
- 队列共有20个新增10-epoch训练任务，之后自动执行27个冻结模型test评估任务，再生成最终结果和claim matrix。已完成工件可复用续跑。
- 已触发Cora五种子扩展：V10 cached test CPTS−Matched-Q的绝对均值约0.002046，小于0.005。原始validation差异约0.008949亦单独保留。方法不调参。
- 原始CPTS检测器直接只读导入V10；M20、K1、teacher、split、BIC、selection、STRICT_TRAIN_ONLY和epoch10均冻结。V10结果未修改。
- 初步null审计：三数据集real、Null-A、Null-B的tail detection均为100%。`TAIL_DETECTOR_NONDISCRIMINATIVE=true`。性能控制和跨数据集test仍按任务书完成，不修改检测器。

服务器输出目录：`/home/zhoulihui/lchr_v2/HYPERGRAPH_RESEARCH/CPTS_V10_1_AUDIT/`。后台状态在`status.json`，日志在`supervisor.log`。本地文件是启动时快照，最终结果应从服务器重新取回。

按用户要求，完成以上启动确认后结束会话，不进行长时间监控。
