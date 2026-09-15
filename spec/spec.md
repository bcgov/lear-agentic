# Spec — data-tool lockfile + emailer dep cleanup (DEP-017 / DEP-019)

## Feature proposal
Issues **#36** (DEP-017) and **#56** (DEP-019).

## Outcome
- `data-tool/requirements.lock` pins resolvable transitive PyPI deps (documented exclusions).
- `business-emailer` no longer declares unused `Flask-Script` or `legacy-cgi`.

## Sign-off
| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
