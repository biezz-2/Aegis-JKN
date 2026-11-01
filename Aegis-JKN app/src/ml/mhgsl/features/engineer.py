"""
ML-03: Feature Engineer for Tier-2 XGBoost Rapid Screening Model.
Generates engineered features for fraud detection (non-graph features).
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import HashingVectorizer
import warnings
warnings.filterwarnings("ignore")


class Tier2FeatureEngineer:
    """
    Feature Engineering for Tier-2 XGBoost Rapid Screening (<100ms inference).

    Features engineered from claim/patient/provider data:
    - Claim-level: amount, ICD-10 complexity, diagnosis counts
    - Patient-level: age, gender, chronic conditions, claim history
    - Provider-level: billing patterns, specialty, network metrics
    - Temporal: day of week, month, seasonality
    - Interaction: amount per diagnosis, provider-patient frequency
    """

    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.feature_names = []
        self.is_fitted = False

    def fit(self, df: pd.DataFrame, target_col: str = "is_fraud") -> "Tier2FeatureEngineer":
        """Fit encoders and scalers on training data."""

        # Identify column types
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if target_col in num_cols:
            num_cols.remove(target_col)

        # Fit encoders for categorical columns
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = df[col].fillna("UNKNOWN").astype(str)
            le.fit(df[col])
            self.encoders[col] = le

        # Fit scalers for numerical columns
        for col in num_cols:
            scaler = StandardScaler()
            scaler.fit(df[[col]].fillna(0))
            self.scalers[col] = scaler

        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform data using fitted encoders/scalers."""
        if not self.is_fitted:
            raise ValueError("FeatureEngineer must be fitted before transform")

        df = df.copy()

        # Encode categorical
        for col, encoder in self.encoders.items():
            if col in df.columns:
                df[col] = df[col].fillna("UNKNOWN").astype(str)
                # Handle unseen labels
                mask = df[col].isin(encoder.classes_)
                df.loc[mask, col] = encoder.transform(df.loc[mask, col])
                df.loc[~mask, col] = -1  # Unknown category
            else:
                df[col] = -1

        # Scale numerical
        for col, scaler in self.scalers.items():
            if col in df.columns:
                df[col] = scaler.transform(df[[col]].fillna(0))
            else:
                df[col] = 0.0

        return df

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main feature engineering pipeline.
        Creates all Tier-2 features optimized for XGBoost.
        """
        df = df.copy()

        # --- Claim-level features ---
        df = self._engineer_claim_features(df)

        # --- Patient-level features ---
        df = self._engineer_patient_features(df)

        # --- Provider-level features ---
        df = self._engineer_provider_features(df)

        # --- Temporal features ---
        df = self._engineer_temporal_features(df)

        # --- Interaction features ---
        df = self._engineer_interaction_features(df)

        # --- ICD-10 complexity features ---
        df = self._engineer_icd10_features(df)

        return df

    def _engineer_claim_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer claim-specific features."""
        # Amount-based features
        if "amount" in df.columns:
            df["amount_log"] = np.log1p(df["amount"].clip(lower=0))
            df["amount_zscore"] = (df["amount"] - df["amount"].mean()) / (df["amount"].std() + 1e-8)
            df["amount_percentile"] = df["amount"].rank(pct=True)

        # Diagnosis count features
        if "diagnosis_count" in df.columns:
            df["diag_count_log"] = np.log1p(df["diagnosis_count"])

        # Procedure count
        if "procedure_count" in df.columns:
            df["proc_count_log"] = np.log1p(df["procedure_count"])

        # Claim type encoding
        if "claim_type" in df.columns:
            df["claim_type_encoded"] = df["claim_type"].astype("category").cat.codes

        return df

    def _engineer_patient_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer patient-specific features."""
        # Age features
        if "patient_age" in df.columns:
            df["age_log"] = np.log1p(df["patient_age"])
            df["age_bin"] = pd.cut(df["patient_age"], bins=[0, 18, 35, 50, 65, 100],
                                   labels=[0, 1, 2, 3, 4]).astype(float)
            df["is_elderly"] = (df["patient_age"] >= 65).astype(int)
            df["is_pediatric"] = (df["patient_age"] <= 18).astype(int)

        # Gender encoding
        if "patient_gender" in df.columns:
            df["gender_encoded"] = df["patient_gender"].map({"M": 0, "F": 1, "L": 2, "P": 3}).fillna(-1)

        # Chronic conditions
        if "chronic_conditions" in df.columns:
            df["chronic_count"] = df["chronic_conditions"].apply(
                lambda x: len(str(x).split(";")) if pd.notna(x) and x != "" else 0
            )
            df["has_chronic"] = (df["chronic_count"] > 0).astype(int)

        # Claim history features
        if "patient_claim_count_30d" in df.columns:
            df["claim_freq_30d_log"] = np.log1p(df["patient_claim_count_30d"])
        if "patient_claim_count_90d" in df.columns:
            df["claim_freq_90d_log"] = np.log1p(df["patient_claim_count_90d"])
        if "patient_total_amount_90d" in df.columns:
            df["patient_amt_90d_log"] = np.log1p(df["patient_total_amount_90d"])

        return df

    def _engineer_provider_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer provider-specific features."""
        # Provider billing stats
        if "provider_avg_amount" in df.columns:
            df["prov_avg_amt_log"] = np.log1p(df["provider_avg_amount"])
        if "provider_claim_count" in df.columns:
            df["prov_claim_count_log"] = np.log1p(df["provider_claim_count"])
        if "provider_fraud_rate" in df.columns:
            df["prov_fraud_rate"] = df["provider_fraud_rate"].clip(0, 1)

        # Provider specialty
        if "provider_specialty" in df.columns:
            df["prov_specialty_encoded"] = df["provider_specialty"].astype("category").cat.codes

        # Network metrics
        if "provider_network_degree" in df.columns:
            df["prov_net_degree_log"] = np.log1p(df["provider_network_degree"])

        return df

    def _engineer_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer temporal features."""
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df["day_of_week"] = df["date"].dt.dayofweek
            df["month"] = df["date"].dt.month
            df["quarter"] = df["date"].dt.quarter
            df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
            df["is_month_end"] = (df["date"].dt.day >= 28).astype(int)
            df["is_holiday_season"] = df["month"].isin([12, 1, 6, 7]).astype(int)  # Year-end, new year, mid-year

            # Cyclical encoding
            df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
            df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
            df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
            df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

        return df

    def _engineer_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer interaction features."""
        # Amount per diagnosis
        if "amount" in df.columns and "diagnosis_count" in df.columns:
            df["amt_per_diag"] = df["amount"] / (df["diagnosis_count"] + 1)
            df["amt_per_diag_log"] = np.log1p(df["amt_per_diag"])

        # Amount per procedure
        if "amount" in df.columns and "procedure_count" in df.columns:
            df["amt_per_proc"] = df["amount"] / (df["procedure_count"] + 1)
            df["amt_per_proc_log"] = np.log1p(df["amt_per_proc"])

        # Provider-patient interaction frequency
        if "provider_id" in df.columns and "patient_id" in df.columns:
            pair_key = df["provider_id"].astype(str) + "_" + df["patient_id"].astype(str)
            pair_counts = pair_key.value_counts()
            df["prov_pat_pair_freq"] = pair_key.map(pair_counts)
            df["prov_pat_pair_freq_log"] = np.log1p(df["prov_pat_pair_freq"])

        return df

    def _engineer_icd10_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer ICD-10 complexity features."""
        if "icd10" in df.columns:
            # Chapter-based grouping (first character of ICD-10)
            df["icd10_chapter"] = df["icd10"].astype(str).str[0].fillna("X")

            # Complexity: length of code (more chars = more specific)
            df["icd10_complexity"] = df["icd10"].astype(str).str.len().fillna(0)

            # Is primary diagnosis fraud-prone (certain chapters)
            fraud_prone_chapters = ["C", "D", "R", "Z"]  # Neoplasms, Symptoms, Factors
            df["icd10_fraud_prone"] = df["icd10_chapter"].isin(fraud_prone_chapters).astype(int)

            # Hash encoding for high cardinality
            if len(df["icd10"].unique()) > 100:
                vectorizer = HashingVectorizer(n_features=16, alternate_sign=False)
                icd_hash = vectorizer.fit_transform(df["icd10"].fillna("UNKNOWN"))
                for i in range(16):
                    df[f"icd10_hash_{i}"] = icd_hash[:, i].toarray().flatten()

        return df

    def get_feature_names(self, df: pd.DataFrame, exclude_cols: List[str] = None) -> List[str]:
        """Get list of feature column names for model training."""
        if exclude_cols is None:
            exclude_cols = ["is_fraud", "claim_id", "patient_id", "provider_id", "doctor_id",
                          "date", "icd10", "scenario", "claim_type", "provider_specialty",
                          "patient_gender", "chronic_conditions"]

        features = [c for c in df.columns if c not in exclude_cols]
        self.feature_names = features
        return features


def create_tier2_features(df: pd.DataFrame, fit: bool = True,
                          target_col: str = "is_fraud") -> tuple:
    """
    Convenience function to create Tier-2 features.

    Returns:
        X: Feature matrix
        y: Target vector (if target_col in df)
        engineer: Fitted Tier2FeatureEngineer instance
    """
    engineer = Tier2FeatureEngineer()

    # Engineer features
    df_feat = engineer.engineer_features(df)

    # Get feature columns
    feature_cols = engineer.get_feature_names(df_feat)

    if fit:
        engineer.fit(df_feat[feature_cols], target_col)
        X = engineer.transform(df_feat[feature_cols])
    else:
        X = df_feat[feature_cols]

    y = df_feat[target_col].values if target_col in df_feat.columns else None

    return X, y, engineer


# ponytail: Basic feature set. Upgrade with domain-specific features
# (e.g., DRG weights, drug cost ratios) when available.