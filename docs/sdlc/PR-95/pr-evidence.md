# PR evidence

## GD-001 — Jinja2 xmlattr floor (issue #37)

- Spec: `spec/spec.md`, `spec/features/gd-001-colin-jinja2.feature` (`@R-37.1`)
- Plan: `spec/plan.md`
- Change: `colin-api/requirements.txt` — `Jinja2==3.1.4`, `MarkupSafe==2.1.5` (Flask==1.1.2 retained; full stack upgrade is DEP-001 / #6)
- Tests: `colin-api/pin_tests/test_gd001_jinja2_pin.py`
- Residual: no exhaustive `xmlattr` template audit; DEP-001 may re-pin the same Jinja2/MarkupSafe companions with Flask 2.3.3
