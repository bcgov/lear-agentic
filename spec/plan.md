# Plan — SECRET-007 / SECRET-008
1. Derive CI DB password from `github.run_id`/`run_attempt` for job env + service container.
2. Move sql-versioning conftest URL to env; align docker-compose default to `test-only-local-postgres`.
## Approval
| Role | Name | Date |
| --- | --- | --- |
| Architect | local-agent | 2026-09-15 |
