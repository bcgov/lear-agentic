# Spec — Colin API dependency lockfile (DEP-003)

## Feature proposal
Issue **#8** — DEP-003: colin-api has no lockfile for transitive dependencies.

## Outcome
A committed `requirements.lock` captures resolved transitive versions for PyPI pins so installs are reproducible (with documented exceptions for Oracle and git deps).

## Sign-off
| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
