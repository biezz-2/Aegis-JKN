"""
FHIR R4 Resource Mapping Layer for Aegis-JKN.
Maps internal claim/patient/provider data to FHIR R4 standard resources.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid


class ClaimStatus(str, Enum):
    """FHIR Claim.status values."""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    DRAFT = "draft"
    ENTERED_IN_ERROR = "entered-in-error"


class ClaimUse(str, Enum):
    """FHIR Claim.use values."""
    CLAIM = "claim"
    PREAUTHORIZATION = "preauthorization"
    PREAUTHORIZATION = "preauthorization"


class PatientGender(str, Enum):
    """FHIR Patient.gender values (AdministrativeGender)."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class OrganizationType(str, Enum):
    """Organization type codes."""
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    PHARMACY = "pharmacy"
    LAB = "laboratory"
    OTHER = "other"


@dataclass
class FHIRIdentifier:
    """FHIR Identifier element."""
    system: str
    value: str
    use: str = "official"
    type_code: Optional[str] = None
    period_start: Optional[str] = None
    period_end: Optional[str] = None


@dataclass
class FHIRHumanName:
    """FHIR HumanName element."""
    use: str = "official"
    family: str = ""
    given: List[str] = field(default_factory=list)
    prefix: List[str] = field(default_factory=list)
    suffix: List[str] = field(default_factory=list)


@dataclass
class FHIRAddress:
    """FHIR Address element."""
    use: str = "home"
    type: str = "both"
    text: str = ""
    line: List[str] = field(default_factory=list)
    city: str = ""
    district: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = "ID"


@dataclass
class FHIRContactPoint:
    """FHIR ContactPoint element."""
    system: str = "phone"
    value: str = ""
    use: str = "home"
    rank: int = 1


@dataclass
class FHIRCodeableConcept:
    """FHIR CodeableConcept element."""
    coding: List[Dict[str, str]] = field(default_factory=list)
    text: str = ""


@dataclass
class FHIRQuantity:
    """FHIR Quantity element."""
    value: float
    unit: str
    system: str = "http://unitsofmeasure.org"
    code: str = ""


