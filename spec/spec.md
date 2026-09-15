# Spec — COLIN API Oracle CPRD TLS hooks (CONFIG-006)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#25** — `[CONFIG-006] Oracle CPRD Database Connection Without SSL — COLIN API` (Medium).

## Problem

COLIN API opens a pooled connection to the Oracle CPRD legacy register without any application-layer TLS, wallet, or encryption requirement. Transport security depends entirely on listener-side configuration outside this codebase.

## Outcome

The application can build a TLS (TCPS) connect descriptor, accept wallet / DN / net-encryption configuration hooks, and **fail closed** when a require-SSL flag is set without TLS enabled. Full mutual TLS still needs ops-provided wallet files; residual risk is documented.

## Users & personas

| Persona | Goal |
| --- | --- |
| Platform operator | Wire CPRD TLS via env + mounted wallet |
| Security reviewer | Clear fail-closed control when TLS is mandatory |
| API maintainer | Local/test can still run without a wallet |

## Scope

### In scope (this release)

- TCPS DSN builder + SessionPool wiring
- `ORACLE_SSL`, `ORACLE_REQUIRE_SSL`, wallet / DN / net-encryption env hooks
- Prod fail-closed default; test/dev opt-out
- Unit tests for DSN + fail-closed path

### Out of scope

- Shipping wallet files or sqlnet.ora in the repo
- Replacing cx_Oracle Instant Client thick mode
- Data-tool Oracle paths (separate component)

## Journeys

1. Cleartext local — see `features/config-006-colin-oracle-ssl.feature`
2. TCPS + wallet hooks — same feature
3. Fail closed — same feature

## Non-functional requirements

- Accessibility: n/a
- Privacy: protects CPRD credentials and payloads on the wire when TLS is enabled
- Fail closed: `ORACLE_REQUIRE_SSL` without `ORACLE_SSL` must not open a pool

## Open questions

- [ ] Ops provides CPRD TCPS port, wallet mount path, and whether DN match is required
- [x] Residual: wallet/sqlnet.ora remain outside app control

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | | |
| BA | | |
| QA (acceptance ownership) | | |
