from __future__ import annotations
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class GeneratorConfig:
    seed: int = 42
    output_dir: Path = Path("data/raw")
    reference_date: date = date(2026, 10, 19)
    data_start_date: date = date(2023, 1, 1)
    data_end_date: date = date(2025, 12, 31)
    equipment_count: int = 500
    sites_count: int = 8

    @classmethod
    def from_env(cls) -> "GeneratorConfig":
        return cls(
            seed=int(os.getenv("DATA_SEED", "42")),
            output_dir=Path(os.getenv("DATA_OUTPUT_DIR", "data/raw")),
            reference_date=_parse_date(os.getenv("REFERENCE_DATE", "2026-10-19")),
            data_start_date=_parse_date(os.getenv("DATA_START_DATE", "2023-01-01")),
            data_end_date=_parse_date(os.getenv("DATA_END_DATE", "2025-12-31")),
            equipment_count=int(os.getenv("EQUIPMENT_COUNT", "500")),
            sites_count=int(os.getenv("SITES_COUNT", "8")),
        )


def _parse_date(value: str) -> date:
    from datetime import datetime
    return datetime.strptime(value, "%Y-%m-%d").date()