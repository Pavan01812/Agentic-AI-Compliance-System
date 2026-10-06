"""
Tests for EPFO Form 5A compliance.
"""

from domains.epfo.compliance.form5a import assess_form5a


def base_context():
    return {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
    }


def test_form5a_compliant():
    evidence = {
        "form5a": {
            "establishment_name_as_per_pan": "ABC Technologies Pvt Ltd",
            "pan": "ABCDE1234F",
            "coverage_basis": "EPF_ACT",
            "establishment_code": "1234567",
            "branches": [],
        }
    }

    result = assess_form5a(
        context=base_context(),
        evidence=evidence,
    )

    assert result["compliance_id"] == "EPFO.FORM5A"
    assert result["readiness"] == "READY_FOR_FILING"


def test_form5a_pan_mismatch_fails():
    evidence = {
        "form5a": {
            "establishment_name_as_per_pan": "ABC Technologies Pvt Ltd",
            "pan": "ABCDE9999F",
            "coverage_basis": "EPF_ACT",
            "establishment_code": "1234567",
            "branches": [],
        }
    }

    result = assess_form5a(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"

    assert any(
        finding["outcome"] == "FAIL"
        for finding in result["findings"]
    )


def test_form5a_name_mismatch_requires_review():
    evidence = {
        "form5a": {
            "establishment_name_as_per_pan": "Different Technologies Pvt Ltd",
            "pan": "ABCDE1234F",
            "coverage_basis": "EPF_ACT",
            "establishment_code": "1234567",
            "branches": [],
        }
    }

    result = assess_form5a(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "REVIEW_REQUIRED"


def test_form5a_missing_data_requires_review():
    evidence = {
        "form5a": {}
    }

    result = assess_form5a(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "REVIEW_REQUIRED"

    assert any(
        finding["outcome"] == "REVIEW"
        for finding in result["findings"]
    )


def test_form5a_establishment_code_mismatch():
    evidence = {
        "form5a": {
            "establishment_name_as_per_pan": "ABC Technologies Pvt Ltd",
            "pan": "ABCDE1234F",
            "coverage_basis": "EPF_ACT",
            "establishment_code": "7654321",
            "branches": [],
        }
    }

    result = assess_form5a(
        context=base_context(),
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"