# ingest/

Synthetic data generator for P1. Produces the four source tables defined in
`contracts/sap_export_schema.yml`.

## Usage

    source .venv/bin/activate
    python -m ingest generate --table equipment

Output: `data/raw/equipment/equipment.parquet` (overwritten each run).

## Reproducibility

The `DATA_SEED` env var (default 42) seeds a single `random.Random` shared
across all generators, so reruns produce byte-identical output. Changing
`DATA_SEED` changes the data; the tests use a fixed seed and will fail if the
generation logic changes in a way that alters output.

## Status

- [x] equipment
- [ ] technicians
- [ ] failure_codes
- [ ] work_orders (requires the three above)