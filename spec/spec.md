# Spec — Pin internal git dependencies (DEP-005)

## Feature proposal
GitHub issue **#10** — DEP-005: internal libraries sourced from `@main` without commit SHA.

## Problem
Modern components pull internal packages from GitHub `@main`, so every reinstall can silently change production code.

## Outcome
Git dependency URLs reference immutable commit SHAs for `bcgov/lear` and `bcgov/sbc-connect-common` packages.

## Scope
### In scope
- Replace `@main` with commit SHAs across pyproject.toml files in this repository that use those hosts

### Out of scope
- Migrating to published package versions / path deps (follow-up modernization)

## Journeys
1. Reproducible installs — `features/dep-005-pin-git-main.feature`

## Sign-off
| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
