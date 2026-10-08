"""Matched, validation-only V5 Cross-View Hard Negative Mining experiment."""
from __future__ import annotations

import csv
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
RUNS = BASE / "B_CVHNM" / "candidate_runs"
STATUS = BASE / "B_CVHNM" / "candidate_status.json"
RESULTS = BASE / "results.json"
POOL_PER_POSITIVE = 20
ARMS = ("B1", "B2", "B3", "B4")


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


def make_candidate_pool(dataset) -> tuple[np.ndarray, dict, dict[str, np.ndarray]]:
    from dcdlp.data.negative_sampling import grouped_negatives, uniform_negative_sampling
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.utils import array_hash

    positives = np.asarray(dataset.train_pos, dtype=np.int64)
    pool_count = len(positives) * POOL_PER_POSITIVE
    pool_seed = 20261002
    grouping_seed = pool_seed + 1
    pool = uniform_negative_sampling(
        dataset.num_nodes, dataset.all_positive, pool_count, pool_seed
    )
    grouped = grouped_negatives(positives, pool, POOL_PER_POSITIVE, grouping_seed)
    x = torch.as_tensor(dataset.features, dtype=torch.float32, device="cuda")
    edges = edge_index_from_graph(dataset.train_graph(), torch.device("cuda"))
    flat = grouped.reshape(-1, 2)
    scored: dict[str, np.ndarray] = {}
    checkpoints = {
        "Graph": next((BASELINE / "G" / "checkpoints").glob("*.pt")),
        "Raw-HG": next((BASELINE / "H" / "checkpoints").glob("*.pt")),
    }
    for label, checkpoint in checkpoints.items():
        model, _ = load_checkpoint_model(checkpoint, device="cuda")
        output = score_pairs(model, x, edges, flat, batch_size=8192)
        scored[label] = output["logit"].reshape(len(positives), POOL_PER_POSITIVE)
        del model
    metadata = {
        "split": "training positives and training-only uniform negative candidates",
        "positive_hash": array_hash(positives),
        "candidate_pool_hash": array_hash(grouped),
        "pool_seed": pool_seed,
        "grouping_seed": grouping_seed,
        "pool_candidates_per_positive": POOL_PER_POSITIVE,
        "selected_training_negatives_per_positive_per_epoch": 1,
        "teacher_checkpoints": {key: str(value) for key, value in checkpoints.items()},
        "teacher_score_hashes": {key: array_hash(value) for key, value in scored.items()},
        "valid_or_test_labels_used_for_selection": False,
    }
    return grouped, metadata, scored


def rank_rows(scores: np.ndarray) -> np.ndarray:
    return np.argsort(np.argsort(scores, axis=1, kind="stable"), axis=1, kind="stable")


def choose_negatives(grouped: np.ndarray, scores: dict[str, np.ndarray], mode: str, epoch: int) -> np.ndarray:
    rng = np.random.default_rng(400_000 + epoch)
    if mode == "B1":
        index = scores["Graph"].argmax(axis=1)
    elif mode == "B2":
        index = scores["Raw-HG"].argmax(axis=1)
    elif mode == "B3":
        index = rng.integers(0, grouped.shape[1], size=len(grouped))
    elif mode == "B4":
        g_rank = rank_rows(scores["Graph"])
        h_rank = rank_rows(scores["Raw-HG"])
        threshold = (2 * grouped.shape[1]) // 3
        g_hard = (g_rank >= threshold) & (h_rank < threshold)
        h_hard = (h_rank >= threshold) & (g_rank < threshold)
        joint_hard = (g_rank >= threshold) & (h_rank >= threshold)
        assignment_order = np.random.default_rng(44_002).permutation(len(grouped))
        category = np.empty(len(grouped), dtype=np.int8)
        category[assignment_order] = (np.arange(len(grouped)) + epoch) % 3
        index = np.zeros(len(grouped), dtype=np.int64)
        for row in range(len(grouped)):
            if category[row] == 0:
                eligible = np.flatnonzero(g_hard[row])
                if len(eligible) == 0:
                    eligible = np.flatnonzero(g_rank[row] >= threshold)
                index[row] = eligible[np.argmax(scores["Graph"][row, eligible])]
            elif category[row] == 1:
                eligible = np.flatnonzero(h_hard[row])
                if len(eligible) == 0:
                    eligible = np.flatnonzero(h_rank[row] >= threshold)
                index[row] = eligible[np.argmax(scores["Raw-HG"][row, eligible])]
            else:
                eligible = np.flatnonzero(joint_hard[row])
                if len(eligible) == 0:
                    combined = g_rank[row] + h_rank[row]
                    eligible = np.asarray([combined.argmax()])
                index[row] = eligible[np.argmax(
                    scores["Graph"][row, eligible] + scores["Raw-HG"][row, eligible]
                )]
    else:
        raise ValueError(f"Unknown CVHNM arm {mode}")
    return grouped[np.arange(len(grouped)), index]


