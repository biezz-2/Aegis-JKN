"""
INA-CBGs Validation Layer for Aegis-JKN.
Implements local INA-CBGs code validation and pseudonymization middleware.
No external API calls - uses mock for SATUSEHAT integration.
"""
import re
import hashlib
import json
import uuid
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# --- INA-CBGs Code Validation ---

class CBGSGroup(str, Enum):
    """INA-CBGs Group categories."""
    KELAS_1 = "Kelas 1"
    KELAS_2 = "Kelas 2"
    KELAS_3 = "Kelas 3"
    VVIP = "VVIP"
    VIP = "VIP"
    UTAMA = "Utama"

class INACBGSValidator:
    """
    Local validator for INA-CBGs (Case Based Groups) codes.
    Validates format, grouping logic, and tariff mapping without external API.
    """

    # INA-CBGs code pattern: e.g., J-4-07-02-001
    # Format: {Specialty}-{Group}-{Subgroup}-{Code}-{Seq}
    CBGS_CODE_PATTERN = re.compile(r'^[A-Z]-\d-\d{2}-\d{2}-\d{3}$')

    # Valid specialties (first letter)
    VALID_SPECIALTIES = {
        'J': 'Penyakit Dalam',
        'K': 'Kebidanan dan Kandungan',
        'B': 'Bedah Umum',
        'P': 'Penyakit Kulit dan Kelamin',
        'M': 'Penyakit Mata',
        'T': 'Penyakit THT',
        'S': 'Saraf',
        'R': 'Radiologi',
        'L': 'Patologi Klinik',
        'A': 'Anestesi',
        'F': 'Farmasi Klinik',
        'G': 'Gizi Klinik',
        'H': 'Hematologi',
        'I': 'Imunologi',
        'N': 'Nefrologi',
        'O': 'Onkologi',
        'U': 'Urologi',
        'V': 'Neurologi',
        'W': 'Penyakit Paru',
        'X': 'Penyakit Jantung',
        'Y': 'Penyakit Ginjal',
        'Z': 'Lainnya'
    }

    # Group codes (second digit): 1-4 for classes, 5-6 for special
    # Group 4 = Kelas 1 (top tier)
    VALID_GROUPS = {
        '1': CBGSGroup.KELAS_1,
        '2': CBGSGroup.KELAS_2,
        '3': CBGSGroup.KELAS_3,
        '4': CBGSGroup.KELAS_1,
        '5': CBGSGroup.VIP,
        '6': CBGSGroup.VVIP,
        '7': CBGSGroup.UTAMA
    }

    # Mock tariff mapping (local reference table)
    MOCK_TARIFFS = {
        "J-4-07-02-001": {"name": "Demam Berdarah Dengue", "tariff": 3500000, "group": "Kelas 1"},
        "J-4-07-02-002": {"name": "Typhoid Fever", "tariff": 2800000, "group": "Kelas 1"},
        "K-4-12-01-001": {"name": "Persalinan Normal", "tariff": 2200000, "group": "Kelas 1"},
        "K-4-12-01-002": {"name": "Sectio Caesarea", "tariff": 5500000, "group": "Kelas 1"},
        "B-4-05-03-001": {"name": "Apendektomi", "tariff": 4500000, "group": "Kelas 1"},
        "B-4-05-03-002": {"name": "Herniorafi", "tariff": 3800000, "group": "Kelas 1"},
    }

    @classmethod
    def validate_code(cls, cbgs_code: str) -> Dict[str, Any]:
        """
        Validate INA-CBGs code format and return validation result.

        Returns:
            dict with keys: valid (bool), errors (list), details (dict)
        """
        result = {"valid": True, "errors": [], "details": {}}

        # Check format
        if not cls.CBGS_CODE_PATTERN.match(cbgs_code):
            result["valid"] = False
            result["errors"].append(
                f"Invalid format. Expected pattern: {{Specialty}}-{{Group}}-{{Subgroup}}-{{Code}}-{{Seq}} (e.g., J-4-07-02-001)"
            )
            return result

        parts = cbgs_code.split('-')
        specialty, group, subgroup, code, seq = parts

        # Validate specialty
        if specialty not in cls.VALID_SPECIALTIES:
            result["valid"] = False
            result["errors"].append(f"Invalid specialty code: {specialty}")

        # Validate group
        if group not in cls.VALID_GROUPS:
            result["valid"] = False
            result["errors"].append(f"Invalid group code: {group}")

        # Validate subgroup range (01-99)
        try:
            subgroup_num = int(subgroup)
            if not (1 <= subgroup_num <= 99):
                result["valid"] = False
                result["errors"].append(f"Subgroup out of range: {subgroup} (valid: 01-99)")
        except ValueError:
            result["valid"] = False
            result["errors"].append(f"Invalid subgroup format: {subgroup}")

        # Validate code range (01-99)
        try:
            code_num = int(code)
            if not (1 <= code_num <= 99):
                result["valid"] = False
                result["errors"].append(f"Code out of range: {code} (valid: 01-99)")
        except ValueError:
            result["valid"] = False
            result["errors"].append(f"Invalid code format: {code}")

        # Validate sequence (001-999)
        try:
            seq_num = int(seq)
            if not (1 <= seq_num <= 999):
                result["valid"] = False
                result["errors"].append(f"Sequence out of range: {seq} (valid: 001-999)")
        except ValueError:
            result["valid"] = False
            result["errors"].append(f"Invalid sequence format: {seq}")

        if result["valid"]:
            result["details"] = {
                "specialty": specialty,
                "specialty_name": cls.VALID_SPECIALTIES.get(specialty, "Unknown"),
                "group": group,
                "group_name": cls.VALID_GROUPS.get(group, "Unknown"),
                "subgroup": subgroup,
                "code": code,
                "sequence": seq,
                "tariff_info": cls.MOCK_TARIFFS.get(cbgs_code)
            }

        return result

    @classmethod
    def get_tariff(cls, cbgs_code: str) -> Optional[Dict[str, Any]]:
        """Get tariff information for a validated CBGS code."""
        validation = cls.validate_code(cbgs_code)
        if not validation["valid"]:
            return None
        return cls.MOCK_TARIFFS.get(cbgs_code)

    @classmethod
    def suggest_codes(cls, partial_code: str, limit: int = 5) -> List[str]:
        """Suggest valid CBGS codes matching a partial input."""
        suggestions = []
        for code in cls.MOCK_TARIFFS.keys():
            if code.startswith(partial_code.upper()):
                suggestions.append(code)
            if len(suggestions) >= limit:
                break
        return suggestions


