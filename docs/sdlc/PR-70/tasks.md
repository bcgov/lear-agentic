# Tasks — VULN-002 parameterize reset IN lists

Derive from `spec.md` + `features/`. Prefer vertical slices.

## Milestone 1

- [x] TASK-001 — Add `build_in_clause` / `build_cooper_reset_filings_query` and document `stringify_list` as unsafe for untrusted input — covers `@R-04.1`
- [x] TASK-002 — Parameterize `Reset.get_filings_for_reset` for `identifiers` / `filing_types` — covers `@R-04.2`, `@R-04.3`
- [x] TASK-003 — Unit tests with `criterion: @R-04.x` provenance — covers `@R-04.1`–`@R-04.3`
- [x] TASK-004 — Append `docs/pr-evidence.md` and open draft PR Fixes #23

## Backlog

- [ ] VULN-003 — replace remaining `stringify_list` call sites with binds where values may be untrusted
