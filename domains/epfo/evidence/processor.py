"""
EPFO evidence processing layer.

Responsibilities:

1. Normalize extracted evidence.
2. Identify available document types.
3. Validate required document presence.
4. Preserve evidence provenance.
5. Produce clean evidence for deterministic compliance rules.

This layer does not decide compliance.
Deterministic rules remain responsible for PASS / FAIL / REVIEW.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, Optional

from .evidence_requirements import (
    validate_evidence_presence,
)
from .normalizer import (
    normalize_evidence,
)


class EvidenceProcessingResult:
    """Structured result produced by EPFO evidence processing."""

    def __init__(
        self,
        evidence: Dict[str, Any],
        missing: Optional[list[str]] = None,
        warnings: Optional[list[str]] = None,
        provenance: Optional[list[Dict[str, Any]]] = None,
        available_document_types: Optional[list[str]] = None,
    ) -> None:

        self.evidence = evidence
        self.missing = missing or []
        self.warnings = warnings or []
        self.provenance = provenance or []
        self.available_document_types = (
            available_document_types or []
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable representation."""

        return {
            "evidence": self.evidence,
            "missing": self.missing,
            "warnings": self.warnings,
            "provenance": self.provenance,
            "available_document_types": (
                self.available_document_types
            ),
        }


def extract_provenance(
    evidence: Dict[str, Any],
) -> list[Dict[str, Any]]:
    """
    Extract optional provenance metadata.

    Supported metadata structure:

    "_provenance": [
        {
            "document": "form5a.pdf",
            "document_type": "FORM_5A",
            "page": 2,
            "source": "uploaded_document"
        }
    ]
    """

    provenance = evidence.get(
        "_provenance",
        [],
    )

    if not isinstance(provenance, list):
        return []

    return [
        item
        for item in provenance
        if isinstance(item, dict)
    ]


def extract_document_types(
    evidence: Dict[str, Any],
) -> list[str]:
    """
    Extract available document types from evidence.

    Preferred structure:

    "_documents": [
        {
            "document_type": "FORM_5A",
            "document": "form5a.pdf"
        }
    ]

    Also supports:

    "_document_types": [
        "FORM_5A",
        "ECR_FILE"
    ]

    The method intentionally does not infer document types
    from arbitrary evidence sections.
    """

    document_types: set[str] = set()

    explicit_types = evidence.get(
        "_document_types",
        [],
    )

    if isinstance(explicit_types, list):
        for value in explicit_types:
            if isinstance(value, str) and value.strip():
                document_types.add(
                    value.strip().upper()
                )

    documents = evidence.get(
        "_documents",
        [],
    )

    if isinstance(documents, list):
        for document in documents:
            if not isinstance(document, dict):
                continue

            document_type = document.get(
                "document_type"
            )

            if (
                isinstance(document_type, str)
                and document_type.strip()
            ):
                document_types.add(
                    document_type.strip().upper()
                )

    return sorted(document_types)


def remove_internal_metadata(
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Remove processor-only metadata.

    Deterministic compliance rules should receive
    the actual evidence, not processor metadata.
    """

    cleaned = deepcopy(evidence)

    cleaned.pop(
        "_provenance",
        None,
    )

    cleaned.pop(
        "_documents",
        None,
    )

    cleaned.pop(
        "_document_types",
        None,
    )

    cleaned.pop(
        "_metadata",
        None,
    )

    return cleaned


def process_evidence(
    evidence: Optional[Dict[str, Any]],
    compliance_id: Optional[str] = None,
) -> EvidenceProcessingResult:
    """
    Normalize and validate EPFO evidence.

    Parameters
    ----------
    evidence:
        Raw or partially normalized EPFO evidence.

    compliance_id:
        Optional compliance identifier such as
        EPFO.REGISTRATION or EPFO.ECR.

    Returns
    -------
    EvidenceProcessingResult
        Normalized evidence and document-presence information.
    """

    raw_evidence = (
        evidence
        if isinstance(evidence, dict)
        else {}
    )

    # ---------------------------------------------------------------
    # 1. Normalize extracted values
    # ---------------------------------------------------------------

    normalized = normalize_evidence(
        raw_evidence
    )

    # ---------------------------------------------------------------
    # 2. Extract document metadata
    # ---------------------------------------------------------------

    provenance = extract_provenance(
        normalized
    )

    available_document_types = (
        extract_document_types(
            normalized
        )
    )

    # ---------------------------------------------------------------
    # 3. Validate required document presence
    # ---------------------------------------------------------------

    missing: list[str] = []
    warnings: list[str] = []

    if compliance_id:

        validation = validate_evidence_presence(
            compliance_id=compliance_id,
            available_document_types=(
                available_document_types
            ),
        )

        if validation.get("known"):

            missing = list(
                validation.get(
                    "missing",
                    [],
                )
            )

            if missing:

                warnings.append(
                    "Required EPFO evidence documents "
                    "are missing."
                )

        else:

            warnings.append(
                f"Unknown EPFO compliance ID: "
                f"{compliance_id}"
            )

    # ---------------------------------------------------------------
    # 4. Remove internal metadata
    # ---------------------------------------------------------------

    clean_evidence = remove_internal_metadata(
        normalized
    )

    return EvidenceProcessingResult(
        evidence=clean_evidence,
        missing=missing,
        warnings=warnings,
        provenance=provenance,
        available_document_types=(
            available_document_types
        ),
    )


def process_for_compliance(
    compliance_id: str,
    evidence: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Convenience wrapper returning a serializable result.
    """

    result = process_evidence(
        evidence=evidence,
        compliance_id=compliance_id,
    )

    return result.to_dict()


def get_available_evidence_sections(
    evidence: Optional[Dict[str, Any]],
) -> list[str]:
    """
    Return available top-level evidence sections.

    Internal metadata sections are excluded.
    """

    if not isinstance(evidence, dict):
        return []

    return [
        key
        for key in evidence.keys()
        if not key.startswith("_")
    ]


def get_missing_required_evidence(
    compliance_id: str,
    evidence: Optional[Dict[str, Any]],
) -> list[str]:
    """
    Return missing required document types.
    """

    result = process_evidence(
        evidence=evidence,
        compliance_id=compliance_id,
    )

    return result.missing