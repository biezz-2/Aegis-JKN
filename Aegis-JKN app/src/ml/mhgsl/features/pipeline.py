import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import RobustScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

class FeatureChannelPipeline:
    """
    Feature Engineering Pipeline for MHGSL.
    Implements construction of numerical/categorical features with strict Anti-Leakage.
    """
    def __init__(self):
        self.scaler = RobustScaler()
        self.imputer = IterativeImputer(max_iter=10, random_state=42)

        # Strict Anti-Leakage: Columns that MUST be removed before training
        self.leakage_columns = {
            'target', 'fraud_label', 'is_fraud',
            'shap_value', 'channel_contribution',
            'prediction_prob', 'ground_truth'
        }

    def _apply_anti_leakage(self, df):
        """
        Explicit filter to remove target and signal columns.
        """
        cols_to_drop = [col for col in df.columns if col.lower() in self.leakage_columns]
        if cols_to_drop:
            # print(f"Anti-Leakage: Dropping {cols_to_drop}")
            df = df.drop(columns=cols_to_drop)
        return df

    def construct_features(self, claims_df, providers_df=None, patients_df=None):
        """
        Constructs feature tensors for claims, providers, and patients.

        Returns:
            feature_dict: { 'claim': Tensor, 'provider': Tensor, 'patient': Tensor }
        """
        # 1. Anti-Leakage Pass
        claims_df = self._apply_anti_leakage(claims_df)
        if providers_df is not None:
            providers_df = self._apply_anti_leakage(providers_df)
        if patients_df is not None:
            patients_df = self._apply_anti_leakage(patients_df)

        # 2. Feature Construction (Claim nodes)
        # Numerical: cost, duration, frequency
        num_cols = claims_df.select_dtypes(include=[np.number]).columns.tolist()

        # Remove IDs from numerical features to prevent model from memorizing them
        id_cols = [col for col in num_cols if 'id' in col.lower()]
        num_cols = [col for col in num_cols if col not in id_cols]

        # Handling Missing Values (Iterative Imputer)
        if not claims_df[num_cols].empty:
            claims_df[num_cols] = self.imputer.fit_transform(claims_df[num_cols])

            # Normalization (RobustScaler for cost outliers)
            claims_df[num_cols] = self.scaler.fit_transform(claims_df[num_cols])

        # Categorical handling (One-hot encoding)
        cat_cols = claims_df.select_dtypes(include=['object', 'category']).columns.tolist()
        # Also exclude IDs from one-hot encoding
        cat_cols = [col for col in cat_cols if 'id' not in col.lower()]

        claims_df_final = pd.get_dummies(claims_df, columns=cat_cols)

        # Remove remaining ID columns before tensor conversion
        all_id_cols = [col for col in claims_df_final.columns if 'id' in col.lower()]
        claims_df_final = claims_df_final.drop(columns=all_id_cols)

        # 3. Convert to Tensors
        feature_dict = {}
        feature_dict['claim'] = torch.tensor(claims_df_final.values.astype(np.float32), dtype=torch.float32)

        if providers_df is not None:
            # Anti-Leakage already applied. Remove IDs.
            prov_df_final = providers_df.copy()
            prov_id_cols = [col for col in prov_df_final.columns if 'id' in col.lower()]
            prov_df_final = prov_df_final.drop(columns=prov_id_cols)

            prov_num = prov_df_final.select_dtypes(include=[np.number]).columns.tolist()
            if prov_num:
                prov_df_final[prov_num] = self.scaler.fit_transform(prov_df_final[prov_num])

            prov_cat = prov_df_final.select_dtypes(include=['object', 'category']).columns.tolist()
            prov_df_final = pd.get_dummies(prov_df_final, columns=prov_cat)

            feature_dict['provider'] = torch.tensor(prov_df_final.values.astype(np.float32), dtype=torch.float32)

        if patients_df is not None:
            # Anti-Leakage already applied. Remove IDs.
            pat_df_final = patients_df.copy()
            pat_id_cols = [col for col in pat_df_final.columns if 'id' in col.lower()]
            pat_df_final = pat_df_final.drop(columns=pat_id_cols)

            pat_num = pat_df_final.select_dtypes(include=[np.number]).columns.tolist()
            if pat_num:
                pat_df_final[pat_num] = self.scaler.fit_transform(pat_df_final[pat_num])

            pat_cat = pat_df_final.select_dtypes(include=['object', 'category']).columns.tolist()
            pat_df_final = pd.get_dummies(pat_df_final, columns=pat_cat)

            feature_dict['patient'] = torch.tensor(pat_df_final.values.astype(np.float32), dtype=torch.float32)

        return feature_dict

    def transform(self, claims_df, providers_df=None, patients_df=None):
        """
        Transform new data using fitted imputer and scaler.
        """
        claims_df = self._apply_anti_leakage(claims_df)

        num_cols = claims_df.select_dtypes(include=[np.number]).columns.tolist()
        if not claims_df[num_cols].empty:
            claims_df[num_cols] = self.imputer.transform(claims_df[num_cols])
            claims_df[num_cols] = self.scaler.transform(claims_df[num_cols])

        # Categorical (ensure columns match training)
        # In real impl, we'd save the categories from fit
        cat_cols = claims_df.select_dtypes(include=['object', 'category']).columns.tolist()
        claims_df = pd.get_dummies(claims_df, columns=cat_cols)

        feature_dict = {}
        feature_dict['claim'] = torch.tensor(claims_df.values, dtype=torch.float32)
        # ... similarly for others

        return feature_dict
