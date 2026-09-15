# Spec — Redact user JWT DEBUG logs (LOG-002)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#17** — `[LOG-002] Full JWT token dictionary logged at DEBUG in user creation and lookup paths` (High).

## Problem

On every authenticated path that creates or looks up a local user from an identity token, the service writes the complete token dictionary to DEBUG logs. Those dictionaries carry identity PII (names, IdP user id, login source, subject, issuer). If DEBUG logging is enabled in any environment that aggregates logs, that PII is exposed beyond the identity provider boundary (CWE-532).

## Outcome

User create and lookup from JWT never emit the full token dictionary (or equivalent claim dump) at DEBUG. Operators can still see that a token was present and, after create, the internal user id — without names, IdP ids, login source, subject, or issuer values in the log line.

## Users & personas

| Persona | Goal |
| --- | --- |
| Authenticated registry user | Account linkage works without their identity claims appearing in app logs |
| Operator / SRE | Enough DEBUG signal to confirm create vs lookup without PII |
| Security reviewer | LOG-002 / CWE-532 closed for these paths |

## Scope

### In scope (this release)

- Close LOG-002 for `User.create_from_jwt_token` and `User.get_or_create_user_by_jwt`
- Remove or redact DEBUG logs that interpolate the full token (and user object dumps that would re-emit the same claims)
- At most: token presence and internal user id after create
- Unit coverage that forbidden claim values do not appear in DEBUG messages

### Out of scope

- LOG-001 (OIDC token logged at INFO in legal-api business routes)
- Other queue/job JWT DEBUG findings (LOG-003+)
- Changing how user rows are populated from JWT claims

## Journeys

1. Create user from JWT without PII in DEBUG — see `features/log-002-redact-user-jwt-debug-logs.feature`
2. Lookup / get-or-create without PII in DEBUG — same feature

## Non-functional requirements

- Accessibility: n/a (library model)
- Privacy: identity-pii must not appear in DEBUG for these methods
- Behaviour: create / lookup / exception paths unchanged aside from log content

## Open questions

- [x] Remove logs entirely vs presence/user-id only: presence + internal user id after create (`@R-09.1+`)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
