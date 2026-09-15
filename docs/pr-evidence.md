# PR evidence

## SECRET-007 (issue #61)
- `.github/workflows/colin-api-ci.yml` uses `ci-ephemeral-{run_id}-{run_attempt}` for `DATABASE_*_PASSWORD` and service `POSTGRES_PASSWORD`
- Residual: password remains in workflow logs/env of an ephemeral job-scoped container (acceptable for destroyed CI services)

## SECRET-008 (issue #62)
- `python/common/sql-versioning/tests/conftest.py` reads `SQL_VERSIONING_TEST_DATABASE_URL`
- Default labeled test-only: `postgresql://postgres:test-only-local-postgres@localhost:5433/test`
- docker-compose default password aligned via `SQL_VERSIONING_TEST_POSTGRES_PASSWORD`
