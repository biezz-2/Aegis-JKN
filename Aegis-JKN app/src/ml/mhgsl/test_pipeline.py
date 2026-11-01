import torch
from torch_geometric.data import HeteroData
from torch_geometric.loader import DataLoader
from src.ml.mhgsl.core import MHGSLModel, compute_channel_contribution

def test_mhgsl_pipeline():
    # 1. Mock Heterogeneous Data (Claim, Provider, Patient)
    data = HeteroData()

    # Node features
    data['claim'].x = torch.randn(10, 16)    # 10 claims, 16 features
    data['provider'].x = torch.randn(3, 8)   # 3 providers, 8 features
    data['patient'].x = torch.randn(5, 8)    # 5 patients, 8 features

    # Edge indices
    data['claim', 'provider'].edge_index = torch.tensor([[0, 1, 2, 3], [0, 0, 1, 2]], dtype=torch.long)
    data['claim', 'patient'].edge_index = torch.tensor([[0, 1, 2, 3], [0, 1, 2, 3]], dtype=torch.long)

    # Create Loader for batching support
    loader = DataLoader([data], batch_size=1, shuffle=False)

    # Initialize Model
    node_types = ['claim', 'provider', 'patient']
    edge_types = [('claim', 'provider'), ('claim', 'patient')]
    model = MHGSLModel(node_types, edge_types)

    # Forward Pass
    for batch in loader:
        x_dict = batch.x_dict
        edge_index_dict = batch.edge_index_dict

        probs, embeddings = model(x_dict, edge_index_dict)
        contribs = compute_channel_contribution(embeddings)

        print(f"Fraud Probabilities shape: {probs.shape}")
        print(f"Channel Contributions: {contribs}")

        assert probs.shape == (10, 1)
        assert "topology" in contribs
        assert "feature" in contribs
        assert "semantic" in contribs
        print("Pipeline check passed.")

if __name__ == "__main__":
    test_mhgsl_pipeline()
