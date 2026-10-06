"""
Tests for EPFO ECR compliance.
"""

from domains.epfo.compliance.ecr import assess_ecr


def base_context():
    return {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
        "assessment_period": "2026-09",
    }


def compliant_ecr():
    return {
        "period": "2026-09",
        "establishment_code": "1234567",
        "rows": [
            {
                "uan": "100000000001",
                "employee_name": "Rahul Sharma",
                "establishment_code": "1234567",
                "wages": 30000,
                "epf_wages": 30000,
                "eps_wages": 30000,
                "edli_wages": 30000,
                "employee_share": 3600,
                "employer_share": 3600,
                "ncp_days": 0,
            }
        ],
    }


def test_ecr_compliant():
    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": compliant_ecr()},
    )

    assert result["compliance_id"] == "EPFO.ECR"
    assert result["readiness"] == "READY_FOR_FILING"


def test_ecr_period_mismatch_fails():
    ecr = compliant_ecr()
    ecr["period"] = "2026-08"

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_ecr_establishment_mismatch_fails():
    ecr = compliant_ecr()
    ecr["establishment_code"] = "7654321"

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_ecr_invalid_uan_fails():
    ecr = compliant_ecr()
    ecr["rows"][0]["uan"] = "12345"

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_ecr_duplicate_uan_fails():
    ecr = compliant_ecr()

    ecr["rows"].append({
        "uan": "100000000001",
        "employee_name": "Priya Nair",
        "establishment_code": "1234567",
        "wages": 28000,
        "epf_wages": 28000,
        "eps_wages": 28000,
        "edli_wages": 28000,
        "employee_share": 3360,
        "employer_share": 3360,
        "ncp_days": 0,
    })

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_ecr_wage_component_exceeds_total_wages():
    ecr = compliant_ecr()
    ecr["rows"][0]["epf_wages"] = 35000

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_ecr_invalid_ncp_days():
    ecr = compliant_ecr()
    ecr["rows"][0]["ncp_days"] = 32

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_ecr_missing_employee_name_requires_review():
    ecr = compliant_ecr()
    ecr["rows"][0]["employee_name"] = None

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "REVIEW_REQUIRED"


def test_ecr_missing_rows_requires_review():
    ecr = {
        "period": "2026-09",
        "establishment_code": "1234567",
        "rows": [],
    }

    result = assess_ecr(
        context=base_context(),
        evidence={"ecr": ecr},
    )

    assert result["readiness"] == "REVIEW_REQUIRED"