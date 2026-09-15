# PR evidence

## DEP-015 — furnishings flask-restplus → flask-restx (issue #34)

- Spec: `spec/spec.md`, `spec/features/dep-015-furnishings-restx.feature` (`@R-715.1`, `@R-715.2`)
- Plan: `spec/plan.md`
- Change: `gcp-jobs/furnishings/pyproject.toml` — `flask-restx (>=1.3.0,<2.0.0)` replaces `flask-restplus`
- Change: refreshed `gcp-jobs/furnishings/poetry.lock`
- Tests: `gcp-jobs/furnishings/tests/unit/test_dep_015_flask_restx.py`
- Residual: furnishings does not currently import restx APIs; lock-only consumer verification not run beyond poetry lock
