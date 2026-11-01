"""
ML-06: XGBoost Architect.
Implementation of Tier-2 Gradient Boosting model for rapid screening (<100ms).
"""
import numpy as np
import pandas as pd
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, f1_score, classification_report
import joblib
import time
import os
from typing import Dict, Any, Tuple, Optional

# Import engineered features from ML-03
from src.ml.mhgsl.features.engineer import Tier2FeatureEngineer

class Tier2RapidScreeningModel:
    """
    Tier-2 XGBoost model for binary classification of fraud.
    Optimized for latency <100ms per inference.
    """
    def __init__(self, params: Optional[Dict[str, Any]] = None):
        # Default hyperparameters optimized for fraud detection (imbalanced data)
        self.params = params or {
            "n_estimators": 500,
            "max_depth": 6,
            "learning_rate": 0.05,
            "subsample": 0.8,
            "colsample_bytree": 0.8,
            "random_state": 42,
            "objective": "binary:logistic",
            "eval_metric": "aucpr",
            "tree_method": "hist",  # Fast histogram-based algorithm
            "n_jobs": -1,
        }
        self.model = XGBClassifier(**self.params)
        self.feature_engineer = Tier2FeatureEngineer()
        self.is_fitted = False
        self.optimal_threshold = 0.5

    def fit(self, df: pd.DataFrame, target_col: str = "is_fraud", early_stopping_rounds: int = 50):
        """
        Train XGBoost model with early stopping.
        """
        # 1. Feature Engineering (ML-03)
        print("Engineering Tier-2 features...")
        df_feat = self.feature_engineer.engineer_features(df)
        feature_cols = self.feature_engineer.get_feature_names(df_feat)

        X = df_feat[feature_cols]
        y = df_feat[target_col]

        # Handle class imbalance using scale_pos_weight
        pos_weight = (y == 0).sum() / (y == 1).sum()
        self.model.set_params(scale_pos_weight=pos_weight)

        # 2. Train/Val Split for Early Stopping
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print(f"Training XGBoost on {len(X_train)} samples...")
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=early_stopping_rounds,
            verbose=False
        )

        # 3. Threshold Optimization (F1-Score)
        probs = self.model.predict_proba(X_val)[:, 1]
        self.optimal_threshold = self._optimize_threshold(y_val, probs)

        self.is_fitted = True
        print(f"Model fitted. Optimal Threshold: {self.optimal_threshold:.4f}")

    def _optimize_threshold(self, y_true, y_prob) -> float:
        """Find threshold that maximizes F1-score."""
        thresholds = np.linspace(0, 1, 100)
        best_f1 = 0
        best_thresh = 0.5

        for t in thresholds:
            preds = (y_prob >= t).astype(int)
            f1 = f1_score(y_true, preds)
            if f1 > best_f1:
                best_f1 = f1
                best_thresh = t
        return best_thresh

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Binary predictions using optimal threshold."""
        probs = self.predict_proba(df)
        return (probs >= self.optimal_threshold).astype(int)

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """Probability of fraud."""
        # Use pre-fitted engineer to transform
        df_feat = self.feature_engineer.engineer_features(df)
        feature_cols = self.feature_engineer.get_feature_names(df_feat)
        X = df_feat[feature_cols]

        return self.model.predict_proba(X)[:, 1]

    def evaluate(self, df: pd.DataFrame, target_col: str = "is_fraud") -> Dict[str, Any]:
        """Comprehensive evaluation of model performance."""
        X_full = df
        y_true = df[target_col]

        y_prob = self.predict_proba(X_full)
        y_pred = self.predict(X_full)

        return {
            "roc_auc": roc_auc_score(y_true, y_prob),
            "auprc": average_precision_score(y_true, y_prob),
            "f1": f1_score(y_true, y_pred),
            "report": classification_report(y_true, y_pred)
        }

    def benchmark_latency(self, df: pd.DataFrame, n_iterations: int = 100) -> Dict[str, float]:
        """Benchmark inference latency to ensure <100ms."""
        latencies = []
        for _ in range(n_iterations):
            start = time.perf_counter()
            self.predict_proba(df)
            latencies.append((time.perf_counter() - start) * 1000)

        return {
            "mean_latency_ms": np.mean(latencies),
            "p95_latency_ms": np.percentile(latencies, 95),
            "p99_latency_ms": np.percentile(latencies, 99),
        }

    def save_for_triton(self, path: str):
        """
        Serialize model for Triton Inference Server.
        Triton's XGBoost backend usually expects a JSON or binary model file.
        """
        os.makedirs(path, exist_ok=True)

        # Save XGBoost model in JSON format (compatible with Triton)
        model_path = os.path.join(path, "model.json")
        self.model.get_booster().save_model(model_path)

        # Save Feature Engineer (as it's required for pre-processing before Triton)
        joblib.dump(self.feature_engineer, os.path.join(path, "feature_engineer.joblib"))

        print(f"Model serialized for Triton at: {path}")

# ponytail: Uses basic XGBClassifier. Upgrade to XGBoost's native DMatrix for extreme latency gains.