# --- Pseudonymization Middleware ---

class Pseudonymizer:
    """
    Local pseudonymization for PII data (Name, NIK).
    Converts to format: D01 (Doctor), P01 (Patient), RS_A (Organization).
    Deterministic: same input always produces same pseudonym.
    """

    PREFIXES = {
        "patient": "P",
        "practitioner": "D",
        "organization": "RS",
        "claim": "C",
        "diagnosis": "DX"
    }

    def __init__(self, salt: str = "AEGIS-JKN-PSEUDONYM-SALT-2024"):
        self.salt = salt
        self._cache: Dict[str, str] = {}

    def _hash_value(self, value: str) -> str:
        """Generate deterministic hash for a value."""
        hash_input = f"{self.salt}:{value}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()[:8].upper()

    def pseudonymize(self, value: str, entity_type: str) -> str:
        """
        Pseudonymize a PII value.

        Args:
            value: The original value (name, NIK, etc.)
            entity_type: One of 'patient', 'practitioner', 'organization', 'claim', 'diagnosis'

        Returns:
            Pseudonymized string like P01, D01, RS_A
        """
        cache_key = f"{entity_type}:{value}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        prefix = self.PREFIXES.get(entity_type, "X")
        hash_suffix = self._hash_value(value)

        # Format: Prefix + zero-padded number from hash
        # Use first 4 chars of hash as hex, convert to int, mod 10000 for 4 digits
        num = int(hash_suffix[:4], 16) % 10000
        pseudonym = f"{prefix}{num:04d}"

        self._cache[cache_key] = pseudonym
        return pseudonym

    def pseudonymize_patient(self, patient_name: str, nik: str = None) -> Dict[str, str]:
        """Pseudonymize patient data."""
        return {
            "name": self.pseudonymize(patient_name, "patient"),
            "nik": self.pseudonymize(nik, "patient") if nik else None
        }

    def pseudonymize_practitioner(self, doctor_name: str, sip: str = None) -> Dict[str, str]:
        """Pseudonymize practitioner data."""
        return {
            "name": self.pseudonymize(doctor_name, "practitioner"),
            "sip": self.pseudonymize(sip, "practitioner") if sip else None
        }

    def pseudonymize_organization(self, org_name: str, npwp: str = None) -> Dict[str, str]:
        """Pseudonymize organization data."""
        return {
            "name": self.pseudonymize(org_name, "organization"),
            "npwp": self.pseudonymize(npwp, "organization") if npwp else None
        }

    def pseudonymize_claim(self, claim_id: str) -> str:
        """Pseudonymize claim ID."""
        return self.pseudonymize(claim_id, "claim")

    def clear_cache(self):
        """Clear pseudonymization cache."""
        self._cache.clear()


