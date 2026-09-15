# Spec — Remove weak and hardcoded secrets (SECRET-003/004/005)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#48**, **#49**, **#50** — SECRET-003 (weak default session key), SECRET-004 (Postman username=password), SECRET-005 (docker-compose credentials).

## Problem

Developers and operators can inherit or copy weak or committed credentials: a shared literal session signing key, a service-account password identical to its username in API explorer fixtures, and local orchestration passwords checked into compose files.

## Outcome

No service defaults to a guessable session key; API explorer fixtures use placeholders; local compose credentials are supplied via environment substitution with an obviously non-production default only.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | No weak literals or real-looking committed secrets in tree |
| Local developer | Clear env overrides / placeholders without inventing production values |
| Operator | Residual rotation guidance for previously exposed accounts |

## Scope

### In scope (this release)

- Base config session keys: env or random one-shot with warning (legal-api, colin-api, GCP jobs)
- Redact coops-updater-job username=password in Legal API Postman collection
- Substitute Hasura/Postgres/Prefect secrets in `data-tool/docker-compose.yaml`

### Out of scope

- Rotating live OIDC passwords (ops)
- Rewriting git history
- Changing how production injects secrets in the cluster

## Journeys

1. Session key hygiene — see `features/secret-003-004-005-secrets-hygiene.feature` (`@R-48.1`, `@R-48.2`)
2. Postman placeholders — same feature (`@R-49.1`, `@R-49.2`)
3. Compose env substitution — same feature (`@R-50.1`)

## Non-functional requirements

- Never commit weak literal `"a secret"` or username=password service credentials
- Compose defaults must read as `dev-only-change-me`, not production-like material

## Open questions

- [x] One PR for all three: yes — cohesive secrets hygiene

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
