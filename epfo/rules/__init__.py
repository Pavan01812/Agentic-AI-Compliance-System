"""
EPFO deterministic compliance rules.

This package contains the rule engine for:

- Establishment registration
- Form 5A
- UAN/member records
- ECR
- Contribution/challan/payment reconciliation
"""

from .common import (
    finding,
    readiness,
    normalize_text,
    normalize_pan,
    normalize_uan,
    same_text,
    same_identifier,
    valid_pan,
    valid_uan,
    valid_establishment_code,
    parse_non_negative_number,
)

from .registration_rules import check_registration
from .form5a_rules import check_form5a
from .uan_rules import check_uan
from .ecr_rules import check_ecr
from .contribution_rules import check_contribution


__all__ = [
    "finding",
    "readiness",
    "normalize_text",
    "normalize_pan",
    "normalize_uan",
    "same_text",
    "same_identifier",
    "valid_pan",
    "valid_uan",
    "valid_establishment_code",
    "parse_non_negative_number",
    "check_registration",
    "check_form5a",
    "check_uan",
    "check_ecr",
    "check_contribution",
]