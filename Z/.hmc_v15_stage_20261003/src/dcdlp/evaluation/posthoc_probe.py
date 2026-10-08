from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import networkx as nx
import numpy as np

from dcdlp.utils import array_hash


def canonical_pair(pair: Iterable[int]) -> tuple[int, int]:
    """Return an undirected pair in deterministic endpoint order."""
    values = np.asarray(list(pair), dtype=np.int64).reshape(-1)
    if values.size != 2:
        raise ValueError(f"A pair must contain exactly two endpoints, got {values}")
    u, v = int(values[0]), int(values[1])
    if u == v:
        raise ValueError("A probe pair must not be a self-loop")
    return (u, v) if u < v else (v, u)


def context_graph_edges(graph: nx.Graph) -> np.ndarray:
    """Return canonical undirected graph edges for stable protocol hashing."""
    edges = sorted(canonical_pair(edge) for edge in graph.edges())
    if not edges:
        return np.empty((0, 2), dtype=np.int64)
    return np.asarray(edges, dtype=np.int64).reshape(-1, 2)


def context_graph_hash(graph: nx.Graph) -> str:
    """Hash the complete canonical edge set of a context graph."""
    return array_hash(context_graph_edges(graph))


def remove_target_edge_if_present(
    graph: nx.Graph, pair: Iterable[int]
) -> nx.Graph:
    """Copy ``graph`` and remove only the supplied undirected target edge."""
    u, v = canonical_pair(pair)
    context = graph.copy()
    if context.has_edge(u, v):
        context.remove_edge(u, v)
    return context


def degree_bin_boundaries(train_values: Iterable[float], bins: int = 10) -> np.ndarray:
    values = np.asarray(list(train_values), dtype=float)
    if len(values) == 0:
        raise ValueError("Training values are empty")
    quantiles = np.linspace(0.0, 1.0, bins + 1)[1:-1]
    return np.unique(np.quantile(values, quantiles))


def apply_degree_bins(values: Iterable[float], boundaries: np.ndarray) -> np.ndarray:
    return np.digitize(np.asarray(list(values), dtype=float), boundaries).astype(int)


def _classification_metrics(y_true, y_pred) -> dict[str, float]:
    from sklearn.metrics import accuracy_score, f1_score

    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "macro_f1": float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
    }


def _regression_metrics(y_true, y_pred) -> dict[str, float]:
    from scipy.stats import spearmanr
    from sklearn.metrics import mean_absolute_error, r2_score

    correlation = spearmanr(y_true, y_pred).statistic
    return {
        "r2": float(r2_score(y_true, y_pred)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "spearman": float(correlation) if np.isfinite(correlation) else 0.0,
    }


@dataclass
class ProbeResult:
    task: str
    selected_hyperparameter: float
    validation_metric: float
    test_metrics: dict[str, float]
    test_predictions: np.ndarray
    architecture: str
    hyperparameter_candidates: tuple[float, ...]
    seed: int
    diagnostics: dict[str, object] = field(default_factory=dict)


def classification_probe(
    train_x,
    train_y,
    valid_x,
    valid_y,
    test_x,
    test_y,
    *,
    seed: int = 0,
    candidates: tuple[float, ...] = (0.01, 0.1, 1.0, 10.0),
) -> ProbeResult:
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    best_c, best_metric = None, -np.inf
    for candidate in candidates:
        model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                C=candidate, max_iter=2_000, random_state=seed,
                class_weight="balanced",
            ),
        )
        model.fit(train_x, train_y)
        metric = _classification_metrics(valid_y, model.predict(valid_x))["macro_f1"]
        if metric > best_metric + 1e-12:
            best_c, best_metric = candidate, metric
    combined_x = np.concatenate([np.asarray(train_x), np.asarray(valid_x)])
    combined_y = np.concatenate([np.asarray(train_y), np.asarray(valid_y)])
    final_model = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            C=float(best_c), max_iter=2_000, random_state=seed,
            class_weight="balanced",
        ),
    ).fit(combined_x, combined_y)
    predictions = final_model.predict(test_x)
    return ProbeResult(
        task="classification",
        selected_hyperparameter=float(best_c),
        validation_metric=float(best_metric),
        test_metrics=_classification_metrics(test_y, predictions),
        test_predictions=np.asarray(predictions),
        architecture="StandardScaler+LogisticRegression",
        hyperparameter_candidates=tuple(map(float, candidates)),
        seed=int(seed),
    )


