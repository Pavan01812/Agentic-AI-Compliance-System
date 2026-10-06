"""
EPFO domain orchestration.

This module coordinates the individual EPFO compliance assessors.

Important:
- Rules remain deterministic.
- Missing/ambiguous evidence is not guessed.
- Individual modules can be assessed independently.
"""

from typing import Any, Dict, Iterable, Optional

from .registry import (
    EPFO_COMPLIANCE_REGISTRY,
    get_assessor,
)


def assess_epfo(
    context: Optional[Dict[str, Any]] = None,
    evidence: Optional[Dict[str, Any]] = None,
    compliance_ids: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """
    Run one or more EPFO compliance assessments.

    Args:
        context:
            Establishment/employer context.

        evidence:
            Evidence extracted from documents or structured records.

        compliance_ids:
            Specific EPFO modules to execute.
            If omitted, all registered EPFO modules are executed.

    Returns:
        Consolidated EPFO assessment result.
    """

    context = context or {}
    evidence = evidence or {}

    if compliance_ids is None:
        selected_ids = list(EPFO_COMPLIANCE_REGISTRY.keys())
    else:
        selected_ids = list(compliance_ids)

    unknown_ids = [
        compliance_id
        for compliance_id in selected_ids
        if compliance_id not in EPFO_COMPLIANCE_REGISTRY
    ]

    if unknown_ids:
        raise ValueError(
            f"Unsupported EPFO compliance IDs: {unknown_ids}"
        )

    results = []

    for compliance_id in selected_ids:
        assessor = get_assessor(compliance_id)

        result = assessor(
            context=context,
            evidence=evidence,
        )

        results.append(result)

    readiness_values = [
        result.get("readiness")
        for result in results
        if result.get("readiness")
    ]

    overall_readiness = _calculate_overall_readiness(
        readiness_values
    )

    return {
        "domain": "EPFO",
        "domain_name": "Employees' Provident Fund Organisation",
        "modules_assessed": selected_ids,
        "module_count": len(results),
        "overall_readiness": overall_readiness,
        "results": results,
        "summary": _build_summary(results),
    }


def _calculate_overall_readiness(
    readiness_values: list[str],
) -> str:
    """
    Calculate domain-level readiness.

    Priority:
        NOT_READY_FOR_FILING
        REVIEW_REQUIRED
        READY_FOR_FILING
    """

    if not readiness_values:
        return "REVIEW_REQUIRED"

    if "NOT_READY_FOR_FILING" in readiness_values:
        return "NOT_READY_FOR_FILING"

    if "REVIEW_REQUIRED" in readiness_values:
        return "REVIEW_REQUIRED"

    if all(
        readiness == "READY_FOR_FILING"
        for readiness in readiness_values
    ):
        return "READY_FOR_FILING"

    return "REVIEW_REQUIRED"


def _build_summary(results: list[Dict[str, Any]]) -> Dict[str, int]:
    """
    Build a compact summary of findings across modules.
    """

    summary = {
        "modules": len(results),
        "ready_modules": 0,
        "review_modules": 0,
        "failed_modules": 0,
        "total_findings": 0,
        "pass_findings": 0,
        "review_findings": 0,
        "fail_findings": 0,
    }

    for result in results:

        readiness = result.get("readiness")

        if readiness == "READY_FOR_FILING":
            summary["ready_modules"] += 1

        elif readiness == "REVIEW_REQUIRED":
            summary["review_modules"] += 1

        elif readiness == "NOT_READY_FOR_FILING":
            summary["failed_modules"] += 1

        findings = result.get("findings", [])

        summary["total_findings"] += len(findings)

        for item in findings:
            outcome = item.get("outcome")

            if outcome == "PASS":
                summary["pass_findings"] += 1

            elif outcome == "REVIEW":
                summary["review_findings"] += 1

            elif outcome == "FAIL":
                summary["fail_findings"] += 1

    return summary