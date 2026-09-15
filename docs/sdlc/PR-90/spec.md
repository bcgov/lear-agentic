# Spec — Bind remaining string-typed stringify_list paths (VULN-003)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#53** — `[VULN-003] Inadequate SQL sanitization in stringify_list() utility` (Medium).

## Problem

A shared list-to-SQL helper wraps values in quotes without escaping embedded quote characters. Any string-typed list passed into Oracle `IN (...)` clauses via that helper can alter query structure. VULN-002 closed the cooper-reset request filters; other string-typed call sites (corporation numbers, filing type codes, business identifiers / corp types) remained.

## Outcome

All string-typed `IN`-list values in colin-api that previously used the unsafe helper are bound as data. Injection-like strings cannot change SQL structure on those paths. Trusted integer event / address ID lists may still use the legacy helper until a follow-up, with documented residual risk.

## Users & personas

| Persona | Goal |
| --- | --- |
| Registry / COLIN service | Reset and lookup paths treat corp nums / filing codes as data |
| Security reviewer | CWE-89 closed for remaining string-typed `stringify_list` sites |
| Maintainer | Same `build_in_clause` pattern as VULN-002; residual int-ID sites noted |

## Scope

### In scope (this release)

- Close VULN-003 for string-typed / untrusted list paths in reset, business, and filing_type models
- Reuse / extend VULN-002 `build_in_clause` (and cooper reset query builder where applicable)
- Unit coverage that malicious string items are not interpolated into SQL text
- Document residual risk for integer `event_ids` / `address_ids` / `delete_from_table_by_event_ids`

### Out of scope

- Mandatory bind conversion of trusted integer event/address ID lists (residual)
- Auth / role changes
- Changing reset or lookup business rules beyond safe query construction

## Journeys

1. String IN-lists bind as placeholders — see `features/vuln-003-stringify-list-remaining.feature`
2. Residual integer ID sites remain documented — same feature

## Non-functional requirements

- Accessibility: n/a (API)
- Privacy: no change to data classification
- Fail closed: non-empty string lists must bind every element

## Open questions

- [x] Convert int event_id sites now? No — residual note per issue guidance; prefer binds wherever string values flow

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
