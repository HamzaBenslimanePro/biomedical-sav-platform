# Technical Debt / Scope-Creep Parking Lot

> Ideas that are worth doing LATER, not NOW. Anything added here must name the
> project that will absorb it. Do not touch these during P1.

| ID | Idea | Why parked | Target project | Date parked |
|----|------|-----------|----------------|-------------|
| D-001 | Kafka streaming for equipment telemetry | Out of P1 scope | P2 | — |
| D-002 | Kubernetes deployment | Out of P1 scope | P11 | — |
| D-003 | Great Expectations full integration | dbt tests cover P1 | P4 | — |
| D-004 | Multi-warehouse support (Snowflake + BigQuery) | Pick one | P12 | — |
| D-005 | dbt-expectations advanced suite | After P0 done | P3 | — |

## Rules
- Adding here is free. Removing requires a written reason in `docs/decisions.md`.
- If a debt item becomes urgent, it means the project scope was wrong — check
  PROJECT_BRIEF.md before acting.
