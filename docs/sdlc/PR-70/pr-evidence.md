# PR evidence

## VULN-002 — Parameterize cooper reset IN lists (issue #23)

- Spec: `spec/spec.md`, `spec/features/vuln-002-parameterize-stringify-list.feature` (`@R-04.1`, `@R-04.2`, `@R-04.3`)
- Plan: `spec/plan.md`
- Change: `colin-api/src/colin_api/utils/__init__.py` adds `build_in_clause` + `build_cooper_reset_filings_query`; `stringify_list` docstring warns against untrusted input
- Change: `colin-api/src/colin_api/models/reset.py` `get_filings_for_reset` uses the parameterized query builder for `identifiers` / `filing_types`
- Tests: `colin-api/tests/test_vuln002_build_in_clause.py`
- Residual: other `stringify_list` call sites remain (VULN-003); internal event-id lists not changed in this PR
