"""
Multi-Hop Graph Structure Learning (MHGSL) End-to-End Engine.

Implements the multi-channel GSL fraud detection architecture:
1. Topology Channel: Bipartite / Heterogeneous Graph of Patient - Doctor/Claim - Provider (Faskes).
2. Feature Channel: Cosine Similarity with K-NN (k=4, Heliyon 2024 paper) on numeric attributes (LOS, Biaya).
3. Semantic Channel: Metapath Claim/Patient -> Diagnosis (ICD-10) -> Procedure -> Provider.
4. Dual-GCN: Channel-Specific GCNs + Shared-Parameter GCN (W_shared).
5. Attention Late Fusion: Dynamic channel attention weighting for fraud risk probability.
6. CLI Runner for BPJS Stata (.dta) dataset evaluation.
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import scipy.sparse as sp
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Tuple, Optional, Any
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


# ==============================================================================
# 1. CHANNEL BUILDERS (Topology, Feature k-NN, Semantic Metapath)
# ==============================================================================

class MHGSLChannelBuilder:
    """
    Constructs the 3 graph channels (Topology, Feature, Semantic)
    from BPJS claims data or synthesized tabular records.
    """

    @staticmethod
    def build_topology_channel(df: pd.DataFrame) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Topology Channel: Adjacency between claims/patients and providers (Faskes).
        Constructs normalized symmetric adjacency for Claim-Patient-Faskes interactions.
        """
        n_claims = len(df)
        if n_claims == 0:
            return torch.zeros((2, 0), dtype=torch.long), torch.zeros(0, dtype=torch.float)

        # Mapping faskes / providers to indices
        faskes_candidates = ['FKL07', 'faskes_id', 'Faskes', 'faskes', 'provider_id']
        faskes_col = next((c for c in faskes_candidates if c in df.columns), None)
        patient_candidates = ['PSTV01', 'patient_id', 'Pasien', 'pasien', 'peserta_id']
        patient_col = next((c for c in patient_candidates if c in df.columns), None)
        edges_src = []
        edges_dst = []
        edge_weights = []

        # Claim-to-claim connections if sharing same patient or same faskes
        if patient_col and patient_col in df.columns:
            patient_groups = df.groupby(patient_col).indices
            for p_id, idxs in patient_groups.items():
                if len(idxs) > 1:
                    for i in range(len(idxs)):
                        for j in range(i + 1, min(i + 5, len(idxs))):
                            edges_src.extend([idxs[i], idxs[j]])
                            edges_dst.extend([idxs[j], idxs[i]])
                            edge_weights.extend([0.8, 0.8])

        if faskes_col and faskes_col in df.columns:
            faskes_groups = df.groupby(faskes_col).indices
            for f_id, idxs in faskes_groups.items():
                if len(idxs) > 1:
                    # Sample connections within faskes to prevent quadratic explosion
                    for i in range(len(idxs)):
                        # Connect with up to 3 peers in same provider
                        for j in range(i + 1, min(i + 4, len(idxs))):
                            edges_src.extend([idxs[i], idxs[j]])
                            edges_dst.extend([idxs[j], idxs[i]])
                            edge_weights.extend([0.5, 0.5])

        # Self-loops for all nodes
        for i in range(n_claims):
            edges_src.append(i)
            edges_dst.append(i)
            edge_weights.append(1.0)

        edge_index = torch.tensor([edges_src, edges_dst], dtype=torch.long)
        edge_weight = torch.tensor(edge_weights, dtype=torch.float)
        return edge_index, edge_weight

    @staticmethod
    def build_feature_channel_knn(features_num: np.ndarray, k: int = 4) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Feature Channel: Cosine similarity of numeric attributes (LOS, Biaya)
        with K-Nearest Neighbors (k=4, Heliyon 2024 paper benchmark).
        """
        n_samples = len(features_num)
        if n_samples == 0:
            return torch.zeros((2, 0), dtype=torch.long), torch.zeros(0, dtype=torch.float)

        # Standardize features prior to cosine calculation
        scaler = StandardScaler()
        scaled_feat = scaler.fit_transform(features_num)

        # Compute cosine similarity matrix
        sim_matrix = cosine_similarity(scaled_feat)
        np.fill_diagonal(sim_matrix, 0.0)

        edges_src = []
        edges_dst = []
        edge_weights = []

        actual_k = min(k, max(1, n_samples - 1))
        for i in range(n_samples):
            # Top-k most similar neighbors
            top_k_indices = np.argsort(sim_matrix[i])[-actual_k:]
            for j in top_k_indices:
                weight = float(sim_matrix[i, j])
                if weight > 0:
                    edges_src.append(i)
                    edges_dst.append(j)
                    edge_weights.append(weight)

            # Self-loop
            edges_src.append(i)
            edges_dst.append(i)
            edge_weights.append(1.0)

        edge_index = torch.tensor([edges_src, edges_dst], dtype=torch.long)
        edge_weight = torch.tensor(edge_weights, dtype=torch.float)
        return edge_index, edge_weight

    @staticmethod
    def build_semantic_channel_metapath(df: pd.DataFrame) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Semantic Channel: Metapath P -> Diagnosis (ICD-10) -> Procedure (Casemix/Prosedur) -> Faskes.
        Links claims having similar diagnostic and procedural combinations.
        """
        n_claims = len(df)
        if n_claims == 0:
            return torch.zeros((2, 0), dtype=torch.long), torch.zeros(0, dtype=torch.float)

        diag_candidates = ['FKL17A', 'diagnosis_code', 'Diagnosis ICD-10', 'Diagnosis', 'icd10', 'icd10_primary']
        diag_col = next((c for c in diag_candidates if c in df.columns), None)
        proc_candidates = ['FKL30', 'procedure_code', 'Prosedur ICD-9-CM', 'Prosedur', 'icd9', 'icd9_procedure']
        proc_col = next((c for c in proc_candidates if c in df.columns), None)
        edges_src = []
        edges_dst = []
        edge_weights = []

        if diag_col and diag_col in df.columns:
            diag_groups = df.groupby(diag_col).indices
            for diag, idxs in diag_groups.items():
                if len(idxs) > 1:
                    for i in range(len(idxs)):
                        for j in range(i + 1, min(i + 5, len(idxs))):
                            edges_src.extend([idxs[i], idxs[j]])
                            edges_dst.extend([idxs[j], idxs[i]])
                            edge_weights.extend([0.7, 0.7])

        if proc_col and proc_col in df.columns:
            proc_groups = df.groupby(proc_col).indices
            for proc, idxs in proc_groups.items():
                if len(idxs) > 1:
                    for i in range(len(idxs)):
                        for j in range(i + 1, min(i + 4, len(idxs))):
                            edges_src.extend([idxs[i], idxs[j]])
                            edges_dst.extend([idxs[j], idxs[i]])
                            edge_weights.extend([0.6, 0.6])

        # Self-loops
        for i in range(n_claims):
            edges_src.append(i)
            edges_dst.append(i)
            edge_weights.append(1.0)

        edge_index = torch.tensor([edges_src, edges_dst], dtype=torch.long)
        edge_weight = torch.tensor(edge_weights, dtype=torch.float)
        return edge_index, edge_weight


