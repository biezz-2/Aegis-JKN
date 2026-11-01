"""
Batch Inference Script for Daily Fraud Scoring Pipeline.

This script is executed by the Argo Workflow's model-inference step.
It uses Ray for distributed scoring of 300+ claims.
"""
import argparse
import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any

import torch
from torch_geometric.data import HeteroData

from src.ml.distributed.ray_cluster import (
    init_ray_cluster, RayConfig, DistributedInferenceEngine
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_features(features_path: str) -> List[Dict[str, Any]]:
    """Load features from the feature extraction output."""
    path = Path(features_path)
    if path.is_dir():
        # Load all JSON files in directory
        features = []
        for f in path.glob("*.json"):
            with open(f) as fp:
                features.append(json.load(fp))
        return features
    else:
        with open(path) as f:
            return json.load(f)


def save_predictions(predictions: List[Dict[str, Any]], output_path: str, metadata: Dict[str, Any]):
    """Save predictions to output directory."""
    out_path = Path(output_path)
    out_path.mkdir(parents=True, exist_ok=True)

    # Save individual predictions
    for pred in predictions:
        claim_id = pred.get("claim_id", "unknown")
        with open(out_path / f"{claim_id}.json", "w") as f:
            json.dump(pred, f)

    # Save metadata
    with open(out_path / "metadata.json", "w") as f:
        json.dump(metadata, f)

    logger.info(f"Saved {len(predictions)} predictions to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Batch MHGSL Inference")
    parser.add_argument("--features", required=True, help="Path to features input")
    parser.add_argument("--output", required=True, help="Output directory for predictions")
    parser.add_argument("--model-version", default="latest", help="Model version to use")
    parser.add_argument("--num-actors", type=int, default=4, help="Number of Ray actors")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size per actor")
    args = parser.parse_args()

    # Initialize Ray
    config = RayConfig()
    init_ray_cluster(config)

    try:
        # Load features
        logger.info(f"Loading features from {args.features}")
        claims_data = load_features(args.features)
        logger.info(f"Loaded {len(claims_data)} claims for scoring")

        # Start inference engine
        model_path = f"/models/mhgsl_{args.model_version}.pt"
        engine = DistributedInferenceEngine(
            num_actors=args.num_actors,
            model_path=model_path if os.path.exists(model_path) else None
        )
        engine.start()

        try:
            # Run batch inference
            logger.info(f"Starting batch inference with {args.num_actors} actors...")
            results = engine.batch_score(claims_data, batch_size=args.batch_size)

            # Process results
            predictions = []
            for i, result in enumerate(results):
                if result.get("status") == "success":
                    for res in result["results"]:
                        predictions.append({
                            "claim_id": claims_data[i].get("claim_id", f"CLM-{i:06d}"),
                            "fraud_probability": res["fraud_probability"],
                            "channel_contributions": res["channel_contributions"],
                            "risk_level": res["risk_level"],
                            "model_version": args.model_version,
                        })
                else:
                    logger.error(f"Claim {i} failed: {result.get('error')}")
                    predictions.append({
                        "claim_id": claims_data[i].get("claim_id", f"CLM-{i:06d}"),
                        "fraud_probability": 0.0,
                        "channel_contributions": {},
                        "risk_level": "ERROR",
                        "model_version": args.model_version,
                        "error": result.get("error"),
                    })

            # Save results
            metadata = {
                "claims_processed": len(predictions),
                "successful": sum(1 for p in predictions if p["risk_level"] != "ERROR"),
                "failed": sum(1 for p in predictions if p["risk_level"] == "ERROR"),
                "model_version": args.model_version,
            }
            save_predictions(predictions, args.output, metadata)

            logger.info(f"Batch inference complete: {metadata}")

        finally:
            engine.shutdown()

    finally:
        import ray
        ray.shutdown()


if __name__ == "__main__":
    main()