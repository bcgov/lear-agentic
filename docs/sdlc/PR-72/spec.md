# Spec — Ephemeral JWT test keys (SECRET-001)

## Feature proposal
GitHub issue **#18** — `[SECRET-001] RSA JWT Private Test Key Committed in Source TestConfig Classes` (High).

## Problem
A static RSA private key used for JWT test mode is committed in Legal API and business-registry-account TestConfig. If test mode is mis-enabled in a higher environment, attackers can forge tokens with that published key.

## Outcome
TestConfig no longer embeds a static private key. Test JWT material is generated per process so the repository does not publish a reusable forging key.

## Scope
### In scope
- Remove committed PEM/JWKS private material from both TestConfig classes
- Generate ephemeral matching public/private test material at runtime

### Out of scope
- Git history purge of the prior key; enforcing JWT_OIDC_TEST_MODE=false in deploy configs (ops)

## Journeys
1. TestConfig uses process-local keys — `features/secret-001-ephemeral-jwt-test-keys.feature`

## Sign-off (checkpoint 1)
| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
