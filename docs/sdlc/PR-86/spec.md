# Spec — Upgrade data-tool Flask / Werkzeug (DEP-007)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#12** — `[DEP-007] DEP-007` (High). End-of-life web framework pins in the data-tool migration utility.

## Problem

The data-tool production dependency list pins an end-of-life 2.0.x web stack (and matching HTTP utility) solely to keep an older API documentation library working. That stack no longer receives security fixes while the tool handles Auth and corporate migration data.

## Outcome

data-tool runs on a supported 3.x web stack. The API documentation library is upgraded far enough to support that stack. Companion libraries that break under 3.x are bumped only as needed so installs remain coherent.

## Users & personas

| Persona | Goal |
| --- | --- |
| Platform engineer | Supported, installable dependency set for migration flows |
| Security reviewer | Exit EOL web-framework / HTTP-utility pins (CWE-1104) |
| Maintainer | Clear residual risks for unused or still-legacy companions |

## Scope

### In scope (this release)

- Close DEP-007 for `data-tool/requirements.txt` Flask / Werkzeug pins
- Upgrade the API documentation library that blocked Flask 3
- Minimal companion bumps required for a resolvable, importable Flask 3 stack
- Unit assertions for Flask 3.x, Werkzeug 3.x, and documentation-library floors

### Out of scope

- Full end-to-end Prefect / Oracle migration smoke in CI
- Replacing abandoned Flask-Script / modernizing Flask-Moment for Python 3.12 `distutils`
- Broader dependency modernization (urllib3 1.26, certifi 2020, requests 2.25, etc.)

## Journeys

1. Supported Flask / Werkzeug pins — see `features/dep-007-data-tool-flask.feature`

## Non-functional requirements

- Prefer exact pins matching verified installable versions
- Document residual risk for companions not covered by this finding

## Open questions

- [x] flask-restx ≥1.3 unlocks Flask 3; companion FSA / Babel / jwt-oidc bumps required for importability

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
