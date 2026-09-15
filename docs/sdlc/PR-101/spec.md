# Spec — NATS client remediation (DEP-013 / DEP-014)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#32** (`DEP-013`) and **#33** (`DEP-014`) (Medium). data-tool and queue-services-common still declare deprecated NATS client libraries (and queue-common previously left them unpinned).

## Problem

Unmaintained messaging clients create supply-chain risk. data-tool listed deprecated clients with no in-tree imports. queue-common still needs those clients for NATS Streaming workers, so a drop-in nats-py swap is not feasible without a JetStream rewrite.

## Outcome

data-tool declares maintained `nats-py` and drops unused deprecated clients. queue-common keeps pinned deprecated clients (coordinated with DEP-008 / PR #82) and documents the JetStream residual explicitly.

## Scope

### In scope

- data-tool: replace unused `asyncio-nats-*` with `nats-py` range
- queue-common: pin NATS deps (same ranges as DEP-008) + deprecation residual comments
- Spec `@R-713.1`, `@R-714.1`, `@R-714.2`

### Out of scope

- Rewriting `entity_queue_common` STAN workers to JetStream / nats-py
- Removing NATS Streaming from production queue topology

## Non-functional requirements

- Coordinate pins with DEP-008 / PR #82 to avoid conflicting ranges
- Residual: queue-common remains on EOL Streaming clients until JetStream migration

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
