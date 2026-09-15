# Spec — Pin queue-services-common PyPI deps (DEP-008)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#13** — `[DEP-008] DEP-008` (High). Unconstrained shared queue library dependencies.

## Problem

The shared queue-services common library declares six production dependencies with no version constraints and no lock file. That library underpins multiple queue workers, so any install can silently pull a new major or incompatible release and propagate it across production consumers.

## Outcome

Each of the six dependencies carries an explicit minimum and/or compatible version bound. Reinstalls stay within those ranges until a maintainer deliberately widens or bumps the pins.

## Users & personas

| Persona | Goal |
| --- | --- |
| Platform engineer | Reproducible installs for shared queue common |
| Security reviewer | No unconstrained floating of third-party packages into queue workers |
| Maintainer | Clear, deliberate pin bumps when upgrades are intentional |

## Scope

### In scope (this release)

- Close DEP-008 for `queue_services/common/requirements.txt` (and matching `requirements/prod.txt` used by the local req-build flow)
- Conservative compatible pins for: aiohttp, attrs, python-dotenv, sentry-sdk[flask], asyncio-nats-client, asyncio-nats-streaming
- Unit assertion that each declared package retains a version specifier

### Out of scope

- Introducing a full lockfile for queue-services-common (separate supply-chain hardening)
- Migrating deprecated NATS Streaming clients to JetStream / nats-py
- Changing consumer queue service poetry locks

## Journeys

1. Requirements pins are version-constrained — see `features/dep-008-pin-queue-common-deps.feature`

## Non-functional requirements

- Compatible ranges preferred over exact pins where sibling services already float within a major
- Residual: deprecated NATS client packages remain in use (pinned, not replaced)

## Open questions

- [x] Pin style: minimum + upper-bound compatible ranges informed by sibling poetry.lock / requirements pins

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
