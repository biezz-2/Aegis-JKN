import numpy as np
import pandas as pd
from typing import Tuple, List, Optional

class TemporalSplitter:
    """
    Train/Val/Test split with temporal ordering to prevent data leakage.
    Fraud detection requires strict temporal splits since future data
    cannot inform past predictions.
    """
    def __init__(
        self,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        date_column: str = "claim_date",
        gap_days: int = 7  # Gap between splits to prevent leakage
    ):
        assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1.0"
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.date_column = date_column
        self.gap_days = gap_days

    def split(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Split DataFrame temporally.
        Returns: (train_df, val_df, test_df)
        """
        # Sort by date
        df = df.sort_values(self.date_column).reset_index(drop=True)
        n = len(df)

        # Calculate split indices
        train_end = int(n * self.train_ratio)
        val_end = train_end + int(n * self.val_ratio)

        # Apply gap to prevent leakage
        train_df = df.iloc[:train_end]
        val_df = df.iloc[train_end + self.gap_days:val_end]
        test_df = df.iloc[val_end + self.gap_days:]

        return train_df, val_df, test_df

    def get_split_indices(self, n_samples: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get integer indices for splits (useful for PyTorch datasets)"""
        train_end = int(n_samples * self.train_ratio)
        val_end = train_end + int(n_samples * self.val_ratio)

        train_idx = np.arange(0, train_end)
        val_idx = np.arange(train_end + self.gap_days, val_end)
        test_idx = np.arange(val_end + self.gap_days, n_samples)

        return train_idx, val_idx, test_idx

class KFoldTemporalSplitter:
    """
    K-Fold cross-validation with temporal ordering.
    Each fold maintains temporal sequence.
    """
    def __init__(
        self,
        n_splits: int = 5,
        date_column: str = "claim_date",
        gap_days: int = 7
    ):
        self.n_splits = n_splits
        self.date_column = date_column
        self.gap_days = gap_days

    def split(self, df: pd.DataFrame) -> List[Tuple[np.ndarray, np.ndarray]]:
        """
        Generate train/test indices for each fold.
        Returns list of (train_idx, test_idx) tuples.
        """
        df = df.sort_values(self.date_column).reset_index(drop=True)
        n = len(df)
        fold_size = n // self.n_splits

        splits = []
        for i in range(self.n_splits):
            test_start = i * fold_size
            test_end = (i + 1) * fold_size if i < self.n_splits - 1 else n

            test_idx = np.arange(test_start, test_end)
            # Train is everything before test with gap
            train_idx = np.arange(0, max(0, test_start - self.gap_days))

            if len(train_idx) > 0 and len(test_idx) > 0:
                splits.append((train_idx, test_idx))

        return splits