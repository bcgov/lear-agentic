# Spec — COLIN API python-jose floor and oracledb migration (DEP-009 / DEP-010)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#28** (`DEP-009`) and **#29** (`DEP-010`) (Medium). COLIN API’s JWT helper is behind the current 3.4 floor, and its Oracle driver package is officially deprecated in favour of the maintained successor already used elsewhere in this monorepo.

## Problem

JWT verification/signing depends on an outdated helper release that lags known 3.x hardening. Separately, the Oracle access layer still declares the deprecated driver while sibling jobs already use the maintained package, creating an inconsistent and unmaintained database client path.

## Outcome

COLIN API declares python-jose ≥ 3.4.0 and migrates Oracle access to the maintained driver in thin mode with a compatibility alias so SessionPool call sites stay stable. Manifests no longer name the deprecated Oracle package.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | DEP-009 / DEP-010 closed or residual documented |
| COLIN API maintainer | Oracle pool and OPS health checks still compile against the new driver |
| Platform engineer | Pins align with sibling oracledb usage |

## Scope

### In scope (this release)

- Bump `python-jose` to ≥ 3.4.0 in `colin-api` requirements
- Replace deprecated Oracle driver with maintained package (thin mode + import alias)
- Drop removed encoding kwargs that the new driver rejects
- Spec acceptance `@R-709.1`, `@R-710.1`, `@R-710.2` and unit assertions

### Out of scope

- Migrating away from python-jose to joserfc / Authlib (CVE residual may remain)
- Instant Client / thick-mode enablement
- Unrelated colin-api dependency bumps (Flask, requests, LD SDK, etc.)

## Journeys

1. JWT helper pin meets floor — see `features/dep-009-010-colin-jose-oracledb.feature`
2. Oracle manifests and imports use the maintained driver — same feature

## Non-functional requirements

- Security: raise JWT helper floor; retire deprecated Oracle driver package
- Compatibility: keep SessionPool / DatabaseError call sites via alias
- Residual: python-jose may still carry algorithm-confusion residual (CVE-2022-29217); full jose migration is a follow-up

## Open questions

- [x] Thin-mode alias (`import oracledb as cx_Oracle`) preferred over rewriting every call site

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
