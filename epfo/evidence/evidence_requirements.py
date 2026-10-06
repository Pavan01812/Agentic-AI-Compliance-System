"""
EPFO evidence requirements.

This module defines minimum evidence requirements for each compliance
workflow.

Important distinction:

- REQUIRED means the evidence is needed for a reliable assessment.
- OPTIONAL means it strengthens the assessment but is not always needed.
- RECOMMENDED means it should normally be supplied when available.
"""

from typing import Dict, List, Any


EVIDENCE_REQUIREMENTS: Dict[
    str,
    Dict[str, Any]
] = {

    # ===============================================================
    # Registration
    # ===============================================================

    "EPFO.REGISTRATION": {

        "required": [
            {
                "evidence_type": "REGISTRATION_CERTIFICATE",
                "description": (
                    "Evidence of EPFO establishment registration."
                ),
            },
            {
                "evidence_type": "ESTABLISHMENT_RECORD",
                "description": (
                    "Establishment identity and registration data."
                ),
            },
        ],

        "recommended": [
            {
                "evidence_type": "FORM_5A",
                "description": (
                    "Form 5A for establishment/PAN cross-validation."
                ),
            },
        ],

        "fields": [
            "establishment_code",
            "establishment_name",
            "pan",
            "registration_date",
            "coverage_basis",
        ],
    },

    # ===============================================================
    # Form 5A
    # ===============================================================

    "EPFO.FORM5A": {

        "required": [
            {
                "evidence_type": "FORM_5A",
                "description": (
                    "Form 5A document."
                ),
            },
        ],

        "recommended": [
            {
                "evidence_type": "REGISTRATION_CERTIFICATE",
                "description": (
                    "Registration evidence for cross-validation."
                ),
            },
            {
                "evidence_type": "ESTABLISHMENT_RECORD",
                "description": (
                    "Establishment identity context."
                ),
            },
        ],

        "fields": [
            "establishment_name_as_per_pan",
            "pan",
            "coverage_basis",
            "establishment_code",
            "branches",
        ],
    },

    # ===============================================================
    # UAN
    # ===============================================================

    "EPFO.UAN": {

        "required": [
            {
                "evidence_type": "UAN_MEMBER_DATA",
                "description": (
                    "UAN/member-level records."
                ),
            },
        ],

        "recommended": [
            {
                "evidence_type": "FORM_11",
                "description": (
                    "Employee declaration supporting onboarding data."
                ),
            },
            {
                "evidence_type": "MEMBER_REGISTRATION",
                "description": (
                    "Member registration evidence."
                ),
            },
        ],

        "fields": [
            "uan",
            "member_id",
            "employee_name",
            "date_of_joining",
            "first_time_member",
            "previous_uan",
            "establishment_code",
        ],
    },

    # ===============================================================
    # ECR
    # ===============================================================

    "EPFO.ECR": {

        "required": [
            {
                "evidence_type": "ECR_FILE",
                "description": (
                    "Member-level ECR data."
                ),
            },
        ],

        "recommended": [
            {
                "evidence_type": "ECR_RETURN",
                "description": (
                    "Processed ECR return evidence."
                ),
            },
            {
                "evidence_type": "ECR_ACKNOWLEDGEMENT",
                "description": (
                    "ECR acknowledgement evidence."
                ),
            },
            {
                "evidence_type": "UAN_MEMBER_DATA",
                "description": (
                    "UAN/member master data for cross-validation."
                ),
            },
        ],

        "fields": [
            "period",
            "establishment_code",
            "uan",
            "employee_name",
            "wages",
            "epf_wages",
            "eps_wages",
            "edli_wages",
            "employee_share",
            "employer_share",
            "ncp_days",
        ],
    },

    # ===============================================================
    # Contribution
    # ===============================================================

    "EPFO.CONTRIBUTION": {

        "required": [
            {
                "evidence_type": "CHALLAN",
                "description": (
                    "Contribution challan evidence."
                ),
            },
            {
                "evidence_type": "PAYMENT_RECEIPT",
                "description": (
                    "Payment evidence."
                ),
            },
        ],

        "recommended": [
            {
                "evidence_type": "ECR_RETURN",
                "description": (
                    "ECR return for amount reconciliation."
                ),
            },
            {
                "evidence_type": "TRRN_RECORD",
                "description": (
                    "TRRN/payment reference information."
                ),
            },
        ],

        "fields": [
            "period",
            "ecr_total",
            "employee_total",
            "employer_total",
            "challan_amount",
            "paid_amount",
            "trrn",
            "payment_date",
        ],
    },
}


def get_required_evidence(
    compliance_id: str,
) -> List[Dict[str, Any]]:
    """
    Return required evidence for a compliance module.
    """

    config = EVIDENCE_REQUIREMENTS.get(
        compliance_id,
        {},
    )

    return config.get(
        "required",
        [],
    )


def get_recommended_evidence(
    compliance_id: str,
) -> List[Dict[str, Any]]:
    """
    Return recommended evidence for a compliance module.
    """

    config = EVIDENCE_REQUIREMENTS.get(
        compliance_id,
        {},
    )

    return config.get(
        "recommended",
        [],
    )


def get_required_fields(
    compliance_id: str,
) -> List[str]:
    """
    Return fields expected for a compliance module.
    """

    config = EVIDENCE_REQUIREMENTS.get(
        compliance_id,
        {},
    )

    return config.get(
        "fields",
        [],
    )


def validate_evidence_presence(
    compliance_id: str,
    available_document_types: List[str],
) -> Dict[str, Any]:
    """
    Determine whether the minimum evidence set is available.

    This does not assess the content of the documents.
    It only assesses evidence presence.
    """

    config = EVIDENCE_REQUIREMENTS.get(
        compliance_id
    )

    if not config:

        return {
            "compliance_id": compliance_id,
            "known": False,
            "ready_for_content_assessment": False,
            "missing": [],
            "available": [],
        }

    required_types = {
        item["evidence_type"]
        for item in config.get(
            "required",
            [],
        )
    }

    available_types = set(
        available_document_types
    )

    missing = sorted(
        required_types - available_types
    )

    return {
        "compliance_id": compliance_id,
        "known": True,
        "ready_for_content_assessment": (
            len(missing) == 0
        ),
        "missing": missing,
        "available": sorted(
            available_types
        ),
    }