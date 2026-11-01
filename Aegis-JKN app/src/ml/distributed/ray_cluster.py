"""
Ray Cluster Setup for Distributed MHGSL Inference.

Handles batch scoring of 300+ claims using Ray for parallel processing.
Integrates with MHGSLModel from src/ml/mhgsl/core.py.

ponytail: Basic Ray setup. Upgrade to Ray Serve for production HTTP serving
and Ray AIR for unified ML pipeline when scaling beyond single-cluster.
"""
import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import ray
from ray import tune
from ray.util.actor_pool import ActorPool

import torch
from torch_geometric.data import HeteroData
from src.ml.mhgsl.core import MHGSLModel, compute_channel_contribution

logger = logging.getLogger(__name__)


@dataclass
class RayConfig:
    """Configuration for Ray cluster."""
    head_node_ip: str = os.getenv("RAY_HEAD_IP", "127.0.0.1")
    head_node_port: int = int(os.getenv("RAY_HEAD_PORT", "6379"))
    num_cpus: int = int(os.getenv("RAY_NUM_CPUS", "4"))
    num_gpus: int = int(os.getenv("RAY_NUM_GPUS", "0"))
    object_store_memory: int = int(os.getenv("RAY_OBJECT_STORE_MEMORY", "200000000"))  # 200MB
    dashboard_port: int = int(os.getenv("RAY_DASHBOARD_PORT", "8265"))
    include_dashboard: bool = True


def init_ray_cluster(config: Optional[RayConfig] = None) -> ray.runtime_context.RuntimeContext:
    """Initialize Ray cluster connection or start local cluster."""
    config = config or RayConfig()

    if ray.is_initialized():
        logger.info("Ray already initialized, shutting down first")
        ray.shutdown()

    if config.head_node_ip == "127.0.0.1" and config.head_node_port == 6379:
        # Start local cluster
        logger.info("Starting local Ray cluster...")
        return ray.init(
            num_cpus=config.num_cpus,
            num_gpus=config.num_gpus,
            object_store_memory=config.object_store_memory,
            include_dashboard=config.include_dashboard,
            dashboard_port=config.dashboard_port,
            ignore_reinit_error=True,
        )
    else:
        # Connect to existing cluster
        logger.info(f"Connecting to Ray cluster at {config.head_node_ip}:{config.head_node_port}")
        return ray.init(
            address=f"{config.head_node_ip}:{config.head_node_port}",
            ignore_reinit_error=True,
        )


