from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
import run_v13 as runner

OUT = runner.OUT
ROOT = runner.ROOT


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    stage3_path = OUT / "stage3_confirm_results.json"
    if not stage3_path.exists():
        raise RuntimeError("Stage 3 results are missing")
    stage3 = read_json(stage3_path)
    if stage3.get("decision", {}).get("state") != "LOCAL_GO":
        raise RuntimeError("Cora test is forbidden before LOCAL_GO")
    if len(stage3.get("results", [])) != 9:
        raise RuntimeError("Stage 3 must have all nine completed runs")
    if any(row.get("state") != "COMPLETE" or row.get("test_evaluated") is not False
           or int(row.get("train_record", {}).get("epoch_count", -1)) != 10
           for row in stage3["results"]):
        raise RuntimeError("Stage 3 completion/epoch/test gate failed")
    sentinel = OUT / "cora_test_once.started.json"
    final_path = OUT / "cora_test_once.json"
    if sentinel.exists() or final_path.exists():
        raise RuntimeError("Cora test one-time gate already consumed; refusing a second evaluation")

    arms = {}
    for row in stage3["results"]:
        if int(row.get("seed", -1)) == 0:
            arms[row["arm"]] = row
    required = {"BASELINE", "ECR_FULL", "ECR_SHUFFLED"}
    if required - set(arms):
        raise RuntimeError("Seed-0 Stage 3 baseline/candidate/mechanism-control checkpoints missing")

    runner.ACTIVE_ARM = "BASELINE"
    runner.install_hooks()
    import experiment_v8 as v8
    import numpy as np
    from dcdlp import train as train_module

    # Recheck each persisted model on frozen validation candidates before consuming the test gate.
    full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash = v8.dataset_context("cora")
    validation_rechecks = {}
    for arm in ("BASELINE", "ECR_FULL", "ECR_SHUFFLED"):
        runner.ACTIVE_ARM = arm
        metrics, params = v8.metric_for_checkpoint(
            arms[arm]["checkpoint"], view, valid_pos, valid_neg
        )
        expected = float(arms[arm]["validation_metrics"]["mrr"])
        if abs(float(metrics["mrr"]) - expected) > 1e-8:
            raise RuntimeError(f"validation checkpoint recheck mismatch for {arm}")
        validation_rechecks[arm] = {"metrics": metrics, "parameters": params}
    if pool_hash != arms["ECR_FULL"]["train_pool_hash"] or valid_hash != arms["ECR_FULL"]["validation_candidate_hash"]:
        raise RuntimeError("Frozen Cora validation context changed before test evaluation")

    runner.atomic_json(sentinel, {
        "state": "TEST_EVALUATION_STARTED",
        "stage3_decision": stage3["decision"],
        "started_at_utc": now(),
        "note": "One-time Cora test evaluation; no tuning or rerun permitted.",
    })
    meta = v8.ensure_test_candidates("cora")
    eval_dir = v8.OUT / "EVALUATION"
    archive_path = eval_dir / "cora_test_candidates.npz"
    with np.load(archive_path, allow_pickle=False) as archive:
        test_pos = archive["test_positive"].copy()
        test_neg = archive["test_negative_candidates"].copy()
    observed_hash = v8.v61.array_hash(test_neg)
    if observed_hash != meta["candidate_hash"]:
        raise RuntimeError("Frozen Cora test candidate hash mismatch")

    test_rows = {}
    for arm in ("BASELINE", "ECR_FULL", "ECR_SHUFFLED"):
        runner.ACTIVE_ARM = arm
        metrics, params = v8.metric_for_checkpoint(
            arms[arm]["checkpoint"], view, test_pos, test_neg
        )
        test_rows[arm] = {
            "metrics": metrics,
            "trainable_parameters": params,
            "checkpoint_sha256": arms[arm]["checkpoint_sha256"],
            "checkpoint": arms[arm]["checkpoint"],
            "seed": 0,
            "epochs": 10,
        }
    base = float(test_rows["BASELINE"]["metrics"]["mrr"])
    cand = float(test_rows["ECR_FULL"]["metrics"]["mrr"])
    ctrl = float(test_rows["ECR_SHUFFLED"]["metrics"]["mrr"])
    payload = {
        "state": "COMPLETE",
        "dataset": "cora",
        "stage3_state": "LOCAL_GO",
        "test_evaluated": True,
        "one_time_evaluation": True,
        "started_at_utc": json.loads(sentinel.read_text(encoding="utf-8"))["started_at_utc"],
        "completed_at_utc": now(),
        "candidate_hash": meta["candidate_hash"],
        "positive_hash": meta["positive_hash"],
        "positive_count": len(test_pos),
        "negative_count_per_positive": int(test_neg.shape[1]),
        "reused_frozen_test_candidates": bool(meta.get("reused_frozen_V7_1_test_candidates", False)),
        "validation_rechecks": validation_rechecks,
        "arms": test_rows,
        "comparison": {
            "candidate_mrr": cand,
            "baseline_mrr": base,
            "shuffled_control_mrr": ctrl,
            "delta_vs_baseline": cand - base,
            "delta_vs_control": cand - ctrl,
        },
        "test_source_hashes": runner.source_hashes(),
        "test_evaluated_only_after_local_go": True,
        "no_tuning_after_test": True,
    }
    runner.atomic_json(final_path, payload)
    runner.atomic_json(OUT / "cora_test_once.started.json", {
        "state": "CONSUMED",
        "started_at_utc": payload["started_at_utc"],
        "completed_at_utc": payload["completed_at_utc"],
        "candidate_hash": meta["candidate_hash"],
        "test_evaluated": True,
    })
    print(json.dumps(payload["comparison"] | {"state": payload["state"],
                     "candidate_hash": payload["candidate_hash"],
                     "test_evaluated": True}, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
