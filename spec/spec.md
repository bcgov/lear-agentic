# Spec — Ephemeral CI/local test DB credentials (SECRET-007 / SECRET-008)

## Feature proposal
Issues **#61** (SECRET-007) and **#62** (SECRET-008).

## Outcome
- Colin API CI uses a per-run ephemeral Postgres password (not literal `postgres`).
- sql-versioning tests source DB URL from env with a clearly labeled test-only default.

## Sign-off
| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
