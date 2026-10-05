"""Parse the locked V8 baseline artifacts into a compact, auditable JSON."""

import argparse
import json
import re
from pathlib import Path

import numpy as np


METRICS = ["hits1", "hits3", "hits10", "hits20", "hits50", "hits100", "mrr"]
GCN_LABELS = ["Hits@1", "Hits@3", "Hits@10", "Hits@20", "Hits@50", "Hits@100", "MRR"]


def parse_gcn(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    # The final All-runs section is the authoritative summary for runs=1.
    marker = text.rfind("Hits@1\nAll runs:")
    if marker < 0:
        raise ValueError(f"summary marker not found in {path}")
    tail = text[marker:]
    valid, test = {}, {}
    for label, key in zip(GCN_LABELS, METRICS):
        block_start = tail.find(label)
        if block_start < 0:
            raise ValueError(f"missing {label} in {path}")
        block = tail[block_start:]
        vm = re.search(r"Highest Valid:\s*([0-9.]+)", block)
        tm = re.search(r"Final Test:\s*([0-9.]+)", block)
        if not vm or not tm:
            raise ValueError(f"missing summary values for {label} in {path}")
        valid[key] = float(vm.group(1)) / 100.0
        test[key] = float(tm.group(1)) / 100.0
    tm = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*([^\n]+)", text)
    wall = tm.group(1).strip() if tm else None
    rss = re.search(r"Maximum resident set size \(kbytes\):\s*([0-9]+)", text)
    return {"validation": valid, "test": test, "wall_time": wall, "max_rss_kb": int(rss.group(1)) if rss else None,
            "peak_gpu_memory_mb": None, "parameter_count": 83201,
            "resource_note": "parameter count independently probed from the official GCN+MLP constructors; official runner did not record CUDA peak memory"}


def parse_dcdlp(path: Path):
    obj = json.loads(path.read_text(encoding="utf-8"))
    metric_keys = {"mrr": "mrr", "hits10": "hits10", "hits20": "hits20", "hits50": "hits50", "hits100": "hits100"}
    def take(section):
        return {out: float(section[src]) for src, out in metric_keys.items()}
    return {"validation": take(obj["validation"]), "test": take(obj["test"]),
            "runtime_seconds": obj.get("runtime_seconds"),
            "peak_gpu_memory_mb": obj.get("peak_gpu_memory_mb"),
            "parameter_count": obj.get("parameter_count"), "best_epoch": obj.get("best_epoch"),
            "config": obj.get("config"), "dataset": obj.get("dataset"), "seed": obj.get("seed")}


def stats(rows, split, metric):
    values = np.asarray([row[split][metric] for row in rows], dtype=float)
    return {"n": int(values.size), "mean": float(values.mean()), "std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
            "min": float(values.min()), "max": float(values.max()), "values": values.tolist()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--raw", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    raw = Path(args.raw)
    result = {"models": {}, "heuristics": {}}
    for setting, tag in (("A", "2_1"), ("B", "2_4")):
        result["models"][setting] = {}
        drows = [parse_dcdlp(raw / f"v8_dcdlp_pred_{tag}_seed{s}.json") for s in (1, 2, 3)]
        grows = [parse_gcn(raw / f"gcn_saved_{tag}_seed{s}.log") for s in (1, 2, 3)]
        for name, rows in (("DCDLP", drows), ("Official_GCN", grows)):
            result["models"][setting][name] = {
                "per_seed": rows,
                "validation": {m: stats(rows, "validation", m) for m in ("mrr", "hits10", "hits20", "hits50", "hits100")},
                "test": {m: stats(rows, "test", m) for m in ("mrr", "hits10", "hits20", "hits50", "hits100")},
            }
        heuristic = json.loads((raw / f"lpshift_heuristics{'_2_4' if setting == 'B' else ''}.json").read_text(encoding="utf-8"))
        result["heuristics"][setting] = heuristic["heuristics"]
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
