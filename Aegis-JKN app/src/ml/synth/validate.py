import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from generator import SyntheticFraudGenerator, SynthConfig

def validate_statistical_parity(synthetic_df: pd.DataFrame, real_data_path: str = None):
    """
    Validate synthetic data matches real data distribution.
    Compares key statistical moments and distributions.
    """
    print("=== Statistical Parity Validation ===\n")

    # 1. Amount distribution
    print("1. CLAIM AMOUNT DISTRIBUTION")
    print(f"   Synthetic: mean={synthetic_df['amount'].mean():.2f}, std={synthetic_df['amount'].std():.2f}")
    print(f"   Skewness: {synthetic_df['amount'].skew():.3f}, Kurtosis: {synthetic_df['amount'].kurtosis():.3f}")

    # 2. Fraud prevalence check
    print(f"\n2. FRAUD PREVALENCE")
    actual_fraud_rate = synthetic_df['is_fraud'].mean()
    print(f"   Target: {0.08:.1%}, Actual: {actual_fraud_rate:.1%}")

    # 3. Scenario distribution
    print(f"\n3. FRAUD SCENARIO DISTRIBUTION")
    scenario_counts = synthetic_df[synthetic_df['is_fraud']==1]['scenario'].value_counts()
    for sc, count in scenario_counts.items():
        print(f"   {sc}: {count} ({count/len(synthetic_df):.1%})")

    # 4. Provider distribution
    print(f"\n4. PROVIDER DISTRIBUTION")
    prov_dist = synthetic_df['provider_id'].value_counts()
    print(f"   Unique providers: {len(prov_dist)}, Top 3: {prov_dist.head(3).to_dict()}")

    # 5. Missing data rate
    print(f"\n5. MISSING DATA RATE")
    missing_rate = synthetic_df.isnull().mean().mean()
    print(f"   Overall missing rate: {missing_rate:.3%}")

    # 6. KS Test for amount distribution (if real data provided)
    if real_data_path:
        try:
            real_df = pd.read_csv(real_data_path)
            if 'amount' in real_df.columns:
                ks_stat, p_val = stats.ks_2samp(synthetic_df['amount'], real_df['amount'])
                print(f"\n6. KS TEST vs REAL DATA: stat={ks_stat:.4f}, p={p_val:.4f}")
                print(f"   {'PASS' if p_val > 0.05 else 'FAIL'} - {'Distributions match' if p_val > 0.05 else 'Distributions differ'}")
        except Exception as e:
            print(f"\n6. Real data comparison skipped: {e}")

    return True

def generate_report(synthetic_df: pd.DataFrame, output_path: str = "validation_report.txt"):
    """Generate validation report."""
    with open(output_path, "w") as f:
        f.write("SYNTHETIC DATA VALIDATION REPORT v2.1\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Samples: {len(synthetic_df)}\n")
        f.write(f"Fraud Rate: {synthetic_df['is_fraud'].mean():.2%}\n")
        f.write(f"Amount Mean: {synthetic_df['amount'].mean():.2f}\n")
        f.write(f"Amount Std: {synthetic_df['amount'].std():.2f}\n")
        f.write(f"Missing Rate: {synthetic_df.isnull().mean().mean():.3%}\n")
        f.write(f"\nScenario Breakdown:\n")
        for sc, cnt in synthetic_df[synthetic_df['is_fraud']==1]['scenario'].value_counts().items():
            f.write(f"  {sc}: {cnt}\n")

    print(f"\nReport saved to {output_path}")

if __name__ == "__main__":
    config = SynthConfig(fraud_prevalence=0.08, num_samples=5000)
    gen = SyntheticFraudGenerator(config)
    df = gen.generate()

    validate_statistical_parity(df)
    generate_report(df)