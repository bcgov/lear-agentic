# Plan — Remove weak and hardcoded secrets (SECRET-003/004/005)

> Architecture and delivery approach. Technology belongs here (not in `spec.md`).

## Summary

Move Flask `SECRET_KEY` resolution into base `_Config` (env or `os.urandom(24)` + stderr warning) across legal-api, colin-api, and GCP job configs; replace Postman bodies with `{{coops_updater_*}}` variables; use Compose `${VAR:-dev-only-change-me}` for Prefect/Hasura/Postgres in `data-tool/docker-compose.yaml`. Guard with static unit tests and Spec Kit criteria `@R-48.*` / `@R-49.*` / `@R-50.*`.

## Architecture

```text
Env SECRET_KEY ──► _Config.SECRET_KEY
                 └─ missing ──► urandom(24) + WARNING

Postman collection ──► {{coops_updater_username}} / {{coops_updater_password}}

docker-compose ──► ${POSTGRES_PASSWORD:-dev-only-change-me}
                └─ ${HASURA_GRAPHQL_ADMIN_SECRET:-dev-only-change-me}
```

## Key decisions (ADRs may expand)

| Decision | Choice | Rationale |
| --- | --- | --- |
| SECRET_KEY ownership | Base `_Config`, drop Prod-only duplicate | Dev/Test inherit same safe behaviour |
| Missing key behaviour | Random + warning (not hard fail) | Matches existing ProdConfig pattern; local runs keep working |
| Postman | Mustache env vars | Fits Postman; no live password in git |
| Compose defaults | `dev-only-change-me` | Satisfies substitution pattern without looking like a real secret |

## Security & privacy

- Classification: application secrets / local-dev credentials
- Residual: prior commits still contain values; rotate `coops-updater-job` in OIDC realms
- Secrets: no new secrets committed

## Test approach

- Static tests under `legal-api/tests/unit/security/` and `data-tool/tests/`
- Features: `spec/features/secret-003-004-005-secrets-hygiene.feature`

## Rollout

- Environments: local / PR; cluster unchanged
- Migration / cutover: n/a — set `SECRET_KEY` and compose env vars where previously relying on literals

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead | local-agent | 2026-09-15 |