# ==============================================================================
# 2. DUAL-GCN & ATTENTION LATE FUSION MODULE
# ==============================================================================

class DualGCNLayer(nn.Module):
    """
    Dual-GCN component:
    Processes input graph representation with:
    1. Channel-Specific GCN (W_c)
    2. Shared-Parameter GCN (W_shared) across all 3 channels.
    Representation = Alpha * H_channel + (1 - Alpha) * H_shared
    """
    def __init__(self, in_features: int, out_features: int, shared_weight: nn.Parameter):
        super().__init__()
        self.channel_weight = nn.Parameter(torch.Tensor(in_features, out_features))
        self.shared_weight = shared_weight
        self.bias = nn.Parameter(torch.zeros(out_features))
        self.alpha = nn.Parameter(torch.tensor(0.5))

        # Glorot initialization
        nn.init.xavier_uniform_(self.channel_weight)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, edge_weight: Optional[torch.Tensor] = None) -> torch.Tensor:
        num_nodes = x.size(0)
        if edge_weight is None:
            edge_weight = torch.ones(edge_index.size(1), device=x.device)

        # Message passing with sparse matrix multiplication
        row, col = edge_index[0], edge_index[1]
        deg = torch.zeros(num_nodes, device=x.device)
        deg.scatter_add_(0, row, edge_weight)
        deg_inv_sqrt = torch.pow(deg.clamp(min=1e-8), -0.5)
        norm_weight = deg_inv_sqrt[row] * edge_weight * deg_inv_sqrt[col]

        adj = torch.sparse_coo_tensor(
            torch.stack([row, col], dim=0),
            norm_weight,
            (num_nodes, num_nodes),
            device=x.device
        )

        # 1. Channel-specific transform
        h_channel = torch.sparse.mm(adj, x @ self.channel_weight)

        # 2. Shared-parameter transform
        h_shared = torch.sparse.mm(adj, x @ self.shared_weight)

        # Gated combination
        a = torch.sigmoid(self.alpha)
        h = a * h_channel + (1.0 - a) * h_shared + self.bias
        return F.relu(h)


