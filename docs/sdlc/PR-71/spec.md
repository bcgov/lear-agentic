# Spec — Remove committed OIDC client secret (SECRET-002)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#19** — `[SECRET-002] Dev OIDC Client Secret Committed in Postman Environment File` (High).

## Problem

A development identity-provider client secret for a service account is stored in a shared Postman environment file in the repository. Anyone with read access can use that secret to obtain tokens in the development realm.

## Outcome

The repository no longer contains the live client secret. Local/manual API explorers load the secret from a non-committed source. Operators are told to rotate the exposed credential.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | No live OIDC secrets in git history going forward (rotation closes residual) |
| API tester | Clear placeholder to fill locally without committing |

## Scope

### In scope (this release)

- Remove the committed `client_secret` value from the Legal API Postman environment cited by SECRET-002
- Document that the exposed secret must be rotated in the IdP

### Out of scope

- Rewriting git history to purge the secret from past commits
- Rotating the IdP secret (ops action outside this fork)

## Journeys

1. Postman environment has no live secret — see `features/secret-002-redact-postman-client-secret.feature`

## Non-functional requirements

- Secrets never committed; placeholders only
- Residual risk: prior commits still contain the value until rotation + optional history purge

## Open questions

- [x] History rewrite: deferred — rotation is the primary residual control

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
