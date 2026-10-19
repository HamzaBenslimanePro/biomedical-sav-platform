# Biomedical SAV Data Platform

> Production-grade ELT platform for biomedical equipment service (SAV) data:
> ingest → Parquet lake → dbt → warehouse → dashboard, orchestrated and tested.

**Status:** 🚧 In construction — Step 1 of 6.

## Problem
Ad-hoc SAP → Excel → Snowflake → Power BI pipelines are unversioned, untested,
and unreproducible. This project rebuilds the SAV KPI stack as an engineered
platform with data contracts, incremental models, orchestration, and CI.

## Architecture
(placeholder — Mermaid or diagrams.net image goes here)

    SAP-like CSVs
        │
        ▼
    Python ingestion ──► Parquet lake (partitioned by date/modality)
                              │
                              ▼
                         dbt (stg → int → marts)
                              │
                              ▼
                    Warehouse (DuckDB / Snowflake)
                              │
                              ▼
                     BI dashboard (Metabase)

## Stack
| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| Storage | Parquet |
| Transform | dbt-core + dbt-duckdb |
| Warehouse | DuckDB (local) / Snowflake or BigQuery (cloud) |
| Orchestration | Dagster (or Airflow — see ADR-0001) |
| Quality | dbt tests + source freshness |
| CI | GitHub Actions |
| BI | Metabase / Streamlit |

## How to Run
(TBD — filled in at Step 4)

    docker compose up -d
    dbt build

## Results
(TBD — screenshots, dashboard link, test log snippet at Step 6)

## Key Decisions
See `docs/decisions.md` for the ADR log.

## Data Quality
See `docs/data_quality_rules.md`.

## Limitations and Next Steps
- Synthetic data only (no real SAP connectivity by design).
- Streaming ingestion deferred to project P2.
- Kubernetes deployment deferred to project P11.
