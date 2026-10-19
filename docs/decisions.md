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

---

### ADR-0004: Containerization — deferred in P1
- Status: accepted
- Date: 2026-10-19
- Context: the local machine has 15GB of free storage. Docker Desktop + multi-service
  images (dbt, Dagster, Postgres) would consume ~5–7GB and grow with layer caching,
  leaving too little headroom for the data lake, dbt artifacts, and other projects.
  The P1 stack (DuckDB + dbt + Dagster + Python) runs natively without any server process.
- Decision: no Docker in P1. Reproducibility is provided by `make bootstrap` (venv +
  pinned `requirements.txt` + `dbt deps`) and `make run` (pipeline entrypoint).
  Containerization is deferred to P11 (Cloud Deployment Blueprint), where Docker is
  required anyway for the deployment target.
- Alternatives considered:
  - **Docker Desktop + compose** — reproducible and standard, but ~5–7GB of storage
    and a background VM. Incompatible with the 15GB budget alongside the rest of
    the portfolio.
  - **Podman** — lighter than Docker Desktop but still requires image storage; same
    storage math applies.
  - **Dev containers** — heavier, not viable here.
- Consequences:
  - (+) Fits the storage budget; faster iteration (no image rebuilds); simpler
    debugging (native processes, real venv, real `pdb`); no background daemon.
  - (−) The P0 rubric item "docker compose up reproduces the pipeline" is amended to
    "`make bootstrap && make run` reproduces the pipeline from a clean clone."
    Reproducibility relies on pinned requirements + Makefile instead of a container image.
  - Mitigation: include a short "Containerization plan" section in the README
    describing exactly what the `docker-compose.yml` would contain (services:
    dagster, dbt-runner, optionally Postgres) and why it was deferred. This turns a
    constraint into a documented decision — a stronger interview story than silently
    skipping Docker.

### ADR-0005: PM compliance metric definition
- Status: accepted
- Date: 2026-10-19
- Context: "PM compliance" has at least five common definitions (strict on-time,
  grace-window, completion-based, asset-level, work-month attribution). The KPI
  drives a maintenance manager's decisions, so a silent definition is a silent bug.
  The contract supports schedule-based measurement because PM work orders are
  created at schedule time with a nullable `closed_at`.
- Decision: PM compliance = PM work orders closed on or before `pm_due_date + 7
  days` (var `pm_grace_days`), with `pm_due_date` in the period, divided by PM
  work orders with `pm_due_date` in the period, excluding equipment decommissioned
  before period start. Attributed by due date. Event-level grain. A secondary
  `pm_completion_pct` (closed at all ÷ due) is reported alongside.
- Alternatives considered:
  - **Completion-based denominator** (PMs closed in period) — rejected: hides
    missed PMs, flatters the KPI, answers the wrong business question.
  - **Strict 0-day grace** — rejected: penalizes clinically-justified delays;
    sensitivity check shows it understates compliance by N points.
  - **Attribution by close date** — rejected: a January PM closed in February
    would credit February and hide January's failure.
  - **Asset-level granularity** — deferred: variant, not the P1 headline.
- Consequences:
  - (+) Answers the real business question (are we maintaining on schedule?);
    computable from the existing contract; parameterized so the definition is
    auditable and the sensitivity check is one command.
  - (−) Depends on the generator producing scheduled PMs with NULL `closed_at` —
    if it only generates completed work orders, the KPI is silently inflated.
    Mitigation: constraint stated in `docs/domain_glossary.md` and enforced by a
    dbt test (`DQ-COMPLETE-002`: PM rows with `pm_due_date` in the past must have
    non-NULL `closed_at` OR be classified `missed`).

### ADR-0006: MTBF metric definition
- Status: accepted
- Date: 2026-10-19
- Context: "MTBF" has multiple defensible definitions (fleet vs per-asset,
  start-to-start vs end-of-repair, CM-only vs all failure events, censoring
  handling). The glossary name is correct but leaves these decisions silent.
  MTBF is the primary reliability KPI alongside MTTR and PM compliance, and it
  depends on the work_orders generator producing enough CM events to compute
  intervals. Must be fixed before work_orders.py is written.
- Decision:
  - **Headline (fleet MTBF):** total asset-operating-hours in window ÷ total CM
    count in window. Operating hours = `min(decommission or reference, window_end)
    − max(install, window_start)`, in hours.
  - **Diagnostic (per-asset MTBF):** mean of `opened_at[i+1] − opened_at[i]`
    for consecutive CM events on the same asset, for assets with ≥2 CMs.
  - **Interval:** start-to-start (includes repair time; standard for repairable
    systems).
  - **Event types:** CM only. DOWN status events are excluded (they co-occur
    with a CM and would double-count).
  - **First failure:** excluded from MTBF (that is MTTF, a different metric).
  - **Censoring:** left (asset installed before window_start) and right (asset
    still running at reference_date) both handled via the operating-hours
    formula above.
- Alternatives considered:
  - **End-of-repair-to-start intervals** — rejected: answers "operational
    reliability excluding downtime," a different question; standard MTBF is
    start-to-start.
  - **Including first failure (install → first CM)** — rejected: this is MTTF,
    not MTBF; blending them produces a metric nobody recognizes.
  - **Per-asset-only reporting** — rejected: unweighted mean underweights
    high-exposure assets; fleet MTBF is the industry KPI.
  - **Excluding zero-failure assets from fleet denominator** — rejected: biases
    the KPI downward by ignoring reliable assets' exposure.
- Consequences:
  - (+) Fleet number matches what a maintenance manager would compute; censoring
    handled naturally by the operating-hours formula; per-asset number available
    for diagnostics.
  - (−) Generator must produce ≥2 CM events per asset for most assets, or
    per-asset MTBF is NaN-dominated. Mitigation: `CM_RATE_PER_ASSET_YEAR` in
    `domain/distributions.py`; Step 1 exit check = median asset has ≥3 CMs.
  - (−) Depends on `install_date < opened_at < closed_at` for every CM. Add
    invariant `INV-005: CM rows must satisfy install_date <= opened_at` to the
    contract's invariant list; enforce as a dbt test at Step 2.