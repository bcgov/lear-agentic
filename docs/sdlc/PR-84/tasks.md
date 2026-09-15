# Tasks — DEP-006 ETL SFTP HTTP dependency floors

Derive from `spec.md` + `features/`. Prefer vertical slices.

## Milestone 1

- [x] TASK-001 — Bump/add `requests`, `urllib3`, `certifi` in all three SFTP job freezes (`requirements.txt` + `requirements/prod.txt`) — covers `@R-706.1`–`@R-706.3`
- [x] TASK-002 — Unit tests asserting secure floors for each job — covers `@R-706.1`–`@R-706.3`
- [x] TASK-003 — Spec/plan/feature + `docs/pr-evidence.md` and draft PR Fixes #11

## Backlog

- [ ] Gazette Flask / Werkzeug major upgrade (align to sibling Flask 2.3.x+; cascade Jinja2 / Click as needed)
- [ ] ETL job lockfiles (related to DEP-003 class findings)
