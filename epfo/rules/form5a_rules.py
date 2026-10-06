"""
Deterministic rules for EPFO Form 5A.
"""

from typing import Any, Dict, List

from .common import (
    finding,
    normalize_pan,
    same_identifier,
    same_text,
    valid_pan,
    require,
)


LEGAL_SOURCES = [
    "EPFO_FORM_5A",
]


def check_form5a(
    context: Dict[str, Any],
    form: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Validate Form 5A extracted evidence against establishment context.
    """

    context = context or {}
    form = form or {}

    findings: List[Dict[str, Any]] = []

    # ---------------------------------------------------------------
    # Required Form 5A fields
    # ---------------------------------------------------------------

    required_fields = [
        (
            form.get("establishment_name_as_per_pan"),
            "EPFO.FORM5A.NAME_REQUIRED",
            "establishment name as per PAN",
        ),
        (
            form.get("pan"),
            "EPFO.FORM5A.PAN_REQUIRED",
            "PAN",
        ),
        (
            form.get("coverage_basis"),
            "EPFO.FORM5A.COVERAGE_REQUIRED",
            "coverage basis",
        ),
    ]

    for value, rule_id, label in required_fields:

        result = require(
            value=value,
            rule_id=rule_id,
            label=label,
            legal_sources=LEGAL_SOURCES,
        )

        if result:
            findings.append(result)

    # ---------------------------------------------------------------
    # PAN format
    # ---------------------------------------------------------------

    pan = form.get("pan")

    if pan:

        if not valid_pan(pan):
            findings.append(
                finding(
                    rule_id="EPFO.FORM5A.PAN_FORMAT",
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        "The PAN extracted from Form 5A "
                        "has an invalid format."
                    ),
                    evidence=[
                        "form5a.pan"
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the PAN against authoritative "
                        "establishment records."
                    ),
                )
            )

    # ---------------------------------------------------------------
    # Form 5A PAN ↔ context PAN
    # ---------------------------------------------------------------

    context_pan = context.get("pan")

    if pan and context_pan:

        if normalize_pan(pan) != normalize_pan(
            context_pan
        ):
            findings.append(
                finding(
                    rule_id="EPFO.FORM5A.PAN_MATCH",
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        "The PAN in Form 5A does not match "
                        "the establishment PAN in the assessment context."
                    ),
                    evidence=[
                        "form5a.pan",
                        "context.pan",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify that the Form 5A belongs to "
                        "the assessed establishment."
                    ),
                )
            )

    # ---------------------------------------------------------------
    # Form 5A establishment name ↔ context
    # ---------------------------------------------------------------

    form_name = form.get(
        "establishment_name_as_per_pan"
    )

    context_name = context.get(
        "establishment_name"
    )

    if form_name and context_name:

        if not same_text(
            form_name,
            context_name
        ):
            findings.append(
                finding(
                    rule_id="EPFO.FORM5A.NAME_MATCH",
                    outcome="REVIEW",
                    severity="MEDIUM",
                    message=(
                        "The establishment name in Form 5A "
                        "differs from the supplied establishment context."
                    ),
                    evidence=[
                        "form5a.establishment_name_as_per_pan",
                        "context.establishment_name",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify whether the difference is due to "
                        "a legal/trading name variation or an actual mismatch."
                    ),
                    details={
                        "form5a_name": form_name,
                        "context_name": context_name,
                    },
                )
            )

    # ---------------------------------------------------------------
    # Establishment code
    # ---------------------------------------------------------------

    form_code = form.get(
        "establishment_code"
    )

    context_code = context.get(
        "establishment_code"
    )

    if not form_code:

        findings.append(
            finding(
                rule_id="EPFO.FORM5A.CODE_MISSING",
                outcome="REVIEW",
                severity="MEDIUM",
                message=(
                    "Establishment code is unavailable in Form 5A "
                    "evidence for cross-document validation."
                ),
                evidence=[
                    "form5a.establishment_code"
                ],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide the establishment code or "
                    "corresponding registration evidence."
                ),
            )
        )

    elif context_code:

        if not same_identifier(
            form_code,
            context_code
        ):
            findings.append(
                finding(
                    rule_id="EPFO.FORM5A.CODE_MATCH",
                    outcome="FAIL",
                    severity="HIGH",
                    message=(
                        "The establishment code in Form 5A "
                        "does not match the assessment context."
                    ),
                    evidence=[
                        "form5a.establishment_code",
                        "context.establishment_code",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify that Form 5A belongs to "
                        "the assessed establishment."
                    ),
                )
            )

    # ---------------------------------------------------------------
    # Coverage basis
    # ---------------------------------------------------------------

    coverage_basis = form.get(
        "coverage_basis"
    )

    if coverage_basis:

        normalized = str(
            coverage_basis
        ).strip().casefold()

        if normalized in {
            "unknown",
            "not known",
            "n/a",
            "na",
            "none",
        }:
            findings.append(
                finding(
                    rule_id="EPFO.FORM5A.COVERAGE_REVIEW",
                    outcome="REVIEW",
                    severity="HIGH",
                    message=(
                        "Form 5A does not provide a usable "
                        "coverage basis."
                    ),
                    evidence=[
                        "form5a.coverage_basis"
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the coverage basis using "
                        "authoritative EPFO records."
                    ),
                )
            )

    return findings