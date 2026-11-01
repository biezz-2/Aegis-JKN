import torch
import torch.nn as nn
from typing import List, Dict, Optional, Union
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.decomposition import PCA
import logging

logger = logging.getLogger(__name__)

class ClinicalBERTEmbedder:
    """
    Clinical-NLP BERT embedder for medical narrative extraction.

    Uses Clinical-BERT (or BioBERT as fallback) to extract contextual embeddings
    from medical claim narratives.

    Models supported:
    - "emilyalsentzer/Bio_ClinicalBERT" (Clinical-BERT on MIMIC-III)
    - "dmis-lab/biobert-v1.1" (BioBERT on PubMed/PMC)
    - "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract" (PubMedBERT)
    """

    def __init__(
        self,
        model_name: str = "emilyalsentzer/Bio_ClinicalBERT",
        max_length: int = 512,
        device: Optional[str] = None,
        pooling_strategy: str = "cls"  # "cls", "mean", "max"
    ):
        self.model_name = model_name
        self.max_length = max_length
        self.pooling_strategy = pooling_strategy

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        logger.info(f"Loading {model_name} on {self.device}...")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

        self.embedding_dim = self.model.config.hidden_size  # 768 for base models

        logger.info(f"Clinical-BERT loaded. Embedding dimension: {self.embedding_dim}")

    def _pool_embeddings(
        self,
        last_hidden_state: torch.Tensor,
        attention_mask: torch.Tensor
    ) -> torch.Tensor:
        """
        Pool token embeddings to sentence-level representation.

        Args:
            last_hidden_state: [batch_size, seq_len, hidden_dim]
            attention_mask: [batch_size, seq_len]

        Returns:
            [batch_size, hidden_dim]
        """
        if self.pooling_strategy == "cls":
            return last_hidden_state[:, 0, :]  # [CLS] token

        elif self.pooling_strategy == "mean":
            # Mean pooling with attention mask
            mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size()).float()
            summed = torch.sum(last_hidden_state * mask, dim=1)
            counts = torch.clamp(mask.sum(dim=1), min=1e-9)
            return summed / counts

        elif self.pooling_strategy == "max":
            # Max pooling
            mask = attention_mask.unsqueeze(-1).expand(last_hidden_state.size())
            last_hidden_state = last_hidden_state.masked_fill(mask == 0, -1e9)
            return torch.max(last_hidden_state, dim=1)[0]

        else:
            raise ValueError(f"Unknown pooling strategy: {self.pooling_strategy}")

    @torch.no_grad()
    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: int = 16,
        show_progress: bool = False
    ) -> torch.Tensor:
        """
        Encode medical narratives into embeddings.

        Args:
            texts: Single text or list of medical narratives
            batch_size: Batch size for encoding
            show_progress: Show progress bar

        Returns:
            Tensor of shape [num_texts, embedding_dim]
        """
        if isinstance(texts, str):
            texts = [texts]

        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]

            # Tokenize
            encoded = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            ).to(self.device)

            # Forward pass
            outputs = self.model(**encoded)
            last_hidden_state = outputs.last_hidden_state

            # Pool to sentence embedding
            embeddings = self._pool_embeddings(last_hidden_state, encoded["attention_mask"])
            all_embeddings.append(embeddings.cpu())

        return torch.cat(all_embeddings, dim=0)


