"""
EPFO contribution reconciliation schema.
"""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ContributionData(BaseModel):
    """
    Data required to reconcile ECR, challan and payment information.

    No statutory contribution percentage is hard-coded here.
    The schema represents observed/declared amounts.
    """

    model_config = ConfigDict(
        extra="allow",
        str_strip_whitespace=True,
    )

    period: Optional[str] = Field(
        default=None,
        description="Contribution wage/assessment period.",
    )

    establishment_code: Optional[str] = Field(
        default=None,
        description="EPFO establishment code.",
    )

    ecr_total: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Total contribution derived from ECR.",
    )

    employee_total: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Total employee contribution.",
    )

    employer_total: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Total employer contribution.",
    )

    challan_amount: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Amount appearing on the challan.",
    )

    paid_amount: Optional[Decimal] = Field(
        default=None,
        ge=0,
        description="Amount actually paid.",
    )

    trrn: Optional[str] = Field(
        default=None,
        description="Transaction Reference Number.",
    )

    payment_date: Optional[str] = Field(
        default=None,
        description="Date on which payment was made.",
    )

    payment_status: Optional[str] = Field(
        default=None,
        description="Payment status.",
    )

    transaction_reference: Optional[str] = Field(
        default=None,
        description="Bank/payment transaction reference.",
    )

    challan_reference: Optional[str] = Field(
        default=None,
        description="Challan reference.",
    )

    currency: str = Field(
        default="INR",
        description="Currency used for monetary amounts.",
    )

    def calculate_reconciliation(self) -> dict:
        """
        Calculate differences between ECR, challan and payment amounts.
        """

        ecr_total = self.ecr_total or Decimal("0")
        challan_amount = self.challan_amount or Decimal("0")
        paid_amount = self.paid_amount or Decimal("0")

        return {
            "ecr_total": ecr_total,
            "challan_amount": challan_amount,
            "paid_amount": paid_amount,
            "ecr_to_challan_difference": (
                challan_amount - ecr_total
            ),
            "challan_to_payment_difference": (
                paid_amount - challan_amount
            ),
            "fully_reconciled": (
                ecr_total == challan_amount
                and challan_amount == paid_amount
            ),
        }