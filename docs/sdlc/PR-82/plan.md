# Plan — DEP-008 pin queue-services-common deps

> Architecture and delivery approach for issue #13.

## Summary

Replace bare package names in `queue_services/common/requirements.txt` (and matching `requirements/prod.txt`) with conservative compatible version ranges grounded in sibling lockfiles and known in-repo pins. Add a unit test that every required package line includes a version specifier.

## Architecture

```text
queue_services/common/requirements.txt
  → aiohttp / attrs / python-dotenv / sentry-sdk[flask] / nats clients
  → each line: name + (>= and/or ==) version constraint
setup.py install_requires
  → reads requirements.txt
Makefile build-req
  → installs requirements/prod.txt (kept in sync)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Pin style | Compatible ranges (`>=x,<y`) except streaming client exact | Matches sibling poetry floors; avoids overnight major jumps |
| Version floors | Sibling locks / data-tool / model pins | aiohttp ~3.13.x, attrs ≥23.1, dotenv 1.x, sentry ≥1.20, nats 0.11.4 / 0.4.0 |
| prod.txt | Same pins as requirements.txt | Makefile `build-req` installs prod.txt; keep source lists aligned |
| Lockfile | Out of scope | Finding asks for version constraints; full lock is separate work |

## Security & privacy

- Classification: supply-chain / reproducible build (CWE-1357)
- Residual: NATS Streaming stack remains deprecated/unmaintained (pinned only); sentry major 2.x allowed within `<3`

## Test approach

- Unit: parse `requirements.txt`; assert each of the six packages has a non-empty version specifier
- Acceptance: Gherkin `@R-708.1`, `@R-708.2` in `spec/features/dep-008-pin-queue-common-deps.feature`

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
