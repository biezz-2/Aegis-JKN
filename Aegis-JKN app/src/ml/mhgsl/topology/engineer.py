import torch
import numpy as np
from typing import List, Dict, Any, Tuple
from torch_geometric.utils import from_networkx
import networkx as nx

class TopologyEngineer:
    """
    ML-02: Topology Engineer.
    Optimizes the Structural Channel for MHGSL.

    Responsibilities:
    - Construct adjacency matrices from FalkorDB results.
    - Multi-hop aggregation (1, 2, 3 hops) with decay.
    - Symmetric Normalized Laplacian normalization.
    - Graph Centrality feature engineering.
    - Sparse matrix optimization using PyTorch Sparse.
    """

    def __init__(self, decay_factor: float = 0.5):
        self.decay_factor = decay_factor

    def construct_adjacency_matrix(self, query_results: List[Dict[str, Any]]) -> torch.Tensor:
        """
        Converts FalkorDB query results into a sparse adjacency matrix.
        Expected query_results: List of {'source': id, 'target': id, 'weight': w}
        """
        # Map node IDs to indices
        nodes = set()
        for edge in query_results:
            nodes.add(edge['source'])
            nodes.add(edge['target'])

        node_map = {node: i for i, node in enumerate(sorted(list(nodes)))}
        num_nodes = len(node_map)

        # Build coordinate format (COO)
        row = []
        col = []
        data = []
        for edge in query_results:
            row.append(node_map[edge['source']])
            col.append(node_map[edge['target']])
            data.append(edge.get('weight', 1.0))

        # Use PyTorch Sparse Tensor
        edge_index = torch.tensor([row, col], dtype=torch.long)
        edge_weight = torch.tensor(data, dtype=torch.float)

        # Create sparse matrix A
        A = torch.sparse_coo_tensor(edge_index, edge_weight, (num_nodes, num_nodes))
        return A.coalesce()

    def compute_multi_hop_aggregation(self, A: torch.Tensor) -> torch.Tensor:
        """
        Multi-hop aggregation: H = A^1 + d*A^2 + d^2*A^3
        Using sparse matrix multiplication.
        """
        # Sparse matrix multiplication is expensive; we use power iterations
        # A is sparse. result will be dense or sparse depending on density.
        # For MHGSL topology dim, we typically want a feature vector per node.

        A_dense = A.to_dense() # Conversion for power iterations if graph is small

        hop1 = A_dense
        hop2 = torch.mm(A_dense, A_dense)
        hop3 = torch.mm(hop2, A_dense)

        aggregated = hop1 + self.decay_factor * hop2 + (self.decay_factor ** 2) * hop3
        return aggregated

    def normalize_laplacian(self, A: torch.Tensor) -> torch.Tensor:
        """
        Symmetric Normalized Laplacian: L = I - D^(-1/2) A D^(-1/2)
        """
        # A is expected to be dense here for normalization stability
        deg = torch.sum(A, dim=1)
        d_inv_sqrt = torch.pow(deg, -0.5)
        d_inv_sqrt[torch.isinf(d_inv_sqrt)] = 0.0
        D_inv_sqrt = torch.diag(d_inv_sqrt)

        # L_norm = I - D^-1/2 A D^-1/2
        I = torch.eye(A.shape[0])
        L_norm = I - torch.mm(torch.mm(D_inv_sqrt, A), D_inv_sqrt)
        return L_norm

    def engineer_centrality_features(self, A: torch.Tensor) -> torch.Tensor:
        """
        Compute Graph Centralities: Degree, Betweenness, PageRank.
        """
        # Convert to NetworkX for complex centralities
        A_np = A.cpu().numpy()
        G = nx.from_numpy_array(A_np, create_using=nx.DiGraph)

        # 1. Degree Centrality
        deg_cent = list(nx.degree_centrality(G).values())

        # 2. Betweenness Centrality
        bet_cent = list(nx.betweenness_centrality(G).values())

        # 3. PageRank
        pagerank = list(nx.pagerank(G).values())

        # Stack into [num_nodes, 3]
        features = np.column_stack([deg_cent, bet_cent, pagerank])
        return torch.tensor(features, dtype=torch.float)

    def get_topology_tensor(self, query_results: List[Dict[str, Any]]) -> torch.Tensor:
        """
        Full Pipeline: Results -> Adjacency -> Aggregation -> Normalization -> Centrality -> Final Tensor
        """
        # 1. Construct A
        A_sparse = self.construct_adjacency_matrix(query_results)

        # 2. Multi-hop aggregation
        A_agg = self.compute_multi_hop_aggregation(A_sparse)

        # 3. Normalization
        L_norm = self.normalize_laplacian(A_agg)

        # 4. Centrality features
        cent_feat = self.engineer_centrality_features(A_agg)

        # 5. Final Topology Embedding: Concatenate Normalized Laplacian (flattened or reduced) and Centralities
        # Here we use the diagonal/mean of Laplacian as a proxy for structural stability
        # or keep the Laplacian if the model expects a full graph matrix.
        # Per Requirements: "Output: Tensor [num_nodes, topology_dim]"

        # We use the row-sums of the Normalized Laplacian + Centralities
        struct_stability = torch.sum(L_norm, dim=1, keepdim=True)
        topology_tensor = torch.cat([struct_stability, cent_feat], dim=-1)

        return topology_tensor

# ponytail: uses dense conversion for power iterations.
# Upgrade to torch.sparse.mm for truly large graphs (>10k nodes).
