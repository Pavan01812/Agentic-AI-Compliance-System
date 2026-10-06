"""
Tests for EPFO domain orchestration.
"""

import json
from pathlib import Path

import pytest

from domains.epfo.orchestration import assess_epfo


SAMPLE_CASES_DIR = (
    Path(__file__).resolve().parent.parent / "sample_cases"
)


def load_case(filename):
    path = SAMPLE_CASES_DIR / filename

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_compliant_case_is_ready():
    case = load_case("compliant_case.json")

    result = assess_epfo(
        context=case["context"],
        evidence=case["evidence"],
    )

    assert result["domain"] == "EPFO"

    assert (
        result["overall_readiness"]
        == "READY_FOR_FILING"
    )

    assert result["module_count"] == 5

    assert result["summary"]["failed_modules"] == 0
    assert result["summary"]["review_modules"] == 0


def test_non_compliant_case_is_not_ready():
    case = load_case("non_compliant_case.json")

    result = assess_epfo(
        context=case["context"],
        evidence=case["evidence"],
    )

    assert (
        result["overall_readiness"]
        == "NOT_READY_FOR_FILING"
    )

    assert result["summary"]["failed_modules"] > 0
    assert result["summary"]["fail_findings"] > 0


def test_review_case_requires_review():
    case = load_case("review_required_case.json")

    result = assess_epfo(
        context=case["context"],
        evidence=case["evidence"],
    )

    assert (
        result["overall_readiness"]
        == "REVIEW_REQUIRED"
    )

    assert result["summary"]["review_modules"] > 0
    assert result["summary"]["review_findings"] > 0


def test_single_module_orchestration():
    case = load_case("compliant_case.json")

    result = assess_epfo(
        context=case["context"],
        evidence=case["evidence"],
        compliance_ids=[
            "EPFO.REGISTRATION"
        ],
    )

    assert result["module_count"] == 1

    assert (
        result["modules_assessed"]
        == ["EPFO.REGISTRATION"]
    )

    assert (
        result["overall_readiness"]
        == "READY_FOR_FILING"
    )


def test_multiple_selected_modules():
    case = load_case("compliant_case.json")

    result = assess_epfo(
        context=case["context"],
        evidence=case["evidence"],
        compliance_ids=[
            "EPFO.REGISTRATION",
            "EPFO.FORM5A",
            "EPFO.UAN",
        ],
    )

    assert result["module_count"] == 3

    assert (
        result["overall_readiness"]
        == "READY_FOR_FILING"
    )


def test_unknown_compliance_id():
    case = load_case("compliant_case.json")

    with pytest.raises(ValueError):
        assess_epfo(
            context=case["context"],
            evidence=case["evidence"],
            compliance_ids=[
                "EPFO.UNKNOWN"
            ],
        )


def test_empty_module_selection():
    case = load_case("compliant_case.json")

    result = assess_epfo(
        context=case["context"],
        evidence=case["evidence"],
        compliance_ids=[],
    )

    assert result["module_count"] == 0

    assert (
        result["overall_readiness"]
        == "REVIEW_REQUIRED"
    )