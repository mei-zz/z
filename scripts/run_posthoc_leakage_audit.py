"""Independent frozen-checkpoint leakage probes (Post-hoc Probe Protocol V2).

V2 deliberately evaluates one pair at a time. Each pair receives a context
graph made from ``train_graph`` with only that pair removed when it exists.
The same context graph is used for both the model representation and the
structural probe target.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from dcdlp.data.loaders import load_dataset
from dcdlp.data.pair_statistics import pair_features
from dcdlp.evaluate import load_checkpoint_model
from dcdlp.evaluation.posthoc_probe import (
    context_graph_hash,
    context_graph_edges,
    regression_probe,
    remove_target_edge_if_present,
)
from dcdlp.train import (
    TrainConfig,
    edge_index_from_graph,
    fit_training_cn_residualizer,
)
from dcdlp.utils import array_hash, write_json


PROTOCOL_VERSION = "posthoc_probe_v2"
PROBE_SPECS = {
    "z_cn_to_degree": ("z_cn", "degree", "cross_leakage"),
    "z_residual_to_degree": (
        "z_residual", "degree", "cross_leakage"
    ),
    "z_degree_to_cn_residual": (
        "z_degree", "cn_residual", "cross_leakage"
    ),
    "z_degree_to_degree": ("z_degree", "degree", "target_retention"),
    "z_cn_to_cn_residual": (
        "z_cn", "cn_residual", "target_retention"
    ),
}


def _fixed_subset(pairs: np.ndarray, limit: int, seed: int) -> np.ndarray:
    """Sample a deterministic subset; seed now belongs to the probe repeat."""
    pairs = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    if limit <= 0 or len(pairs) <= limit:
        return pairs.copy()
    rng = np.random.default_rng(seed)
    indices = np.sort(rng.choice(len(pairs), size=limit, replace=False))
    return pairs[indices].copy()


def _sampling_seed(base_seed: int, probe_seed: int, split_offset: int) -> int:
    """Derive split-specific seeds without depending on model label."""
    return int(base_seed) + 1_000_003 * int(probe_seed) + int(split_offset)


def _config_from_payload(payload: dict) -> TrainConfig:
    known = TrainConfig.__dataclass_fields__
    return TrainConfig(**{
        key: value for key, value in payload["config"].items()
        if key in known
    })


def _canonical_pair_set(pairs: np.ndarray) -> set[tuple[int, int]]:
    values = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    return {
        (int(min(u, v)), int(max(u, v)))
        for u, v in values
    }


def _assert_selected_splits_are_disjoint(
    split_pairs: dict[str, np.ndarray],
) -> None:
    sets = {
        split: _canonical_pair_set(pairs)
        for split, pairs in split_pairs.items()
    }
    for left, right in (("train", "valid"), ("train", "test"), ("valid", "test")):
        overlap = sets[left] & sets[right]
        if overlap:
            raise AssertionError(
                f"Probe pair leakage between {left} and {right}: "
                f"{len(overlap)} canonical pairs"
            )


def _assert_context_graph(
    base_graph,
    context_graph,
    pair: np.ndarray,
    *,
    split: str,
) -> dict[str, int | bool]:
    """Assert that context construction removed exactly the permitted edge."""
    values = np.asarray(pair, dtype=np.int64).reshape(-1)
    if values.size != 2:
        raise AssertionError(f"Invalid pair shape: {values}")
    u, v = int(values[0]), int(values[1])
    canonical = (min(u, v), max(u, v))
    base_edges = {
        tuple(edge) for edge in context_graph_edges(base_graph).tolist()
    }
    context_edges = {
        tuple(edge) for edge in context_graph_edges(context_graph).tolist()
    }
    removed = base_edges - context_edges
    added = context_edges - base_edges
    target_present = canonical in base_edges

    if split == "train":
        if not target_present:
            raise AssertionError(
                f"Train target edge {canonical} is absent from train_graph"
            )
        expected_removed = {canonical}
        expected_edge_delta = 1
    elif split in {"valid", "test"}:
        if target_present:
            raise AssertionError(
                f"{split} target edge {canonical} unexpectedly exists in train_graph"
            )
        expected_removed = set()
        expected_edge_delta = 0
    else:
        raise ValueError(f"Unknown split: {split}")

    if removed != expected_removed or added:
        raise AssertionError(
            f"Context graph changed unexpected edges for {split} pair {canonical}: "
            f"removed={removed}, added={added}"
        )
    actual_edge_delta = len(base_edges) - len(context_edges)
    if actual_edge_delta != expected_edge_delta:
        raise AssertionError(
            f"Unexpected edge count delta for {split} pair {canonical}: "
            f"expected={expected_edge_delta}, actual={actual_edge_delta}"
        )
    return {
        "target_present_before": bool(target_present),
        "removed_edge_count": int(len(removed)),
        "base_edge_count": int(len(base_edges)),
        "context_edge_count": int(len(context_edges)),
    }


def _extract_contextual_pairs(
    model,
    x,
    base_graph,
    pairs: np.ndarray,
    node_features: np.ndarray,
    residualizer,
    *,
    split: str,
) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], list[dict]]:
    """Extract one representation and one target from one graph per pair."""
    import torch

    pair_array = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    if len(pair_array) == 0:
        raise ValueError(f"Cannot run a probe on an empty {split} split")

    representations: dict[str, list[np.ndarray]] = {
        key: [] for key in ("z_degree", "z_cn", "z_residual")
    }
    statistic_rows: dict[str, list[float]] = {
        key: [] for key in (
            "degree_u", "degree_v", "degree", "degree_score", "cn",
            "cn_residual",
        )
    }
    context_rows: list[dict] = []
    model.eval()
    if model.training:
        raise AssertionError("Probe model must be in eval mode")

    for pair_index, pair in enumerate(pair_array):
        context_graph = remove_target_edge_if_present(base_graph, pair)
        audit = _assert_context_graph(
            base_graph, context_graph, pair, split=split
        )
        graph_hash = context_graph_hash(context_graph)
        context_edges = edge_index_from_graph(context_graph, x.device)
        pair_batch = torch.as_tensor(
            pair.reshape(1, 2), dtype=torch.long, device=x.device
        )

        # The graph has already been made pair-specific. Calling the model
        # with remove_target_edges=False prevents a second batch-level mask.
        with torch.no_grad():
            outputs = model(
                x,
                context_edges,
                pair_batch,
                remove_target_edges=False,
            )
        for key in representations:
            value = outputs[key]
            if not torch.isfinite(value).all():
                raise AssertionError(
                    f"Representation {key} contains NaN/Inf for {split} "
                    f"pair index {pair_index}"
                )
            representations[key].append(
                value[0].detach().cpu().numpy().astype(float, copy=False)
            )

        stats = pair_features(
            context_graph,
            pair.reshape(1, 2),
            node_features,
        )
        _, residual = residualizer.residual(stats)
        target_values = {
            "degree_u": stats["degree_u"][0],
            "degree_v": stats["degree_v"][0],
            "degree": stats["degree_score"][0],
            "degree_score": stats["degree_score"][0],
            "cn": stats["cn"][0],
            "cn_residual": residual[0],
        }
        for key, value in target_values.items():
            statistic_rows[key].append(float(value))

        # X and y are built from the same context_graph object and hash.
        context_rows.append({
            "split": split,
            "pair_index": int(pair_index),
            "u": int(pair[0]),
            "v": int(pair[1]),
            "context_graph_hash": graph_hash,
            **audit,
            "representation_context_graph_hash": graph_hash,
            "target_context_graph_hash": graph_hash,
            "xy_context_hash_match": True,
        })

    representation_arrays = {
        key: np.stack(values, axis=0)
        for key, values in representations.items()
    }
    statistic_arrays = {
        key: np.asarray(values, dtype=float)
        for key, values in statistic_rows.items()
    }
    for key, value in representation_arrays.items():
        if not np.isfinite(value).all():
            raise AssertionError(f"Representation {key} contains NaN/Inf")
    for key, value in statistic_arrays.items():
        if not np.isfinite(value).all():
            raise AssertionError(f"Target statistic {key} contains NaN/Inf")
    return representation_arrays, statistic_arrays, context_rows


def _numeric_target_diagnostics(values: np.ndarray) -> dict[str, object]:
    values = np.asarray(values, dtype=float)
    if not np.isfinite(values).all():
        raise AssertionError("Target contains NaN/Inf")
    return {
        "count": int(len(values)),
        "mean": float(np.mean(values)) if len(values) else 0.0,
        "std": float(np.std(values)) if len(values) else 0.0,
        "min": float(np.min(values)) if len(values) else 0.0,
        "max": float(np.max(values)) if len(values) else 0.0,
    }


def run_posthoc_leakage_audit(
    checkpoint: Path,
    data_root: Path,
    output_dir: Path,
    *,
    probe_seeds: tuple[int, ...] = (0, 1, 2),
    max_pairs_per_split: int = 0,
    pair_sample_seed: int = 0,
    device: str = "cpu",
) -> dict:
    # Existing trusted checkpoints serialize ConditionalCNRegressor. PyTorch
    # 2.6+ defaults torch.load to weights_only=True, which cannot deserialize
    # that checkpoint payload. Scope the compatibility setting to this probe
    # process rather than changing the general checkpoint loader.
    import os

    os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
    import torch

    requested_device = "cuda" if device == "auto" and torch.cuda.is_available() else device
    if requested_device == "auto":
        requested_device = "cpu"
    if requested_device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("Probe requested CUDA but torch.cuda.is_available() is false")
    model, payload = load_checkpoint_model(checkpoint, requested_device)
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    model.eval()
    if model.training or any(parameter.requires_grad for parameter in model.parameters()):
        raise AssertionError("Post-hoc model must be frozen and in eval mode")

    config = payload["config"]
    dataset = load_dataset(
        config["dataset"],
        data_root,
        config.get("protocol_eval", "standard"),
        config["seed"],
    )
    train_config = _config_from_payload(payload)
    residualizer = payload.get("cn_regressor")
    residualizer_metadata = payload.get("cn_feature_metadata", {})
    if residualizer is None:
        residualizer, residualizer_metadata = fit_training_cn_residualizer(
            dataset, train_config
        )
    if residualizer is None:
        raise RuntimeError("A train-only CN residualizer is required for probes")

    x = torch.as_tensor(
        dataset.features, dtype=torch.float32, device=torch.device(requested_device)
    )
    base_graph = dataset.train_graph()
    rows: list[dict] = []
    prediction_rows: list[dict] = []
    top_error_rows: list[dict] = []
    diagnostics: list[dict] = []
    context_rows_all: list[dict] = []
    pair_hashes_by_probe_seed: dict[str, dict[str, str]] = {}
    protocol_assertion_counts = {
        "selected_split_disjoint_checks": 0,
        "train_target_edge_checks": 0,
        "valid_test_noop_checks": 0,
        "xy_context_hash_match_checks": 0,
        "representation_finite_checks": 0,
        "target_finite_checks": 0,
    }

    for probe_seed in probe_seeds:
        split_pairs: dict[str, np.ndarray] = {}
        split_data: dict[str, dict[str, object]] = {}
        for offset, split in enumerate(("train", "valid", "test")):
            split_pairs[split] = _fixed_subset(
                getattr(dataset, f"{split}_pos"),
                max_pairs_per_split,
                _sampling_seed(pair_sample_seed, probe_seed, offset),
            )
        _assert_selected_splits_are_disjoint(split_pairs)
        protocol_assertion_counts["selected_split_disjoint_checks"] += 1

        for split in ("train", "valid", "test"):
            representations, stats, context_rows = _extract_contextual_pairs(
                model,
                x,
                base_graph,
                split_pairs[split],
                dataset.features,
                residualizer,
                split=split,
            )
            for context_row in context_rows:
                context_row["probe_seed"] = int(probe_seed)
                context_rows_all.append(context_row)
                protocol_assertion_counts["xy_context_hash_match_checks"] += 1
                if split == "train":
                    protocol_assertion_counts["train_target_edge_checks"] += 1
                else:
                    protocol_assertion_counts["valid_test_noop_checks"] += 1
            protocol_assertion_counts["representation_finite_checks"] += len(
                split_pairs[split]
            ) * 3
            protocol_assertion_counts["target_finite_checks"] += len(
                split_pairs[split]
            )
            split_data[split] = {
                "representations": representations,
                "stats": stats,
                "context_rows": context_rows,
            }

        pair_hashes_by_probe_seed[str(probe_seed)] = {
            split: array_hash(split_pairs[split])
            for split in ("train", "valid", "test")
        }

        for probe_name, (representation, target, role) in PROBE_SPECS.items():
            result = regression_probe(
                split_data["train"]["representations"][representation],
                split_data["train"]["stats"][target],
                split_data["valid"]["representations"][representation],
                split_data["valid"]["stats"][target],
                split_data["test"]["representations"][representation],
                split_data["test"]["stats"][target],
                seed=probe_seed,
            )
            base = {
                "protocol_version": PROTOCOL_VERSION,
                "probe": probe_name,
                "role": role,
                "representation": representation,
                "target": target,
                "probe_seed": int(probe_seed),
                "probe_sample_seed": int(probe_seed),
                "architecture": result.architecture,
                "hyperparameter_candidates": ";".join(
                    map(str, result.hyperparameter_candidates)
                ),
                "selected_hyperparameter": result.selected_hyperparameter,
                "validation_metric": result.validation_metric,
                "train_count": len(split_pairs["train"]),
                "valid_count": len(split_pairs["valid"]),
                "test_count": len(split_pairs["test"]),
            }
            rows.append({**base, **result.test_metrics})

            result_diagnostics = {
                "probe": probe_name,
                "role": role,
                "representation": representation,
                "target": target,
                "probe_seed": int(probe_seed),
                "pair_hashes": pair_hashes_by_probe_seed[str(probe_seed)],
                "selected_hyperparameter": result.selected_hyperparameter,
                "validation_metric": result.validation_metric,
                "test_metrics": result.test_metrics,
                **result.diagnostics,
            }
            result_diagnostics["target"] = {
                split: _numeric_target_diagnostics(
                    split_data[split]["stats"][target]
                )
                for split in ("train", "valid", "test")
            }
            diagnostics.append(result_diagnostics)

            test_pairs = split_pairs["test"]
            test_stats = split_data["test"]["stats"]
            errors = np.abs(
                test_stats[target] - np.asarray(result.test_predictions)
            )
            order = np.argsort(-errors, kind="stable")[:20]
            for rank, index in enumerate(order, start=1):
                pair = test_pairs[index]
                prediction = float(result.test_predictions[index])
                target_value = float(test_stats[target][index])
                context_row = split_data["test"]["context_rows"][index]
                top_error_rows.append({
                    "probe": probe_name,
                    "probe_seed": int(probe_seed),
                    "rank": int(rank),
                    "pair_id": f"test-{probe_seed}-{int(index)}",
                    "u": int(pair[0]),
                    "v": int(pair[1]),
                    "degree_u": float(test_stats["degree_u"][index]),
                    "degree_v": float(test_stats["degree_v"][index]),
                    "cn": float(test_stats["cn"][index]),
                    "target": target_value,
                    "prediction": prediction,
                    "residual": target_value - prediction,
                    "absolute_error": float(errors[index]),
                    "context_graph_hash": context_row["context_graph_hash"],
                })

            for index, prediction in enumerate(result.test_predictions):
                pair = test_pairs[index]
                context_row = split_data["test"]["context_rows"][index]
                target_value = float(test_stats[target][index])
                prediction_value = float(prediction)
                prediction_rows.append({
                    "probe": probe_name,
                    "probe_seed": int(probe_seed),
                    "pair_id": f"test-{probe_seed}-{int(index)}",
                    "u": int(pair[0]),
                    "v": int(pair[1]),
                    "degree_u": float(test_stats["degree_u"][index]),
                    "degree_v": float(test_stats["degree_v"][index]),
                    "cn": float(test_stats["cn"][index]),
                    "cn_residual": float(test_stats["cn_residual"][index]),
                    "target": target_value,
                    "prediction": prediction_value,
                    "residual": target_value - prediction_value,
                    "absolute_error": abs(target_value - prediction_value),
                    "context_graph_hash": context_row["context_graph_hash"],
                })

    metric_names = ("r2", "mae", "spearman")
    summary_rows: list[dict] = []
    for probe_name in PROBE_SPECS:
        local = [row for row in rows if row["probe"] == probe_name]
        for metric in metric_names:
            values = np.asarray([row[metric] for row in local], dtype=float)
            summary_rows.append({
                "protocol_version": PROTOCOL_VERSION,
                "probe": probe_name,
                "role": local[0]["role"],
                "metric": metric,
                "aggregation": "probe_sample_seed_within_checkpoint",
                "mean": float(values.mean()),
                "std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
                "median": float(np.median(values)),
                "min": float(values.min()),
                "max": float(values.max()),
                "count": len(values),
                "seeds": ";".join(map(str, probe_seeds)),
            })

    output_dir.mkdir(parents=True, exist_ok=True)

    def write_csv(name: str, values: list[dict]) -> None:
        if not values:
            return
        with (output_dir / name).open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=list(values[0]))
            writer.writeheader()
            writer.writerows(values)

    write_csv("posthoc_probe.csv", rows)
    write_csv("posthoc_probe_summary.csv", summary_rows)
    write_csv("posthoc_probe_predictions.csv", prediction_rows)
    write_csv("posthoc_probe_top20_errors.csv", top_error_rows)
    write_csv("posthoc_probe_contexts.csv", context_rows_all)
    write_json(output_dir / "posthoc_probe_diagnostics.json", {
        "protocol_version": PROTOCOL_VERSION,
        "diagnostics": diagnostics,
    })

    first_seed = str(probe_seeds[0]) if probe_seeds else None
    metadata = {
        "protocol_version": PROTOCOL_VERSION,
        "checkpoint": str(checkpoint.resolve()),
        "dataset": dataset.name,
        "model_seed": int(config["seed"]),
        "probe_seeds": list(probe_seeds),
        "probe_sample_seed_semantics": (
            "probe_seed controls split pair sampling; no model label is used"
        ),
        "pair_sample_seed": int(pair_sample_seed),
        "sampling_seed_formula": "base + 1000003 * probe_seed + split_offset",
        "pair_split_hashes": (
            pair_hashes_by_probe_seed[first_seed] if first_seed is not None else {}
        ),
        "pair_split_hashes_by_probe_seed": pair_hashes_by_probe_seed,
        "residualizer": residualizer_metadata,
        "model_frozen": all(
            not parameter.requires_grad for parameter in model.parameters()
        ),
        "model_eval": not model.training,
        "device": requested_device,
        "test_not_used_for_selection": True,
        "context_graph_policy": (
            "per-pair train_graph with only the undirected target edge removed "
            "when present; valid/test removal is a no-op"
        ),
        "representation_forward": (
            "direct model forward on pre-built context graph with "
            "remove_target_edges=False"
        ),
        "protocol_assertions": protocol_assertion_counts,
        "files": {
            "per_seed": str(output_dir / "posthoc_probe.csv"),
            "summary": str(output_dir / "posthoc_probe_summary.csv"),
            "predictions": str(output_dir / "posthoc_probe_predictions.csv"),
            "top20_errors": str(output_dir / "posthoc_probe_top20_errors.csv"),
            "contexts": str(output_dir / "posthoc_probe_contexts.csv"),
            "diagnostics": str(output_dir / "posthoc_probe_diagnostics.json"),
        },
    }
    write_json(output_dir / "posthoc_probe_metadata.json", metadata)
    return {"rows": rows, "summary": summary_rows, "metadata": metadata}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--data-root", default="data")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--probe-seeds", default="0,1,2")
    parser.add_argument("--max-pairs-per-split", type=int, default=0)
    parser.add_argument("--pair-sample-seed", type=int, default=0)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()
    result = run_posthoc_leakage_audit(
        Path(args.checkpoint),
        Path(args.data_root),
        Path(args.output_dir),
        probe_seeds=tuple(
            int(value) for value in args.probe_seeds.split(",") if value
        ),
        max_pairs_per_split=args.max_pairs_per_split,
        pair_sample_seed=args.pair_sample_seed,
        device=args.device,
    )
    print(result["metadata"]["files"]["summary"])


if __name__ == "__main__":
    main()
