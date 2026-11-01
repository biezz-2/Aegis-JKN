"""
FHIR R4 Resource Mapping Layer for Aegis-JKN.
Implements Pydantic models for local FHIR R4 resource mapping.
"""
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator
import uuid

# --- FHIR Enums ---

class ClaimStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    DRAFT = "draft"
    ENTERED_IN_ERROR = "entered-in-error"

class PatientGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"

class OrganizationType(str, Enum):
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    PHARMACY = "pharmacy"
    LAB = "laboratory"
    OTHER = "other"

# --- Common FHIR Elements ---

class FHIRIdentifier(BaseModel):
    system: str
    value: str
    use: str = "official"
    type_code: Optional[str] = None

class FHIRHumanName(BaseModel):
    use: str = "official"
    family: str = ""
    given: List[str] = Field(default_factory=list)

class FHIRAddress(BaseModel):
    use: str = "home"
    type: str = "both"
    city: str = ""
    postal_code: str = ""
    country: str = "ID"

class FHIRCodeableConcept(BaseModel):
    coding: List[Dict[str, str]] = Field(default_factory=list)
    text: str = ""

class FHIRQuantity(BaseModel):
    value: float
    unit: str
    system: str = "http://unitsofmeasure.org"
    code: str = ""

# --- FHIR Resources ---

class FHIRBaseResource(BaseModel):
    resourceType: str
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    meta: Dict[str, Any] = Field(default_factory=lambda: {
        "versionId": "1",
        "lastUpdated": datetime.utcnow().isoformat() + "Z"
    })
    identifier: List[FHIRIdentifier] = Field(default_factory=list)

class FHIRPatient(FHIRBaseResource):
    resourceType: str = "Patient"
    name: List[FHIRHumanName] = Field(default_factory=list)
    gender: PatientGender = PatientGender.UNKNOWN
    birthDate: Optional[str] = None
    address: List[FHIRAddress] = Field(default_factory=list)
    active: bool = True

class FHIRPractitioner(FHIRBaseResource):
    resourceType: str = "Practitioner"
    name: List[FHIRHumanName] = Field(default_factory=list)
    gender: PatientGender = PatientGender.UNKNOWN
    active: bool = True

class FHIROrganization(FHIRBaseResource):
    resourceType: str = "Organization"
    name: str = ""
    active: bool = True
    type_: List[FHIRCodeableConcept] = Field(default_factory=list, alias="type")

    class Config:
        allow_population_by_field_name = True

class FHIRClaim(FHIRBaseResource):
    resourceType: str = "Claim"
    status: ClaimStatus = ClaimStatus.ACTIVE
    use: str = "claim"
    patient: Dict[str, str] = Field(..., description="Reference to Patient resource")
    created: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    insurer: Dict[str, str] = Field(..., description="Reference to Organization resource")
    provider: Dict[str, str] = Field(..., description="Reference to Organization resource")
    diagnosis: List[Dict[str, Any]] = Field(default_factory=list)
    item: List[Dict[str, Any]] = Field(default_factory=list)
    total: Optional[FHIRQuantity] = None

class FHIRBundle(BaseModel):
    resourceType: str = "Bundle"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str = "collection"
    total: int = 0
    entry: List[Dict[str, Any]] = Field(default_factory=list)

    def add_resource(self, resource: FHIRBaseResource):
        self.entry.append({
            "fullUrl": f"urn:uuid:{resource.id}",
            "resource": resource.dict()
        })
        self.total = len(self.entry)

# --- Mapping Logic ---

class FHIRMapper:
    """Service to map internal domain models to FHIR R4."""

    @staticmethod
    def map_patient(internal_patient: Any) -> FHIRPatient:
        # internal_patient expected to be a SQLAlchemy model or dict
        return FHIRPatient(
            id=str(getattr(internal_patient, 'id', str(uuid.uuid4()))),
            identifier=[FHIRIdentifier(system="JKN-ID", value=getattr(internal_patient, 'patient_id', ''))],
            name=[FHIRHumanName(family=getattr(internal_patient, 'name', ''))],
            gender=PatientGender.MALE if getattr(internal_patient, 'gender', '').lower() == 'male' else PatientGender.UNKNOWN,
            birthDate=str(getattr(internal_patient, 'dob', '')),
            active=True
        )

    @staticmethod
    def map_provider(internal_provider: Any) -> FHIROrganization:
        return FHIROrganization(
            id=str(getattr(internal_provider, 'id', str(uuid.uuid4()))),
            identifier=[FHIRIdentifier(system="JKN-PROV", value=getattr(internal_provider, 'provider_id', ''))],
            name=getattr(internal_provider, 'name', ''),
            type_=[FHIRCodeableConcept(text=getattr(internal_provider, 'type', 'Hospital'))],
            active=True
        )

    @staticmethod
    def map_claim(internal_claim: Any, patient_fhir_id: str, provider_fhir_id: str) -> FHIRClaim:
        return FHIRClaim(
            id=str(getattr(internal_claim, 'id', str(uuid.uuid4()))),
            identifier=[FHIRIdentifier(system="JKN-CLAIM", value=getattr(internal_claim, 'claim_id', ''))],
            patient={"reference": f"Patient/{patient_fhir_id}"},
            provider={"reference": f"Organization/{provider_fhir_id}"},
            insurer={"reference": "Organization/BPJS-Kesehatan"},
            total=FHIRQuantity(value=getattr(internal_claim, 'amount', 0.0), unit="IDR") if getattr(internal_claim, 'amount', 0) else None
        )
