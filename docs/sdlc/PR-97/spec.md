# Spec — Non-zero test coverage for data-tool and ETL jobs (TEST-003)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#51** — `[TEST-003] Data Tool and ETL Batch Jobs have zero test coverage` (Medium).

## Problem

The rapid assessment found data-tool and ETL batch jobs lacked automated tests / test configuration, so regressions and security fixes could ship without any executable check.

## Outcome

Data-tool and the cited ETL job areas have a minimal pytest skeleton with at least one assertion each so coverage is non-zero. This does **not** claim full functional coverage.

## Scope

### In scope

- data-tool smoke (`@R-51.1`)
- SFTP ETL smokes for gazette / ICBC / NUANS (`@R-51.2`)
- colin-extract-refresh and dbc-message-sender skeletons (`@R-51.3`)

### Out of scope

- Full end-to-end Prefect / Oracle / live SFTP coverage
- correction-ben-statement notebooks
- Claiming branch / line coverage targets beyond non-zero

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA | local-agent | 2026-09-15 |
