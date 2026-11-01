"""Simulation API Endpoints."""
from fastapi import APIRouter, Depends, BackgroundTasks, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from ...core.responses import APIResponse, PaginatedResponse
from ...core.config import Settings, get_settings
import uuid
from datetime import datetime
from enum import Enum

router = APIRouter(prefix="/simulation", tags=["Fraud Simulation"])

# --- Enums ---

class SimulationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PlatformType(str, Enum):
    TWITTER = "twitter"
    REDDIT = "reddit"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    THREADS = "threads"
    X = "x"

# --- Request Models ---

class SimulationRequest(BaseModel):
    """Configuration for a new fraud detection simulation."""
    iterations: int = Field(1000, ge=100, le=10000, description="Number of simulation iterations")
    platforms: List[PlatformType] = Field(default=[PlatformType.TWITTER, PlatformType.REDDIT], description="Social platforms to simulate")
    ocean_profile: Optional[dict] = Field(None, description="OCEAN personality profile for agents")
    scenario: str = Field("fraud_ring", description="Simulation scenario: 'fraud_ring', 'upcoding', 'phantom_billing'")
    seed: Optional[int] = Field(None, description="Random seed for reproducibility")

class SimulationResult(BaseModel):
    """Results from a completed simulation."""
    simulation_id: str
    status: SimulationStatus
    iterations_completed: int
    total_iterations: int
    fraud_detected_count: int
    false_positive_rate: float
    detection_accuracy: float
    avg_detection_time_ms: float
    created_at: datetime
    completed_at: Optional[datetime] = None
    results_summary: dict

class SimulationStatusResponse(BaseModel):
    """Current status of a running simulation."""
    simulation_id: str
    status: SimulationStatus
    progress_percent: float
    current_iteration: int
    total_iterations: int
    estimated_remaining_seconds: Optional[float]

# In-memory store for demo (replace with Redis/DB in production)
_simulation_store = {}

# --- Endpoints ---

@router.post(
    "/run",
    response_model=APIResponse[SimulationStatusResponse],
    summary="Start Fraud Simulation",
    description="Initiates a multi-platform agent-based simulation to test MHGSL detection algorithms."
)
async def run_simulation(
    request: SimulationRequest,
    background_tasks: BackgroundTasks,
    settings: Settings = Depends(get_settings)
):
    """
    Start a new simulation job.
    Returns immediately with a simulation_id to poll for status.
    """
    sim_id = str(uuid.uuid4())

    # Initialize simulation record
    _simulation_store[sim_id] = {
        "id": sim_id,
        "status": SimulationStatus.PENDING,
        "request": request.dict(),
        "progress": 0,
        "current_iteration": 0,
        "total_iterations": request.iterations,
        "results": None,
        "created_at": datetime.utcnow()
    }

    # Schedule background task
    background_tasks.add_task(run_simulation_background, sim_id, request, settings)

    return APIResponse(
        success=True,
        data=SimulationStatusResponse(
            simulation_id=sim_id,
            status=SimulationStatus.PENDING,
            progress_percent=0.0,
            current_iteration=0,
            total_iterations=request.iterations,
            estimated_remaining_seconds=None
        ),
        message="Simulation queued successfully"
    )

async def run_simulation_background(sim_id: str, request: SimulationRequest, settings: Settings):
    """Background task to run the simulation."""
    sim = _simulation_store[sim_id]
    sim["status"] = SimulationStatus.RUNNING
    sim["started_at"] = datetime.utcnow()

    try:
        # TODO: Integrate with actual Simulation Engine (mirofish-sim-engine)
        # For now, simulate progress
        import asyncio
        for i in range(request.iterations):
            await asyncio.sleep(0.01)  # Simulate work
            sim["current_iteration"] = i + 1
            sim["progress"] = (i + 1) / request.iterations * 100

        # Mock results
        sim["results"] = SimulationResult(
            simulation_id=sim_id,
            status=SimulationStatus.COMPLETED,
            iterations_completed=request.iterations,
            total_iterations=request.iterations,
            fraud_detected_count=int(request.iterations * 0.15),
            false_positive_rate=0.08,
            detection_accuracy=0.92,
            avg_detection_time_ms=45.5,
            created_at=sim["created_at"],
            completed_at=datetime.utcnow(),
            results_summary={"scenario": request.scenario, "platforms": [p.value for p in request.platforms]}
        )
        sim["status"] = SimulationStatus.COMPLETED
        sim["completed_at"] = datetime.utcnow()

    except Exception as e:
        sim["status"] = SimulationStatus.FAILED
        sim["error"] = str(e)
        sim["completed_at"] = datetime.utcnow()

@router.get(
    "/{simulation_id}/status",
    response_model=APIResponse[SimulationStatusResponse],
    summary="Get Simulation Status",
    description="Poll for the current status of a running simulation."
)
async def get_simulation_status(simulation_id: str):
    """Get real-time status of a simulation."""
    sim = _simulation_store.get(simulation_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    return APIResponse(
        success=True,
        data=SimulationStatusResponse(
            simulation_id=sim["id"],
            status=sim["status"],
            progress_percent=sim["progress"],
            current_iteration=sim["current_iteration"],
            total_iterations=sim["total_iterations"],
            estimated_remaining_seconds=None
        ),
        message="Status retrieved"
    )

@router.get(
    "/{simulation_id}/results",
    response_model=APIResponse[SimulationResult],
    summary="Get Simulation Results",
    description="Retrieve the full results of a completed simulation."
)
async def get_simulation_results(simulation_id: str):
    """Get results of a completed simulation."""
    sim = _simulation_store.get(simulation_id)
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")

    if sim["status"] != SimulationStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Simulation not yet completed")

    return APIResponse(
        success=True,
        data=sim["results"],
        message="Results retrieved successfully"
    )

@router.get(
    "/history",
    response_model=PaginatedResponse[SimulationResult],
    summary="List Simulation History",
    description="Get a paginated list of all past simulations."
)
async def list_simulations(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    status: Optional[SimulationStatus] = None
):
    """List past simulations with optional status filter."""
    all_sims = [
        sim["results"] for sim in _simulation_store.values()
        if sim["results"] and (not status or sim["results"].status == status)
    ]

    # Simple pagination
    start = (page - 1) * size
    end = start + size
    paginated = all_sims[start:end]

    return PaginatedResponse(
        success=True,
        data=paginated,
        total_items=len(all_sims),
        total_pages=(len(all_sims) + size - 1) // size,
        current_page=page,
        page_size=size
    )