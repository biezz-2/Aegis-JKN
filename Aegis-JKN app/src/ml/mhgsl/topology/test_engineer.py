import torch
import sys
sys.path.append("N:/HEALTHKATHON/Aegis-JKN app/src")
from ml.mhgsl.topology.engineer import TopologyEngineer

def test_topology_engineer():
    """Test the topology engineer pipeline."""

    # Mock FalkorDB query results
    mock_results = [
        {'source': 'claim_1', 'target': 'provider_1', 'weight': 0.9},
        {'source': 'claim_1', 'target': 'patient_1', 'weight': 0.8},
        {'source': 'claim_2', 'target': 'provider_1', 'weight': 0.7},
        {'source': 'claim_2', 'target': 'patient_2', 'weight': 0.6},
        {'source': 'claim_3', 'target': 'provider_2', 'weight': 0.5},
        {'source': 'claim_3', 'target': 'patient_3', 'weight': 0.4},
        {'source': 'provider_1', 'target': 'claim_4', 'weight': 0.3},
        {'source': 'patient_1', 'target': 'claim_5', 'weight': 0.2},
    ]

    engineer = TopologyEngineer(decay_factor=0.5)

    # Test full pipeline
    topology_tensor = engineer.get_topology_tensor(mock_results)

    print(f"Topology Tensor Shape: {topology_tensor.shape}")
    print(f"Topology Tensor:\n{topology_tensor}")

    # Verify shape [num_nodes, topology_dim]
    # num_nodes = unique nodes in mock_results (claim_1-5, provider_1-2, patient_1-3) = 10
    # topology_dim = 1 (struct stability) + 3 (centralities) = 4
    assert topology_tensor.shape[0] == 10, f"Expected 10 nodes, got {topology_tensor.shape[0]}"
    assert topology_tensor.shape[1] == 4, f"Expected topology_dim=4, got {topology_tensor.shape[1]}"

    # Test individual components
    A = engineer.construct_adjacency_matrix(mock_results)
    print(f"\nSparse Adjacency Shape: {A.shape}")
    print(f"Sparse Adjacency nnz: {A._nnz()}")

    A_agg = engineer.compute_multi_hop_aggregation(A)
    print(f"\nAggregated Adjacency Shape: {A_agg.shape}")

    L_norm = engineer.normalize_laplacian(A_agg)
    print(f"\nNormalized Laplacian Shape: {L_norm.shape}")
    print(f"L_norm diagonal: {torch.diag(L_norm)}")

    cent_feat = engineer.engineer_centrality_features(A_agg)
    print(f"\nCentrality Features Shape: {cent_feat.shape}")
    print(f"Centrality Features:\n{cent_feat}")

    print("\nAll tests passed!")

if __name__ == "__main__":
    test_topology_engineer()