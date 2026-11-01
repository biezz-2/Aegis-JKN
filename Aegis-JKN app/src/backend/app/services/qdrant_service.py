"""Qdrant Vector Database Service for semantic feature retrieval."""
import logging
from typing import List, Dict, Any, Optional, Tuple
from qdrant_client import AsyncQdrantClient, models
from ..core.config import Settings, get_settings

logger = logging.getLogger(__name__)

class QdrantService:
    """
    Service for interacting with Qdrant Vector Database.
    Handles claim embeddings and provider profiles for semantic search.
    """
    _instance: Optional['QdrantService'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QdrantService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    async def initialize(self, settings: Settings):
        """Initialize the async Qdrant client."""
        if self._initialized:
            return

        url = settings.qdrant_url or "http://localhost:6333"
        api_key = settings.qdrant_api_key

        try:
            self.client = AsyncQdrantClient(
                url=url,
                api_key=api_key,
                timeout=settings.qdrant_timeout
            )
            await self._setup_collections()
            self._initialized = True
            logger.info("Qdrant Service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {str(e)}")
            raise e

    async def _setup_collections(self):
        """Create and index collections for claims and providers."""
        collections = {
            "claim_embeddings": models.VectorParams(
                size=768, # Clinical-BERT
                distance=models.Distance.COSINE
            ),
            "provider_profiles": models.VectorParams(
                size=512, # Provider embedding dim
                distance=models.Distance.COSINE
            )
        }

        for name, params in collections.items():
            try:
                # Check if collection exists
                exists = await self.client.collection_exists(name)
                if not exists:
                    await self.client.create_collection(
                        collection_name=name,
                        vectors_config=params
                    )
                    logger.info(f"Created collection: {name}")

                # Setup payload indexing for metadata filters
                if name == "claim_embeddings":
                    # Indexing for claim_type, provider_category, timestamp
                    await self.client.create_payload_index(
                        collection_name=name,
                        field_name="claim_type",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
                    await self.client.create_payload_index(
                        collection_name=name,
                        field_name="provider_category",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
                    await self.client.create_payload_index(
                        collection_name=name,
                        field_name="timestamp",
                        field_schema=models.PayloadSchemaType.INTEGER
                    )
                elif name == "provider_profiles":
                    await self.client.create_payload_index(
                        collection_name=name,
                        field_name="provider_category",
                        field_schema=models.PayloadSchemaType.KEYWORD
                    )
            except Exception as e:
                logger.error(f"Error setting up collection {name}: {str(e)}")

    async def upsert_claim_embedding(self, claim_id: str, vector: List[float], metadata: Dict[str, Any]):
        """Upsert embedding for a new claim."""
        try:
            await self.client.upsert(
                collection_name="claim_embeddings",
                points=models.PointStruct(
                    id=claim_id,
                    vector=vector,
                    payload=metadata
                )
            )
        except Exception as e:
            logger.error(f"Error upserting claim embedding {claim_id}: {str(e)}")
            raise e

    async def semantic_search(self, collection: str, vector: List[float], limit: int = 10, score_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Perform nearest neighbor search with a score threshold."""
        try:
            results = await self.client.search(
                collection_name=collection,
                query_vector=vector,
                limit=limit,
                score_threshold=score_threshold,
                with_payload=True
            )
            return [
                {
                    "id": res.id,
                    "score": res.score,
                    "payload": res.payload
                }
                for res in results
            ]
        except Exception as e:
            logger.error(f"Semantic search error in {collection}: {str(e)}")
            raise e

    async def hybrid_search(self, collection: str, vector: List[float], filter_query: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
        """Perform semantic search combined with metadata filters."""
        try:
            # Construct Qdrant filter from provided query
            # Expected filter_query: {"field": "provider_category", "value": "RS tipe A"}
            q_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key=filter_query["field"],
                        match=models.MatchValue(value=filter_query["value"])
                    )
                ]
            )

            results = await self.client.search(
                collection_name=collection,
                query_vector=vector,
                query_filter=q_filter,
                limit=limit,
                with_payload=True
            )
            return [
                {
                    "id": res.id,
                    "score": res.score,
                    "payload": res.payload
                }
                for res in results
            ]
        except Exception as e:
            logger.error(f"Hybrid search error in {collection}: {str(e)}")
            raise e

# Global instance
qdrant_service = QdrantService()
