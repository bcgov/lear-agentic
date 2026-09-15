# Spec — LEAR furnishings SFTP host-key verification (CONFIG-003)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#2** — `[CONFIG-003] SSH Host Key Validation Unconditionally Bypassed via AutoAddPolicy — GCP Furnishings SFTP` (Critical).

## Problem

Furnishings jobs transfer regulated notices to external SFTP endpoints (BCLaws, BCMail+). Today those connections accept any server identity on first contact, so an attacker on the network path can impersonate the destination and intercept or alter filings and notices without detection.

## Outcome

Production furnishings SFTP connections **reject unknown server identities** and only succeed when the expected host identity is configured. Operators can still disable verification **explicitly** for local/test harnesses; that path is never the default.

## Users & personas

| Persona | Goal |
| --- | --- |
| Registry operator | Notices reach the real BCLaws / BCMail+ endpoints |
| Security reviewer | MITM via silent host-key acceptance is closed |
| Furnishings maintainer | Clear config for known host keys; tests still run |

## Scope

### In scope (this release)

- Close CONFIG-003 for GCP furnishings SFTP connection establishment
- Require configured host identity for verified connections
- Keep an explicit opt-out for automated unit tests / local fixtures
- Document residual risk if vault secrets are not yet populated

### Out of scope

- Rotating production host keys or vault secret values (ops handoff)
- Reworking legacy `jobs/sftp-*` clients (separate findings if any)
- Changing furnishings business logic beyond connection trust

## Journeys

1. Verified production connect — see `features/config-003-sftp-host-key.feature`
2. Explicit test opt-out — same feature (negative / harness path)

## Non-functional requirements

- Accessibility: n/a (batch job)
- Privacy: no change to data classification; protects transfer integrity
- Fail closed: missing host identity with verification enabled must not connect

## Open questions

- [x] Host key material source: environment / vault secrets per endpoint (BCLaws, BCMail+)
- [ ] Ops confirms vault keys populated before promoting to prod

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
