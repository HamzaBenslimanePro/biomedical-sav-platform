from __future__ import annotations
import random
from datetime import date

import pytest

from ingest.domain.catalogs import SKILL_LEVELS
from ingest.generators.technicians import TechnicianRow, generate_technicians

REF = date(2026, 10, 19)


@pytest.fixture
def rows() -> list[TechnicianRow]:
    return generate_technicians(random.Random(42), 50, REF)


def test_count(rows):
    assert len(rows) == 50


def test_ids_unique(rows):
    assert len({r.technician_id for r in rows}) == len(rows)


def test_skill_level_in_allowed_set(rows):
    assert {r.skill_level for r in rows} <= set(SKILL_LEVELS)


def test_hire_before_reference(rows):
    assert all(r.hire_date < REF for r in rows)


def test_reproducible():
    a = generate_technicians(random.Random(42), 20, REF)
    b = generate_technicians(random.Random(42), 20, REF)
    assert a == b