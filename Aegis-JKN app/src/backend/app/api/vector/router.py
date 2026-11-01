"""Qdrant Vector Database API Router."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from ...services.qdrant_service import qdrant_service

router = APIRouter(prefix="/vector", tags=["Vector Database"])


class VectorUpsertRequest(BaseModel):
    """Request model for upserting a vector."""
    id: str
    vector: List[float]
    metadata: Dict[str, Any]


class SemanticSearchRequest(BaseModel):
    """Request model for semantic search."""
    collection: str
    vector: List[float]
    limit: int = 10
    score_threshold: float = 0.7


class HybridSearchRequest(BaseModel):
    """Request model for hybrid search with metadata filters."""
    collection: str
    vector: List[float]
    filter_field: str
    filter_value: str
    limit: int = 10


class SearchResponse(BaseModel):
    """Response model for search results."""
    id: str
    score: float
    payload: Dict[str, Any]


@router.post("/upsert", summary="Upsert a vector embedding")
async def upsert_vector(request: VectorUpsertRequest):
    """
    Upsert a vector embedding with metadata.
    Collections: claim_embeddings (768-dim), provider_profiles (512-dim)
    """
    try:
        await qdrant_service.upsert_claim_embedding(request.id, request.vector, request.metadata)
        return {"status": "success", "message": f"Upserted vector for {request.id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/semantic", response_model=List[SearchResponse], summary="Semantic nearest neighbor search")
async def semantic_search(request: SemanticSearchRequest):
    """
    Perform semantic nearest neighbor search with score threshold.

    Collections:
    - claim_embeddings (768-dim Clinical-BERT)
    - provider_profiles (512-dim)
    """
    try:
        results = await qdrant_service.semantic_search(
            collection=request.collection,
            vector=request.vector,
            limit=request.limit,
            score_threshold=request.score_threshold
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search/hybrid", response_model=List[SearchResponse], summary="Hybrid semantic + metadata filter search")
async def hybrid_search(request: HybridSearchRequest):
    """
    Perform hybrid search combining semantic similarity with metadata filters.

    Example: Find similar claims where provider_category = "RS tipe A"
    """
    try:
        results = await qdrant_service.hybrid_search(
            collection=request.collection,
            vector=request.vector,
            filter_query={"field": request.filter_field, "value": request.filter_value},
            limit=request.limit
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections", summary="List available collections")
async def list_collections():
    """List all available collections in Qdrant."""
    try:
        collections = await qdrant_service.client.get_collections()
        return {"collections": [c.name for c in collections.collections]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))