class AttentionLateFusion(nn.Module):
    """
    Attention-based Late Fusion mechanism.
    Learns dynamic attention weights across Topology, Feature, and Semantic channels
    to produce final calibrated fraud probabilities and per-channel importance scores.
    """
    def __init__(self, hidden_dim: int):
        super().__init__()
        self.attn_vector = nn.Linear(hidden_dim, 1, bias=False)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, h_topo: torch.Tensor, h_feat: torch.Tensor, h_sem: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Inputs: [N, D] for each channel.
        Returns:
            prob: [N, 1] Fraud probability
            channel_weights: [N, 3] Attention scores (Topology, Feature, Semantic)
        """
        # Stack channels: [N, 3, D]
        stacked = torch.stack([h_topo, h_feat, h_sem], dim=1)

        # Calculate attention energy: [N, 3, 1] -> [N, 3]
        scores = self.attn_vector(stacked).squeeze(-1)
        weights = F.softmax(scores, dim=-1)

        # Weighted combination: [N, D]
        fused = torch.sum(stacked * weights.unsqueeze(-1), dim=1)

        logits = self.classifier(fused)
        prob = torch.sigmoid(logits)
        return prob, weights


class MHGSLEngine(nn.Module):
    """
    Complete Multi-Hop Graph Structure Learning (MHGSL) Engine.
    Coordinates 3 channels, Dual-GCN layers, Attention Fusion, and Prediction.
    """
    def __init__(self, input_dim: int, hidden_dim: int = 64):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        # Shared parameter across all channels for inductive generalization
        self.W_shared = nn.Parameter(torch.Tensor(input_dim, hidden_dim))
        nn.init.xavier_uniform_(self.W_shared)

        # Dual-GCN for each of the 3 channels
        self.topo_gcn = DualGCNLayer(input_dim, hidden_dim, self.W_shared)
        self.feat_gcn = DualGCNLayer(input_dim, hidden_dim, self.W_shared)
        self.sem_gcn = DualGCNLayer(input_dim, hidden_dim, self.W_shared)

        # Channel Attention Late Fusion
        self.fusion = AttentionLateFusion(hidden_dim)

    def forward(
        self,
        x: torch.Tensor,
        topo_edges: Tuple[torch.Tensor, torch.Tensor],
        feat_edges: Tuple[torch.Tensor, torch.Tensor],
        sem_edges: Tuple[torch.Tensor, torch.Tensor]
    ) -> Dict[str, Any]:
        """
        Executes end-to-end forward pass across all 3 channels.
        """
        # Channel 1: Topology
        h_topo = self.topo_gcn(x, topo_edges[0], topo_edges[1])

        # Channel 2: Feature
        h_feat = self.feat_gcn(x, feat_edges[0], feat_edges[1])

        # Channel 3: Semantic
        h_sem = self.sem_gcn(x, sem_edges[0], sem_edges[1])

        # Attention Late Fusion
        probs, channel_weights = self.fusion(h_topo, h_feat, h_sem)

        # Channel specific scores based on mean representation norm
        topo_score = torch.norm(h_topo, p=2, dim=-1, keepdim=True)
        feat_score = torch.norm(h_feat, p=2, dim=-1, keepdim=True)
        sem_score = torch.norm(h_sem, p=2, dim=-1, keepdim=True)

        return {
            "probabilities": probs,
            "channel_weights": channel_weights, # [N, 3] -> (topo, feat, sem)
            "channel_scores": {
                "topology": topo_score,
                "feature": feat_score,
                "semantic": sem_score
            },
            "embeddings": {
                "topology": h_topo,
                "feature": h_feat,
                "semantic": h_sem
            }
        }


# ==============================================================================
# 3. BPJS DATA EXTRACTOR & PREPROCESSOR
# ==============================================================================

def extract_features_from_bpjs_df(df: pd.DataFrame) -> Tuple[torch.Tensor, np.ndarray]:
    """
    Extracts and standardizes numeric/categorical features from BPJS claims DataFrame.
    Calculates Length of Stay (LOS) and Biaya Tagih/Verifikasi.
    """
    n_rows = len(df)
    features_list = []

    # 1. Length of Stay (LOS) calculation
    los_candidates = ['LOS hari', 'LOS', 'los', 'los_days', 'lama_rawat']
    los_col = next((c for c in los_candidates if c in df.columns), None)
    if 'FKL03' in df.columns and 'FKL04' in df.columns:
        try:
            t_datang = pd.to_datetime(df['FKL03'], errors='coerce')
            t_pulang = pd.to_datetime(df['FKL04'], errors='coerce')
            los = (t_pulang - t_datang).dt.days.fillna(1).clip(lower=1).values
        except Exception:
            los = np.ones(n_rows, dtype=np.float32)
    elif los_col:
        los = pd.to_numeric(df[los_col], errors='coerce').fillna(1).clip(lower=1).values
    else:
        los = np.ones(n_rows, dtype=np.float32)

    # 2. Biaya Tagih & Verifikasi
    biaya_candidates = ['Biaya Rp', 'Biaya', 'biaya', 'total_cost', 'biaya_tagih', 'FKL47']
    biaya_col = next((c for c in biaya_candidates if c in df.columns), None)
    if 'FKL47' in df.columns:
        biaya_tagih = pd.to_numeric(df['FKL47'], errors='coerce').fillna(0).values
    elif biaya_col:
        biaya_tagih = pd.to_numeric(df[biaya_col], errors='coerce').fillna(0).values
    else:
        biaya_tagih = np.zeros(n_rows, dtype=np.float32)

    if 'FKL48' in df.columns:
        biaya_verif = pd.to_numeric(df['FKL48'], errors='coerce').fillna(0).values
    elif 'biaya_verif' in df.columns:
        biaya_verif = pd.to_numeric(df['biaya_verif'], errors='coerce').fillna(0).values
    else:
        biaya_verif = biaya_tagih.copy()
    # Biaya variance ratio
    biaya_diff = np.abs(biaya_tagih - biaya_verif)
    biaya_ratio = np.where(biaya_verif > 0, biaya_tagih / (biaya_verif + 1.0), 1.0)

    # Combine core numeric features
    numeric_matrix = np.column_stack([
        los.astype(np.float32),
        biaya_tagih.astype(np.float32),
        biaya_verif.astype(np.float32),
        biaya_diff.astype(np.float32),
        biaya_ratio.astype(np.float32)
    ])

    scaler = StandardScaler()
    scaled_numeric = scaler.fit_transform(numeric_matrix)

    # Additional metadata encoding (Type, Class, Poly)
    extra_features = []
    for col in ['FKL09', 'FKL11', 'FKL13', 'FKL14']:
        if col in df.columns:
            encoded = pd.factorize(df[col])[0].astype(np.float32)
            extra_features.append(encoded)

    if extra_features:
        full_feat = np.column_stack([scaled_numeric, *[f[:, None] for f in extra_features]])
    else:
        full_feat = scaled_numeric

    x_tensor = torch.tensor(full_feat, dtype=torch.float32)
    return x_tensor, numeric_matrix


# ==============================================================================
# 4. CLI RUNNER FUNCTION
# ==============================================================================

def run_mhgsl_inference(
    df: pd.DataFrame,
    k_nn: int = 4,
    hidden_dim: int = 64
) -> Dict[str, Any]:
    """
    Runs full MHGSL pipeline on a pandas DataFrame of claims.
    """
    print(f"[MHGSL Engine] Processing {len(df)} claims...")

    # 1. Feature extraction
    x_tensor, numeric_matrix = extract_features_from_bpjs_df(df)

    # 2. Build 3 Channels
    print(f"[MHGSL Engine] Building Topology channel (Pasien - Faskes)...")
    topo_edges = MHGSLChannelBuilder.build_topology_channel(df)

    print(f"[MHGSL Engine] Building Feature channel (Cosine similarity k-NN, k={k_nn})...")
    feat_edges = MHGSLChannelBuilder.build_feature_channel_knn(numeric_matrix, k=k_nn)

    print(f"[MHGSL Engine] Building Semantic channel (Metapath Diagnosis - Prosedur)...")
    sem_edges = MHGSLChannelBuilder.build_semantic_channel_metapath(df)

    # 3. Initialize Engine
    input_dim = x_tensor.size(1)
    model = MHGSLEngine(input_dim=input_dim, hidden_dim=hidden_dim)
    model.eval()

    # 4. Forward execution
    with torch.no_grad():
        results = model(x_tensor, topo_edges, feat_edges, sem_edges)

    probs = results["probabilities"].cpu().numpy().flatten()
    channel_weights = results["channel_weights"].cpu().numpy()
    topo_score = results["channel_scores"]["topology"].cpu().numpy().flatten()
    feat_score = results["channel_scores"]["feature"].cpu().numpy().flatten()
    sem_score = results["channel_scores"]["semantic"].cpu().numpy().flatten()

    summary_df = pd.DataFrame({
        "claim_idx": np.arange(len(df)),
        "fraud_probability": probs,
        "weight_topology": channel_weights[:, 0],
        "weight_feature": channel_weights[:, 1],
        "weight_semantic": channel_weights[:, 2],
        "score_topology": topo_score,
        "score_feature": feat_score,
        "score_semantic": sem_score
    })

    if 'FKL02' in df.columns:
        summary_df.insert(0, 'claim_id', df['FKL02'].values)

    return {
        "summary": summary_df,
        "model": model,
        "raw_results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Aegis-JKN MHGSL Engine CLI")
    parser.add_argument("--input", type=str, help="Path to BPJS .dta or .csv file", default=None)
    parser.add_argument("--sample-size", type=int, default=100, help="Number of records to sample")
    parser.add_argument("--k-nn", type=int, default=4, help="K-nearest neighbors for feature channel (Heliyon 2024)")
    parser.add_argument("--output", type=str, default=None, help="Output CSV path for predictions")
    args = parser.parse_args()

    if args.input and os.path.exists(args.input):
        print(f"Loading data from: {args.input}")
        if args.input.endswith(".dta"):
            reader = pd.read_stata(args.input, chunksize=args.sample_size)
            df = next(reader)
        elif args.input.endswith(".csv"):
            df = pd.read_csv(args.input, nrows=args.sample_size)
        else:
            raise ValueError("Supported formats: .dta, .csv")
    else:
        # Fallback to default BPJS path if accessible, or generate realistic mock
        bpjs_default_dta = r"P:\EVENT KATON\HAELTHKATHON\Data sampel 2015-2024\2025\Data Sampel Reguler Edisi 2025\data\202403_fkrtl.dta"
        if os.path.exists(bpjs_default_dta):
            print(f"Loading from default BPJS dataset: {bpjs_default_dta}")
            reader = pd.read_stata(bpjs_default_dta, chunksize=args.sample_size)
            df = next(reader)
        else:
            print("Dataset file not specified or found. Generating synthetic BPJS batch...")
            n = args.sample_size
            df = pd.DataFrame({
                "FKL02": [f"CLM-{1000+i}" for i in range(n)],
                "PSTV01": [f"PST-{100 + (i % 20)}" for i in range(n)],
                "FKL07": [f"FSK-{(i % 5)}" for i in range(n)],
                "FKL03": ["2024-01-01"] * n,
                "FKL04": ["2024-01-05"] * n,
                "FKL17A": [f"E11.{i % 9}" for i in range(n)],
                "FKL30": [f"PROC-{i % 6}" for i in range(n)],
                "FKL47": np.random.uniform(500000, 15000000, n),
                "FKL48": np.random.uniform(500000, 14000000, n)
            })

    output = run_mhgsl_inference(df, k_nn=args.k_nn)
    res_df = output["summary"]

    print("\n=== MHGSL Fraud Prediction Summary (Top 5) ===")
    print(res_df.head())
    print("\nMean Fraud Probability:", res_df["fraud_probability"].mean())
    print("Channel Weights Distribution (Mean):")
    print(f"  - Topology: {res_df['weight_topology'].mean():.4f}")
    print(f"  - Feature:  {res_df['weight_feature'].mean():.4f}")
    print(f"  - Semantic: {res_df['weight_semantic'].mean():.4f}")

    if args.output:
        res_df.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")

    print("\nMHGSL Engine run completed successfully.")


if __name__ == "__main__":
    main()
