"""Run Cora validation-only follow-up blocks alongside the gated PubMed screen.

This helper deliberately writes its own status/results sidecars. Model run
directories remain unique under the main V7.1 output so the primary runner can
reuse the completed, hash-matched checkpoints without retraining them.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
import traceback
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUNNER = HERE / "experiment_v71.py"
SPEC = importlib.util.spec_from_file_location("qths_v71_parallel", RUNNER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot import V7.1 runner at {RUNNER}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

STATUS_PATH = MODULE.OUT / "parallel_validation_status.json"
RESULTS_PATH = MODULE.OUT / "parallel_validation_results.json"


def persist(result: dict) -> None:
    temp = RESULTS_PATH.with_suffix(".json.tmp")
    temp.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(RESULTS_PATH)


def status(phase: str, current: str | None = None, **extra) -> None:
    payload = {"state": "RUNNING", "phase": phase, "current": current,
               "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **extra}
    temp = STATUS_PATH.with_suffix(".json.tmp")
    temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(STATUS_PATH)


MODULE.save_results = persist
MODULE.status = status

try:
    result = MODULE.read_json(MODULE.OUT / "results.json")
    cora = result.get("cora", {})
    if cora.get("locked_reproduction_status") != "PASS":
        raise RuntimeError("Cora locked-reproduction gate is not PASS; parallel controls remain closed")
    if not cora.get("test", {}).get("locked_gate_details", {}).get("QTHS25_beats_graph_hard_mean"):
        raise RuntimeError("Frozen Cora test gate details are unavailable; parallel controls remain closed")

    status("mechanism_controls", "validation_only")
    MODULE.run_mechanism_controls(result)
    persist(result)

    status("aqths_cora_validation", "validation_only")
    MODULE.run_aqths_cora(result)
    persist(result)

    status("complete", None,
           mechanism_class=result.get("mechanism_controls", {}).get("mechanism_class"),
           aqths_state=result.get("aqths", {}).get("state"),
           aqths_go=result.get("aqths", {}).get("GO"),
           test_evaluated=False)
except Exception:
    status("failed", None, error=traceback.format_exc(), test_evaluated=False)
    raise
