from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import multiprocessing as mp
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import run_v13 as runner

OUT = runner.OUT
ROOT = runner.ROOT
sys.path.insert(0, str(OUT / "candidate_patches"))
import phaseb_hooks_v13 as p1_hooks

DRIVER_REL = Path(__file__).resolve().relative_to(ROOT).as_posix()
HOOK_PATH = OUT / "candidate_patches" / "phaseb_hooks_v13.py"
HOOK_REL = HOOK_PATH.resolve().relative_to(ROOT).as_posix()
STATUS_JSON = OUT / "p1_phaseb_status.json"
RESULTS_JSON = OUT / "p1_phaseb_stage1_results.json"
SELECTION_PATH = OUT / "l1_phaseb_selections_cora" / "QTHS25.npy"
SELECTION_META = OUT / "l1_phaseb_selections_cora" / "QTHS25.json"
L1_AUDIT = OUT / "l1_phaseb_stage1_audit.json"
EXPECTED_CONTEXT = {
    "split": "c5cec7e3bf6eaad41e12ae786246bf454a1bbcd4476286c71eb7e75b0eeba71a",
    "pool": "3d1e3ea691fc19fab65d66ad278d169cf099eb831ad0e46a439510ff5d07a7ba",
    "validation": "aca455fc094f2b037a812d62a4fcb79fd8d48102d021d72418aea1ab0b65b455",
}
STRONG_BASELINE = "Cora Raw-HG DCDLP + QTHS25 + BCE"


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    temp.replace(path)


def assert_prerequisites():
    pubmed_path = OUT / "pubmed_generalization_status.json"
    t1_path = OUT / "t1_phaseb_status.json"
    if not pubmed_path.exists() or not t1_path.exists() or not L1_AUDIT.exists():
        raise RuntimeError("The completed PubMed, T1, and audited L1 records are required before Family P")
    pubmed = json.loads(pubmed_path.read_text(encoding="utf-8"))
    t1 = json.loads(t1_path.read_text(encoding="utf-8"))
    l1 = json.loads(L1_AUDIT.read_text(encoding="utf-8"))
    if (pubmed.get("state") != "GENERALIZATION_REJECT"
            or int(pubmed.get("completed", -1)) != int(pubmed.get("total", -2))
            or pubmed.get("test_evaluated") is not False):
        raise RuntimeError("Family P requires the completed, test-sealed PubMed decision")
    if (t1.get("state") != "STAGE1_REJECT"
            or int(t1.get("completed", -1)) != 7
            or int(t1.get("total", -1)) != 7
            or t1.get("test_evaluated") is not False):
        raise RuntimeError("Family P requires the completed, test-sealed T1 Stage 1 decision")
    if (l1.get("state") != "AUDIT_PASS"
            or l1.get("experiment_decision", {}).get("state") != "STAGE1_REJECT"
            or l1.get("completed_jobs") != 5
            or l1.get("test_evaluated") is not False):
        raise RuntimeError("Family P requires the audited, rejected, test-sealed L1 decision")


def import_context():
    import experiment_v8 as v8
    full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash = v8.dataset_context("cora")
    observed = {
        "split": v8.base.split_hash(view),
        "pool": pool_hash,
        "validation": valid_hash,
    }
    if observed != EXPECTED_CONTEXT:
        raise RuntimeError(f"Frozen Cora context mismatch: {observed}")
    if pool.shape != (len(view.train_pos), 20, 2):
        raise RuntimeError(f"Unexpected fixed train-only pool shape: {pool.shape}")
    if v8.v61.array_hash(pool) != pool_hash:
        raise RuntimeError("Frozen candidate-pool array hash mismatch")
    return v8, full, view, pool, scores, pool_hash, valid_pos, valid_neg, valid_hash


def prepare_selection():
    assert_prerequisites()
    v8, _full, view, _pool, _scores, pool_hash, _vp, _vn, valid_hash = import_context()
    selected = np.load(SELECTION_PATH, allow_pickle=False)
    meta = json.loads(SELECTION_META.read_text(encoding="utf-8"))
    selected_hash = v8.v61.array_hash(selected)
    if selected_hash != meta.get("selected_negative_hash"):
        raise RuntimeError("Saved QTHS25 selection array and metadata differ")
    if (meta.get("split_hash") != v8.base.split_hash(view)
            or meta.get("train_pool_hash") != pool_hash
            or meta.get("validation_candidate_hash") != valid_hash):
        raise RuntimeError("Saved QTHS25 selection metadata does not match the frozen Cora context")
    if selected.shape != (len(view.train_pos), 2):
        raise RuntimeError(f"Unexpected QTHS25 selection shape: {selected.shape}")
    return {
        "selected_negative_hash": selected_hash,
        "selected_file_sha256": sha256_file(SELECTION_PATH),
        "split_hash": meta["split_hash"],
        "train_pool_hash": pool_hash,
        "validation_candidate_hash": valid_hash,
        "test_evaluated": False,
    }


