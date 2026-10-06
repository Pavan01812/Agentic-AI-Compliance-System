"""
EPFO Registration compliance workflow.

This module coordinates registration evidence with the deterministic
registration rules.
"""

from typing import Any, Dict

from ..rules.registration_rules import check_registration
from ..rules.common import readiness


COMPLIANCE_ID = "EPFO.REGISTRATION"


def assess_registration(
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Assess EPFO establishment registration.

    Parameters
    ----------
    context:
        Company/establishment context.

    evidence:
        Registration-related evidence.

    Returns
    -------
    dict
        Structured EPFO compliance assessment.
    """

    context = context or {}
    evidence = evidence or {}

    # The deterministic registration rules expect the complete
    # evidence structure:
    #
    # {
    #     "registration": {
    #         "establishment_code": "...",
    #         "establishment_name": "...",
    #         "pan": "...",
    #         "coverage_basis": "..."
    #     }
    # }
    #
    # Therefore, pass the complete evidence dictionary directly
    # to check_registration().
    findings = check_registration(
        context=context,
        evidence=evidence,
    )

    registration_evidence = evidence.get("registration")

    if isinstance(registration_evidence, dict):
        evidence_used = list(registration_evidence.keys())
    else:
        evidence_used = []

    return {
        "compliance_id": COMPLIANCE_ID,
        "name": "EPFO Registration",
        "category": "REGISTRATION",
        "readiness": readiness(findings),
        "findings": findings,
        "evidence_used": evidence_used,
    }