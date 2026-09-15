# Plan — SECRET-002 Postman client secret redaction

> Architecture and delivery approach. Technology belongs here (not in `spec.md`).

## Summary

Replace the plaintext `client_secret` in `legal-api/tests/postman/legal-dev.postman_environment.json` with a non-secret placeholder. Leave collection scripts that *read* `{{client_secret}}` unchanged. Call out IdP rotation as residual ops work.

## Architecture

```text
Postman env (git) → placeholder only
Local tester → sets client_secret in unsynced Postman env / vault
IdP (dev.oidc.gov.bc.ca) → rotate entity-service-account secret (ops)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Redaction | Placeholder string | Keeps Postman UX; prevents re-commit of live secret |
| History | No rewrite in this PR | High risk; rotation closes active abuse window |

## Security & privacy

- Classification: credential exposure (dev realm)
- Residual: secret remains in git history until rotated and optionally purged

## Test approach

- Assert Postman env `client_secret` is empty or placeholder (no UUID-shaped live secret)

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
