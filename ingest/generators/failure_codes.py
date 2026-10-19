# ingest/generators/failure_codes.py
"""Failure code reference table loader.

This is a DIMENSION table whose contents are GIVEN by domain knowledge, not
synthesized. There is no `rng` parameter because there is nothing to sample:
the catalog IS the data. Randomness enters only in `work_orders.py`, where each
CM event samples a valid code from `FAILURE_CODES_BY_MODALITY[modality]`.

Contrast with `equipment.py` and `technicians.py`, which DO take `rng` because
their population (which units exist, which people work here) must be invented.
"""

from __future__ import annotations
from dataclasses import asdict, dataclass

from ingest.domain.failure_catalog import FAILURE_CODES


@dataclass(frozen=True)
class FailureCodeRow:
    failure_code: str
    label: str
    subsystem: str
    severity: str

    def to_dict(self) -> dict:
        return asdict(self)


def load_failure_codes() -> list[FailureCodeRow]:
    """Return the full failure-code reference table. Deterministic."""
    return [FailureCodeRow(**row) for row in FAILURE_CODES]