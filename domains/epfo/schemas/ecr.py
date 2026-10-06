"""
EPFO Electronic Challan-cum-Return schemas.
"""

from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ECRRow(BaseModel):
    """
    One employee/member row from an ECR.

    Numeric fields use Decimal to avoid floating-point rounding
    problems when handling contribution amounts.
    """

    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
    )

    uan: Optional[str] = Field(
        default=None,
        description="12-digit Universal Account Number.",
    )

    employee_name: Optional[str] = Field(
        default=None,
        description="Employee/member name.",
    )

    establishment_code: Optional[str] = Field(
        default=None,
        description="Establishment code for the row.",
    )

    wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Total wages.",
    )

    epf_wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="EPF wages.",
    )

    eps_wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="EPS wages.",
    )

    edli_wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="EDLI wages.",
    )

    employee_share: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Employee contribution/share.",
    )

    employer_share: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Employer contribution/share.",
    )

    ncp_days: Optional[int] = Field(
        default=None,
        ge=0,
        le=31,
        description="Non-contributory period days.",
    )

    refund_of_advance: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Refund of advance, if present.",
    )

    arrear_epf_wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Arrear EPF wages, if applicable.",
    )

    arrear_eps_wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Arrear EPS wages, if applicable.",
    )

    arrear_edli_wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Arrear EDLI wages, if applicable.",
    )


class ECRData(BaseModel):
    """
    Complete structured ECR submission/return.
    """

    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
    )

    period: Optional[str] = Field(
        default=None,
        description="ECR wage/assessment period, e.g. 2026-09.",
    )

    establishment_code: Optional[str] = Field(
        default=None,
        description="Establishment code for the ECR.",
    )

    rows: List[ECRRow] = Field(
        default_factory=list,
        description="Employee/member contribution rows.",
    )

    ecr_reference: Optional[str] = Field(
        default=None,
        description="ECR reference/acknowledgement number.",
    )

    filing_date: Optional[str] = Field(
        default=None,
        description="Date of ECR filing.",
    )

    status: Optional[str] = Field(
        default=None,
        description="ECR processing status.",
    )

    total_wages: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Declared total wages, if available.",
    )

    total_employee_share: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Declared employee contribution total.",
    )

    total_employer_share: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Declared employer contribution total.",
    )

    total_contribution: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Declared total contribution.",
    )

    def calculate_totals(self) -> dict:
        """
        Calculate aggregate values directly from ECR rows.

        Returns:
            Dictionary containing calculated totals.
        """

        total_wages = sum(
            (row.wages or Decimal("0"))
            for row in self.rows
        )

        total_employee_share = sum(
            (row.employee_share or Decimal("0"))
            for row in self.rows
        )

        total_employer_share = sum(
            (row.employer_share or Decimal("0"))
            for row in self.rows
        )

        total_contribution = (
            total_employee_share +
            total_employer_share
        )

        return {
            "total_wages": total_wages,
            "total_employee_share": total_employee_share,
            "total_employer_share": total_employer_share,
            "total_contribution": total_contribution,
            "row_count": len(self.rows),
        }