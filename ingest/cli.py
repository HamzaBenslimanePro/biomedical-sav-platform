"""CLI entry point.

    python -m ingest generate --table equipment
    python -m ingest generate --table all

Each table gets its own derived RNG (`Random(f"{seed}:{table}")`) so changing
one table's config (e.g. equipment_count) does not shift another table's
output. This is a deliberate change from the earlier "single shared rng"
design — see ADR-0007 if you write it up.
"""

from __future__ import annotations
import argparse
import logging
import random

from ingest.config import GeneratorConfig
from ingest.generators.equipment import generate_equipment
from ingest.generators.failure_codes import load_failure_codes
from ingest.generators.technicians import generate_technicians
from ingest.generators.work_orders import generate_work_orders
from ingest.writer import write_parquet

log = logging.getLogger(__name__)


def _rng_for(seed: int, table: str) -> random.Random:
    return random.Random(f"{seed}:{table}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ingest")
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="Generate synthetic source tables.")
    gen.add_argument(
        "--table",
        choices=["equipment", "technicians", "failure_codes", "work_orders", "all"],
        required=True,
    )
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    args = _build_parser().parse_args()
    config = GeneratorConfig.from_env()

    equipment = technicians = None

    if args.table in ("equipment", "all"):
        rows = generate_equipment(
            _rng_for(config.seed, "equipment"),
            config.equipment_count,
            config.reference_date,
        )
        equipment = rows
        path = write_parquet(rows, "equipment", config.output_dir)
        log.info("equipment: wrote %d rows to %s", len(rows), path)

    if args.table in ("technicians", "all"):
        rows = generate_technicians(
            _rng_for(config.seed, "technicians"),
            config.technicians_count,
            config.reference_date,
        )
        technicians = rows
        path = write_parquet(rows, "technicians", config.output_dir)
        log.info("technicians: wrote %d rows to %s", len(rows), path)

    if args.table in ("failure_codes", "all"):
        rows = load_failure_codes()
        path = write_parquet(rows, "failure_codes", config.output_dir)
        log.info("failure_codes: wrote %d rows to %s", len(rows), path)

    if args.table in ("work_orders", "all"):
        if equipment is None:
            equipment = generate_equipment(
                _rng_for(config.seed, "equipment"),
                config.equipment_count,
                config.reference_date,
            )
        if technicians is None:
            technicians = generate_technicians(
                _rng_for(config.seed, "technicians"),
                config.technicians_count,
                config.reference_date,
            )
        rows = generate_work_orders(
            _rng_for(config.seed, "work_orders"),
            equipment,
            technicians,
            config.reference_date,
            config.data_start_date,
            config.data_end_date,
        )
        path = write_parquet(rows, "work_orders", config.output_dir)
        log.info("work_orders: wrote %d rows to %s", len(rows), path)


if __name__ == "__main__":
    main()