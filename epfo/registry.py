"""
EPFO compliance registry.

The registry provides a single lookup point for all EPFO V1
compliance modules.
"""

from typing import Callable, Dict, Any

from .compliance.registration import assess_registration
from .compliance.form5a import assess_form5a
from .compliance.uan import assess_uan
from .compliance.ecr import assess_ecr
from .compliance.contribution import assess_contribution


EPFO_COMPLIANCE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "EPFO.REGISTRATION": {
        "name": "EPFO Establishment Registration",
        "category": "REGISTRATION",
        "description": (
            "Assessment of EPFO establishment registration details, "
            "establishment identity, PAN and coverage basis."
        ),
        "assessor": assess_registration,
    },

    "EPFO.FORM5A": {
        "name": "EPFO Form 5A",
        "category": "OWNERSHIP_AND_ESTABLISHMENT",
        "description": (
            "Assessment of Form 5A establishment ownership and "
            "identification information."
        ),
        "assessor": assess_form5a,
    },

    "EPFO.UAN": {
        "name": "Universal Account Number Compliance",
        "category": "MEMBER_REGISTRATION",
        "description": (
            "Assessment of UAN records, employee identity, "
            "establishment mapping and joining information."
        ),
        "assessor": assess_uan,
    },

    "EPFO.ECR": {
        "name": "Electronic Challan-cum-Return",
        "category": "RETURN_FILING",
        "description": (
            "Assessment of ECR period, establishment, member rows, "
            "wages, contribution fields and data consistency."
        ),
        "assessor": assess_ecr,
    },

    "EPFO.CONTRIBUTION": {
        "name": "EPFO Contribution Reconciliation",
        "category": "CONTRIBUTION",
        "description": (
            "Reconciliation of ECR contribution totals, challan "
            "amounts and payment amounts."
        ),
        "assessor": assess_contribution,
    },
}


def get_compliance(compliance_id: str) -> Dict[str, Any]:
    """
    Return a registered EPFO compliance module.

    Raises:
        KeyError: If the compliance ID is not registered.
    """

    if compliance_id not in EPFO_COMPLIANCE_REGISTRY:
        raise KeyError(
            f"Unknown EPFO compliance ID: {compliance_id}"
        )

    return EPFO_COMPLIANCE_REGISTRY[compliance_id]


def get_assessor(compliance_id: str) -> Callable:
    """
    Return the assessment function for a compliance module.
    """

    compliance = get_compliance(compliance_id)
    return compliance["assessor"]


def list_compliances() -> list[Dict[str, Any]]:
    """
    Return all registered EPFO compliance modules.
    """

    return [
        {
            "compliance_id": compliance_id,
            "name": metadata["name"],
            "category": metadata["category"],
            "description": metadata["description"],
        }
        for compliance_id, metadata in EPFO_COMPLIANCE_REGISTRY.items()
    ]


def is_supported(compliance_id: str) -> bool:
    """
    Check whether an EPFO compliance ID is supported.
    """

    return compliance_id in EPFO_COMPLIANCE_REGISTRY