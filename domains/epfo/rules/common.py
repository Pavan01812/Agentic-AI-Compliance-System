"""
Common deterministic utilities for the EPFO rule engine.

Design principles:

1. Rules must be deterministic.
2. Missing evidence should normally produce REVIEW, not an invented PASS.
3. Invalid evidence should produce FAIL where objectively detectable.
4. Legal conclusions requiring facts that are not supplied should remain REVIEW.
5. No statutory contribution rate is hard-coded here.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Iterable, List, Optional


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def normalize_text(value: Any) -> str:
    """
    Normalize free-text values for comparison.

    Example:
        " ABC   Technologies Pvt Ltd "
        -> "abc technologies pvt ltd"
    """

    if value is None:
        return ""

    text = str(value).strip()

    # Collapse repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    return text.casefold()


def normalize_identifier(value: Any) -> str:
    """
    Normalize identifiers such as establishment codes.

    Whitespace and hyphens are removed.
    """

    if value is None:
        return ""

    return re.sub(
        r"[\s\-]",
        "",
        str(value).strip()
    ).upper()


def normalize_pan(value: Any) -> str:
    """
    Normalize PAN.
    """

    if value is None:
        return ""

    return re.sub(
        r"\s+",
        "",
        str(value).strip()
    ).upper()


def normalize_uan(value: Any) -> str:
    """
    Normalize UAN.
    """

    if value is None:
        return ""

    return re.sub(
        r"\s+",
        "",
        str(value).strip()
    )


# ---------------------------------------------------------------------------
# Comparisons
# ---------------------------------------------------------------------------

def same_text(a: Any, b: Any) -> bool:
    """
    Compare free-text values after normalization.

    Empty values are never considered equal.
    """

    a_norm = normalize_text(a)
    b_norm = normalize_text(b)

    if not a_norm or not b_norm:
        return False

    return a_norm == b_norm


def same_identifier(a: Any, b: Any) -> bool:
    """
    Compare identifiers after normalization.
    """

    a_norm = normalize_identifier(a)
    b_norm = normalize_identifier(b)

    if not a_norm or not b_norm:
        return False

    return a_norm == b_norm


def same_pan(a: Any, b: Any) -> bool:
    """
    Compare PAN values.
    """

    a_norm = normalize_pan(a)
    b_norm = normalize_pan(b)

    if not a_norm or not b_norm:
        return False

    return a_norm == b_norm


def same_uan(a: Any, b: Any) -> bool:
    """
    Compare UAN values.
    """

    a_norm = normalize_uan(a)
    b_norm = normalize_uan(b)

    if not a_norm or not b_norm:
        return False

    return a_norm == b_norm


# ---------------------------------------------------------------------------
# Format validation
# ---------------------------------------------------------------------------

PAN_PATTERN = re.compile(
    r"^[A-Z]{5}[0-9]{4}[A-Z]$"
)

UAN_PATTERN = re.compile(
    r"^[0-9]{12}$"
)

# EPFO establishment code commonly uses a 7-digit numeric identifier.
ESTABLISHMENT_CODE_PATTERN = re.compile(
    r"^[0-9]{7}$"
)


def valid_pan(value: Any) -> bool:
    """
    Validate PAN format.

    This validates syntax only.
    It does NOT verify PAN against the Income Tax Department.
    """

    return bool(
        PAN_PATTERN.fullmatch(
            normalize_pan(value)
        )
    )


def valid_uan(value: Any) -> bool:
    """
    Validate UAN syntax.

    This validates the expected 12-digit structure only.
    """

    return bool(
        UAN_PATTERN.fullmatch(
            normalize_uan(value)
        )
    )


def valid_establishment_code(value: Any) -> bool:
    """
    Validate the normalized establishment code format.
    """

    return bool(
        ESTABLISHMENT_CODE_PATTERN.fullmatch(
            normalize_identifier(value)
        )
    )


# ---------------------------------------------------------------------------
# Numeric validation
# ---------------------------------------------------------------------------

def parse_non_negative_number(
    value: Any,
) -> Optional[Decimal]:
    """
    Convert a value to Decimal if it is a valid non-negative number.

    Returns:
        Decimal -> valid
        None    -> missing/invalid/negative
    """

    if value is None:
        return None

    if isinstance(value, bool):
        return None

    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError, TypeError):
        return None

    if number < 0:
        return None

    return number


def numbers_equal(
    a: Any,
    b: Any,
    tolerance: Decimal = Decimal("0.01"),
) -> bool:
    """
    Compare monetary/numeric values using a small tolerance.
    """

    a_num = parse_non_negative_number(a)
    b_num = parse_non_negative_number(b)

    if a_num is None or b_num is None:
        return False

    return abs(a_num - b_num) <= tolerance


# ---------------------------------------------------------------------------
# Finding creation
# ---------------------------------------------------------------------------

VALID_OUTCOMES = {
    "PASS",
    "FAIL",
    "REVIEW",
}


VALID_SEVERITIES = {
    "INFO",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
}


def finding(
    rule_id: str,
    outcome: str,
    message: str,
    severity: str = "MEDIUM",
    evidence: Optional[Iterable[Any]] = None,
    legal_sources: Optional[Iterable[str]] = None,
    remediation: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create a standardized compliance finding.
    """

    if outcome not in VALID_OUTCOMES:
        raise ValueError(
            f"Invalid outcome: {outcome}"
        )

    if severity not in VALID_SEVERITIES:
        raise ValueError(
            f"Invalid severity: {severity}"
        )

    return {
        "rule_id": rule_id,
        "outcome": outcome,
        "severity": severity,
        "message": message,
        "evidence": list(evidence or []),
        "legal_sources": list(
            legal_sources or []
        ),
        "remediation": remediation,
        "details": details or {},
    }


