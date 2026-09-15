# Plan — SECRET-001 ephemeral JWT test keys

## Summary
Add a small helper that generates an RSA keypair once per process and wire TestConfig JWT_OIDC_TEST_* fields from it in legal-api and business-registry-account.

## Key decisions
| Decision | Choice | Rationale |
| --- | --- | --- |
| Generation | cryptography RSA 2048 | Already common transitive dep for JWT stacks |
| Scope | Both cited TestConfig sites | Matches RA finding |

## Residual risk
Prior private key remains in git history — treat as compromised for any env that ever used JWT_OIDC_TEST_MODE with that key.

## Approval
| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
