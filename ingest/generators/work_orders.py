"""Work order generator — PM and CM events for every asset.

Design references:
- ADR-0005 (PM compliance): PM work orders are created at schedule time, with
  `pm_due_date` set and `closed_at` nullable. Missed PMs are rows where
  `pm_due_date` is in the past and `closed_at IS NULL`.
- ADR-0006 (MTBF): CM events follow a Poisson process per asset with rate
  `CM_RATE_PER_ASSET_YEAR[age_bucket]`. Sorted failure code list ensures
  index-to-code mapping is deterministic (see ADR-0007 below).

Reproducibility caveat (this is the "check question" answer): adding a new
failure code to `FAILURE_CODES_BY_MODALITY[modality]` changes which code the
same RNG index picks. That's intentional — the catalog IS the data. If you
change the catalog, bump DATA_SEED or accept the churn. The sorted() call
below makes the mapping stable across Python versions (no dict-order drift).
"""

from __future__ import annotations
import random
from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timedelta

from ingest.domain.catalogs import MODALITIES, MODELS_BY_MODALITY  # noqa: F401 (type check)
from ingest.domain.distributions import (
    CM_RATE_PER_ASSET_YEAR,
    PM_OUTCOMES,
    PM_RATE_PER_ASSET_YEAR,
)
from ingest.domain.failure_catalog import FAILURE_CODES_BY_MODALITY
from ingest.generators.base import weighted_choice
from ingest.generators.equipment import EquipmentRow
from ingest.generators.technicians import TechnicianRow


@dataclass(frozen=True)
class WorkOrderRow:
    work_order_id: str
    equipment_id: str
    technician_id: str
    wo_type: str            # PM | CM
    opened_at: datetime
    closed_at: datetime | None
    failure_code: str | None
    pm_due_date: date | None
    parts_cost_eur: float | None
    labor_hours: float | None
    resolution_notes: str | None

    def to_dict(self) -> dict:
        return asdict(self)


def generate_work_orders(
    rng: random.Random,
    equipment: list[EquipmentRow],
    technicians: list[TechnicianRow],
    reference_date: date,
    data_start_date: date,
    data_end_date: date,
) -> list[WorkOrderRow]:
    """Generate all PM + CM work orders in the observation window."""
    obs_end_global = min(data_end_date, reference_date)
    rows: list[WorkOrderRow] = []
    counter = 0

    for asset in equipment:
        obs_start = max(asset.install_date, data_start_date)
        obs_end = obs_end_global

        # Approximate decommissioning: stop observation 90-180 days early.
        # (P1 simplification — no decommission date field in contract. See DEBT.)
        if asset.status == "DECOMMISSIONED":
            obs_end -= timedelta(days=rng.randint(90, 180))

        if obs_start >= obs_end:
            continue

        for wo in _generate_cm_events(rng, asset, obs_start, obs_end, technicians):
            counter += 1
            wo["work_order_id"] = f"WO-{counter:07d}"
            rows.append(WorkOrderRow(**wo))

        for wo in _generate_pm_events(rng, asset, obs_start, obs_end, technicians):
            counter += 1
            wo["work_order_id"] = f"WO-{counter:07d}"
            rows.append(WorkOrderRow(**wo))

    return rows


# --- CM generation (ADR-0006) -------------------------------------------

def _generate_cm_events(
    rng: random.Random,
    asset: EquipmentRow,
    obs_start: date,
    obs_end: date,
    technicians: list[TechnicianRow],
) -> list[dict]:
    bucket = _age_bucket(asset.install_date, obs_start)
    rate = CM_RATE_PER_ASSET_YEAR[bucket]
    mean_interval_days = 365.0 / rate

    codes = sorted(FAILURE_CODES_BY_MODALITY[asset.modality])  # deterministic index → code

    events: list[dict] = []
    current = obs_start + timedelta(days=rng.expovariate(1.0 / mean_interval_days))

    while current <= obs_end:
        tech = rng.choice(technicians)
        repair_hours = min(rng.expovariate(1.0 / 12.0), 72.0)  # mean 12h, cap 72h

        opened = datetime.combine(current, time(hour=rng.randint(6, 20)))
        closed = opened + timedelta(hours=repair_hours)
        still_open = closed.date() > obs_end
        if still_open:
            closed = None

        events.append({
            "equipment_id": asset.equipment_id,
            "technician_id": tech.technician_id,
            "wo_type": "CM",
            "opened_at": opened,
            "closed_at": closed,
            "failure_code": rng.choice(codes),
            "pm_due_date": None,
            "parts_cost_eur": round(rng.uniform(0, 3000), 2) if closed else None,
            "labor_hours": round(repair_hours, 1) if closed else None,
            "resolution_notes": "Repaired" if closed else "Open at observation end",
        })
        current += timedelta(days=rng.expovariate(1.0 / mean_interval_days))

    return events


# --- PM generation (ADR-0005) -------------------------------------------

def _generate_pm_events(
    rng: random.Random,
    asset: EquipmentRow,
    obs_start: date,
    obs_end: date,
    technicians: list[TechnicianRow],
) -> list[dict]:
    rate = PM_RATE_PER_ASSET_YEAR[asset.modality]
    interval_days = 365.0 / rate

    events: list[dict] = []
    # Anchor PM schedule to install_date, not obs_start, so cadence is stable.
    pm_due = asset.install_date + timedelta(days=interval_days)

    while pm_due <= obs_end:
        if pm_due < obs_start:
            pm_due += timedelta(days=interval_days)
            continue

        outcome = weighted_choice(rng, PM_OUTCOMES)
        tech = rng.choice(technicians)

        if outcome == "missed":
            opened = datetime.combine(pm_due - timedelta(days=7), time(hour=8))
            closed = None
            parts = labor = None
            notes = "MISSED — PM not performed"
        elif outcome == "on_time":
            opened = datetime.combine(pm_due, time(hour=rng.randint(7, 10)))
            duration = rng.uniform(1.0, 4.0)
            closed = opened + timedelta(hours=duration)
            parts = round(rng.uniform(50, 500), 2)
            labor = round(duration, 1)
            notes = None
        else:  # late
            delay_days = rng.randint(8, 30)
            opened = datetime.combine(pm_due + timedelta(days=delay_days), time(hour=rng.randint(7, 10)))
            duration = rng.uniform(1.0, 4.0)
            closed = opened + timedelta(hours=duration)
            parts = round(rng.uniform(50, 500), 2)
            labor = round(duration, 1)
            notes = f"Performed {delay_days}d late"

        events.append({
            "equipment_id": asset.equipment_id,
            "technician_id": tech.technician_id,
            "wo_type": "PM",
            "opened_at": opened,
            "closed_at": closed,
            "failure_code": None,
            "pm_due_date": pm_due,
            "parts_cost_eur": parts,
            "labor_hours": labor,
            "resolution_notes": notes,
        })
        pm_due += timedelta(days=interval_days)

    return events


# --- helpers ------------------------------------------------------------

def _age_bucket(install_date: date, as_of: date) -> str:
    years = (as_of - install_date).days / 365.25
    if years < 3:
        return "young"
    if years <= 10:
        return "mid"
    return "old"