def source_config(label: str):
    from dcdlp.train import TrainConfig

    raw = json.loads((BASELINE / "H" / "config.json").read_text(encoding="utf-8"))
    values = {key: value for key, value in raw.items() if key in TrainConfig.__dataclass_fields__}
    values.update({
        "pretrain_epochs": 10,
        "disentangle_epochs": 0,
        "hypergraph_mode": "raw",
        "hypergraph_construction": "raw_star",
        "ghhr_training_mode": "none",
        "evaluate_test": False,
        "output_dir": str((RUNS / label).relative_to(ROOT)),
        "device": "cuda",
    })
    return TrainConfig(**values)


def run_arm(label: str, dataset, initial_state: dict[str, torch.Tensor],
            grouped: np.ndarray, scores: dict[str, np.ndarray]) -> dict:
    from dcdlp import train as train_module

    out = RUNS / label
    out.mkdir(parents=True, exist_ok=True)
    config = source_config(label)
    original_optimizer = train_module._build_optimizer
    original_sampler = train_module._sample_train_negatives
    original_evaluate = train_module.evaluate_split
    state = {"active": False, "epoch": 0, "negative_hashes": [], "pair_order_hashes": []}

    def matched_optimizer(model, probes, current_config):
        if current_config is config:
            incompatible = model.load_state_dict(initial_state, strict=False)
            if incompatible.missing_keys or incompatible.unexpected_keys:
                raise RuntimeError(f"{label} state mismatch: {incompatible}")
            if state_hash(model.state_dict()) != state_hash(initial_state):
                raise RuntimeError(f"{label} failed exact Raw-HG initialization copy")
            state["active"] = True
            write_status(state="running", stage="candidate_B_10_epoch",
                         current=f"{label}/epoch_0", completed=[],
                         test_evaluated=False, training_epochs=10)
        return original_optimizer(model, probes, current_config)

    def selected_sampler(current_dataset, current_config, epoch):
        if current_config is not config or not state["active"]:
            return original_sampler(current_dataset, current_config, epoch)
        selected = choose_negatives(grouped, scores, label, epoch)
        state["negative_hashes"].append(train_module.array_hash(selected))
        return selected

    def tracked_evaluate(model, current_dataset, positives, *args, **kwargs):
        result = original_evaluate(model, current_dataset, positives, *args, **kwargs)
        if current_dataset is dataset and np.array_equal(positives, dataset.valid_pos):
            state["epoch"] += 1
            write_status(state="running", stage="candidate_B_10_epoch",
                         current=f"{label}/epoch_{state['epoch']}", completed=[],
                         validation_mrr_so_far=float(result[0]["mrr"]),
                         training_epochs=10, test_evaluated=False)
        return result

    train_module._build_optimizer = matched_optimizer
    train_module._sample_train_negatives = selected_sampler
    train_module.evaluate_split = tracked_evaluate
    try:
        _, result = train_module.train_model(dataset, config)
    finally:
        train_module._build_optimizer = original_optimizer
        train_module._sample_train_negatives = original_sampler
        train_module.evaluate_split = original_evaluate
    if len(result.get("validation_curve", [])) != 10 or state["epoch"] != 10:
        raise RuntimeError(f"{label} did not complete exactly ten validation epochs")
    if len(state["negative_hashes"]) != 10:
        raise RuntimeError(f"{label} did not log ten selected-negative arrays")
    if result.get("metrics") != {} or result.get("evaluation_candidates", {}).get("test_evaluated") is not False:
        raise RuntimeError(f"{label} unexpectedly evaluated test candidates")
    result["selected_negative_hashes_by_epoch"] = state["negative_hashes"]
    result["matched_raw_initial_state_hash"] = state_hash(initial_state)
    result["train_negatives_per_positive_per_epoch"] = 1
    result["test_evaluated"] = False
    write_json(out / "metrics.json", result)
    write_json(out / "config.json", asdict(config))
    return result


def mrr(result: dict) -> float:
    return float(result["validation"]["mrr"])


