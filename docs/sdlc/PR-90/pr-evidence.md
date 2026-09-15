# PR evidence

## VULN-003 — Bind remaining string-typed stringify_list paths (issue #53)

- Spec: `spec/spec.md`, `spec/features/vuln-003-stringify-list-remaining.feature` (`@R-53.1`, `@R-53.2`, `@R-53.3`)
- Plan: `spec/plan.md`
- Change: `colin-api/src/colin_api/utils/__init__.py` — `build_in_clause` + `build_cooper_reset_filings_query`; `stringify_list` / `delete_from_table_by_event_ids` residual docs for trusted int IDs
- Change: `colin-api/src/colin_api/models/reset.py` — cooper reset filters + corp_num deletes use binds
- Change: `colin-api/src/colin_api/models/business.py` — identifiers / corp_types use binds
- Change: `colin-api/src/colin_api/models/filing_type.py` — matching_filing_types use binds
- Tests: `colin-api/tests/test_vuln003_build_in_clause.py`
- Residual: integer `event_ids` / `address_ids` still use `stringify_list` in `address.py`, `office.py`, `corp_party.py`, reset event deletes, and `delete_from_table_by_event_ids` (trusted DB-sourced ints; optional follow-up)
