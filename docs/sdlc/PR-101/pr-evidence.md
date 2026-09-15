# PR evidence

## DEP-013 / DEP-014 — NATS clients data-tool + queue-common (issues #32, #33)

- Spec: `spec/spec.md`, `spec/features/dep-013-014-nats.feature` (`@R-713.1`, `@R-714.1`, `@R-714.2`)
- Plan: `spec/plan.md`
- Change: `data-tool/requirements.txt` — remove unused `asyncio-nats-client` / `asyncio-nats-streaming`; add `nats-py>=2.9.0,<3.0.0`
- Change: `queue_services/common/requirements.txt` (+ `requirements/prod.txt`) — pin NATS deps (aligned with DEP-008 / PR #82) and document deprecation / JetStream residual
- Tests: `queue_services/common/tests/unit/test_dep_013_014_nats.py`
- Residual: queue-common STAN workers still require EOL `asyncio-nats-streaming` until JetStream migration; if PR #82 merges first, pin hunks may already be present and this PR’s unique value is the residual documentation + data-tool swap
