"""
Common EPFO establishment context.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EPFOContext(BaseModel):
    """
    Common establishment context for EPFO compliance assessment.

    This model contains identity information that can be cross-checked
    against Form 5A, registration records, UAN records and ECR data.
    """

    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
    )

    establishment_code: Optional[str] = Field(
        default=None,
        description="EPFO establishment code.",
    )

    establishment_name: Optional[str] = Field(
        default=None,
        description="Registered establishment name.",
    )

    pan: Optional[str] = Field(
        default=None,
        description="PAN of the establishment.",
    )

    coverage_basis: Optional[str] = Field(
        default=None,
        description="Basis under which the establishment is covered.",
    )

    registration_date: Optional[date] = Field(
        default=None,
        description="Date of EPFO establishment registration.",
    )

    effective_from: Optional[date] = Field(
        default=None,
        description="Date from which EPFO coverage is effective.",
    )

    state: Optional[str] = Field(
        default=None,
        description="State in which the establishment is registered.",
    )

    district: Optional[str] = Field(
        default=None,
        description="District of the establishment.",
    )

    address: Optional[str] = Field(
        default=None,
        description="Registered establishment address.",
    )

    employer_name: Optional[str] = Field(
        default=None,
        description="Employer/owner name where available.",
    )

    employee_count: Optional[int] = Field(
        default=None,
        ge=0,
        description="Employee count, if available.",
    )

    assessment_period: Optional[str] = Field(
        default=None,
        description="Expected assessment/wage period, e.g. 2026-09.",
    )