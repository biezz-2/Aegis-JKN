"""
MHGSL (Multi-Channel Heterogeneous Graph Structure Learning)
Faithful Implementation based directly on:
Hong et al., Heliyon 10 (2024) e30045, DOI: 10.1016/j.heliyon.2024.e30045
"Health insurance fraud detection based on multi-channel heterogeneous graph structure learning"

Equations implemented:
- Eq (1): Cosine similarity for Feature Graph G_f = (A_f, X) with top-k KNN (k=4)
- Eq (2): Semantic Meta-path sampling P_PKP, P_PTP, P_PMP and Common Path Sampling A_s = A_PKTMP
- Eq (3), (4), (5): Channel-Specific GCNs (H_t, H_f, H_s) with dimensions 768 -> 256, ReLU, Dropout 0.5
- Eq (6), (7), (8): Shared-Parameter GCNs (W_shared) with mean aggregation Z_CTF, Z_CTS, Z_CFS
- Eq (9), (10), (11), (12): Multi-Graph Attention Mechanism Z_dep + Z_com = Z
- Eq (13), (14): Softmax classification & Cross-Entropy Loss L_cross
- Eq (15), (16): HSIC (Hilbert-Schmidt Independence Criterion) Discrepancy Loss L_similar
- Eq (17), (18): Frobenius Norm Consistency Loss L_common
- Eq (19): Total Loss L = L_cross + alpha * L_similar + beta * L_common (alpha=1e-4, beta=0.5)
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Dict, Any, Optional


def normalize_adjacency(adj: torch.Tensor) -> torch.Tensor:
    """
    Kipf & Welling symmetric normalization:
    \tilde{A} = A + I
    \hat{A} = \tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2}
    """
    device = adj.device
    N = adj.size(0)
    # Add self-loops
    adj_tilde = adj + torch.eye(N, device=device)
    deg = torch.sum(adj_tilde, dim=1)
    deg_inv_sqrt = torch.pow(deg.clamp(min=1e-8), -0.5)
    deg_inv_sqrt[torch.isinf(deg_inv_sqrt)] = 0.0
    D_mat = torch.diag(deg_inv_sqrt)
    return torch.mm(torch.mm(D_mat, adj_tilde), D_mat)


def build_cosine_knn_graph(X: torch.Tensor, k: int = 4) -> torch.Tensor:
    """
    Equation (1): Cosine similarity:
    S_{ij} = (x_i . x_j) / (||x_i|| * ||x_j||)
    Returns binary symmetric adjacency A_f from top-k neighbors.
    """
    N = X.size(0)
    # L2 normalize
    norm_X = F.normalize(X, p=2, dim=1)
    sim_matrix = torch.mm(norm_X, norm_X.t())
    
    # Avoid selecting self in top-k
    sim_matrix.fill_diagonal_(-1.0)
    
    # Pick top-k
    k_val = min(k, N - 1)
    _, topk_indices = torch.topk(sim_matrix, k=k_val, dim=1)
    
    adj_f = torch.zeros(N, N, device=X.device)
    for i in range(N):
        adj_f[i, topk_indices[i]] = 1.0
        
    # Symmetrize
    adj_f = torch.maximum(adj_f, adj_f.t())
    return adj_f


class GCNLayer(nn.Module):
    """
    Graph Convolutional Layer:
    H^{(l)} = ReLU( \hat{A} H^{(l-1)} W^{(l)} )
    """
    def __init__(self, in_features: int, out_features: int, dropout: float = 0.5):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features, bias=True)
        self.dropout = nn.Dropout(dropout)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.linear.weight)
        if self.linear.bias is not None:
            nn.init.zeros_(self.linear.bias)

    def forward(self, x: torch.Tensor, norm_adj: torch.Tensor) -> torch.Tensor:
        x = self.dropout(x)
        # Message passing: A_hat * X
        ax = torch.mm(norm_adj, x)
        out = self.linear(ax)
        return F.relu(out)


class ChannelSpecificGCN(nn.Module):
    """
    Two-layer Channel-Specific GCN:
    input_dim -> 768 -> 256
    """
    def __init__(self, in_dim: int, hidden_dim: int = 768, out_dim: int = 256, dropout: float = 0.5):
        super().__init__()
        self.gc1 = GCNLayer(in_dim, hidden_dim, dropout=dropout)
        self.gc2 = GCNLayer(hidden_dim, out_dim, dropout=dropout)

    def forward(self, x: torch.Tensor, norm_adj: torch.Tensor) -> torch.Tensor:
        h1 = self.gc1(x, norm_adj)
        z = self.gc2(h1, norm_adj)
        return z


class SharedParameterGCN(nn.Module):
    """
    Two-layer Shared-Parameter GCN (W_shared):
    Same weights used across Topology, Feature, and Semantic channels.
    """
    def __init__(self, in_dim: int, hidden_dim: int = 768, out_dim: int = 256, dropout: float = 0.5):
        super().__init__()
        self.gc1 = GCNLayer(in_dim, hidden_dim, dropout=dropout)
        self.gc2 = GCNLayer(hidden_dim, out_dim, dropout=dropout)

    def forward(self, x: torch.Tensor, norm_adj: torch.Tensor) -> torch.Tensor:
        h1 = self.gc1(x, norm_adj)
        z = self.gc2(h1, norm_adj)
        return z


class MultiGraphAttention(nn.Module):
    """
    Equations (9)-(12): Multi-Graph Attention Mechanism:
    Synthesizes Z_dep and Z_com from 6 embeddings into final Z.
    """
    def __init__(self, embed_dim: int = 256):
        super().__init__()
        self.att_linear = nn.Linear(embed_dim, 1, bias=False)
        nn.init.xavier_uniform_(self.att_linear.weight)

    def forward(
        self,
        Z_T: torch.Tensor,
        Z_F: torch.Tensor,
        Z_S: torch.Tensor,
        Z_CTF: torch.Tensor,
        Z_CTS: torch.Tensor,
        Z_CFS: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        # Stack: (6, N, embed_dim)
        stacked = torch.stack([Z_T, Z_F, Z_S, Z_CTF, Z_CTS, Z_CFS], dim=0)
        
        # Calculate attention scores per embedding
        # Shape: (6, N, 1)
        att_scores = self.att_linear(stacked)
        # Softmax over the 6 representations
        att_weights = F.softmax(att_scores, dim=0) # (6, N, 1)

        a_T = att_weights[0]
        a_F = att_weights[1]
        a_S = att_weights[2]
        a_CTF = att_weights[3]
        a_CTS = att_weights[4]
        a_CFS = att_weights[5]

        # Equation (10): Z_dep
        Z_dep = a_T * Z_T + a_F * Z_F + a_S * Z_S
        # Equation (11): Z_com
        Z_com = a_CTF * Z_CTF + a_CTS * Z_CTS + a_CFS * Z_CFS
        # Equation (12): Final Z
        Z = Z_dep + Z_com

        # Average channel weights across nodes for reporting
        mean_weights = att_weights.mean(dim=1).squeeze(-1) # (6,)
        return Z, mean_weights


def hsic_loss(Z1: torch.Tensor, Z2: torch.Tensor) -> torch.Tensor:
    """
    Equation (15)-(16): Hilbert-Schmidt Independence Criterion (HSIC).
    Discrepancy loss between specific and shared embeddings:
    L_T = (n - 1)^{-2} tr( R S_T R S_{CT} )
    where R = I - (1/n) e e^T
    """
    n = Z1.size(0)
    if n <= 1:
        return torch.tensor(0.0, device=Z1.device)

    # Gram matrices: Linear kernel S = Z Z^T
    S1 = torch.mm(Z1, Z1.t())
    S2 = torch.mm(Z2, Z2.t())

    # Centering matrix R = I - (1/n) * J
    H = torch.eye(n, device=Z1.device) - (1.0 / n) * torch.ones(n, n, device=Z1.device)
    
    # tr( H S1 H S2 )
    HK1 = torch.mm(H, S1)
    HK2 = torch.mm(H, S2)
    hsic_val = torch.trace(torch.mm(HK1, HK2)) / ((n - 1) ** 2)
    return hsic_val


def consistency_loss(Z1: torch.Tensor, Z2: torch.Tensor) -> torch.Tensor:
    """
    Equation (17)-(18): Frobenius norm consistency loss:
    L_{CTF} = || F_{CT} - F_{CF} ||_F^2
    where F is L2-normalized embedding.
    """
    F1 = F.normalize(Z1, p=2, dim=1)
    F2 = F.normalize(Z2, p=2, dim=1)
    return torch.norm(F1 - F2, p='fro') ** 2


class MHGSLPaperModel(nn.Module):
    """
    Full MHGSL Model (Hong et al., Heliyon 2024).
    """
    def __init__(
        self,
        in_dim: int,
        hidden_dim: int = 768,
        out_dim: int = 256,
        num_classes: int = 2,
        dropout: float = 0.5,
        alpha: float = 1e-4,
        beta: float = 0.5,
        knn_k: int = 4
    ):
        super().__init__()
        self.alpha = alpha
        self.beta = beta
        self.knn_k = knn_k

        # 1. Channel-Specific GCNs (Equations 3, 4, 5)
        self.gcn_topo = ChannelSpecificGCN(in_dim, hidden_dim, out_dim, dropout)
        self.gcn_feat = ChannelSpecificGCN(in_dim, hidden_dim, out_dim, dropout)
        self.gcn_sem = ChannelSpecificGCN(in_dim, hidden_dim, out_dim, dropout)

        # 2. Shared-Parameter GCN (Equations 6, 7)
        self.gcn_shared = SharedParameterGCN(in_dim, hidden_dim, out_dim, dropout)

        # 3. Multi-Graph Attention (Equations 9-12)
        self.attention = MultiGraphAttention(out_dim)

        # 4. Final Classification Layer (Equation 13)
        self.classifier = nn.Linear(out_dim, num_classes)
        nn.init.xavier_uniform_(self.classifier.weight)
        nn.init.zeros_(self.classifier.bias)

    def forward(
        self,
        X: torch.Tensor,
        adj_topo: torch.Tensor,
        adj_sem: torch.Tensor,
        adj_feat: Optional[torch.Tensor] = None
    ) -> Dict[str, Any]:
        device = X.device

        # If adj_feat not precomputed, compute Equation (1) via Cosine KNN (k=4)
        if adj_feat is None:
            adj_feat = build_cosine_knn_graph(X, k=self.knn_k)

        # Normalize adjacencies: \tilde{D}^{-1/2} \tilde{A} \tilde{D}^{-1/2}
        norm_adj_t = normalize_adjacency(adj_topo)
        norm_adj_f = normalize_adjacency(adj_feat)
        norm_adj_s = normalize_adjacency(adj_sem)

        # 1. Specific GCN Forward: Z_T, Z_F, Z_S
        Z_T = self.gcn_topo(X, norm_adj_t)
        Z_F = self.gcn_feat(X, norm_adj_f)
        Z_S = self.gcn_sem(X, norm_adj_s)

        # 2. Shared-Parameter GCN Forward: Z_CT, Z_CF, Z_CS
        Z_CT = self.gcn_shared(X, norm_adj_t)
        Z_CF = self.gcn_shared(X, norm_adj_f)
        Z_CS = self.gcn_shared(X, norm_adj_s)

        # Equation (8): Pairwise mean representations
        Z_CTF = 0.5 * (Z_CT + Z_CF)
        Z_CTS = 0.5 * (Z_CT + Z_CS)
        Z_CFS = 0.5 * (Z_CF + Z_CS)

        # 3. Attention Fusion: Equations (9)-(12)
        Z_final, att_weights = self.attention(Z_T, Z_F, Z_S, Z_CTF, Z_CTS, Z_CFS)

        # 4. Classification: Equation (13)
        logits = self.classifier(Z_final)
        probs = F.softmax(logits, dim=1)

        return {
            "logits": logits,
            "probs": probs,
            "Z_final": Z_final,
            "att_weights": att_weights,
            "embeddings": {
                "Z_T": Z_T, "Z_F": Z_F, "Z_S": Z_S,
                "Z_CT": Z_CT, "Z_CF": Z_CF, "Z_CS": Z_CS,
                "Z_CTF": Z_CTF, "Z_CTS": Z_CTS, "Z_CFS": Z_CFS
            }
        }

    def compute_loss(
        self,
        output: Dict[str, Any],
        labels: torch.Tensor,
        train_mask: Optional[torch.Tensor] = None
    ) -> Dict[str, torch.Tensor]:
        """
        Total Loss L = L_cross + alpha * L_similar + beta * L_common
        """
        logits = output["logits"]
        emb = output["embeddings"]

        # 1. Cross-Entropy Loss (Equation 14)
        if train_mask is not None:
            l_cross = F.cross_entropy(logits[train_mask], labels[train_mask])
        else:
            l_cross = F.cross_entropy(logits, labels)

        # 2. Disparity Loss via HSIC (Equations 15-16)
        l_sim_t = hsic_loss(emb["Z_T"], emb["Z_CT"])
        l_sim_f = hsic_loss(emb["Z_F"], emb["Z_CF"])
        l_sim_s = hsic_loss(emb["Z_S"], emb["Z_CS"])
        l_similar = l_sim_t + l_sim_f + l_sim_s

        # 3. Consistency Loss via Frobenius Norm (Equations 17-18)
        l_com_tf = consistency_loss(emb["Z_CT"], emb["Z_CF"])
        l_com_ts = consistency_loss(emb["Z_CT"], emb["Z_CS"])
        l_com_fs = consistency_loss(emb["Z_CF"], emb["Z_CS"])
        l_common = l_com_tf + l_com_ts + l_com_fs

        # Equation (19): Combined Loss
        total_loss = l_cross + self.alpha * l_similar + self.beta * l_common

        return {
            "total_loss": total_loss,
            "l_cross": l_cross,
            "l_similar": l_similar,
            "l_common": l_common
        }
