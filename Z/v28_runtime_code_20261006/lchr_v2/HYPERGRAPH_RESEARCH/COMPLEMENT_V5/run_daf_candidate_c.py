"""Run the V5 disagreement-aware fusion candidate and gated confirmation."""
from __future__ import annotations

from dataclasses import asdict
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
RUNS = BASE / "C_DAF" / "candidate_runs"
STATUS = BASE / "C_DAF" / "candidate_status.json"
RESULTS = BASE / "results.json"
FUSIONS = {"C2": "average", "C3": "global", "C4": "gate", "C5": "daf"}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def write_status(**fields) -> None:
    fields["updated_unix"] = time.time()
    write_json(STATUS, fields)


def mrr(result: dict) -> float:
    return float(result["validation"]["mrr"])


def source_config(label: str, seed: int, fusion_mode: str, hypergraph_mode: str):
    from dcdlp.train import TrainConfig

    raw = json.loads((BASELINE / "H" / "config.json").read_text(encoding="utf-8"))
    values = {key: value for key, value in raw.items() if key in TrainConfig.__dataclass_fields__}
    values.update({
        "seed": seed,
        "pretrain_epochs": 10,
        "disentangle_epochs": 0,
        "hypergraph_mode": hypergraph_mode,
        "hypergraph_construction": "raw_star",
        "ghhr_training_mode": "none",
        "complementarity_fusion_mode": fusion_mode,
        "fusion_gate_hidden_dim": 8,
        "fusion_margin_graph_threshold": 0.0,
        "fusion_margin_hypergraph_threshold": 0.0,
        "evaluate_test": False,
        "output_dir": str((RUNS / label).relative_to(ROOT)),
        "device": "cuda",
    })
    return TrainConfig(**values)


def run_arm(label: str, seed: int, fusion_mode: str, hypergraph_mode: str,
            dataset, initial_reference: dict[str, torch.Tensor] | None = None,
            capture_initial: bool = False) -> tuple[dict, dict[str, torch.Tensor] | None]:
    from dcdlp import train as train_module

    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    config = source_config(label, seed, fusion_mode, hypergraph_mode)
    original_optimizer = train_module._build_optimizer
    original_evaluate = train_module.evaluate_split
    state = {"epoch": 0}
    captured: dict[str, torch.Tensor] | None = None

    def matched_optimizer(model, probes, current_config):
        nonlocal captured
        if current_config is config:
            current = model.state_dict()
            if initial_reference is not None:
                missing = sorted(set(initial_reference) - set(current))
                if missing:
                    raise RuntimeError(f"{label} is missing Raw-HG initialization keys: {missing}")
                incompatible = model.load_state_dict(initial_reference, strict=False)
                if incompatible.unexpected_keys:
                    raise RuntimeError(f"{label} unexpected initial keys: {incompatible.unexpected_keys}")
                expected_extra = []
                if hypergraph_mode == "disabled":
                    expected_extra = []
                elif fusion_mode == "global":
                    expected_extra = ["fusion_global_logit"]
                elif fusion_mode in {"gate", "daf"}:
                    expected_extra = [
                        "fusion_gate.0.bias", "fusion_gate.0.weight",
                        "fusion_gate.2.bias", "fusion_gate.2.weight",
                    ]
                if sorted(incompatible.missing_keys) != sorted(expected_extra):
                    raise RuntimeError(f"{label} unexpected extra init keys: {incompatible.missing_keys}")
                copied = {key: model.state_dict()[key].detach().cpu() for key in initial_reference}
                if state_hash(copied) != state_hash(initial_reference):
                    raise RuntimeError(f"{label} did not copy the Raw-HG initial state exactly")
            elif capture_initial:
                captured = {key: value.detach().cpu().clone() for key, value in current.items()}
                torch.save(captured, out / "initial_state.pt")
            write_status(state="running", stage="candidate_C_10_epoch",
                         current=f"{label}/seed{seed}/epoch_0", completed=[],
                         test_evaluated=False)
        return original_optimizer(model, probes, current_config)

    def tracked_evaluate(model, current_dataset, positives, *args, **kwargs):
        result = original_evaluate(model, current_dataset, positives, *args, **kwargs)
        if current_dataset is dataset and np.array_equal(positives, dataset.valid_pos):
            state["epoch"] += 1
            write_status(state="running", stage="candidate_C_10_epoch",
                         current=f"{label}/seed{seed}/epoch_{state['epoch']}",
                         completed=[], validation_mrr_so_far=float(result[0]["mrr"]),
                         training_epochs=10, test_evaluated=False)
        return result

    train_module._build_optimizer = matched_optimizer
    train_module.evaluate_split = tracked_evaluate
    try:
        _, result = train_module.train_model(dataset, config)
    finally:
        train_module._build_optimizer = original_optimizer
        train_module.evaluate_split = original_evaluate
    if len(result.get("validation_curve", [])) != 10 or state["epoch"] != 10:
        raise RuntimeError(f"{label} did not complete exactly ten validation epochs")
    if result.get("metrics") != {} or result.get("evaluation_candidates", {}).get("test_evaluated") is not False:
        raise RuntimeError(f"{label} unexpectedly evaluated test candidates")
    result["matched_raw_initial_state_hash"] = (
        state_hash(initial_reference) if initial_reference is not None else None
    )
    result["matched_initialization"] = initial_reference is not None
    result["test_evaluated"] = False
    write_json(out / "metrics.json", result)
    write_json(out / "config.json", asdict(config))
    return result, captured


