"""
EPFO establishment registration schema.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RegistrationData(BaseModel):
    """
    Structured establishment registration information.
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
        description="Name of the establishment.",
    )

    pan: Optional[str] = Field(
        default=None,
        description="PAN associated with the establishment.",
    )

    registration_date: Optional[date] = Field(
        default=None,
        description="Date of EPFO registration.",
    )

    coverage_basis: Optional[str] = Field(
        default=None,
        description="Basis of EPFO coverage.",
    )

    registration_number: Optional[str] = Field(
        default=None,
        description="Registration/reference number, if available.",
    )

    establishment_type: Optional[str] = Field(
        default=None,
        description="Type of establishment.",
    )

    address: Optional[str] = Field(
        default=None,
        description="Registered address.",
    )

    state: Optional[str] = Field(
        default=None,
        description="State of establishment.",
    )

    district: Optional[str] = Field(
        default=None,
        description="District of establishment.",
    )

    effective_from: Optional[date] = Field(
        default=None,
        description="Effective date of EPFO coverage.",
    )