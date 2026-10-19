# Environment — Pinned Versions

> Rule: the AI must ask for these versions before proposing any config or API.
> Rule: after any `pip install`, update this file with the resolved version.
> Rule: versions must be reproducible — pin in `pyproject.toml` / `requirements.txt`.

| Tool | Version | Verified on | Notes |
|------|---------|-------------|-------|
| Python | 3.12.4 | 2026-10-19 | target local + CI |
| dbt-core | 1.12.6 | 2026-10-19 | pinned in requirements.txt |
| dbt-duckdb | 1.11.0 | 2026-10-19 | local adapter |
| dbt-snowflake | TBD (optional) | TBD | only if cloud target is Snowflake |
| DuckDB | 1.5.6 | 2026-10-19 | local warehouse engine |
| Dagster | 1.13.26 | 2026-10-19 | orchestration (see ADR-0001) |
| pandas | 2.2.2 | 2026-10-19 | generator only — not for pipeline |
| Faker | 40.43.0 | 2026-10-19 | synthetic data |
| pyarrow | 24.0.0 | 2026-10-19 | Parquet |
| ruff | 0.17.1 | 2026-10-19 | Python lint |
| sqlfluff | 4.4.0 | 2026-10-19 | SQL lint |
| Great Expectations | optional | TBD | only if adopted (see DEBT.md D-003) |

## Local environment
- OS: Windows
- Make: GNU Make ≥ 3.82 (required by `.RECIPEPREFIX`)

## CI environment
- GitHub Actions runner: ubuntu-latest
- Python : Python 3.12.4

## Defered:
- containerization: N/A (see ADR-0004)