import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime

from .metrics import compute_all_metrics
from .splits import TemporalSplitter
from .robustness import MaskingRobustnessTest, CamouflageTest
from .baselines import get_baselines, run_baseline_comparison
from .report import generate_report


class BenchmarkSuite:
    """
    Complete evaluation benchmark suite for Aegis-JKN fraud detection.

    Includes:
    - Temporal train/val/test split
    - Core metrics: AUPRC, ROC-AUC, Precision@K, Recall@K, F1
    - Masking Robustness Test (10%, 20%, 30% feature masking)
    - Camouflage Test (adversarial fraud injection)
    - Baseline comparison: Logistic Regression, XGBoost, GCN
    - Automated JSON + HTML report generation
    """

    def __init__(
        self,
        model_predict_fn: Callable,
        task_type: str = "tabular",
        temporal_column: str = "claim_date",
        mask_ratios: List[float] = [0.1, 0.2, 0.3],
        n_mask_trials: int = 5,
        n_camouflage: int = 100,
        mimic_strength: float = 0.8,
        output_dir: str = "reports/evaluation",
        random_seed: int = 42
    ):
        self.model_predict_fn = model_predict_fn
        self.task_type = task_type
        self.temporal_column = temporal_column
        self.output_dir = output_dir
        self.random_seed = random_seed

        # Initialize components
        self.splitter = TemporalSplitter(date_column=temporal_column)
        self.masking_test = MaskingRobustnessTest(
            mask_ratios=mask_ratios,
            n_trials=n_mask_trials,
            random_seed=random_seed
        )
        self.camouflage_test = CamouflageTest(
            n_injected=n_camouflage,
            mimic_strength=mimic_strength,
            random_seed=random_seed
        )
        self.baselines = get_baselines(task_type=task_type)

        # Results storage
        self.results = {}

    def run(
        self,
        X: np.ndarray,
        y: np.ndarray,
        X_graph: Optional[np.ndarray] = None,
        edge_index: Optional[np.ndarray] = None,
        df: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Run complete evaluation pipeline.

        Args:
            X: Feature matrix (n_samples, n_features)
            y: Labels (n_samples,)
            X_graph: Graph features (for GCN baseline)
            edge_index: Graph edge indices (for GCN baseline)
            df: Optional DataFrame with temporal column for temporal splitting

        Returns:
            Dictionary with all evaluation results
        """
        print("=" * 60)
        print("AEGIS-JKN BENCHMARK SUITE")
        print("=" * 60)

        # 1. Temporal Split
        if df is not None and self.temporal_column in df.columns:
            print("\n[1/5] Performing temporal split...")
            train_df, val_df, test_df = self.splitter.split(df)
            train_idx = train_df.index.values
            val_idx = val_df.index.values
            test_idx = test_df.index.values
        else:
            # Fallback to simple temporal index split
            print("\n[1/5] Performing index-based temporal split...")
            n = len(X)
            train_idx, val_idx, test_idx = self.splitter.get_split_indices(n)

        X_train, y_train = X[train_idx], y[train_idx]
        X_val, y_val = X[val_idx], y[val_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        print(f"  Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

        # 2. Main Metrics on Test Set
        print("\n[2/5] Computing main metrics...")
        y_prob_test = self.model_predict_fn(X_test)
        main_metrics = compute_all_metrics(y_test, y_prob_test)
        print(f"  AUPRC: {main_metrics['auprc']:.4f}")
        print(f"  ROC-AUC: {main_metrics['roc_auc']:.4f}")
        print(f"  F1: {main_metrics['f1']:.4f}")

        # 3. Baseline Comparison
        print("\n[3/5] Running baseline comparison...")
        baseline_results = run_baseline_comparison(
            self.baselines,
            X_train, y_train,
            X_test, y_test,
            edge_index=edge_index,
            X_val=X_val, y_val=y_val
        )

        # 4. Masking Robustness
        print("\n[4/5] Running masking robustness test...")
        masking_results = self.masking_test.evaluate(
            self.model_predict_fn,
            X_test, y_test
        )

        # 5. Camouflage Test
        print("\n[5/5] Running camouflage detection test...")
        camouflage_results = self.camouflage_test.evaluate(
            self.model_predict_fn,
            X_test, y_test,
            X_train=X_train, y_train=y_train
        )

        # Compile results
        self.results = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "task_type": self.task_type,
                "train_size": len(X_train),
                "val_size": len(X_val),
                "test_size": len(X_test),
                "positive_rate": float(np.mean(y_test)),
                "random_seed": self.random_seed,
            },
            "main_metrics": main_metrics,
            "baseline_comparison": baseline_results,
            "robustness": {
                "masking": masking_results,
                "camouflage": camouflage_results,
            }
        }

        # Generate reports
        print("\nGenerating reports...")
        report_paths = generate_report(self.results, self.output_dir)
        print(f"  JSON: {report_paths['json_report']}")
        print(f"  HTML: {report_paths['html_report']}")

        return self.results

    def get_summary(self) -> str:
        """Get human-readable summary of results"""
        if not self.results:
            return "No results available. Run benchmark first."

        m = self.results["main_metrics"]
        b = self.results["baseline_comparison"]
        r = self.results["robustness"]

        summary = f"""
AEGIS-JKN EVALUATION SUMMARY
{'='*50}
Main Metrics:
  AUPRC:      {m['auprc']:.4f}
  ROC-AUC:    {m['roc_auc']:.4f}
  F1-Score:   {m['f1']:.4f}
  Precision@100: {m.get('precision@100', 'N/A'):.4f}
  Recall@100:    {m.get('recall@100', 'N/A'):.4f}

Baselines:
"""
        for name, res in b.items():
            if "error" not in res:
                summary += f"  {name:20s}: AUC={res['roc_auc']:.4f}, AUPRC={res['auprc']:.4f}\n"
            else:
                summary += f"  {name:20s}: ERROR - {res['error']}\n"

        summary += "\nMasking Robustness:\n"
        for ratio, res in r["masking"]["mask_results"].items():
            summary += f"  {ratio}: AUC deg={res['roc_auc_rel_degradation']:.1f}%, AUPRC deg={res['auprc_rel_degradation']:.1f}%\n"

        cam = r["camouflage"]["camouflage_only"]
        summary += f"\nCamouflage Detection Rate: {cam['detection_rate']:.2%}\n"
        summary += f"  AUC: {cam['roc_auc']:.4f}, AUPRC: {cam['auprc']:.4f}\n"

        return summary


def create_benchmark_suite(
    model_predict_fn: Callable,
    **kwargs
) -> BenchmarkSuite:
    """Factory function to create BenchmarkSuite with defaults"""
    return BenchmarkSuite(model_predict_fn, **kwargs)