class SemanticDimensionalityReducer:
    """
    Dimensionality reduction for semantic embeddings.

    Supports PCA (linear) and UMAP (non-linear) for reducing
    BERT embeddings (768-dim) to semantic channel dimension (e.g., 64-dim).
    """

    def __init__(
        self,
        method: str = "pca",
        target_dim: int = 64,
        random_state: int = 42,
        **kwargs
    ):
        self.method = method.lower()
        self.target_dim = target_dim
        self.random_state = random_state
        self.kwargs = kwargs

        self.reducer = None
        self._is_fitted = False

        if self.method == "pca":
            self.reducer = PCA(
                n_components=target_dim,
                random_state=random_state,
                **kwargs
            )
        elif self.method == "umap":
            try:
                import umap
                self.reducer = umap.UMAP(
                    n_components=target_dim,
                    random_state=random_state,
                    **kwargs
                )
            except ImportError:
                logger.warning("UMAP not installed. Falling back to PCA.")
                self.method = "pca"
                self.reducer = PCA(
                    n_components=target_dim,
                    random_state=random_state,
                    **kwargs
                )
        else:
            raise ValueError(f"Unknown reduction method: {method}. Use 'pca' or 'umap'.")

    def fit(self, embeddings: torch.Tensor) -> "SemanticDimensionalityReducer":
        """Fit reducer on training embeddings."""
        X = embeddings.cpu().numpy() if isinstance(embeddings, torch.Tensor) else embeddings
        self.reducer.fit(X)
        self._is_fitted = True
        logger.info(f"Fitted {self.method.upper()} reducer: {X.shape[1]} -> {self.target_dim}")
        return self

    def transform(self, embeddings: torch.Tensor) -> torch.Tensor:
        """Transform embeddings to reduced dimension."""
        if not self._is_fitted:
            raise RuntimeError("Reducer must be fitted before transform. Call fit() first.")

        X = embeddings.cpu().numpy() if isinstance(embeddings, torch.Tensor) else embeddings
        reduced = self.reducer.transform(X)
        return torch.tensor(reduced, dtype=torch.float32)

    def fit_transform(self, embeddings: torch.Tensor) -> torch.Tensor:
        """Fit and transform in one step."""
        X = embeddings.cpu().numpy() if isinstance(embeddings, torch.Tensor) else embeddings
        self.reducer.fit(X)
        self._is_fitted = True
        reduced = self.reducer.transform(X)
        logger.info(f"Fit-transform {self.method.upper()}: {X.shape[1]} -> {self.target_dim}")
        return torch.tensor(reduced, dtype=torch.float32)


