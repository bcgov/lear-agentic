# PR evidence

## DEP-008 — Pin queue-services-common PyPI deps (issue #13)

- Spec: `spec/spec.md`, `spec/features/dep-008-pin-queue-common-deps.feature` (`@R-708.1`, `@R-708.2`)
- Plan: `spec/plan.md`
- Change: `queue_services/common/requirements.txt` (+ aligned `requirements/prod.txt`)
  - `aiohttp>=3.13.3,<4.0.0` (sibling queue poetry.lock ~3.13.5)
  - `attrs>=23.1.0,<27.0.0` (legal-api / queue locks 23.x–26.x)
  - `python-dotenv>=1.1.0,<2.0.0` (queue poetry constraints)
  - `sentry-sdk[flask]>=1.20.0,<3.0.0` (business-registry-model pin floor)
  - `asyncio-nats-client>=0.11.4,<0.12.0` (data-tool pin)
  - `asyncio-nats-streaming==0.4.0` (data-tool / latest stable)
- Tests: `queue_services/common/tests/unit/test_dep_008_pin_requirements.py`
- Residual: no full lockfile yet; deprecated NATS Streaming clients remain (pinned only, not migrated)
