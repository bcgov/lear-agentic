# PR evidence

## LOG-001 — Redact OIDC JWT INFO log (issue #16)

- Spec: `spec/spec.md`, `spec/features/log-001-redact-jwt-oidc-info-log.feature` (`@R-08.1`, `@R-08.2`, `@R-08.3`)
- Plan: `spec/plan.md`
- Change: `legal-api/src/legal_api/resources/v2/business/business.py` — VALID account request INFO log uses only `accountId` + business identifier (no `preferred_username`, full `g.jwt_oidc_token_info`, or org dump)
- Tests: `legal-api/tests/unit/resources/v2/test_business.py` (`test_get_business_account_info_log_omits_jwt_oidc_pii`, `test_get_business_account_info_sets_account_id`, `test_get_business_account_info_omits_account_id_when_unmatched`)
- Residual: WARNING unauthorized paths still log `preferred_username` in `business.py` / `business_filings.py`; LOG-002+ DEBUG JWT dumps remain separate issues
