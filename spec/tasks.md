# Tasks — VULN-003 bind remaining string-typed stringify_list paths

Derive from `spec.md` + `features/`. Prefer vertical slices.

## Milestone 1

- [x] TASK-001 — Add / extend `build_in_clause` (+ cooper reset query builder) and document `stringify_list` residual for int IDs — covers `@R-53.1`
- [x] TASK-002 — Parameterize string-typed paths in `reset.py`, `business.py`, `filing_type.py` — covers `@R-53.2`, `@R-53.3`
- [x] TASK-003 — Unit tests with `criterion: @R-53.x` provenance — covers `@R-53.1`–`@R-53.3`
- [x] TASK-004 — Append `docs/pr-evidence.md` and open draft PR Fixes #53 (review receipt + residual)

## Backlog

- [ ] Optional follow-up: bind integer `event_ids` / `address_ids` / `delete_from_table_by_event_ids`
