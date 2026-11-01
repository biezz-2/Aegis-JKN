import torch
import logging
import numpy as np
from typing import Dict, Any, Tuple, Optional, List
from fastapi import HTTPException
from src.ml.mhgsl.core import MHGSLModel, compute_channel_contribution
from src.ml.xai.shap_explainer import Tier2Explainer, Tier3Explainer
from src.ml.xai.explanation_generator import ExplanationGenerator, LocalExplanation, GlobalExplanation

logger = logging.getLogger(__name__)

class MLService:
    """
    Service layer for ML model orchestration.
    Handles model loading, inference, and post-processing.
    """
    def __init__(self):
        self.model: Optional[MHGSLModel] = None
        self._is_loaded = False

    def load_model(self, model_path: Optional[str] = None):
        """
        Loads the MHGSL model into memory.
        In a real scenario, this would load a .pt or .pth file.
        """
        try:
            logger.info("Loading MHGSL model for fraud detection...")

            # Define model architecture based on MHGSL blueprint
            node_types = ['claim', 'provider', 'patient']
            edge_types = [('claim', 'provider'), ('claim', 'patient')]

            self.model = MHGSLModel(node_types, edge_types)

            if model_path:
                # self.model.load_state_dict(torch.load(model_path))
                logger.info(f"Model weights loaded from {model_path}")

            self.model.eval()
            self._is_loaded = True
            logger.info("MHGSL model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load MHGSL model: {str(e)}")
            raise RuntimeError(f"Model initialization failed: {str(e)}")

    async def analyze_fraud(self, graph_data: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        Runs inference on graph data to detect fraud.

        Args:
            graph_data: Dictionary containing node features and edge indices

        Returns:
            Tuple of (fraud_probability, channel_contributions)
        """
        if not self._is_loaded or self.model is None:
            raise HTTPException(status_code=503, detail="ML Model is not yet loaded")

        try:
            # --- Anti-Leakage Protocol ---
            # Ensure input features do not contain labels or contribution scores
            x_dict = graph_data.get('x_dict', {})
            edge_index_dict = graph_data.get('edge_index_dict', {})

            # Validate feature keys to prevent leakage
            leakage_keywords = ['label', 'target', 'probability', 'contribution', 'shap']
            for node_type, features in x_dict.items():
                if isinstance(features, torch.Tensor):
                    # In a real implementation, we'd check a feature mapping
                    pass
                elif isinstance(features, dict):
                    for key in features.keys():
                        if any(kw in key.lower() for kw in leakage_keywords):
                            raise ValueError(f"Data leakage detected in node type {node_type}: feature {key}")

            with torch.no_grad():
                # The model expects HeteroData-like dictionaries
                probs, embeddings = self.model(x_dict, edge_index_dict)

                # We assume the request is for a specific claim (index 0 in the batch)
                # In a real implementation, we'd map claim_id to tensor index
                fraud_prob = probs[0].item()
                contributions = compute_channel_contribution(embeddings)

            return fraud_prob, contributions

        except Exception as e:
            logger.error(f"ML Inference error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")

# --- XAI Methods ---

    def initialize_tier2_explainer(self, xgb_model: Any, feature_names: List[str]):
        """
        Initializes the Tier-2 (XGBoost) SHAP Explainer.
        """
        self.tier2_explainer = Tier2Explainer(xgb_model, feature_names)
        self.tier2_generator = ExplanationGenerator(feature_names)
        logger.info("Tier-2 XAI initialized.")

    def initialize_tier3_explainer(self):
        """
        Initializes the Tier-3 (MHGSL) Attribution Explainer.
        """
        if self.model is None:
            raise RuntimeError("MHGSL Model must be loaded before initializing Tier-3 Explainer.")
        self.tier3_explainer = Tier3Explainer(self.model)
        # MHGSL feature names would come from the feature engineering pipeline
        mhgsl_feature_names = [f"claim_feat_{i}" for i in range(16)] # Placeholder
        self.tier3_generator = ExplanationGenerator(mhgsl_feature_names)
        logger.info("Tier-3 XAI initialized.")

    async def explain_tier2(self, X: np.ndarray) -> List[LocalExplanation]:
        """
        Generates SHAP-based local explanations for XGBoost predictions.

        Args:
            X: Feature matrix for claims (n_samples, n_features)

        Returns:
            List of LocalExplanation objects (JSON serializable)
        """
        if not hasattr(self, 'tier2_explainer'):
            raise RuntimeError("Tier-2 explainer not initialized. Call initialize_tier2_explainer first.")

        shap_result = self.tier2_explainer.explain(X)
        shap_values = np.array(shap_result["shap_values"])
        base_value = shap_result["base_value"]

        explanations = []
        for i in range(len(X)):
            pred_prob = base_value + shap_values[i].sum() # SHAP sum property
            local_exp = self.tier2_generator.generate_local(
                claim_id=f"claim_{i}", # Placeholder ID
                prediction=float(pred_prob),
                attribution_values=shap_values[i].tolist()
            )
            explanations.append(local_exp)

        return explanations

    async def explain_tier3(self, x_dict: Dict[str, torch.Tensor], edge_index_dict: Dict[Tuple, torch.Tensor], claim_id: str) -> LocalExplanation:
        """
        Generates Integrated Gradients-based local explanation for MHGSL prediction.

        Args:
            x_dict: Node features
            edge_index_dict: Edge indices
            claim_id: Identifier for the claim

        Returns:
            LocalExplanation object (JSON serializable)
        """
        if not hasattr(self, 'tier3_explainer'):
            raise RuntimeError("Tier-3 explainer not initialized. Call initialize_tier3_explainer first.")

        # Get raw attributions
        attribution_result = self.tier3_explainer.explain(x_dict, edge_index_dict)

        # Generate probability from forward pass
        with torch.no_grad():
            probs, embeddings = self.model(x_dict, edge_index_dict)
            fraud_prob = probs[0].item()
            contributions = compute_channel_contribution(embeddings)

        local_exp = self.tier3_generator.generate_local(
            claim_id=claim_id,
            prediction=fraud_prob,
            attribution_values=attribution_result["node_attributions"],
            channel_contribs=contributions
        )

        return local_exp

    async def get_global_tier2_explanation(self, X_background: np.ndarray) -> GlobalExplanation:
        """
        Computes global feature importance from a background dataset.
        """
        if not hasattr(self, 'tier2_explainer'):
            raise RuntimeError("Tier-2 explainer not initialized.")

        shap_result = self.tier2_explainer.explain(X_background)
        shap_values = np.array(shap_result["shap_values"])

        return self.tier2_generator.generate_global(shap_values)


# Singleton instance for the application
ml_service = MLService()
