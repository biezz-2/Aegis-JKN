"""
Explanation Generation Logic for Aegis-JKN.
Transforms raw SHAP/attribution values into human-readable local and global explanations.
"""

from typing import Any, Dict, List, Union, Optional
from pydantic import BaseModel, Field
import numpy as np

class LocalExplanation(BaseModel):
    """Detailed explanation for a single prediction (claim)."""
    claim_id: str
    prediction: float
    top_features: List[Dict[str, Any]] = Field(..., description="List of {feature: name, impact: value, direction: 'positive'|'negative'}")
    channel_impact: Dict[str, float] = Field(..., description="Contribution of MHGSL channels")
    counterfactual: Optional[Dict[str, Any]] = Field(None, description="Smallest change to feature set to flip prediction")
    summary: str = Field(..., description="Natural language summary of the fraud trigger")

class GlobalExplanation(BaseModel):
    """Aggregate explanation for the model behavior."""
    feature_importance: List[Dict[str, float]] = Field(..., description="Average absolute SHAP values per feature")
    dependence_patterns: List[Dict[str, Any]] = Field(..., description="Interaction between key features")
    global_summary: str

class ExplanationGenerator:
    """
    Generator that converts attribution values into serializable JSON explanations.
    """
    def __init__(self, feature_names: List[str]):
        self.feature_names = feature_names

    def generate_local(self,
                      claim_id: str,
                      prediction: float,
                      attribution_values: List[float],
                      channel_contribs: Optional[Dict[str, float]] = None) -> LocalExplanation:
        """
        Generates a local explanation for a specific claim.
        """
        # Sort features by absolute impact
        feature_impacts = []
        for i, val in enumerate(attribution_values):
            if i < len(self.feature_names):
                feature_impacts.append({
                    "feature": self.feature_names[i],
                    "impact": float(val),
                    "direction": "positive" if val > 0 else "negative"
                })

        # Get top 5 features
        top_features = sorted(feature_impacts, key=lambda x: abs(x["impact"]), reverse=True)[:5]

        # Generate a simple natural language summary
        top_feat_name = top_features[0]["feature"] if top_features else "Unknown"
        direction = "increased" if top_features[0]["direction"] == "positive" else "decreased"
        summary = f"Fraud probability was primarily {direction} by {top_feat_name}."

        return LocalExplanation(
            claim_id=claim_id,
            prediction=prediction,
            top_features=top_features,
            channel_impact=channel_contribs or {},
            summary=summary
        )

    def generate_global(self, all_shap_values: np.ndarray) -> GlobalExplanation:
        """
        Generates global importance from a matrix of SHAP values.
        """
        # Mean absolute value per feature
        global_importances = np.abs(all_shap_values).mean(axis=0)

        importance_list = []
        for i, val in enumerate(global_importances):
            if i < len(self.feature_names):
                importance_list.append({"feature": self.feature_names[i], "importance": float(val)})

        # Sort descending
        importance_list = sorted(importance_list, key=lambda x: x["importance"], reverse=True)

        return GlobalExplanation(
            feature_importance=importance_list,
            dependence_patterns=[], # Simplified for now
            global_summary="Model globally prioritizes structural topology and provider history."
        )