# --- Audit Trail Logging ---

@dataclass
class AuditLogEntry:
    """Immutable audit log entry for PostgreSQL."""
    id: str
    entity_type: str  # patient, claim, provider, cbgs_validation
    entity_id: str
    action: str       # create, read, update, delete, validate, pseudonymize
    actor_id: str     # user/system ID performing action
    actor_role: str   # doctor, admin, system, auditor
    details: Dict[str, Any]
    timestamp: datetime
    hash_chain: str   # SHA256 of previous log + current data for immutability

class AuditTrail:
    """
    Immutable audit trail logger for PostgreSQL.
    Logs compliance-related events with hash chaining for integrity.
    """

    def __init__(self, db_session=None):
        self.db_session = db_session
        self._last_hash = "0" * 64  # Genesis hash

    def _compute_hash(self, entry: AuditLogEntry) -> str:
        """Compute hash chain for immutability."""
        data = f"{self._last_hash}:{entry.entity_type}:{entry.entity_id}:{entry.action}:{entry.actor_id}:{json.dumps(entry.details, sort_keys=True)}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def log(
        self,
        entity_type: str,
        entity_id: str,
        action: str,
        actor_id: str,
        actor_role: str,
        details: Dict[str, Any]
    ) -> AuditLogEntry:
        """Create and persist an immutable audit log entry."""
        entry = AuditLogEntry(
            id=str(uuid.uuid4()),
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            actor_id=actor_id,
            actor_role=actor_role,
            details=details,
            timestamp=datetime.utcnow(),
            hash_chain=self._compute_hash(AuditLogEntry(
                id="", entity_type=entity_type, entity_id=entity_id,
                action=action, actor_id=actor_id, actor_role=actor_role,
                details=details, timestamp=datetime.utcnow(), hash_chain=""
            ))
        )

        self._last_hash = entry.hash_chain

        # Persist to PostgreSQL if session available
        if self.db_session:
            self._persist_to_db(entry)

        return entry

    def _persist_to_db(self, entry: AuditLogEntry):
        """Persist audit entry to PostgreSQL audit_logs table."""
        try:
            from src.backend.app.models.audit import AuditLog
            from sqlalchemy import text

            # Use raw SQL for immutable append-only
            sql = text("""
                INSERT INTO audit_logs (entity_id, action, user_id, details, timestamp)
                VALUES (:entity_id, :action, :user_id, :details, :timestamp)
            """)

            self.db_session.execute(sql, {
                "entity_id": f"{entry.entity_type}:{entry.entity_id}",
                "action": f"{entry.action}:{entry.actor_role}",
                "user_id": entry.actor_id,
                "details": {
                    "entity_type": entry.entity_type,
                    "entity_id": entry.entity_id,
                    "action": entry.action,
                    "actor_id": entry.actor_id,
                    "actor_role": entry.actor_role,
                    "details": entry.details,
                    "hash_chain": entry.hash_chain,
                    "log_id": entry.id
                },
                "timestamp": entry.timestamp
            })
            self.db_session.commit()
        except Exception as e:
            # Log error but don't fail the operation
            import logging
            logging.getLogger("audit").error(f"Failed to persist audit log: {e}")
            if self.db_session:
                self.db_session.rollback()

    def verify_chain(self, entries: List[AuditLogEntry]) -> bool:
        """Verify hash chain integrity."""
        if not entries:
            return True

        prev_hash = "0" * 64
        for entry in entries:
            expected = hashlib.sha256(
                f"{prev_hash}:{entry.entity_type}:{entry.entity_id}:{entry.action}:{entry.actor_id}:{json.dumps(entry.details, sort_keys=True)}".encode()
            ).hexdigest()
            if entry.hash_chain != expected:
                return False
            prev_hash = entry.hash_chain
        return True


