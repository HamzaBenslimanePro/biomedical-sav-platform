"""CLI entry point.

    python -m ingest generate --table equipment
    python -m ingest generate --table all
"""

from __future__ import annotations
import argparse
import logging
import random

from ingest.config import GeneratorConfig
from ingest.generators.equipment import generate_equipment
from ingest.generators.failure_codes import generate_failure_codes
from ingest.writer import write_parquet

log = logging.getLogger(__name__)


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
    rng = random.Random(config.seed)  # single shared RNG → reproducible across tables

    if args.table in ("equipment", "all"):
        rows = generate_equipment(rng, config.equipment_count, config.reference_date)
        path = write_parquet(rows, "equipment", config.output_dir)
        log.info("equipment: wrote %d rows to %s", len(rows), path)

    if args.table in ("failure_codes", "all"):
        rows = generate_failure_codes()
        path = write_parquet(rows, "failure_codes", config.output_dir)
        log.info("failure_codes: wrote %d rows to %s", len(rows), path)

    if args.table in ("technicians", "work_orders"):
        raise NotImplementedError(f"{args.table} generator not implemented yet")


if __name__ == "__main__":
    main()