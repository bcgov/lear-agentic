# Spec — ETL SFTP jobs HTTP dependency floors (DEP-006)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#11** — `[DEP-006]` outdated HTTP / web-framework stack on sftp-gazette (and align sibling SFTP ETL jobs).

## Problem

The gazette SFTP ETL job freezes its outbound HTTP client and related certificate-bundle packages at versions that predate multiple documented security advisories. Sibling ICBC and NUANS SFTP jobs already meet the client floors in places but do not declare matching direct pins for the certificate bundle and HTTP transport library, so rebuilds can drift.

## Outcome

All three SFTP ETL jobs (`sftp-gazette`, `sftp-icbc-report`, `sftp-nuans-report`) declare secure floors for the outbound HTTP client stack. Operators can verify the pins from each job’s freeze without a full container smoke. Any web-framework major upgrade that remains unsafe under the gazette freeze is recorded as residual risk—not claimed fixed.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | DEP-006 partially or fully closed with explicit residual where needed |
| ETL maintainer | Predictable pins across the three SFTP jobs |
| Operator | Pin bumps alone do not change SFTP / notebook job contracts |

## Scope

### In scope (this release)

- Raise or add `requests`, `urllib3`, and `certifi` pins in each job’s `requirements.txt` (and matching `requirements/prod.txt`)
- Prefer `urllib3` 2.x when compatible with `requests`; otherwise patched 1.26.x with residual noted
- Spec scenarios `@R-706.1`+ and minimal pin-assertion tests
- Evidence pack and draft PR Fixes #11
- Document Flask / Werkzeug major upgrade as residual if not clearly safe under gazette’s remaining freeze

### Out of scope

- Full ETL / OpenShift cronjob smoke or deploy verification
- Broader gazette modernization (Jinja, Click, Jupyter stack, lockfiles)
- Flask 3.x upgrade

## Journeys

1. Each job’s `requests` pin meets the remediated floor — see `features/dep-006-etl-sftp-http-deps.feature` (`@R-706.1`)
2. Each job’s `urllib3` pin meets the remediated floor — same feature (`@R-706.2`)
3. Each job’s `certifi` pin is current — same feature (`@R-706.3`)

## Non-functional requirements

- Accessibility: n/a (dependency pins)
- Privacy: no change to data handling
- Compatibility: pin set must install beside existing notebook / SFTP job dependencies

## Open questions

- [x] Target: `requests>=2.32.3`, `urllib3` 2.x (or 1.26.20 fallback), current `certifi`
- [x] Flask / Werkzeug on gazette: residual major upgrade (align toward sibling Flask 2.3.x) — not claimed fixed here
- [ ] Ops/smoke confirms the three cronjobs start cleanly after merge

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
