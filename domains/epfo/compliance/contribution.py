"""
EPFO contribution and challan reconciliation workflow.
"""

from typing import Any, Dict

from ..rules.contribution_rules import check_contribution
from ..rules.common import readiness


COMPLIANCE_ID = "EPFO.CONTRIBUTION"


def assess_contribution(
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Assess EPFO contribution/challan/payment reconciliation.

    Expected evidence:

    {
        "contribution": {
            "period": "2026-09",
            "ecr_total": 3750,
            "challan_amount": 3750,
            "paid_amount": 3750,
            "trrn": "TRRN123456",
            "payment_date": "2026-10-15"
        }
    }
    """

    context = context or {}
    evidence = evidence or {}

    contribution_data = evidence.get(
        "contribution",
        {}
    )

    findings = check_contribution(
        context=context,
        data=contribution_data,
    )

    ecr_total = contribution_data.get(
        "ecr_total"
    )

    challan_amount = contribution_data.get(
        "challan_amount"
    )

    paid_amount = contribution_data.get(
        "paid_amount"
    )

    # Calculate differences where both values exist.
    ecr_challan_difference = None
    challan_payment_difference = None

    if ecr_total is not None and challan_amount is not None:
        ecr_challan_difference = round(
            float(ecr_total) -
            float(challan_amount),
            2
        )

    if challan_amount is not None and paid_amount is not None:
        challan_payment_difference = round(
            float(challan_amount) -
            float(paid_amount),
            2
        )

    return {
        "compliance_id": COMPLIANCE_ID,
        "name": "EPFO Contribution",
        "category": "CONTRIBUTION_RECONCILIATION",

        "readiness": readiness(findings),

        "findings": findings,

        "period": contribution_data.get(
            "period"
        ),

        "trrn": contribution_data.get(
            "trrn"
        ),

        "reconciliation": {
            "ecr_total": ecr_total,
            "challan_amount": challan_amount,
            "paid_amount": paid_amount,

            "ecr_vs_challan_difference":
                ecr_challan_difference,

            "challan_vs_payment_difference":
                challan_payment_difference,
        },

        "evidence_used": [
            key
            for key in contribution_data.keys()
        ],
    }