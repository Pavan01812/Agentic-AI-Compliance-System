from domains.epfo.evidence import normalize_evidence, process_evidence
from domains.epfo.evidence.evidence_requirements import validate_evidence_presence


def test_normalize_evidence_canonicalizes_values():
    evidence = {
        "registration": {
            "establishment_code": " 123 4567 ",
            "establishment_name": "  abc technologies pvt ltd  ",
            "pan": " abcd 1234 f ",
            "coverage_basis": " epf_act ",
            "registration_date": "01/04/2024",
        },
        "_documents": [{"document_type": "REGISTRATION_CERTIFICATE"}],
    }

    normalized = normalize_evidence(evidence)

    assert normalized["registration"]["establishment_code"] == "1234567"
    assert normalized["registration"]["establishment_name"] == "ABC TECHNOLOGIES PVT LTD"
    assert normalized["registration"]["pan"] == "ABCD1234F"
    assert normalized["registration"]["coverage_basis"] == "EPF_ACT"
    assert normalized["registration"]["registration_date"] == "2024-04-01"
    assert normalized["_documents"][0]["document_type"] == "REGISTRATION_CERTIFICATE"


def test_process_evidence_tracks_document_presence_and_normalizes_records():
    evidence = {
        "_documents": [{"document_type": "FORM_5A"}],
        "form5a": {
            "establishment_name_as_per_pan": "  abc technologies pvt ltd  ",
            "pan": " abcd 1234 f ",
            "coverage_basis": " epf_act ",
            "establishment_code": " 123 4567 ",
        },
    }

    result = process_evidence(evidence, compliance_id="EPFO.FORM5A")

    assert result.missing == []
    assert result.evidence["form5a"]["pan"] == "ABCD1234F"
    assert result.evidence["form5a"]["establishment_code"] == "1234567"
    assert "FORM_5A" in result.available_document_types


def test_validate_evidence_presence_is_stable_for_known_and_unknown_ids():
    known = validate_evidence_presence("EPFO.REGISTRATION", ["REGISTRATION_CERTIFICATE"])
    unknown = validate_evidence_presence("EPFO.NOPE", ["REGISTRATION_CERTIFICATE"])

    assert known["known"] is True
    assert known["ready_for_content_assessment"] is False
    assert known["missing"]
    assert unknown["known"] is False
    assert unknown["missing"] == []
