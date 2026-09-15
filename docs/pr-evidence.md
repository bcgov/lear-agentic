# PR evidence

## LOG-002 — Redact user JWT DEBUG logs (issue #17)

- Spec: `spec/spec.md`, `spec/features/log-002-redact-user-jwt-debug-logs.feature` (`@R-09.1`, `@R-09.2`, `@R-09.3`)
- Plan: `spec/plan.md`
- Change: `python/common/business-registry-model/src/business_model/models/user.py` — DEBUG logs token presence / internal `user.id` only; no token dict or User column dump
- Tests: `python/common/business-registry-model/tests/models/test_user.py` (`test_create_from_jwt_token_debug_logs_omit_pii`, `test_get_or_create_user_by_jwt_debug_logs_omit_pii`)
- Residual: LOG-001 (legal-api INFO OIDC dump) and other LOG-* JWT DEBUG findings remain on their issues

## Review receipt (checkpoint 3)

**Checked:** `@R-09.1`–`@R-09.3` implemented in `user.py`; unit tests assert forbidden claim values absent from DEBUG.

**Could not check:** Full `business-registry-model` pytest suite may require Docker/testcontainers locally.

**Residual risk:** Other services may still log JWT/OIDC material (tracked under LOG-001 / LOG-003+).

- Reviewer: _______________ Date: _______________