# --- SATUSEHAT Mock Integration ---

class SatusehatMockClient:
    """
    Mock client for SATUSEHAT integration.
    No external API calls - simulates FHIR R4 interactions locally.
    """

    def __init__(self):
        self.base_url = "http://localhost:8080/fhir"  # Local mock server
        self.access_token = "mock-token-aegis-jkn"

    def push_patient(self, fhir_patient: Dict[str, Any]) -> Dict[str, Any]:
        """Mock: Push Patient to SATUSEHAT."""
        return {
            "success": True,
            "resourceType": "Patient",
            "id": fhir_patient.get("id", str(uuid.uuid4())),
            "meta": {"versionId": "1", "lastUpdated": datetime.utcnow().isoformat() + "Z"},
            "message": "Patient pushed to SATUSEHAT (mock)"
        }

    def push_practitioner(self, fhir_practitioner: Dict[str, Any]) -> Dict[str, Any]:
        """Mock: Push Practitioner to SATUSEHAT."""
        return {
            "success": True,
            "resourceType": "Practitioner",
            "id": fhir_practitioner.get("id", str(uuid.uuid4())),
            "meta": {"versionId": "1", "lastUpdated": datetime.utcnow().isoformat() + "Z"},
            "message": "Practitioner pushed to SATUSEHAT (mock)"
        }

    def push_organization(self, fhir_org: Dict[str, Any]) -> Dict[str, Any]:
        """Mock: Push Organization to SATUSEHAT."""
        return {
            "success": True,
            "resourceType": "Organization",
            "id": fhir_org.get("id", str(uuid.uuid4())),
            "meta": {"versionId": "1", "lastUpdated": datetime.utcnow().isoformat() + "Z"},
            "message": "Organization pushed to SATUSEHAT (mock)"
        }

    def push_claim(self, fhir_claim: Dict[str, Any]) -> Dict[str, Any]:
        """Mock: Push Claim to SATUSEHAT."""
        return {
            "success": True,
            "resourceType": "Claim",
            "id": fhir_claim.get("id", str(uuid.uuid4())),
            "meta": {"versionId": "1", "lastUpdated": datetime.utcnow().isoformat() + "Z"},
            "message": "Claim pushed to SATUSEHAT (mock)"
        }

    def validate_cbgs(self, cbgs_code: str) -> Dict[str, Any]:
        """Mock: Validate CBGS code with SATUSEHAT terminology."""
        validation = INACBGSValidator.validate_code(cbgs_code)
        return {
            "success": validation["valid"],
            "code": cbgs_code,
            "validation": validation,
            "source": "SATUSEHAT Terminology Service (mock)"
        }

    def get_claim_status(self, claim_id: str) -> Dict[str, Any]:
        """Mock: Get claim status from SATUSEHAT."""
        return {
            "success": True,
            "claim_id": claim_id,
            "status": "approved",
            "paid_amount": 2500000,
            "processed_at": datetime.utcnow().isoformat() + "Z",
            "source": "SATUSEHAT Claim Service (mock)"
        }