class FHIRResource:
    """Base FHIR Resource class."""

    def __init__(self, resource_type: str, id: Optional[str] = None):
        self.resource_type = resource_type
        self.id = id or str(uuid.uuid4())
        self.meta = {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z",
            "profile": []
        }
        self.identifier: List[FHIRIdentifier] = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to FHIR JSON dict."""
        result = {
            "resourceType": self.resource_type,
            "id": self.id,
            "meta": self.meta,
        }
        if self.identifier:
            result["identifier"] = [
                {
                    "use": i.use,
                    "system": i.system,
                    "value": i.value,
                    "type": {"coding": [{"code": i.type_code}]} if i.type_code else None,
                    "period": {
                        "start": i.period_start,
                        "end": i.period_end
                    } if i.period_start or i.period_end else None
                }
                for i in self.identifier
            ]
        return result


class FHIROperationOutcome:
    """FHIR OperationOutcome for validation errors."""

    def __init__(self):
        self.resource_type = "OperationOutcome"
        self.issue: List[Dict[str, Any]] = []

    def add_issue(self, severity: str, code: str, details: str, location: List[str] = None):
        self.issue.append({
            "severity": severity,
            "code": code,
            "details": {"text": details},
            "location": location or []
        })

    def has_errors(self) -> bool:
        return any(i["severity"] == "error" for i in self.issue)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resourceType": self.resource_type,
            "issue": self.issue
        }


class FHIRPatient(FHIRResource):
    """FHIR R4 Patient Resource."""

    def __init__(
        self,
        id: Optional[str] = None,
        identifier: List[FHIRIdentifier] = None,
        name: List[FHIRHumanName] = None,
        gender: PatientGender = PatientGender.UNKNOWN,
        birth_date: Optional[str] = None,
        address: List[FHIRAddress] = None,
        telecom: List[FHIRContactPoint] = None,
        active: bool = True,
        deceased: Optional[bool] = None,
        deceased_date_time: Optional[str] = None,
        marital_status: Optional[FHIRCodeableConcept] = None,
        multiple_birth: Optional[bool] = None,
        contact: List[Dict] = None,
        communication: List[Dict] = None,
        general_practitioner: List[Dict] = None,
        managing_organization: Optional[str] = None,
    ):
        super().__init__("Patient", id)
        self.identifier = identifier or []
        self.name = name or []
        self.gender = gender.value
        self.birth_date = birth_date
        self.address = address or []
        self.telecom = telecom or []
        self.active = active
        self.deceased_boolean = deceased
        self.deceased_date_time = deceased_date_time
        self.marital_status = marital_status
        self.multiple_birth_boolean = multiple_birth
        self.contact = contact or []
        self.communication = communication or []
        self.general_practitioner = general_practitioner or []
        self.managing_organization = {"reference": managing_organization} if managing_organization else None

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "identifier": [
                {
                    "use": i.use,
                    "system": i.system,
                    "value": i.value,
                    "type": {"coding": [{"code": i.type_code}]} if i.type_code else None
                } for i in self.identifier
            ],
            "name": [
                {
                    "use": n.use,
                    "family": n.family,
                    "given": n.given,
                    "prefix": n.prefix,
                    "suffix": n.suffix
                } for n in self.name
            ],
            "gender": self.gender,
            "birthDate": self.birth_date,
            "address": [
                {
                    "use": a.use,
                    "type": a.type,
                    "text": a.text,
                    "line": a.line,
                    "city": a.city,
                    "district": a.district,
                    "state": a.state,
                    "postalCode": a.postal_code,
                    "country": a.country
                } for a in self.address
            ],
            "telecom": [
                {"system": t.system, "value": t.value, "use": t.use, "rank": t.rank}
                for t in self.telecom
            ],
            "active": self.active,
            "deceasedBoolean": self.deceased_boolean,
            "deceasedDateTime": self.deceased_date_time,
            "maritalStatus": self.marital_status.to_dict() if self.marital_status else None,
            "multipleBirthBoolean": self.multiple_birth_boolean,
            "contact": self.contact,
            "communication": self.communication,
            "generalPractitioner": self.general_practitioner,
            "managingOrganization": self.managing_organization,
        })
        return {k: v for k, v in base.items() if v is not None}


class FHIRPractitioner(FHIRResource):
    """FHIR R4 Practitioner Resource."""

    def __init__(
        self,
        id: Optional[str] = None,
        identifier: List[FHIRIdentifier] = None,
        name: List[FHIRHumanName] = None,
        gender: PatientGender = PatientGender.UNKNOWN,
        birth_date: Optional[str] = None,
        active: bool = True,
        qualification: List[Dict] = None,
        communication: List[Dict] = None,
    ):
        super().__init__("Practitioner", id)
        self.identifier = identifier or []
        self.name = name or []
        self.gender = gender.value
        self.birth_date = birth_date
        self.active = active
        self.qualification = qualification or []
        self.communication = communication or []

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "identifier": [
                {"use": i.use, "system": i.system, "value": i.value} for i in self.identifier
            ],
            "name": [
                {"use": n.use, "family": n.family, "given": n.given} for n in self.name
            ],
            "gender": self.gender,
            "birthDate": self.birth_date,
            "active": self.active,
            "qualification": self.qualification,
            "communication": self.communication,
        })
        return {k: v for k, v in base.items() if v is not None}


class FHIROrganization(FHIRResource):
    """FHIR R4 Organization Resource."""

    def __init__(
        self,
        id: Optional[str] = None,
        identifier: List[FHIRIdentifier] = None,
        active: bool = True,
        type_code: List[FHIRCodeableConcept] = None,
        name: str = "",
        alias: List[str] = None,
        telecom: List[FHIRContactPoint] = None,
        address: List[FHIRAddress] = None,
        part_of: Optional[str] = None,
        contact: List[Dict] = None,
        endpoint: List[str] = None,
    ):
        super().__init__("Organization", id)
        self.identifier = identifier or []
        self.active = active
        self.type_code = type_code or []
        self.name = name
        self.alias = alias or []
        self.telecom = telecom or []
        self.address = address or []
        self.part_of = {"reference": part_of} if part_of else None
        self.contact = contact or []
        self.endpoint = [{"reference": e} for e in (endpoint or [])]

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "identifier": [
                {"use": i.use, "system": i.system, "value": i.value} for i in self.identifier
            ],
            "active": self.active,
            "type": [t.to_dict() if hasattr(t, 'to_dict') else t for t in self.type_code],
            "name": self.name,
            "alias": self.alias,
            "telecom": [
                {"system": t.system, "value": t.value, "use": t.use, "rank": t.rank}
                for t in self.telecom
            ],
            "address": [
                {
                    "use": a.use, "type": a.type, "text": a.text,
                    "line": a.line, "city": a.city, "district": a.district,
                    "state": a.state, "postalCode": a.postal_code, "country": a.country
                } for a in self.address
            ],
            "partOf": self.part_of,
            "contact": self.contact,
            "endpoint": self.endpoint,
        })
        return {k: v for k, v in base.items() if v is not None}


class FHIRClaim(FHIRResource):
    """FHIR R4 Claim Resource for JKN."""

    def __init__(
        self,
        id: Optional[str] = None,
        identifier: List[FHIRIdentifier] = None,
        status: ClaimStatus = ClaimStatus.ACTIVE,
        use: ClaimUse = ClaimUse.CLAIM,
        patient: Optional[str] = None,
        created: Optional[str] = None,
        insurer: Optional[str] = None,
        provider: Optional[str] = None,
        priority: Optional[FHIRCodeableConcept] = None,
        funds_reserve: Optional[FHIRCodeableConcept] = None,
        related: List[Dict] = None,
        prescription: Optional[str] = None,
        original_prescription: Optional[str] = None,
        payee: Optional[Dict] = None,
        referral: Optional[str] = None,
        diagnosis: List[Dict] = None,
        procedure: List[Dict] = None,
        insurance: List[Dict] = None,
        accident: Optional[Dict] = None,
        supporting_info: List[Dict] = None,
        item: List[Dict] = None,
        total: Optional[FHIRQuantity] = None,
    ):
        super().__init__("Claim", id)
        self.identifier = identifier or []
        self.status = status.value
        self.use = use.value
        self.patient = {"reference": f"Patient/{patient}"} if patient else None
        self.created = created or datetime.utcnow().isoformat() + "Z"
        self.insurer = {"reference": f"Organization/{insurer}"} if insurer else None
        self.provider = {"reference": f"Organization/{provider}"} if provider else None
        self.priority = priority
        self.funds_reserve = funds_reserve
        self.related = related or []
        self.prescription = {"reference": prescription} if prescription else None
        self.original_prescription = {"reference": original_prescription} if original_prescription else None
        self.payee = payee
        self.referral = {"reference": referral} if referral else None
        self.diagnosis = diagnosis or []
        self.procedure = procedure or []
        self.insurance = insurance or []
        self.accident = accident
        self.supporting_info = supporting_info or []
        self.item = item or []
        self.total = total

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "identifier": [
                {"use": i.use, "system": i.system, "value": i.value} for i in self.identifier
            ],
            "status": self.status,
            "use": self.use,
            "patient": self.patient,
            "created": self.created,
            "insurer": self.insurer,
            "provider": self.provider,
            "priority": self.priority.to_dict() if self.priority else None,
            "fundsReserve": self.funds_reserve.to_dict() if self.funds_reserve else None,
            "related": self.related,
            "prescription": self.prescription,
            "originalPrescription": self.original_prescription,
            "payee": self.payee,
            "referral": self.referral,
            "diagnosis": self.diagnosis,
            "procedure": self.procedure,
            "insurance": self.insurance,
            "accident": self.accident,
            "supportingInfo": self.supporting_info,
            "item": self.item,
            "total": self.total.to_dict() if self.total else None,
        })
        return {k: v for k, v in base.items() if v is not None}


class FHIRBundle:
    """FHIR R4 Bundle Resource."""

    def __init__(
        self,
        bundle_type: str = "collection",
        entries: List[Dict] = None,
        total: int = 0,
    ):
        self.resource_type = "Bundle"
        self.id = str(uuid.uuid4())
        self.meta = {
            "lastUpdated": datetime.utcnow().isoformat() + "Z"
        }
        self.type = bundle_type
        self.total = total
        self.entry = entries or []

    def add_entry(self, resource: FHIRResource, full_url: str = None, search_mode: str = "match"):
        self.entry.append({
            "fullUrl": full_url or f"urn:uuid:{resource.id}",
            "resource": resource.to_dict(),
            "search": {"mode": search_mode}
        })
        self.total = len(self.entry)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resourceType": self.resource_type,
            "id": self.id,
            "meta": self.meta,
            "type": self.type,
            "total": self.total,
            "entry": self.entry,
        }