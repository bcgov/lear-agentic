# Tasks — Legal API HTTP security response headers (CONFIG-001)

Derive from `spec.md` + `features/`. Prefer vertical slices.

## Milestone 1

- [x] TASK-001 — Add `apply_security_headers` helper — covers `@R-06.1`, `@R-06.3`
- [x] TASK-002 — Wire helper into Legal API `after_request` (preserve version headers) — covers `@R-06.2`
- [x] TASK-003 — Unit tests for required headers + version-header preservation — covers `@R-06.1`–`@R-06.3`
- [x] TASK-004 — Spec / feature / plan / pr-evidence for issue #3

## Backlog

- [ ] CONFIG-002 — COLIN API security headers (separate issue)