# --- Compliance Service Facade ---

class ComplianceService:
    """
    Facade for compliance operations: FHIR mapping, CBGS validation,
    pseudonymization, and audit logging.
    """

    def __init__(self, db_session=None):
        self.fhir_mapper = None  # Import from fhir_mapper module
        self.cbgs_validator = INACBGSValidator()
        self.pseudonymizer = Pseudonymizer()
        self.audit_trail = AuditTrail(db_session)
        self.satusehat = SatusehatMockClient()

    def process_claim_compliance(
        self,
        claim_data: Any,
        patient_data: Any,
        provider_data: Any,
        actor_id: str,
        actor_role: str
    ) -> Dict[str, Any]:
        """Process a claim through full compliance pipeline."""

        # 1. Pseudonymize PII
        patient_pseudo = self.pseudonymizer.pseudonymize_patient(
            getattr(patient_data, 'name', ''), getattr(patient_data, 'patient_id', '')
        )
        provider_pseudo = self.pseudonymizer.pseudonymize_organization(
            getattr(provider_data, 'name', ''), getattr(provider_data, 'provider_id', '')
        )
        claim_pseudo = self.pseudonymizer.pseudonymize_claim(
            getattr(claim_data, 'claim_id', '')
        )

        # 2. Validate CBGS codes if present
        cbgs_results = []
        if hasattr(claim_data, 'diagnosis_codes'):
            for code in claim_data.diagnosis_codes:
                cbgs_results.append(self.cbgs_validator.validate_code(code))

        # 3. Map to FHIR
        # Import here to avoid circular dependency
        from src.backend.app.api.compliance.fhir_mapper import FHIRMapper
        fhir_mapper = FHIRMapper()

        fhir_patient = fhir_mapper.map_patient(patient_data)
        fhir_provider = fhir_mapper.map_provider(provider_data)
        fhir_claim = fhir_mapper.map_claim(claim_data, fhir_patient.id, fhir_provider.id)

        # 4. Audit log
        self.audit_trail.log(
            entity_type="claim",
            entity_id=claim_pseudo,
            action="process_compliance",
            actor_id=actor_id,
            actor_role=actor_role,
            details={
                "patient_pseudo": patient_pseudo,
                "provider_pseudo": provider_pseudo,
                "cbgs_validations": cbgs_results,
                "fhir_patient_id": fhir_patient.id,
                "fhir_provider_id": fhir_provider.id,
                "fhir_claim_id": fhir_claim.id
            }
        )

        return {
            "pseudonymized": {
                "patient": patient_pseudo,
                "provider": provider_pseudo,
                "claim": claim_pseudo
            },
            "cbgs_validation": cbgs_results,
            "fhir_resources": {
                "patient": fhir_patient.dict(),
                "provider": fhir_provider.dict(),
                "claim": fhir_claim.dict()
            },
            "audit_logged": True
        }

    def validate_and_audit_cbgs(
        self,
        cbgs_code: str,
        actor_id: str,
        actor_role: str
    ) -> Dict[str, Any]:
        """Validate CBGS code and audit the validation."""
        result = self.cbgs_validator.validate_code(cbgs_code)

        self.audit_trail.log(
            entity_type="cbgs_validation",
            entity_id=cbgs_code,
            action="validate",
            actor_id=actor_id,
            actor_role=actor_role,
            details={
                "code": cbgs_code,
                "valid": result["valid"],
                "errors": result["errors"],
                "details": result["details"]
            }
        )

        return result


