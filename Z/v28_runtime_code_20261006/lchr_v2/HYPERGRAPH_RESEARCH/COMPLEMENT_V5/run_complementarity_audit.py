"""Matched 10-epoch Graph-only vs Raw-HG audit; validation only."""
from __future__ import annotations

import csv
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import time

import numpy as np
import torch
from scipy.stats import pearsonr, spearmanr

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "HYPERGRAPH_RESEARCH" / "COMPLEMENT_V5"
RUNS = BASE / "A_GHHR" / "remote_evidence" / "baseline_10_epoch"
DATA = ROOT / "data"
ARMS = {"G": "disabled", "H": "raw"}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def write_status(**fields) -> None:
    fields["updated_unix"] = time.time()
    write_json(RUNS / "status.json", fields)


def _state_hash(state: dict[str, torch.Tensor]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state):
        value = state[key].detach().cpu().contiguous()
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(value.numpy().tobytes())
    return digest.hexdigest()


def run_arm(
    label: str,
    hypergraph_mode: str,
    dataset,
    shared_reference: dict[str, torch.Tensor] | None,
) -> tuple[dict, dict[str, torch.Tensor] | None, list[str]]:
    from dcdlp import train as train_module
    from dcdlp.train import TrainConfig

    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    output_arg = str(out.relative_to(ROOT))
    config = TrainConfig(
        dataset="cora", protocol_train="uniform", protocol_eval="standard", seed=0,
        hidden_dim=16, branch_dim=8, num_layers=2, dropout=0.0, backbone="gcn",
        lr=1e-3, weight_decay=1e-4, batch_size=4096,
        pretrain_epochs=10, disentangle_epochs=0,
        negatives_per_positive_eval=20, device="cuda", ablation="A5",
        hypergraph_mode=hypergraph_mode, hypergraph_construction="raw_star",
        evaluate_test=False, output_dir=output_arg,
    )
    config_record = asdict(config)
    config_record.update({
        "arm": label,
        "meaning": "Graph-only A5 DCDLP" if label == "G" else "current Raw-HG A5 DCDLP",
        "matched_shared_initialization": True,
        "test_evaluated": False,
    })
    write_json(out / "config.json", config_record)

    state = {"active": False, "epoch": 0, "train_negative_hashes": []}
    captured_raw_state: dict[str, torch.Tensor] | None = None
    initial_shared_hash = None
    original_build_optimizer = train_module._build_optimizer
    original_sample_negatives = train_module._sample_train_negatives
    original_evaluate_split = train_module.evaluate_split

    def build_optimizer_with_matched_init(model, probes, current_config):
        nonlocal captured_raw_state, initial_shared_hash
        if current_config is config:
            current_state = model.state_dict()
            if label == "H":
                captured_raw_state = {
                    key: value.detach().cpu().clone()
                    for key, value in current_state.items()
                }
                shared = {
                    key: value for key, value in captured_raw_state.items()
                    if not key.startswith("hypergraph.")
                }
                initial_shared_hash = _state_hash(shared)
                torch.save(captured_raw_state, RUNS / "raw_initial_state.pt")
            else:
                if shared_reference is None:
                    raise RuntimeError("Graph-only arm lacks the Raw shared initial state")
                common = {
                    key: value for key, value in shared_reference.items()
                    if key in current_state and current_state[key].shape == value.shape
                }
                missing = sorted(set(current_state) - set(common))
                unexpected_raw = sorted(set(shared_reference) - set(common))
                if missing or any(not key.startswith("hypergraph.") for key in unexpected_raw):
                    raise RuntimeError(
                        f"shared initialization key mismatch: graph_missing={missing}; raw_extra={unexpected_raw}"
                    )
                model.load_state_dict(common, strict=False)
                updated = model.state_dict()
                aligned = {key: updated[key].detach().cpu() for key in common}
                initial_shared_hash = _state_hash(aligned)
                if initial_shared_hash != _state_hash(common):
                    raise RuntimeError("Graph-only shared parameters did not align exactly to Raw-HG init")
            state["active"] = True
        return original_build_optimizer(model, probes, current_config)

    def tracked_sample_negatives(current_dataset, current_config, epoch):
        sample = original_sample_negatives(current_dataset, current_config, epoch)
        if state["active"] and current_config is config:
            state["train_negative_hashes"].append(train_module.array_hash(sample))
        return sample

    def tracked_evaluate_split(model, current_dataset, positives, *args, **kwargs):
        result = original_evaluate_split(model, current_dataset, positives, *args, **kwargs)
        if state["active"] and current_dataset is dataset and positives is dataset.valid_pos:
            state["epoch"] += 1
            write_status(
                state="running", stage="matched_10_epoch_baseline",
                current=f"{label}/validation_epoch_{state['epoch']}",
                completed=["H"] if label == "G" else [],
                validation_mrr_so_far=float(result[0]["mrr"]),
                training_epochs=10, test_evaluated=False,
            )
        return result

    train_module._build_optimizer = build_optimizer_with_matched_init
    train_module._sample_train_negatives = tracked_sample_negatives
    train_module.evaluate_split = tracked_evaluate_split
    started = time.time()
    try:
        _, result = train_module.train_model(dataset, config)
    finally:
        train_module._build_optimizer = original_build_optimizer
        train_module._sample_train_negatives = original_sample_negatives
        train_module.evaluate_split = original_evaluate_split
    if (result.get("evaluation_candidates", {}).get("test_evaluated") is not False
            or result.get("metrics") != {}):
        raise RuntimeError(f"arm {label} unexpectedly evaluated test candidates")
    if len(result.get("validation_curve", [])) != 10:
        raise RuntimeError(f"arm {label} did not record ten validation epochs")
    result["wall_seconds"] = time.time() - started
    result["test_evaluated"] = False
    result["matched_shared_initialization"] = True
    result["shared_initial_state_hash"] = initial_shared_hash
    result["train_negative_hashes_by_epoch"] = state["train_negative_hashes"]
    write_json(out / "metrics.json", result)
    write_json(out / "train_negative_hashes.json", state["train_negative_hashes"])
    return result, captured_raw_state, state["train_negative_hashes"]


