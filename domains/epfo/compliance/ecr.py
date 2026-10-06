"""
EPFO ECR compliance workflow.

ECR is treated as structured member-level data. This workflow delegates
row-level validation to the deterministic ECR rules engine.
"""

from typing import Any, Dict

from ..rules.ecr_rules import check_ecr
from ..rules.common import readiness


COMPLIANCE_ID = "EPFO.ECR"


def assess_ecr(
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Assess an EPFO Electronic Challan-cum-Return (ECR).

    Parameters
    ----------
    context:
        Establishment and assessment-period context.

    evidence:
        Expected format:

        {
            "ecr": {
                "period": "2026-09",
                "establishment_code": "1234567",
                "rows": [...]
            }
        }

    Returns
    -------
    dict
        Structured ECR assessment.
    """

    context = context or {}
    evidence = evidence or {}

    ecr_data = evidence.get(
        "ecr",
        {}
    )

    findings = check_ecr(
        context=context,
        ecr=ecr_data,
    )

    rows = ecr_data.get("rows", [])

    # Calculate useful summary values without making
    # any unsupported statutory assumption.
    total_wages = sum(
        float(row.get("wages") or 0)
        for row in rows
    )

    total_employee_share = sum(
        float(row.get("employee_share") or 0)
        for row in rows
    )

    total_employer_share = sum(
        float(row.get("employer_share") or 0)
        for row in rows
    )

    return {
        "compliance_id": COMPLIANCE_ID,
        "name": "EPFO Electronic Challan-cum-Return",
        "category": "RETURN",
        "readiness": readiness(findings),
        "findings": findings,

        "period": ecr_data.get("period"),

        "establishment_code": ecr_data.get(
            "establishment_code"
        ),

        "row_count": len(rows),

        "summary": {
            "total_wages": round(total_wages, 2),
            "total_employee_share": round(
                total_employee_share,
                2
            ),
            "total_employer_share": round(
                total_employer_share,
                2
            ),
        },

        "evidence_used": [
            "ECR period",
            "ECR member rows",
            "ECR establishment code",
        ],
    }