# Spec — business-emailer / business-bn LD + protobuf (DEP-011 / DEP-012 / DEP-016)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#30** (`DEP-011`), **#31** (`DEP-012`), and **#35** (`DEP-016`) (Medium). business-emailer lags the platform LaunchDarkly major line and pins an obsolete protobuf series; business-bn hard-caps protobuf below 3.20 and blocks upgrades.

## Problem

Feature-flag evaluation in emailer still depends on an SDK two majors behind siblings. Both emailer and business-bn constrain Protocol Buffers to aging 3.x bands that conflict with modern grpc/gcp-queue transitive expectations.

## Outcome

emailer declares LaunchDarkly ≥ 9.10 with Context-compatible flag wiring. emailer and business-bn relax protobuf to a modern compatible range that admits 4.x/5.x while retaining an explicit upper bound.

## Users & personas

| Persona | Goal |
| --- | --- |
| Security reviewer | DEP-011 / DEP-012 / DEP-016 closed with evidence |
| Queue maintainer | Flag evaluation still works; poetry resolves protobuf without the old ceilings |
| Platform engineer | emailer LD pin matches legal-api / business-bn / furnishings floor |

## Scope

### In scope

- Raise emailer LaunchDarkly constraint to ≥ 9.10 and adapt flags helper to public Files/Context APIs
- Relax emailer and business-bn protobuf constraints to `>=4.25.1,<6.0.0`
- Refresh poetry locks for those packages
- Spec `@R-711.1`, `@R-712.1`, `@R-716.1`

### Out of scope

- Migrating other services still on LD 7.x (colin-api, digital-credentials copy of private FileDataSource)
- Forcing protobuf 5.x exact pin
- Full emailer integration suite against live LaunchDarkly

## Journeys

1. LD floor + Context API — `features/dep-011-012-016-emailer-bn.feature`
2. Protobuf ranges relaxed — same feature

## Non-functional requirements

- Align with platform LD ≥ 9.10 floor
- Residual: lock refresh may still prefer different 4.x/5.x minors across services; CI poetry install not fully executed against live GCP queue here

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
