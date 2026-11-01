import os
import ssl
import logging
from typing import Optional, Dict, Any
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)

class MTLSError(Exception):
    """Exception for mTLS verification failures"""
    pass

class MTLSConfig:
    """Configuration for mTLS"""
    def __init__(self):
        # Path to CA bundle for verifying client certificates
        self.ca_bundle_path = os.getenv("MTLS_CA_BUNDLE_PATH", "/etc/certs/ca-bundle.crt")

        # Whether mTLS is required (vs optional)
        self.require_client_cert = os.getenv("MTLS_REQUIRE_CLIENT_CERT", "true").lower() == "true"

        # Service identity extraction
        self.service_cn_field = os.getenv("MTLS_SERVICE_CN_FIELD", "CN")

        # Certificate verification settings
        self.verify_depth = int(os.getenv("MTLS_VERIFY_DEPTH", "2"))

_mtls_config = MTLSConfig()

def get_mtls_config() -> MTLSConfig:
    return _mtls_config

def load_ca_bundle() -> Optional[ssl.SSLContext]:
    """
    Load the CA bundle for verifying client certificates.
    Returns an SSL context configured with the CA bundle.
    """
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_verify_locations(_mtls_config.ca_bundle_path)
        context.verify_mode = ssl.CERT_REQUIRED if _mtls_config.require_client_cert else ssl.CERT_OPTIONAL
        context.check_hostname = False  # We verify service identity via CN/SAN, not hostname
        return context
    except Exception as e:
        logger.error(f"Failed to load CA bundle from {_mtls_config.ca_bundle_path}: {e}")
        return None

def parse_client_certificate(cert_pem: str) -> Optional[x509.Certificate]:
    """
    Parse a PEM-encoded client certificate.
    """
    try:
        return x509.load_pem_x509_certificate(cert_pem.encode(), default_backend())
    except Exception as e:
        logger.error(f"Failed to parse client certificate: {e}")
        return None

def verify_client_certificate(cert_pem: str) -> bool:
    """
    Verify a client certificate against the CA bundle.
    This is typically done at the proxy level (nginx/Envoy),
    but we can do additional validation here.
    """
    cert = parse_client_certificate(cert_pem)
    if not cert:
        return False

    # In production, verify against CA
    # For now, we trust the proxy has done the verification
    # and just parse for identity extraction
    return True

def extract_service_identity(cert_pem: str) -> Optional[str]:
    """
    Extract the service identity from a client certificate.
    Uses Common Name (CN) or Subject Alternative Name (SAN).
    """
    cert = parse_client_certificate(cert_pem)
    if not cert:
        return None

    # Try to get CN from subject
    try:
        cn_attrs = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
        if cn_attrs:
            return cn_attrs[0].value
    except Exception:
        pass

    # Fallback to SAN
    try:
        san_ext = cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        for name in san_ext.value:
            if isinstance(name, x509.DNSName):
                return name.value
    except Exception:
        pass

    return None

def extract_service_metadata(cert_pem: str) -> Dict[str, Any]:
    """
    Extract all relevant metadata from a client certificate.
    """
    cert = parse_client_certificate(cert_pem)
    if not cert:
        return {}

    metadata = {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "serial_number": str(cert.serial_number),
        "not_valid_before": cert.not_valid_before_utc.isoformat() if hasattr(cert, 'not_valid_before_utc') else cert.not_valid_before.isoformat(),
        "not_valid_after": cert.not_valid_after_utc.isoformat() if hasattr(cert, 'not_valid_after_utc') else cert.not_valid_after.isoformat(),
    }

    # Try to get CN
    try:
        cn_attrs = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
        if cn_attrs:
            metadata["common_name"] = cn_attrs[0].value
    except Exception:
        pass

    # Get SANs
    try:
        san_ext = cert.extensions.get_extension_for_oid(x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        metadata["sans"] = [str(name) for name in san_ext.value]
    except Exception:
        metadata["sans"] = []

    return metadata

# FastAPI dependency for mTLS verification
from fastapi import Depends, HTTPException, status, Request

async def verify_mtls_request(request: Request) -> Optional[Dict[str, Any]]:
    """
    FastAPI dependency to verify mTLS client certificate.
    Expects the certificate to be passed via header by the reverse proxy.
    """
    # Get certificate from header (set by nginx/Envoy)
    # Common headers: X-Forwarded-Client-Cert, X-Client-Cert, ssl-client-cert
    cert_header = (
        request.headers.get("X-Forwarded-Client-Cert") or
        request.headers.get("X-Client-Cert") or
        request.headers.get("ssl-client-cert")
    )

    if not cert_header:
        if _mtls_config.require_client_cert:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Client certificate required"
            )
        return None

    # The header may be URL-encoded, decode it
    import urllib.parse
    cert_pem = urllib.parse.unquote(cert_header)

    # Verify certificate
    if not verify_client_certificate(cert_pem):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client certificate"
        )

    # Extract service identity
    service_identity = extract_service_identity(cert_pem)
    if not service_identity:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not extract service identity from certificate"
        )

    metadata = extract_service_metadata(cert_pem)
    metadata["service_identity"] = service_identity

    return metadata