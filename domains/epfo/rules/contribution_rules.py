"""
Deterministic rules for EPFO contribution/challan/payment reconciliation.

This module verifies supplied financial evidence.

It does not independently calculate statutory contribution rates.
"""

from decimal import Decimal
from typing import Any, Dict, List

from .common import (
    finding,
    numbers_equal,
    parse_non_negative_number,
    require,
)


LEGAL_SOURCES = [
    "EPFO_ECR_REVAMP_2025",
    "EPFO_SCHEME_1952",
]


MONEY_TOLERANCE = Decimal(
    "0.01"
)


def check_contribution(
    context: Dict[str, Any],
    data: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Validate ECR/challan/payment reconciliation.
    """

    context = context or {}
    data = data or {}

    findings: List[Dict[str, Any]] = []

    # ===============================================================
    # Required period
    # ===============================================================

    period = data.get(
        "period"
    )

    missing_period = require(
        value=period,
        rule_id="EPFO.CONTRIBUTION.PERIOD_REQUIRED",
        label="contribution period",
        legal_sources=LEGAL_SOURCES,
    )

    if missing_period:
        findings.append(
            missing_period
        )

    assessment_period = context.get(
        "assessment_period"
    )

    if (
        period
        and assessment_period
        and str(period) != str(assessment_period)
    ):

        findings.append(
            finding(
                rule_id="EPFO.CONTRIBUTION.PERIOD_MISMATCH",
                outcome="FAIL",
                severity="HIGH",
                message=(
                    "Contribution period does not match "
                    "the assessment period."
                ),
                evidence=[
                    "contribution.period",
                    "context.assessment_period",
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Verify that the contribution evidence "
                    "belongs to the intended period."
                ),
            )
        )

    # ===============================================================
    # Required financial values
    # ===============================================================

    ecr_total = data.get(
        "ecr_total"
    )

    challan_amount = data.get(
        "challan_amount"
    )

    paid_amount = data.get(
        "paid_amount"
    )

    # ECR total
    missing_ecr = require(
        value=ecr_total,
        rule_id="EPFO.CONTRIBUTION.ECR_TOTAL_MISSING",
        label="ECR contribution total",
        legal_sources=LEGAL_SOURCES,
    )

    if missing_ecr:
        findings.append(
            missing_ecr
        )

    # Challan
    missing_challan = require(
        value=challan_amount,
        rule_id="EPFO.CONTRIBUTION.CHALLAN_MISSING",
        label="challan amount",
        legal_sources=LEGAL_SOURCES,
    )

    if missing_challan:
        findings.append(
            missing_challan
        )

    # Payment
    missing_payment = require(
        value=paid_amount,
        rule_id="EPFO.CONTRIBUTION.PAYMENT_MISSING",
        label="payment amount",
        legal_sources=LEGAL_SOURCES,
    )

    if missing_payment:
        findings.append(
            missing_payment
        )

    # ===============================================================
    # Numeric validation
    # ===============================================================

    parsed_values = {}

    for field_name, label in [
        (
            "ecr_total",
            "ECR contribution total",
        ),
        (
            "challan_amount",
            "challan amount",
        ),
        (
            "paid_amount",
            "paid amount",
        ),
        (
            "employee_total",
            "employee contribution total",
        ),
        (
            "employer_total",
            "employer contribution total",
        ),
    ]:

        value = data.get(
            field_name
        )

        if value is None:
            continue

        parsed = parse_non_negative_number(
            value
        )

        if parsed is None:

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.CONTRIBUTION."
                        f"{field_name.upper()}_INVALID"
                    ),
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        f"{label} is not a valid "
                        "non-negative monetary value."
                    ),
                    evidence=[
                        f"contribution.{field_name}"
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        f"Correct the {label} using "
                        "the authoritative source."
                    ),
                )
            )

        else:

            parsed_values[
                field_name
            ] = parsed

    # ===============================================================
    # ECR ↔ Challan
    # ===============================================================

    if (
        ecr_total is not None
        and challan_amount is not None
    ):

        if not numbers_equal(
            ecr_total,
            challan_amount,
            MONEY_TOLERANCE,
        ):

            difference = (
                parsed_values.get(
                    "ecr_total",
                    Decimal("0")
                )
                -
                parsed_values.get(
                    "challan_amount",
                    Decimal("0")
                )
            )

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.CONTRIBUTION."
                        "ECR_CHALLAN_MISMATCH"
                    ),
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        "ECR contribution total does not "
                        "match the challan amount."
                    ),
                    evidence=[
                        "contribution.ecr_total",
                        "contribution.challan_amount",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Reconcile the ECR total with the "
                        "challan before proceeding."
                    ),
                    details={
                        "difference": float(
                            difference
                        )
                    },
                )
            )

        else:

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.CONTRIBUTION."
                        "ECR_CHALLAN_MATCH"
                    ),
                    outcome="PASS",
                    severity="INFO",
                    message=(
                        "ECR contribution total matches "
                        "the challan amount."
                    ),
                    evidence=[
                        "contribution.ecr_total",
                        "contribution.challan_amount",
                    ],
                    legal_sources=LEGAL_SOURCES,
                )
            )

    # ===============================================================
    # Challan ↔ Payment
    # ===============================================================

    if (
        challan_amount is not None
        and paid_amount is not None
    ):

        if not numbers_equal(
            challan_amount,
            paid_amount,
            MONEY_TOLERANCE,
        ):

            difference = (
                parsed_values.get(
                    "challan_amount",
                    Decimal("0")
                )
                -
                parsed_values.get(
                    "paid_amount",
                    Decimal("0")
                )
            )

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.CONTRIBUTION."
                        "PAYMENT_MISMATCH"
                    ),
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        "Paid amount does not match "
                        "the challan amount."
                    ),
                    evidence=[
                        "contribution.challan_amount",
                        "contribution.paid_amount",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the challan and payment "
                        "receipt/TRRN before proceeding."
                    ),
                    details={
                        "difference": float(
                            difference
                        )
                    },
                )
            )

        else:

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.CONTRIBUTION."
                        "PAYMENT_MATCH"
                    ),
                    outcome="PASS",
                    severity="INFO",
                    message=(
                        "Payment amount matches "
                        "the challan amount."
                    ),
                    evidence=[
                        "contribution.challan_amount",
                        "contribution.paid_amount",
                    ],
                    legal_sources=LEGAL_SOURCES,
                )
            )

    # ===============================================================
    # TRRN
    # ===============================================================

    trrn = data.get(
        "trrn"
    )

    if not trrn:

        findings.append(
            finding(
                rule_id="EPFO.CONTRIBUTION.TRRN_MISSING",
                outcome="REVIEW",
                severity="MEDIUM",
                message=(
                    "TRRN/payment reference is not "
                    "available in the supplied evidence."
                ),
                evidence=[
                    "contribution.trrn"
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide the official payment/challan "
                    "reference for audit traceability."
                ),
            )
        )

    # ===============================================================
    # Payment date
    # ===============================================================

    if not data.get(
        "payment_date"
    ):

        findings.append(
            finding(
                rule_id=(
                    "EPFO.CONTRIBUTION."
                    "PAYMENT_DATE_MISSING"
                ),
                outcome="REVIEW",
                severity="MEDIUM",
                message=(
                    "Payment date is missing from "
                    "the supplied evidence."
                ),
                evidence=[
                    "contribution.payment_date"
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide the payment date from "
                    "the official payment evidence."
                ),
            )
        )

    # ===============================================================
    # Reconciliation summary
    # ===============================================================

    findings.append(
        finding(
            rule_id=(
                "EPFO.CONTRIBUTION."
                "RECONCILIATION_SUMMARY"
            ),
            outcome="PASS",
            severity="INFO",
            message=(
                "Contribution reconciliation values "
                "were processed."
            ),
            evidence=[
                "contribution.ecr_total",
                "contribution.challan_amount",
                "contribution.paid_amount",
            ],
            legal_sources=LEGAL_SOURCES,
            details={
                "ecr_total": (
                    float(ecr_total)
                    if ecr_total is not None
                    else None
                ),
                "challan_amount": (
                    float(challan_amount)
                    if challan_amount is not None
                    else None
                ),
                "paid_amount": (
                    float(paid_amount)
                    if paid_amount is not None
                    else None
                ),
            },
        )
    )

    return findings