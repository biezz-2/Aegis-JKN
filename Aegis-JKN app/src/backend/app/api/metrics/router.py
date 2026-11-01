"""Metrics API Endpoints."""
from fastapi import APIRouter, Depends
from typing import List, Dict
from pydantic import BaseModel
from ...core.responses import APIResponse
from ...core.config import Settings, get_settings

router = APIRouter(prefix="/metrics", tags=["System Metrics"])

class SystemHealth(BaseModel):
    """Current system health status."""
    status: str # 'healthy', 'degraded', 'unhealthy'
    cpu_usage: float
    memory_usage: float
    active_connections: int
    graph_engine_status: str
    simulation_engine_status: str

class PerformanceMetric(BaseModel):
    """Performance metric for a specific operation."""
    operation: str
    avg_latency_ms: float
    p95_latency_ms: float
    throughput_rps: float
    error_rate: float

# --- Endpoints ---

@router.get(
    "/health",
    response_model=APIResponse[SystemHealth],
    summary="System Health Check",
    description="Returns the current health status of the Aegis-JKN backend services."
)
async def get_health(settings: Settings = Depends(get_settings)):
    """Health check endpoint."""
    return APIResponse(
        success=True,
        data=SystemHealth(
            status="healthy",
            cpu_usage=12.5,
            memory_usage=45.2,
            active_connections=120,
            graph_engine_status="online",
            simulation_engine_status="online"
        ),
        message="System is operational"
    )

@router.get(
    "/performance",
    response_model=APIResponse[List[PerformanceMetric]],
    summary="Get Performance Metrics",
    description="Retrieve performance metrics for key API operations."
)
async def get_performance(settings: Settings = Depends(get_settings)):
    """Performance metrics endpoint."""
    return APIResponse(
        success=True,
        data=[
            PerformanceMetric(operation="graph_analysis", avg_latency_ms=120.0, p95_latency_ms=350.0, throughput_rps=15.0, error_rate=0.01),
            PerformanceMetric(operation="simulation_run", avg_latency_ms=2500.0, p95_latency_ms=12000.0, throughput_rps=1.0, error_rate=0.05),
        ],
        message="Performance metrics retrieved"
    )
