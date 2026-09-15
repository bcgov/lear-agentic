# Spec — COLIN API Flask / Werkzeug stack upgrade (DEP-001)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#6** — `[DEP-001] DEP-001` (High). COLIN API runs on an end-of-life web framework stack with known fixed advisories that cannot be patched in-place.

## Problem

COLIN API’s HTTP framework and WSGI toolkit are multiple major versions behind supported releases. Advisories that were fixed in later minors (session-cookie handling; multipart DOS) have no backport on the pinned EOL series. Remaining on that series means production cannot take security fixes without a deliberate upgrade.

## Outcome

COLIN API declares a post-EOL intermediate stack that includes the fixed releases for the cited advisories (Flask ≥ 2.3.2, Werkzeug ≥ 2.2.3), with companion library pins and the small application changes required for that intermediate major line. Flask 3.x remains out of scope until JWT helper modernization.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | DEP-001 CVEs addressed or residual risk documented |
| COLIN API maintainer | App still boots; OPS/meta routes respond; manage CLI works without Flask-Script |
| Platform engineer | Pin set is explicit and test-enforced |

## Scope

### In scope (this release)

- Close DEP-001 for `colin-api` by upgrading Flask/Werkzeug and companions (Jinja2, MarkupSafe, itsdangerous, click, flask-restx; blinker floor for Flask 2.3)
- Minimal app fixes for Flask 2.3 (`ENV` config, Oracle pool via app context `g`, Click manage CLI)
- Spec acceptance `@R-701.1`–`@R-701.4` and unit pin assertions
- Document residual: not yet on Flask 3.x; `flask-jwt-oidc==0.3.0` blocks Flask 3 without a separate bump

### Out of scope

- Flask 3.x / full framework modernization
- Upgrading `flask-jwt-oidc` beyond 0.3.0
- Unrelated dependency bumps (requests, urllib3, gunicorn, etc.)
- Oracle driver replacement (`cx_Oracle` → `oracledb`)

## Journeys

1. Manifest pins meet advisory floors — see `features/dep-001-colin-flask-upgrade.feature`
2. Application boots on the upgraded stack — same feature
3. Flask-Script removed; manage CLI via Click — same feature

## Non-functional requirements

- Security: remediate CVE-2023-30861 (Flask ≥ 2.3.2) and CVE-2023-25577 (Werkzeug ≥ 2.2.3)
- Compatibility: preserve existing JSON API routes; additive/internal changes only
- Residual: stack remains on Flask 2.3.x (itself aging); Flask 3 requires jwt-oidc upgrade

## Open questions

- [x] Intermediate target: Flask 2.3.3 + Werkzeug 2.3.8 + flask-restx 1.3.0 (`@R-701.1+`)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
