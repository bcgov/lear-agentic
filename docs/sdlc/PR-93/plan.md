# Plan — CONFIG-005 data-tool Postgres sslmode

> Architecture and delivery approach for issue #24.

## Summary

Centralize Postgres URI construction in `data-tool/flows/config.py` so LEAR, COLIN migr, and AUTH URIs always include `?sslmode=…`. Default is `require` unless the environment looks local/dev (`prefer`) or `DATABASE_SSLMODE` is set.

## Architecture

```text
env (DATABASE_SSLMODE | FLASK_ENV / DATA_LOAD_ENV)
  → _postgres_sslmode()
  → _postgres_uri(...)
  → SQLALCHEMY_DATABASE_URI*
  → create_engine(...)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Default non-local | `require` | Closes cleartext TCP finding |
| Default local | `prefer` | Avoid breaking laptop Postgres without TLS |
| Override | `DATABASE_SSLMODE` | Ops / local explicit control |
| Scope | Three URIs only | Matches CONFIG-005 evidence |

## Security & privacy

- Residual: `prefer`/`disable` still allow cleartext if operator chooses; non-local default is require
- Cert validation (`verify-full`) remains an ops opt-in via env

## Test approach

- Unit: reload config under controlled env; assert URI query params (`@R-24.1`–`@R-24.3`)
- Acceptance: Gherkin in `spec/features/config-005-data-tool-pg-ssl.feature`

## Rollout

1. Merge code (human checkpoint 3)
2. Ops confirms target Postgres accepts SSL
3. Deploy data-tool workers; set `DATABASE_SSLMODE=require` explicitly in vault if desired

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead | | |
| Security | | |
