# PR evidence

## DEP-011 / DEP-012 / DEP-016 — emailer LD + protobuf, bn protobuf (issues #30, #31, #35)

- Spec: `spec/spec.md`, `spec/features/dep-011-012-016-emailer-bn.feature` (`@R-711.1`, `@R-712.1`, `@R-716.1`)
- Plan: `spec/plan.md`
- Change: `queue_services/business-emailer/pyproject.toml` — `launchdarkly-server-sdk >=9.10.0,<10.0.0`; `protobuf >=4.25.1,<6.0.0` (lock: LD 9.17.0, protobuf 5.29.6)
- Change: `queue_services/business-emailer/src/business_emailer/services/flags.py` — Context + Files APIs (aligned with business-pay)
- Change: `queue_services/business-bn/pyproject.toml` — `protobuf >=4.25.1,<6.0.0` (lock: protobuf 4.25.9)
- Change: refreshed `poetry.lock` for emailer and bn
- Tests: `queue_services/business-emailer/tests/unit/test_dep_011_012_016_deps.py`
- Residual: full emailer/bn integration against live LD / gcp-queue not run here; emailer and bn locks resolve different protobuf minors within the shared range
