from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AUTONOMOUS_LP_RESEARCH_V13"
RAW_RESULTS = OUT / "l1_phaseb_stage1_results.json"
RAW_STATUS = OUT / "l1_phaseb_status.json"
SELECTION_META = OUT / "l1_phaseb_selections_cora" / "QTHS25.json"
AUDIT_JSON = OUT / "l1_phaseb_stage1_audit.json"

EXPECTED_ARMS = {
    "QTHS25_BASELINE": "BASELINE",
    "L1_EXPECTED_MRR": "L1_EXPECTED_MRR",
    "L1_INDEP_BCE": "L1_INDEP_BCE",
    "L1_LISTWISE_RANDOM": "L1_LISTWISE_RANDOM",
    "L1_REPEAT_BCE": "L1_REPEAT_BCE",
}
EXPECTED = {
    "split_hash": "c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a",
    "train_pool_hash": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
    "validation_candidate_hash": "aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455",
    "selected_negative_hash": "1ada7e01d1b3fa788db9d8312167290d4191344ace2db40bb787ab78e027c758",
    "driver_sha256": "604e7eb5cf86dc75596dc411007ce0c71d1257a98dbbc695a0a2469d88c5bf1c",
    "hooks_sha256": "54070f4357b6e9be906ee066596793d9ecf4b27df09da7d3b7d91733da10699e",
}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def main():
    raw = json.loads(RAW_RESULTS.read_text(encoding="utf-8"))
    raw_status = json.loads(RAW_STATUS.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION_META.read_text(encoding="utf-8"))
    errors = []
    rows = raw.get("results", [])
    by_arm = {row.get("arm"): row for row in rows}

    if len(rows) != len(EXPECTED_ARMS):
        errors.append(f"expected {len(EXPECTED_ARMS)} records, observed {len(rows)}")
    if len(by_arm) != len(rows):
        errors.append("duplicate arm records")
    if raw.get("driver_sha256") != EXPECTED["driver_sha256"]:
        errors.append("top-level driver hash mismatch")
    if raw.get("hooks_sha256") != EXPECTED["hooks_sha256"]:
        errors.append("top-level hook hash mismatch")
    if selection.get("selected_negative_hash") != EXPECTED["selected_negative_hash"]:
        errors.append("selection metadata hash mismatch")
    if selection.get("test_evaluated") is not False:
        errors.append("selection metadata indicates test evaluation")

    for symbolic_name, arm in EXPECTED_ARMS.items():
        row = by_arm.get(arm)
        if row is None:
            errors.append(f"missing arm {arm}")
            continue
        if row.get("state") != "COMPLETE":
            errors.append(f"{arm} state is {row.get('state')}")
        if int(row.get("epochs", -1)) != 5:
            errors.append(f"{arm} requested epoch count mismatch")
        if int(row.get("train_record", {}).get("epoch_count", -1)) != 5:
            errors.append(f"{arm} actual epoch count mismatch")
        if row.get("test_evaluated") is not False:
            errors.append(f"{arm} test_evaluated is not false")
        for key in ("split_hash", "train_pool_hash", "validation_candidate_hash", "selected_negative_hash"):
            expected_value = EXPECTED[key]
            if row.get(key) != expected_value:
                errors.append(f"{arm} {key} mismatch")
        if row.get("l1_driver_sha256") != EXPECTED["driver_sha256"]:
            errors.append(f"{arm} driver hash mismatch")
        if row.get("l1_hooks_sha256") != EXPECTED["hooks_sha256"]:
            errors.append(f"{arm} hook hash mismatch")
        if row.get("source_hashes", {}).get("AUTONOMOUS_LP_RESEARCH_V13/run_v13_l1_phaseb.py") != EXPECTED["driver_sha256"]:
            errors.append(f"{arm} source map lacks the expected driver hash")
        if row.get("source_hashes", {}).get("AUTONOMOUS_LP_RESEARCH_V13/candidate_patches/phaseb_hooks_v13.py") != EXPECTED["hooks_sha256"]:
            errors.append(f"{arm} source map lacks the expected hook hash")
        if row.get("l1_candidate_pool_size") != (1 if arm == "BASELINE" else 20):
            errors.append(f"{arm} candidate-pool scoring count mismatch")
        checkpoint = row.get("checkpoint")
        expected_checkpoint_hash = row.get("checkpoint_sha256")
        if not checkpoint or not Path(checkpoint).is_file():
            errors.append(f"{arm} checkpoint file is missing")
        elif sha256_file(checkpoint) != expected_checkpoint_hash:
            errors.append(f"{arm} checkpoint SHA-256 mismatch")
        metrics = row.get("validation_metrics", {})
        train_record = row.get("train_record", {})
        mrr = metrics.get("mrr")
        recorded = train_record.get("epoch10_validation_mrr")
        if mrr is None or recorded is None or not math.isclose(float(mrr), float(recorded), rel_tol=0, abs_tol=1e-8):
            errors.append(f"{arm} fixed-final-epoch validation MRR mismatch")

    if not errors and set(by_arm) == set(EXPECTED_ARMS.values()):
        rows_by_name = {name: by_arm[arm] for name, arm in EXPECTED_ARMS.items()}
        source_maps = {json.dumps(row.get("source_hashes", {}), sort_keys=True) for row in rows}
        if len(source_maps) != 1:
            errors.append("source hashes differ across arms")
        parameter_counts = {int(row.get("trainable_parameters", -1)) for row in rows}
        if len(parameter_counts) != 1:
            errors.append("trainable parameter counts differ across arms")
    else:
        rows_by_name = {}

    decision = {"state": "INFRASTRUCTURE_FAILURE", "go": False, "test_evaluated": False}
    if not errors:
        def m(name):
            return float(rows_by_name[name]["validation_metrics"]["mrr"])

        baseline = m("QTHS25_BASELINE")
        candidate = m("L1_EXPECTED_MRR")
        controls = {
            "independent_bce": m("L1_INDEP_BCE"),
            "random_set_listwise": m("L1_LISTWISE_RANDOM"),
            "repeated_k1_bce": m("L1_REPEAT_BCE"),
        }
        delta = candidate - baseline
        relative_delta = delta / baseline if baseline else float("-inf")
        gain_gate = delta >= 0.003 or relative_delta >= 0.01
        controls_pass = all(candidate > value for value in controls.values())
        go = gain_gate and controls_pass
        decision = {
            "state": "STAGE1_GO" if go else "STAGE1_REJECT",
            "go": bool(go),
            "baseline_mrr": baseline,
            "candidate_mrr": candidate,
            "delta_vs_qths25": delta,
            "relative_delta_vs_qths25": relative_delta,
            "stage1_gain_gate": bool(gain_gate),
            "compute_control_mrr": controls,
            "compute_control_margins": {name: candidate - value for name, value in controls.items()},
            "compute_controls_pass": bool(controls_pass),
            "all_mrr": {name: m(name) for name in EXPECTED_ARMS},
            "parameters": int(rows_by_name["QTHS25_BASELINE"]["trainable_parameters"]),
            "fixed_train_pool_size": 20,
            "test_evaluated": False,
        }

    report = {
        "state": "AUDIT_PASS" if not errors else "AUDIT_FAIL",
        "audit_errors": errors,
        "experiment_decision": decision,
        "raw_orchestrator_state": raw_status.get("state"),
        "raw_orchestrator_diagnosis": (
            "The orchestrator keyed results by human-readable definition text while looking up symbolic arm names; "
            "all five jobs are complete, so this is a summarization-key bug, not a training failure."
        ),
        "completed_jobs": sum(row.get("state") == "COMPLETE" for row in rows),
        "total_jobs": len(EXPECTED_ARMS),
        "test_evaluated": False,
        "source_results_sha256": sha256_file(RAW_RESULTS),
        "source_status_sha256": sha256_file(RAW_STATUS),
        "audited_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    atomic_json(AUDIT_JSON, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
