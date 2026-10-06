"""
EPFO Compliance Domain.

Employer-side EPFO compliance V1.

Supported compliance modules:
- EPFO.REGISTRATION
- EPFO.FORM5A
- EPFO.UAN
- EPFO.ECR
- EPFO.CONTRIBUTION
"""

from .registry import (
    EPFO_COMPLIANCE_REGISTRY,
    get_compliance,
    list_compliances,
)

from .orchestration import (
    assess_epfo,
)

__all__ = [
    "EPFO_COMPLIANCE_REGISTRY",
    "get_compliance",
    "list_compliances",
    "assess_epfo",
]