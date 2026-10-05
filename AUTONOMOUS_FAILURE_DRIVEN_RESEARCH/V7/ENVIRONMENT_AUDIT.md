# Environment Audit

## 1. 官方环境与实际环境

官方 `environment.yml` 要求 Python 3.9、CUDA 11.6、PyTorch 1.13 系列、PyG 2.5.2 及较旧的 sparse extensions。实际远程 `mei_env` 为：

| 项目 | 实际值 |
|---|---|
| Python | 3.11.11 |
| PyTorch | 2.8.0+cu128 |
| PyG | 2.5.3 |
| torch-scatter | 2.1.2 |
| torch-sparse | 0.6.18 |
| torch-cluster | 1.6.3 |
| OGB | 1.3.6 |
| SciPy | 1.15.2 |
| scikit-learn | 1.6.1 |
| GPU | Tesla V100-PCIE-16GB |
| driver | 550.163.01 |
| CUDA available | yes |
| 磁盘剩余 | 约 35 GB |

没有覆盖、降级或修改 `mei_env`。所有 V7 代码均通过 wrapper 在该环境执行。

## 2. 失败诊断

### 网络/下载

GitHub `git ls-remote`、codeload archive 均正常；失败点是 OGB SNAP archive 的低吞吐下载。官方 URL 返回 HTTP 200、Content-Length `121625147`、支持 range；单连接约 10–40 KB/s，5 分钟只得到约 7 MB。8 路 range 下载完成后 ZIP `unzip -t` 无错误。

官方 archive：`collab.zip`，大小 `121625147` bytes，SHA256：

`c5563198e041c338f0a78e11322bb2de76b68f0e9ae3e3b6d6af2d8ca64cc`

### 依赖/运行时

第一次 OGB cache 读取因 PyTorch 新版安全反序列化默认值改变而失败：`Unsupported global torch_geometric.data.data.Data`。之后 SciPy sparse indexing 对官方 edge-index 类型的假设也不兼容。两者均由隔离 wrapper 处理，官方源文件未改动。

### CUDA/资源

V100 可见且可用。官方 GCN seed=1 完整运行峰值 RSS 约 2.54 GB；GPU 监控峰值约 10.85 GB，未发生 OOM。100 epoch wall time `3:54.87`，CPU user time `785.19 s`。数据生成是 CPU 密集型，默认 `(1,2)` 约 11 分钟 wall time。

## 3. 复现脚本

本地 wrapper/审计脚本：

- `../scripts/lpcompat_run.py`
- `../scripts/parallel_range_download.py`
- `../scripts/audit_lpshift_dataset.py`
- `../scripts/audit_lpshift_heuristics.py`

它们不替换官方 `main_gnn.py`、`gen_synth.py` 或 `eval.py`；wrapper 只处理加载和索引兼容。

## 4. GitHub/官方文件边界

本轮审计的官方来源是 [LPShift repository](https://github.com/revolins/LPShift) 及其 README、`environment.yml`、`gen_synth.py`、`gen_synth.sh`、`main_gnn.py` 和 `eval.py`。所有实际运行来自上述官方 commit，不使用自制负样本或普通 OGB split 替代。

