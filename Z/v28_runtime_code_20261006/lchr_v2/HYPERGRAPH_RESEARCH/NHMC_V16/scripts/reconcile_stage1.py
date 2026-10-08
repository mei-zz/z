from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import torch


HERE = Path(__file__).resolve()
OUT = HERE.parents[1]
ROOT = Path(os.environ.get(
    "NHMC_RUNTIME_ROOT",
    "/home/ubuntu/lchr_v2/HYPERGRAPH_RESEARCH/HMC_V15/runtime",
)).resolve()
sys.path.insert(0, str(ROOT / "src"))
from dcdlp.evaluate import load_checkpoint_model  # noqa: E402


ARMS = ("B0_BASELINE", "B1_HRA", "B2_NATIVE_SCALAR", "C1_NHMC_SIZE",
        "C2_NHMC_SHUFFLE", "H1_NHMC_REAL")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def reconcile(dataset: str) -> dict:
    result_path = OUT / "experiments" / f"stage1_{dataset}" / "results.json"
    result = read_json(result_path)
    if result.get("dataset") != dataset or set(result.get("arms", {})) != set(ARMS):
        raise RuntimeError("completed six-arm result set is incomplete or mismatched")

    original = OUT / "diagnostics" / f"stage1_{dataset}_pre_reconciliation_results.json"
    status_path = OUT / "diagnostics" / f"stage1_{dataset}_status.json"
    original_status = OUT / "diagnostics" / f"stage1_{dataset}_pre_reconciliation_status.json"
    if not original.exists():
        shutil.copy2(result_path, original)
    if status_path.exists() and not original_status.exists():
        shutil.copy2(status_path, original_status)

    for arm in ARMS:
        record = result["arms"][arm]
        if record.get("state") != "COMPLETE" or record.get("test_evaluated") is not False:
            raise RuntimeError(f"arm is incomplete or test was evaluated: {arm}")
        if record.get("epochs") != 5 or record.get("seed") != 0:
            raise RuntimeError(f"arm violates the frozen quick-screen settings: {arm}")
        checkpoint = Path(record["checkpoint"])
        if not checkpoint.is_file():
            raise RuntimeError(f"missing completed checkpoint for {arm}: {checkpoint}")

    baseline_checkpoint = Path(result["arms"]["B0_BASELINE"]["checkpoint"])
    baseline_model, _ = load_checkpoint_model(baseline_checkpoint, device="cpu")
    baseline_parameters = sum(
        int(parameter.numel()) for parameter in baseline_model.parameters()
        if parameter.requires_grad
    )
    del baseline_model
    if baseline_parameters <= 0:
        raise RuntimeError(f"invalid baseline parameter count: {baseline_parameters}")

    parameter_budget = {}
    for arm in ARMS:
        record = result["arms"][arm]
        added = int(record.get("added_nhmc_parameters", 0))
        count = baseline_parameters + added
        record["trainable_parameters"] = count
        parameter_budget[arm] = {
            "added": added,
            "fraction_of_baseline": added / baseline_parameters,
        }
        arm_path = OUT / "experiments" / f"stage1_{dataset}" / f"{arm}.json"
        if arm_path.exists():
            arm_record = read_json(arm_path)
            arm_record["trainable_parameters"] = count
            write_json(arm_path, arm_record)

    mrr = {arm: float(result["arms"][arm]["validation_metrics"]["mrr"]) for arm in ARMS}
    h1 = mrr["H1_NHMC_REAL"]
    deltas = {
        arm: h1 - mrr[arm]
        for arm in ARMS if arm != "H1_NHMC_REAL"
    }
    shuffle_power = float(result["train_cache"]["shuffle"]["informative_shuffle_fraction"])
    shuffle_threshold = .002 if shuffle_power >= .30 else 0.0
    budget_ok = all(row["fraction_of_baseline"] <= .02
                    for row in parameter_budget.values())
    gate_ok = (
        deltas["B0_BASELINE"] >= .003
        and deltas["B1_HRA"] >= .002
        and deltas["B2_NATIVE_SCALAR"] >= .002
        and deltas["C1_NHMC_SIZE"] >= .002
        and (deltas["C2_NHMC_SHUFFLE"] >= .002 if shuffle_power >= .30
             else deltas["C2_NHMC_SHUFFLE"] > 0.0)
    )
    decision = ("PARAMETER_BUDGET_VIOLATION" if not budget_ok else
                "NHMC_STAGE1_GO" if gate_ok else "NHMC_STAGE1_REJECT")

    placeholders = result.get("heldout_positive_placeholder_reads", {})
    result.update({
        "state": "COMPLETE",
        "decision": decision,
        "decision_origin": "RECONCILED_FROM_COMPLETED_ARM_CHECKPOINTS_AND_VALIDATION_METRICS",
        "mrr": mrr,
        "deltas_h1_minus_controls": deltas,
        "stage1_gate": {
            "passed": decision == "NHMC_STAGE1_GO",
            "thresholds": {"H1-B0": .003, "H1-B1": .002, "H1-B2": .002,
                           "H1-C1": .002,
                           "H1-C2": .002 if shuffle_power >= .30 else ">0"},
            "shuffle_power_train": shuffle_power,
            "shuffle_power_validation": float(
                result["validation_cache"]["shuffle"]["informative_shuffle_fraction"]
            ),
        },
        "parameter_budget": {
            "baseline_trainable_parameters": baseline_parameters,
            "per_arm": parameter_budget,
            "max_allowed_fraction": .02,
            "count_source": "loaded B0 checkpoint; added arm parameters from frozen NHMC module definitions",
        },
        "legacy_train_api_empty_placeholders": {
            "placeholder_reads": placeholders,
            "placeholder_values_exposed": False,
            "test_identities_loaded": False,
            "test_evaluated": False,
            "explanation": "The legacy trainer reads empty TrainOnlyView sentinels while constructing an unused default forbidden set; the fixed train-only QTHS25 sampler and explicit validation evaluator provide the data used by the run.",
        },
    })
    if not budget_ok:
        result["decision_reason"] = "At least one NHMC arm exceeds the frozen 2% parameter overhead cap."
    elif not gate_ok:
        result["decision_reason"] = "One or more predeclared validation MRR promotion thresholds failed."
    else:
        result["decision_reason"] = "All six frozen arms, the 2% parameter cap, and all Cora Stage1 validation gates passed."

    write_json(result_path, result)
    write_json(status_path, {
        "state": "COMPLETE", "phase": "stage1_complete", "dataset": dataset,
        "decision": decision, "completed_arms": list(ARMS), "test_evaluated": False,
        "reconciled_from_completed_checkpoints": True,
        "placeholder_reads_are_empty_legacy_sentinels": True,
    })
    print(json.dumps({"decision": decision, "baseline_trainable_parameters": baseline_parameters,
                      "mrr": mrr, "deltas": deltas, "parameter_budget": parameter_budget},
                     indent=2))
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: reconcile_stage1.py {cora|pubmed|citeseer}")
    reconcile(sys.argv[1].lower())
