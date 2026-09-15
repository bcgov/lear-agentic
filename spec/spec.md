# Spec — COLIN API dependency pins (GD-002 / GD-003)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#14** (`[GD-002]`) and **#15** (`[GD-003]`) — High severity dependency findings on COLIN API.

## Problem

COLIN API ships with outdated cryptographic and HTTP-server dependencies that expose known weaknesses: ECDSA signing without modern timing-attack countermeasures, and an HTTP worker that does not correctly validate transfer-encoding headers (request smuggling / desync).

## Outcome

COLIN API dependency pins meet or exceed the remediated versions for both findings. Direct pins win over any older transitive suggestions from JWT libraries. Operators can verify the pins in the requirements freeze without a full application smoke.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | Confirmed High findings closed via version pins |
| COLIN API maintainer | Predictable freeze; rebuild does not silently regress |
| Operator | No unexpected runtime behaviour from the pin bumps alone |

## Scope

### In scope (this release)

- Raise the ECDSA package pin to a Minerva-mitigated release (`>=0.19.0`)
- Raise the Gunicorn pin to a Transfer-Encoding–validating release (`>=22.0.0`, prefer aligning with Legal API’s 23.x)
- Keep a direct ECDSA pin so older transitive constraints cannot win
- Spec scenarios `@R-14.1` and `@R-15.1` plus a minimal pin assertion test
- Evidence pack and draft PR closing both issues

### Out of scope

- Migrating off python-jose to another JWT library
- Full COLIN API / container smoke or deploy verification
- Bumping the same packages in other monorepo components (data-tool, business-registry-model, etc.)

## Journeys

1. ECDSA pin meets remediated floor — see `features/gd-002-003-ecdsa-gunicorn.feature` (`@R-14.1`)
2. Gunicorn pin meets remediated floor — same feature (`@R-15.1`)

## Non-functional requirements

- Accessibility: n/a (dependency pins)
- Privacy: no change to data handling
- Compatibility: prefer Legal API’s Gunicorn 23.x line when compatible

## Open questions

- [x] Gunicorn target: prefer `23.0.0` to match Legal API
- [ ] Ops/smoke confirms COLIN API starts cleanly under the new Gunicorn after merge

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
