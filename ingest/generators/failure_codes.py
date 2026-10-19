"""Failure code reference table generator.

Unlike the other generators, this is a static catalog — no randomness. The
function takes no `rng` parameter for that reason; the CLI handles it
separately. Adding `rng` and ignoring it would be misleading.
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


def generate_failure_codes() -> list[FailureCodeRow]:
    """Return the full static failure-code reference table."""
    return [FailureCodeRow(**row) for row in FAILURE_CODES]