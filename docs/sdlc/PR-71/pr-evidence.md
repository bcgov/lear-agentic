# PR evidence

## SECRET-002 — Postman OIDC client secret (issue #19)

- Spec: `spec/features/secret-002-redact-postman-client-secret.feature` (`@R-19.1`, `@R-19.2`)
- Change: `legal-api/tests/postman/legal-dev.postman_environment.json` — `client_secret` replaced with placeholder
- Residual: value remains in git history; **rotate** `entity-service-account` secret on `dev.oidc.gov.bc.ca` (ops)
