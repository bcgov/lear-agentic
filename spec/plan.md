# Plan — DEP-013 / DEP-014 NATS residual

## Summary

In data-tool, remove unused `asyncio-nats-client` / `asyncio-nats-streaming` and add `nats-py>=2.9.0,<3.0.0`. In queue-common, apply the same compatible pins as DEP-008 (`asyncio-nats-client>=0.11.4,<0.12.0`, `asyncio-nats-streaming==0.4.0`) plus deprecation comments documenting that STAN usage blocks a minimal nats-py migration.

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| data-tool | swap to nats-py | No in-tree imports of deprecated clients |
| queue-common | pin + residual | STAN APIs in entity_queue_common are not drop-in with nats-py |
| Pin values | match DEP-008 / #82 | Avoid divergent ranges across open PRs |

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
