"""
EPFO Form 5A schema.
"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Form5ABranch(BaseModel):
    """
    Branch/establishment location information appearing in Form 5A.
    """

    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
    )

    name: Optional[str] = Field(
        default=None,
        description="Branch name.",
    )

    address: Optional[str] = Field(
        default=None,
        description="Branch address.",
    )

    establishment_code: Optional[str] = Field(
        default=None,
        description="Branch establishment code, if available.",
    )


class Form5AData(BaseModel):
    """
    Structured Form 5A information.

    The field names intentionally match the canonical field names
    used by the EPFO evidence and rule layers.
    """

    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
    )

    establishment_name_as_per_pan: Optional[str] = Field(
        default=None,
        description="Establishment name as appearing against PAN.",
    )

    pan: Optional[str] = Field(
        default=None,
        description="PAN of the establishment.",
    )

    coverage_basis: Optional[str] = Field(
        default=None,
        description="Basis of EPF coverage.",
    )

    establishment_code: Optional[str] = Field(
        default=None,
        description="EPFO establishment code.",
    )

    branches: List[Form5ABranch] = Field(
        default_factory=list,
        description="Branches/locations declared in Form 5A.",
    )

    employer_name: Optional[str] = Field(
        default=None,
        description="Employer/owner name.",
    )

    address: Optional[str] = Field(
        default=None,
        description="Registered address.",
    )

    state: Optional[str] = Field(
        default=None,
        description="State.",
    )

    district: Optional[str] = Field(
        default=None,
        description="District.",
    )

    effective_from: Optional[str] = Field(
        default=None,
        description="Effective date or coverage date.",
    )