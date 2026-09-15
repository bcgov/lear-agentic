# Spec — Data-tool Postgres SSL mode (CONFIG-005)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#24** — `[CONFIG-005] PostgreSQL Connections Without SSL Enforcement — Data Tool` (Medium).

## Problem

Data-tool Prefect flows build three database connection strings (LEAR, COLIN migration extract, AUTH) over plain TCP with no transport encryption setting. Unlike Cloud SQL connector paths elsewhere, these flows can speak cleartext to Postgres unless the operator remembers to configure SSL outside the app.

## Outcome

Every data-tool Postgres connection string carries an explicit SSL mode. Non-local environments **require** encrypted transport by default. Local/dev may use a softer default so laptop databases without TLS still work. Operators can override the mode via configuration.

## Users & personas

| Persona | Goal |
| --- | --- |
| Migration operator | Flows reach the intended databases without MITM on the wire |
| Security reviewer | Application-level SSL mode is set, not left to listener luck |
| Local developer | Can still point at a TLS-less local Postgres with an explicit or local default |

## Scope

### In scope (this release)

- Append configurable `sslmode` to the three SQLAlchemy Postgres URIs in data-tool config
- Secure default (`require`) for non-local; softer default for local/dev
- Env override + sample documentation
- Unit coverage for defaults and override

### Out of scope

- Changing Oracle CPRD connection SSL (CONFIG-006)
- Rotating certificates or OpenShift secret values (ops)
- Migrating data-tool onto Cloud SQL connector

## Journeys

1. Non-local require — see `features/config-005-data-tool-pg-ssl.feature`
2. Local prefer — same feature
3. Explicit override — same feature

## Non-functional requirements

- Accessibility: n/a (batch / flows)
- Privacy: protects registry data in transit between flow workers and Postgres
- Fail closed (non-local): default requires TLS negotiation

## Open questions

- [x] Local default: `prefer` (attempt TLS, allow cleartext) vs `disable`
- [ ] Ops confirms deployed Postgres endpoints accept `sslmode=require`

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | | |
| BA | | |
| QA (acceptance ownership) | | |
