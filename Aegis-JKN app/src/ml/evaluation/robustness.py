import numpy as np
import torch
from typing import Dict, List, Callable, Optional
from sklearn.metrics import roc_auc_score, average_precision_score

class MaskingRobustnessTest:
    """
    Random feature masking robustness test.
    Masks features at 10%, 20%, 30% rates and measures performance degradation.
    """
    def __init__(
        self,
        mask_ratios: List[float] = [0.1, 0.2, 0.3],
        n_trials: int = 5,
        random_seed: int = 42
    ):
        self.mask_ratios = mask_ratios
        self.n_trials = n_trials
        self.random_seed = random_seed
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)

    def mask_features(self, x: np.ndarray, mask_ratio: float) -> np.ndarray:
        """Randomly mask features by setting them to zero"""
        x_masked = x.copy()
        n_features = x.shape[1]
        n_mask = int(n_features * mask_ratio)

        for i in range(x.shape[0]):
            mask_idx = np.random.choice(n_features, n_mask, replace=False)
            x_masked[i, mask_idx] = 0.0

        return x_masked

    def evaluate(
        self,
        model_predict_fn: Callable,
        X_test: np.ndarray,
        y_test: np.ndarray,
        node_types: Optional[List[str]] = None
    ) -> Dict:
        """
        Evaluate model robustness under feature masking.

        Args:
            model_predict_fn: Function that takes X and returns probabilities
            X_test: Test features
            y_test: Test labels
            node_types: If heterogeneous, list of node types to mask (default: all)

        Returns:
            Dictionary with degradation metrics per mask ratio
        """
        # Baseline performance
        y_prob_baseline = model_predict_fn(X_test)
        baseline_auc = roc_auc_score(y_test, y_prob_baseline)
        baseline_auprc = average_precision_score(y_test, y_prob_baseline)

        results = {
            "baseline": {"roc_auc": baseline_auc, "auprc": baseline_auprc},
            "mask_results": {}
        }

        for ratio in self.mask_ratios:
            ratio_results = {"roc_auc": [], "auprc": []}

            for trial in range(self.n_trials):
                X_masked = self.mask_features(X_test, ratio)
                y_prob = model_predict_fn(X_masked)

                ratio_results["roc_auc"].append(roc_auc_score(y_test, y_prob))
                ratio_results["auprc"].append(average_precision_score(y_test, y_prob))

            # Aggregate across trials
            results["mask_results"][f"mask_{int(ratio*100)}%"] = {
                "roc_auc_mean": np.mean(ratio_results["roc_auc"]),
                "roc_auc_std": np.std(ratio_results["roc_auc"]),
                "auprc_mean": np.mean(ratio_results["auprc"]),
                "auprc_std": np.std(ratio_results["auprc"]),
                "roc_auc_degradation": baseline_auc - np.mean(ratio_results["roc_auc"]),
                "auprc_degradation": baseline_auprc - np.mean(ratio_results["auprc"]),
                "roc_auc_rel_degradation": (baseline_auc - np.mean(ratio_results["roc_auc"])) / baseline_auc * 100,
                "auprc_rel_degradation": (baseline_auprc - np.mean(ratio_results["auprc"])) / baseline_auprc * 100,
            }

        return results

class CamouflageTest:
    """
    Adversarial fraud injection with feature mimicry.
    Injects synthetic fraud samples that mimic legitimate claim patterns
    to test model's ability to detect camouflaged fraud.
    """
    def __init__(
        self,
        n_injected: int = 100,
        mimic_strength: float = 0.8,
        random_seed: int = 42
    ):
        self.n_injected = n_injected
        self.mimic_strength = mimic_strength
        self.random_seed = random_seed
        np.random.seed(random_seed)
        torch.manual_seed(random_seed)

    def generate_camouflaged_fraud(
        self,
        X_legitimate: np.ndarray,
        y_legitimate: np.ndarray,
        n_samples: Optional[int] = None
    ) -> tuple:
        """
        Generate fraud samples that mimic legitimate claim features.
        Uses convex combination: fraud_feature = alpha * legit_feature + (1-alpha) * fraud_pattern
        """
        if n_samples is None:
            n_samples = self.n_injected

        # Sample legitimate claims as templates
        legit_indices = np.where(y_legitimate == 0)[0]
        if len(legit_indices) < n_samples:
            n_samples = len(legit_indices)

        template_indices = np.random.choice(legit_indices, n_samples, replace=True)
        templates = X_legitimate[template_indices]

        # Generate base fraud pattern (random noise around fraud mean)
        fraud_mean = X_legitimate[y_legitimate == 1].mean(axis=0) if np.any(y_legitimate == 1) else np.zeros(X_legitimate.shape[1])
        fraud_pattern = np.random.randn(n_samples, X_legitimate.shape[1]) * 0.5 + fraud_mean

        # Mimic: convex combination
        alpha = self.mimic_strength
        camouflaged = alpha * templates + (1 - alpha) * fraud_pattern

        # Labels: all fraud (1)
        labels = np.ones(n_samples)

        return camouflaged, labels

    def evaluate(
        self,
        model_predict_fn: Callable,
        X_test: np.ndarray,
        y_test: np.ndarray,
        X_train: Optional[np.ndarray] = None,
        y_train: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Evaluate model on camouflaged fraud samples.
        """
        # Generate camouflaged fraud
        X_cam, y_cam = self.generate_camouflaged_fraud(
            X_train if X_train is not None else X_test,
            y_train if y_train is not None else y_test
        )

        # Get predictions on camouflaged samples
        y_prob_cam = model_predict_fn(X_cam)

        # Metrics on camouflaged set
        cam_auc = roc_auc_score(y_cam, y_prob_cam)
        cam_auprc = average_precision_score(y_cam, y_prob_cam)

        # Also test on original test set mixed with camouflaged
        X_mixed = np.vstack([X_test, X_cam])
        y_mixed = np.hstack([y_test, y_cam])
        y_prob_mixed = model_predict_fn(X_mixed)

        mixed_auc = roc_auc_score(y_mixed, y_prob_mixed)
        mixed_auprc = average_precision_score(y_mixed, y_prob_mixed)

        # Detection rate: fraction of camouflaged fraud correctly identified
        threshold = 0.5
        detection_rate = np.mean((y_prob_cam >= threshold).astype(int))

        return {
            "camouflage_only": {
                "roc_auc": cam_auc,
                "auprc": cam_auprc,
                "detection_rate": detection_rate,
                "mean_fraud_prob": np.mean(y_prob_cam),
            },
            "mixed_with_test": {
                "roc_auc": mixed_auc,
                "auprc": mixed_auprc,
            },
            "config": {
                "n_injected": self.n_injected,
                "mimic_strength": self.mimic_strength,
            }
        }