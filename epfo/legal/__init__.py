"""
EPFO legal source and provenance package.

This package provides:
- Authoritative EPFO legal/reference sources
- Source metadata
- Rule-to-source mapping
- Legal provenance lookup
- Manifest validation
"""

from .sources import (
    LegalSource,
    LEGAL_SOURCES,
    RULE_SOURCE_MAP,
    get_source,
    get_sources,
    get_sources_for_rule,
    get_primary_source_for_rule,
    validate_source_manifest,
)

__all__ = [
    "LegalSource",
    "LEGAL_SOURCES",
    "RULE_SOURCE_MAP",
    "get_source",
    "get_sources",
    "get_sources_for_rule",
    "get_primary_source_for_rule",
    "validate_source_manifest",
]