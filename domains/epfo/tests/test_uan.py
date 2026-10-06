"""
Tests for EPFO UAN compliance.
"""

from domains.epfo.compliance.uan import assess_uan


def base_context():
    return {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
    }


def test_uan_compliant():
    evidence = {
        "uan_records": [
            {
                "uan": "100000000001",
                "member_id": "KA/BLR/1234567/000001",
                "employee_name": "Rahul Sharma",
                "date_of_joining": "2025-01-15",
                "first_time_member": True,
                "previous_uan": None,
                "establishment_code": "1234567",
            }
        ]
    }

    result = assess_uan(
        context=base_context(),
        evidence=evidence,
    )

    assert result["compliance_id"] == "EPFO.UAN"
    assert result["readiness"] == "READY_FOR_FILING"


def test_uan_invalid_format_fails():
    evidence = {
        "uan_records": [
            {
                "uan": "12345",
                "employee_name": "Rahul Sharma",
                "date_of_joining": "2025-01-15",
                "establishment_code": "1234567",
            }
        ]
    }

    result = assess_uan(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"

    assert any(
        finding["outcome"] == "FAIL"
        for finding in result["findings"]
    )


def test_duplicate_uan_fails():
    evidence = {
        "uan_records": [
            {
                "uan": "100000000001",
                "employee_name": "Rahul Sharma",
                "date_of_joining": "2025-01-15",
                "establishment_code": "1234567",
            },
            {
                "uan": "100000000001",
                "employee_name": "Priya Nair",
                "date_of_joining": "2025-03-10",
                "establishment_code": "1234567",
            },
        ]
    }

    result = assess_uan(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_missing_employee_name_requires_review():
    evidence = {
        "uan_records": [
            {
                "uan": "100000000001",
                "employee_name": None,
                "date_of_joining": "2025-01-15",
                "establishment_code": "1234567",
            }
        ]
    }

    result = assess_uan(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "REVIEW_REQUIRED"


def test_missing_date_of_joining_requires_review():
    evidence = {
        "uan_records": [
            {
                "uan": "100000000001",
                "employee_name": "Rahul Sharma",
                "date_of_joining": None,
                "establishment_code": "1234567",
            }
        ]
    }

    result = assess_uan(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "REVIEW_REQUIRED"


def test_uan_establishment_mismatch_fails():
    evidence = {
        "uan_records": [
            {
                "uan": "100000000001",
                "employee_name": "Rahul Sharma",
                "date_of_joining": "2025-01-15",
                "establishment_code": "7654321",
            }
        ]
    }

    result = assess_uan(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"