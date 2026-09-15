# Plan — Redact GCP auth / payment bearer logs (LOG-003–013)

> Architecture and delivery approach. Technology belongs here (not in `spec.md`).

## Summary

Sanitize DEBUG logging and add WARNING on auth failure across five queue `gcp_auth.py` modules, email-reminder fee lookup, and business-emailer event processing. Replace `finally: return` with a normal return so exceptions are not silently discarded.

## Architecture

```text
Authorization header → verify_gcp_jwt
  → id_token.verify_oauth2_token (unchanged)
  → DEBUG: config presence only (no token / claim)
  → on mismatch/exception: WARNING (non-PII) + return msg string
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| WARNING content | Exception type name / mismatch phrase | Avoid logging exception text that may embed token fragments |
| Return `msg` | Keep existing strings including claim email in mismatch msg | Preserve caller HTTP/error contract; only logs are redacted |
| emailer `ce.data` | Log type + dict keys | Enough for dispatch debugging without contact PII |
| Scope | One PR for #38–#47 + #57 | Same pattern; filer WARNING is Low but trivial alongside LOG-007 |

## Test approach

- Feature: `spec/features/log-003-013-redact-gcp-auth.feature` (`@R-38.1`–`@R-38.4`)
- Unit: extend digital-credentials `test_gcp_auth.py` with caplog assertions

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | *(agent-proposed — awaiting human)* | 2026-09-15 |
| Security (if required) | *(agent-proposed — awaiting human)* | 2026-09-15 |
