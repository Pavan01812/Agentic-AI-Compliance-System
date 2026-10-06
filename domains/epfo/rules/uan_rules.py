"""
Deterministic rules for EPFO UAN/member records.
"""

from typing import Any, Dict, List, Set

from .common import (
    finding,
    require,
    same_identifier,
    valid_uan,
)


LEGAL_SOURCES = [
    "EPFO_UAN_GUIDANCE",
]


def check_uan(
    context: Dict[str, Any],
    records: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Validate a collection of UAN/member records.
    """

    context = context or {}
    records = records or []

    findings: List[Dict[str, Any]] = []

    # ---------------------------------------------------------------
    # No records
    # ---------------------------------------------------------------

    if not records:

        findings.append(
            finding(
                rule_id="EPFO.UAN.NO_RECORDS",
                outcome="REVIEW",
                severity="HIGH",
                message=(
                    "No UAN/member records were supplied "
                    "for assessment."
                ),
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide the relevant UAN/member registration "
                    "evidence for the assessment period."
                ),
            )
        )

        return findings

    # ---------------------------------------------------------------
    # Duplicate detection
    # ---------------------------------------------------------------

    seen_uans: Set[str] = set()

    context_establishment_code = context.get(
        "establishment_code"
    )

    # ---------------------------------------------------------------
    # Process every member
    # ---------------------------------------------------------------

    for index, record in enumerate(
        records,
        start=1,
    ):

        record = record or {}

        uan = record.get("uan")
        employee_name = record.get(
            "employee_name"
        )

        # -----------------------------------------------------------
        # UAN required
        # -----------------------------------------------------------

        missing_uan = require(
            value=uan,
            rule_id="EPFO.UAN.MISSING",
            label=f"UAN for member row {index}",
            legal_sources=LEGAL_SOURCES,
        )

        if missing_uan:
            findings.append(missing_uan)

        # -----------------------------------------------------------
        # UAN format
        # -----------------------------------------------------------

        if uan:

            if not valid_uan(uan):

                findings.append(
                    finding(
                        rule_id="EPFO.UAN.FORMAT",
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"UAN format is invalid for "
                            f"member row {index}."
                        ),
                        evidence=[
                            f"uan_records[{index - 1}].uan"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Verify the UAN against official "
                            "EPFO member records."
                        ),
                    )
                )

        # -----------------------------------------------------------
        # Duplicate UAN
        # -----------------------------------------------------------

        if uan:

            normalized_uan = str(
                uan
            ).strip()

            if normalized_uan in seen_uans:

                findings.append(
                    finding(
                        rule_id="EPFO.UAN.DUPLICATE",
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"Duplicate UAN detected: "
                            f"{normalized_uan}."
                        ),
                        evidence=[
                            f"uan_records[{index - 1}].uan"
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Investigate the duplicate member "
                            "record before processing the return."
                        ),
                    )
                )

            else:
                seen_uans.add(
                    normalized_uan
                )

        # -----------------------------------------------------------
        # Employee name
        # -----------------------------------------------------------

        missing_name = require(
            value=employee_name,
            rule_id="EPFO.UAN.NAME_MISSING",
            label=f"employee name for member row {index}",
            legal_sources=LEGAL_SOURCES,
            severity="MEDIUM",
        )

        if missing_name:
            findings.append(
                missing_name
            )

        # -----------------------------------------------------------
        # Establishment mapping
        # -----------------------------------------------------------

        record_establishment_code = record.get(
            "establishment_code"
        )

        if (
            record_establishment_code
            and context_establishment_code
        ):

            if not same_identifier(
                record_establishment_code,
                context_establishment_code,
            ):

                findings.append(
                    finding(
                        rule_id=(
                            "EPFO.UAN."
                            "ESTABLISHMENT_MISMATCH"
                        ),
                        outcome="FAIL",
                        severity="HIGH",
                        message=(
                            f"Member row {index} is mapped "
                            "to an establishment code that differs "
                            "from the assessment establishment."
                        ),
                        evidence=[
                            f"uan_records[{index - 1}].establishment_code",
                            "context.establishment_code",
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Verify the member's establishment "
                            "mapping in EPFO records."
                        ),
                    )
                )

        elif not record_establishment_code:

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.UAN."
                        "ESTABLISHMENT_CODE_MISSING"
                    ),
                    outcome="REVIEW",
                    severity="MEDIUM",
                    message=(
                        f"Establishment mapping is unavailable "
                        f"for member row {index}."
                    ),
                    evidence=[
                        f"uan_records[{index - 1}]"
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Provide establishment mapping evidence "
                        "for the member."
                    ),
                )
            )

        # -----------------------------------------------------------
        # Date of joining
        # -----------------------------------------------------------

        if not record.get(
            "date_of_joining"
        ):

            findings.append(
                finding(
                    rule_id=(
                        "EPFO.UAN."
                        "DATE_OF_JOINING_MISSING"
                    ),
                    outcome="REVIEW",
                    severity="MEDIUM",
                    message=(
                        f"Date of joining is missing "
                        f"for member row {index}."
                    ),
                    evidence=[
                        f"uan_records[{index - 1}].date_of_joining"
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Provide the member's verified "
                        "date of joining."
                    ),
                )
            )

    return findings