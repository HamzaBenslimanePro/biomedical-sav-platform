# Environment — Pinned Versions

> Rule: the AI must ask for these versions before proposing any config or API.
> Rule: after any `pip install`, update this file with the resolved version.
> Rule: versions must be reproducible — pin in `pyproject.toml` / `requirements.txt`.

| Tool | Version | Verified on | Notes |
|------|---------|-------------|-------|
| Python | 3.12.x | TBD | target local + CI |
| dbt-core | TBD | TBD | pin in requirements |
| dbt-duckdb | TBD | TBD | local adapter |
| dbt-snowflake | TBD (optional) | TBD | only if cloud target is Snowflake |
| DuckDB | TBD | TBD | local warehouse engine |
| Dagster | TBD | TBD | orchestration (see ADR-0001) |
| pandas | TBD | TBD | generator only — not for pipeline |
| Faker | TBD | TBD | synthetic data |
| pyarrow | TBD | TBD | Parquet |
| ruff | TBD | TBD | Python lint |
| sqlfluff | TBD | TBD | SQL lint |
| Great Expectations | optional | TBD | only if adopted (see DEBT.md D-003) |

## Local environment
- OS: macOS / Linux (fill in)
- Docker Desktop: TBD
- Make: GNU Make ≥ 3.82 (required by `.RECIPEPREFIX`)

## CI environment
- GitHub Actions runner: ubuntu-latest
- Python via actions/setup-python: 3.12
