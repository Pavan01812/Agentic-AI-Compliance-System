"""
Deterministic rules for EPFO establishment registration.
"""

from typing import Any, Dict

from .common import (
    finding,
    normalize_identifier,
    normalize_pan,
    readiness,
    valid_establishment_code,
    valid_pan,
)


LEGAL_SOURCES = [
    "EPFO_FORM_5A",
    "EPFO_SCHEME_1952",
]


def check_registration(
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> list[dict]:
    """
    Evaluate EPFO establishment registration.

    Missing evidence produces REVIEW.
    Objective inconsistencies produce FAIL.
    """

    findings = []

    registration = evidence.get("registration")

    # ---------------------------------------------------------------
    # Registration evidence must exist
    # ---------------------------------------------------------------

    if not isinstance(registration, dict):
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.EVIDENCE_REQUIRED",
                outcome="REVIEW",
                message=(
                    "Registration evidence is missing or is not "
                    "provided as a structured record."
                ),
                severity="HIGH",
                evidence=["registration"],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide the official EPFO establishment "
                    "registration record."
                ),
            )
        )

        return findings

    # ---------------------------------------------------------------
    # Extract values
    # ---------------------------------------------------------------

    establishment_code = registration.get(
        "establishment_code"
    )

    establishment_name = registration.get(
        "establishment_name"
    )

    pan = registration.get("pan")

    coverage_basis = registration.get(
        "coverage_basis"
    )

    # ---------------------------------------------------------------
    # Required establishment code
    # ---------------------------------------------------------------

    if not establishment_code:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.REQUIRED_ESTABLISHMENT_CODE",
                outcome="REVIEW",
                message="Establishment code is missing from registration evidence.",
                severity="HIGH",
                evidence=["registration.establishment_code"],
                legal_sources=LEGAL_SOURCES,
                remediation="Provide the EPFO establishment code.",
            )
        )
    else:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.REQUIRED_ESTABLISHMENT_CODE",
                outcome="PASS",
                message="Establishment code is present.",
                severity="INFO",
                evidence=["registration.establishment_code"],
                legal_sources=LEGAL_SOURCES,
            )
        )

        if not valid_establishment_code(
            establishment_code
        ):
            findings.append(
                finding(
                    rule_id="EPFO.REGISTRATION.ESTABLISHMENT_CODE_FORMAT",
                    outcome="FAIL",
                    message=(
                        "The establishment code does not match "
                        "the expected EPFO establishment-code format."
                    ),
                    severity="HIGH",
                    evidence=[
                        "registration.establishment_code"
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the establishment code against "
                        "the official EPFO registration record."
                    ),
                    details={
                        "value": establishment_code
                    },
                )
            )
        else:
            findings.append(
                finding(
                    rule_id="EPFO.REGISTRATION.ESTABLISHMENT_CODE_FORMAT",
                    outcome="PASS",
                    message="Establishment code format is valid.",
                    severity="INFO",
                    evidence=[
                        "registration.establishment_code"
                    ],
                    legal_sources=LEGAL_SOURCES,
                )
            )

    # ---------------------------------------------------------------
    # Required establishment name
    # ---------------------------------------------------------------

    if not establishment_name:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.REQUIRED_ESTABLISHMENT_NAME",
                outcome="REVIEW",
                message="Establishment name is missing from registration evidence.",
                severity="HIGH",
                evidence=["registration.establishment_name"],
                legal_sources=LEGAL_SOURCES,
                remediation="Provide the registered establishment name.",
            )
        )
    else:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.REQUIRED_ESTABLISHMENT_NAME",
                outcome="PASS",
                message="Establishment name is present.",
                severity="INFO",
                evidence=["registration.establishment_name"],
                legal_sources=LEGAL_SOURCES,
            )
        )

        context_name = context.get(
            "establishment_name"
        )

        if context_name:
            if normalize_identifier(
                establishment_name
            ) == normalize_identifier(
                context_name
            ):
                findings.append(
                    finding(
                        rule_id="EPFO.REGISTRATION.NAME_CROSS_CHECK",
                        outcome="PASS",
                        message=(
                            "Registration establishment name "
                            "matches the compliance context."
                        ),
                        severity="INFO",
                        evidence=[
                            "registration.establishment_name",
                            "context.establishment_name",
                        ],
                        legal_sources=LEGAL_SOURCES,
                    )
                )
            else:
                findings.append(
                    finding(
                        rule_id="EPFO.REGISTRATION.NAME_CROSS_CHECK",
                        outcome="FAIL",
                        message=(
                            "Registration establishment name does "
                            "not match the compliance context."
                        ),
                        severity="HIGH",
                        evidence=[
                            "registration.establishment_name",
                            "context.establishment_name",
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Verify the registered establishment "
                            "name and update the incorrect record."
                        ),
                        details={
                            "registration_name": establishment_name,
                            "context_name": context_name,
                        },
                    )
                )

    # ---------------------------------------------------------------
    # Required PAN
    # ---------------------------------------------------------------

    if not pan:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.REQUIRED_PAN",
                outcome="REVIEW",
                message="PAN is missing from registration evidence.",
                severity="HIGH",
                evidence=["registration.pan"],
                legal_sources=LEGAL_SOURCES,
                remediation="Provide the establishment PAN.",
            )
        )
    else:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.REQUIRED_PAN",
                outcome="PASS",
                message="PAN is present.",
                severity="INFO",
                evidence=["registration.pan"],
                legal_sources=LEGAL_SOURCES,
            )
        )

        if not valid_pan(pan):
            findings.append(
                finding(
                    rule_id="EPFO.REGISTRATION.PAN_FORMAT",
                    outcome="FAIL",
                    message="The registration PAN format is invalid.",
                    severity="HIGH",
                    evidence=["registration.pan"],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the PAN against the official "
                        "establishment PAN record."
                    ),
                    details={
                        "value": pan
                    },
                )
            )
        else:
            findings.append(
                finding(
                    rule_id="EPFO.REGISTRATION.PAN_FORMAT",
                    outcome="PASS",
                    message="Registration PAN format is valid.",
                    severity="INFO",
                    evidence=["registration.pan"],
                    legal_sources=LEGAL_SOURCES,
                )
            )

        context_pan = context.get("pan")

        if context_pan:
            if normalize_pan(pan) == normalize_pan(
                context_pan
            ):
                findings.append(
                    finding(
                        rule_id="EPFO.REGISTRATION.PAN_CROSS_CHECK",
                        outcome="PASS",
                        message=(
                            "Registration PAN matches the "
                            "compliance context."
                        ),
                        severity="INFO",
                        evidence=[
                            "registration.pan",
                            "context.pan",
                        ],
                        legal_sources=LEGAL_SOURCES,
                    )
                )
            else:
                findings.append(
                    finding(
                        rule_id="EPFO.REGISTRATION.PAN_CROSS_CHECK",
                        outcome="FAIL",
                        message=(
                            "Registration PAN does not match "
                            "the compliance context."
                        ),
                        severity="HIGH",
                        evidence=[
                            "registration.pan",
                            "context.pan",
                        ],
                        legal_sources=LEGAL_SOURCES,
                        remediation=(
                            "Verify the establishment PAN and "
                            "correct the inconsistent record."
                        ),
                        details={
                            "registration_pan": pan,
                            "context_pan": context_pan,
                        },
                    )
                )

    # ---------------------------------------------------------------
    # Establishment code cross-check
    # ---------------------------------------------------------------

    context_code = context.get(
        "establishment_code"
    )

    if establishment_code and context_code:

        if normalize_identifier(
            establishment_code
        ) == normalize_identifier(
            context_code
        ):
            findings.append(
                finding(
                    rule_id="EPFO.REGISTRATION.ESTABLISHMENT_CODE_CROSS_CHECK",
                    outcome="PASS",
                    message=(
                        "Registration establishment code matches "
                        "the compliance context."
                    ),
                    severity="INFO",
                    evidence=[
                        "registration.establishment_code",
                        "context.establishment_code",
                    ],
                    legal_sources=LEGAL_SOURCES,
                )
            )

        else:
            findings.append(
                finding(
                    rule_id="EPFO.REGISTRATION.ESTABLISHMENT_CODE_CROSS_CHECK",
                    outcome="FAIL",
                    message=(
                        "Registration establishment code does "
                        "not match the compliance context."
                    ),
                    severity="HIGH",
                    evidence=[
                        "registration.establishment_code",
                        "context.establishment_code",
                    ],
                    legal_sources=LEGAL_SOURCES,
                    remediation=(
                        "Verify the establishment code against "
                        "the official EPFO record."
                    ),
                    details={
                        "registration_code": establishment_code,
                        "context_code": context_code,
                    },
                )
            )

    # ---------------------------------------------------------------
    # Coverage basis
    # ---------------------------------------------------------------

    if not coverage_basis:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.COVERAGE_BASIS_UNKNOWN",
                outcome="REVIEW",
                message=(
                    "The basis of EPFO coverage cannot be established "
                    "from the available registration evidence."
                ),
                severity="MEDIUM",
                evidence=["registration.coverage_basis"],
                legal_sources=LEGAL_SOURCES,
                remediation=(
                    "Provide evidence establishing the applicable "
                    "EPFO coverage basis."
                ),
            )
        )
    else:
        findings.append(
            finding(
                rule_id="EPFO.REGISTRATION.COVERAGE_BASIS",
                outcome="PASS",
                message="EPFO coverage basis is present.",
                severity="INFO",
                evidence=["registration.coverage_basis"],
                legal_sources=LEGAL_SOURCES,
                details={
                    "coverage_basis": coverage_basis
                },
            )
        )

    return findings