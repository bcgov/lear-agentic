# PR evidence

## CONFIG-002 — COLIN API HTTP security headers (issue #4)

- Spec: `spec/spec.md`, `spec/features/config-002-colin-api-security-headers.feature` (`@R-07.1`, `@R-07.2`, `@R-07.3`)
- Plan: `spec/plan.md`
- Change: `colin-api/src/colin_api/utils/security_headers.py` defines the Legal API–aligned header set and `apply_security_headers`
- Change: `colin-api/src/colin_api/__init__.py` applies headers in the existing `after_request` hook after setting `API`
- Tests: `colin-api/tests/test_config002_security_headers.py`
- Residual: HSTS effectiveness depends on HTTPS client paths / edge TLS; CORS wildcard remains CONFIG-008
