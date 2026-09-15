# PR evidence

## SECRET-001 — Ephemeral JWT test keys (issue #18)

- Spec: `spec/features/secret-001-ephemeral-jwt-test-keys.feature` (`@R-18.1`, `@R-18.2`)
- Change: `legal_api/jwt_oidc_test_keys.py` + `business_account/jwt_oidc_test_keys.py`; TestConfigs load process-local material
- Residual: old key still in git history; ensure JWT_OIDC_TEST_MODE never enabled outside tests
