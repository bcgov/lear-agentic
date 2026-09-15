# Spec — COLIN API requests / urllib3 pins (DEP-002)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#7** — `[DEP-002]` outdated `requests` / `urllib3` on COLIN API (High).

## Problem

COLIN API freezes `requests` and `urllib3` at versions that predate multiple documented HTTP-client security advisories (header injection / proxy credential leakage class issues). Rebuilds keep shipping those floors until the freeze is raised.

## Outcome

COLIN API production requirements pin `requests` and `urllib3` at secure floors (`requests` ≥ 2.32.3; `urllib3` ≥ 2.2.0 on the 2.x line when compatible). Operators can verify the pins from the freeze without a full application smoke.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | DEP-002 closed via version pins covering known advisories |
| COLIN API maintainer | Predictable freeze; no silent downgrade on rebuild |
| Operator | Pin bumps alone do not change API contracts |

## Scope

### In scope (this release)

- Raise `requests` and `urllib3` pins in `colin-api/requirements.txt`
- Prefer urllib3 2.x; if incompatible with the requests / cx_Oracle stack, pin latest patched 1.26.x and document residual
- Spec scenarios `@R-702.1`+ and a minimal pin-assertion test
- Evidence pack and draft PR Fixes #7

### Out of scope

- Full COLIN API / container smoke or deploy verification
- Bumping the same packages in other monorepo components
- Broader dependency modernization (certifi, Flask stack, lockfiles — separate findings)

## Journeys

1. `requests` pin meets remediated floor — see `features/dep-002-colin-requests-urllib3.feature` (`@R-702.1`)
2. `urllib3` pin meets remediated floor — same feature (`@R-702.2`)

## Non-functional requirements

- Accessibility: n/a (dependency pins)
- Privacy: no change to data handling
- Compatibility: pin set must install beside existing `cx-Oracle` and `requests` consumers

## Open questions

- [x] Target: `requests>=2.32.3`, `urllib3` latest compatible 2.x
- [ ] Ops/smoke confirms COLIN API starts cleanly after merge

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
