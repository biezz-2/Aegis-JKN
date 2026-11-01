"""Report API Endpoints."""
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from ...core.responses import APIResponse, PaginatedResponse
from ...core.config import Settings, get_settings
from ...services.llm_reporter import generate_claim_audit_report

router = APIRouter(prefix="/report", tags=["Fraud Reporting"])

class ClaimExplanationRequest(BaseModel):
    claim_id: str
    hospital: Optional[str] = None
    doctor: Optional[str] = None
    diagnosis_icd10: str
    procedure_icd9: Optional[str] = None
    cost_rp: float = 0.0
    los_days: int = 0
    clinical_narrative: Optional[str] = None
    patient_feedback: Optional[str] = None
    has_contradiction: bool = False
    fraud_score: float = 0.5
    topology_score: float = 0.33
    feature_score: float = 0.33
    semantic_score: float = 0.34

# --- Request Models ---

class ReportRequest(BaseModel):
    """Query for fraud intelligence reports."""
    time_range: str = Field("last_30_days", description="Time range: 'last_7_days', 'last_30_days', 'last_90_days', 'custom'")
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    filter_by: Optional[str] = Field(None, description="Filter by 'region', 'hospital', 'provider_type'")
    detail_level: str = Field("summary", description="Detail level: 'summary', 'detailed', 'forensic'")

class FraudFinding(BaseModel):
    """A single fraud finding from a report."""
    finding_id: str
    severity: str # 'Low', 'Medium', 'High', 'Critical'
    description: str
    confidence_score: float
    evidence_nodes: List[str] # IDs of graph nodes as evidence
    recommendation: str

class ReportSummary(BaseModel):
    """Summary of a fraud intelligence report."""
    report_id: str
    total_suspicious_claims: int
    estimated_loss: float
    high_risk_clusters: int
    findings: List[FraudFinding]
    generated_at: str

# --- Endpoints ---

@router.post(
    "/generate",
    response_model=APIResponse[ReportSummary],
    summary="Generate Fraud Report",
    description="Generates a fraud intelligence report using ReACT reasoning over the detected graph patterns."
)
async def generate_report(
    request: ReportRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Generates an intelligence report.
    Integrates with ReportAgent for analytic reasoning.
    """
    # Mock result
    return APIResponse(
        success=True,
        data=ReportSummary(
            report_id="REP-2026-001",
            total_suspicious_claims=142,
            estimated_loss=1250000000.0,
            high_risk_clusters=5,
            findings=[
                FraudFinding(
                    finding_id="F1",
                    severity="High",
                    description="Detected coordinated billing ring across 3 hospitals in Central Jakarta",
                    confidence_score=0.88,
                    evidence_nodes=["P1", "PR1", "C1"],
                    recommendation="Initiate immediate forensic audit for these providers"
                )
            ],
            generated_at="2026-10-23T10:00:00Z"
        ),
        message="Report generated successfully"
    )

@router.get(
    "/history",
    response_model=PaginatedResponse[ReportSummary],
    summary="List Report History",
    description="Retrieve a list of previously generated reports."
)
async def list_reports(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50)
):
    return PaginatedResponse(
        success=True,
        data=[],
        total_items=0,
        total_pages=0,
        current_page=page,
        page_size=size
    )

@router.post(
    "/generate-claim-explanation",
    response_model=APIResponse[dict],
    summary="Generate Clinical Audit Explanation (Model: aegis-jkn)",
    description="Generates an expert clinical audit report analyzing ICD-10 vs ICD-9 discrepancies and narrative contradictions using the aegis-jkn model."
)
async def generate_explanation_endpoint(request: ClaimExplanationRequest):
    claim_dict = {
        "id": request.claim_id,
        "hospital": request.hospital,
        "doctor": request.doctor,
        "diagnosisIcd10": request.diagnosis_icd10,
        "procedureIcd9": request.procedure_icd9,
        "costRp": request.cost_rp,
        "losDays": request.los_days,
        "clinicalNarrative": request.clinical_narrative,
        "patientFeedback": request.patient_feedback,
        "hasContradiction": request.has_contradiction,
        "fraudScore": request.fraud_score,
    }
    scores_dict = {
        "topology": request.topology_score,
        "feature": request.feature_score,
        "semantic": request.semantic_score,
        "fraud_score": request.fraud_score,
    }
    try:
        result = generate_claim_audit_report(claim_dict, scores_dict)
        return APIResponse(
            success=True,
            data=result,
            message="Laporan audit klinis berhasil dihasilkan oleh model aegis-jkn."
        )
    except Exception as e:
        return APIResponse(
            success=False,
            data={"error": str(e)},
            message=f"Gagal memanggil model aegis-jkn: {str(e)}"
        )
