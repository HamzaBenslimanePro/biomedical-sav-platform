from __future__ import annotations
import random
from datetime import date

import pytest # type: ignore

from ingest.domain.catalogs import MODALITIES, STATUSES
from ingest.generators.equipment import EquipmentRow, generate_equipment

REF = date(2026, 10, 19)


@pytest.fixture
def rows() -> list[EquipmentRow]:
    return generate_equipment(random.Random(42), 200, REF)


def test_count(rows):
    assert len(rows) == 200


def test_ids_unique(rows):
    assert len({r.equipment_id for r in rows}) == len(rows)


def test_modality_in_allowed_set(rows):
    assert {r.modality for r in rows} <= set(MODALITIES)


def test_status_in_allowed_set(rows):
    assert {r.status for r in rows} <= set(STATUSES)


def test_install_before_reference(rows):
    assert all(r.install_date < REF for r in rows)


def test_reproducible_with_same_seed():
    a = generate_equipment(random.Random(42), 50, REF)
    b = generate_equipment(random.Random(42), 50, REF)
    assert a == b


def test_young_assets_not_decommissioned():
    for r in generate_equipment(random.Random(1), 500, REF):
        if (REF - r.install_date).days / 365.25 < 1:
            assert r.status != "DECOMMISSIONED"