def _corr(left: np.ndarray, right: np.ndarray, method: str) -> float | None:
    if len(left) < 2 or np.std(left) == 0 or np.std(right) == 0:
        return None
    fn = pearsonr if method == "pearson" else spearmanr
    value = fn(left, right).statistic
    return float(value) if np.isfinite(value) else None


def main() -> None:
    RUNS.mkdir(parents=True, exist_ok=True)
    if not torch.cuda.is_available():
        raise RuntimeError("V5 matched audit requires the registered CUDA V100 server")
    from dcdlp.data.loaders import load_dataset
    from dcdlp import train as train_module
    from dcdlp.train import TrainConfig
    from dcdlp.utils import array_hash
    baseline: dict[str, dict] = {}
    write_status(state="running", stage="matched_10_epoch_baseline", current=None,
                 completed=[], test_evaluated=False)
    dataset = load_dataset("cora", DATA, "standard", 0)
    raw_initial_state = None
    negative_hashes_by_arm = {}
    raw_snapshot = RUNS / "raw_initial_state.pt"
    raw_result_dir = RUNS / "H" / "raw"
    prior_raw_files = sorted(raw_result_dir.glob("*.json")) if raw_result_dir.exists() else []
    if raw_snapshot.exists() and prior_raw_files:
        # The previous process finished the H training and wrote its standard
        # run artifact, then stopped on an overly strict audit-field guard.
        # Recover that completed run after validating the official no-test flag.
        baseline["H"] = json.loads(prior_raw_files[-1].read_text(encoding="utf-8"))
        raw_initial_state = torch.load(raw_snapshot, map_location="cpu", weights_only=True)
        if (baseline["H"].get("metrics") != {}
                or baseline["H"].get("evaluation_candidates", {}).get("test_evaluated") is not False
                or len(baseline["H"].get("validation_curve", [])) != 10):
            raise RuntimeError("existing Raw-HG artifact is not a complete validation-only 10-epoch run")
        common_raw_state = {
            key: value for key, value in raw_initial_state.items()
            if not key.startswith("hypergraph.")
        }
        config_data = json.loads((RUNS / "H" / "config.json").read_text(encoding="utf-8"))
        config = TrainConfig(**{
            key: value for key, value in config_data.items()
            if key in TrainConfig.__dataclass_fields__
        })
        raw_neg_hashes = [
            array_hash(train_module._sample_train_negatives(dataset, config, epoch))
            for epoch in range(10)
        ]
        baseline["H"].update({
            "test_evaluated": False,
            "matched_shared_initialization": True,
            "shared_initial_state_hash": _state_hash(common_raw_state),
            "train_negative_hashes_by_epoch": raw_neg_hashes,
            "recovered_from_completed_training_artifact": str(prior_raw_files[-1]),
        })
        write_json(RUNS / "H" / "metrics.json", baseline["H"])
        write_json(RUNS / "H" / "train_negative_hashes.json", raw_neg_hashes)
        negative_hashes_by_arm["H"] = raw_neg_hashes
    else:
        write_status(state="running", stage="matched_10_epoch_baseline", current="H",
                     completed=[], test_evaluated=False)
        baseline["H"], raw_initial_state, negative_hashes_by_arm["H"] = run_arm(
            "H", ARMS["H"], dataset, None
        )
    write_json(RUNS / "baseline_results.json", baseline)

    write_status(state="running", stage="matched_10_epoch_baseline", current="G",
                 completed=["H"], test_evaluated=False)
    baseline["G"], _, negative_hashes_by_arm["G"] = run_arm(
        "G", ARMS["G"], dataset, raw_initial_state
    )
    write_json(RUNS / "baseline_results.json", baseline)
    if negative_hashes_by_arm["H"] != negative_hashes_by_arm["G"]:
        raise RuntimeError("Graph and Raw-HG training negative samples differ by epoch")
    write_json(RUNS / "matched_training_audit.json", {
        "raw_hg_training_recovered_from_completed_artifact": "recovered_from_completed_training_artifact" in baseline["H"],
        "training_negative_hashes_equal_by_epoch": True,
        "training_negative_hashes_by_epoch": negative_hashes_by_arm,
        "shared_initialization_hash_H": baseline["H"]["shared_initial_state_hash"],
        "shared_initialization_hash_G": baseline["G"]["shared_initial_state_hash"],
        "shared_model_parameters_aligned_exactly": (
            baseline["H"]["shared_initial_state_hash"] == baseline["G"]["shared_initial_state_hash"]
        ),
        "test_evaluated": False,
    })

    # Use the same deterministic candidate-generation path as evaluate_split
    # for standard Cora: pool seed = seed + 777, grouping seed = pool seed + 1.
    from dcdlp.data.loaders import load_dataset
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.utils import array_hash

    positives = np.asarray(dataset.valid_pos, dtype=np.int64)
    negatives_per_positive = 20
    pool_seed = 777
    pool_count = max(negatives_per_positive * len(positives), negatives_per_positive)
    pool = uniform_negative_sampling(dataset.num_nodes, dataset.all_positive, pool_count, pool_seed)
    negatives = grouped_negatives(positives, pool, negatives_per_positive, pool_seed + 1)
    candidates = np.concatenate([positives[:, None, :], negatives], axis=1)
    np.savez_compressed(
        RUNS / "validation_candidates.npz",
        positives=positives,
        negatives=negatives,
        candidates=candidates,
    )
    candidate_meta = {
        "split": "validation only",
        "positive_count": int(len(positives)),
        "negative_count_per_positive": int(negatives_per_positive),
        "candidate_count_total": int(candidates.shape[0] * candidates.shape[1]),
        "negative_source": "uniform_negative_sampling + grouped_negatives; same as standard evaluate_split",
        "pool_seed": pool_seed,
        "grouping_seed": pool_seed + 1,
        "positive_hash": array_hash(positives),
        "negative_hash": array_hash(negatives),
        "grouped_candidate_hash": array_hash(candidates),
        "test_scoring": False,
    }
    write_json(RUNS / "validation_candidate_metadata.json", candidate_meta)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device=device)
    edge_index = edge_index_from_graph(dataset.train_graph(), device)
    branch_scores: dict[str, dict[str, np.ndarray]] = {}
    for label in ("G", "H"):
        model, payload = load_checkpoint_model(Path(baseline[label]["checkpoint"]), device=device)
        pos_out = score_pairs(model, x, edge_index, positives)
        neg_out = score_pairs(model, x, edge_index, negatives.reshape(-1, 2), batch_size=8192)
        branch_scores[label] = {
            "positive": np.asarray(pos_out["logit"], dtype=np.float64),
            "negative": np.asarray(neg_out["logit"], dtype=np.float64).reshape(len(positives), negatives_per_positive),
        }
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    from dcdlp.evaluation.ranking import ranking_metrics, reciprocal_ranks

    score_g = branch_scores["G"]
    score_h = branch_scores["H"]
    rr_g = reciprocal_ranks(score_g["positive"], score_g["negative"])
    rr_h = reciprocal_ranks(score_h["positive"], score_h["negative"])
    mrr_g = float(rr_g.mean())
    mrr_h = float(rr_h.mean())
    for label, actual in (("G", mrr_g), ("H", mrr_h)):
        recorded = float(baseline[label]["validation"]["mrr"])
        if not np.isclose(actual, recorded, atol=1e-12, rtol=0):
            raise RuntimeError(f"candidate export MRR mismatch for {label}: {actual} != {recorded}")

    delta = rr_h - rr_g
    oracle_rr = np.maximum(rr_g, rr_h)
    oracle_mrr = float(oracle_rr.mean())
    best_single = max(mrr_g, mrr_h)
    oracle_gain = oracle_mrr - best_single
    rank_g = 1.0 / rr_g
    rank_h = 1.0 / rr_h
    margin_g = score_g["positive"] - score_g["negative"].max(axis=1)
    mean_margin_g = score_g["positive"] - score_g["negative"].mean(axis=1)
    delta_counts = {
        "hypergraph_wins": int((delta > 0).sum()),
        "graph_wins": int((delta < 0).sum()),
        "ties": int((delta == 0).sum()),
        "total": int(len(delta)),
    }
    score_flat_g = np.concatenate([score_g["positive"][:, None], score_g["negative"]], axis=1).reshape(-1)
    score_flat_h = np.concatenate([score_h["positive"][:, None], score_h["negative"]], axis=1).reshape(-1)

    order = np.argsort(margin_g, kind="mergesort")
    hard_idx, medium_idx, easy_idx = np.array_split(order, 3)
    tertiles = {}
    for name, indices in (("Hard", hard_idx), ("Medium", medium_idx), ("Easy", easy_idx)):
        tertiles[name] = {
            "count": int(len(indices)),
            "graph_margin_min": float(margin_g[indices].min()),
            "graph_margin_max": float(margin_g[indices].max()),
            "graph_mrr": float(rr_g[indices].mean()),
            "raw_hypergraph_mrr": float(rr_h[indices].mean()),
            "delta_mrr": float((rr_h[indices] - rr_g[indices]).mean()),
        }

    summary = {
        "candidate_metadata": candidate_meta,
        "validation_mrr": {"graph_only": mrr_g, "raw_hypergraph": mrr_h},
        "graph_only_best_epoch": int(baseline["G"]["best_epoch"]) + 1,
        "raw_hypergraph_best_epoch": int(baseline["H"]["best_epoch"]) + 1,
        "paired_reciprocal_rank_delta_hg_minus_graph": {
            "hypergraph_wins": delta_counts["hypergraph_wins"],
            "hypergraph_win_percent": 100.0 * delta_counts["hypergraph_wins"] / len(delta),
            "graph_wins": delta_counts["graph_wins"],
            "graph_win_percent": 100.0 * delta_counts["graph_wins"] / len(delta),
            "ties": delta_counts["ties"],
            "tie_percent": 100.0 * delta_counts["ties"] / len(delta),
            "mean_delta_rr": float(delta.mean()),
            "median_delta_rr": float(np.median(delta)),
        },
        "score_correlations_over_all_aligned_validation_candidates": {
            "pearson": _corr(score_flat_g, score_flat_h, "pearson"),
            "spearman": _corr(score_flat_g, score_flat_h, "spearman"),
            "candidate_count": int(len(score_flat_g)),
        },
        "positive_rank_correlations": {
            "pearson": _corr(rank_g, rank_h, "pearson"),
            "spearman": _corr(rank_g, rank_h, "spearman"),
        },
        "graph_hardest_negative_margin_vs_delta_rr": {
            "pearson": _corr(margin_g, delta, "pearson"),
            "spearman": _corr(margin_g, delta, "spearman"),
            "mean_hardest_negative_margin": float(margin_g.mean()),
            "mean_margin_vs_all_negatives": float(mean_margin_g.mean()),
        },
        "graph_margin_tertiles": tertiles,
        "oracle": {
            "oracle_mrr": oracle_mrr,
            "best_single_mrr": best_single,
            "best_single_branch": "Graph-only" if mrr_g >= mrr_h else "Raw-HG",
            "oracle_gain_over_best_single": oracle_gain,
            "strong_complementarity_threshold_0_01": bool(oracle_gain >= 0.01),
            "continue_threshold_0_003": bool(oracle_gain >= 0.003),
        },
        "test_evaluated": False,
    }

    rows = []
    positive_rows = []
    for i in range(len(positives)):
        positive_rows.append({
            "positive_index": i,
            "u": int(positives[i, 0]), "v": int(positives[i, 1]),
            "graph_positive_score": float(score_g["positive"][i]),
            "raw_hg_positive_score": float(score_h["positive"][i]),
            "graph_rank": float(rank_g[i]), "raw_hg_rank": float(rank_h[i]),
            "graph_rr": float(rr_g[i]), "raw_hg_rr": float(rr_h[i]),
            "delta_rr_hg_minus_graph": float(delta[i]),
            "graph_hardest_negative_margin": float(margin_g[i]),
            "graph_mean_negative_margin": float(mean_margin_g[i]),
            "graph_margin_tertile": next(name for name, idx in (("Hard", hard_idx), ("Medium", medium_idx), ("Easy", easy_idx)) if i in set(idx.tolist())),
            "oracle_rr": float(oracle_rr[i]),
        })
        candidate_items = [(int(positives[i, 0]), int(positives[i, 1]), "positive", -1)]
        candidate_items += [
            (int(negatives[i, j, 0]), int(negatives[i, j, 1]), "negative", j)
            for j in range(negatives_per_positive)
        ]
        for j, (u, v, kind, negative_index) in enumerate(candidate_items):
            score_g_j = score_g["positive"][i] if j == 0 else score_g["negative"][i, j - 1]
            score_h_j = score_h["positive"][i] if j == 0 else score_h["negative"][i, j - 1]
            rows.append({
                "positive_index": i, "candidate_kind": kind,
                "negative_index": negative_index, "u": u, "v": v,
                "score_graph": float(score_g_j), "score_raw_hypergraph": float(score_h_j),
                "rank_graph_for_positive": float(rank_g[i]),
                "rank_hypergraph_for_positive": float(rank_h[i]),
                "rr_graph_for_positive": float(rr_g[i]),
                "rr_hypergraph_for_positive": float(rr_h[i]),
                "delta_rr_for_positive": float(delta[i]),
            })

    with (RUNS / "positive_complementarity.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(positive_rows[0]))
        writer.writeheader()
        writer.writerows(positive_rows)
    with (RUNS / "candidate_scores.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    write_json(RUNS / "complementarity_summary.json", summary)
    write_json(RUNS / "baseline_results.json", baseline)
    gain = summary["oracle"]["oracle_gain_over_best_single"]
    gate = "NO_COMPLEMENTARITY_SIGNAL" if gain < 0.003 else "AUDIT_PASS"
    write_status(
        state="complete", stage="complementarity_analysis", current=None,
        completed=["G", "H", "candidate_score_export"],
        graph_only_mrr=mrr_g, raw_hypergraph_mrr=mrr_h,
        oracle_mrr=oracle_mrr, oracle_gain=gain, gate_decision=gate,
        strong_complementarity=(gain >= 0.01), test_evaluated=False,
    )
    print(json.dumps({"status": gate, **summary}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", stage="complementarity_analysis", error=str(exc), test_evaluated=False)
        raise
