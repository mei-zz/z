"""Aggregate V9 controls and verify pairing against V8 DCDLP hashes."""

import argparse
import json
from pathlib import Path

import numpy as np


METRICS = ("mrr", "hits10", "hits20", "hits50", "hits100")


def stats(rows, split, metric):
    values = np.asarray([row[split][metric] for row in rows], dtype=float)
    return {"n": int(len(values)), "mean": float(values.mean()),
            "std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
            "values": values.tolist(), "min": float(values.min()), "max": float(values.max())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--v8-summary", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    raw = Path(args.raw)
    result = {"settings": {}, "pairing": {}, "dcdlp_v8": json.loads(Path(args.v8_summary).read_text(encoding="utf-8"))["models"]}
    for setting, tag in (("A", "2_1"), ("B", "2_4")):
        paths = [raw / ("v9_controls_{}_seed{}.json".format(tag, seed)) for seed in (1, 2, 3)]
        docs = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
        model_names = list(docs[0]["models"].keys())
        setting_out = {}
        for name in model_names:
            rows = [doc["models"][name] for doc in docs]
            setting_out[name] = {
                "per_seed": rows,
                "validation": {metric: stats(rows, "validation", metric) for metric in METRICS},
                "test": {metric: stats(rows, "test", metric) for metric in METRICS},
                "parameter_count": rows[0]["parameter_count"],
                "runtime_seconds": stats(rows, "validation", "mrr") if False else {
                    "values": [row.get("runtime_seconds", 0.0) for row in rows],
                    "mean": float(np.mean([row.get("runtime_seconds", 0.0) for row in rows])),
                    "std": float(np.std([row.get("runtime_seconds", 0.0) for row in rows], ddof=1)),
                },
                "peak_gpu_memory_mb": [row.get("peak_gpu_memory_mb") for row in rows],
            }
        result["settings"][setting] = setting_out

        # Compare each V9 shared negative/order hash against the corresponding
        # V8 DCDLP trace. This is a protocol pairing check, not a result check.
        negative_match = []
        order_match = []
        for seed, doc in zip((1, 2, 3), docs):
            v8 = json.loads((raw.parent.parent / "V8" / "raw" / "v8_dcdlp_pred_{}_seed{}.json".format(tag, seed)).read_text(encoding="utf-8"))
            v8_neg = [row["negative_hash"] for row in v8["trace"]]
            v8_order = [row["order_hash"] for row in v8["trace"]]
            negative_match.append(doc["protocol"]["shared_negative_hashes"] == v8_neg)
            order_match.append(doc["protocol"]["shared_order_hashes"] == v8_order)
        result["pairing"][setting] = {"negative_hash_match_by_seed": negative_match, "order_hash_match_by_seed": order_match,
                                       "all_match": all(negative_match + order_match)}
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
