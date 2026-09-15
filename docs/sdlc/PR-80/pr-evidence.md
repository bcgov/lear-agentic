# PR evidence

## DEP-004 — Pin business-schemas git dependency (issue #9)

- Spec: `spec/spec.md`, `spec/features/dep-004-pin-business-schemas.feature` (`@R-704.1`, `@R-704.2`)
- Plan: `spec/plan.md`
- Change: `colin-api/requirements.txt` — `git+https://github.com/bcgov/business-schemas.git@cf41a551b08cb51afd3e88bec0eab155dc856b24#egg=registry_schemas`
- SHA source: `git ls-remote https://github.com/bcgov/business-schemas.git HEAD` at remediation time
- Tests: `colin-api/tests/unit/security/test_dep_004_pin_business_schemas.py`
- Residual: maintainers must bump the SHA when intentional schema updates are required; dependency remains a git install (not a versioned package index artifact)