class SemanticChannel(nn.Module):
    """
    Semantic Channel for MHGSL.

    Implements: Tokenization -> Embedding (Clinical-BERT) -> Dimensionality Reduction (PCA/UMAP)

    Output: Tensor [num_nodes, semantic_dim] ready for fusion in MHGSL model.
    """

    def __init__(
        self,
        model_name: str = "emilyalsentzer/Bio_ClinicalBERT",
        semantic_dim: int = 64,
        reduction_method: str = "pca",
        max_length: int = 512,
        pooling_strategy: str = "cls",
        device: Optional[str] = None,
        freeze_bert: bool = True,
        pca_fitted: bool = False  # Set True after fitting on training data
    ):
        super().__init__()

        self.semantic_dim = semantic_dim
        self.reduction_method = reduction_method
        self.pca_fitted = pca_fitted

        # Clinical-BERT Embedder
        self.embedder = ClinicalBERTEmbedder(
            model_name=model_name,
            max_length=max_length,
            device=device,
            pooling_strategy=pooling_strategy
        )

        # Freeze BERT parameters if specified
        if freeze_bert:
            for param in self.embedder.model.parameters():
                param.requires_grad = False
            logger.info("Clinical-BERT parameters frozen.")

        # Dimensionality Reducer
        self.reducer = SemanticDimensionalityReducer(
            method=reduction_method,
            target_dim=semantic_dim
        )

        # Optional: Learnable projection layer for fine-tuning
        self.projection = nn.Linear(semantic_dim, semantic_dim)

        logger.info(f"Semantic Channel initialized: dim={semantic_dim}, reduction={reduction_method}")

    def fit_reducer(self, narratives: List[str], batch_size: int = 16) -> "SemanticChannel":
        """
        Fit the dimensionality reducer on a corpus of medical narratives.

        Should be called once during training pipeline setup.
        """
        logger.info(f"Fitting reducer on {len(narratives)} narratives...")
        embeddings = self.embedder.encode(narratives, batch_size=batch_size, show_progress=True)
        self.reducer.fit(embeddings)
        self.pca_fitted = True
        return self

    def forward(
        self,
        narratives: Union[str, List[str]],
        return_embeddings: bool = False
    ) -> Union[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Forward pass: narratives -> BERT embeddings -> reduced semantic features.

        Args:
            narratives: Medical claim narratives (single string or list)
            return_embeddings: If True, also return raw BERT embeddings

        Returns:
            If return_embeddings=False: Tensor [num_nodes, semantic_dim]
            If return_embeddings=True: Dict with 'semantic' (reduced) and 'raw' (BERT) embeddings
        """
        # Encode with Clinical-BERT
        raw_embeddings = self.embedder.encode(narratives)

        # Reduce dimensionality
        if self.pca_fitted and self.reducer._is_fitted:
            semantic_embeddings = self.reducer.transform(raw_embeddings)
        else:
            # If not fitted, fit on the fly (not recommended for production)
            logger.warning("Reducer not fitted. Fitting on current batch.")
            semantic_embeddings = self.reducer.fit_transform(raw_embeddings)
            self.pca_fitted = True

        # Optional learnable projection
        semantic_embeddings = self.projection(semantic_embeddings)

        if return_embeddings:
            return {
                "semantic": semantic_embeddings,  # [num_nodes, semantic_dim]
                "raw": raw_embeddings  # [num_nodes, 768]
            }

        return semantic_embeddings


class SemanticSimilarity:
    """
    Semantic similarity measures between medical claim narratives.

    Computes similarity based on Clinical-BERT embeddings.
    """

    def __init__(
        self,
        embedder: Optional[ClinicalBERTEmbedder] = None,
        model_name: str = "emilyalsentzer/Bio_ClinicalBERT",
        device: Optional[str] = None
    ):
        if embedder is not None:
            self.embedder = embedder
        else:
            self.embedder = ClinicalBERTEmbedder(model_name=model_name, device=device)

    @torch.no_grad()
    def cosine_similarity(
        self,
        text1: Union[str, List[str]],
        text2: Union[str, List[str]]
    ) -> torch.Tensor:
        """
        Compute cosine similarity between two sets of medical narratives.

        Args:
            text1: First narrative(s)
            text2: Second narrative(s)

        Returns:
            If both single: scalar tensor
            If one list, one single: tensor [len(list)]
            If both lists: tensor [len(text1), len(text2)]
        """
        # Encode both
        if isinstance(text1, str):
            text1 = [text1]
        if isinstance(text2, str):
            text2 = [text2]

        emb1 = self.embedder.encode(text1)
        emb2 = self.embedder.encode(text2)

        # Normalize
        emb1_norm = F.normalize(emb1, p=2, dim=1)
        emb2_norm = F.normalize(emb2, p=2, dim=1)

        # Cosine similarity
        sim = torch.mm(emb1_norm, emb2_norm.t())

        # Return appropriate shape
        if sim.shape == (1, 1):
            return sim[0, 0]
        elif sim.shape[0] == 1:
            return sim[0]
        elif sim.shape[1] == 1:
            return sim[:, 0]
        return sim

    @torch.no_grad()
    def euclidean_distance(
        self,
        text1: Union[str, List[str]],
        text2: Union[str, List[str]]
    ) -> torch.Tensor:
        """Compute Euclidean distance between narratives."""
        if isinstance(text1, str):
            text1 = [text1]
        if isinstance(text2, str):
            text2 = [text2]

        emb1 = self.embedder.encode(text1)
        emb2 = self.embedder.encode(text2)

        # Pairwise distances
        return torch.cdist(emb1, emb2, p=2)

    @torch.no_grad()
    def similarity_matrix(self, texts: List[str]) -> torch.Tensor:
        """
        Compute full similarity matrix for a list of narratives.

        Returns: [num_texts, num_texts]
        """
        emb = self.embedder.encode(texts)
        emb_norm = F.normalize(emb, p=2, dim=1)
        return torch.mm(emb_norm, emb_norm.t())


# Import functional for similarity
import torch.nn.functional as F

# ponytail: Basic Clinical-BERT + PCA pipeline.
# Upgrade: Fine-tune BERT on JKN claim corpus if domain shift detected.
# Upgrade: Use UMAP for non-linear manifold preservation if clusters are non-convex.