"""
API Router for monitoring batch jobs and async workers.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

# In a real scenario, this would be a DB-backed store (e.g. PostgreSQL or Redis)
# For now, we use a simple in-memory store to track job status
# ponytail: Use PostgreSQL 'job_execution_log' table to track jobs across restarts.
JOB_STATUS_STORE: Dict[str, Dict[str, Any]] = {}

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    progress: float
    result_summary: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

router = APIRouter(
    prefix="/jobs",
    tags=["Async Jobs"]
)

@router.get("/", response_model=List[JobStatusResponse])
async def list_jobs():
    """List all recent batch jobs."""
    return [JobStatusResponse(**job) for job in JOB_STATUS_STORE.values()]

@router.get("/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get detailed status of a specific job."""
    if job_id not in JOB_STATUS_STORE:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatusResponse(**JOB_STATUS_STORE[job_id])

@router.post("/trigger/{pipeline_id}")
async def trigger_job(pipeline_id: str):
    """
    Trigger a batch pipeline.
    In production, this would call the Argo Workflow API or a Kubernetes job.
    """
    # Mock trigger
    import uuid
    job_id = str(uuid.uuid4())
    JOB_STATUS_STORE[job_id] = {
        "job_id": job_id,
        "status": "PENDING",
        "start_time": datetime.utcnow(),
        "end_time": None,
        "progress": 0.0,
        "result_summary": None,
        "error": None,
    }

    # ponytail: Integrate with Argo Workflow SDK to submit the YAML from deploy/argo/
    return {"job_id": job_id, "message": f"Pipeline {pipeline_id} triggered successfully"}