def main() -> None:
    if not torch.cuda.is_available() or "V100" not in torch.cuda.get_device_name(0):
        raise RuntimeError("Candidate B requires the registered CUDA V100 server")
    from dcdlp.data.loaders import load_dataset
    from dcdlp.data.negative_sampling import uniform_negative_sampling
    from dcdlp.evaluate import load_checkpoint_model
    from dcdlp.train import edge_index_from_graph, score_pairs
    from dcdlp.utils import array_hash

    RUNS.mkdir(parents=True, exist_ok=True)
    result_file = json.loads(RESULTS.read_text(encoding="utf-8"))
    result_file["status"] = "RUNNING"
    result_file["final_decision"] = "CANDIDATE_B_RUNNING"
    result_file["candidates"]["B_CVHNM"] = {"decision": "RUNNING"}
    write_json(RESULTS, result_file)
    write_status(state="running", stage="candidate_B_pool_build",
                 current="training_negative_pool", completed=[], test_evaluated=False)
    dataset = load_dataset("cora", ROOT / "data", "standard", 0)
    grouped, pool_metadata, view_scores = make_candidate_pool(dataset)
    pool_metadata["view_scores_used"] = ["Graph", "Raw-HG"]
    RUNS.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        RUNS / "train_negative_pool.npz",
        train_positive=dataset.train_pos,
        negative_candidates=grouped,
        score_graph=view_scores["Graph"],
        score_raw_hg=view_scores["Raw-HG"],
    )
    write_json(RUNS / "pool_metadata.json", pool_metadata)
    ranks_g = rank_rows(view_scores["Graph"])
    ranks_h = rank_rows(view_scores["Raw-HG"])
    score_csv = RUNS / "train_negative_pool_scores.csv"
    with score_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["positive_index", "negative_index", "u", "v", "score_graph", "score_raw_hg", "rank_graph", "rank_raw_hg"])
        for p_index, negatives in enumerate(grouped):
            for n_index, (u, v) in enumerate(negatives):
                writer.writerow([p_index, n_index, int(u), int(v),
                                 float(view_scores["Graph"][p_index, n_index]),
                                 float(view_scores["Raw-HG"][p_index, n_index]),
                                 int(ranks_g[p_index, n_index]), int(ranks_h[p_index, n_index])])
    del view_scores
    initial_state = torch.load(BASELINE / "raw_initial_state.pt", map_location="cpu", weights_only=True)
    raw_result = json.loads((BASELINE / "H" / "metrics.json").read_text(encoding="utf-8"))
    arms = {"B0": raw_result}
    for label in ARMS:
        # Scores are memory-resident through the pool file so selection is
        # recomputed from the same fixed train-only candidate tensor.
        with np.load(RUNS / "train_negative_pool.npz") as saved:
            score_arrays = {
                "Graph": saved["score_graph"],
                "Raw-HG": saved["score_raw_hg"],
            }
            candidate_array = saved["negative_candidates"]
        result = run_arm(label, dataset, initial_state, candidate_array, score_arrays)
        arms[label] = result
        write_status(state="running", stage="candidate_B_10_epoch",
                     current=f"{label}/complete",
                     completed=[key for key in ARMS if key in arms],
                     validation_mrr_so_far=mrr(result), test_evaluated=False,
                     training_epochs=10)
    baseline_mrr = mrr(arms["B0"])
    b4_mrr = mrr(arms["B4"])
    absolute_gain = b4_mrr - baseline_mrr
    relative_gain = absolute_gain / baseline_mrr
    comparisons = {key: b4_mrr > mrr(arms[key]) for key in ("B0", "B1", "B2", "B3")}
    go = all(comparisons.values()) and (absolute_gain >= 0.003 or relative_gain >= 0.01)
    summary = {
        "decision": "GO" if go else "REJECT",
        "arms": arms,
        "pool_metadata": pool_metadata,
        "B0_mrr": baseline_mrr,
        "B4_mrr": b4_mrr,
        "absolute_gain_over_B0": absolute_gain,
        "relative_gain_over_B0": relative_gain,
        "beats_required_controls": comparisons,
        "go_threshold_met": bool(go),
        "test_evaluated": False,
        "budget_note": "one selected training negative per positive per epoch, matching the audited trainer; a 20-negative-per-positive train-only mining pool supports per-view ranking",
    }
    write_json(RUNS / "candidate_b_summary.json", summary)
    result_file = json.loads(RESULTS.read_text(encoding="utf-8"))
    result_file["candidates"]["B_CVHNM"] = summary
    result_file["status"] = "RUNNING" if go else "COMPLETE"
    result_file["final_decision"] = "CANDIDATE_B_GO_CONFIRMATION_PENDING" if go else "CANDIDATE_B_REJECT_NEXT_C"
    if go:
        result_file["candidates"]["C_DAF"] = {"decision": "STOPPED_AFTER_B_GO"}
    write_json(RESULTS, result_file)
    write_status(state="complete" if not go else "running",
                 stage="candidate_B_go" if go else "candidate_B_rejected",
                 current=None if not go else "confirmation_pending",
                 completed=["B0", "B1", "B2", "B3", "B4"],
                 final_decision="B_REJECT_NEXT_C" if not go else "B_GO_CONFIRMATION_PENDING",
                 test_evaluated=False)
    print(json.dumps({"decision": summary["decision"],
                      "validation_mrr": {key: mrr(value) for key, value in arms.items()},
                      "absolute_gain": absolute_gain, "relative_gain": relative_gain,
                      "test_evaluated": False}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_status(state="failed", stage="candidate_B", current=None,
                     error=f"{type(exc).__name__}: {exc}", test_evaluated=False)
        raise
