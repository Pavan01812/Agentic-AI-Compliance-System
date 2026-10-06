"""
EPFO document and evidence type definitions.

These identifiers are used by:

- Document AI
- evidence routing
- compliance modules
- field extraction
- audit trails
- tests
"""

from enum import Enum
from typing import Dict, Any


class EPFODocumentType(str, Enum):
    """
    Canonical EPFO document/evidence identifiers.
    """

    # ---------------------------------------------------------------
    # Establishment
    # ---------------------------------------------------------------

    REGISTRATION_CERTIFICATE = (
        "REGISTRATION_CERTIFICATE"
    )

    ESTABLISHMENT_RECORD = (
        "ESTABLISHMENT_RECORD"
    )

    # ---------------------------------------------------------------
    # Form 5A
    # ---------------------------------------------------------------

    FORM_5A = "FORM_5A"

    # ---------------------------------------------------------------
    # Employee / UAN
    # ---------------------------------------------------------------

    FORM_11 = "FORM_11"

    UAN_MEMBER_DATA = (
        "UAN_MEMBER_DATA"
    )

    MEMBER_REGISTRATION = (
        "MEMBER_REGISTRATION"
    )

    # ---------------------------------------------------------------
    # ECR
    # ---------------------------------------------------------------

    ECR_FILE = "ECR_FILE"

    ECR_RETURN = "ECR_RETURN"

    ECR_ACKNOWLEDGEMENT = (
        "ECR_ACKNOWLEDGEMENT"
    )

    # ---------------------------------------------------------------
    # Contribution / payment
    # ---------------------------------------------------------------

    CHALLAN = "CHALLAN"

    PAYMENT_RECEIPT = (
        "PAYMENT_RECEIPT"
    )

    TRRN_RECORD = "TRRN_RECORD"


# -------------------------------------------------------------------
# Document metadata
# -------------------------------------------------------------------

EPFO_DOCUMENT_METADATA: Dict[
    str,
    Dict[str, Any]
] = {

    EPFODocumentType.REGISTRATION_CERTIFICATE.value: {
        "name": "EPFO Registration Certificate",
        "category": "REGISTRATION",
        "format": [
            "PDF",
            "IMAGE",
        ],
        "structured": False,
        "table_based": False,
        "description": (
            "Evidence of EPFO establishment registration."
        ),
    },

    EPFODocumentType.ESTABLISHMENT_RECORD.value: {
        "name": "EPFO Establishment Record",
        "category": "REGISTRATION",
        "format": [
            "PDF",
            "IMAGE",
            "JSON",
        ],
        "structured": True,
        "table_based": False,
        "description": (
            "Structured or extracted establishment information."
        ),
    },

    EPFODocumentType.FORM_5A.value: {
        "name": "EPFO Form 5A",
        "category": "FORM",
        "format": [
            "PDF",
            "IMAGE",
        ],
        "structured": False,
        "table_based": False,
        "description": (
            "Employer/establishment Form 5A information."
        ),
    },

    EPFODocumentType.FORM_11.value: {
        "name": "EPFO Form 11",
        "category": "MEMBER",
        "format": [
            "PDF",
            "IMAGE",
        ],
        "structured": False,
        "table_based": False,
        "description": (
            "Employee declaration/form used for member onboarding."
        ),
    },

    EPFODocumentType.UAN_MEMBER_DATA.value: {
        "name": "UAN Member Data",
        "category": "MEMBER",
        "format": [
            "CSV",
            "XLSX",
            "JSON",
            "PDF",
        ],
        "structured": True,
        "table_based": True,
        "description": (
            "Member-level UAN and establishment mapping data."
        ),
    },

    EPFODocumentType.MEMBER_REGISTRATION.value: {
        "name": "EPFO Member Registration Record",
        "category": "MEMBER",
        "format": [
            "PDF",
            "CSV",
            "XLSX",
            "JSON",
        ],
        "structured": True,
        "table_based": True,
        "description": (
            "Evidence of employee/member registration."
        ),
    },

    EPFODocumentType.ECR_FILE.value: {
        "name": "Electronic Challan-cum-Return File",
        "category": "ECR",
        "format": [
            "TXT",
            "CSV",
            "XLSX",
            "JSON",
        ],
        "structured": True,
        "table_based": True,
        "description": (
            "Member-level ECR data used for return validation."
        ),
    },

    EPFODocumentType.ECR_RETURN.value: {
        "name": "Electronic Challan-cum-Return",
        "category": "ECR",
        "format": [
            "PDF",
            "CSV",
            "XLSX",
            "JSON",
        ],
        "structured": True,
        "table_based": True,
        "description": (
            "ECR return information for an assessment period."
        ),
    },

    EPFODocumentType.ECR_ACKNOWLEDGEMENT.value: {
        "name": "ECR Acknowledgement",
        "category": "ECR",
        "format": [
            "PDF",
        ],
        "structured": False,
        "table_based": False,
        "description": (
            "Evidence acknowledging ECR processing."
        ),
    },

    EPFODocumentType.CHALLAN.value: {
        "name": "EPFO Challan",
        "category": "PAYMENT",
        "format": [
            "PDF",
            "IMAGE",
        ],
        "structured": False,
        "table_based": False,
        "description": (
            "EPFO contribution challan/payment demand evidence."
        ),
    },

    EPFODocumentType.PAYMENT_RECEIPT.value: {
        "name": "EPFO Payment Receipt",
        "category": "PAYMENT",
        "format": [
            "PDF",
            "IMAGE",
        ],
        "structured": False,
        "table_based": False,
        "description": (
            "Evidence of payment against the contribution challan."
        ),
    },

    EPFODocumentType.TRRN_RECORD.value: {
        "name": "TRRN Record",
        "category": "PAYMENT",
        "format": [
            "PDF",
            "JSON",
            "CSV",
        ],
        "structured": True,
        "table_based": False,
        "description": (
            "Temporary Return Reference Number and "
            "associated payment metadata."
        ),
    },
}


def get_document_metadata(
    document_type: str,
) -> Dict[str, Any]:
    """
    Return metadata for an EPFO document type.
    """

    return EPFO_DOCUMENT_METADATA.get(
        document_type,
        {},
    )


def is_supported_document_type(
    document_type: str,
) -> bool:
    """
    Check whether an EPFO document type is supported.
    """

    return (
        document_type
        in EPFO_DOCUMENT_METADATA
    )


def list_document_types():
    """
    Return all supported EPFO document identifiers.
    """

    return list(
        EPFO_DOCUMENT_METADATA.keys()
    )