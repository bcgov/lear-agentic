# Spec — SAST integration and coverage fail-under (TEST-001 / TEST-002)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#20** (`[TEST-001]`) and **#21** (`[TEST-002]`) — High severity testing / security-assurance findings.

## Problem

The delivery pipeline does not enforce static application security scanning as a first-class check, and unit coverage can regress silently because no minimum coverage floor is configured for the primary registry APIs.

## Outcome

1. Pull requests and the default branch run committed SAST that covers at least the Legal API and COLIN API Python trees (alongside any organization-level scanning already enabled).
2. Legal API and COLIN API test runs fail when coverage drops below an explicit, non-zero floor calibrated below currently observed coverage so the gate is meaningful without always failing.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | SAST evidence on every PR; TEST-001 closed |
| Maintainer | Coverage cannot drift to zero unnoticed; TEST-002 closed |
| Developer | Thresholds low enough that legitimate work is not blocked day one |

## Scope

### In scope (this release)

- Close TEST-001: committed CodeQL analysis workflow plus lightweight Bandit for `legal-api` and `colin-api`
- Document existing organization/default CodeQL setup if already analyzing PRs
- Close TEST-002: `--cov-fail-under` (or equivalent) for Legal API and COLIN API, plus Codecov project targets for those flags
- Spec criteria `@R-20.1+` / `@R-21.1+`

### Out of scope

- Raising coverage to an aspirational 80%+ across all components
- Fixing every Medium Bandit finding already tracked as separate VULN tickets
- Disabling existing CI workflows
- Self-merge / production deploy

## Journeys

1. SAST on PRs — see `features/test-001-002-sast-coverage.feature`
2. Coverage floor — same feature

## Non-functional requirements

- SAST High findings fail the Bandit job; Medium findings may be reported elsewhere without blocking this gate
- Coverage floors sit below Codecov-observed flag totals so CI stays green while still non-zero

## Open questions

- [x] CodeQL already on PRs via default setup? Yes — document and still commit `codeql-analysis.yml` + Bandit
- [x] Threshold values? legal-api 70 (flag ~78%); colin-api 25 (flag ~31%)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
