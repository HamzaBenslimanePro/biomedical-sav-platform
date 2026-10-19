"""Technician (field service engineer) generator.

Synthesized dimension: names, hire dates, skills are invented because no real
hospital roster exists. This is why `rng` is required — contrast with
`failure_codes.py`, whose contents are given by domain knowledge.

Faker is seeded from the passed rng so it stays reproducible under the same
(parent) seed. Faker's seed_instance is instance-scoped — we don't mutate the
global Faker state.
"""

from __future__ import annotations
import random
from dataclasses import asdict, dataclass
from datetime import date, timedelta

from faker import Faker

from ingest.domain.catalogs import SITE_CATALOG, SKILL_LEVELS
from ingest.domain.distributions import HIRE_YEAR_WEIGHTS, SKILL_WEIGHTS
from ingest.generators.base import weighted_choice


@dataclass(frozen=True)
class TechnicianRow:
    technician_id: str
    full_name: str
    skill_level: str
    region: str
    hire_date: date

    def to_dict(self) -> dict:
        return asdict(self)


def generate_technicians(
    rng: random.Random,
    count: int,
    reference_date: date,
    regions: list[str] | None = None,
) -> list[TechnicianRow]:
    """Generate `count` technician rows conforming to the technicians contract."""
    regions = regions or SITE_CATALOG
    fake = Faker("fr_FR")
    fake.seed_instance(rng.randint(0, 2**31 - 1))
    rows: list[TechnicianRow] = []

    for i in range(1, count + 1):
        rows.append(TechnicianRow(
            technician_id=f"TECH-{i:04d}",
            full_name=fake.name(),
            skill_level=weighted_choice(rng, SKILL_WEIGHTS),
            region=rng.choice(regions),
            hire_date=_pick_hire_date(rng, reference_date),
        ))
    return rows


def _pick_hire_date(rng: random.Random, reference_date: date) -> date:
    bucket = weighted_choice(rng, HIRE_YEAR_WEIGHTS)
    low, high = {"0-2": (0, 2), "3-5": (3, 5), "6-10": (6, 10), "11-15": (11, 15)}[bucket]
    years_ago = rng.randint(low, high)
    days_jitter = rng.randint(0, 364)
    return reference_date - timedelta(days=years_ago * 365 + days_jitter)