"""Tests for the failure code reference table."""

from __future__ import annotations

from ingest.domain.catalogs import MODALITIES
from ingest.domain.failure_catalog import FAILURE_CODES, FAILURE_CODES_BY_MODALITY
from ingest.generators.failure_codes import load_failure_codes

ALLOWED_SEVERITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_count_matches_catalog():
    assert len(load_failure_codes()) == len(FAILURE_CODES)


def test_codes_unique():
    codes = [r.failure_code for r in load_failure_codes()]
    assert len(set(codes)) == len(codes)


def test_severity_in_allowed_set():
    assert {r.severity for r in load_failure_codes()} <= ALLOWED_SEVERITIES


def test_all_modalities_have_codes():
    for modality in MODALITIES:
        assert FAILURE_CODES_BY_MODALITY.get(modality), f"{modality} has no codes"


def test_modality_mapping_references_known_codes():
    known = {r["failure_code"] for r in FAILURE_CODES}
    for modality, codes in FAILURE_CODES_BY_MODALITY.items():
        unknown = set(codes) - known
        assert not unknown, f"{modality} references unknown codes: {unknown}"


def test_no_orphan_codes():
    """Every code in the reference table is used by at least one modality."""
    known = {r["failure_code"] for r in FAILURE_CODES}
    used = set().union(*FAILURE_CODES_BY_MODALITY.values())
    assert known == used, f"Orphan codes: {known - used}"