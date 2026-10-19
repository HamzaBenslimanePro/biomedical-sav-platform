"""Equipment generator.

Produces EquipmentRow instances conforming to
contracts/sap_export_schema.yml (table: equipment).

Design notes
------------
* Single seeded RNG → reproducibility. Same (seed, count, reference_date)
  produces byte-identical rows.
* IDs are prefixed by modality (EQ-MRI-0001) so the table is readable without
  a join. Per-modality counters make IDs stable across runs.
* Status is age-aware: assets younger than 1 year are never DECOMMISSIONED;
  assets older than 10 years are biased toward it (realistic fleet aging).
* Warranty = install_date + modality-specific months; always in the past for
  old assets, which the KPI layer uses later (out-of-warranty work orders).
"""

from __future__ import annotations
import random
from dataclasses import asdict, dataclass
from datetime import date, timedelta

from ingest.domain.catalogs import MODELS_BY_MODALITY, SITE_CATALOG, STATUSES
from ingest.domain.distributions import (
    INSTALL_AGE_WEIGHTS,
    MODALITY_WEIGHTS,
    STATUS_WEIGHTS,
    WARRANTY_MONTHS_BY_MODALITY,
)
from ingest.generators.base import weighted_choice


@dataclass(frozen=True)
class EquipmentRow:
    equipment_id: str
    modality: str
    model: str
    manufacturer: str
    install_date: date
    site_id: str
    warranty_end: date | None
    status: str

    def to_dict(self) -> dict:
        return asdict(self)


def generate_equipment(
    rng: random.Random,
    count: int,
    reference_date: date,
    sites: list[str] | None = None,
) -> list[EquipmentRow]:
    """Generate `count` equipment rows conforming to the equipment contract."""
    sites = sites or SITE_CATALOG
    counters: dict[str, int] = {m: 0 for m in MODELS_BY_MODALITY}
    rows: list[EquipmentRow] = []

    for _ in range(count):
        modality = weighted_choice(rng, MODALITY_WEIGHTS)
        manufacturer, model = _pick_model(rng, modality)
        install_date = _pick_install_date(rng, reference_date)
        status = _pick_status(rng, install_date, reference_date)

        counters[modality] += 1
        rows.append(EquipmentRow(
            equipment_id=f"EQ-{modality}-{counters[modality]:04d}",
            modality=modality,
            model=model,
            manufacturer=manufacturer,
            install_date=install_date,
            site_id=rng.choice(sites),
            warranty_end=_warranty_end(install_date, modality),
            status=status,
        ))
    return rows


# --- internal helpers -------------------------------------------------------

def _pick_model(rng: random.Random, modality: str) -> tuple[str, str]:
    catalog = MODELS_BY_MODALITY[modality]
    manufacturer = rng.choice(list(catalog.keys()))
    return manufacturer, rng.choice(catalog[manufacturer])


def _pick_install_date(rng: random.Random, reference_date: date) -> date:
    bucket = weighted_choice(rng, INSTALL_AGE_WEIGHTS)
    low, high = {
        "0-2": (0, 2),
        "3-5": (3, 5),
        "6-10": (6, 10),
        "11-15": (11, 15),
    }[bucket]
    years_ago = rng.randint(low, high)
    days_jitter = rng.randint(0, 364)  # avoid clustering on Jan 1
    return reference_date - timedelta(days=years_ago * 365 + days_jitter)


def _pick_status(rng: random.Random, install_date: date, reference_date: date) -> str:
    age_years = (reference_date - install_date).days / 365.25
    if age_years < 1:
        return weighted_choice(rng, {"OPERATIONAL": 95, "DEGRADED": 4, "DOWN": 1})
    if age_years > 10:
        return weighted_choice(rng, {
            "OPERATIONAL": 55, "DEGRADED": 15, "DOWN": 5, "DECOMMISSIONED": 25,
        })
    return weighted_choice(rng, STATUS_WEIGHTS)


def _warranty_end(install_date: date, modality: str) -> date | None:
    months = WARRANTY_MONTHS_BY_MODALITY.get(modality)
    if months is None:
        return None
    return install_date + timedelta(days=months * 30)  # approximate; fine for synthetic