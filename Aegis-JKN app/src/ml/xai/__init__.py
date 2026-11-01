"""
XAI (Explainable AI) Module for Aegis-JKN
Provides SHAP-based explanations for Tier-2 (XGBoost) and Tier-3 (MHGSL) models.
"""

from .shap_explainer import SHAPExplainer, Tier2Explainer, Tier3Explainer
from .explanation_generator import ExplanationGenerator, LocalExplanation, GlobalExplanation

__all__ = [
    "SHAPExplainer",
    "Tier2Explainer",
    "Tier3Explainer",
    "ExplanationGenerator",
    "LocalExplanation",
    "GlobalExplanation",
]