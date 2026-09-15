# PR evidence

## CONFIG-005 — Postgres sslmode (issue #24)

- Spec: `spec/spec.md`, `spec/features/config-005-data-tool-pg-ssl.feature` (`@R-24.1`, `@R-24.2`, `@R-24.3`)
- Plan: `spec/plan.md`
- Change: `data-tool/flows/config.py` — `_postgres_sslmode` / `_postgres_uri`; LEAR, COLIN migr, AUTH URIs append `?sslmode=…`
- Default: `require` when non-local; `prefer` when `FLASK_ENV`/`APP_SETTINGS`/`DATA_LOAD_ENV` signal local/dev; override via `DATABASE_SSLMODE`
- Sample: `data-tool/.corps.env.sample`
- Tests: `data-tool/tests/flows/test_config_005_postgres_sslmode.py`
- Residual: operators can still set `DATABASE_SSLMODE=disable`; certificate pinning (`verify-full`) is opt-in
