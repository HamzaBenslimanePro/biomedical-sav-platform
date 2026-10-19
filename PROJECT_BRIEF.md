# Project Brief — Biomedical SAV Data Platform (P1)

## Problem
The SAV KPI dashboard built during a Siemens Healthineers internship was ad-hoc:
manual SAP exports → Excel → Snowflake → Power BI. It was neither versioned, nor
tested, nor reproducible. This project replaces it with a production-grade ELT
platform that is orchestrated, tested, documented, and defendable in an interview.

## Objective
Build an ELT platform over synthetic SAP-style biomedical service data that:
- ingests equipment, work orders, technicians, and failure codes;
- lands raw data in Parquet (partitioned);
- transforms via dbt (staging → intermediate → marts);
- orchestrates the full DAG;
- enforces data quality gates (tests + source freshness);
- exposes SAV KPIs (MTTR, MTBF, PM compliance, cost per intervention) via a dashboard.

## In Scope
- Python ingestion generator (deterministic, realistic SAV distributions).
- Parquet lake partitioned by date / modality.
- dbt project with 8–12 layered models, tests, and documentation.
- Orchestration with Dagster OR Airflow (pick one, justify in ADR).
- Local Docker Compose stack (orchestrator + warehouse + dbt runner).
- GitHub Actions CI running dbt build on PRs.
- One BI dashboard (Metabase / Streamlit / Power BI).
- Data contract for the SAP export, validated at ingestion.

## Out of Scope (park in DEBT.md)
- Streaming ingestion (that is P2).
- Kubernetes deployment (that is P11).
- A second warehouse (Snowflake AND BigQuery).
- Real SAP connectivity. Data is synthetic by design.
- Authentication / multi-tenancy.

## Deliverables Rubric

### P0 — Non-negotiable foundation
- [ ] Public GitHub repo, clean commit history.
- [ ] README: problem, architecture diagram, how to run, decisions, limitations.
- [ ] `docker compose up` reproduces the full pipeline from a clean state.
- [ ] 8–12 dbt models following staging → intermediate → marts.
- [ ] Generic tests (unique, not_null) + custom tests on every layer.
- [ ] Orchestrated DAG that runs ingest → transform → tests → dashboard refresh.
- [ ] Evidence the pipeline catches bad data (screenshot of a failing run).

### P1 — "Hire me" signals
- [ ] At least one incremental fact model using unique_key + is_incremental() filter.
- [ ] Documented, idempotent backfill command that does not duplicate rows.
- [ ] Source freshness check configured and failing loudly on stale SAP data.
- [ ] GitHub Actions CI: lint + `dbt build` on every PR; broken model fails CI.

### P2 — Differentiators
- [ ] `contracts/sap_export_schema.yml` validated at ingestion.
- [ ] `dbt docs generate` produces a usable lineage + glossary site.
- [ ] `docs/decisions.md` ADR log with at least 5 entries.

## Build Steps and Exit Criteria

Step 1 — Scaffold and simulate (Days 1–2)
  Build: repo tree, synthetic data generator with realistic distributions.
  Exit: rerunnable generator, no crashes, counts match expected ranges.

Step 2 — ELT skeleton (Days 3–5)
  Build: ingest to Parquet; dbt init; stg_ models; one fct_ model.
  Exit: `dbt build` succeeds, table queryable in DuckDB.

Step 3 — Incremental logic + tests (Days 6–8)
  Build: incremental fct_ with unique_key; generic + custom tests.
  Exit: double-run does not duplicate rows; breaking a source file fails a test.

Step 4 — Orchestration + Docker (Days 9–11)
  Build: Dagster job (or Airflow DAG); Dockerfile; docker-compose.yml.
  Exit: `docker compose up` runs the full pipeline from clean; UI shows green run.

Step 5 — Quality gates + CI (Days 12–13)
  Build: source freshness or Great Expectations checkpoint in DAG; GitHub Actions.
  Exit: broken model fails CI; DAG blocks dashboard on quality failure.

Step 6 — Dashboard + docs (Days 14–15)
  Build: BI dashboard over marts (3–4 charts); dbt docs; README; demo video.
  Exit: live dashboard, docs generated, 2-minute recorded demo exists.

## Definition of Done
The repo is publishable only when: P0 items all checked; at least 3 P1 items checked;
README allows a stranger to reproduce the stack; and I can pass a 10-question
interview-style quiz on this repo (see AGENTS.md, QUIZ mode).
