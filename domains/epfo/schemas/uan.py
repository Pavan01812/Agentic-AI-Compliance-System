"""
EPFO UAN/member schema.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UANRecord(BaseModel):
    """
    Individual employee UAN/member record.
    """

    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
    )

    uan: Optional[str] = Field(
        default=None,
        description="12-digit Universal Account Number.",
    )

    member_id: Optional[str] = Field(
        default=None,
        description="EPFO member ID.",
    )

    employee_name: Optional[str] = Field(
        default=None,
        description="Employee/member name.",
    )

    date_of_joining: Optional[date] = Field(
        default=None,
        description="Date of joining the establishment.",
    )

    date_of_exit: Optional[date] = Field(
        default=None,
        description="Date of exit, if applicable.",
    )

    first_time_member: Optional[bool] = Field(
        default=None,
        description="Whether this is the employee's first EPF membership.",
    )

    previous_uan: Optional[str] = Field(
        default=None,
        description="Previous UAN, if available.",
    )

    establishment_code: Optional[str] = Field(
        default=None,
        description="Establishment code mapped to the member.",
    )

    gender: Optional[str] = Field(
        default=None,
        description="Member gender, when available.",
    )

    date_of_birth: Optional[date] = Field(
        default=None,
        description="Member date of birth, when available.",
    )

    aadhaar_linked: Optional[bool] = Field(
        default=None,
        description="Whether Aadhaar linkage is recorded.",
    )

    kyc_status: Optional[str] = Field(
        default=None,
        description="KYC status, when available.",
    )