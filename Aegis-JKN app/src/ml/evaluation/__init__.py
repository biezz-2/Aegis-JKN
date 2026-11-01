"""Aegis-JKN evaluation benchmark suite.

Public surface:

* :mod:`.metrics` -- pure NumPy/scikit-learn metrics, always importable.
* Optional heavier sub-modules (``splits``, ``robustness``, ``baselines``,
  ``report``, ``benchmark``) -- each is imported inside its own ``try`` /
  ``except`` so a missing optional dependency (PyTorch, PyTorch Geometric,
  XGBoost, pandas) can never make the whole package unimportable.

The availability flags (``HAS_METRICS``, ``HAS_BENCHMARK``, ...) tell callers
what is usable, and ``IMPORT_ERRORS`` keeps the underlying reason. Metrics are
imported first so they are available even when every optional sub-module fails.
"""

from __future__ import annotations

import importlib
from typing import Dict, Tuple

from .metrics import (
    compute_all_metrics,
    compute_auprc,
    compute_f1_score,
    compute_precision_at_k,
    compute_recall_at_k,
    compute_roc_auc,
)

__all__ = [
    "compute_auprc",
    "compute_roc_auc",
    "compute_precision_at_k",
    "compute_recall_at_k",
    "compute_f1_score",
    "compute_all_metrics",
]

#: Optional sub-modules mapped to the names each one is expected to expose.
_OPTIONAL_EXPORTS: Dict[str, Tuple[str, ...]] = {
    "splits": ("TemporalSplitter",),
    "robustness": ("MaskingRobustnessTest", "CamouflageTest"),
    "baselines": ("XGBoostBaseline", "GCNBaseline", "LogisticRegressionBaseline"),
    "report": ("generate_report",),
    "benchmark": ("BenchmarkSuite",),
}

#: ``sub-module name -> "ExceptionType: message"`` for optional imports that failed.
IMPORT_ERRORS: Dict[str, str] = {}


def _import_optional() -> None:
    """Import optional sub-modules without letting one failure break the package."""
    for module_name, names in _OPTIONAL_EXPORTS.items():
        try:
            module = importlib.import_module("." + module_name, __name__)
        except Exception as exc:  # optional heavy dependencies may be missing
            IMPORT_ERRORS[module_name] = f"{type(exc).__name__}: {exc}"
            module = None
        for name in names:
            value = getattr(module, name, None) if module is not None else None
            if value is None and module is not None:
                IMPORT_ERRORS.setdefault(
                    module_name, f"AttributeError: {name!r} is not exported"
                )
            globals()[name] = value
            if value is not None:
                __all__.append(name)


_import_optional()
del _import_optional

HAS_METRICS = True
HAS_SPLITS = "splits" not in IMPORT_ERRORS
HAS_ROBUSTNESS = "robustness" not in IMPORT_ERRORS
HAS_BASELINES = "baselines" not in IMPORT_ERRORS
HAS_REPORT = "report" not in IMPORT_ERRORS
HAS_BENCHMARK = "benchmark" not in IMPORT_ERRORS
HAS_FULL_SUITE = all(
    (HAS_SPLITS, HAS_ROBUSTNESS, HAS_BASELINES, HAS_REPORT, HAS_BENCHMARK)
)
BENCHMARK_IMPORT_ERROR = IMPORT_ERRORS.get("benchmark")

__all__ += [
    "HAS_METRICS",
    "HAS_SPLITS",
    "HAS_ROBUSTNESS",
    "HAS_BASELINES",
    "HAS_REPORT",
    "HAS_BENCHMARK",
    "HAS_FULL_SUITE",
    "BENCHMARK_IMPORT_ERROR",
    "IMPORT_ERRORS",
]