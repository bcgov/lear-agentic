# PR evidence

## VULN-001 — Parameterize get_last_event_id (issue #22)

- Spec: `spec/spec.md`, `spec/features/vuln-001-parameterize-get-last-event-id.feature` (`@R-22.1`, `@R-22.2`, `@R-22.3`)
- Plan: `spec/plan.md`
- Change: `legal-api/src/legal_api/resources/v2/business/colin_sync.py` — `get_last_event_id` uses `:identifier` bound parameter instead of f-string interpolation
- Tests: `legal-api/tests/unit/resources/v2/test_colin_sync.py` (`test_get_last_event_id_for_identifier`, `test_get_last_event_id_not_found`, `test_get_last_event_id_rejects_sql_injection_payload`)
