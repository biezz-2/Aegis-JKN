"""Evaluation metrics for the Aegis-JKN fraud-detection models.

Every metric here is built on scikit-learn primitives, so the module imports
with the project's pinned dependencies:

* ``compute_auprc`` uses :func:`sklearn.metrics.average_precision_score`, the
  standard step-interpolated average precision. The previous implementation
  integrated the precision-recall curve with ``np.trapz``, which was both the
  wrong definition and unusable because NumPy 2.x removed ``np.trapz``.
* The ``from auc import trapz`` import is gone: ``auc`` is not a dependency of
  this project, and it made the whole ``src.ml.evaluation`` package fail to
  import.

Scores that are mathematically undefined for the given labels (for example
ROC-AUC when ``y_true`` contains a single class) are reported as
``float("nan")``. :func:`compute_all_metrics` replaces every non-finite value
with ``None`` so callers can serialise the result with ``json.dump`` without
producing the non-standard ``NaN`` literal.
"""

from __future__ import annotations

import math
from typing import Any, Dict, Iterable, Sequence

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_recall_curve,
    roc_auc_score,
)

__all__ = [
    "DEFAULT_K_VALUES",
    "compute_all_metrics",
    "compute_auprc",
    "compute_f1_score",
    "compute_precision_at_k",
    "compute_pr_curve",
    "compute_recall_at_k",
    "compute_roc_auc",
]

#: Cut-offs used by :func:`compute_all_metrics` when the caller passes none.
DEFAULT_K_VALUES: Sequence[int] = (100, 500, 1000)


def _prepare_inputs(
    y_true: Iterable[Any], y_prob: Iterable[Any]
) -> tuple[np.ndarray, np.ndarray]:
    """Coerce inputs to equal-length 1-D arrays of int labels and float scores."""
    labels = np.asarray(y_true).ravel()
    scores = np.asarray(y_prob, dtype=float).ravel()
    if labels.size != scores.size:
        raise ValueError(
            "y_true and y_prob must have the same number of elements, "
            f"got {labels.size} and {scores.size}"
        )
    return labels.astype(int), scores


def _single_class(labels: np.ndarray) -> bool:
    """True when ``labels`` contains only one class (metric is undefined)."""
    positives = int(np.count_nonzero(labels))
    return positives == 0 or positives == labels.size


def _top_k_indices(scores: np.ndarray, k: int) -> np.ndarray:
    """Indices of the ``k`` highest scores, highest first (ties are stable)."""
    return np.argsort(-scores, kind="stable")[: max(int(k), 0)]


def _json_safe(value: Any) -> Any:
    """Return ``value`` as a finite float, or ``None`` when it is not finite."""
    if value is None:
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def compute_auprc(y_true, y_prob) -> float:
    """Area under the precision-recall curve (average precision).

    Uses :func:`sklearn.metrics.average_precision_score`, i.e. the standard
    step-interpolated AUPRC. Returns ``nan`` for a single-class ``y_true``
    because average precision is undefined in that case.
    """
    labels, scores = _prepare_inputs(y_true, y_prob)
    if labels.size == 0 or _single_class(labels):
        return float("nan")
    return float(average_precision_score(labels, scores))


def compute_roc_auc(y_true, y_prob) -> float:
    """Receiver operating characteristic AUC.

    Returns ``nan`` when ``y_true`` contains a single class, where ROC-AUC is
    undefined.
    """
    labels, scores = _prepare_inputs(y_true, y_prob)
    if labels.size == 0 or _single_class(labels):
        return float("nan")
    try:
        return float(roc_auc_score(labels, scores))
    except ValueError:  # pragma: no cover - defensive, e.g. non-finite scores
        return float("nan")


def compute_precision_at_k(y_true, y_prob, k: int = 100) -> float:
    """Precision among the top-``k`` scored claims.

    The denominator is ``min(k, N)`` instead of ``k``, so asking for more
    predictions than the sample holds does not shrink the score.
    """
    labels, scores = _prepare_inputs(y_true, y_prob)
    if labels.size == 0 or k <= 0:
        return 0.0
    k_eff = min(int(k), labels.size)
    top = _top_k_indices(scores, k_eff)
    return float(np.count_nonzero(labels[top]) / k_eff)


def compute_recall_at_k(y_true, y_prob, k: int = 100) -> float:
    """Recall among the top-``k`` scored claims, relative to all positives."""
    labels, scores = _prepare_inputs(y_true, y_prob)
    positives = int(np.count_nonzero(labels))
    if labels.size == 0 or positives == 0 or k <= 0:
        return 0.0
    top = _top_k_indices(scores, min(int(k), labels.size))
    return float(np.count_nonzero(labels[top]) / positives)


def compute_f1_score(y_true, y_prob, threshold: float = 0.5) -> float:
    """Binary F1 at a fixed decision ``threshold`` (a claim is positive if >=)."""
    labels, scores = _prepare_inputs(y_true, y_prob)
    if labels.size == 0:
        return 0.0
    predictions = (scores >= threshold).astype(int)
    try:
        return float(f1_score(labels, predictions, zero_division=0))
    except Exception:  # pragma: no cover - sklearn is a hard dependency
        true_positive = int(np.count_nonzero((predictions == 1) & (labels == 1)))
        false_positive = int(np.count_nonzero((predictions == 1) & (labels == 0)))
        false_negative = int(np.count_nonzero((predictions == 0) & (labels == 1)))
        denominator = 2 * true_positive + false_positive + false_negative
        return float(2 * true_positive / denominator) if denominator else 0.0


def compute_pr_curve(y_true, y_prob) -> tuple[np.ndarray, np.ndarray]:
    """Raw ``(precision, recall)`` arrays from scikit-learn, for diagnostics."""
    labels, scores = _prepare_inputs(y_true, y_prob)
    precision, recall, _ = precision_recall_curve(labels, scores)
    return precision, recall


def compute_all_metrics(
    y_true, y_prob, k_values: Iterable[int] | None = None
) -> Dict[str, Any]:
    """Full metric suite with stable keys and JSON-safe values.

    Keys are ``auprc``, ``roc_auc``, ``f1`` plus ``precision@<k>`` and
    ``recall@<k>`` for every cut-off in ``k_values`` (default
    :data:`DEFAULT_K_VALUES`). Values are plain Python floats, or ``None`` when
    a metric is undefined for the labels at hand (e.g. a single-class sample),
    so the mapping never feeds ``NaN`` into :func:`json.dump`.
    """
    labels, scores = _prepare_inputs(y_true, y_prob)
    cut_offs = DEFAULT_K_VALUES if k_values is None else tuple(k_values)

    metrics: Dict[str, float] = {
        "auprc": compute_auprc(labels, scores),
        "roc_auc": compute_roc_auc(labels, scores),
        "f1": compute_f1_score(labels, scores),
    }
    for cut_off in cut_offs:
        k = int(cut_off)
        metrics[f"precision@{k}"] = compute_precision_at_k(labels, scores, k)
        metrics[f"recall@{k}"] = compute_recall_at_k(labels, scores, k)
    return {name: _json_safe(value) for name, value in metrics.items()}
