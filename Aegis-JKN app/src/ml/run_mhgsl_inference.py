"""
Aegis-JKN MHGSL Inference Runner CLI
Reads BPJS claims datasets (bpjs-real-claims.json or klaim-dataset.json),
executes the Multi-Hop Graph Structure Learning (MHGSL) engine,
and computes Topology (T), Feature (F), Semantic (S) channel metrics and fraud scores.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import torch

# Ensure Aegis-JKN app/src directory is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
SRC_DIR = SCRIPT_DIR.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import MHGSL Engine and components
try:
    from ml.mhgsl.engine import run_mhgsl_inference, MHGSLEngine, MHGSLChannelBuilder, extract_features_from_bpjs_df
except ImportError:
    from src.ml.mhgsl.engine import run_mhgsl_inference, MHGSLEngine, MHGSLChannelBuilder, extract_features_from_bpjs_df


DEFAULT_DATA_PATHS = [
    Path(r"N:\HEALTHKATHON\Aegis-JKN app\frontend\src\lib\data\bpjs-real-claims.json"),
    Path(r"N:\HEALTHKATHON\Aegis-JKN app\frontend\src\lib\data\klaim-dataset.json"),
]

DEFAULT_OUTPUT_PATH = Path(r"N:\HEALTHKATHON\Aegis-JKN app\src\ml\mhgsl_inference_output.json")

def load_claims_data(input_path: Optional[str] = None) -> tuple:
    """
    Loads claims data from a specified JSON/CSV/DTA file or searches defaults.
    Falls back gracefully between bpjs-real-claims.json and klaim-dataset.json.
    """
    chosen_path: Optional[Path] = None

    if input_path:
        p = Path(input_path)
        if p.exists() and p.stat().st_size > 5:
            chosen_path = p
        else:
            print(f"[Warning] Specified input {input_path} not found or empty. Falling back to defaults...")

    if not chosen_path:
        for p in DEFAULT_DATA_PATHS:
            if p.exists() and p.stat().st_size > 10:
                # Check if it has non-empty list
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data_preview = json.load(f)
                    if isinstance(data_preview, list) and len(data_preview) > 0:
                        chosen_path = p
                        break
                except Exception:
                    continue

    if not chosen_path:
        raise FileNotFoundError(
            f"No valid claims dataset found. Checked paths: {[str(p) for p in DEFAULT_DATA_PATHS]}"
        )

    print(f"[MHGSL Runner] Loading claims dataset from: {chosen_path}")

    if str(chosen_path).endswith(".json"):
        with open(chosen_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        df = pd.DataFrame(raw_data)
    elif str(chosen_path).endswith(".csv"):
        df = pd.read_csv(chosen_path)
    elif str(chosen_path).endswith(".dta"):
        df = pd.read_stata(chosen_path)
    else:
        raise ValueError(f"Unsupported file format: {chosen_path}")

    return df, chosen_path


def run_inference(
    df: pd.DataFrame,
    sample_size: Optional[int] = None,
    k_nn: int = 4,
    hidden_dim: int = 64
) -> Dict[str, Any]:
    """
    Executes MHGSL inference on DataFrame and extracts T, F, S channel metrics.
    """
    if sample_size and len(df) > sample_size:
        print(f"[MHGSL Runner] Subsampling dataset to {sample_size} records...")
        df_eval = df.iloc[:sample_size].copy().reset_index(drop=True)
    else:
        df_eval = df.copy().reset_index(drop=True)

    n_samples = len(df_eval)
    print(f"[MHGSL Runner] Running MHGSL inference across {n_samples} claims...")

    # Run core inference pipeline
    output = run_mhgsl_inference(df_eval, k_nn=k_nn, hidden_dim=hidden_dim)
    summary_df: pd.DataFrame = output["summary"]
    raw_results: Dict[str, Any] = output["raw_results"]

    # Extract claims identification
    name_col = next((c for c in ['Name', 'name', 'FKL02', 'claim_id'] if c in df_eval.columns), None)
    claim_names = df_eval[name_col].tolist() if name_col else [f"CLM-{i+1:04d}" for i in range(n_samples)]

    # Extract diagnosis & procedure labels for reporting
    diag_col = next((c for c in ['Diagnosis ICD-10', 'Diagnosis', 'FKL17A', 'icd10'] if c in df_eval.columns), None)
    proc_col = next((c for c in ['Prosedur ICD-9-CM', 'Prosedur', 'FKL30', 'icd9'] if c in df_eval.columns), None)
    cost_col = next((c for c in ['Biaya Rp', 'Biaya', 'FKL47', 'biaya_tagih'] if c in df_eval.columns), None)

    # Format detailed predictions list
    predictions: List[Dict[str, Any]] = []
    for i in range(n_samples):
        prob = float(summary_df.loc[i, "fraud_probability"])
        w_t = float(summary_df.loc[i, "weight_topology"])
        w_f = float(summary_df.loc[i, "weight_feature"])
        w_s = float(summary_df.loc[i, "weight_semantic"])
        s_t = float(summary_df.loc[i, "score_topology"])
        s_f = float(summary_df.loc[i, "score_feature"])
        s_s = float(summary_df.loc[i, "score_semantic"])

        # Determine risk tier based on threshold
        if prob >= 0.80:
            risk = "fraud"
            status = "escalate"
        elif prob >= 0.50:
            risk = "high"
            status = "flagged"
        elif prob >= 0.25:
            risk = "medium"
            status = "review"
        else:
            risk = "low"
            status = "auto_approved"

        item = {
            "claim_index": i,
            "claim_id": claim_names[i],
            "fraud_score": round(prob, 4),
            "risk_tier": risk,
            "status": status,
            "channels": {
                "topology": {
                    "weight": round(w_t, 4),
                    "score": round(s_t, 4)
                },
                "feature": {
                    "weight": round(w_f, 4),
                    "score": round(s_f, 4)
                },
                "semantic": {
                    "weight": round(w_s, 4),
                    "score": round(s_s, 4)
                }
            },
            "channel_contribution_str": f"T {w_t:.2f} · F {w_f:.2f} · S {w_s:.2f}"
        }

        if diag_col:
            item["diagnosis"] = str(df_eval.loc[i, diag_col])
        if proc_col:
            item["procedure"] = str(df_eval.loc[i, proc_col])
        if cost_col:
            item["cost_rp"] = float(pd.to_numeric(df_eval.loc[i, cost_col], errors='coerce') or 0.0)

        predictions.append(item)

    # Calculate aggregate metrics & distributions
    probs_array = summary_df["fraud_probability"].to_numpy()
    w_topo = summary_df["weight_topology"].to_numpy()
    w_feat = summary_df["weight_feature"].to_numpy()
    w_sem = summary_df["weight_semantic"].to_numpy()

    metrics = {
        "total_claims_evaluated": n_samples,
        "mean_fraud_score": round(float(np.mean(probs_array)), 4),
        "std_fraud_score": round(float(np.std(probs_array)), 4),
        "median_fraud_score": round(float(np.median(probs_array)), 4),
        "max_fraud_score": round(float(np.max(probs_array)), 4),
        "min_fraud_score": round(float(np.min(probs_array)), 4),
        "high_risk_count": int(np.sum(probs_array >= 0.50)),
        "high_risk_ratio": round(float(np.mean(probs_array >= 0.50)), 4),
        "channel_weights_mean": {
            "topology_T": round(float(np.mean(w_topo)), 4),
            "feature_F": round(float(np.mean(w_feat)), 4),
            "semantic_S": round(float(np.mean(w_sem)), 4)
        },
        "channel_scores_mean": {
            "topology_T": round(float(summary_df["score_topology"].mean()), 4),
            "feature_F": round(float(summary_df["score_feature"].mean()), 4),
            "semantic_S": round(float(summary_df["score_semantic"].mean()), 4)
        },
        "tensor_shapes": {
            "probabilities_shape": list(raw_results["probabilities"].shape),
            "channel_weights_shape": list(raw_results["channel_weights"].shape),
            "embedding_topology_shape": list(raw_results["embeddings"]["topology"].shape),
            "embedding_feature_shape": list(raw_results["embeddings"]["feature"].shape),
            "embedding_semantic_shape": list(raw_results["embeddings"]["semantic"].shape)
        }
    }

    return {
        "status": "success",
        "engine": "MHGSL-v2.1",
        "metrics": metrics,
        "predictions": predictions
    }


def main():
    parser = argparse.ArgumentParser(description="MHGSL Inference CLI Runner for BPJS Claims")
    parser.add_argument("--input", "-i", type=str, default=None, help="Input claims file (.json, .csv, .dta)")
    parser.add_argument("--output", "-o", type=str, default=str(DEFAULT_OUTPUT_PATH), help="Output JSON path")
    parser.add_argument("--sample-size", "-n", type=int, default=None, help="Max records to evaluate")
    parser.add_argument("--k-nn", "-k", type=int, default=4, help="K for feature channel similarity")
    parser.add_argument("--hidden-dim", type=int, default=64, help="Hidden dimensions for Dual-GCN")
    args = parser.parse_args()

    # 1. Load data
    df, source_file = load_claims_data(args.input)

    # 2. Run MHGSL inference
    results = run_inference(
        df=df,
        sample_size=args.sample_size,
        k_nn=args.k_nn,
        hidden_dim=args.hidden_dim
    )
    results["source_dataset"] = str(source_file)

    # 3. Save to output JSON
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[MHGSL Runner] Successfully saved inference results to: {output_path}")
    print("\n=== Aggregate Metrics ===")
    print(f"Total Evaluated Claims : {results['metrics']['total_claims_evaluated']}")
    print(f"Mean Fraud Score       : {results['metrics']['mean_fraud_score']}")
    print(f"High Risk Ratio (>=0.5): {results['metrics']['high_risk_ratio'] * 100:.1f}%")
    print(f"Channel Weights Mean   : T={results['metrics']['channel_weights_mean']['topology_T']:.4f}, "
          f"F={results['metrics']['channel_weights_mean']['feature_F']:.4f}, "
          f"S={results['metrics']['channel_weights_mean']['semantic_S']:.4f}")
    print(f"Tensor Shapes          : {results['metrics']['tensor_shapes']}")


if __name__ == "__main__":
    main()