# --- Global Instances ---

# Singleton instances
_pseudonymizer = None
_audit_trail = None
_cbgs_validator = None
_compliance_service = None

def get_pseudonymizer() -> Pseudonymizer:
    global _pseudonymizer
    if _pseudonymizer is None:
        _pseudonymizer = Pseudonymizer()
    return _pseudonymizer

def get_audit_trail(db_session=None) -> AuditTrail:
    global _audit_trail
    if _audit_trail is None:
        _audit_trail = AuditTrail(db_session)
    return _audit_trail

def get_cbgs_validator() -> INACBGSValidator:
    global _cbgs_validator
    if _cbgs_validator is None:
        _cbgs_validator = INACBGSValidator()
    return _cbgs_validator

def get_compliance_service(db_session=None) -> ComplianceService:
    global _compliance_service
    if _compliance_service is None:
        _compliance_service = ComplianceService(db_session)
    return _compliance_service


# --- Usage Example / Testing ---

if __name__ == "__main__":
    # Test CBGS validation
    validator = INACBGSValidator()

    test_codes = [
        "J-4-07-02-001",   # Valid
        "K-4-12-01-002",   # Valid
        "X-1-99-99-999",   # Valid format
        "INVALID-CODE",    # Invalid format
        "Z-9-00-00-000",   # Invalid group, subgroup, code, seq
    ]

    print("=== INA-CBGs Validation Tests ===")
    for code in test_codes:
        result = validator.validate_code(code)
        print(f"\nCode: {code}")
        print(f"  Valid: {result['valid']}")
        if result['errors']:
            print(f"  Errors: {result['errors']}")
        if result['details']:
            print(f"  Details: {result['details']}")

    # Test pseudonymization
    print("\n=== Pseudonymization Tests ===")
    pseudo = Pseudonymizer()

    patient_name = "Budi Santoso"
    patient_nik = "3201234567890001"
    doctor_name = "dr. Siti Rahayu, Sp.PD"
    org_name = "RSUD Jakarta Pusat"

    print(f"Patient: {patient_name} -> {pseudo.pseudonymize_patient(patient_name, patient_nik)}")
    print(f"Doctor: {doctor_name} -> {pseudo.pseudonymize_practitioner(doctor_name)}")
    print(f"Organization: {org_name} -> {pseudo.pseudonymize_organization(org_name)}")
    print(f"Claim: CLM-2024-001234 -> {pseudo.pseudonymize_claim('CLM-2024-001234')}")

    # Test determinism
    print(f"\nDeterminism check (same input):")
    print(f"  {patient_name} -> {pseudo.pseudonymize(patient_name, 'patient')}")
    print(f"  {patient_name} -> {pseudo.pseudonymize(patient_name, 'patient')}")

    # Test audit trail
    print("\n=== Audit Trail Tests ===")
    audit = AuditTrail()

    entry1 = audit.log(
        entity_type="patient",
        entity_id="P0001",
        action="create",
        actor_id="doctor_001",
        actor_role="doctor",
        details={"name": "Budi Santoso", "nik": "3201234567890001"}
    )
    print(f"Entry 1: {entry1.id} | Hash: {entry1.hash_chain[:16]}...")

    entry2 = audit.log(
        entity_type="claim",
        entity_id="C0001",
        action="create",
        actor_id="doctor_001",
        actor_role="doctor",
        details={"amount": 5000000, "cbgs_code": "J-4-07-02-001"}
    )
    print(f"Entry 2: {entry2.id} | Hash: {entry2.hash_chain[:16]}...")

    # Verify chain
    entries = [entry1, entry2]
    print(f"Chain valid: {audit.verify_chain(entries)}")