import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score
from typing import Dict, Optional, Tuple, Any
import warnings
warnings.filterwarnings("ignore")

# Try to import XGBoost
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

# Try to import PyTorch Geometric for GCN
try:
    from torch_geometric.nn import GCNConv
    from torch_geometric.data import Data
    HAS_PYG = True
except ImportError:
    HAS_PYG = False


class BaselineModel:
    """Abstract baseline model interface"""
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs):
        raise NotImplementedError

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> Dict:
        y_prob = self.predict_proba(X)
        return {
            "roc_auc": roc_auc_score(y, y_prob),
            "auprc": average_precision_score(y, y_prob),
        }


class LogisticRegressionBaseline(BaselineModel):
    """Logistic Regression baseline with StandardScaler"""
    def __init__(self, max_iter: int = 1000, C: float = 1.0, random_state: int = 42):
        self.model = LogisticRegression(max_iter=max_iter, C=C, random_state=random_state, n_jobs=-1)
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_fitted = True

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]


class XGBoostBaseline(BaselineModel):
    """XGBoost baseline for tabular fraud detection"""
    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: int = 6,
        learning_rate: float = 0.1,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8,
        random_state: int = 42,
        scale_pos_weight: Optional[float] = None
    ):
        if not HAS_XGBOOST:
            raise ImportError("XGBoost not installed. Install with: pip install xgboost")

        self.params = {
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "learning_rate": learning_rate,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "random_state": random_state,
            "n_jobs": -1,
            "eval_metric": "auc",
            "objective": "binary:logistic",
        }
        if scale_pos_weight:
            self.params["scale_pos_weight"] = scale_pos_weight

        self.model = xgb.XGBClassifier(**self.params)
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray, X_val: Optional[np.ndarray] = None, y_val: Optional[np.ndarray] = None, **kwargs):
        eval_set = [(X, y)]
        if X_val is not None and y_val is not None:
            eval_set.append((X_val, y_val))

        self.model.fit(X, y, eval_set=eval_set, verbose=False)
        self.is_fitted = True

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        return self.model.predict_proba(X)[:, 1]


class GCNBaseline(BaselineModel):
    """Graph Convolutional Network baseline for graph-based fraud detection"""
    def __init__(
        self,
        hidden_channels: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2,
        lr: float = 0.01,
        epochs: int = 100,
        device: str = "cpu"
    ):
        if not HAS_PYG:
            raise ImportError("PyTorch Geometric not installed. Install with: pip install torch-geometric")

        self.hidden_channels = hidden_channels
        self.num_layers = num_layers
        self.dropout = dropout
        self.lr = lr
        self.epochs = epochs
        self.device = device
        self.model = None
        self.is_fitted = False

    def _build_model(self, num_features: int):
        """Build GCN model architecture"""
        class GCN(nn.Module):
            def __init__(self, in_channels, hidden_channels, num_layers, dropout):
                super().__init__()
                self.convs = nn.ModuleList()
                self.convs.append(GCNConv(in_channels, hidden_channels))
                for _ in range(num_layers - 2):
                    self.convs.append(GCNConv(hidden_channels, hidden_channels))
                self.convs.append(GCNConv(hidden_channels, 1))
                self.dropout = dropout

            def forward(self, x, edge_index):
                for i, conv in enumerate(self.convs):
                    x = conv(x, edge_index)
                    if i < len(self.convs) - 1:
                        x = F.relu(x)
                        x = F.dropout(x, p=self.dropout, training=self.training)
                return torch.sigmoid(x)

        self.model = GCN(
            in_channels=num_features,
            hidden_channels=self.hidden_channels,
            num_layers=self.num_layers,
            dropout=self.dropout
        ).to(self.device)

    def fit(self, X: np.ndarray, y: np.ndarray, edge_index: np.ndarray, **kwargs):
        """Train GCN on graph data"""
        num_features = X.shape[1]
        self._build_model(num_features)

        # Convert to PyTorch tensors
        x_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).to(self.device)
        edge_index_tensor = torch.LongTensor(edge_index).to(self.device)

        # Create PyG Data object
        data = Data(x=x_tensor, edge_index=edge_index_tensor, y=y_tensor)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        criterion = nn.BCELoss()

        self.model.train()
        for epoch in range(self.epochs):
            optimizer.zero_grad()
            out = self.model(data.x, data.edge_index).squeeze()
            loss = criterion(out, data.y)
            loss.backward()
            optimizer.step()

            if epoch % 20 == 0:
                print(f"GCN Epoch {epoch}, Loss: {loss.item():.4f}")

        self.is_fitted = True

    def predict_proba(self, X: np.ndarray, edge_index: np.ndarray) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")

        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.FloatTensor(X).to(self.device)
            edge_index_tensor = torch.LongTensor(edge_index).to(self.device)
            probs = self.model(x_tensor, edge_index_tensor).cpu().numpy().squeeze()

        return probs


def get_baselines(
    task_type: str = "tabular",
    **kwargs
) -> Dict[str, BaselineModel]:
    """
    Factory function to get all baseline models.

    Args:
        task_type: "tabular" or "graph"
        **kwargs: Additional parameters for specific models

    Returns:
        Dictionary of baseline models
    """
    baselines = {
        "logistic_regression": LogisticRegressionBaseline(**kwargs.get("lr_params", {})),
    }

    if HAS_XGBOOST:
        baselines["xgboost"] = XGBoostBaseline(**kwargs.get("xgb_params", {}))

    if task_type == "graph" and HAS_PYG:
        baselines["gcn"] = GCNBaseline(**kwargs.get("gcn_params", {}))

    return baselines


def run_baseline_comparison(
    baselines: Dict[str, BaselineModel],
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    edge_index: Optional[np.ndarray] = None,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None
) -> Dict:
    """
    Run comparison across all baseline models.
    """
    results = {}

    for name, model in baselines.items():
        print(f"Training {name}...")
        try:
            if name == "gcn" and edge_index is not None:
                model.fit(X_train, y_train, edge_index=edge_index, X_val=X_val, y_val=y_val)
                y_prob = model.predict_proba(X_test, edge_index)
            else:
                model.fit(X_train, y_train, X_val=X_val, y_val=y_val)
                y_prob = model.predict_proba(X_test)

            results[name] = model.evaluate(X_test, y_test)
            results[name]["predictions"] = y_prob
            print(f"  {name}: ROC-AUC={results[name]['roc_auc']:.4f}, AUPRC={results[name]['auprc']:.4f}")
        except Exception as e:
            print(f"  {name} failed: {e}")
            results[name] = {"error": str(e)}

    return results