@ray.remote(num_cpus=1)
class MHGSLInferenceActor:
    """Ray actor for distributed MHGSL inference."""

    def __init__(self, model_path: Optional[str] = None):
        self.model = self._load_model(model_path)
        self.model.eval()
        logger.info("MHGSLInferenceActor initialized")

    def _load_model(self, model_path: Optional[str]) -> MHGSLModel:
        node_types = ['claim', 'provider', 'patient']
        edge_types = [('claim', 'provider'), ('claim', 'patient')]
        model = MHGSLModel(node_types, edge_types)
        if model_path and os.path.exists(model_path):
            model.load_state_dict(torch.load(model_path, map_location='cpu'))
            logger.info(f"Loaded model weights from {model_path}")
        return model

    def predict(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run inference on a single graph data dict."""
        try:
            x_dict = graph_data.get('x_dict', {})
            edge_index_dict = graph_data.get('edge_index_dict', {})

            # Convert to tensors if needed
            x_dict_tensor = {k: torch.tensor(v) if not isinstance(v, torch.Tensor) else v
                           for k, v in x_dict.items()}
            edge_index_dict_tensor = {k: torch.tensor(v, dtype=torch.long)
                                    if not isinstance(v, torch.Tensor) else v
                                    for k, v in edge_index_dict.items()}

            with torch.no_grad():
                probs, embeddings = self.model(x_dict_tensor, edge_index_dict_tensor)
                contributions = compute_channel_contribution(embeddings)

                results = []
                for i in range(probs.shape[0]):
                    results.append({
                        "claim_index": i,
                        "fraud_probability": float(probs[i].item()),
                        "channel_contributions": contributions,
                        "risk_level": self._get_risk_level(probs[i].item()),
                    })

            return {"status": "success", "results": results}
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return {"status": "error", "error": str(e)}

    def _get_risk_level(self, prob: float) -> str:
        if prob >= 0.8:
            return "CRITICAL"
        elif prob >= 0.6:
            return "HIGH"
        elif prob >= 0.4:
            return "MEDIUM"
        elif prob >= 0.2:
            return "LOW"
        return "MINIMAL"


class DistributedInferenceEngine:
    """Manages distributed batch inference using Ray ActorPool."""

    def __init__(self, num_actors: int = 4, model_path: Optional[str] = None):
        self.num_actors = num_actors
        self.model_path = model_path
        self.actors: List[ray.actor.ActorHandle] = []
        self.pool: Optional[ActorPool] = None

    def start(self):
        """Initialize actor pool."""
        self.actors = [MHGSLInferenceActor.remote(self.model_path)
                      for _ in range(self.num_actors)]
        self.pool = ActorPool(self.actors)
        logger.info(f"Started DistributedInferenceEngine with {self.num_actors} actors")

    def shutdown(self):
        """Clean up actors."""
        for actor in self.actors:
            ray.kill(actor)
        self.actors = []
        self.pool = None
        logger.info("DistributedInferenceEngine shut down")

    def batch_score(self, claims_data: List[Dict[str, Any]], batch_size: int = 50) -> List[Dict[str, Any]]:
        """
        Score multiple claims in parallel.

        Args:
            claims_data: List of graph data dicts for each claim
            batch_size: Number of claims per actor batch

        Returns:
            List of results with fraud probabilities and risk levels
        """
        if not self.pool:
            raise RuntimeError("Engine not started. Call start() first.")

        all_results = []
        for i in range(0, len(claims_data), batch_size):
            batch = claims_data[i:i + batch_size]
            # Map batch to actors
            batch_results = list(self.pool.map(lambda actor, data: actor.predict.remote(data), batch))
            all_results.extend(batch_results)

        return all_results

    def score_async(self, claims_data: List[Dict[str, Any]]) -> List[ray.ObjectRef]:
        """Submit async scoring jobs, returns futures."""
        if not self.pool:
            raise RuntimeError("Engine not started. Call start() first.")

        futures = []
        for data in claims_data:
            # Round-robin assignment to actors
            actor = self.actors[len(futures) % self.num_actors]
            futures.append(actor.predict.remote(data))
        return futures

    def get_results(self, futures: List[ray.ObjectRef]) -> List[Dict[str, Any]]:
        """Collect results from async futures."""
        return ray.get(futures)


def create_sample_claims(num_claims: int = 300) -> List[Dict[str, Any]]:
    """Generate sample claim data for testing."""
    claims = []
    for i in range(num_claims):
        data = HeteroData()
        # Variable number of nodes per claim
        n_providers = torch.randint(1, 4, (1,)).item()
        n_patients = torch.randint(1, 3, (1,)).item()

        data['claim'].x = torch.randn(1, 16)
        data['provider'].x = torch.randn(n_providers, 8)
        data['patient'].x = torch.randn(n_patients, 8)

        # Random edges
        claim_provider_edges = torch.randint(0, n_providers, (2, torch.randint(1, n_providers+1, (1,)).item()))
        claim_patient_edges = torch.randint(0, n_patients, (2, torch.randint(1, n_patients+1, (1,)).item()))

        data['claim', 'provider'].edge_index = claim_provider_edges
        data['claim', 'patient'].edge_index = claim_patient_edges

        claims.append({
            "claim_id": f"CLM-{i:06d}",
            "x_dict": {k: v.tolist() for k, v in data.x_dict.items()},
            "edge_index_dict": {str(k): v.tolist() for k, v in data.edge_index_dict.items()},
        })
    return claims


if __name__ == "__main__":
    # Demo: Run batch scoring on 300 claims
    logging.basicConfig(level=logging.INFO)

    config = RayConfig()
    init_ray_cluster(config)

    engine = DistributedInferenceEngine(num_actors=4)
    engine.start()

    try:
        # Generate test claims
        claims = create_sample_claims(300)
        logger.info(f"Scoring {len(claims)} claims...")

        # Batch score
        results = engine.batch_score(claims, batch_size=50)

        # Summary
        successful = sum(1 for r in results if r.get("status") == "success")
        risk_counts = {}
        for r in results:
            if r.get("status") == "success":
                for res in r["results"]:
                    level = res["risk_level"]
                    risk_counts[level] = risk_counts.get(level, 0) + 1

        logger.info(f"Completed: {successful}/{len(results)} batches successful")
        logger.info(f"Risk distribution: {risk_counts}")

    finally:
        engine.shutdown()
        ray.shutdown()