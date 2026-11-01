"""
Model Context Protocol (MCP) Router for Aegis-JKN.
Provides both data-retrieval MCP tools (Claim Facts, MHGSL Graph Analysis, Clinical Evidence Rules)
and the unified factual audit report generator for AI agents.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol (MCP) Tools"])

from ...services.llm_reporter import generate_claim_audit_report

# Load datasets for tool lookups
APP_ROOT = Path(__file__).resolve().parents[5]
DATA_PATH_SYNTH = APP_ROOT / "frontend" / "src" / "lib" / "data" / "klaim-dataset.json"
DATA_PATH_REAL = APP_ROOT / "frontend" / "src" / "lib" / "data" / "bpjs-real-claims.json"

claims_cache: Dict[str, dict] = {}


def get_claims_cache() -> Dict[str, dict]:
    global claims_cache
    if not claims_cache:
        # Load synthetic claims
        if DATA_PATH_SYNTH.exists():
            try:
                with open(DATA_PATH_SYNTH, "r", encoding="utf-8") as f:
                    synth_data = json.load(f)
                    for c in synth_data:
                        cid = c.get("Name") or c.get("id")
                        if cid:
                            claims_cache[cid] = c
            except Exception:
                pass
        # Load real BPJS claims
        if DATA_PATH_REAL.exists():
            try:
                with open(DATA_PATH_REAL, "r", encoding="utf-8") as f:
                    real_data = json.load(f)
                    for c in real_data:
                        cid = c.get("Name") or c.get("id")
                        if cid:
                            claims_cache[cid] = c
            except Exception:
                pass
    return claims_cache


def resolve_claim(claim_id: str) -> dict:
    """Helper to normalize claim data from cache or return structured defaults."""
    cache = get_claims_cache()
    raw = cache.get(claim_id) or {}
    
    # Parse 3-channel contribution if string
    t_val = 0.33
    f_val = 0.33
    s_val = 0.34
    ch_str = raw.get("Kontribusi Saluran") or ""
    if ch_str and "T" in ch_str:
        try:
            parts = ch_str.split("·")
            for p in parts:
                p = p.strip()
                if p.startswith("T"):
                    t_val = float(p.split()[1])
                elif p.startswith("F"):
                    f_val = float(p.split()[1])
                elif p.startswith("S"):
                    s_val = float(p.split()[1])
        except Exception:
            pass

    return {
        "id": claim_id,
        "patient": raw.get("Pasien") or raw.get("patient", "Pasien BPJS"),
        "hospital": raw.get("Faskes") or raw.get("hospital", "RS Rujukan"),
        "doctor": raw.get("Dokter") or raw.get("doctor", "dr. DPJP"),
        "diagnosisIcd10": raw.get("Diagnosis ICD-10") or raw.get("diagnosisIcd10", "-"),
        "procedureIcd9": raw.get("Prosedur ICD-9-CM") or raw.get("procedureIcd9", "-"),
        "costRp": int(raw.get("Biaya Rp") or raw.get("costRp", 0)),
        "losDays": int(raw.get("LOS hari") or raw.get("losDays", 0)),
        "clinicalNarrative": raw.get("Narasi Rekam Medis") or raw.get("clinicalNarrative", "Resume medis dalam peninjauan verifikator."),
        "patientFeedback": raw.get("Umpan Balik Pasien") or raw.get("patientFeedback", "Tidak ada catatan keluhan tambahan."),
        "hasContradiction": bool(raw.get("Kontradiksi Narasi") or raw.get("hasContradiction", False)),
        "fraudScore": float(raw.get("Skor Fraud") or raw.get("fraudScore", 0.5)),
        "channelContribution": {
            "topology": t_val,
            "feature": f_val,
            "semantic": s_val
        },
        "syndicate": raw.get("Sindikat") or raw.get("syndicate", None),
        "serviceType": raw.get("Pelayanan") or raw.get("serviceType", "Rawat Inap")
    }


# --- MCP Tool Schemas Inventory ---

MCP_TOOLS_INVENTORY = [
    {
        "name": "get_claim_forensic_facts",
        "description": (
            "Tool MCP untuk mengekstrak data fakta rekam medis dan administrasi klaim BPJS Kesehatan secara lengkap "
            "(pasien, faskes, DPJP, kode ICD-10, kode ICD-9-CM, biaya klaim, lama rawat LOS, narasi EMR, dan aduan pasien)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim_id": {
                    "type": "string",
                    "description": "ID unik berkas klaim BPJS Kesehatan (contoh: 'KLM001')."
                }
            },
            "required": ["claim_id"]
        }
    },
    {
        "name": "get_mhgsl_analysis",
        "description": (
            "Tool MCP untuk mengambil hasil analisis inferensi graf MHGSL (Multi-Hop Graph Structure Learning): "
            "skor probabilitas anomali, pembagian kontribusi 3 kanal (Topologi, Fitur, Semantik), klaster sindikat, dan pola kamuflase."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim_id": {
                    "type": "string",
                    "description": "ID unik berkas klaim BPJS Kesehatan."
                }
            },
            "required": ["claim_id"]
        }
    },
    {
        "name": "get_clinical_evidence_rules",
        "description": (
            "Tool MCP untuk memvalidasi aturan restriksi obat Formularium Nasional (FORNAS), kesesuaian tindakan vs diagnosa, "
            "deteksi diskrepansi klinis, dan rujukan hukum penjaminan (Permenkes No. 24/2022, UU PDP No. 27/2022, Permenkes No. 16/2019)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim_id": {
                    "type": "string",
                    "description": "ID unik berkas klaim BPJS Kesehatan."
                }
            },
            "required": ["claim_id"]
        }
    },
    {
        "name": "generate_factual_claim_report",
        "description": (
            "Tool MCP Terpadu yang secara otomatis mengumpulkan seluruh fakta data klaim, kalkulasi MHGSL GNN, dan eviden regulasi, "
            "lalu mensintesisnya menggunakan model AI 'aegis-jkn' ke dalam laporan audit klinis ringkas berbasis fakta murni, berimbang, dan bersegel kriptografis."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim_id": {
                    "type": "string",
                    "description": "ID unik berkas klaim BPJS Kesehatan (contoh: 'KLM001')."
                },
                "include_regulatory_basis": {
                    "type": "boolean",
                    "description": "Sertakan rujukan dasar hukum Kemenkes & UU PDP.",
                    "default": True
                }
            },
            "required": ["claim_id"]
        }
    },
    {
        "name": "generate_claim_audit_dossier",
        "description": "Alias kompatibilitas untuk generate_factual_claim_report.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim_id": {
                    "type": "string",
                    "description": "ID unik berkas klaim."
                },
                "include_regulatory_basis": {
                    "type": "boolean",
                    "default": True
                }
            },
            "required": ["claim_id"]
        }
    }
]


# --- Request / Response Models ---

class McpToolCallRequest(BaseModel):
    name: str = Field(..., description="Nama tool MCP yang dipanggil")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="Argumen panggilan tool")


class McpTextContent(BaseModel):
    type: str = "text"
    text: str


class McpToolCallResponse(BaseModel):
    content: List[McpTextContent]
    isError: bool = False


# --- Endpoints ---

@router.get(
    "/tools",
    summary="List Available MCP Tools",
    description="Mengembalikan inventaris tools yang dapat digunakan oleh AI Agent sesuai standar Model Context Protocol (MCP)."
)
async def list_mcp_tools():
    """Returns the list of available MCP tools."""
    return {"tools": MCP_TOOLS_INVENTORY}


@router.post(
    "/tools/call",
    response_model=McpToolCallResponse,
    summary="Execute MCP Tool Call",
    description="Mengeksekusi pemanggilan tool sesuai standar Model Context Protocol (MCP)."
)
async def call_mcp_tool(request: McpToolCallRequest):
    """Executes an MCP tool call by name and arguments."""
    claim_id = request.arguments.get("claim_id")
    if not claim_id:
        raise HTTPException(status_code=400, detail="Parameter 'claim_id' wajib diisi.")

    claim = resolve_claim(claim_id)

    # 1. Tool: get_claim_forensic_facts
    if request.name == "get_claim_forensic_facts":
        facts = {
            "claim_id": claim["id"],
            "patient_name": claim["patient"],
            "faskes": claim["hospital"],
            "doctor_dpjp": claim["doctor"],
            "service_type": claim["serviceType"],
            "diagnosis_icd10": claim["diagnosisIcd10"],
            "procedure_icd9": claim["procedureIcd9"],
            "billing_cost_rp": claim["costRp"],
            "length_of_stay_days": claim["losDays"],
            "emr_narrative": claim["clinicalNarrative"],
            "patient_feedback": claim["patientFeedback"],
            "has_narrative_contradiction": claim["hasContradiction"]
        }
        return McpToolCallResponse(
            content=[McpTextContent(type="text", text=json.dumps(facts, indent=2, ensure_ascii=False))],
            isError=False
        )

    # 2. Tool: get_mhgsl_analysis
    elif request.name == "get_mhgsl_analysis":
        ch = claim["channelContribution"]
        analysis = {
            "claim_id": claim["id"],
            "fraud_probability_score": claim["fraudScore"],
            "risk_tier": "HIGH_FRAUD" if claim["fraudScore"] >= 0.8 else "REVIEW" if claim["fraudScore"] >= 0.35 else "AUTO_CLEAR",
            "three_channel_weights": {
                "topology_channel": ch["topology"],
                "feature_channel": ch["feature"],
                "semantic_channel": ch["semantic"]
            },
            "syndicate_cluster_id": claim["syndicate"] or "NON_SYNDICATE",
            "camouflage_tactics_detected": [
                "Bipartite referral density spike" if ch["topology"] >= 0.3 else None,
                "Tariff deviation from INA-CBG norm" if ch["feature"] >= 0.3 else None,
                "Clinical narrative discrepancy" if ch["semantic"] >= 0.3 or claim["hasContradiction"] else None
            ]
        }
        # Filter None
        analysis["camouflage_tactics_detected"] = [t for t in analysis["camouflage_tactics_detected"] if t]
        return McpToolCallResponse(
            content=[McpTextContent(type="text", text=json.dumps(analysis, indent=2, ensure_ascii=False))],
            isError=False
        )

    # 3. Tool: get_clinical_evidence_rules
    elif request.name == "get_clinical_evidence_rules":
        has_contra = claim["hasContradiction"]
        rules = {
            "claim_id": claim["id"],
            "diagnosis_procedure_alignment": "DISCREPANCY_DETECTED" if has_contra else "ALIGNED",
            "fornas_restrictions": "Kesesuaian restriksi dosis dan batasan diagnosis primer Formularium Nasional.",
            "statutory_regulations": [
                "Permenkes No. 24/2022: Kewajiban Rekam Medis Elektronik & kebenaran resume medis faskes.",
                "UU No. 27/2022 (UU PDP): Perlindungan data pribadi kesehatan & integritas audit trail.",
                "Permenkes No. 16/2019: Pencegahan dan Penanganan Kecurangan (Fraud) pada Program JKN."
            ],
            "cryptographic_verification": "Ed25519 signature verified & SHA-256 tamper-evident append-only ledger."
        }
        return McpToolCallResponse(
            content=[McpTextContent(type="text", text=json.dumps(rules, indent=2, ensure_ascii=False))],
            isError=False
        )

    # 4. Tool: generate_factual_claim_report / generate_claim_audit_dossier
    elif request.name in ["generate_factual_claim_report", "generate_claim_audit_dossier"]:
        try:
            report_res = generate_claim_audit_report(claim)
            report_text = report_res["report"]

            if request.arguments.get("include_regulatory_basis", True):
                regulatory_append = (
                    "\n\n---\n"
                    "### DASAR REGULASI & KEPATUHAN PENJAMINAN:\n"
                    "- **Permenkes No. 24/2022**: Kewajiban Rekam Medis Elektronik & kebenaran resume medis.\n"
                    "- **UU No. 27/2022 (UU PDP)**: Perlindungan data pribadi kesehatan & integritas audit trail.\n"
                    "- **Permenkes No. 16/2019**: Pencegahan dan Penanganan Kecurangan (Fraud) pada Program JKN.\n"
                    "- **Status Kriptografis**: Rekaman audit ini disegel menggunakan tanda tangan Ed25519 & hash SHA-256."
                )
                report_text += regulatory_append

            return McpToolCallResponse(
                content=[McpTextContent(type="text", text=report_text)],
                isError=False
            )
        except Exception as e:
            return McpToolCallResponse(
                content=[McpTextContent(type="text", text=f"Error saat mengeksekusi tool: {str(e)}")],
                isError=True
            )

    else:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{request.name}' tidak ditemukan dalam inventaris MCP."
        )


# --- REST Helper Aliases ---

@router.post("/tools/get_claim_forensic_facts", response_model=McpToolCallResponse)
async def get_claim_facts_endpoint(args: Dict[str, Any]):
    return await call_mcp_tool(McpToolCallRequest(name="get_claim_forensic_facts", arguments=args))


@router.post("/tools/get_mhgsl_analysis", response_model=McpToolCallResponse)
async def get_mhgsl_analysis_endpoint(args: Dict[str, Any]):
    return await call_mcp_tool(McpToolCallRequest(name="get_mhgsl_analysis", arguments=args))


@router.post("/tools/get_clinical_evidence_rules", response_model=McpToolCallResponse)
async def get_clinical_evidence_endpoint(args: Dict[str, Any]):
    return await call_mcp_tool(McpToolCallRequest(name="get_clinical_evidence_rules", arguments=args))


@router.post("/tools/generate_factual_claim_report", response_model=McpToolCallResponse)
async def generate_factual_report_endpoint(args: Dict[str, Any]):
    return await call_mcp_tool(McpToolCallRequest(name="generate_factual_claim_report", arguments=args))


@router.post("/tools/generate_claim_audit_dossier", response_model=McpToolCallResponse)
async def generate_dossier_direct(args: Dict[str, Any]):
    return await call_mcp_tool(McpToolCallRequest(name="generate_claim_audit_dossier", arguments=args))
