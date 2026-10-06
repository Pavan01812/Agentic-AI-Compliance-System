"""
Tests for EPFO compliance registry.
"""

import pytest

from domains.epfo.registry import (
    EPFO_COMPLIANCE_REGISTRY,
    get_assessor,
    get_compliance,
    is_supported,
    list_compliances,
)


EXPECTED_COMPLIANCES = {
    "EPFO.REGISTRATION",
    "EPFO.FORM5A",
    "EPFO.UAN",
    "EPFO.ECR",
    "EPFO.CONTRIBUTION",
}


def test_all_expected_compliances_registered():
    registered = set(
        EPFO_COMPLIANCE_REGISTRY.keys()
    )

    assert EXPECTED_COMPLIANCES.issubset(
        registered
    )


def test_registry_contains_five_epfo_modules():
    assert len(EPFO_COMPLIANCE_REGISTRY) == 5


@pytest.mark.parametrize(
    "compliance_id",
    sorted(EXPECTED_COMPLIANCES),
)
def test_compliance_can_be_retrieved(compliance_id):
    compliance = get_compliance(
        compliance_id
    )

    assert compliance["name"]
    assert compliance["category"]
    assert compliance["description"]
    assert callable(compliance["assessor"])


@pytest.mark.parametrize(
    "compliance_id",
    sorted(EXPECTED_COMPLIANCES),
)
def test_assessor_can_be_retrieved(compliance_id):
    assessor = get_assessor(
        compliance_id
    )

    assert callable(assessor)


def test_unknown_compliance_raises_key_error():
    with pytest.raises(KeyError):
        get_compliance(
            "EPFO.UNKNOWN"
        )


def test_unknown_assessor_raises_key_error():
    with pytest.raises(KeyError):
        get_assessor(
            "EPFO.UNKNOWN"
        )


def test_supported_compliance():
    for compliance_id in EXPECTED_COMPLIANCES:
        assert is_supported(
            compliance_id
        )


def test_unsupported_compliance():
    assert not is_supported(
        "EPFO.UNKNOWN"
    )


def test_list_compliances():
    compliances = list_compliances()

    assert len(compliances) == 5

    ids = {
        item["compliance_id"]
        for item in compliances
    }

    assert ids == EXPECTED_COMPLIANCES