# ---------------------------------------------------------------------------
# Missing evidence
# ---------------------------------------------------------------------------

def require(
    value: Any,
    rule_id: str,
    label: str,
    legal_sources: Optional[Iterable[str]] = None,
    severity: str = "HIGH",
) -> Optional[Dict[str, Any]]:
    """
    Create a REVIEW finding when required evidence is missing.
    """

    if value is None:
        return finding(
            rule_id=rule_id,
            outcome="REVIEW",
            severity=severity,
            message=f"Required evidence is missing: {label}.",
            legal_sources=legal_sources,
            remediation=f"Provide or verify {label}.",
        )

    if isinstance(value, str) and not value.strip():
        return finding(
            rule_id=rule_id,
            outcome="REVIEW",
            severity=severity,
            message=f"Required evidence is missing: {label}.",
            legal_sources=legal_sources,
            remediation=f"Provide or verify {label}.",
        )

    return None


# ---------------------------------------------------------------------------
# Readiness calculation
# ---------------------------------------------------------------------------

def readiness(
    findings: List[Dict[str, Any]],
) -> str:
    """
    Convert rule findings into a module-level readiness state.

    Precedence:

        FAIL  -> NOT_READY_FOR_FILING
        REVIEW -> REVIEW_REQUIRED
        no findings blocking -> READY_FOR_FILING
    """

    if any(
        item.get("outcome") == "FAIL"
        for item in findings
    ):
        return "NOT_READY_FOR_FILING"

    if any(
        item.get("outcome") == "REVIEW"
        for item in findings
    ):
        return "REVIEW_REQUIRED"

    return "READY_FOR_FILING"


# ---------------------------------------------------------------------------
# Finding helpers
# ---------------------------------------------------------------------------

def has_failures(
    findings: List[Dict[str, Any]]
) -> bool:
    return any(
        item.get("outcome") == "FAIL"
        for item in findings
    )


def has_reviews(
    findings: List[Dict[str, Any]]
) -> bool:
    return any(
        item.get("outcome") == "REVIEW"
        for item in findings
    )


def count_by_outcome(
    findings: List[Dict[str, Any]]
) -> Dict[str, int]:
    """
    Return counts of PASS/FAIL/REVIEW findings.
    """

    result = {
        "PASS": 0,
        "FAIL": 0,
        "REVIEW": 0,
    }

    for item in findings:
        outcome = item.get("outcome")

        if outcome in result:
            result[outcome] += 1

    return result