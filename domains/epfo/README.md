# EPFO Compliance Domain

[![CI](https://github.com/Pavan01812/Agentic-AI-Compliance-System/actions/workflows/ci.yml/badge.svg)](https://github.com/Pavan01812/Agentic-AI-Compliance-System/actions/workflows/ci.yml)

## Overview

The EPFO domain performs deterministic, employer-side EPFO compliance assessment for registration, Form 5A, UAN/member records, ECR, and contribution/challan reconciliation.

Version: V1

This domain is intentionally independent from the MCA domain and is designed to be independently runnable and independently testable.

---

## 1. EPFO scope

Supported compliance IDs:

- EPFO.REGISTRATION
- EPFO.FORM5A
- EPFO.UAN
- EPFO.ECR
- EPFO.CONTRIBUTION

These modules cover the mandated evidence and deterministic rule checks for the current EPFO scope only.

---

## 2. Architecture

```text
        EPFO DOMAIN
            |
    +-------+-------+
    |               |
 context          evidence
    |               |
    +-------+-------+
            |
     orchestration
            |
   +--------+--------+
   |                 |
 registration    form5a     uan     ecr     contribution
   |                 |
   +---------+-------+
             |
         deterministic rules
             |
       PASS / FAIL / REVIEW
             |
       readiness aggregation
             |
READY_FOR_FILING > REVIEW_REQUIRED > NOT_READY_FOR_FILING
```

The domain keeps a strict separation between:

1. document presence
2. evidence extraction and normalization
3. deterministic rules
4. readiness and reporting

Evidence processing itself does not decide compliance.

---

## 3. Supported modules

| Compliance ID | Module | Purpose |
|---|---|---|
| EPFO.REGISTRATION | Establishment registration | registration identity, PAN, and coverage basis |
| EPFO.FORM5A | Form 5A | establishment/PAN/coverage validation |
| EPFO.UAN | UAN/member records | UAN validity, duplicates, identity, and establishment mapping |
| EPFO.ECR | ECR data | wage-month, row integrity, wage components, and NCP validation |
| EPFO.CONTRIBUTION | Contribution reconciliation | ECR-challan-payment reconciliation and payment metadata |

---

## 4. Folder structure

```text
domains/epfo/
├── __init__.py
├── registry.py
├── orchestration.py
├── README.md
├── compliance/
│   ├── registration.py
│   ├── form5a.py
│   ├── uan.py
│   ├── ecr.py
│   ├── contribution.py
├── evidence/
│   ├── __init__.py
│   ├── document_types.py
│   ├── evidence_requirements.py
│   ├── field_mappings.py
│   ├── normalizer.py
│   └── processor.py
├── legal/
│   ├── __init__.py
│   └── sources.py
├── rules/
│   ├── common.py
│   ├── registration_rules.py
│   ├── form5a_rules.py
│   ├── uan_rules.py
│   ├── ecr_rules.py
│   └── contribution_rules.py
├── schemas/
│   ├── context.py
│   ├── registration.py
│   ├── form5a.py
│   ├── uan.py
│   ├── ecr.py
│   └── contribution.py
├── sample_cases/
│   ├── compliant_case.json
│   ├── non_compliant_case.json
│   └── review_required_case.json
└── tests/
    ├── ...
```

---

## 5. Evidence model

Evidence is supplied as a dictionary keyed by compliance section, for example:

```python
{
    "registration": {...},
    "form5a": {...},
    "uan_records": [...],
    "ecr": {...},
    "contribution": {...},
    "_documents": [{"document_type": "FORM_5A"}],
    "_provenance": [{"document": "form5a.pdf", "document_type": "FORM_5A"}],
}
```

The evidence pipeline is responsible for:

- identifying document types
- checking required evidence presence
- normalizing extracted values
- preserving provenance metadata
- passing clean evidence to deterministic rules

It does not decide compliance by itself.

---

## 6. Document types

The canonical document identifiers include:

- REGISTRATION_CERTIFICATE
- ESTABLISHMENT_RECORD
- FORM_5A
- FORM_11
- UAN_MEMBER_DATA
- MEMBER_REGISTRATION
- ECR_FILE
- ECR_RETURN
- ECR_ACKNOWLEDGEMENT
- CHALLAN
- PAYMENT_RECEIPT
- TRRN_RECORD

Document metadata is available through the evidence utilities and document mapping layer.

---

## 7. Normalization

Normalization is conservative. The system strips extraneous whitespace, canonicalizes common EPFO identifiers, and converts safely identifiable values such as dates, numbers, booleans, PANs, UANs, establishment codes, periods, and common field aliases.

If a value cannot be safely interpreted, it is preserved or left as-is rather than guessed.

---

## 8. Rule engine

Deterministic rules are implemented in:

- registration_rules.py
- form5a_rules.py
- uan_rules.py
- ecr_rules.py
- contribution_rules.py

Each finding includes:

- rule_id
- outcome
- severity
- message
- evidence references
- legal_sources
- remediation, when appropriate
- details, where useful

Semantics:

- PASS: objective validation succeeded and evidence is present
- FAIL: objective contradiction or invalid value was detected
- REVIEW: evidence is missing, ambiguous, incomplete, or requires human verification

---

## 9. Orchestration

The public orchestration entry point is:

```python
from domains.epfo.orchestration import assess_epfo

result = assess_epfo(
    context=context,
    evidence=evidence,
)
```

It can also accept a compliance_ids iterable to assess only a subset of EPFO modules.

Readiness precedence is:

```text
NOT_READY_FOR_FILING > REVIEW_REQUIRED > READY_FOR_FILING
```

---

## 10. Registry

The registry exposes the five supported EPFO modules and resolves them by compliance ID:

- get_compliance()
- get_assessor()
- list_compliances()
- is_supported()

Unknown IDs raise a clear error rather than silently falling back.

---

## 11. Legal provenance

Legal source metadata is maintained in the legal package and mapped to rule IDs. Findings include legal source references, enabling traceability without embedding unsupported legal claims directly in rules.

This keeps the deterministic engine tied to a structured provenance model rather than invented statutory assumptions.

---

## 12. Sample cases

The sample cases under the sample_cases folder represent:

- compliant_case.json
- non_compliant_case.json
- review_required_case.json

They are intended to demonstrate the expected readiness states:

- READY_FOR_FILING
- NOT_READY_FOR_FILING
- REVIEW_REQUIRED

---

## 13. Testing

Run the EPFO suite from the project parent directory:

```bash
python -m pytest domains\epfo\tests -v
```

This verifies the EPFO domain independently of the MCA domain.

---

## 14. Integration API

The supported public entry points are:

```python
from domains.epfo.registry import list_compliances
from domains.epfo.orchestration import assess_epfo
```

Expected integration contract:

- context: establishment and assessment metadata
- evidence: structured evidence keyed by section and optional document metadata
- supported compliance IDs: the five EPFO IDs above
- result: dictionary with domain name, module results, readiness, and summary counts
- failure/unknown IDs: explicit exceptions or validation errors

---

## 15. Example input

```python
context = {
    "establishment_code": "1234567",
    "establishment_name": "ABC TECHNOLOGIES PVT LTD",
    "pan": "ABCDE1234F",
    "assessment_period": "2026-09",
}

evidence = {
    "registration": {
        "establishment_code": "1234567",
        "establishment_name": "ABC TECHNOLOGIES PVT LTD",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
    },
    "form5a": {
        "establishment_name_as_per_pan": "ABC TECHNOLOGIES PVT LTD",
        "pan": "ABCDE1234F",
        "coverage_basis": "EPF_ACT",
        "establishment_code": "1234567",
    },
}
```

---

## 16. Example output

```python
{
    "domain": "EPFO",
    "overall_readiness": "READY_FOR_FILING",
    "modules_assessed": [
        "EPFO.REGISTRATION",
        "EPFO.FORM5A",
        "EPFO.UAN",
        "EPFO.ECR",
        "EPFO.CONTRIBUTION",
    ],
    "summary": {
        "modules": 5,
        "ready_modules": 5,
        "review_modules": 0,
        "failed_modules": 0,
    },
}
```

---

## 17. Known limitations

- This domain intentionally does not integrate with MCA.
- Legal sources are structured references, not a full law database.
- Deterministic rules do not invent missing statutory values or contribution rates.
- Ambiguous or missing evidence remains REVIEW unless the existing architecture defines an explicit objective failure.

---

## 18. Future integration boundary

The current EPFO domain is a self-contained compliance engine. It remains ready for later integration into a broader Agentic AI Compliance System without coupling to MCA or making compliance decisions through LLM inference.