def regression_probe(
    train_x,
    train_y,
    valid_x,
    valid_y,
    test_x,
    test_y,
    *,
    seed: int = 0,
    candidates: tuple[float, ...] = (0.01, 0.1, 1.0, 10.0, 100.0),
) -> ProbeResult:
    from sklearn.linear_model import Ridge
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    train_x = np.asarray(train_x, dtype=float)
    valid_x = np.asarray(valid_x, dtype=float)
    test_x = np.asarray(test_x, dtype=float)
    train_y = np.asarray(train_y, dtype=float)
    valid_y = np.asarray(valid_y, dtype=float)
    test_y = np.asarray(test_y, dtype=float)
    for name, value in {
        "train_x": train_x, "valid_x": valid_x, "test_x": test_x,
        "train_y": train_y, "valid_y": valid_y, "test_y": test_y,
    }.items():
        if not np.isfinite(value).all():
            raise ValueError(f"Probe input contains NaN/Inf in {name}")

    best_alpha, best_mae = None, np.inf
    for candidate in candidates:
        model = make_pipeline(StandardScaler(), Ridge(alpha=candidate))
        model.fit(train_x, train_y)
        metric = _regression_metrics(valid_y, model.predict(valid_x))["mae"]
        if metric < best_mae - 1e-12:
            best_alpha, best_mae = candidate, metric
    combined_x = np.concatenate([train_x, valid_x])
    combined_y = np.concatenate([train_y, valid_y])
    final_model = make_pipeline(
        StandardScaler(), Ridge(alpha=float(best_alpha))
    ).fit(combined_x, combined_y)
    predictions = final_model.predict(test_x)
    scaler = final_model.named_steps["standardscaler"]

    def feature_stats(values: np.ndarray) -> dict[str, object]:
        return {
            "mean": np.mean(values, axis=0).astype(float).tolist(),
            "std": np.std(values, axis=0).astype(float).tolist(),
        }

    def max_abs_standardized(values: np.ndarray) -> float:
        transformed = scaler.transform(values)
        return float(np.max(np.abs(transformed))) if transformed.size else 0.0

    x_diagnostics = {
        "train": feature_stats(train_x),
        "valid": feature_stats(valid_x),
        "test": feature_stats(test_x),
        "scaler_mean": scaler.mean_.astype(float).tolist(),
        "scaler_scale": scaler.scale_.astype(float).tolist(),
        "min_scaler_scale": float(np.min(scaler.scale_)),
        "median_scaler_scale": float(np.median(scaler.scale_)),
        "max_scaler_scale": float(np.max(scaler.scale_)),
        "near_constant_feature_count": int(
            np.sum(np.std(train_x, axis=0) < 1e-6)
        ),
        "max_abs_standardized_train": max_abs_standardized(train_x),
        "max_abs_standardized_valid": max_abs_standardized(valid_x),
        "max_abs_standardized_test": max_abs_standardized(test_x),
        "final_scaler_fit": "train_plus_valid",
    }

    def target_stats(values: np.ndarray) -> dict[str, object]:
        return {
            "count": int(len(values)),
            "mean": float(np.mean(values)) if len(values) else 0.0,
            "std": float(np.std(values)) if len(values) else 0.0,
            "min": float(np.min(values)) if len(values) else 0.0,
            "max": float(np.max(values)) if len(values) else 0.0,
        }

    return ProbeResult(
        task="regression",
        selected_hyperparameter=float(best_alpha),
        validation_metric=float(best_mae),
        test_metrics=_regression_metrics(test_y, predictions),
        test_predictions=np.asarray(predictions),
        architecture="StandardScaler+Ridge",
        hyperparameter_candidates=tuple(map(float, candidates)),
        seed=int(seed),
        diagnostics={
            "x": x_diagnostics,
            "target": {
                "train": target_stats(train_y),
                "valid": target_stats(valid_y),
                "test": target_stats(test_y),
            },
        },
    )
