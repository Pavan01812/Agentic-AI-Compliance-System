"""
EPFO legal and authoritative reference sources.

Important design principle:
--------------------------------
The compliance engine should never invent legal requirements.

This module stores authoritative sources used to support EPFO rules.
Rules reference source IDs instead of embedding URLs or legal metadata
directly inside rule implementations.

This gives us:
    Rule -> Legal Source -> Official EPFO Document

The system can therefore maintain legal provenance for every finding.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass(frozen=True)
class LegalSource:
    """
    Represents an authoritative EPFO legal/reference source.
    """

    source_id: str
    title: str
    authority: str
    source_type: str
    url: str
    description: str
    status: str = "ACTIVE"
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None
    last_verified: Optional[str] = None

    def to_dict(self) -> dict:
        """Return the source as a serializable dictionary."""
        return asdict(self)


# ---------------------------------------------------------------------------
# AUTHORITATIVE SOURCES
# ---------------------------------------------------------------------------

LEGAL_SOURCES: Dict[str, LegalSource] = {

    "EPFO_FORM_5A": LegalSource(
        source_id="EPFO_FORM_5A",
        title="Form 5A / Return of Ownership",
        authority="Employees' Provident Fund Organisation",
        source_type="OFFICIAL_EPFO_GUIDANCE",
        url=(
            "https://www.epfindia.gov.in/site_docs/"
            "PDFs/MiscPDFs/Employer_Information_Booklet.pdf"
        ),
        description=(
            "Official EPFO employer information describing Form 5A, "
            "ownership particulars, establishment details and updating "
            "requirements."
        ),
        status="ACTIVE",
        last_verified="2026-10-05",
    ),

    "EPFO_SCHEME_1952": LegalSource(
        source_id="EPFO_SCHEME_1952",
        title="Employees' Provident Funds Scheme, 1952",
        authority="Government of India / Employees' Provident Fund Organisation",
        source_type="STATUTORY_SCHEME",
        url=(
            "https://www.epfindia.gov.in/site_docs/"
            "PDFs/Downloads_PDFs/EPFScheme.pdf"
        ),
        description=(
            "Official text of the Employees' Provident Funds Scheme, 1952. "
            "Used as the principal statutory reference for EPF scheme "
            "requirements."
        ),
        status="ACTIVE",
        last_verified="2026-10-05",
    ),

    "EPFO_UAN_GUIDANCE": LegalSource(
        source_id="EPFO_UAN_GUIDANCE",
        title="User Manual on UAN Functions",
        authority="Employees' Provident Fund Organisation",
        source_type="OFFICIAL_EPFO_GUIDANCE",
        url=(
            "https://www.epfindia.gov.in/site_docs/"
            "PDFs/UAN_PDFs/UAN_ForEmployers/"
            "UserManual_Ver1.4_Employers_new.pdf"
        ),
        description=(
            "Official EPFO employer guidance covering UAN functions, "
            "linking of member IDs, previous employment/UAN information "
            "and first-time membership declarations."
        ),
        status="ACTIVE",
        last_verified="2026-10-05",
    ),

    "EPFO_ECR_REVAMP_2025": LegalSource(
        source_id="EPFO_ECR_REVAMP_2025",
        title="Revamped Electronic Challan-cum-Return (ECR)",
        authority="Employees' Provident Fund Organisation",
        source_type="OFFICIAL_EPFO_CIRCULAR",
        url=(
            "https://www.epfindia.gov.in/site_docs/"
            "PDFs/Circulars/Y2025-2026/ECRRevamp_26092025.pdf"
        ),
        description=(
            "EPFO Circular No. Compliance/ECR Revamp/2025/12997 dated "
            "26 September 2025 introducing the revamped ECR system "
            "for wage month September 2025 onwards."
        ),
        status="ACTIVE",
        effective_from="2025-09-01",
        last_verified="2026-10-05",
    ),

    "EPFO_EMPLOYER_PORTAL": LegalSource(
        source_id="EPFO_EMPLOYER_PORTAL",
        title="EPFO Employer Unified Portal",
        authority="Employees' Provident Fund Organisation",
        source_type="OFFICIAL_EPFO_PORTAL",
        url=(
            "https://unifiedportal-emp.epfindia.gov.in/epfo/"
        ),
        description=(
            "Official EPFO employer portal providing establishment "
            "registration, ECR-related services and employer compliance "
            "workflows."
        ),
        status="ACTIVE",
        last_verified="2026-10-05",
    ),
}


# ---------------------------------------------------------------------------
# RULE -> SOURCE MAPPING
# ---------------------------------------------------------------------------

RULE_SOURCE_MAP: Dict[str, List[str]] = {

    # -----------------------------------------------------------------------
    # REGISTRATION
    # -----------------------------------------------------------------------

    "EPFO.REGISTRATION.REQUIRED_ESTABLISHMENT_CODE": [
        "EPFO_SCHEME_1952",
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.REGISTRATION.REQUIRED_ESTABLISHMENT_NAME": [
        "EPFO_FORM_5A",
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.REGISTRATION.REQUIRED_PAN": [
        "EPFO_FORM_5A",
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.REGISTRATION.REQUIRED_COVERAGE_BASIS": [
        "EPFO_SCHEME_1952",
    ],

    "EPFO.REGISTRATION.ESTABLISHMENT_CODE_FORMAT": [
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.REGISTRATION.PAN_FORMAT": [
        "EPFO_FORM_5A",
    ],

    "EPFO.REGISTRATION.NAME_CROSS_CHECK": [
        "EPFO_FORM_5A",
    ],

    "EPFO.REGISTRATION.PAN_CROSS_CHECK": [
        "EPFO_FORM_5A",
    ],

    "EPFO.REGISTRATION.ESTABLISHMENT_CODE_CROSS_CHECK": [
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.REGISTRATION.COVERAGE_BASIS_UNKNOWN": [
        "EPFO_SCHEME_1952",
    ],

    # -----------------------------------------------------------------------
    # FORM 5A
    # -----------------------------------------------------------------------

    "EPFO.FORM5A.REQUIRED_ESTABLISHMENT_NAME": [
        "EPFO_FORM_5A",
    ],

    "EPFO.FORM5A.REQUIRED_PAN": [
        "EPFO_FORM_5A",
    ],

    "EPFO.FORM5A.REQUIRED_COVERAGE_BASIS": [
        "EPFO_FORM_5A",
        "EPFO_SCHEME_1952",
    ],

    "EPFO.FORM5A.PAN_FORMAT": [
        "EPFO_FORM_5A",
    ],

    "EPFO.FORM5A.PAN_MATCH": [
        "EPFO_FORM_5A",
    ],

    "EPFO.FORM5A.NAME_MATCH": [
        "EPFO_FORM_5A",
    ],

    "EPFO.FORM5A.ESTABLISHMENT_CODE_PRESENT": [
        "EPFO_FORM_5A",
    ],

    "EPFO.FORM5A.ESTABLISHMENT_CODE_MATCH": [
        "EPFO_FORM_5A",
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.FORM5A.COVERAGE_BASIS_UNKNOWN": [
        "EPFO_SCHEME_1952",
    ],

    # -----------------------------------------------------------------------
    # UAN
    # -----------------------------------------------------------------------

    "EPFO.UAN.RECORDS_PRESENT": [
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.UAN.REQUIRED_UAN": [
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.UAN.INVALID_UAN": [
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.UAN.DUPLICATE_UAN": [
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.UAN.EMPLOYEE_NAME_MISSING": [
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.UAN.ESTABLISHMENT_MAPPING_MISMATCH": [
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.UAN.ESTABLISHMENT_MAPPING_MISSING": [
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.UAN.DATE_OF_JOINING_MISSING": [
        "EPFO_UAN_GUIDANCE",
    ],

    # -----------------------------------------------------------------------
    # ECR
    # -----------------------------------------------------------------------

    "EPFO.ECR.PERIOD_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.ESTABLISHMENT_CODE_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.ECR.ROWS_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.UAN_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
        "EPFO_UAN_GUIDANCE",
    ],

    "EPFO.ECR.INVALID_UAN": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.DUPLICATE_UAN": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.EMPLOYEE_NAME_MISSING": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.INVALID_WAGES": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.INVALID_EPF_WAGES": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.INVALID_EPS_WAGES": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.INVALID_EDLI_WAGES": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.INVALID_EMPLOYEE_SHARE": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.INVALID_EMPLOYER_SHARE": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.WAGE_COMPONENT_EXCEEDS_WAGES": [
        "EPFO_ECR_REVAMP_2025",
        "EPFO_SCHEME_1952",
    ],

    "EPFO.ECR.INVALID_NCP_DAYS": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.ESTABLISHMENT_CODE_MISMATCH": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.PERIOD_MISMATCH": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.ECR.AGGREGATE_SUMMARY": [
        "EPFO_ECR_REVAMP_2025",
    ],

    # -----------------------------------------------------------------------
    # CONTRIBUTION
    # -----------------------------------------------------------------------

    "EPFO.CONTRIBUTION.PERIOD_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.CONTRIBUTION.ECR_TOTAL_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.CONTRIBUTION.CHALLAN_AMOUNT_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.CONTRIBUTION.PAID_AMOUNT_REQUIRED": [
        "EPFO_ECR_REVAMP_2025",
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.CONTRIBUTION.ECR_CHALLAN_MATCH": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.CONTRIBUTION.CHALLAN_PAYMENT_MATCH": [
        "EPFO_ECR_REVAMP_2025",
    ],

    "EPFO.CONTRIBUTION.TRRN_MISSING": [
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.CONTRIBUTION.PAYMENT_DATE_MISSING": [
        "EPFO_EMPLOYER_PORTAL",
    ],

    "EPFO.CONTRIBUTION.RECONCILIATION_SUMMARY": [
        "EPFO_ECR_REVAMP_2025",
    ],
}


# ---------------------------------------------------------------------------
# SOURCE LOOKUP FUNCTIONS
# ---------------------------------------------------------------------------

def get_source(source_id: str) -> Optional[LegalSource]:
    """
    Return a legal source by source ID.

    Example:
        get_source("EPFO_SCHEME_1952")
    """
    return LEGAL_SOURCES.get(source_id)


def get_sources() -> List[LegalSource]:
    """
    Return all registered legal sources.
    """
    return list(LEGAL_SOURCES.values())


def get_sources_for_rule(rule_id: str) -> List[LegalSource]:
    """
    Return all legal sources associated with a rule.
    """
    source_ids = RULE_SOURCE_MAP.get(rule_id, [])

    return [
        LEGAL_SOURCES[source_id]
        for source_id in source_ids
        if source_id in LEGAL_SOURCES
    ]


def get_primary_source_for_rule(rule_id: str) -> Optional[LegalSource]:
    """
    Return the first/primary legal source for a rule.

    The first source in RULE_SOURCE_MAP is treated as the primary
    provenance source.
    """
    sources = get_sources_for_rule(rule_id)

    if not sources:
        return None

    return sources[0]


def validate_source_manifest() -> dict:
    """
    Validate the internal legal source registry.

    Checks:
    - Every mapped source ID exists.
    - Every source has a valid URL.
    - Every source has a title.
    - Every source has an authority.

    Returns:
        {
            "valid": bool,
            "errors": [...],
            "source_count": int,
            "mapped_rule_count": int
        }
    """

    errors: List[str] = []

    for source_id, source in LEGAL_SOURCES.items():

        if source.source_id != source_id:
            errors.append(
                f"Source key mismatch: {source_id} != {source.source_id}"
            )

        if not source.title.strip():
            errors.append(
                f"Missing title for source: {source_id}"
            )

        if not source.authority.strip():
            errors.append(
                f"Missing authority for source: {source_id}"
            )

        if not source.url.startswith(("http://", "https://")):
            errors.append(
                f"Invalid URL for source: {source_id}"
            )

    for rule_id, source_ids in RULE_SOURCE_MAP.items():

        if not rule_id.startswith("EPFO."):
            errors.append(
                f"Invalid EPFO rule ID: {rule_id}"
            )

        if not source_ids:
            errors.append(
                f"No legal source mapped to rule: {rule_id}"
            )

        for source_id in source_ids:
            if source_id not in LEGAL_SOURCES:
                errors.append(
                    f"Unknown source '{source_id}' "
                    f"mapped to rule '{rule_id}'"
                )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "source_count": len(LEGAL_SOURCES),
        "mapped_rule_count": len(RULE_SOURCE_MAP),
    }