def p1_decoder_smoke(view, pool):
    import torch
    from dcdlp.models.dcdlp import DCDLP

    counts = {}
    p1_hooks.install_hooks()
    for arm in ("BASELINE", "P1_SYM", "P1_GENERIC", "P1_CONCAT"):
        p1_hooks.configure(arm, view.train_pos, pool, runner)
        model = DCDLP(
            int(view.features.shape[1]), 64, 32, 2, 0.3, "gcn",
            hypergraph_mode="raw",
        )
        counts[arm] = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
        if arm.startswith("P1_"):
            hu = torch.randn(64)
            hv = torch.randn(64)
            cn = torch.tensor([0.25])
            features_ab = torch.cat([torch.abs(hu - hv), hu * hv, cn])
            features_ba = torch.cat([torch.abs(hv - hu), hv * hu, cn])
            if arm == "P1_SYM" and not torch.equal(features_ab, features_ba):
                raise RuntimeError("P1_SYM pair features are not symmetric")
            probe = torch.randn(3, 129, requires_grad=True)
            values = model.v13_pair_decoder(probe).sum()
            values.backward()
            if not torch.isfinite(values) or not torch.isfinite(probe.grad).all():
                raise RuntimeError(f"{arm} decoder smoke produced non-finite gradients")
        del model
    if counts["P1_SYM"] != counts["P1_GENERIC"]:
        raise RuntimeError(f"Candidate and generic MLP parameter counts differ: {counts}")
    if not (counts["BASELINE"] < counts["P1_CONCAT"] < counts["P1_SYM"]):
        raise RuntimeError(f"Unexpected pair-decoder parameter ordering: {counts}")
    return counts


def stage1_tasks(selection_meta):
    specs = [
        ("QTHS25_BASELINE", "BASELINE", "QTHS25 plus the registered BCE baseline", "strong baseline"),
        ("P1_SYM", "P1_SYM", "Low-rank MLP over symmetric endpoint difference, Hadamard product, and standardized CN", "candidate"),
        ("P1_GENERIC", "P1_GENERIC", "Same-parameter generic endpoint concatenation MLP with the same CN channel", "same-parameter control"),
        ("P1_CONCAT", "P1_CONCAT", "Same-input-dimension linear concatenation decoder with the same CN channel", "same-dimension control"),
    ]
    tasks = []
    for name, arm, definition, purpose in specs:
        tasks.append({
            "job_id": f"V13-PHASEB-P1-STAGE1-{name}-s0",
            "candidate_id": "V13_PHASEB_P1_STAGE1_s0",
            "arm": arm,
            "definition": definition,
            "purpose": purpose,
            "stage": "phase1_phaseb_p1_stage1",
            "dataset": "cora",
            "seed": 0,
            "epochs": 5,
            "sampler": "QTHS25",
            "negative_override_path": str(SELECTION_PATH),
            "negative_override_hash": selection_meta["selected_negative_hash"],
            "priority": "P1",
            "status": "QUEUED",
            "stage1": True,
            "strong_baseline_identity": STRONG_BASELINE,
            "research_context": (
                "Same frozen Cora split, train-only 20-candidate pool, QTHS25 selected negatives, "
                "validation candidates, backbone, seed, and five-epoch budget. P1_SYM and P1_GENERIC "
                "have exactly matched decoder parameter counts; P1_CONCAT preserves the input dimension."
            ),
            "selection_file_sha256": selection_meta["selected_file_sha256"],
        })
    return tasks


