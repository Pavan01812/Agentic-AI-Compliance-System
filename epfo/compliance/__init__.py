"""
EPFO compliance modules.

This package contains the five primary EPFO compliance workflows:

1. EPFO Registration
2. Form 5A
3. UAN / Member
4. ECR
5. Contribution / Challan reconciliation
"""

from .registration import assess_registration
from .form5a import assess_form5a
from .uan import assess_uan
from .ecr import assess_ecr
from .contribution import assess_contribution

__all__ = [
    "assess_registration",
    "assess_form5a",
    "assess_uan",
    "assess_ecr",
    "assess_contribution",
]