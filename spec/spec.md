# Spec — Redact OIDC JWT info from INFO logs (LOG-001)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#16** — `[LOG-001] Full OIDC JWT token info object logged at INFO level` (High).

## Problem

On every account-affiliated business lookup, the service writes the full authenticated identity token info (username, subject, email, realm roles, and related claims) into INFO-level logs. INFO logs are retained in production by default, so identity-PII is unnecessarily exposed to log aggregators and operators.

## Outcome

Account-affiliation request logs at INFO include only non-PII correlation fields needed for operations (e.g. account id and business identifier). They never include preferred username, email, subject, roles dumps, or the full token-info object. Existing response behaviour (attach `accountId` when the org matches) is preserved.

## Users & personas

| Persona | Goal |
| --- | --- |
| System / account-identity caller | Look up a business and optionally receive affiliated account id |
| Security reviewer | CWE-532 for this INFO path is closed |
| Operators / SRE | Retain enough correlation in logs without identity-PII |

## Scope

### In scope (this release)

- Remediate LOG-001 on the business GET account-affiliation INFO path
- Log only non-PII correlation fields at INFO for that path
- Unit coverage for log redaction and unchanged accountId attachment behaviour

### Out of scope

- WARNING-level unauthorized logs that still include `preferred_username` (separate hardening)
- LOG-002+ (DEBUG JWT dumps in other components) — separate issues
- Changing authentication, authorization, or account-service behaviour

## Journeys

1. Redacted VALID account request logging — see `features/log-001-redact-jwt-oidc-info-log.feature`

## Non-functional requirements

- Accessibility: n/a (API logging)
- Privacy: reduces identity-PII written to production INFO logs (CWE-532)
- Compatibility: HTTP response shape unchanged

## Open questions

- [x] Fix target: business GET VALID account request INFO log only (issue #16 / LOG-001)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
