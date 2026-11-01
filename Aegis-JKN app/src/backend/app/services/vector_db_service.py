"""Qdrant Vector Database Service for Semantic Feature Retrieval."""
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType,
    OptimizersConfigDiff,
    CollectionStatus,
)
from ..core.config import Settings, get_settings

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Result from vector search."""
    id: str
    score: float
    payload: Dict[str, Any]


class VectorDBService:
    """Service for managing Qdrant vector database operations."""

    # Collection names
    CLAIM_EMBEDDINGS = "claim_embeddings"
    PROVIDER_PROFILES = "provider_profiles"

    # Vector dimensions
    CLAIM_EMBEDDING_DIM = 768  # Clinical-BERT
    PROVIDER_PROFILE_DIM = 512

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.client: Optional[AsyncQdrantClient] = None
        self._initialized = False

    async def initialize(self):
        """Initialize Qdrant client and create collections."""
        if self._initialized:
            return

        try:
            # Get Qdrant URL from settings (default to local)
            qdrant_url = getattr(self.settings, 'qdrant_url', 'http://localhost:6333')
            qdrant_api_key = getattr(self.settings, 'qdrant_api_key', None)

            self.client = AsyncQdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
            )

            # Create collections if they don't exist
            await self._create_collections()

            # Create payload indexes for filtering
            await self._create_payload_indexes()

            self._initialized = True
            logger.info("Qdrant Vector DB Service initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {str(e)}")
            raise RuntimeError(f"Vector DB initialization failed: {str(e)}")

    async def _create_collections(self):
        """Create vector collections with proper configuration."""
        collections_to_create = [
            {
                "name": self.CLAIM_EMBEDDINGS,
                "dim": self.CLAIM_EMBEDDING_DIM,
                "description": "Clinical-BERT embeddings for claims",
            },
            {
                "name": self.PROVIDER_PROFILES,
                "dim": self.PROVIDER_PROFILE_DIM,
                "description": "Provider profile embeddings",
            },
        ]

        for coll in collections_to_create:
            exists = await self.client.collection_exists(coll["name"])
            if not exists:
                await self.client.create_collection(
                    collection_name=coll["name"],
                    vectors_config=VectorParams(
                        size=coll["dim"],
                        distance=Distance.COSINE,
                    ),
                    optimizers_config=OptimizersConfigDiff(
                        indexing_threshold=20000,
                        memmap_threshold=50000,
                    ),
                )
                logger.info(f"Created collection: {coll['name']} ({coll['description']})")
            else:
                logger.info(f"Collection already exists: {coll['name']}")

    async def _create_payload_indexes(self):
        """Create payload indexes for efficient metadata filtering."""
        indexes = [
            # Claim embeddings indexes
            (self.CLAIM_EMBEDDINGS, "claim_type", PayloadSchemaType.KEYWORD),
            (self.CLAIM_EMBEDDINGS, "provider_category", PayloadSchemaType.KEYWORD),
            (self.CLAIM_EMBEDDINGS, "timestamp", PayloadSchemaType.DATETIME),
            (self.CLAIM_EMBEDDINGS, "provider_id", PayloadSchemaType.KEYWORD),
            (self.CLAIM_EMBEDDINGS, "patient_id", PayloadSchemaType.KEYWORD),
            (self.CLAIM_EMBEDDINGS, "fraud_label", PayloadSchemaType.BOOL),

            # Provider profiles indexes
            (self.PROVIDER_PROFILES, "provider_category", PayloadSchemaType.KEYWORD),
            (self.PROVIDER_PROFILES, "provider_type", PayloadSchemaType.KEYWORD),
            (self.PROVIDER_PROFILES, "region", PayloadSchemaType.KEYWORD),
            (self.PROVIDER_PROFILES, "specialization", PayloadSchemaType.KEYWORD),
            (self.PROVIDER_PROFILES, "risk_tier", PayloadSchemaType.KEYWORD),
        ]

        for collection, field, schema_type in indexes:
            try:
                await self.client.create_payload_index(
                    collection_name=collection,
                    field_name=field,
                    field_schema=schema_type,
                )
                logger.debug(f"Created index on {collection}.{field}")
            except Exception as e:
                # Index might already exist
                logger.debug(f"Index on {collection}.{field} may already exist: {str(e)}")

    # --- Claim Embeddings Operations ---

    async def upsert_claim_embedding(
        self,
        claim_id: str,
        embedding: List[float],
        metadata: Dict[str, Any],
    ) -> bool:
        """
        Upsert a new claim embedding with metadata.

        Args:
            claim_id: Unique identifier for the claim
            embedding: 768-dimensional Clinical-BERT embedding
            metadata: Dict containing claim_type, provider_category, timestamp, etc.

        Returns:
            True if successful
        """
        if not self._initialized:
            await self.initialize()

        if len(embedding) != self.CLAIM_EMBEDDING_DIM:
            raise ValueError(
                f"Embedding dimension mismatch: expected {self.CLAIM_EMBEDDING_DIM}, "
                f"got {len(embedding)}"
            )

        # Ensure required metadata fields
        payload = {
            "claim_id": claim_id,
            "claim_type": metadata.get("claim_type", "unknown"),
            "provider_category": metadata.get("provider_category", "unknown"),
            "provider_id": metadata.get("provider_id", ""),
            "patient_id": metadata.get("patient_id", ""),
            "timestamp": metadata.get("timestamp", ""),
            "fraud_label": metadata.get("fraud_label", False),
            "amount": metadata.get("amount", 0.0),
            "diagnosis_codes": metadata.get("diagnosis_codes", []),
            "procedure_codes": metadata.get("procedure_codes", []),
        }

        point = PointStruct(
            id=claim_id,
            vector=embedding,
            payload=payload,
        )

        try:
            await self.client.upsert(
                collection_name=self.CLAIM_EMBEDDINGS,
                points=[point],
            )
            logger.debug(f"Upserted claim embedding: {claim_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to upsert claim embedding {claim_id}: {str(e)}")
            raise

    async def upsert_claim_embeddings_batch(
        self,
        claims: List[Dict[str, Any]],
    ) -> int:
        """
        Batch upsert multiple claim embeddings.

        Args:
            claims: List of dicts with claim_id, embedding, and metadata

        Returns:
            Number of successfully upserted points
        """
        if not self._initialized:
            await self.initialize()

        points = []
        for claim in claims:
            claim_id = claim["claim_id"]
            embedding = claim["embedding"]
            metadata = claim.get("metadata", {})

            if len(embedding) != self.CLAIM_EMBEDDING_DIM:
                logger.warning(f"Skipping {claim_id}: dimension mismatch")
                continue

            payload = {
                "claim_id": claim_id,
                "claim_type": metadata.get("claim_type", "unknown"),
                "provider_category": metadata.get("provider_category", "unknown"),
                "provider_id": metadata.get("provider_id", ""),
                "patient_id": metadata.get("patient_id", ""),
                "timestamp": metadata.get("timestamp", ""),
                "fraud_label": metadata.get("fraud_label", False),
                "amount": metadata.get("amount", 0.0),
                "diagnosis_codes": metadata.get("diagnosis_codes", []),
                "procedure_codes": metadata.get("procedure_codes", []),
            }

            points.append(PointStruct(id=claim_id, vector=embedding, payload=payload))

        if not points:
            return 0

        try:
            await self.client.upsert(
                collection_name=self.CLAIM_EMBEDDINGS,
                points=points,
            )
            logger.info(f"Batch upserted {len(points)} claim embeddings")
            return len(points)
        except Exception as e:
            logger.error(f"Batch upsert failed: {str(e)}")
            raise

    async def semantic_search_claims(
        self,
        query_embedding: List[float],
        limit: int = 10,
        score_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """
        Semantic search for similar claims using nearest neighbors.

        Args:
            query_embedding: 768-dim query embedding
            limit: Maximum number of results
            score_threshold: Minimum cosine similarity score
            filters: Optional metadata filters (claim_type, provider_category, etc.)

        Returns:
            List of SearchResult with id, score, and payload
        """
        if not self._initialized:
            await self.initialize()

        if len(query_embedding) != self.CLAIM_EMBEDDING_DIM:
            raise ValueError(
                f"Query embedding dimension mismatch: expected {self.CLAIM_EMBEDDING_DIM}"
            )

        # Build filter if provided
        query_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, list):
                    conditions.append(FieldCondition(key=key, match=MatchValue(any=value)))
                else:
                    conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
            if conditions:
                query_filter = Filter(must=conditions)

        try:
            results = await self.client.search(
                collection_name=self.CLAIM_EMBEDDINGS,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter,
                with_payload=True,
            )

            return [
                SearchResult(
                    id=str(r.id),
                    score=r.score,
                    payload=r.payload or {},
                )
                for r in results
            ]
        except Exception as e:
            logger.error(f"Semantic search failed: {str(e)}")
            raise

    async def hybrid_search_claims(
        self,
        query_embedding: List[float],
        filters: Dict[str, Any],
        limit: int = 10,
        score_threshold: float = 0.7,
    ) -> List[SearchResult]:
        """
        Hybrid search: semantic similarity + metadata filtering.

        Example use case: Find similar claims ONLY for "Hospital Type A" providers.

        Args:
            query_embedding: 768-dim query embedding
            filters: Required metadata filters (e.g., {"provider_category": "hospital_type_a"})
            limit: Maximum results
            score_threshold: Minimum similarity score

        Returns:
            List of SearchResult
        """
        return await self.semantic_search_claims(
            query_embedding=query_embedding,
            limit=limit,
            score_threshold=score_threshold,
            filters=filters,
        )

    # --- Provider Profiles Operations ---

    async def upsert_provider_profile(
        self,
        provider_id: str,
        embedding: List[float],
        metadata: Dict[str, Any],
    ) -> bool:
        """Upsert a provider profile embedding."""
        if not self._initialized:
            await self.initialize()

        if len(embedding) != self.PROVIDER_PROFILE_DIM:
            raise ValueError(
                f"Provider embedding dimension mismatch: expected {self.PROVIDER_PROFILE_DIM}, "
                f"got {len(embedding)}"
            )

        payload = {
            "provider_id": provider_id,
            "provider_category": metadata.get("provider_category", "unknown"),
            "provider_type": metadata.get("provider_type", "unknown"),
            "region": metadata.get("region", ""),
            "specialization": metadata.get("specialization", ""),
            "risk_tier": metadata.get("risk_tier", "low"),
            "total_claims": metadata.get("total_claims", 0),
            "fraud_rate": metadata.get("fraud_rate", 0.0),
        }

        point = PointStruct(id=provider_id, vector=embedding, payload=payload)

        try:
            await self.client.upsert(
                collection_name=self.PROVIDER_PROFILES,
                points=[point],
            )
            return True
        except Exception as e:
            logger.error(f"Failed to upsert provider profile {provider_id}: {str(e)}")
            raise

    async def semantic_search_providers(
        self,
        query_embedding: List[float],
        limit: int = 10,
        score_threshold: float = 0.7,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Semantic search for similar provider profiles."""
        if not self._initialized:
            await self.initialize()

        if len(query_embedding) != self.PROVIDER_PROFILE_DIM:
            raise ValueError(
                f"Query embedding dimension mismatch: expected {self.PROVIDER_PROFILE_DIM}"
            )

        query_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                if isinstance(value, list):
                    conditions.append(FieldCondition(key=key, match=MatchValue(any=value)))
                else:
                    conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
            if conditions:
                query_filter = Filter(must=conditions)

        try:
            results = await self.client.search(
                collection_name=self.PROVIDER_PROFILES,
                query_vector=query_embedding,
                limit=limit,
                score_threshold=score_threshold,
                query_filter=query_filter,
                with_payload=True,
            )

            return [
                SearchResult(id=str(r.id), score=r.score, payload=r.payload or {})
                for r in results
            ]
        except Exception as e:
            logger.error(f"Provider semantic search failed: {str(e)}")
            raise

    # --- Integration with Graph Service ---

    async def enrich_node_features(
        self,
        node_type: str,
        node_ids: List[str],
    ) -> Dict[str, List[float]]:
        """
        Retrieve embeddings for graph nodes to enrich features.

        Args:
            node_type: "claim" or "provider"
            node_ids: List of node IDs

        Returns:
            Dict mapping node_id to embedding vector
        """
        if not self._initialized:
            await self.initialize()

        collection = (
            self.CLAIM_EMBEDDINGS if node_type == "claim"
            else self.PROVIDER_PROFILES
        )

        try:
            points = await self.client.retrieve(
                collection_name=collection,
                ids=node_ids,
                with_vectors=True,
                with_payload=False,
            )

            return {
                str(p.id): p.vector
                for p in points
                if p.vector is not None
            }
        except Exception as e:
            logger.error(f"Failed to enrich node features: {str(e)}")
            return {}

    async def get_similar_claims_for_graph(
        self,
        claim_id: str,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Get similar claims for graph neighborhood expansion.
        Used by Graph Service to add semantic edges.
        """
        if not self._initialized:
            await self.initialize()

        # First get the claim's embedding
        point = await self.client.retrieve(
            collection_name=self.CLAIM_EMBEDDINGS,
            ids=[claim_id],
            with_vectors=True,
        )

        if not point or not point[0].vector:
            return []

        # Search for similar claims
        results = await self.semantic_search_claims(
            query_embedding=point[0].vector,
            limit=top_k + 1,  # +1 to exclude self
            score_threshold=0.75,
        )

        # Exclude the query claim itself
        return [
            {"claim_id": r.id, "similarity_score": r.score, "metadata": r.payload}
            for r in results
            if r.id != claim_id
        ][:top_k]

    async def health_check(self) -> Dict[str, Any]:
        """Check Qdrant cluster health."""
        if not self._initialized:
            await self.initialize()

        try:
            collections = await self.client.get_collections()
            cluster_info = await self.client.get_cluster_info()

            return {
                "status": "healthy",
                "collections": len(collections.collections),
                "cluster_info": {
                    "peer_id": cluster_info.peer_id if cluster_info else None,
                    "status": "connected",
                },
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def close(self):
        """Close the client connection."""
        if self.client:
            await self.client.close()
            self._initialized = False


# Global instance
vector_db_service = VectorDBService()