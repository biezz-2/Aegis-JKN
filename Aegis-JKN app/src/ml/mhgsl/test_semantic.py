import torch
from torch_geometric.data import HeteroData
from torch_geometric.loader import DataLoader
from src.ml.mhgsl.core import MHGSLModel, compute_channel_contribution
from src.ml.mhgsl.semantic.channel import SemanticChannel, SemanticSimilarity

def test_semantic_channel():
    print("Testing Semantic Channel...")

    # 1. Mock medical narratives
    narratives = [
        "Patient presents with acute myocardial infarction, prescribed aspirin and statins.",
        "Chest pain and ST-elevation on ECG, diagnosed as myocardial infarction.",
        "Routine checkup for hypertension, blood pressure controlled with lisinopril.",
        "Patient with chronic kidney disease, dialysis required twice weekly.",
        "Severe respiratory distress, suspected pneumonia, started on IV antibiotics."
    ]

    # Initialize Semantic Channel
    # Using a small semantic_dim for test
    sem_channel = SemanticChannel(semantic_dim=16)

    # Fit reducer on the narratives
    sem_channel.fit_reducer(narratives)

    # Forward pass
    semantic_embeddings = sem_channel(narratives)

    print(f"Semantic Embeddings shape: {semantic_embeddings.shape}")
    assert semantic_embeddings.shape == (5, 16)
    print("Semantic Channel forward pass successful.")

    # 2. Test Semantic Similarity
    print("\nTesting Semantic Similarity...")
    sim_tool = SemanticSimilarity()

    # Compare two similar claims (MI)
    sim_mi = sim_tool.cosine_similarity(
        "Patient presents with acute myocardial infarction",
        "Chest pain and ST-elevation on ECG, diagnosed as MI"
    )

    # Compare two different claims (MI vs Kidney)
    sim_diff = sim_tool.cosine_similarity(
        "Patient presents with acute myocardial infarction",
        "Patient with chronic kidney disease, dialysis required"
    )

    print(f"Similarity (Similar): {sim_mi.item():.4f}")
    print(f"Similarity (Different): {sim_diff.item():.4f}")

    assert sim_mi > sim_diff
    print("Semantic Similarity check passed.")

def test_integrated_mhgsl_with_semantic():
    print("\nTesting Integrated MHGSL with Semantic Channel...")

    # Mock Heterogeneous Data
    data = HeteroData()
    data['claim'].x = torch.randn(5, 16)
    data['provider'].x = torch.randn(3, 8)
    data['patient'].x = torch.randn(5, 8)
    data['claim', 'provider'].edge_index = torch.tensor([[0, 1, 2, 3], [0, 0, 1, 2]], dtype=torch.long)
    data['claim', 'patient'].edge_index = torch.tensor([[0, 1, 2, 3], [0, 1, 2, 3]], dtype=torch.long)

    # Narratives corresponding to the 5 claim nodes
    narratives = [
        "Claim 0: Myocardial Infarction",
        "Claim 1: Heart Attack",
        "Claim 2: Hypertension",
        "Claim 3: Chronic Kidney Disease",
        "Claim 4: Pneumonia"
    ]

    # 1. Setup Semantic Channel
    sem_channel = SemanticChannel(semantic_dim=64)
    sem_channel.fit_reducer(narratives)

    # 2. Extract semantic features for claims
    semantic_feats = sem_channel(narratives)

    # 3. Inject into x_dict for MHGSL
    # We add the semantic embeddings as a new feature channel for 'claim' nodes
    x_dict = data.x_dict
    # Replace or augment 'claim' features with semantic ones
    # In real MHGSL, x_dict['claim'] is the concatenated feature vector [attr, semantic]
    x_dict['claim'] = torch.cat([x_dict['claim'], semantic_feats], dim=-1)

    # 4. Forward pass through MHGSL
    node_types = ['claim', 'provider', 'patient']
    edge_types = [('claim', 'provider'), ('claim', 'patient')]
    model = MHGSLModel(node_types, edge_types, hidden_channels=64)

    # Note: We must update the model's channel dimensions if we changed input feature size
    # Since MHGSLModel uses SAGEConv(-1, hidden_channels), it handles varying input sizes

    probs, embeddings = model(x_dict, data.edge_index_dict)
    contribs = compute_channel_contribution(embeddings)

    print(f"Fraud Probabilities shape: {probs.shape}")
    print(f"Channel Contributions: {contribs}")

    assert probs.shape == (5, 1)
    assert "semantic" in contribs
    print("Integrated MHGSL with Semantic Channel successful.")

if __name__ == "__main__":
    test_semantic_channel()
    test_integrated_mhgsl_with_semantic()
