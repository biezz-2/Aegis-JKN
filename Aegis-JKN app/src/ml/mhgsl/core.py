import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv, Linear
from torch_geometric.data import HeteroData, DataLoader

class MHGSLModel(nn.Module):
    """
    Multi-Hop Graph Structure Learning (MHGSL) Core Logic.
    Implements a 3-channel structure (Topology, Feature, Semantic)
    with Heterogeneous Graph Convolutional Network (HGCN) and Late Fusion.
    """
    def __init__(self, node_types, edge_types, hidden_channels=64, out_channels=1):
        super().__init__()

        # 1. Channel-specific Encoders
        # Topology Channel: Focuses on structural connectivity (Graph Topology)
        self.topology_conv = HeteroConv({
            edge_type: SAGEConv(-1, hidden_channels)
            for edge_type in edge_types
        }, aggr='sum')

        # Feature Channel: Focuses on node attributes (Claim/Provider/Patient features)
        self.feature_conv = HeteroConv({
            edge_type: GCNConv(-1, hidden_channels, add_self_loops=False)
            for edge_type in edge_types
        }, aggr='sum')

        # Semantic Channel: Focuses on high-level semantic relations (Fraud Patterns)
        self.semantic_conv = HeteroConv({
            edge_type: SAGEConv(-1, hidden_channels)
            for edge_type in edge_types
        }, aggr='sum')

        # Late Fusion Layer: Aggregates the 3 channels
        # Input: hidden_channels * 3 (Topology, Feature, Semantic)
        self.fusion_layer = nn.Sequential(
            Linear(hidden_channels * 3, hidden_channels),
            nn.ReLU(),
            nn.Dropout(0.2),
            Linear(hidden_channels, out_channels)
            # Sigmoid removed for calibration compatibility
        )

        # Calibration Parameter: Temperature Scaling
        self.temperature = nn.Parameter(torch.ones(1))

        self.hidden_channels = hidden_channels

    def forward(self, x_dict, edge_index_dict, return_logits=False):
        # --- Anti-Leakage Protocol: No target labels used in forward pass ---

        # Topology Channel Pass
        h_topo = self.topology_conv(x_dict, edge_index_dict)

        # Feature Channel Pass
        h_feat = self.feature_conv(x_dict, edge_index_dict)

        # Semantic Channel Pass
        h_sem = self.semantic_conv(x_dict, edge_index_dict)

        # Late Fusion for 'claim' nodes (the target for fraud probability)
        # We only perform fusion on the target node type to optimize compute
        claim_topo = h_topo['claim']
        claim_feat = h_feat['claim']
        claim_sem = h_sem['claim']

        # Concatenate channels: [Batch, hidden*3]
        combined = torch.cat([claim_topo, claim_feat, claim_sem], dim=-1)

        # Final logits (before sigmoid/temperature scaling)
        logits = self.fusion_layer(combined)

        # Temperature Scaling for calibration
        calibrated_logits = logits / self.temperature
        prob = torch.sigmoid(calibrated_logits)

        if return_logits:
            return prob, logits, calibrated_logits, {
                "topology": claim_topo,
                "feature": claim_feat,
                "semantic": claim_sem
            }

        return prob, {
            "topology": claim_topo,
            "feature": claim_feat,
            "semantic": claim_sem
        }

    def calibrate_temperature(self, logits, targets):
        """
        Temperature Scaling calibration (Guo et al., 2017).
        Optimizes temperature parameter on validation set using NLL loss.
        """
        from torch.optim import LBFGS

        self.eval()
        logits = logits.detach()
        targets = targets.detach()

        optimizer = LBFGS([self.temperature], lr=0.01, max_iter=100)

        def eval_loss():
            optimizer.zero_grad()
            loss = F.binary_cross_entropy_with_logits(logits / self.temperature, targets)
            loss.backward()
            return loss

        optimizer.step(eval_loss)
        self.train()

        return self.temperature.item()

    def platt_scaling(self, logits, targets):
        """
        Platt Scaling calibration (Platt, 1999).
        Fits sigmoid: 1 / (1 + exp(A * logits + B))
        """
        from torch.optim import LBFGS

        # Platt scaling parameters
        A = nn.Parameter(torch.ones(1))
        B = nn.Parameter(torch.zeros(1))

        self.eval()
        logits = logits.detach()
        targets = targets.detach()

        optimizer = LBFGS([A, B], lr=0.01, max_iter=100)

        def eval_loss():
            optimizer.zero_grad()
            calibrated = torch.sigmoid(A * logits + B)
            loss = F.binary_cross_entropy(calibrated, targets)
            loss.backward()
            return loss

        optimizer.step(eval_loss)
        self.train()

        return A.item(), B.item()

    def predict_with_uncertainty(self, x_dict, edge_index_dict, n_samples=50):
        """
        Monte Carlo Dropout for uncertainty quantification (Gal & Ghahramani, 2016).
        Returns mean probability and variance across stochastic forward passes.
        """
        self.train()  # Enable dropout during inference

        probs_list = []
        for _ in range(n_samples):
            with torch.no_grad():
                prob, _ = self.forward(x_dict, edge_index_dict)
                probs_list.append(prob)

        probs = torch.stack(probs_list, dim=0)  # [n_samples, N, 1]
        mean_prob = probs.mean(dim=0)
        std_prob = probs.std(dim=0)
        variance = probs.var(dim=0)

        self.eval()  # Restore eval mode

        return {
            "probability": mean_prob,
            "uncertainty_std": std_prob,
            "uncertainty_variance": variance,
            "epistemic_uncertainty": variance  # MC Dropout captures epistemic uncertainty
        }

    def optimize_threshold(self, probabilities, targets, target_metric='f1'):
        """
        Optimize decision threshold for target metric (default: F1-Score).
        Returns optimal threshold and corresponding metric value.
        """
        import numpy as np
        from sklearn.metrics import f1_score, precision_recall_curve

        probs = probabilities.detach().cpu().numpy().flatten()
        targets = targets.detach().cpu().numpy().flatten()

        # Use precision-recall curve for efficient threshold search
        precision, recall, thresholds = precision_recall_curve(targets, probs)

        if target_metric == 'f1':
            f1_scores = 2 * (precision * recall) / (precision + recall + 1e-8)
            optimal_idx = np.argmax(f1_scores)
            optimal_threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else 0.5
            best_score = f1_scores[optimal_idx]
        elif target_metric == 'fbeta':
            # F-beta with beta=2 (recall emphasis for fraud detection)
            beta = 2
            fbeta_scores = (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall + 1e-8)
            optimal_idx = np.argmax(fbeta_scores)
            optimal_threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else 0.5
            best_score = fbeta_scores[optimal_idx]
        else:
            optimal_threshold = 0.5
            best_score = 0.0

        return float(optimal_threshold), float(best_score)

def compute_channel_contribution(channel_embeddings):
    """
    Calculates the contribution of each channel to the final decision.
    Based on the L2 norm of the embeddings post-convolution.
    """
    contribs = {}
    total_norm = 0

    for name, emb in channel_embeddings.items():
        norm = torch.norm(emb, p=2, dim=-1).mean().item()
        contribs[name] = norm
        total_norm += norm

    # Normalize to percentage
    return {k: (v / total_norm) * 100 for k, v in contribs.items()}

# ponytail: Basic HGCN. Upgrade to Attention-based (HGT) if semantic weighting needs to be dynamic.
