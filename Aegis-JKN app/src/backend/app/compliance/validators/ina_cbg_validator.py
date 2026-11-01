"""
INA-CBGs (Indonesia Case Base Groups) Validation Layer for Aegis-JKN.
Validates INA-CBG codes, grouping logic, and tariff calculation per BPJS Kesehatan standards.
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum
from datetime import datetime
import json
import re


class CBGVersion(str, Enum):
    """Supported INA-CBG versions."""
    V2_2017 = "2017"
    V3_2020 = "2020"
    V4_2022 = "2022"
    V5_2024 = "2024"


class CBGCategory(str, Enum):
    """INA-CBG Categories."""
    BEDAH = "A"           # Bedah
    BEDAH_MULUT = "B"     # Bedah Mulut
    ANESTESI = "C"        # Anestesi
    RADIOLOGI = "D"       # Radiologi
    PATOLOGI = "E"        # Patologi
    FISIK = "F"           # Fisik & Rehabilitasi
    KAMAR = "G"           # Rawat Inap (Kamar)
    INTENSIF = "H"        # Perawatan Intensif
    JASA_DOKTER = "I"     # Jasa Dokter
    JASA_PARAMEDIS = "J"  # Jasa Paramedis
    OBAT = "K"            # Obat & Alkes
    ALKES = "L"           # Alat Kesehatan
    LABORATORIUM = "M"    # Laboratorium
    REHAB_MEDIK = "N"     # Rehabilitasi Medik
    LAINNYA = "Z"         # Lainnya


class SeverityLevel(str, Enum):
    """Severity levels for INA-CBG grouping."""
    RENDAH = "1"
    SEDANG = "2"
    TINGGI = "3"
    SANGAT_TINGGI = "4"


@dataclass
class CBGCode:
    """INA-CBG Code structure."""
    code: str
    version: CBGVersion
    category: CBGCategory
    severity: SeverityLevel
    sub_code: str  # 3-digit sub code
    description: str = ""
    base_tariff: float = 0.0
    is_active: bool = True

    @property
    def full_code(self) -> str:
        """Full INA-CBG code format: {category}{version_last2}{severity}{sub_code}"""
        return f"{self.category.value}{self.version.value[-2:]}{self.severity.value}{self.sub_code}"

    @classmethod
    def parse(cls, code: str, version: CBGVersion = CBGVersion.V5_2024) -> 'CBGCode':
        """Parse INA-CBG code string."""
        if len(code) < 7:
            raise ValueError(f"Invalid CBG code format: {code}")

        cat_char = code[0]
        version_digits = code[1:3]
        severity_digit = code[3]
        sub_code = code[4:7]

        category = CBGCategory(cat_char)
        severity = SeverityLevel(severity_digit)

        return cls(
            code=code,
            version=version,
            category=category,
            severity=severity,
            sub_code=sub_code,
        )


@dataclass
class CBGGroupingResult:
    """Result of INA-CBG grouping logic."""
    cbg_code: CBGCode
    drg_code: Optional[str] = None
    base_tariff: float = 0.0
    adjusted_tariff: float = 0.0
    components: Dict[str, float] = field(default_factory=dict)
    los_days: int = 0  # Length of Stay
    is_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cbg_code": self.cbg_code.full_code,
            "cbg_description": self.cbg_code.description,
            "drg_code": self.drg_code,
            "base_tariff": self.base_tariff,
            "adjusted_tariff": self.adjusted_tariff,
            "components": self.components,
            "los_days": self.los_days,
            "is_valid": self.is_valid,
            "validation_errors": self.validation_errors,
            "warnings": self.warnings,
        }


@dataclass
class ClaimValidationContext:
    """Context for claim validation."""
    patient_age: int
    patient_gender: str
    diagnosis_codes: List[str]  # ICD-10
    procedure_codes: List[str]  # ICD-9-CM / ICD-10-PCS
    los_days: int
    facility_type: str  # hospital, clinic, etc.
    facility_class: str  # A, B, C, D
    is_emergency: bool = False
    is_national_referral: bool = False
    complication_codes: List[str] = field(default_factory=list)
    comorbidity_codes: List[str] = field(default_factory=list)


class INACBGValidator:
    """
    INA-CBGs Validator for JKN Claims.
    Implements grouping logic per PERATURAN BPJS KESEHATAN.
    """

    # Tariff base rates per category (simplified - real rates from BPJS)
    BASE_TARIFFS = {
        CBGCategory.BEDAH: 2500000,
        CBGCategory.BEDAH_MULUT: 1800000,
        CBGCategory.ANESTESI: 800000,
        CBGCategory.RADIOLOGI: 500000,
        CBGCategory.PATOLOGI: 400000,
        CBGCategory.FISIK: 300000,
        CBGCategory.KAMAR: 1200000,
        CBGCategory.INTENSIF: 3500000,
        CBGCategory.JASA_DOKTER: 1500000,
        CBGCategory.JASA_PARAMEDIS: 600000,
        CBGCategory.OBAT: 1000000,
        CBGCategory.ALKES: 1200000,
        CBGCategory.LABORATORIUM: 450000,
        CBGCategory.REHAB_MEDIK: 800000,
        CBGCategory.LAINNYA: 500000,
    }

    # Severity multipliers
    SEVERITY_MULTIPLIERS = {
        SeverityLevel.RENDAH: 1.0,
        SeverityLevel.SEDANG: 1.35,
        SeverityLevel.TINGGI: 1.85,
        SeverityLevel.SANGAT_TINGGI: 2.5,
    }

    # Facility class multipliers
    FACILITY_CLASS_MULTIPLIERS = {
        "A": 1.5,
        "B": 1.25,
        "C": 1.0,
        "D": 0.85,
    }

    # Emergency multiplier
    EMERGENCY_MULTIPLIER = 1.25

    # National referral multiplier
    NATIONAL_REFERRAL_MULTIPLIER = 1.15

    # LOS (Length of Stay) thresholds per category
    LOS_THRESHOLDS = {
        CBGCategory.BEDAH: {"min": 1, "max": 14, "standard": 5},
        CBGCategory.KAMAR: {"min": 1, "max": 30, "standard": 7},
        CBGCategory.INTENSIF: {"min": 1, "max": 21, "standard": 5},
        CBGCategory.BEDAH_MULUT: {"min": 1, "max": 7, "standard": 3},
        CBGCategory.ANESTESI: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.RADIOLOGI: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.PATOLOGI: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.FISIK: {"min": 1, "max": 14, "standard": 5},
        CBGCategory.JASA_DOKTER: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.JASA_PARAMEDIS: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.OBAT: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.ALKES: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.LABORATORIUM: {"min": 0, "max": 1, "standard": 0},
        CBGCategory.REHAB_MEDIK: {"min": 1, "max": 30, "standard": 10},
        CBGCategory.LAINNYA: {"min": 0, "max": 14, "standard": 3},
    }

    def __init__(self, version: CBGVersion = CBGVersion.V5_2024):
        self.version = version
        self._cbg_database: Dict[str, CBGCode] = {}
        self._load_cbg_database()

    def _load_cbg_database(self):
        """Load INA-CBG code database (simplified - in production load from BPJS master data)."""
        # This would normally load from BPJS master data file
        # For now, we'll generate common codes programmatically
        for category in CBGCategory:
            for severity in SeverityLevel:
                for sub in range(1, 50):  # 001-049
                    sub_code = f"{sub:03d}"
                    code = f"{category.value}{self.version.value[-2:]}{severity.value}{sub_code}"
                    base_tariff = self.BASE_TARIFFS.get(category, 500000)
                    adjusted = base_tariff * self.SEVERITY_MULTIPLIERS[severity]

                    self._cbg_database[code] = CBGCode(
                        code=code,
                        version=self.version,
                        category=category,
                        severity=severity,
                        sub_code=sub_code,
                        description=f"{category.name} - Severity {severity.name} - Sub {sub_code}",
                        base_tariff=adjusted,
                    )

    def validate_code(self, cbg_code: str) -> Tuple[bool, List[str]]:
        """Validate INA-CBG code format and existence."""
        errors = []

        # Format validation
        if not re.match(r'^[A-Z]\d{2}[1-4]\d{3}$', cbg_code):
            errors.append(f"Invalid CBG code format: {cbg_code}. Expected format: [A-Z]YY[1-4]NNN")
            return False, errors

        # Version check
        version_str = cbg_code[1:3]
        expected_version = self.version.value[-2:]
        if version_str != expected_version:
            errors.append(f"Version mismatch: code has {version_str}, expected {expected_version}")

        # Category check
        cat_char = cbg_code[0]
        try:
            CBGCategory(cat_char)
        except ValueError:
            errors.append(f"Invalid category code: {cat_char}")

        # Severity check
        sev_char = cbg_code[3]
        try:
            SeverityLevel(sev_char)
        except ValueError:
            errors.append(f"Invalid severity level: {sev_char}")

        # Existence check
        if cbg_code not in self._cbg_database:
            errors.append(f"CBG code not found in master data: {cbg_code}")

        return len(errors) == 0, errors

    def group_claim(self, context: ClaimValidationContext) -> CBGGroupingResult:
        """
        Perform INA-CBG grouping based on claim context.
        Implements simplified grouping logic per BPJS Kesehatan rules.
        """
        errors = []
        warnings = []

        # Determine primary diagnosis category
        primary_category = self._determine_category(context.diagnosis_codes, context.procedure_codes)

        # Determine severity based on comorbidities, complications, age, LOS
        severity = self._determine_severity(context)

        # Determine sub-code based on specific procedure/diagnosis combination
        sub_code = self._determine_sub_code(context, primary_category)

        # Build CBG code
        cbg_code_str = f"{primary_category.value}{self.version.value[-2:]}{severity.value}{sub_code}"

        # Validate the generated code
        is_valid, val_errors = self.validate_code(cbg_code_str)
        errors.extend(val_errors)

        cbg_code = self._cbg_database.get(cbg_code_str)
        if not cbg_code:
            # Fallback
            cbg_code = CBGCode(
                code=cbg_code_str,
                version=self.version,
                category=primary_category,
                severity=severity,
                sub_code=sub_code,
                description=f"Auto-grouped: {primary_category.name}",
                base_tariff=self.BASE_TARIFFS.get(primary_category, 500000) * self.SEVERITY_MULTIPLIERS[severity],
            )

        # Calculate tariff
        base_tariff = cbg_code.base_tariff
        adjusted_tariff = self._calculate_adjusted_tariff(base_tariff, context)

        # LOS validation
        los_warnings = self._validate_los(context, primary_category)
        warnings.extend(los_warnings)

        # Component breakdown
        components = self._calculate_components(base_tariff, context)

        return CBGGroupingResult(
            cbg_code=cbg_code,
            base_tariff=base_tariff,
            adjusted_tariff=adjusted_tariff,
            components=components,
            los_days=context.los_days,
            is_valid=is_valid,
            validation_errors=errors,
            warnings=warnings,
        )

    def _determine_category(self, diagnosis_codes: List[str], procedure_codes: List[str]) -> CBGCategory:
        """Determine CBG category from diagnosis/procedure codes."""
        # Simplified mapping - real implementation uses BPJS grouper logic
        # Check procedures first (more specific)
        for proc in procedure_codes:
            if proc.startswith(("0", "1", "2", "3", "4", "5")):  # Surgery codes
                return CBGCategory.BEDAH
            if proc.startswith("8"):  # Radiology
                return CBGCategory.RADIOLOGI
            if proc.startswith("9"):  # Lab
                return CBGCategory.LABORATORIUM

        # Check diagnosis
        for diag in diagnosis_codes:
            if diag.startswith(("C", "D0", "D1", "D2", "D3", "D4")):  # Neoplasms -> surgery
                return CBGCategory.BEDAH
            if diag.startswith("K") and diag[1:3].isdigit():  # Digestive
                return CBGCategory.BEDAH
            if diag.startswith("I"):  # Circulatory -> intensive
                return CBGCategory.INTENSIF
            if diag.startswith("J"):  # Respiratory -> kamar
                return CBGCategory.KAMAR

        return CBGCategory.KAMAR  # Default

    def _determine_severity(self, context: ClaimValidationContext) -> SeverityLevel:
        """Determine severity level based on clinical factors."""
        severity_score = 0

        # Age factor
        if context.patient_age >= 65:
            severity_score += 2
        elif context.patient_age >= 45:
            severity_score += 1

        # Comorbidities
        severity_score += min(len(context.comorbidity_codes), 3)

        # Complications
        severity_score += min(len(context.complication_codes) * 2, 4)

        # LOS factor
        if context.los_days > 14:
            severity_score += 2
        elif context.los_days > 7:
            severity_score += 1

        # Emergency
        if context.is_emergency:
            severity_score += 1

        # Map score to severity
        if severity_score >= 7:
            return SeverityLevel.SANGAT_TINGGI
        elif severity_score >= 4:
            return SeverityLevel.TINGGI
        elif severity_score >= 2:
            return SeverityLevel.SEDANG
        return SeverityLevel.RENDAH

    def _determine_sub_code(self, context: ClaimValidationContext, category: CBGCategory) -> str:
        """Determine sub-code (001-049) based on specific clinical details."""
        # Simplified - real implementation uses detailed grouper tables
        sub_base = 1

        # Add offset based on primary procedure
        if context.procedure_codes:
            proc_hash = hash(context.procedure_codes[0]) % 20
            sub_base += proc_hash

        # Add offset for diagnosis
        if context.diagnosis_codes:
            diag_hash = hash(context.diagnosis_codes[0]) % 15
            sub_base += diag_hash

        # Add for facility class
        class_offset = {"A": 10, "B": 5, "C": 0, "D": -5}.get(context.facility_class, 0)
        sub_base += class_offset

        # Clamp to valid range
        sub_base = max(1, min(49, sub_base))
        return f"{sub_base:03d}"

    def _calculate_adjusted_tariff(self, base_tariff: float, context: ClaimValidationContext) -> float:
        """Calculate final adjusted tariff with all multipliers."""
        tariff = base_tariff

        # Facility class multiplier
        class_mult = self.FACILITY_CLASS_MULTIPLIERS.get(context.facility_class, 1.0)
        tariff *= class_mult

        # Emergency multiplier
        if context.is_emergency:
            tariff *= self.EMERGENCY_MULTIPLIER

        # National referral multiplier
        if context.is_national_referral:
            tariff *= self.NATIONAL_REFERRAL_MULTIPLIER

        # LOS adjustment (per diem for extended stay)
        los_threshold = self.LOS_THRESHOLDS.get(
            CBGCategory.KAMAR, {"standard": 7}
        )["standard"]
        if context.los_days > los_threshold:
            # Per diem rate (simplified)
            per_diem = base_tariff * 0.05
            tariff += per_diem * (context.los_days - los_threshold)

        return round(tariff, 2)

    def _validate_los(self, context: ClaimValidationContext, category: CBGCategory) -> List[str]:
        """Validate Length of Stay against thresholds."""
        warnings = []
        thresholds = self.LOS_THRESHOLDS.get(category, {"min": 1, "max": 30, "standard": 7})

        if context.los_days < thresholds["min"]:
            warnings.append(f"LOS ({context.los_days}) below minimum ({thresholds['min']}) for {category.name}")
        elif context.los_days > thresholds["max"]:
            warnings.append(f"LOS ({context.los_days}) exceeds maximum ({thresholds['max']}) for {category.name}")
        elif context.los_days > thresholds["standard"] * 1.5:
            warnings.append(f"LOS ({context.los_days}) significantly exceeds standard ({thresholds['standard']}) for {category.name}")

        return warnings

    def _calculate_components(self, base_tariff: float, context: ClaimValidationContext) -> Dict[str, float]:
        """Calculate tariff component breakdown."""
        return {
            "base_tariff": round(base_tariff, 2),
            "facility_class_adj": round(base_tariff * (self.FACILITY_CLASS_MULTIPLIERS.get(context.facility_class, 1.0) - 1), 2),
            "emergency_adj": round(base_tariff * (self.EMERGENCY_MULTIPLIER - 1), 2) if context.is_emergency else 0,
            "referral_adj": round(base_tariff * (self.NATIONAL_REFERRAL_MULTIPLIER - 1), 2) if context.is_national_referral else 0,
            "los_adj": 0,  # Calculated separately
        }

    def get_cbg_info(self, cbg_code: str) -> Optional[CBGCode]:
        """Get CBG code info from database."""
        return self._cbg_database.get(cbg_code)

    def search_cbg(self, category: Optional[CBGCategory] = None,
                   severity: Optional[SeverityLevel] = None,
                   keyword: str = "") -> List[CBGCode]:
        """Search CBG codes."""
        results = []
        for code in self._cbg_database.values():
            if category and code.category != category:
                continue
            if severity and code.severity != severity:
                continue
            if keyword and keyword.lower() not in code.description.lower():
                continue
            results.append(code)
        return results


# Singleton instance
_validator_instance: Optional[INACBGValidator] = None


def get_ina_cbg_validator(version: CBGVersion = CBGVersion.V5_2024) -> INACBGValidator:
    """Get or create INA-CBG validator singleton."""
    global _validator_instance
    if _validator_instance is None or _validator_instance.version != version:
        _validator_instance = INACBGValidator(version)
    return _validator_instance