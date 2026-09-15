# Spec — Document/permissions logging + Postman syntax CI (LOG-014 / LOG-015 / TEST-005)

## Feature proposal
Issues **#58**, **#59**, **#66**.

## Outcome
- Document service decode failures are logged.
- 403/permission denials log actor id + roles presence + resource (non-PII).
- CI syntax-validates Postman collection/environment without live secrets.

## Sign-off
| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
