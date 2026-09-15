# Tasks — LOG-002 redact user JWT DEBUG logs

Derive from `spec.md` + `features/`. Prefer vertical slices.

## Milestone 1

- [x] TASK-001 — Redact DEBUG logs in `User.create_from_jwt_token` / `User.get_or_create_user_by_jwt` — covers `@R-09.1`, `@R-09.2`, `@R-09.3`
- [x] TASK-002 — Unit tests with caplog proving token PII is absent from DEBUG — covers `@R-09.1`–`@R-09.3`
- [x] TASK-003 — Append `docs/pr-evidence.md` and open draft PR Fixes #17

## Backlog

- [ ] LOG-001 — OIDC token at INFO in legal-api business routes
- [ ] Other LOG-* JWT DEBUG findings in queue/job workers
