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
- Status: accepted
- Date: 2026-10-19
- Context: local dev needs a fast, zero-ops, file-backed warehouse so `docker compose up` stays simple. The pipeline is analytical (columnar scans, aggregations over fact tables), not transactional.
- Decision: DuckDB locally; Snowflake or BigQuery in cloud. dbt adapter switch via profile.
- Alternatives considered:
  - **Postgres** — more "production-realistic" and closer to a traditional warehouse, but requires a running server, heavier Docker image, and OLTP-oriented storage that is suboptimal for large analytical scans.
  - **SQLite** — zero-ops and file-backed, but row-oriented (no columnar), no native Parquet, no analytical query pushdown. Wrong tool for the workload.
- Consequences:
  - (+) In-process, zero-ops, single file; columnar engine; native Parquet reads (no load step); fast on 50M+ rows locally; keeps `docker compose up` simple.
  - (−) SQL dialect differs from cloud targets (Snowflake/BigQuery), so dialect-specific bugs will not be caught locally.
  - Mitigation: document the DuckDB ↔ cloud dialect boundary in README; treat "cloud validation tier" as a future step; keep dbt models ANSI-leaning and avoid DuckDB-only functions in marts.

---

### ADR-0002: Orchestrator — Dagster vs Airflow
- Status: accepted
- Date: 2026-10-19
- Context: asset-oriented dbt orchestration, small team, local-first. The stack is dbt-centric; models are the primary unit of work and lineage.
- Decision: Dagster. Chosen for its asset-oriented model, first-class dbt integration (ingests `manifest.json` so each dbt model becomes a Dagster asset with native lineage), and a superior local development experience.
- Alternatives considered:
  - **Airflow** — larger ecosystem and more common in enterprise hiring, but task-centric (does not natively model dbt models as assets), heavier local setup, and a weaker dbt-native integration path.
  - **Make + cron** — rejected: not reproducible, not observable, no lineage, no retry/alerting primitives.
- Consequences:
  - (+) dbt models surface as Dagster assets with lineage in the UI; better local dev/test loop; asset-based mental model maps 1:1 to dbt's model graph; aligns with the project's "asset = data product" framing.
  - (−) Smaller hiring pool than Airflow; fewer tutorials for edge cases.
  - Mitigation: note in README that Airflow concepts map 1:1 (DAGs ≈ jobs, tasks ≈ ops, sensors ≈ schedules/asset checks) so the skill transfers; revisit if a role explicitly requires Airflow.

---

### ADR-0003: Data quality — dbt tests vs Great Expectations
- Status: accepted
- Date: 2026-10-19
- Context: need row-level, column-level, and freshness checks. The project is dbt-centric; minimizing tool sprawl and configuration surface is a stated goal for P1.
- Decision: dbt tests + `dbt source freshness` for P1; defer Great Expectations to P4 (where distributional checks and ML feature validation become relevant).
- Alternatives considered:
  - **Great Expectations (GX)** — more expressive (distributional expectations, data docs, checkpoint framework), but adds a second tool, a separate configuration surface, and a heavier operational footprint. Overkill for P1 scope.
  - **dbt-expectations package** — a middle ground that brings GE-style assertions into dbt; not adopted in P1 to keep the dependency footprint minimal, but flagged as a cheap upgrade path if needed.
- Consequences:
  - (+) One tool, one mental model; tests live in YAML next to models; run inside `dbt build` (single command, single failure surface); zero extra infra.
  - (−) Less expressive than GX for distributional/statistical checks.
  - Mitigation: `dbt-expectations` can be added without changing the mental model; GX adoption is parked in DEBT D-003 and revisited in P4 where its power is justified.