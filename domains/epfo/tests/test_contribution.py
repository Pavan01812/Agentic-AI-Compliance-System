"""
Tests for EPFO contribution reconciliation.
"""

from domains.epfo.compliance.contribution import assess_contribution


def base_context():
    return {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "assessment_period": "2026-09",
    }


def compliant_contribution():
    return {
        "period": "2026-09",
        "establishment_code": "1234567",
        "ecr_total": 21600,
        "employee_total": 10800,
        "employer_total": 10800,
        "challan_amount": 21600,
        "paid_amount": 21600,
        "trrn": "TRRN202610123456",
        "payment_date": "2026-10-15",
    }


def test_contribution_compliant():
    result = assess_contribution(
        context=base_context(),
        evidence={
            "contribution": compliant_contribution()
        },
    )

    assert result["compliance_id"] == "EPFO.CONTRIBUTION"
    assert result["readiness"] == "READY_FOR_FILING"


def test_ecr_challan_mismatch_fails():
    data = compliant_contribution()
    data["challan_amount"] = 20000

    result = assess_contribution(
        context=base_context(),
        evidence={"contribution": data},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"

    assert any(
        finding["outcome"] == "FAIL"
        for finding in result["findings"]
    )


def test_challan_payment_mismatch_fails():
    data = compliant_contribution()
    data["paid_amount"] = 19000

    result = assess_contribution(
        context=base_context(),
        evidence={"contribution": data},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_missing_trrn_requires_review():
    data = compliant_contribution()
    data["trrn"] = None

    result = assess_contribution(
        context=base_context(),
        evidence={"contribution": data},
    )

    assert result["readiness"] == "REVIEW_REQUIRED"


def test_missing_payment_date_requires_review():
    data = compliant_contribution()
    data["payment_date"] = None

    result = assess_contribution(
        context=base_context(),
        evidence={"contribution": data},
    )

    assert result["readiness"] == "REVIEW_REQUIRED"


def test_missing_challan_amount_requires_review():
    data = compliant_contribution()
    data["challan_amount"] = None

    result = assess_contribution(
        context=base_context(),
        evidence={"contribution": data},
    )

    assert result["readiness"] == "REVIEW_REQUIRED"


def test_missing_paid_amount_requires_review():
    data = compliant_contribution()
    data["paid_amount"] = None

    result = assess_contribution(
        context=base_context(),
        evidence={"contribution": data},
    )

    assert result["readiness"] == "REVIEW_REQUIRED"