def execute_task(task, driver_hash, hook_hash):
    runner.worker_init()
    import experiment_v8 as v8
    v8_module, _full, view, pool, _scores, pool_hash, _vp, _vn, valid_hash = import_context()
    selected = np.load(task["negative_override_path"], allow_pickle=False)
    if v8_module.v61.array_hash(selected) != task["negative_override_hash"]:
        raise RuntimeError(f"Registered QTHS25 selection hash mismatch for {task['job_id']}")
    if (v8.base.split_hash(view) != EXPECTED_CONTEXT["split"]
            or pool_hash != EXPECTED_CONTEXT["pool"]
            or valid_hash != EXPECTED_CONTEXT["validation"]):
        raise RuntimeError("Worker loaded a different frozen Cora context")

    p1_hooks.configure(task["arm"], view.train_pos, pool, runner)
    p1_hooks.install_hooks()
    runner.install_hooks()
    result = runner.run_one(task)
    result.setdefault("source_hashes", {})[DRIVER_REL] = driver_hash
    result["source_hashes"][HOOK_REL] = hook_hash
    result["p1_driver_sha256"] = driver_hash
    result["p1_hooks_sha256"] = hook_hash
    result["p1_pair_state"] = (
        "abs(endpoint difference) + Hadamard product + standardized CN" if task["arm"] == "P1_SYM"
        else "ordered endpoint concatenation + standardized CN" if task["arm"] in {"P1_GENERIC", "P1_CONCAT"}
        else "base decoder"
    )
    result["research_context"] = task["research_context"]
    result["test_evaluated"] = False
    folder = OUT / "experiments" / task["candidate_id"] / task["arm"]
    runner.atomic_json(folder / "result.json", result)
    return result


def summarize_stage1(rows, driver_hash, hook_hash):
    expected_arms = {"BASELINE", "P1_SYM", "P1_GENERIC", "P1_CONCAT"}
    by_arm = {row.get("arm"): row for row in rows if row.get("state") == "COMPLETE"}
    missing = sorted(expected_arms - set(by_arm))
    if missing:
        return {"state": "RUNNING" if len(rows) < len(expected_arms) else "INFRASTRUCTURE_FAILURE",
                "go": False, "missing_arms": missing, "test_evaluated": False}
    all_rows = list(by_arm.values())
    for row in all_rows:
        if (int(row.get("epochs", -1)) != 5
                or int(row.get("train_record", {}).get("epoch_count", -1)) != 5
                or row.get("test_evaluated") is not False
                or row.get("p1_driver_sha256") != driver_hash
                or row.get("p1_hooks_sha256") != hook_hash):
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                    "invalid_job": row.get("job_id"), "test_evaluated": False}
    for key in ("split_hash", "train_pool_hash", "validation_candidate_hash", "selected_negative_hash"):
        if len({row.get(key) for row in all_rows}) != 1:
            return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                    "context_mismatch": key, "test_evaluated": False}
    source_maps = {json.dumps(row.get("source_hashes", {}), sort_keys=True) for row in all_rows}
    if len(source_maps) != 1:
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                "context_mismatch": "source_hashes", "test_evaluated": False}
    if int(by_arm["P1_SYM"].get("trainable_parameters", -1)) != int(by_arm["P1_GENERIC"].get("trainable_parameters", -2)):
        return {"state": "INFRASTRUCTURE_FAILURE", "go": False,
                "context_mismatch": "candidate_generic_parameter_count", "test_evaluated": False}

    def m(arm):
        return float(by_arm[arm]["validation_metrics"]["mrr"])

    baseline = m("BASELINE")
    candidate = m("P1_SYM")
    controls = {"same_parameter_generic_mlp": m("P1_GENERIC"),
                "same_dimension_concat_decoder": m("P1_CONCAT")}
    delta = candidate - baseline
    relative_delta = delta / baseline if baseline else float("-inf")
    gain_gate = delta >= 0.003 or relative_delta >= 0.01
    controls_pass = all(candidate > value for value in controls.values())
    go = gain_gate and controls_pass
    return {
        "state": "STAGE1_GO" if go else "STAGE1_REJECT",
        "go": bool(go),
        "baseline_mrr": baseline,
        "candidate_mrr": candidate,
        "delta_vs_qths25": delta,
        "relative_delta_vs_qths25": relative_delta,
        "stage1_gain_gate": bool(gain_gate),
        "matched_control_mrr": controls,
        "matched_control_margins": {name: candidate - value for name, value in controls.items()},
        "matched_controls_pass": bool(controls_pass),
        "all_mrr": {arm: m(arm) for arm in sorted(expected_arms)},
        "parameter_counts": {arm: int(by_arm[arm]["trainable_parameters"]) for arm in sorted(expected_arms)},
        "test_evaluated": False,
    }


