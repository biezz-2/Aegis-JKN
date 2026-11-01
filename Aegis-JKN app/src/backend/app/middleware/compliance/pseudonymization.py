"""
Pseudonymization Middleware for Aegis-JKN.
Ensures PII (Personally Identifiable Information) is converted to compliant formats.
"""
from typing import Any, Dict, List, Union
from functools import wraps
from fastapi import Request, Response
import hashlib
import hmac
import os

# Format constants
FORMAT_D01 = "D01"  # Dummy identifier for Patient
FORMAT_P01 = "P01"  # Dummy identifier for Practitioner
FORMAT_RS_A = "RS_A" # Dummy identifier for Hospital/Organization

class Pseudonymizer:
    """
    Handles pseudonymization of sensitive data.
    In production, this would use a secure vault/salt managed by KMS.
    """
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or os.environ.get("PSEUDONYM_SECRET", "default-dev-secret-key")
        self.salt = os.environ.get("PSEUDONYM_SALT", "dev-salt-12345")

    def _generate_pseudonym(self, original_value: str, prefix: str) -> str:
        """Generate a deterministic pseudonym using HMAC-SHA256."""
        if not original_value:
            return ""

        # HMAC ensures that we can consistently map the same PII to the same pseudonym
        # without being able to reverse it without the secret key.
        hashed = hmac.new(
            self.secret_key.encode(),
            (original_value + self.salt).encode(),
            hashlib.sha256
        ).hexdigest()

        # Return prefix + first 12 chars of hash for brevity
        return f"{prefix}_{hashed[:12]}"

    def pseudonymize_patient(self, patient_id: str) -> str:
        """Convert Patient PII to D01 format."""
        return self._generate_pseudonym(patient_id, FORMAT_D01)

    def pseudonymize_practitioner(self, practitioner_id: str) -> str:
        """Convert Practitioner PII to P01 format."""
        return self._generate_pseudonym(practitioner_id, FORMAT_P01)

    def pseudonymize_organization(self, org_id: str) -> str:
        """Convert Organization PII to RS_A format."""
        return self._generate_pseudonym(org_id, FORMAT_RS_A)

    def pseudonymize_dict(self, data: Dict[str, Any], field_mappings: Dict[str, str]) -> Dict[str, Any]:
        """
        Recursively pseudonymize a dictionary based on field mappings.
        field_mappings: { "field_name": "patient" | "practitioner" | "organization" }
        """
        new_data = data.copy()
        for field, p_type in field_mappings.items():
            if field in new_data:
                val = new_data[field]
                if p_type == "patient":
                    new_data[field] = self.pseudonymize_patient(str(val))
                elif p_type == "practitioner":
                    new_data[field] = self.pseudonymize_practitioner(str(val))
                elif p_type == "organization":
                    new_data[field] = self.pseudonymize_organization(str(val))

        # Recursive for nested lists/dicts
        for k, v in new_data.items():
            if isinstance(v, dict):
                new_data[k] = self.pseudonymize_dict(v, field_mappings)
            elif isinstance(v, list):
                new_data[k] = [
                    self.pseudonymize_dict(i, field_mappings) if isinstance(i, dict) else i
                    for i in v
                ]

        return new_data

# FastAPI Middleware implementation
async def pseudonymization_middleware(request: Request, call_next):
    """
    Intercepts responses and pseudonymizes sensitive fields.
    Note: In a real app, this would check for specific headers (e.g., X-Compliance-Mode: pseudonymized).
    """
    # We only pseudonymize outgoing responses for compliance
    response = await call_next(request)

    # This is a conceptual implementation.
    # Intercepting response body in FastAPI requires custom Response subclass
    # or using a middleware that buffers the body.
    return response

# Global instance for use in services
compliance_pseudonymizer = Pseudonymizer()
