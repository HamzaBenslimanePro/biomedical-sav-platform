from __future__ import annotations
import random
from collections import Counter
from datetime import date

import pytest

from ingest.domain.failure_catalog import FAILURE_CODES_BY_MODALITY
from ingest.generators.equipment import generate_equipment
from ingest.generators.technicians import generate_technicians
from ingest.generators.work_orders import generate_work_orders

REF = date(2026, 10, 19)
START = date(2023, 1, 1)
END = date(2025, 12, 31)


@pytest.fixture(scope="module")
def world():
    rng_eq = random.Random("42:equipment")
    rng_tc = random.Random("42:technicians")
    rng_wo = random.Random("42:work_orders")
    equipment = generate_equipment(rng_eq, 100, REF)
    technicians = generate_technicians(rng_tc, 30, REF)
    work_orders = generate_work_orders(rng_wo, equipment, technicians, REF, START, END)
    return equipment, technicians, work_orders


def test_rows_generated(world):
    _, _, work_orders = world
    assert len(work_orders) > 0


def test_ids_unique(world):
    _, _, work_orders = world
    ids = [wo.work_order_id for wo in work_orders]
    assert len(set(ids)) == len(ids)


def test_pm_has_no_failure_code(world):
    _, _, work_orders = world
    for wo in work_orders:
        if wo.wo_type == "PM":
            assert wo.failure_code is None
            assert wo.pm_due_date is not None


def test_cm_has_failure_code(world):
    _, _, work_orders = world
    for wo in work_orders:
        if wo.wo_type == "CM":
            assert wo.failure_code is not None
            assert wo.pm_due_date is None


def test_failure_code_matches_modality(world):
    equipment, _, work_orders = world
    eq_modality = {e.equipment_id: e.modality for e in equipment}
    for wo in work_orders:
        if wo.wo_type == "CM":
            allowed = FAILURE_CODES_BY_MODALITY[eq_modality[wo.equipment_id]]
            assert wo.failure_code in allowed


def test_closed_after_opened(world):
    _, _, work_orders = world
    for wo in work_orders:
        if wo.closed_at is not None:
            assert wo.closed_at >= wo.opened_at


def test_reproducible():
    rng_eq = random.Random("42:equipment")
    rng_tc = random.Random("42:technicians")
    equipment = generate_equipment(rng_eq, 30, REF)
    technicians = generate_technicians(rng_tc, 10, REF)
    a = generate_work_orders(random.Random("42:work_orders"), equipment, technicians, REF, START, END)
    b = generate_work_orders(random.Random("42:work_orders"), equipment, technicians, REF, START, END)
    assert a == b


def test_mtbf_sanity_median_asset_has_multiple_cms(world):
    """ADR-0006 exit check: median asset should have >= 3 CMs."""
    _, _, work_orders = world
    cm_per_asset = Counter(wo.equipment_id for wo in work_orders if wo.wo_type == "CM")
    counts = sorted(cm_per_asset.values())
    median = counts[len(counts) // 2]
    assert median >= 3, f"median CM count per asset is {median}; bump CM_RATE_PER_ASSET_YEAR"