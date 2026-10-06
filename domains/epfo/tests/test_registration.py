"""
Tests for EPFO registration compliance.
"""

from domains.epfo.compliance.registration import assess_registration
from domains.epfo.rules.registration_rules import check_registration


def test_registration_compliant():
    context = {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
    }

    evidence = {
        "registration": {
            "establishment_code": "1234567",
            "establishment_name": "ABC Technologies Pvt Ltd",
            "pan": "ABCDE1234F",
            "coverage_basis": "EPF_ACT",
        }
    }

    result = assess_registration(
        context=context,
        evidence=evidence,
    )

    assert result["compliance_id"] == "EPFO.REGISTRATION"
    assert result["readiness"] == "READY_FOR_FILING"

    assert any(
        finding["outcome"] == "PASS"
        for finding in result["findings"]
    )


def test_registration_pan_mismatch_fails():
    context = {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
    }

    evidence = {
        "registration": {
            "establishment_code": "1234567",
            "establishment_name": "ABC Technologies Pvt Ltd",
            "pan": "ABCDE9999F",
            "coverage_basis": "EPF_ACT",
        }
    }

    result = assess_registration(
        context=context,
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"

    assert any(
        finding["outcome"] == "FAIL"
        for finding in result["findings"]
    )


def test_registration_missing_evidence_requires_review():
    context = {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
    }

    evidence = {
        "registration": {}
    }

    result = assess_registration(
        context=context,
        evidence=evidence,
    )

    assert result["readiness"] == "REVIEW_REQUIRED"

    assert any(
        finding["outcome"] == "REVIEW"
        for finding in result["findings"]
    )


def test_registration_invalid_establishment_code():
    context = {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
    }

    evidence = {
        "registration": {
            "establishment_code": "INVALID",
            "establishment_name": "ABC Technologies Pvt Ltd",
            "pan": "ABCDE1234F",
            "coverage_basis": "EPF_ACT",
        }
    }

    result = assess_registration(
        context=context,
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"


def test_registration_invalid_pan_format():
    context = {
        "establishment_code": "1234567",
        "establishment_name": "ABC Technologies Pvt Ltd",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
    }

    evidence = {
        "registration": {
            "establishment_code": "1234567",
            "establishment_name": "ABC Technologies Pvt Ltd",
            "pan": "INVALIDPAN",
            "coverage_basis": "EPF_ACT",
        }
    }

    result = assess_registration(
        context=context,
        evidence=evidence,
    )

    assert result["readiness"] == "NOT_READY_FOR_FILING"
