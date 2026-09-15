# PR evidence

## SECRET-003 — Weak Flask SECRET_KEY default (issue #48)

- Spec: `spec/features/secret-003-004-005-secrets-hygiene.feature` (`@R-48.1`, `@R-48.2`)
- Change: base `_Config` in legal-api, colin-api, and 8 GCP job configs — `SECRET_KEY` from env or `os.urandom(24)` with warning; removed weak `"a secret"` literal
- Samples: `gcp-jobs/furnishings/.env.sample`, `gcp-jobs/update-colin-filings/.env.sample` cleared of weak default
- Tests: `legal-api/tests/unit/security/test_secret_003_004.py`

## SECRET-004 — Postman coops-updater-job username=password (issue #49)

- Spec criteria: `@R-49.1`, `@R-49.2`
- Change: `legal-api/tests/postman/legal-api.postman_collection.json` — 11 bodies use `{{coops_updater_username}}` / `{{coops_updater_password}}`
- Change: `legal-api/tests/postman/legal-dev.postman_environment.json` — placeholder env keys (no live password)
- Residual: prior commits still contain the credential; **rotate** `coops-updater-job` in OIDC realms (ops)

## SECRET-005 — data-tool docker-compose credentials (issue #50)

- Spec criteria: `@R-50.1`
- Change: `data-tool/docker-compose.yaml` — `${POSTGRES_PASSWORD:-dev-only-change-me}` and `${HASURA_GRAPHQL_ADMIN_SECRET:-dev-only-change-me}`
- Tests: `data-tool/tests/test_secret_005_docker_compose.py`
- Residual: previous literals remain in git history; local stacks should set stronger env values when shared
