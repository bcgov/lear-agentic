# Spec — LEAR ETL SFTP host-key verification default (CONFIG-004)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#5** — `[CONFIG-004] SFTP Host Key Verification Conditionally Disabled via Environment Variable — ETL SFTP Jobs` (High).

## Problem

Gazette, ICBC, and NUANS batch jobs can transfer filings/reports to external SFTP endpoints with host identity checks turned off by setting a single environment flag. That opt-out is documented as local-only, but nothing fails closed if the flag is set (or host identity is missing) in a deployed environment — opening a MITM path on those transfers.

## Outcome

By default, all three ETL SFTP jobs **verify** the remote host identity and **refuse to connect** when the expected host identity is not configured. Operators may still disable verification **explicitly** for local development; that path is never the default and logs a warning.

## Users & personas

| Persona | Goal |
| --- | --- |
| Registry operator | Batch uploads reach the real SFTP endpoints |
| Security reviewer | Host-key bypass cannot silently ship as the production default |
| Job maintainer | Clear env contract: verify on + known host key, or explicit local opt-out |

## Scope

### In scope (this release)

- Close CONFIG-004 for `jobs/sftp-gazette`, `jobs/sftp-icbc-report`, `jobs/sftp-nuans-report`
- Default host verification on; require known host identity when verification is on
- Keep explicit `SFTP_VERIFY_HOST=false` for local/dev only
- Unit coverage for fail-closed and opt-out paths

### Out of scope

- Rotating production host keys or OpenShift secret values (ops handoff)
- Furnishings / GCP SFTP clients (CONFIG-003)
- Changing batch business logic beyond connection trust

## Journeys

1. Verified connect requires host identity — see `features/config-004-sftp-verify-host-default.feature`
2. Missing host identity fails closed — same feature
3. Explicit local opt-out — same feature

## Non-functional requirements

- Accessibility: n/a (batch jobs)
- Privacy: no change to data classification; protects transfer integrity
- Fail closed: verification on + missing host identity must not connect

## Open questions

- [x] Opt-out mechanism: keep `SFTP_VERIFY_HOST=false` for local; default verify
- [ ] Ops confirms production secrets keep verification enabled and `SFTP_HOST_KEY` populated

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
