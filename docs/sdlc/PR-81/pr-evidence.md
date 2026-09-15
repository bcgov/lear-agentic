# PR evidence

## GD-002 / GD-003 — COLIN API ecdsa + gunicorn pins (issues #14, #15)

- Spec: `spec/spec.md`, `spec/features/gd-002-003-ecdsa-gunicorn.feature` (`@R-14.1`, `@R-15.1`)
- Plan: `spec/plan.md`
- Change: `colin-api/requirements.txt` — `ecdsa==0.19.1`, `gunicorn==23.0.0`
- Change: `colin-api/requirements/prod.txt` — `ecdsa>=0.19.0`, `gunicorn>=23.0.0` so `make build-req` does not re-freeze vulnerable versions
- Tests: `colin-api/tests/test_gd002_003_dependency_pins.py` (parse freeze; assert pin floors / exact pins)
- Residual: `python-jose==3.2.0` may still declare an older ecdsa transitive preference — mitigated by the direct pin; full COLIN API / container smoke under Gunicorn 23 was **not** run in this PR
