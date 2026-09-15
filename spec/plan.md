# Plan — CONFIG-007 / CONFIG-008 CORS origin allowlist

> Architecture and delivery approach for issues #26 and #27.

## Summary

Replace hardcoded `Access-Control-Allow-Origin: *` on Legal API and COLIN API
cors_preflight (and Legal API auth-error / redirect handlers) with a shared
allowlist helper driven by `CORS_ORIGINS`. Fail closed when unset; echo only
exact matches; never honour `*` from config.

## Architecture

```text
CORS_ORIGINS env (comma-separated)
        │
        ▼
 legal_api.utils.cors / colin_api.utils.cors
   parse → allowlist (drops *)
   resolve(request Origin) → echo or None
        │
        ├── legal_api.utils.util.cors_preflight
        ├── legal_api JWT auth error handler
        ├── legal_api endpoints redirect OPTIONS
        └── colin_api.utils.util.cors_preflight
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Config key | `CORS_ORIGINS` | Explicit, matches remediation brief |
| Empty allowlist | Omit header | Fail closed |
| Match rule | Exact Origin string | Avoid partial/substring bypass |
| Wildcard in env | Ignored | Prevents accidental reopen of `*` |
| Scope | Named finding paths | Matches RA locations; residual flask_cors/crossdomain noted |

## Security & privacy

- Classification: CONFIG-007 / CONFIG-008 (CWE-942)
- Residual: Legal API `@cross_origin()` and COLIN `@cors.crossdomain(origin='*')` on many resources still may emit `*` on non-preflight responses until a follow-up

## Test approach

- Acceptance: Gherkin `@R-26.1`–`@R-26.3`, `@R-27.1`–`@R-27.3`
- Unit: allowlist helper + source assertions that hardcoded `*` call sites are gone
- Local: pytest on updated `test_util_cors.py` for both APIs

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | *(agent-proposed — awaiting human)* | 2026-09-15 |
