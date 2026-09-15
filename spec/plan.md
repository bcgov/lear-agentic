# Plan — CONFIG-002 COLIN API security headers

> Architecture and delivery approach for issue #4.

## Summary

Add a small `security_headers` helper (same values as Legal API) and invoke it from the existing Flask `after_request` hook after setting the `API` version header so every response gains defence-in-depth headers without clearing existing ones.

## Architecture

```text
Client
  → COLIN API (Flask)
      → after_request: set API version header
      → after_request: apply_security_headers(response)
  → Response with version + security headers
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Header set | Match Legal API CONFIG-001 | Consistent registry API posture; issue requires parity |
| CSP | `default-src 'none'; frame-ancestors 'none'` | JSON API; not a browser app |
| Application point | Existing `after_request` | Single place; preserves current version header behaviour |
| Helper module | `colin_api.utils.security_headers` | Keeps factory thin; unit-testable without full app |

## Security & privacy

- Classification: unchanged (JWT + Oracle CPRD data paths)
- Residual: HSTS is most effective when clients use HTTPS end-to-end; edge TLS still required
- Secrets: none added

## Test approach

- Unit: header presence; version header preservation; CSP API-oriented (`@R-07.1`–`@R-07.3`)
- Acceptance: Gherkin in `spec/features/config-002-colin-api-security-headers.feature`
- Provenance header on new unit test file

## Rollout

1. Merge code (human checkpoint 3) — no self-merge
2. Deploy COLIN API; confirm response headers on a health/ops or authenticated route

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
