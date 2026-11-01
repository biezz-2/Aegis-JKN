"""
SHAP Attribution Logic for Aegis-JKN.
Implements TreeExplainer for XGBoost and Integrated Gradients / GNNExplainer approximations for MHGSL.
"""

import numpy as np
import torch
import shap
from typing import Any, Dict, List, Tuple, Union, Optional
import logging

logger = logging.getLogger(__name__)

class SHAPExplainer:
    """Base class for attribution explainers."""
    def explain(self, model: Any, data: Any) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement explain()")

class Tier2Explainer(SHAPExplainer):
    """
    SHAP TreeExplainer for XGBoost (Tier-2).
    Computes exact SHAP values for tree-based models.
    """
    def __init__(self, model: Any, feature_names: List[str]):
        self.model = model
        self.feature_names = feature_names
        # Initialize TreeExplainer for XGBoost
        self.explainer = shap.TreeExplainer(self.model)

    def explain(self, X: np.ndarray) -> Dict[str, Any]:
        """
        Computes SHAP values for a given set of samples.

        Args:
            X: Input feature matrix (numpy array)

        Returns:
            Dictionary containing SHAP values and base value.
        """
        shap_values = self.explainer.shap_values(X)

        # XGBoost sometimes returns a list for multi-class, we want the positive class (fraud)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]

        return {
            "shap_values": shap_values.tolist(),
            "base_value": self.explainer.expected_value.item() if hasattr(self.explainer.expected_value, 'item') else self.explainer.expected_value,
            "feature_names": self.feature_names
        }

class Tier3Explainer(SHAPExplainer):
    """
    Attribution for MHGSL (Tier-3).
    Uses a combination of Integrated Gradients and MHGSL Channel Analysis.
    """
    def __init__(self, model: Any):
        self.model = model

    def explain(self, x_dict: Dict[str, torch.Tensor], edge_index_dict: Dict[Tuple, torch.Tensor]) -> Dict[str, Any]:
        """
        Implements local explanation for MHGSL using Integrated Gradients approximation.

        Args:
            x_dict: Node features dictionary
            edge_index_dict: Edge index dictionary

        Returns:
            Attribution dictionary for the 'claim' node.
        """
        self.model.eval()

        # 1. Baseline for Integrated Gradients (Zero-tensor baseline)
        baseline_x = {node_type: torch.zeros_like(x) for node_type, x in x_dict.items()}

        # 2. Compute gradients along the path from baseline to input
        # We focus on the 'claim' node as the target
        steps = 50
        alphas = torch.linspace(0, 1, steps)
        total_grads = torch.zeros_like(x_dict['claim'])

        # Enable gradients for 'claim' node
        x_dict['claim'].requires_grad = True

        for alpha in alphas:
            # Linear interpolation
            interpolated_x = {
                node_type: (alpha * x + (1 - alpha) * b)
                for node_type, (x, b) in zip(x_dict.items(), baseline_x.items())
            }

            # Forward pass
            prob, _ = self.model(interpolated_x, edge_index_dict)

            # Backprop to get gradients w.r.t 'claim' features
            # we use the first sample in batch
            loss = prob[0]

            # Use torch.autograd.grad to avoid full backprop overhead
            grads = torch.autograd.grad(loss, x_dict['claim'], retain_graph=False)[0]
            total_grads += grads

        # Average gradients and multiply by (input - baseline)
        avg_grads = total_grads / steps
        attribution = avg_grads * (x_dict['claim'] - baseline_x['claim'])

        # 3. Channel Contributions (from core.py)
        # We run one final forward pass to get embeddings
        with torch.no_grad():
            _, embeddings = self.model(x_dict, edge_index_dict)
            # Reuse the contribution logic from MHGSL core (implemented locally here for independence)
            contribs = {}
            total_norm = 0
            for name, emb in embeddings.items():
                norm = torch.norm(emb, p=2, dim=-1).mean().item()
                contribs[name] = norm
                total_norm += norm
            channel_weights = {k: (v / total_norm) * 100 for k, v in contribs.items()}

        return {
            "node_attributions": attribution[0].detach().cpu().numpy().tolist(),
            "channel_contributions": channel_weights,
            "target_node": "claim"
        }
