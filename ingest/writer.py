from __future__ import annotations
from dataclasses import asdict, is_dataclass
from pathlib import Path

import pyarrow as pa  # type: ignore
import pyarrow.parquet as pq # type: ignore


def write_parquet(rows: list, table_name: str, output_dir: Path) -> Path:
    """Write rows to Parquet. P1: one file per table (partitioning lands at Step 2)."""
    output_dir = Path(output_dir) / table_name
    output_dir.mkdir(parents=True, exist_ok=True)

    records = [_row_to_dict(r) for r in rows]
    pq.write_table(pa.Table.from_pylist(records), output_dir / f"{table_name}.parquet")
    return output_dir / f"{table_name}.parquet"


def _row_to_dict(row) -> dict:
    if hasattr(row, "to_dict"):
        return row.to_dict()
    if is_dataclass(row):
        return asdict(row)
    return dict(row)