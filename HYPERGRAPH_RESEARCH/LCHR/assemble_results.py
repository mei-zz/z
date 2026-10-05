import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = Path(r"E:\Z\lchr_remote\lchr_stage1")
dest = Path(__file__).resolve().parent
result = {
    "status": "EXECUTED",
    "candidate": "LCHR - Link-Conditioned Hyperedge Routing",
    "server": {
        "host": "ubuntu-ProLiant-DL380-Gen9",
        "gpu": "Tesla V100-PCIE-16GB",
        "environment": "mei_env / Python 3.11 / PyTorch 2.8.0+cu128",
        "state": "complete",
    },
    "dataset": "Cora standard, seed 0, 1 pretraining epoch, 0 disentanglement epochs, 20 uniform evaluation negatives per positive",
    "top_k": 8,
    "baselines": {},
    "decision": "REJECT",
    "targeted_revision": "none",
}
for key in ("B0", "B1", "B2", "B3", "B4"):
    run = source / key
    metrics = json.loads((run / "metrics.json").read_text(encoding="utf-8"))
    config = json.loads((run / "config.json").read_text(encoding="utf-8"))
    result["baselines"][key] = {
        "mode": metrics["hypergraph_mode"],
        "seed": metrics["seed"],
        "validation": metrics["validation"],
        "test": metrics["metrics"],
        "parameters": metrics["parameter_count"]["total"],
        "runtime_seconds": metrics["runtime"]["train_seconds"],
        "peak_gpu_memory_mb": metrics["runtime"]["peak_gpu_mb"],
        "config": config,
        "config_hash": metrics["config_hash"],
        "git_commit": metrics["git_commit"],
        "checkpoint": metrics["checkpoint"],
        "remote_metrics_file": f"/home/ubuntu/lchr_stage1/runs/lchr_stage1/{key}/metrics.json",
    }
result["mechanism_analysis"] = json.loads(
    (source / "mechanism_analysis.json").read_text(encoding="utf-8")
)
result["comparisons"] = {
    key: result["baselines"]["B4"]["validation"]["mrr"]
    - result["baselines"][key]["validation"]["mrr"]
    for key in ("B1", "B2", "B3")
}
(dest / "results.json").write_text(
    json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8"
)
