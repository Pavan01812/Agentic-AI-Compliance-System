"""
EPFO evidence normalization utilities.

Converts extracted or manually supplied evidence into a consistent
canonical representation before it reaches deterministic compliance rules.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Iterable, Optional


def normalize_text(value: Any) -> Optional[str]:
    """Normalize a text value."""
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    return " ".join(text.split())


def normalize_upper_text(value: Any) -> Optional[str]:
    """Normalize text and convert it to uppercase."""
    value = normalize_text(value)

    if value is None:
        return None

    return value.upper()


def normalize_identifier(value: Any) -> Optional[str]:
    """Normalize an identifier by removing surrounding/internal whitespace."""
    value = normalize_text(value)

    if value is None:
        return None

    return value.replace(" ", "").replace("\t", "").upper()


def normalize_pan(value: Any) -> Optional[str]:
    """Normalize an Indian PAN."""
    value = normalize_identifier(value)

    if value is None:
        return None

    return value


def normalize_uan(value: Any) -> Optional[str]:
    """Normalize a UAN to a digit-only representation."""
    value = normalize_identifier(value)

    if value is None:
        return None

    return value


def normalize_establishment_code(value: Any) -> Optional[str]:
    """Normalize an EPFO establishment code."""
    value = normalize_identifier(value)

    if value is None:
        return None

    return value


def normalize_boolean(value: Any) -> Optional[bool]:
    """Convert common extracted boolean representations."""
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, (int, float)):
        if value == 1:
            return True
        if value == 0:
            return False

    text = normalize_upper_text(value)

    if text in {"TRUE", "YES", "Y", "1", "T"}:
        return True

    if text in {"FALSE", "NO", "N", "0", "F"}:
        return False

    return None


def normalize_decimal(value: Any) -> Optional[Decimal]:
    """Convert a numeric value to Decimal."""
    if value is None or value == "":
        return None

    if isinstance(value, Decimal):
        return value

    try:
        text = str(value).strip()
        text = text.replace(",", "")
        text = text.replace("₹", "")
        text = text.replace("INR", "")
        text = text.strip()

        if not text:
            return None

        return Decimal(text)

    except (InvalidOperation, ValueError, TypeError):
        return None


def normalize_date(value: Any) -> Optional[str]:
    """
    Normalize common date representations to ISO YYYY-MM-DD.

    Returns None when the value cannot be interpreted safely.
    """

    if value is None:
        return None

    if isinstance(value, datetime):
        return value.date().isoformat()

    if isinstance(value, date):
        return value.isoformat()

    text = normalize_text(value)

    if not text:
        return None

    formats = (
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d.%m.%Y",
        "%Y/%m/%d",
        "%d-%b-%Y",
        "%d-%B-%Y",
        "%d %b %Y",
        "%d %B %Y",
    )

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue

    return None


def normalize_period(value: Any) -> Optional[str]:
    """
    Normalize an assessment period.

    Accepted examples:
        2025-04
        04-2025
        Apr-2025
        April 2025
    """

    if value is None:
        return None

    text = normalize_upper_text(value)

    if not text:
        return None

    month_map = {
        "JAN": "01",
        "JANUARY": "01",
        "FEB": "02",
        "FEBRUARY": "02",
        "MAR": "03",
        "MARCH": "03",
        "APR": "04",
        "APRIL": "04",
        "MAY": "05",
        "JUN": "06",
        "JUNE": "06",
        "JUL": "07",
        "JULY": "07",
        "AUG": "08",
        "AUGUST": "08",
        "SEP": "09",
        "SEPT": "09",
        "SEPTEMBER": "09",
        "OCT": "10",
        "OCTOBER": "10",
        "NOV": "11",
        "NOVEMBER": "11",
        "DEC": "12",
        "DECEMBER": "12",
    }

    compact = text.replace(" ", "").replace("/", "-").replace(".", "-")

    parts = compact.split("-")

    if len(parts) == 2:
        first, second = parts

        if len(first) == 4 and first.isdigit() and second.isdigit():
            month = int(second)

            if 1 <= month <= 12:
                return f"{first}-{month:02d}"

        if len(second) == 4 and second.isdigit():
            month = month_map.get(first)

            if month:
                return f"{second}-{month}"

            if first.isdigit():
                month = int(first)

                if 1 <= month <= 12:
                    return f"{second}-{month:02d}"

    return None


def normalize_value(field_name: str, value: Any) -> Any:
    """
    Normalize a value according to a canonical field name.
    """

    field = normalize_identifier(field_name)

    if field is None:
        return normalize_text(value)

    if field in {
        "ESTABLISHMENT_NAME",
        "ESTABLISHMENT_NAME_AS_PER_PAN",
        "EMPLOYEE_NAME",
        "EMPLOYER_NAME",
        "MEMBER_NAME",
        "NAME",
        "COVERAGE_BASIS",
        "STATE",
        "DISTRICT",
        "ADDRESS",
        "STATUS",
        "PAYMENT_STATUS",
        "CURRENCY",
    }:
        return normalize_upper_text(value)

    if field in {
        "PAN",
    }:
        return normalize_pan(value)

    if field in {
        "UAN",
    }:
        return normalize_uan(value)

    if field in {
        "ESTABLISHMENT_CODE",
        "MEMBER_ID",
        "TRRN",
    }:
        return normalize_establishment_code(value)

    if field in {
        "WAGES",
        "EPF_WAGES",
        "EPS_WAGES",
        "EDLI_WAGES",
        "EMPLOYEE_SHARE",
        "EMPLOYER_SHARE",
        "EMPLOYEE_TOTAL",
        "EMPLOYER_TOTAL",
        "ECR_TOTAL",
        "CHALLAN_AMOUNT",
        "PAID_AMOUNT",
        "ARREARS",
        "REFUND",
    }:
        return normalize_decimal(value)

    if field in {
        "DATE_OF_JOINING",
        "DATE_OF_EXIT",
        "DOB",
        "REGISTRATION_DATE",
        "EFFECTIVE_FROM",
        "PAYMENT_DATE",
    }:
        return normalize_date(value)

    if field in {
        "PERIOD",
        "ASSESSMENT_PERIOD",
    }:
        return normalize_period(value)

    if field in {
        "FIRST_TIME_MEMBER",
        "AADHAAR_LINKED",
    }:
        return normalize_boolean(value)

    return normalize_text(value)


def normalize_record(
    record: Dict[str, Any],
    fields: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """
    Normalize a dictionary of extracted evidence.

    Unknown fields are preserved.
    """

    if not isinstance(record, dict):
        return {}

    field_set = set(fields or record.keys())

    normalized: Dict[str, Any] = {}

    for key, value in record.items():
        if key in field_set:
            normalized[key] = normalize_value(key, value)
        else:
            normalized[key] = value

    return normalized


def normalize_records(
    records: Iterable[Dict[str, Any]],
    fields: Optional[Iterable[str]] = None,
) -> list[Dict[str, Any]]:
    """Normalize multiple evidence records."""
    return [
        normalize_record(record, fields=fields)
        for record in records
        if isinstance(record, dict)
    ]


def normalize_evidence(
    evidence: Any,
) -> Any:
    """
    Recursively normalize EPFO evidence while preserving metadata and
    nested record structures.

    This is intentionally conservative: values are only normalized when a
    canonical EPFO field name or safe conversion rule is known. Unknown or
    ambiguous values are left intact instead of being guessed.
    """

    if evidence is None:
        return None

    if isinstance(evidence, dict):
        normalized: Dict[str, Any] = {}

        for key, value in evidence.items():
            if not isinstance(key, str):
                normalized[key] = value
                continue

            if isinstance(value, dict):
                normalized[key] = normalize_evidence(value)
                continue

            if isinstance(value, list):
                normalized[key] = [
                    normalize_evidence(item)
                    for item in value
                ]
                continue

            if key.startswith("_"):
                normalized[key] = value
                continue

            normalized[key] = normalize_value(key, value)

        return normalized

    if isinstance(evidence, list):
        return [normalize_evidence(item) for item in evidence]

    return evidence
