"""Run the V5 GHHR controls and, on GO, its registered confirmation."""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
BASE = ROOT / "HYPERGRAPH_RESEARCH" / "COMPLEMENT_V5"
BASELINE = BASE / "A_GHHR" / "remote_evidence" / "baseline_10_epoch"
RUNS = BASE / "A_GHHR" / "candidate_runs"
STATUS = BASE / "A_GHHR" / "candidate_status.json"
RESULTS = BASE / "results.json"
MODES = {"A2": "uniform", "A3": "shuffled", "A4": "difficulty"}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def write_status(**fields) -> None:
    fields["updated_unix"] = time.time()
    write_json(STATUS, fields)


def state_hash(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def source_config(seed: int, label: str, hypergraph_mode: str, ghhr_mode: str):
    from dcdlp.train import TrainConfig

    raw = json.loads((BASELINE / "H" / "config.json").read_text(encoding="utf-8"))
    values = {key: value for key, value in raw.items() if key in TrainConfig.__dataclass_fields__}
    values.update({
        "seed": seed,
        "pretrain_epochs": 10,
        "disentangle_epochs": 0,
        "hypergraph_mode": hypergraph_mode,
        "hypergraph_construction": "raw_star",
        "evaluate_test": False,
        "ghhr_training_mode": ghhr_mode,
        "lambda_h": 1.0,
        "ghhr_tau": 1.0,
        "output_dir": str((RUNS / label).relative_to(ROOT)),
        "device": "cuda",
    })
    return TrainConfig(**values)


def run_arm(label: str, seed: int, hypergraph_mode: str, ghhr_mode: str,
            dataset, initial_reference: dict[str, torch.Tensor] | None = None,
            capture_initial: bool = False) -> tuple[dict, dict[str, torch.Tensor] | None]:
    from dcdlp import train as train_module

    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    config = source_config(seed, label, hypergraph_mode, ghhr_mode)
    original_optimizer = train_module._build_optimizer
    original_evaluate = train_module.evaluate_split
    state = {"epoch": 0}
    captured: dict[str, torch.Tensor] | None = None

    # A prior process may have completed train_model and failed only in its
    # post-run evidence guard. Recover that complete, validation-only artifact.
    existing = sorted((out / "raw").glob("*.json")) if (out / "raw").exists() else []
    if len(existing) == 1:
        recovered = json.loads(existing[0].read_text(encoding="utf-8"))
        from dcdlp.utils import stable_hash
        if (recovered.get("config_hash") == stable_hash(asdict(config))
                and len(recovered.get("validation_curve", [])) == 10
                and recovered.get("metrics") == {}
                and recovered.get("evaluation_candidates", {}).get("test_evaluated") is False
                and (ghhr_mode == "none" or len(recovered.get("ghhr_epoch_diagnostics", [])) == 10)):
            recovered["train_negative_hashes_by_epoch"] = [
                train_module.array_hash(train_module._sample_train_negatives(dataset, config, epoch))
                for epoch in range(10)
            ]
            if ghhr_mode != "none" and recovered["train_negative_hashes_by_epoch"] != [
                row["train_negative_hash"] for row in recovered["ghhr_epoch_diagnostics"]
            ]:
                raise RuntimeError(f"recovered {label} negative hashes differ from recorded diagnostics")
            recovered["initial_reference_hash"] = state_hash(initial_reference) if initial_reference is not None else None
            recovered["matched_initialization"] = initial_reference is not None
            recovered["test_evaluated"] = False
            if capture_initial:
                initial_path = out / "initial_state.pt"
                if not initial_path.exists():
                    raise RuntimeError(f"cannot recover captured initialization for {label}")
                captured = torch.load(initial_path, map_location="cpu", weights_only=True)
            write_json(out / "metrics.json", recovered)
            write_json(out / "config.json", asdict(config))
            return recovered, captured

    def matched_optimizer(model, probes, current_config):
        nonlocal captured
        if current_config is config:
            current = model.state_dict()
            if initial_reference is not None:
                missing_raw = sorted(set(initial_reference) - set(current))
                if missing_raw:
                    raise RuntimeError(f"candidate model misses Raw-HG keys: {missing_raw}")
                incompatible = model.load_state_dict(initial_reference, strict=False)
                if incompatible.unexpected_keys:
                    raise RuntimeError(f"unexpected matched initial keys: {incompatible.unexpected_keys}")
                expected_missing = ["ghhr_beta"] if ghhr_mode != "none" else []
                if sorted(incompatible.missing_keys) != expected_missing:
                    raise RuntimeError(
                        f"unexpected unmatched initial keys: {incompatible.missing_keys}"
                    )
                matched = {key: model.state_dict()[key].detach().cpu() for key in initial_reference}
                if state_hash(matched) != state_hash(initial_reference):
                    raise RuntimeError("Raw-HG initial parameters did not copy exactly")
            elif capture_initial:
                captured = {key: value.detach().cpu().clone() for key, value in current.items()}
                torch.save(captured, out / "initial_state.pt")
            write_status(
                state="running", stage="candidate_A_10_epoch",
                current=f"{label}/seed{seed}/epoch_0", completed=[],
                test_evaluated=False,
            )
        return original_optimizer(model, probes, current_config)

    def tracked_evaluate(model, current_dataset, positives, *args, **kwargs):
        if current_dataset is dataset and np.array_equal(positives, dataset.test_pos):
            raise RuntimeError("candidate runner attempted forbidden test evaluation")
        result = original_evaluate(model, current_dataset, positives, *args, **kwargs)
        if current_dataset is dataset and np.array_equal(positives, dataset.valid_pos):
            state["epoch"] += 1
            write_status(
                state="running", stage="candidate_A_10_epoch",
                current=f"{label}/seed{seed}/epoch_{state['epoch']}",
                completed=[], validation_mrr_so_far=float(result[0]["mrr"]),
                training_epochs=10, test_evaluated=False,
            )
        return result

    train_module._build_optimizer = matched_optimizer
    train_module.evaluate_split = tracked_evaluate
    try:
        _, result = train_module.train_model(dataset, config)
    finally:
        train_module._build_optimizer = original_optimizer
        train_module.evaluate_split = original_evaluate
    if result.get("metrics") != {} or result.get("evaluation_candidates", {}).get("test_evaluated") is not False:
        raise RuntimeError(f"{label} unexpectedly evaluated test candidates")
    if len(result.get("validation_curve", [])) != 10 or state["epoch"] != 10:
        raise RuntimeError(f"{label} did not complete exactly ten validation epochs")
    result["train_negative_hashes_by_epoch"] = [
        train_module.array_hash(train_module._sample_train_negatives(dataset, config, epoch))
        for epoch in range(10)
    ]
    if ghhr_mode != "none" and result["train_negative_hashes_by_epoch"] != [
        row["train_negative_hash"] for row in result["ghhr_epoch_diagnostics"]
    ]:
        raise RuntimeError(f"{label} training-negative hashes do not match the recorded epochs")
    result["initial_reference_hash"] = state_hash(initial_reference) if initial_reference is not None else None
    result["matched_initialization"] = initial_reference is not None
    result["test_evaluated"] = False
    write_json(out / "metrics.json", result)
    write_json(out / "config.json", asdict(config))
    return result, captured


def validation_mrr(metrics: dict) -> float:
    return float(metrics["validation"]["mrr"])


def update_main_results(candidate_summary: dict, decision: str, phase: str) -> None:
    current = json.loads(RESULTS.read_text(encoding="utf-8"))
    current["status"] = "RUNNING" if phase != "complete" else "COMPLETE"
    current["baseline_results"] = {
        "graph_only_mrr": 0.49605565734757956,
        "raw_hypergraph_mrr": 0.5030120048647342,
        "graph_only_best_epoch": 5,
        "raw_hypergraph_best_epoch": 10,
    }
    current["complementarity_audit"] = json.loads(
        (BASELINE / "complementarity_summary.json").read_text(encoding="utf-8")
    )
    current["candidates"]["A_GHHR"] = candidate_summary
    if decision == "GO":
        current["final_decision"] = "CANDIDATE_A_GO_CONFIRMATION_RUNNING"
        current["candidates"]["B_CVHNM"] = {"decision": "STOPPED_AFTER_A_GO"}
        current["candidates"]["C_DAF"] = {"decision": "STOPPED_AFTER_A_GO"}
    elif decision == "REJECT":
        current["final_decision"] = "CANDIDATE_A_REJECT_NEXT_B"
    write_json(RESULTS, current)


def graph_margin_tertiles(dataset, seed: int, checkpoints: dict[str, str]) -> dict:
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import score_pairs
    from dcdlp.evaluation.ranking import reciprocal_ranks
    from dcdlp.utils import array_hash

    positives = np.asarray(dataset.valid_pos, dtype=np.int64)
    per_positive = 20
    candidate_seed = seed + 777
    pool_count = max(per_positive * len(positives), per_positive)
    pool = uniform_negative_sampling(dataset.num_nodes, dataset.all_positive, pool_count, candidate_seed)
    negatives = grouped_negatives(positives, pool, per_positive, candidate_seed + 1)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    from dcdlp.train import edge_index_from_graph
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    pairs_neg = negatives.reshape(-1, 2)
    scores = {}
    for label, path in checkpoints.items():
        model, _ = load_checkpoint_model(Path(path), device="cuda")
        positive_output = score_pairs(model, x, edges, positives)
        negative_output = score_pairs(model, x, edges, pairs_neg)
        scores[label] = {
            "positive": positive_output["logit"],
            "negative": negative_output["logit"].reshape(len(positives), per_positive),
        }
        del model
    graph_margin = scores["Graph"]["positive"] - scores["Graph"]["negative"].max(axis=1)
    order = np.argsort(graph_margin, kind="stable")
    chunks = np.array_split(order, 3)
    groups = {"Hard": chunks[0], "Medium": chunks[1], "Easy": chunks[2]}
    output = {
        "validation_candidate_hash": array_hash(negatives),
        "positive_hash": array_hash(positives),
        "groups": {},
    }
    for group, indices in groups.items():
        output["groups"][group] = {
            "count": int(len(indices)),
            "graph_margin_min": float(graph_margin[indices].min()),
            "graph_margin_max": float(graph_margin[indices].max()),
            "mrr": {
                label: float(reciprocal_ranks(
                    values["positive"][indices], values["negative"][indices]
                ).mean())
                for label, values in scores.items()
            },
        }
    return output


def run_confirmation(candidate_summary: dict) -> dict:
    from dcdlp.data.loaders import load_dataset
    from dcdlp import train as train_module
    from dcdlp.train import edge_index_from_graph, evaluate_split
    from dcdlp.utils import project_root

    arm_results = candidate_summary["arms"]
    control_label = max(("A2", "A3"), key=lambda key: validation_mrr(arm_results[key]))
    control_mode = MODES[control_label]
    confirmation_dir = RUNS / "confirmation_3seed"
    confirmation_dir.mkdir(parents=True, exist_ok=True)
    records = {}
    seed0 = {
        "G": json.loads((BASELINE / "G" / "metrics.json").read_text(encoding="utf-8")),
        "H": json.loads((BASELINE / "H" / "metrics.json").read_text(encoding="utf-8")),
        "control": arm_results[control_label],
        "winner": arm_results["A4"],
    }
    for key, result in seed0.items():
        records.setdefault(key, {})[0] = result
    tertiles = {}
    seed0_data = load_dataset("cora", ROOT / "data", "standard", 0)
    tertiles[0] = graph_margin_tertiles(seed0_data, 0, {
        "Graph": seed0["G"]["checkpoint"],
        "Raw-HG": seed0["H"]["checkpoint"],
        "Winner": seed0["winner"]["checkpoint"],
    })
    del seed0_data
    for seed in (1, 2):
        dataset = load_dataset("cora", ROOT / "data", "standard", seed)
        raw_result, raw_state = run_arm(
            f"confirmation_3seed/seed{seed}/Raw_HG", seed, "raw", "none",
            dataset, capture_initial=True,
        )
        if raw_state is None:
            raise RuntimeError(f"seed {seed} Raw-HG initialization was not captured")
        graph_result, _ = run_arm(
            f"confirmation_3seed/seed{seed}/Graph", seed, "disabled", "none",
            dataset, initial_reference={k: v for k, v in raw_state.items() if not k.startswith("hypergraph.")},
        )
        control_result, _ = run_arm(
            f"confirmation_3seed/seed{seed}/matched_control_{control_label}", seed, "raw", control_mode,
            dataset, initial_reference=raw_state,
        )
        winner_result, _ = run_arm(
            f"confirmation_3seed/seed{seed}/GHHR", seed, "raw", "difficulty",
            dataset, initial_reference=raw_state,
        )
        records["G"][seed] = graph_result
        records["H"][seed] = raw_result
        records["control"][seed] = control_result
        records["winner"][seed] = winner_result
        tertiles[seed] = graph_margin_tertiles(dataset, seed, {
            "Graph": graph_result["checkpoint"],
            "Raw-HG": raw_result["checkpoint"],
            "Winner": winner_result["checkpoint"],
        })
        del dataset
    mrrs = {
        key: [validation_mrr(records[key][seed]) for seed in (0, 1, 2)]
        for key in ("G", "H", "control", "winner")
    }
    gain_by_seed = [w - h for w, h in zip(mrrs["winner"], mrrs["H"])]
    strong = sum(gain > 0 for gain in gain_by_seed) >= 2 and float(np.mean(gain_by_seed)) > 0
    summary = {
        "control_selected_by_seed0_validation": control_label,
        "validation_mrr_by_seed": mrrs,
        "mean_std_sample": {
            key: {"mean": float(np.mean(values)), "std": float(np.std(values, ddof=1))}
            for key, values in mrrs.items()
        },
        "winner_minus_raw_by_seed": gain_by_seed,
        "mean_gain_over_raw": float(np.mean(gain_by_seed)),
        "graph_margin_tertiles_by_seed": tertiles,
        "strong_signal": bool(strong),
        "test_evaluated": False,
    }
    write_json(confirmation_dir / "confirmation_summary.json", summary)
    write_status(
        state="running" if strong else "complete",
        stage="test_evaluation" if strong else "confirmation_complete",
        current=None, completed=[f"seed_{seed}" for seed in (0, 1, 2)],
        strong_signal=bool(strong), test_evaluated=False,
    )
    if not strong:
        candidate_summary["confirmation"] = summary
        update_main_results(candidate_summary, "REJECT", "complete")
        final = json.loads(RESULTS.read_text(encoding="utf-8"))
        final["final_decision"] = "NO_TASK_LEVEL_SIGNAL"
        final["candidates"]["A_GHHR"]["decision"] = "GO_BUT_CONFIRMATION_FAILED"
        write_json(RESULTS, final)
        write_status(state="complete", stage="final", current=None,
                     final_decision="NO_TASK_LEVEL_SIGNAL", test_evaluated=False)
        return summary

    # The seed-0 checkpoints are evaluated exactly once, only after confirmation.
    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edges = train_module.edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    checkpoint_paths = {
        "Graph": Path(seed0["G"]["checkpoint"]),
        "Raw-HG": Path(seed0["H"]["checkpoint"]),
        "GHHR": Path(seed0["winner"]["checkpoint"]),
    }
    from dcdlp.evaluate import load_checkpoint_model
    test_results = {}
    test_candidate_hash = None
    for label, checkpoint in checkpoint_paths.items():
        model, payload = load_checkpoint_model(checkpoint, device="cuda")
        test_metrics, _ = evaluate_split(
            model, dataset, dataset.test_pos, 999,
            int(payload["config"].get("negatives_per_positive_eval", 20)),
            x, edges, negative_method="uniform",
            candidate_metadata=(metadata := {}),
        )
        if test_candidate_hash is None:
            test_candidate_hash = metadata["hash"]
        elif metadata["hash"] != test_candidate_hash:
            raise RuntimeError("test candidates were not identical across final three models")
        test_results[label] = {
            "metrics": test_metrics,
            "checkpoint": str(checkpoint),
            "candidate_hash": metadata["hash"],
        }
        del model
    summary["test_evaluated"] = True
    summary["test_candidate_hash"] = test_candidate_hash
    summary["test_results"] = test_results
    write_json(confirmation_dir / "confirmation_summary.json", summary)
    candidate_summary["confirmation"] = summary
    candidate_summary["decision"] = "STRONG_SIGNAL"
    update_main_results(candidate_summary, "GO", "complete")
    final = json.loads(RESULTS.read_text(encoding="utf-8"))
    final["status"] = "COMPLETE"
    final["final_decision"] = "STRONG_SIGNAL"
    final["winning_candidate"] = "A_GHHR"
    final["test_evaluated"] = True
    write_json(RESULTS, final)
    write_status(state="complete", stage="final", current=None,
                 final_decision="STRONG_SIGNAL", test_evaluated=True)
    return summary


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("Candidate A requires the registered CUDA V100 server")
    device_name = torch.cuda.get_device_name(0)
    if "V100" not in device_name:
        raise RuntimeError(f"Expected V100, found {device_name}")
    from dcdlp.data.loaders import load_dataset

    RUNS.mkdir(parents=True, exist_ok=True)
    summary_path = RUNS / "candidate_a_summary.json"
    write_status(state="running", stage="candidate_A_10_epoch", current="A2/seed0/epoch_0",
                 completed=[], training_epochs=10, test_evaluated=False,
                 device=device_name)
    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    raw_initial_state = torch.load(BASELINE / "raw_initial_state.pt", map_location="cpu", weights_only=True)
    arms = {}
    for label, mode in MODES.items():
        result, _ = run_arm(
            label, 0, "raw", mode, dataset,
            initial_reference=raw_initial_state,
        )
        arms[label] = result
        write_status(state="running", stage="candidate_A_10_epoch",
                     current=f"{label}/complete", completed=[key for key in MODES if key in arms],
                     validation_mrr_so_far=validation_mrr(result),
                     training_epochs=10, test_evaluated=False, device=device_name)
        if len(arms) > 1:
            hash_sets = [arms[key]["train_negative_hashes_by_epoch"] for key in arms]
            if any(values != hash_sets[0] for values in hash_sets[1:]):
                raise RuntimeError("A2/A3/A4 training negative arrays are not matched")
            pair_hashes = [[row["pair_order_hash"] for row in arms[key]["ghhr_epoch_diagnostics"]] for key in arms]
            if any(values != pair_hashes[0] for values in pair_hashes[1:]):
                raise RuntimeError("A2/A3/A4 pair orders are not matched")
    del dataset
    baseline_summary = json.loads((BASELINE / "complementarity_summary.json").read_text(encoding="utf-8"))
    a1 = float(baseline_summary["validation_mrr"]["raw_hypergraph"])
    a4 = validation_mrr(arms["A4"])
    absolute_gain = a4 - a1
    relative_gain = absolute_gain / a1
    beats_controls = all(a4 > validation_mrr(arms[key]) for key in ("A2", "A3"))
    beats_raw = a4 > a1
    go = beats_raw and beats_controls and (absolute_gain >= 0.003 or relative_gain >= 0.01)
    candidate_summary = {
        "decision": "GO" if go else "REJECT",
        "arms": arms,
        "a1_raw_hg_mrr": a1,
        "a4_ghhr_mrr": a4,
        "absolute_gain_over_a1": absolute_gain,
        "relative_gain_over_a1": relative_gain,
        "beats_A1": bool(beats_raw),
        "beats_A2": bool(a4 > validation_mrr(arms["A2"])),
        "beats_A3": bool(a4 > validation_mrr(arms["A3"])),
        "go_threshold_met": bool(go),
        "test_evaluated": False,
        "device": device_name,
    }
    write_json(summary_path, candidate_summary)
    update_main_results(candidate_summary, candidate_summary["decision"], "candidate_A_complete")
    if go:
        write_status(state="running", stage="confirmation_3seed", current="seed1/Raw-HG",
                     completed=["candidate_A"], validation_mrr_so_far=a4,
                     test_evaluated=False, device=device_name)
        confirmation = run_confirmation(candidate_summary)
        candidate_summary["confirmation"] = confirmation
        write_json(summary_path, candidate_summary)
    else:
        write_status(state="complete", stage="candidate_A_rejected",
                     current=None, completed=["candidate_A"],
                     final_decision="A_REJECT_NEXT_B", test_evaluated=False,
                     device=device_name)
    print(json.dumps({
        "decision": candidate_summary["decision"],
        "validation_mrr": {key: validation_mrr(value) for key, value in arms.items()},
        "a1_mrr": a1,
        "absolute_gain": absolute_gain,
        "relative_gain": relative_gain,
        "test_evaluated": candidate_summary.get("confirmation", {}).get("test_evaluated", False),
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", stage="candidate_A", current=None,
                     error=f"{type(exc).__name__}: {exc}", test_evaluated=False)
        raise
