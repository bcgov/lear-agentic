# PR evidence

## CONFIG-007 — Legal API CORS origins (issue #26)

- Spec: `spec/spec.md`, `spec/features/config-007-008-cors-origins.feature` (`@R-26.1`, `@R-26.2`, `@R-26.3`)
- Plan: `spec/plan.md`
- Change: `legal-api/src/legal_api/utils/cors.py` — allowlist parse/resolve/apply; rejects `*`
- Change: `legal-api/src/legal_api/utils/util.py` — `cors_preflight` uses allowlist (no `*`)
- Change: `legal-api/src/legal_api/__init__.py` — JWT auth error handler echoes listed Origin only
- Change: `legal-api/src/legal_api/resources/endpoints.py` — redirect/OPTIONS access-control uses allowlist
- Change: `legal-api/src/legal_api/config.py` — `CORS_ORIGINS` from env (default empty / fail closed)
- Tests: `legal-api/tests/unit/utils/test_util_cors.py`
- Residual: many routes still use `flask_cors.cross_origin()` defaults; follow-up if those still emit `*`

## CONFIG-008 — COLIN API CORS origins (issue #27)

- Spec criteria: `@R-27.1`, `@R-27.2`, `@R-27.3`
- Change: `colin-api/src/colin_api/utils/cors.py` — same allowlist helper
- Change: `colin-api/src/colin_api/utils/util.py` — `cors_preflight` uses allowlist (no `*`)
- Change: `colin-api/src/colin_api/config.py` — `CORS_ORIGINS` from env
- Tests: `colin-api/tests/unit/utils/test_util_cors.py`
- Residual: flask-restx `@cors.crossdomain(origin='*')` on resource methods still present; out of named finding path for this PR
