"""
EPFO document-to-schema field mappings.

These mappings provide extraction vocabulary for Document AI.

The mapping deliberately contains multiple aliases because real documents
may use different labels, capitalization, spacing, or wording.
"""

from typing import Dict, List, Any


FIELD_MAPPINGS: Dict[
    str,
    Dict[str, List[str]]
] = {

    # ===============================================================
    # Registration
    # ===============================================================

    "REGISTRATION_CERTIFICATE": {

        "establishment_code": [
            "establishment code",
            "establishment code number",
            "epf establishment code",
            "pf establishment code",
            "code number",
            "epfo code",
        ],

        "establishment_name": [
            "name of establishment",
            "establishment name",
            "name of the establishment",
            "employer name",
            "name of employer",
        ],

        "pan": [
            "pan",
            "pan number",
            "permanent account number",
            "income tax pan",
        ],

        "registration_date": [
            "registration date",
            "date of registration",
            "date of coverage",
            "coverage date",
        ],

        "coverage_basis": [
            "coverage basis",
            "basis of coverage",
            "basis on which code number was obtained",
            "code obtained based on",
            "applicability basis",
        ],
    },

    # ===============================================================
    # Establishment record
    # ===============================================================

    "ESTABLISHMENT_RECORD": {

        "establishment_code": [
            "establishment code",
            "pf code",
            "epf code",
            "epfo establishment code",
        ],

        "establishment_name": [
            "establishment name",
            "legal name",
            "name of establishment",
            "employer name",
        ],

        "pan": [
            "pan",
            "permanent account number",
            "pan number",
        ],

        "state": [
            "state",
            "state name",
        ],

        "city": [
            "city",
            "town",
            "district",
        ],

        "registration_date": [
            "registration date",
            "date of registration",
            "date of coverage",
        ],
    },

    # ===============================================================
    # Form 5A
    # ===============================================================

    "FORM_5A": {

        "establishment_name_as_per_pan": [
            "name of the establishment as per pan",
            "name of establishment as per pan",
            "establishment name as per pan",
            "name as per pan",
            "pan registered name",
        ],

        "pan": [
            "pan",
            "pan number",
            "permanent account number",
            "permanent account no",
        ],

        "coverage_basis": [
            "code number was obtained based on",
            "basis on which code number was obtained",
            "basis of coverage",
            "coverage basis",
            "reason for coverage",
        ],

        "establishment_code": [
            "establishment code",
            "code number",
            "pf code number",
            "epf code",
            "epfo code",
        ],

        "branches": [
            "branches",
            "branch offices",
            "branch/unit",
            "branch or unit",
            "units",
        ],
    },

    # ===============================================================
    # Form 11
    # ===============================================================

    "FORM_11": {

        "employee_name": [
            "name of member",
            "member name",
            "employee name",
            "name of employee",
        ],

        "uan": [
            "uan",
            "universal account number",
            "uan number",
        ],

        "previous_uan": [
            "previous uan",
            "old uan",
            "earlier uan",
            "previous universal account number",
        ],

        "date_of_joining": [
            "date of joining",
            "joining date",
            "date of joining epf",
        ],

        "first_time_member": [
            "first time member",
            "first time epf member",
            "member of epf for first time",
        ],
    },

    # ===============================================================
    # UAN member data
    # ===============================================================

    "UAN_MEMBER_DATA": {

        "uan": [
            "uan",
            "uan number",
            "universal account number",
        ],

        "member_id": [
            "member id",
            "member account number",
            "pf member id",
            "member account",
        ],

        "employee_name": [
            "employee name",
            "member name",
            "name",
        ],

        "date_of_joining": [
            "date of joining",
            "joining date",
            "doj",
        ],

        "first_time_member": [
            "first time member",
            "first time epf member",
        ],

        "previous_uan": [
            "previous uan",
            "old uan",
            "previous universal account number",
        ],

        "establishment_code": [
            "establishment code",
            "epf establishment code",
            "pf code",
        ],
    },

    # ===============================================================
    # Member registration
    # ===============================================================

    "MEMBER_REGISTRATION": {

        "uan": [
            "uan",
            "universal account number",
        ],

        "member_id": [
            "member id",
            "pf member id",
            "member account",
        ],

        "employee_name": [
            "employee name",
            "member name",
            "name of member",
        ],

        "date_of_joining": [
            "date of joining",
            "joining date",
            "doj",
        ],

        "establishment_code": [
            "establishment code",
            "pf establishment code",
            "epfo establishment code",
        ],
    },

    # ===============================================================
    # ECR
    # ===============================================================

    "ECR_FILE": {

        "period": [
            "wage month",
            "wage month and year",
            "period",
            "contribution month",
            "return period",
        ],

        "establishment_code": [
            "establishment code",
            "pf establishment code",
            "epfo establishment code",
        ],

        "uan": [
            "uan",
            "uan number",
            "universal account number",
        ],

        "employee_name": [
            "member name",
            "employee name",
            "name",
        ],

        "wages": [
            "wages",
            "gross wages",
            "total wages",
        ],

        "epf_wages": [
            "epf wages",
            "epf wage",
            "pf wages",
        ],

        "eps_wages": [
            "eps wages",
            "eps wage",
        ],

        "edli_wages": [
            "edli wages",
            "edli wage",
        ],

        "employee_share": [
            "employee share",
            "employee contribution",
            "employee pf share",
        ],

        "employer_share": [
            "employer share",
            "employer contribution",
            "employer pf share",
        ],

        "ncp_days": [
            "ncp days",
            "non contributory period",
            "non-contributory days",
            "non contributory days",
        ],
    },

    # ===============================================================
    # ECR Return
    # ===============================================================

    "ECR_RETURN": {

        "period": [
            "period",
            "wage month",
            "return period",
        ],

        "establishment_code": [
            "establishment code",
            "epf code",
            "pf code",
        ],

        "uan": [
            "uan",
            "universal account number",
        ],

        "employee_name": [
            "member name",
            "employee name",
        ],

        "wages": [
            "wages",
            "gross wages",
        ],

        "epf_wages": [
            "epf wages",
        ],

        "eps_wages": [
            "eps wages",
        ],

        "edli_wages": [
            "edli wages",
        ],

        "employee_share": [
            "employee share",
            "employee contribution",
        ],

        "employer_share": [
            "employer share",
            "employer contribution",
        ],

        "ncp_days": [
            "ncp days",
            "non-contributory days",
        ],
    },

    # ===============================================================
    # ECR acknowledgement
    # ===============================================================

    "ECR_ACKNOWLEDGEMENT": {

        "period": [
            "period",
            "wage month",
            "return period",
        ],

        "establishment_code": [
            "establishment code",
            "epf code",
            "pf code",
        ],

        "trrn": [
            "trrn",
            "temporary return reference number",
            "return reference number",
        ],

        "acknowledgement_number": [
            "acknowledgement number",
            "acknowledgment number",
            "ack no",
            "acknowledgement no",
        ],

        "date": [
            "date",
            "submission date",
            "filing date",
        ],
    },

    # ===============================================================
    # Challan
    # ===============================================================

    "CHALLAN": {

        "trrn": [
            "trrn",
            "temporary return reference number",
            "trrn number",
        ],

        "establishment_code": [
            "establishment code",
            "epf establishment code",
            "pf code",
        ],

        "period": [
            "period",
            "wage month",
            "contribution period",
            "month",
        ],

        "challan_amount": [
            "challan amount",
            "total amount",
            "amount payable",
            "total contribution",
            "amount",
        ],

        "payment_date": [
            "payment date",
            "date of payment",
            "paid on",
        ],
    },

    # ===============================================================
    # Payment receipt
    # ===============================================================

    "PAYMENT_RECEIPT": {

        "trrn": [
            "trrn",
            "temporary return reference number",
            "payment reference number",
        ],

        "payment_date": [
            "payment date",
            "date of payment",
            "transaction date",
        ],

        "paid_amount": [
            "paid amount",
            "amount paid",
            "payment amount",
            "total amount paid",
        ],

        "transaction_reference": [
            "transaction reference",
            "transaction id",
            "transaction number",
            "payment reference",
        ],
    },

    # ===============================================================
    # TRRN
    # ===============================================================

    "TRRN_RECORD": {

        "trrn": [
            "trrn",
            "temporary return reference number",
        ],

        "period": [
            "period",
            "wage month",
            "contribution month",
        ],

        "establishment_code": [
            "establishment code",
            "pf establishment code",
        ],

        "amount": [
            "amount",
            "total amount",
            "challan amount",
        ],

        "payment_date": [
            "payment date",
            "date of payment",
        ],

        "status": [
            "status",
            "payment status",
            "transaction status",
        ],
    },
}


def get_field_mapping(
    document_type: str,
) -> Dict[str, List[str]]:
    """
    Return field aliases for a specific document type.
    """

    return FIELD_MAPPINGS.get(
        document_type,
        {},
    )


def get_field_aliases(
    document_type: str,
    field_name: str,
) -> List[str]:
    """
    Return aliases for a particular field.
    """

    mapping = get_field_mapping(
        document_type
    )

    return mapping.get(
        field_name,
        [],
    )


def get_all_document_fields(
    document_type: str,
) -> List[str]:
    """
    Return all canonical fields for a document type.
    """

    mapping = get_field_mapping(
        document_type
    )

    return list(
        mapping.keys()
    )


def find_canonical_field(
    document_type: str,
    extracted_label: str,
) -> str | None:
    """
    Map a raw extracted document label to its canonical field.

    Example:

        document_type = "FORM_5A"
        extracted_label = "PAN Number"

        returns:
            "pan"
    """

    mapping = get_field_mapping(
        document_type
    )

    normalized_label = (
        extracted_label
        or ""
    ).strip().casefold()

    for canonical_field, aliases in mapping.items():

        for alias in aliases:

            if normalized_label == (
                alias.casefold()
            ):
                return canonical_field

    return None