def run_stage1(workers, selection_meta):
    assert_prerequisites()
    driver_hash = sha256_file(__file__)
    hook_hash = sha256_file(HOOK_PATH)
    tasks = stage1_tasks(selection_meta)
    old = []
    if RESULTS_JSON.exists():
        try:
            old = json.loads(RESULTS_JSON.read_text(encoding="utf-8")).get("results", [])
        except Exception:
            old = []
    prior = {row.get("job_id"): row for row in old}
    results, pending = [], []
    for task in tasks:
        row = prior.get(task["job_id"])
        valid = (
            row is not None and row.get("state") == "COMPLETE"
            and int(row.get("train_record", {}).get("epoch_count", -1)) == 5
            and row.get("p1_driver_sha256") == driver_hash
            and row.get("p1_hooks_sha256") == hook_hash
            and row.get("selected_negative_hash") == task["negative_override_hash"]
            and row.get("test_evaluated") is False
        )
        (results if valid else pending).append(row if valid else task)

    atomic_json(STATUS_JSON, {
        "state": "STAGE1_RUNNING", "stage": "phase1_phaseb_p1_stage1",
        "completed": len(results), "total": len(tasks), "workers": min(workers, len(pending)),
        "failed": [], "test_evaluated": False, "driver_sha256": driver_hash,
        "hooks_sha256": hook_hash, "updated_at_utc": utc_now(),
    })
    if pending:
        with cf.ProcessPoolExecutor(max_workers=min(workers, len(pending)),
                                    mp_context=mp.get_context("spawn"),
                                    initializer=runner.worker_init) as executor:
            futures = {executor.submit(execute_task, task, driver_hash, hook_hash): task for task in pending}
            for future in cf.as_completed(futures):
                task = futures[future]
                try:
                    row = future.result()
                except Exception as exc:
                    row = {**task, "state": "FAILED", "error": repr(exc),
                           "traceback": traceback.format_exc(), "test_evaluated": False,
                           "completed_at_utc": utc_now()}
                results.append(row)
                decision = summarize_stage1(results, driver_hash, hook_hash)
                atomic_json(RESULTS_JSON, {
                    "stage": "phase1_phaseb_p1_stage1", "results": results,
                    "decision": decision, "test_evaluated": False,
                    "driver_sha256": driver_hash, "hooks_sha256": hook_hash,
                })
                atomic_json(STATUS_JSON, {
                    "state": "STAGE1_RUNNING", "stage": "phase1_phaseb_p1_stage1",
                    "completed": sum(item.get("state") == "COMPLETE" for item in results),
                    "total": len(tasks), "workers": min(workers, len(pending)),
                    "failed": [item.get("job_id") for item in results if item.get("state") != "COMPLETE"],
                    "test_evaluated": False, "driver_sha256": driver_hash,
                    "hooks_sha256": hook_hash, "updated_at_utc": utc_now(),
                })

    decision = summarize_stage1(results, driver_hash, hook_hash)
    atomic_json(RESULTS_JSON, {
        "stage": "phase1_phaseb_p1_stage1",
        "results": sorted(results, key=lambda row: row.get("job_id", "")),
        "decision": decision, "test_evaluated": False,
        "driver_sha256": driver_hash, "hooks_sha256": hook_hash,
        "completed_at_utc": utc_now(),
    })
    atomic_json(STATUS_JSON, {
        "state": decision["state"], "stage": "phase1_phaseb_p1_stage1",
        "completed": sum(item.get("state") == "COMPLETE" for item in results),
        "total": len(tasks), "decision": decision, "test_evaluated": False,
        "driver_sha256": driver_hash, "hooks_sha256": hook_hash,
        "updated_at_utc": utc_now(),
    })
    return decision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    assert_prerequisites()
    selection_meta = prepare_selection()
    _v8, _full, view, pool, _scores, _pool_hash, _vp, _vn, _valid_hash = import_context()
    counts = p1_decoder_smoke(view, pool)
    if args.preflight_only:
        print(json.dumps({"state": "PREFLIGHT_PASS", "parameter_counts": counts,
                          "selection": selection_meta, "driver_sha256": sha256_file(__file__),
                          "hooks_sha256": sha256_file(HOOK_PATH), "test_evaluated": False}, indent=2))
        return
    decision = run_stage1(max(1, int(args.workers)), selection_meta)
    print(json.dumps(decision, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
