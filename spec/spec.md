# Spec — Pin colin-api business-schemas (DEP-004)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#9** — `[DEP-004] DEP-004` (High). Unpinned git dependency for registry schemas.

## Problem

COLIN API installs shared registry schemas from a git repository URL with no branch, tag, or commit. Any new commit on that repository’s default branch is adopted on the next install, so builds are not reproducible and supply-chain changes land without a deliberate bump.

## Outcome

The registry schemas dependency is pinned to an explicit commit identity. Reinstalls resolve the same revision until a maintainer intentionally updates the pin.

## Users & personas

| Persona | Goal |
| --- | --- |
| Platform engineer | Reproducible COLIN API installs |
| Security reviewer | No silent floating of third-party (internal) schema code |
| Maintainer | Clear, deliberate pin bumps when schemas change |

## Scope

### In scope (this release)

- Close DEP-004 for `colin-api` requirements declaration of registry schemas
- Pin to a specific commit of the schemas repository default branch tip at remediation time
- Unit assertion that the pin format remains a full commit SHA

### Out of scope

- Publishing registry schemas to an artifact index / replacing git install with a versioned package
- Pinning other colin-api dependencies (separate DEP findings)
- Changing schema content itself

## Journeys

1. Requirements pin is commit-SHA based — see `features/dep-004-pin-business-schemas.feature`

## Non-functional requirements

- Reproducible installs for the schemas dependency
- Residual: pin age — maintainers must bump SHA when intentional schema updates are needed

## Open questions

- [x] Pin form: git URL `@<sha>#egg=registry_schemas` (matches existing install style)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
