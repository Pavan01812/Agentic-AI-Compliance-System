"""
EPFO Form 5A compliance workflow.
"""

from typing import Any, Dict

from ..rules.form5a_rules import check_form5a
from ..rules.common import readiness


COMPLIANCE_ID = "EPFO.FORM5A"


def assess_form5a(
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Assess EPFO Form 5A evidence.

    Parameters
    ----------
    context:
        Establishment/company context.

    evidence:
        Form 5A evidence.

    Returns
    -------
    dict
        Structured Form 5A compliance result.
    """

    context = context or {}
    evidence = evidence or {}

    form5a_evidence = evidence.get(
        "form5a",
        evidence
    )

    findings = check_form5a(
        context=context,
        form=form5a_evidence,
    )

    return {
        "compliance_id": COMPLIANCE_ID,
        "name": "EPFO Form 5A",
        "category": "FORM_VALIDATION",
        "readiness": readiness(findings),
        "findings": findings,
        "evidence_used": list(form5a_evidence.keys()),
    }