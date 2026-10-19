# Data Quality Rulebook

> Every rule has: an ID, the layer it runs at, the expectation, and the action on
> failure. A rule that cannot fail is not a rule — test it by breaking the data.

## Rule ID format
`DQ-<DOMAIN>-<NNN>` where DOMAIN ∈ {SCHEMA, COMPLETE, UNIQUE, RELATION, RANGE, FRESH, BUSINESS}.

## Rules

| ID | Layer | Expectation | Action | Implemented |
|----|-------|-------------|--------|-------------|
| DQ-SCHEMA-001 | ingestion | Raw export matches `contracts/sap_export_schema.yml` | fail pipeline | ☐ |
| DQ-COMPLETE-001 | staging | `work_orders.equipment_id` not null | fail pipeline | ☐ |
| DQ-UNIQUE-001 | staging | `work_order_id` unique | fail pipeline | ☐ |
| DQ-RELATION-001 | intermediate | every `work_orders.equipment_id` exists in `equipment` | fail pipeline | ☐ |
| DQ-RANGE-001 | marts | `mtbf_hours >= 0` | fail pipeline | ☐ |
| DQ-FRESH-001 | source | raw export updated within 24h | alert + block downstream | ☐ |
| DQ-BUSINESS-001 | marts | MTTR for CM `<= 30 days` | warn | ☐ |
| DQ-BUSINESS-002 | marts | PM compliance KPI between 0 and 100 | fail pipeline | ☐ |

## On failure
- `fail pipeline` — DAG run marked failed, downstream models not refreshed.
- `warn` — DAG run passes, alert logged, KPI flagged on the dashboard.
- `alert + block downstream` — dashboard is NOT refreshed; SRE-style alert sent.

## Verification
For each rule, the tester must:
1. Insert a known-bad row.
2. Run the rule.
3. Capture the failure output (screenshot / log path) in the PR.
4. Revert the bad row.
