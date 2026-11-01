"""Graph database schema and query management for Aegis-JKN."""
from .graph_service import falkor_db

class GraphSchema:
    """Defines the FalkorDB schema and common queries."""

    # --- Node Labels ---
    NODE_PROVIDER = "Provider"
    NODE_PATIENT = "Patient"
    NODE_CLAIM = "Claim"
    NODE_DOCTOR = "Doctor"

    # --- Edge Types ---
    EDGE_CLAIMS_AT = "CLAIMS_AT"       # Claim -> Provider
    EDGE_REFERRED_TO = "REFERRED_TO"   # Provider -> Provider
    EDGE_SHARED_PATIENT = "SHARED_PATIENT" # Provider -> Provider
    EDGE_COLOCATED = "COLOCATED"       # Provider -> Provider

    @staticmethod
    async def setup_schema():
        """Initialize indexes and constraints for fast filtering."""
        # FalkorDB/RedisGraph uses indices automatically for some properties,
        # but we explicitly ensure properties used in filters are optimized.
        # Note: RedisGraph/FalkorDB doesn't use 'CREATE INDEX' exactly like Neo4j,
        # but we ensure the properties are present.

        queries = [
            # Sample constraints/indexes if supported by specific FalkorDB version
            # "CREATE INDEX ON :Claim(claim_id)",
            # "CREATE INDEX ON :Provider(provider_id)",
            # "CREATE INDEX ON :Patient(patient_id)",
        ]
        for q in queries:
            await falkor_db.execute_cypher(q)

    # --- Implementation of Required Cypher Queries ---

    @staticmethod
    async def get_2hop_neighborhood(claim_id: str):
        """1. 2-hop neighborhood from Claim node."""
        query = (
            f"MATCH (c:Claim {{claim_id: '{claim_id}'}}) "
            f"-[*1..2]-(neighbor) "
            f"RETURN neighbor, relationships(c)" # simplified for example
        )
        # Better Cypher:
        query = (
            "MATCH (c:Claim {claim_id: $claim_id}) "
            "MATCH (c)-[r1]-(n1)-[r2]-(n2) "
            "RETURN c, r1, n1, r2, n2"
        )
        return await falkor_db.execute_cypher(query, {"claim_id": claim_id})

    @staticmethod
    async def get_path_between_providers(prov_a: str, prov_b: str):
        """2. Path between Provider A and Provider B (max 3 hops)."""
        query = (
            "MATCH (p1:Provider {provider_id: $id_a}), (p2:Provider {provider_id: $id_b}) "
            "MATCH path = shortestPath((p1)-[*..3]-(p2)) "
            "RETURN path"
        )
        return await falkor_db.execute_cypher(query, {"id_a": prov_a, "id_b": prov_b})

    @staticmethod
    async def get_aggregated_risk_score(cluster_id: str):
        """3. Aggregated risk score per Provider cluster."""
        # Assuming cluster_id is a property on Provider nodes or a cluster label
        query = (
            "MATCH (p:Provider) WHERE p.cluster_id = $cluster_id "
            "RETURN avg(p.risk_score) as avg_risk, sum(p.risk_score) as total_risk, count(p) as size"
        )
        return await falkor_db.execute_cypher(query, {"cluster_id": cluster_id})
