"""FalkorDB Connection and Client Setup."""
import redis
from typing import Optional, List
from ..core.config import Settings, get_settings
from .vector_db_service import vector_db_service

class FalkorDBClient:
    """Singleton client for FalkorDB (RedisGraph based)."""
    _instance: Optional['FalkorDBClient'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FalkorDBClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(self, settings: Settings):
        """Initialize the Redis connection for FalkorDB."""
        if self._initialized:
            return

        # FalkorDB typically runs on Redis. We use redis-py.
        # Default fallback if redis_url is not set in config.
        url = settings.redis_url or "redis://localhost:6379"

        # Connection pooling is handled by redis-py internally.
        self.client = redis.from_url(
            url,
            decode_responses=True,
            max_connections=settings.database_pool_size
        )
        self._initialized = True

    async def execute_cypher(self, query: str, params: dict = None):
        """Execute a Cypher query against FalkorDB."""
        # FalkorDB provides the Graph module via Redis.
        # Using the 'graph.query' command.
        try:
            # Note: In a real FalkorDB setup, you might need to specify the graph name.
            # Default graph name is usually 'graph' or specified in settings.
            result = self.client.execute_command('GRAPH.QUERY', 'aegis_graph', query, params)
            return result
        except Exception as e:
            print(f"FalkorDB Query Error: {str(e)}")
            raise e

    async def enrich_node_with_semantic_features(self, node_id: str, node_type: str, vector: List[float]):
        """
        Enriches a graph node with semantic features from Qdrant.
        Integrates Qdrant nearest neighbors to find similar patterns.
        """
        from .qdrant_service import qdrant_service

        collection = "claim_embeddings" if node_type == "claim" else "provider_profiles"

        try:
            # Find top 5 similar nodes
            similar_nodes = await qdrant_service.semantic_search(
                collection=collection,
                vector=vector,
                limit=5,
                score_threshold=0.8
            )

            # Store these as a temporary feature set for the ML model
            # In a real system, this might be a Cypher update to add a 'similar_to' edge
            # or adding a property to the node.
            similar_ids = [res["id"] for res in similar_nodes]

            # Update node in FalkorDB with semantic neighbors
            query = f"MATCH (n {{id: '{node_id}'}}) SET n.semantic_neighbors = {similar_ids}"
            await self.execute_cypher(query)

            return similar_ids
        except Exception as e:
            print(f"Semantic enrichment error for node {node_id}: {str(e)}")
            return []


    async def add_semantic_edges(self, claim_id: str, top_k: int = 5):
        """
        Integrate Vector DB to add semantic edges based on claim similarity.
        Used to enrich the graph with semantic similarity relations.
        """
        try:
            similar_claims = await vector_db_service.get_similar_claims_for_graph(claim_id, top_k=top_k)
            for sim in similar_claims:
                sim_id = sim["claim_id"]
                score = sim["similarity_score"]
                query = (
                    f"MATCH (c1:Claim {{claim_id: '{claim_id}'}}), (c2:Claim {{claim_id: '{sim_id}'}}) "
                    f"MERGE (c1)-[r:SEMANTICALLY_SIMILAR {{score: {score}}}]->(c2)"
                )
                await self.execute_cypher(query)
            return len(similar_claims)
        except Exception as e:
            print(f"Error adding semantic edges: {str(e)}")
            return 0

    def create_graph(self, graph_name: str = "aegis_graph"):
        """Create a new graph if it doesn't exist."""
        try:
            self.client.execute_command('GRAPH.CREATE', graph_name)
        except redis.exceptions.ResponseError as e:
            if "already exists" not in str(e).lower():
                raise e

# Global instance
falkor_db = FalkorDBClient()