def state_hash(state: dict[str, torch.Tensor]) -> str:
    import hashlib
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def update_results(candidate_summary: dict, decision: str, phase: str) -> None:
    current = json.loads(RESULTS.read_text(encoding="utf-8"))
    current["status"] = "RUNNING" if phase != "complete" else "COMPLETE"
    current["candidates"]["C_DAF"] = candidate_summary
    current["final_decision"] = decision
    write_json(RESULTS, current)


def graph_margin_tertiles(dataset, seed: int, checkpoints: dict[str, str]) -> dict:
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.evaluation.ranking import reciprocal_ranks
    from dcdlp.utils import array_hash

    positives = np.asarray(dataset.valid_pos, dtype=np.int64)
    per_positive, candidate_seed = 20, seed + 777
    pool_count = max(per_positive * len(positives), per_positive)
    pool = uniform_negative_sampling(dataset.num_nodes, dataset.all_positive, pool_count, candidate_seed)
    negatives = grouped_negatives(positives, pool, per_positive, candidate_seed + 1)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    flat_negatives = negatives.reshape(-1, 2)
    scores = {}
    for label, path in checkpoints.items():
        model, _ = load_checkpoint_model(Path(path), device="cuda")
        pos = score_pairs(model, x, edges, positives)["logit"]
        neg = score_pairs(model, x, edges, flat_negatives)["logit"].reshape(len(positives), per_positive)
        scores[label] = (pos, neg)
        del model
    margin = scores["Graph"][0] - scores["Graph"][1].max(axis=1)
    chunks = np.array_split(np.argsort(margin, kind="stable"), 3)
    groups = {"Hard": chunks[0], "Medium": chunks[1], "Easy": chunks[2]}
    return {
        "validation_candidate_hash": array_hash(negatives),
        "groups": {
            name: {
                "count": int(len(indices)),
                "graph_margin_min": float(margin[indices].min()),
                "graph_margin_max": float(margin[indices].max()),
                "mrr": {
                    label: float(reciprocal_ranks(pos[indices], neg[indices]).mean())
                    for label, (pos, neg) in scores.items()
                },
            }
            for name, indices in groups.items()
        },
    }


