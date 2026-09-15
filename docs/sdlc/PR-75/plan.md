# Plan — Legal API HTTP security response headers (CONFIG-001)

> Architecture and delivery approach. Technology belongs here (not in `spec.md`).

## Summary

Extend the existing Flask `after_request` hook in `legal_api/__init__.py` so every response receives standard security headers via a small pure helper (`legal_api.utils.security_headers`). No Flask-Talisman dependency.

## Architecture

```text
Client → Legal API (Flask)
           └─ after_request: version headers (API, SCHEMAS)
           └─ after_request: apply_security_headers(...)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Mechanism | `after_request` + helper | Matches existing version-header pattern; no new deps |
| CSP | `default-src 'none'; frame-ancestors 'none'` | JSON/PDF API; HTML used only for PDF templates |
| HSTS | `max-age=31536000; includeSubDomains` | Standard long-lived HSTS signal |
| X-Frame-Options | `DENY` | Complement CSP frame-ancestors |
| Referrer-Policy | `no-referrer` | API responses should not leak path via Referer |
| Permissions-Policy | disable common powerful features | Defence in depth for any browser-handled response |

## Security & privacy

- Classification: unchanged (registry API)
- Finding: CONFIG-001 / CWE-16 / OWASP A05:2021
- Secrets: n/a

## Test approach

- Unit tests on `apply_security_headers` (no DB / full app required)
- Criterion tags `@R-06.1`–`@R-06.3` in feature + test docstrings
- Default integrity tier: CODEOWNERS on acceptance criteria

## Rollout

- Environments: all Legal API deployments on next release
- Migration / cutover: n/a (additive response headers)

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | *(agent-proposed — awaiting human)* | 2026-09-15 |
| Security (if required) | *(agent-proposed — awaiting human)* | 2026-09-15 |
