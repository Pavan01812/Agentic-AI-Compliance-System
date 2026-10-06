"""
Deterministic rules for EPFO Electronic Challan-cum-Return (ECR).

The engine validates the internal consistency of supplied ECR data.

It deliberately does NOT infer a statutory contribution rate from the
employee wage alone. Statutory applicability, wage ceilings, exclusions,
special categories and historical rules can require additional facts.
Where those facts are unavailable, the engine returns REVIEW.
"""

from decimal import Decimal
from typing import Any, Dict, List, Set

from .common import (
    finding,
    parse_non_negative_number,
    require,
    same_identifier,
    valid_uan,
)


LEGAL_SOURCES = [
    "EPFO_ECR_REVAMP_2025",
    "EPFO_SCHEME_1952",
]


def check_ecr(
    context: Dict[str, Any],
    ecr: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Validate an ECR dataset.
    """

    context = context or {}
    ecr = ecr or {}

    findings: List[Dict[str, Any]] = []

    period = ecr.get(
        "period"
    )

    rows = ecr.get(
        "rows"
    ) or []

    establishment_code = ecr.get(
        "establishment_code"
    )

    # ===============================================================
    # ECR period
    # ===============================================================

    missing_period = require(
        value=period,
        rule_id="EPFO.ECR.PERIOD_REQUIRED",
        label="ECR period",
        legal_sources=LEGAL_SOURCES,
    )

    if missing_period:
        findings.append(
            missing_period
        )

    # ===============================================================
    # ECR establishment
    # ===============================================================

    context_establishment_code = context.get(
        "establishment_code"
    )

    if (
        establishment_code
        and context_establishment_code
    ):

        if not same_identifier(
            establishment_code,
            context_establishment_code,
        ):

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.ECR."
                        "ESTABLISHMENT_MISMATCH"
                    ),
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        "The ECR establishment code does not "
                        "match the assessment establishment."
                    ),
                    evidence=[
                        "ecr.establishment_code",
                        "context.establishment_code",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify that the ECR belongs to "
                        "the assessed EPFO establishment."
                    ),
                )
            )

    elif not establishment_code:

        findings.append(
            finding(
                rule_id=(
                    "EPFO.ECR."
                    "ESTABLISHMENT_CODE_MISSING"
                ),
                outcome="REVIEW",
                severity="MEDIUM",
                message=(
                    "ECR establishment code is unavailable."
                ),
                evidence=[
                    "ecr.establishment_code"
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide establishment-code evidence "
                    "for cross-document validation."
                ),
            )
        )

    # ===============================================================
    # ECR rows
    # ===============================================================

    if not rows:

        findings.append(
            finding(
                rule_id="EPFO.ECR.NO_ROWS",
                outcome="REVIEW",
                severity="HIGH",
                message=(
                    "No member rows were found in the ECR."
                ),
                evidence=[
                    "ecr.rows"
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide the ECR member-level data "
                    "for the assessment period."
                ),
            )
        )

        return findings

    # ===============================================================
    # Aggregates
    # ===============================================================

    total_wages = Decimal("0")
    total_epf_wages = Decimal("0")
    total_eps_wages = Decimal("0")
    total_edli_wages = Decimal("0")
    total_employee_share = Decimal("0")
    total_employer_share = Decimal("0")

    seen_uans: Set[str] = set()

    # ===============================================================
    # Row validation
    # ===============================================================

    for index, row in enumerate(
        rows,
        start=1,
    ):

        row = row or {}

        row_prefix = (
            f"ecr.rows[{index - 1}]"
        )

        # -----------------------------------------------------------
        # UAN
        # -----------------------------------------------------------

        uan = row.get(
            "uan"
        )

        missing_uan = require(
            value=uan,
            rule_id="EPFO.ECR.UAN_MISSING",
            label=f"UAN in ECR row {index}",
            legal_sources=LEGAL_SOURCES,
        )

        if missing_uan:
            findings.append(
                missing_uan
            )

        if uan:

            if not valid_uan(
                uan
            ):

                findings.append(
                    finding(
                        rule_id="EPFO.ECR.UAN_FORMAT",
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"Invalid UAN in ECR row {index}."
                        ),
                        evidence=[
                            f"{row_prefix}.uan"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Verify the UAN against "
                            "official EPFO member records."
                        ),
                    )
                )

            normalized_uan = str(
                uan
            ).strip()

            if normalized_uan in seen_uans:

                findings.append(
                    finding(
                        rule_id="EPFO.ECR.DUPLICATE_UAN",
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"Duplicate UAN found in ECR: "
                            f"{normalized_uan}."
                        ),
                        evidence=[
                            f"{row_prefix}.uan"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Remove or resolve the duplicate "
                            "member row after verifying official records."
                        ),
                    )
                )

            seen_uans.add(
                normalized_uan
            )

        # -----------------------------------------------------------
        # Employee name
        # -----------------------------------------------------------

        if not row.get(
            "employee_name"
        ):

            findings.append(
                finding(
                    rule_id="EPFO.ECR.NAME_MISSING",
                    outcome="REVIEW",
                    severity="MEDIUM",
                    message=(
                        f"Employee name is missing in "
                        f"ECR row {index}."
                    ),
                    evidence=[
                        f"{row_prefix}.employee_name"
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the member identity from "
                        "authoritative EPFO records."
                    ),
                )
            )

        # -----------------------------------------------------------
        # Numeric fields
        # -----------------------------------------------------------

        numeric_fields = [
            ("wages", "Wages"),
            ("epf_wages", "EPF wages"),
            ("eps_wages", "EPS wages"),
            ("edli_wages", "EDLI wages"),
            ("employee_share", "Employee share"),
            ("employer_share", "Employer share"),
        ]

        parsed_values: Dict[str, Decimal] = {}

        for field_name, label in numeric_fields:

            raw_value = row.get(
                field_name
            )

            if raw_value is None:

                findings.append(
                    finding(
                        rule_id=(
                            "EPFO.ECR."
                            f"{field_name.upper()}_MISSING"
                        ),
                        outcome="REVIEW",
                        severity="MEDIUM",
                        message=(
                            f"{label} is missing in "
                            f"ECR row {index}."
                        ),
                        evidence=[
                            f"{row_prefix}.{field_name}"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            f"Provide or verify {label} "
                            "from the source ECR."
                        ),
                    )
                )

                continue

            parsed = parse_non_negative_number(
                raw_value
            )

            if parsed is None:

                findings.append(
                    finding(
                        rule_id=(
                            "EPFO.ECR."
                            f"{field_name.upper()}_INVALID"
                        ),
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"{label} in ECR row {index} "
                            "is not a valid non-negative number."
                        ),
                        evidence=[
                            f"{row_prefix}.{field_name}"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            f"Correct the {label} value "
                            "using the source ECR."
                        ),
                    )
                )

                continue

            parsed_values[
                field_name
            ] = parsed

        # -----------------------------------------------------------
        # Add valid numeric values to aggregates
        # -----------------------------------------------------------

        total_wages += parsed_values.get(
            "wages",
            Decimal("0")
        )

        total_epf_wages += parsed_values.get(
            "epf_wages",
            Decimal("0")
        )

        total_eps_wages += parsed_values.get(
            "eps_wages",
            Decimal("0")
        )

        total_edli_wages += parsed_values.get(
            "edli_wages",
            Decimal("0")
        )

        total_employee_share += parsed_values.get(
            "employee_share",
            Decimal("0")
        )

        total_employer_share += parsed_values.get(
            "employer_share",
            Decimal("0")
        )

        # -----------------------------------------------------------
        # Wage hierarchy checks
        # -----------------------------------------------------------

        wages = parsed_values.get(
            "wages"
        )

        epf_wages = parsed_values.get(
            "epf_wages"
        )

        eps_wages = parsed_values.get(
            "eps_wages"
        )

        edli_wages = parsed_values.get(
            "edli_wages"
        )

        if (
            wages is not None
            and epf_wages is not None
            and epf_wages > wages
        ):

            findings.append(
                finding(
                    rule_id="EPFO.ECR.EPF_WAGES_EXCEED_WAGES",
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        f"EPF wages exceed total wages "
                        f"in ECR row {index}."
                    ),
                    evidence=[
                        f"{row_prefix}.wages",
                        f"{row_prefix}.epf_wages",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the wage values and "
                        "source ECR data."
                    ),
                )
            )

        if (
            wages is not None
            and eps_wages is not None
            and eps_wages > wages
        ):

            findings.append(
                finding(
                    rule_id="EPFO.ECR.EPS_WAGES_EXCEED_WAGES",
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        f"EPS wages exceed total wages "
                        f"in ECR row {index}."
                    ),
                    evidence=[
                        f"{row_prefix}.wages",
                        f"{row_prefix}.eps_wages",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the EPS wage value "
                        "against the source ECR."
                    ),
                )
            )

        if (
            wages is not None
            and edli_wages is not None
            and edli_wages > wages
        ):

            findings.append(
                finding(
                    rule_id="EPFO.ECR.EDLI_WAGES_EXCEED_WAGES",
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        f"EDLI wages exceed total wages "
                        f"in ECR row {index}."
                    ),
                    evidence=[
                        f"{row_prefix}.wages",
                        f"{row_prefix}.edli_wages",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the EDLI wage value "
                        "against the source ECR."
                    ),
                )
            )

        # -----------------------------------------------------------
        # NCP days
        # -----------------------------------------------------------

        ncp_days = row.get(
            "ncp_days"
        )

        if ncp_days is not None:

            parsed_ncp = parse_non_negative_number(
                ncp_days
            )

            if parsed_ncp is None:

                findings.append(
                    finding(
                        rule_id="EPFO.ECR.NCP_DAYS_INVALID",
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"NCP days is invalid in "
                            f"ECR row {index}."
                        ),
                        evidence=[
                            f"{row_prefix}.ncp_days"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Correct NCP days using the "
                            "source ECR/member records."
                        ),
                    )
                )

            elif parsed_ncp > 31:

                findings.append(
                    finding(
                        rule_id="EPFO.ECR.NCP_DAYS_RANGE",
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"NCP days exceeds 31 in "
                            f"ECR row {index}."
                        ),
                        evidence=[
                            f"{row_prefix}.ncp_days"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Verify NCP days against the "
                            "relevant wage month."
                        ),
                    )
                )

    # ===============================================================
    # Context expected establishment code
    # ===============================================================

    expected_code = context.get(
        "expected_establishment_code"
    )

    if (
        expected_code
        and establishment_code
        and not same_identifier(
            expected_code,
            establishment_code,
        )
    ):

        findings.append(
            finding(
                rule_id=(
                    "EPFO.ECR."
                    "EXPECTED_ESTABLISHMENT_MISMATCH"
                ),
                outcome="FAIL",
                severity="HIGH",
                message=(
                    "ECR establishment code differs from "
                    "the expected establishment code."
                ),
                evidence=[
                    "context.expected_establishment_code",
                    "ecr.establishment_code",
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Verify that the ECR belongs to "
                    "the intended establishment."
                ),
            )
        )

    # ===============================================================
    # Assessment period consistency
    # ===============================================================

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
                rule_id="EPFO.ECR.PERIOD_MISMATCH",
                outcome="FAIL",
                severity="HIGH",
                message=(
                    "ECR period does not match "
                    "the assessment period."
                ),
                evidence=[
                    "ecr.period",
                    "context.assessment_period",
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Verify that the ECR belongs to "
                    "the intended assessment period."
                ),
            )
        )

    # ===============================================================
    # Aggregate metadata
    #
    # Add a non-blocking PASS finding so the report has a useful
    # deterministic aggregate summary.
    # ===============================================================

    findings.append(
        finding(
            rule_id="EPFO.ECR.AGGREGATE_SUMMARY",
            outcome="PASS",
            severity="INFO",
            message=(
                "ECR member rows were processed and "
                "aggregate values were calculated."
            ),
            evidence=[
                "ecr.rows"
            ],
            legal_sources=LEGAL_SOURCES,
            details={
                "row_count": len(rows),
                "total_wages": float(total_wages),
                "total_epf_wages": float(
                    total_epf_wages
                ),
                "total_eps_wages": float(
                    total_eps_wages
                ),
                "total_edli_wages": float(
                    total_edli_wages
                ),
                "total_employee_share": float(
                    total_employee_share
                ),
                "total_employer_share": float(
                    total_employer_share
                ),
            },
        )
    )

    return findings