def run_confirmation(candidate_summary: dict) -> dict:
    from dcdlp.data.loaders import load_dataset
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, evaluate_split

    arms = candidate_summary["arms"]
    control_label = max(("C2", "C3", "C4"), key=lambda key: mrr(arms[key]))
    control_mode = FUSIONS[control_label]
    confirmation_dir = RUNS / "confirmation_3seed"
    confirmation_dir.mkdir(parents=True, exist_ok=True)
    seed0 = {
        "Graph": json.loads((BASELINE / "G" / "metrics.json").read_text(encoding="utf-8")),
        "Raw-HG": json.loads((BASELINE / "H" / "metrics.json").read_text(encoding="utf-8")),
        "control": arms[control_label],
        "winner": arms["C5"],
    }
    records = {key: {0: value} for key, value in seed0.items()}
    tertiles = {}
    data0 = load_dataset("cora", ROOT / "data", "standard", 0)
    tertiles[0] = graph_margin_tertiles(data0, 0, {
        "Graph": seed0["Graph"]["checkpoint"],
        "Raw-HG": seed0["Raw-HG"]["checkpoint"],
        "Winner": seed0["winner"]["checkpoint"],
    })
    del data0
    raw_initial_by_seed = {}
    for seed in (1, 2):
        dataset = load_dataset("cora", ROOT / "data", "standard", seed)
        raw_result, raw_initial = run_arm(
            f"confirmation_3seed/seed{seed}/Raw_HG", seed, "none", "raw",
            dataset, capture_initial=True,
        )
        if raw_initial is None:
            raise RuntimeError(f"missing seed-{seed} Raw-HG initialization")
        raw_initial_by_seed[seed] = raw_initial
        graph_initial = {key: value for key, value in raw_initial.items() if not key.startswith("hypergraph.")}
        graph_result, _ = run_arm(
            f"confirmation_3seed/seed{seed}/Graph", seed, "none", "disabled",
            dataset, initial_reference=graph_initial,
        )
        control_result, _ = run_arm(
            f"confirmation_3seed/seed{seed}/control_{control_label}", seed, control_mode, "raw",
            dataset, initial_reference=raw_initial,
        )
        winner_result, _ = run_arm(
            f"confirmation_3seed/seed{seed}/DAF", seed, "daf", "raw",
            dataset, initial_reference=raw_initial,
        )
        records["Graph"][seed] = graph_result
        records["Raw-HG"][seed] = raw_result
        records["control"][seed] = control_result
        records["winner"][seed] = winner_result
        tertiles[seed] = graph_margin_tertiles(dataset, seed, {
            "Graph": graph_result["checkpoint"],
            "Raw-HG": raw_result["checkpoint"],
            "Winner": winner_result["checkpoint"],
        })
        del dataset
    values = {
        key: [mrr(records[key][seed]) for seed in (0, 1, 2)]
        for key in ("Graph", "Raw-HG", "control", "winner")
    }
    gains = [winner - raw for winner, raw in zip(values["winner"], values["Raw-HG"])]
    strong = sum(gain > 0 for gain in gains) >= 2 and float(np.mean(gains)) > 0
    summary = {
        "matched_control_selected_by_seed0_validation": control_label,
        "validation_mrr_by_seed": values,
        "mean_std_sample": {
            key: {"mean": float(np.mean(row)), "std": float(np.std(row, ddof=1))}
            for key, row in values.items()
        },
        "winner_minus_raw_by_seed": gains,
        "mean_gain_over_raw": float(np.mean(gains)),
        "graph_margin_tertiles_by_seed": tertiles,
        "strong_signal": bool(strong),
        "test_evaluated": False,
    }
    write_json(confirmation_dir / "confirmation_summary.json", summary)
    if not strong:
        candidate_summary["confirmation"] = summary
        candidate_summary["decision"] = "GO_BUT_CONFIRMATION_FAILED"
        update_results(candidate_summary, "NO_TASK_LEVEL_SIGNAL", "complete")
        write_status(state="complete", stage="final", current=None,
                     final_decision="NO_TASK_LEVEL_SIGNAL", test_evaluated=False,
                     strong_signal=False)
        return summary

    # The three seed-0 test sets are evaluated only after validation confirmation.
    data0 = load_dataset("cora", ROOT / "data", "standard", 0)
    x = torch.as_tensor(data0.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(data0.train_graph(), torch.device("cuda"))
    test_results = {}
    candidate_hash = None
    for label in ("Graph", "Raw-HG", "Winner"):
        result = seed0[label if label != "Winner" else "winner"]
        checkpoint = Path(result["checkpoint"])
        model, payload = load_checkpoint_model(checkpoint, device="cuda")
        metrics, _ = evaluate_split(
            model, data0, data0.test_pos, 999,
            int(payload["config"].get("negatives_per_positive_eval", 20)),
            x, edges, negative_method="uniform", candidate_metadata=(metadata := {}),
        )
        if candidate_hash is None:
            candidate_hash = metadata["hash"]
        elif metadata["hash"] != candidate_hash:
            raise RuntimeError("final three models did not use the same test candidates")
        test_results[label] = {"metrics": metrics, "checkpoint": str(checkpoint), "candidate_hash": metadata["hash"]}
        del model
    summary["test_evaluated"] = True
    summary["test_candidate_hash"] = candidate_hash
    summary["test_results"] = test_results
    candidate_summary["confirmation"] = summary
    candidate_summary["decision"] = "STRONG_SIGNAL"
    candidate_summary["winning_candidate"] = "C5_DAF"
    update_results(candidate_summary, "STRONG_SIGNAL", "complete")
    final = json.loads(RESULTS.read_text(encoding="utf-8"))
    final["status"] = "COMPLETE"
    final["winning_candidate"] = "C5_DAF"
    final["test_evaluated"] = True
    write_json(RESULTS, final)
    write_status(state="complete", stage="final", current=None,
                 final_decision="STRONG_SIGNAL", test_evaluated=True,
                 strong_signal=True)
    write_json(confirmation_dir / "confirmation_summary.json", summary)
    return summary


def main() -> None:
    if not torch.cuda.is_available() or "V100" not in torch.cuda.get_device_name(0):
        raise RuntimeError("Candidate C requires the registered CUDA V100 server")
    from dcdlp.data.loaders import load_dataset

    current = json.loads(RESULTS.read_text(encoding="utf-8"))
    current["status"] = "RUNNING"
    current["final_decision"] = "CANDIDATE_C_RUNNING"
    current["candidates"]["C_DAF"] = {"decision": "RUNNING"}
    write_json(RESULTS, current)
    RUNS.mkdir(parents=True, exist_ok=True)
    write_status(state="running", stage="candidate_C_10_epoch", current="C2/epoch_0",
                 completed=[], training_epochs=10, test_evaluated=False)
    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    raw_initial = torch.load(BASELINE / "raw_initial_state.pt", map_location="cpu", weights_only=True)
    arms = {}
    for label, fusion_mode in FUSIONS.items():
        result, _ = run_arm(label, 0, fusion_mode, "raw", dataset, initial_reference=raw_initial)
        arms[label] = result
        write_status(state="running", stage="candidate_C_10_epoch",
                     current=f"{label}/complete", completed=[key for key in FUSIONS if key in arms],
                     validation_mrr_so_far=mrr(result), training_epochs=10,
                     test_evaluated=False)
    del dataset
    raw_result = json.loads((BASELINE / "H" / "metrics.json").read_text(encoding="utf-8"))
    c1 = mrr(raw_result)
    c5 = mrr(arms["C5"])
    gain = c5 - c1
    relative = gain / c1
    comparisons = {key: c5 > mrr(arms[key]) for key in ("C2", "C3", "C4")}
    comparisons["C1"] = c5 > c1
    go = all(comparisons.values()) and (gain >= 0.003 or relative >= 0.01)
    summary = {
        "decision": "GO" if go else "REJECT",
        "arms": {"C0_Graph": json.loads((BASELINE / "G" / "metrics.json").read_text(encoding="utf-8")),
                 "C1_Raw_HG": raw_result, **arms},
        "validation_mrr": {"C0_Graph": mrr(json.loads((BASELINE / "G" / "metrics.json").read_text(encoding="utf-8"))),
                            "C1_Raw_HG": c1, **{key: mrr(value) for key, value in arms.items()}},
        "absolute_gain_over_C1": gain,
        "relative_gain_over_C1": relative,
        "beats_required_controls": comparisons,
        "go_threshold_met": bool(go),
        "oracle_gain": 0.02868774618280201,
        "novelty_status": "CONCEPTUAL_OVERLAP; EXACT_RULE_UNVERIFIED",
        "test_evaluated": False,
    }
    write_json(RUNS / "candidate_c_summary.json", summary)
    update_results(summary, "CANDIDATE_C_GO_CONFIRMATION_PENDING" if go else "NO_TASK_LEVEL_SIGNAL",
                   "candidate_C_complete" if go else "complete")
    if go:
        write_status(state="running", stage="confirmation_3seed", current="seed1/Raw-HG",
                     completed=["candidate_C"], validation_mrr_so_far=c5,
                     test_evaluated=False)
        run_confirmation(summary)
        write_json(RUNS / "candidate_c_summary.json", summary)
    else:
        write_status(state="complete", stage="final", current=None,
                     final_decision="NO_TASK_LEVEL_SIGNAL", test_evaluated=False)
    print(json.dumps({"decision": summary["decision"],
                      "validation_mrr": summary["validation_mrr"],
                      "absolute_gain": gain, "relative_gain": relative,
                      "test_evaluated": summary.get("confirmation", {}).get("test_evaluated", False)},
                     ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", stage="candidate_C", current=None,
                     error=f"{type(exc).__name__}: {exc}", test_evaluated=False)
        raise
