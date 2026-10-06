"""
EPFO UAN / Member compliance workflow.
"""

from typing import Any, Dict

from ..rules.uan_rules import check_uan
from ..rules.common import readiness


COMPLIANCE_ID = "EPFO.UAN"


def assess_uan(
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Assess UAN/member onboarding records.

    Expected evidence format:

    {
        "uan_records": [
            {
                "uan": "100000000001",
                "employee_name": "EMPLOYEE ONE",
                "establishment_code": "1234567"
            }
        ]
    }
    """

    context = context or {}
    evidence = evidence or {}

    records = evidence.get(
        "uan_records",
        []
    )

    findings = check_uan(
        context=context,
        records=records,
    )

    return {
        "compliance_id": COMPLIANCE_ID,
        "name": "EPFO UAN / Member",
        "category": "MEMBER_COMPLIANCE",
        "readiness": readiness(findings),
        "findings": findings,
        "member_count": len(records),
    }