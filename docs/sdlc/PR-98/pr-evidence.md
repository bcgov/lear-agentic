# PR evidence

## VULN-006 — business-bn defusedxml for CRA BN Hub XML (issue #64)

- Spec: `spec/spec.md`, `spec/features/vuln-006-business-bn-defusedxml.feature` (`@R-64.1`, `@R-64.2`, `@R-64.3`)
- Plan: `spec/plan.md`
- Change: `queue_services/business-bn` processors import `defusedxml.ElementTree as Et`; `pyproject.toml` / `poetry.lock` add `defusedxml`
- Tests: `queue_services/business-bn/tests/test_vuln006_defusedxml.py` (outside `tests/unit/` to avoid `business_model` import via `unit/__init__.py`)

## Review receipt (checkpoint 3 — agent draft)

**Checked:** All four processor modules that called `Et.fromstring` now import defusedxml; unit tests cover `@R-64.1`–`@R-64.3`.

**Could not check:** Full business-bn poetry install + existing processor integration suite against live CRA BN Hub.

**Residual risk:** Test modules that build fixtures with stdlib ElementTree remain unchanged (trusted test XML only). Correction processor has no direct `fromstring` and is unchanged.
