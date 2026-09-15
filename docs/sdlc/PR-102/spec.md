# Spec — furnishings flask-restplus → flask-restx (DEP-015)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#34** (`DEP-015`) (Medium). The furnishings job declares an unmaintained REST helper package that was renamed/succeeded by a maintained fork.

## Problem

Unmaintained API helper packages receive no security patches. furnishings still names the deprecated package even though no in-tree Python imports reference it.

## Outcome

furnishings declares the maintained successor package and no longer lists the deprecated one.

## Scope

### In scope

- Replace flask-restplus with flask-restx in `gcp-jobs/furnishings/pyproject.toml`
- Refresh poetry.lock
- Spec `@R-715.1`, `@R-715.2`

### Out of scope

- Introducing new REST namespaces in furnishings (none currently import either package)
- Migrating other components still mentioning restplus historically

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
