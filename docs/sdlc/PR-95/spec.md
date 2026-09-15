# Spec — COLIN API Jinja2 xmlattr floor (GD-001)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#37** — `[GD-001] Jinja2 before 3.1.3 xmlattr XSS` (Medium).

## Problem

COLIN API pins Jinja2 2.11.3. Versions before 3.1.3 do not escape attribute names in the `xmlattr` filter, allowing a context-data supplier to inject arbitrary HTML attributes (XSS).

## Outcome

Jinja2 is directly pinned at **>= 3.1.3** (3.1.4) with a compatible MarkupSafe companion, coordinated so the current Flask 1.1.2 stack still installs. Broader Flask 2.3 upgrade remains DEP-001.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | Known Jinja2 advisory is cleared in the freeze file |
| API maintainer | Minimal pin change without waiting on full Flask 3 |

## Scope

### In scope (this release)

- Bump `Jinja2` and `MarkupSafe` in `colin-api/requirements.txt`
- Pin test + feature criterion `@R-37.1`

### Out of scope

- Full Flask / Werkzeug / flask-restx upgrade (DEP-001)
- Auditing every template for `xmlattr` usage beyond the floor bump

## Journeys

1. Pin floor — see `features/gd-001-colin-jinja2.feature`

## Non-functional requirements

- Accessibility: n/a
- Privacy: reduces XSS risk from templated attribute rendering
- Compatibility: keep Flask==1.1.2 on this branch; DEP-001 supersedes the stack later

## Open questions

- [x] Coordinate MarkupSafe with Jinja2 3.1.x without forcing Flask 2.3 in this PR

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | | |
| BA | | |
| QA (acceptance ownership) | | |
