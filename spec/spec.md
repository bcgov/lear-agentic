# Spec — Parameterize get_last_event_id (VULN-001)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#22** — `[VULN-001] SQL Injection via unparameterized f-string in get_last_event_id()` (High).

## Problem

The COLIN sync endpoint that returns the last COLIN event id for a business identifier builds its database query by embedding the path parameter directly into the SQL text. A caller with the COLIN service role can supply a crafted identifier and change the meaning of the query (read or disrupt data beyond the intended business).

## Outcome

Looking up the last COLIN event id for a business uses a bound parameter for the identifier. Attacker-controlled path input cannot alter SQL structure. Existing happy-path behaviour (max id for a real identifier; not-found when none) is preserved.

## Users & personas

| Persona | Goal |
| --- | --- |
| COLIN sync service | Retrieve last event id for a known business identifier |
| Security reviewer | CWE-89 in this endpoint is closed |
| Legal-api maintainer | Minimal, style-consistent change with regression tests |

## Scope

### In scope (this release)

- Remediate VULN-001 on `/internal/last-event-id/<identifier>`
- Bound-parameter query for business identifier (no string interpolation into SQL)
- Unit coverage for success, not-found, and injection-style identifier

### Out of scope

- VULN-002 / VULN-003 (colin-api `stringify_list`) — separate issues
- Other f-string SQL in `colin_sync.py` (e.g. integer `colin_id` insert) unless required for this finding
- Auth / role changes for the COLIN endpoint

## Journeys

1. Parameterized last-event-id lookup — see `features/vuln-001-parameterize-get-last-event-id.feature`

## Non-functional requirements

- Accessibility: n/a (internal API)
- Privacy: no change to data classification; reduces unauthorized data exposure via injection
- Compatibility: response shape (`maxId` / not-found message) unchanged

## Open questions

- [x] Fix target: `get_last_event_id` only (issue #22 / VULN-001)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
