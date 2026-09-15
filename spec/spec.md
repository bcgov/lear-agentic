# Spec — Parameterize reset IN lists (VULN-002)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#23** — `[VULN-002] SQL Injection via stringify_list() with user-supplied identifiers and filing_types` (High).

## Problem

The COLIN cooper reset path accepts corporation identifiers and filing type codes from the caller. Those values were embedded into the reset lookup SQL as quoted list literals after a weak sanitize step. An authenticated caller who can reach the reset endpoint can alter query structure (classic SQL injection) instead of only filtering to named corporations or filing types.

## Outcome

Reset lookup filters for identifiers and filing types treat caller-supplied values as **data**, never as SQL text. Injection payloads in those fields cannot change the query structure. Operators still filter resets by identifier and filing type lists as before.

## Users & personas

| Persona | Goal |
| --- | --- |
| Registry / COLIN service | Reset COOPER changes for selected corps / filing types safely |
| Security reviewer | CWE-89 closed for request-sourced IN-list values on this path |
| Maintainer | Clear helper for parameterized IN lists; legacy helper documented as unsafe for untrusted input |

## Scope

### In scope (this release)

- Close VULN-002 for `/reset/cooper` → `get_filings_for_reset` filters on `identifiers` and `filing_types`
- Parameterized (bind-variable) construction for those request-sourced lists
- Unit coverage that malicious list items are not interpolated into SQL text
- Document residual risk for other `stringify_list` call sites (tracked as VULN-003)

### Out of scope

- Full remediation of every `stringify_list` call site (VULN-003)
- Auth / role changes on the reset endpoint
- Changing reset business rules beyond safe query construction

## Journeys

1. Safe filter by identifiers / filing types — see `features/vuln-002-parameterize-stringify-list.feature`
2. Injection payload treated as literal filter value — same feature

## Non-functional requirements

- Accessibility: n/a (API)
- Privacy: no change to data classification
- Fail closed: empty filter lists omit the clause (existing behaviour); non-empty lists must bind every element

## Open questions

- [x] Minimal fix vs rewrite all stringify_list sites: minimal — user-supplied path only; residual → VULN-003

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
