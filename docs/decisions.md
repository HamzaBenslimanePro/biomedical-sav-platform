# Architecture Decision Records (ADR)

> One entry per significant decision. Append-only. Superseding requires a new ADR.

## Template

    ### ADR-XXXX: <title>
    - Status: proposed | accepted | superseded by ADR-YYYY | rejected
    - Date: YYYY-MM-DD
    - Context: <what forced the decision>
    - Decision: <what we chose>
    - Alternatives considered: <...>
    - Consequences: <what becomes easier, what becomes harder>

---

### ADR-0001: Local warehouse choice — DuckDB vs Postgres
- Status: proposed
- Date: TBD
- Context: local dev needs a fast, zero-ops, file-backed warehouse so `docker compose up` stays simple.
- Decision: DuckDB locally; Snowflake or BigQuery in cloud. dbt adapter switch via profile.
- Alternatives considered: Postgres (more realistic but heavier), SQLite (no columnar).
- Consequences: (+) fast, zero-ops, single file. (−) SQL dialect differences when moving to cloud; must document the switch in README.

### ADR-0002: Orchestrator — Dagster vs Airflow
- Status: proposed
- Date: TBD
- Context: asset-oriented dbt orchestration, small team, local-first.
- Decision: TBD — evaluate both against a minimal DAG, then commit.
- Alternatives considered: Make + cron (rejected: not reproducible / not observable).
- Consequences: TBD.

### ADR-0003: Data quality — dbt tests vs Great Expectations
- Status: proposed
- Date: TBD
- Context: need row-level, column-level, and freshness checks.
- Decision: dbt tests + dbt source freshness for P1; defer Great Expectations to P4.
- Consequences: (+) one tool, one mental model. (−) less expressive than GE for distributional checks — parked in DEBT D-003.
