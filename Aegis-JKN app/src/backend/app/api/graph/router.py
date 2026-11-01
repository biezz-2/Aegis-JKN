"""Graph API Endpoints."""
from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from ...core.responses import APIResponse, PaginatedResponse
from ...core.config import Settings, get_settings
from ...services.ml_service import ml_service
from ...services.graph_service import falkor_db
from ...services.graph_schema import GraphSchema

router = APIRouter(prefix="/graph", tags=["Graph Analysis"])

# --- Request Models ---

class GraphQueryRequest(BaseModel):
    """Query for suspicious patterns in the claims graph."""
    claim_id: str = Field(..., description="Claim ID to analyze")
    patient_id: Optional[str] = Field(None, description="Patient ID to center the analysis on")
    provider_id: Optional[str] = Field(None, description="Healthcare provider ID to analyze")
    pattern_type: str = Field("cycle", description="Pattern to search: 'cycle', 'cluster', 'star'")
    max_depth: int = Field(3, ge=1, le=5, description="Max traversal depth for pattern detection")
    min_weight: float = Field(0.1, ge=0.0, le=1.0, description="Minimum edge weight to consider")

class NodeInfo(BaseModel):
    """Basic information about a node in the graph."""
    id: str
    label: str
    type: str # 'Patient', 'Provider', 'Claim', 'Diagnosis'
    properties: dict

class EdgeInfo(BaseModel):
    """Information about an edge connecting two nodes."""
    source: str
    target: str
    weight: float
    relation: str # 'TreatedBy', 'DiagnosedWith', 'LinkedTo'

class GraphQueryResult(BaseModel):
    """Result of a graph pattern query."""
    nodes: List[NodeInfo]
    edges: List[EdgeInfo]
    suspicion_score: float = Field(..., ge=0.0, le=1.0)
    findings: List[str]

class FraudAnalysisResult(BaseModel):
    """Result of MHGSL fraud analysis."""
    claim_id: str
    fraud_probability: float = Field(..., ge=0.0, le=1.0)
    channel_contributions: dict = Field(..., description="Contribution percentage from each MHGSL channel (topology, feature, semantic)")
    risk_level: str = Field(..., description="Risk classification: LOW, MEDIUM, HIGH, CRITICAL")

# --- Endpoints ---

@router.post(
    "/analyze",
    response_model=APIResponse[FraudAnalysisResult],
    summary="Analyze Claim Fraud using MHGSL",
    description="Runs MHGSL inference on the claim graph to compute fraud probability and channel contributions."
)
async def analyze_graph(
    request: GraphQueryRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Implementation of MHGSL fraud detection.
    Queries graph DB for claim subgraph, runs MHGSL inference, returns fraud probability + channel contributions.
    """
    try:
        # TODO: Replace with actual Graph DB query (Neo4j/FalkorDB)
        # Mock graph data for architecture validation
        import torch
        graph_data = {
            'x_dict': {
                'claim': torch.randn(1, 16),
                'provider': torch.randn(1, 8),
                'patient': torch.randn(1, 8),
            },
            'edge_index_dict': {
                ('claim', 'provider'): torch.tensor([[0], [0]], dtype=torch.long),
                ('claim', 'patient'): torch.tensor([[0], [0]], dtype=torch.long),
            }
        }

        fraud_prob, contributions = await ml_service.analyze_fraud(graph_data)

        # Determine risk level
        if fraud_prob >= 0.8:
            risk_level = "CRITICAL"
        elif fraud_prob >= 0.6:
            risk_level = "HIGH"
        elif fraud_prob >= 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return APIResponse(
            success=True,
            data=FraudAnalysisResult(
                claim_id=request.claim_id,
                fraud_probability=fraud_prob,
                channel_contributions=contributions,
                risk_level=risk_level
            ),
            message="MHGSL fraud analysis completed successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph analysis failed: {str(e)}")

@router.get(
    "/analyze",
    response_model=APIResponse[GraphQueryResult],
    summary="Analyze Claim Graph (Legacy Pattern Detection)",
    description="Detects suspicious patterns (cycles, stars, clusters) in the claim graph based on MHGSL theory."
)
async def analyze_graph_legacy(
    query: GraphQueryRequest = Depends(),
    settings: Settings = Depends(get_settings)
):
    """
    Implementation of MHGSL pattern detection.
    Returns a GraphQueryResult containing the subgraph of suspicious activity.
    """
    # TODO: Integrate with Graph Engine (Neo4j/FalkorDB)
    # Mock response for architecture validation
    mock_nodes = [
        NodeInfo(id="P1", label="Patient A", type="Patient", properties={"age": 45}),
        NodeInfo(id="PR1", label="Clinic X", type="Provider", properties={"location": "Jakarta"}),
        NodeInfo(id="C1", label="Claim 101", type="Claim", properties={"amount": 500000}),
    ]
    mock_edges = [
        EdgeInfo(source="P1", target="C1", weight=0.8, relation="Filed"),
        EdgeInfo(source="C1", target="PR1", weight=0.9, relation="ProcessedBy"),
    ]

    return APIResponse(
        success=True,
        data=GraphQueryResult(
            nodes=mock_nodes,
            edges=mock_edges,
            suspicion_score=0.75,
            findings=["Detected high-frequency cycle between Patient A and Clinic X"]
        ),
        message="Graph analysis completed successfully"
    )

@router.get(
    "/nodes",
    response_model=PaginatedResponse[NodeInfo],
    summary="List Graph Nodes",
    description="Retrieve a paginated list of all nodes in the graph."
)
async def list_nodes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    type: Optional[str] = None
):
    # Mock pagination
    return PaginatedResponse(
        success=True,
        data=[NodeInfo(id="N1", label="Node 1", type="Patient", properties={})],
        total_items=100,
        total_pages=5,
        current_page=page,
        page_size=size
    )
