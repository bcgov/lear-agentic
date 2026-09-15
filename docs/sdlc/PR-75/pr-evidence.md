# PR evidence

## CONFIG-001 — Legal API HTTP security response headers (issue #3)

- Spec: `spec/spec.md`, `spec/features/config-001-legal-api-security-headers.feature` (`@R-06.1`, `@R-06.2`, `@R-06.3`)
- Plan: `spec/plan.md`
- Change: `legal-api/src/legal_api/utils/security_headers.py` — `apply_security_headers` + API-oriented CSP
- Change: `legal-api/src/legal_api/__init__.py` — `after_request` applies security headers after version headers
- Tests: `legal-api/tests/unit/utils/test_security_headers.py`
- Residual: COLIN API headers remain CONFIG-002; platform/route-level HSTS not changed by this PR
