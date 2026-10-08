"""Run independent Cora validation units concurrently after the locked gate.

All methods, seeds, candidate arrays, model settings and validation checks are
the same as the primary runner. Each worker writes only its unique model run
directory and a per-unit status file; it never accesses test data or updates
the primary results/status files.
"""
from __future__ import annotations

import concurrent.futures
import importlib.util
import json
import multiprocessing as mp
import os
import sys
import time
import traceback
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUNNER = HERE / "experiment_v71.py"
OUT = HERE
UNIT_DIR = OUT / "PARALLEL_UNITS"
STATUS_PATH = OUT / "parallel_units_status.json"
WORKERS = 6


def load_runner(name: str):
    spec = importlib.util.spec_from_file_location(name, RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import runner at {RUNNER}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    module.status = lambda *args, **kwargs: None
    module.save_results = lambda *args, **kwargs: None
    return module


def run_one(spec: tuple[str, int]) -> dict:
    method, seed = spec
    module = load_runner(f"qths_v71_unit_{method.lower()}_{seed}")
    import numpy as np

    unit_path = UNIT_DIR / method / f"seed{seed}.json"
    unit_path.parent.mkdir(parents=True, exist_ok=True)
    state = {"state": "RUNNING", "method": method, "seed": seed,
             "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "test_evaluated": False}
    unit_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    try:
        full, view = module.init_dataset("cora")
        archive_path = module.V61 / "strict_train_candidates_and_selections.npz"
        with np.load(archive_path, allow_pickle=False) as archive:
            pool = archive["negative_candidates"].copy()
            scores = archive["score_graph"].copy()
        valid_pos, valid_neg, valid_hash = module.make_eval_candidates(full, "valid")
        pool_hash = module.v61.array_hash(pool)
        qths_ids, _ = module.v7.make_ids(pool, scores, view.train_pos, module.QTHS_ALPHA)
        qths_selected = pool[np.arange(len(pool)), qths_ids].copy()

        if method.startswith("MECH_"):
            if method == "MECH_HMC":
                selected, detail = module.build_hmc(pool, scores, view.train_pos, qths_ids, seed)
            elif method == "MECH_DMC":
                graph = view.train_graph()
                degree = np.asarray([graph.degree(node) for node in range(view.num_nodes)], dtype=np.int64)
                selected, detail = module.build_dmc(pool, scores, view.train_pos, qths_selected, degree, seed)
            else:
                raise ValueError(f"Unknown mechanism method: {method}")
        else:
            graph = view.train_graph()
            degree = np.asarray([graph.degree(node) for node in range(view.num_nodes)], dtype=np.int64)
            selections, details = module.prepare_aqths_selections(
                "cora", pool, scores, view.train_pos, degree, seed,
            )
            selected = selections[method]
            detail = details["metadata"].get(method, {})

        record = module.run_model(
            "cora", view, method, seed, selected, pool, pool_hash,
            valid_pos, valid_neg, valid_hash, hypergraph_mode="raw",
        )
        output = {
            "state": "COMPLETE", "method": method, "seed": seed,
            "record": record, "selection_diagnostics": detail,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "test_evaluated": False,
        }
        unit_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"method": method, "seed": seed, "mrr": record["validation_metrics"]["mrr"],
                "train_seconds": record.get("train_seconds"), "state": "COMPLETE"}
    except Exception:
        state.update({"state": "FAILED", "error": traceback.format_exc(),
                      "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        unit_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        raise


def write_status(state: str, complete: list, current=None, error=None) -> None:
    payload = {"state": state, "phase": "cora_validation_parallel",
               "workers": WORKERS, "complete_count": len(complete),
               "complete": complete, "current": current,
               "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
               "test_evaluated": False}
    if error:
        payload["error"] = error
    temp = STATUS_PATH.with_suffix(".json.tmp")
    temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(STATUS_PATH)


def main() -> None:
    source = json.loads((OUT / "results.json").read_text(encoding="utf-8"))
    cora = source.get("cora", {})
    if cora.get("locked_reproduction_status") != "PASS":
        raise RuntimeError("Cora locked-reproduction gate is not PASS")
    if not cora.get("test", {}).get("locked_gate_details", {}).get("QTHS25_beats_graph_hard_mean"):
        raise RuntimeError("Cora frozen test gate is not PASS")

    tasks = [(f"MECH_{method}", seed) for method in ("HMC", "DMC") for seed in (1, 2)]
    tasks += [(method, seed) for method in
              ("A2_RANDOM_ADAPTIVE", "A3_DEGREE_ADAPTIVE", "A4_AQTHS") for seed in (0, 1, 2)]
    complete = []
    for method, seed in tasks:
        path = UNIT_DIR / method / f"seed{seed}.json"
        if path.exists():
            try:
                old = json.loads(path.read_text(encoding="utf-8"))
                if old.get("state") == "COMPLETE":
                    complete.append({"method": method, "seed": seed,
                                     "mrr": old["record"]["validation_metrics"]["mrr"],
                                     "train_seconds": old.get("record", {}).get("train_seconds"),
                                     "state": "CACHED"})
            except Exception:
                pass
    pending = [(m, s) for m, s in tasks
               if not any(x["method"] == m and x["seed"] == s for x in complete)]
    if not pending:
        write_status("COMPLETE", complete)
        return

    write_status("RUNNING", complete)
    context = mp.get_context("spawn")
    with concurrent.futures.ProcessPoolExecutor(max_workers=WORKERS, mp_context=context) as pool:
        futures = {pool.submit(run_one, task): task for task in pending}
        for future in concurrent.futures.as_completed(futures):
            task = futures[future]
            try:
                item = future.result()
                complete.append(item)
                write_status("RUNNING", complete, current=None)
            except Exception:
                error = traceback.format_exc()
                write_status("FAILED", complete, current={"method": task[0], "seed": task[1]}, error=error)
                for other in futures:
                    other.cancel()
                raise
    write_status("COMPLETE", complete)


if __name__ == "__main__":
    main()
