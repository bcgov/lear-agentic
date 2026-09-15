# Spec — Configurable CORS origins (CONFIG-007 / CONFIG-008)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#26** (`[CONFIG-007] CORS Wildcard Origin Configured — Legal API`) and
**#27** (`[CONFIG-008] CORS Wildcard Origin Configured — COLIN API`) — Medium.

## Problem

Legal API and COLIN API emit `Access-Control-Allow-Origin: *` on CORS preflight and
(for Legal API) auth-error / redirect paths. Any browser origin can read cross-origin
responses, widening information-leakage risk (CWE-942).

## Outcome

Both APIs use a configurable Origin allowlist from the environment (for example
`CORS_ORIGINS`). Unlisted or missing Origins fail closed (no allow-origin header).
Wildcard `*` is never echoed, including if mis-set in configuration.

## Users & personas

| Persona | Goal |
| --- | --- |
| Registry browser client | Cross-origin calls work only from approved front-end Origins |
| Security reviewer | CONFIG-007 / CONFIG-008 closed for named call sites |
| Operator | Set allowlist per environment without code changes |

## Scope

### In scope (this release)

- Legal API: cors_preflight decorator, JWT auth error handler, redirect/OPTIONS access-control headers
- COLIN API: cors_preflight decorator
- `CORS_ORIGINS` config on both services (comma-separated Origins)
- Fail closed when empty; echo only exact listed Origins; ignore `*` in config
- Unit coverage for allowlist behaviour (`@R-26.1+`, `@R-27.1+`)

### Out of scope

- Rewiring every `flask_cors` / flask-restx `crossdomain(origin='*')` resource decorator (residual — document)
- Changing WebSocket `WS_ALLOWED_ORIGINS` behaviour
- Self-merge / production deploy of allowlist values

## Journeys

1. Fail closed / echo listed Origins — see `features/config-007-008-cors-origins.feature`

## Non-functional requirements

- Compatibility: browser clients must receive the concrete Origin they sent when allowlisted (cannot use `*` with credentials)
- Privacy: reduces cross-origin readability of API error and preflight responses

## Open questions

- [x] Fail closed vs default public Origins? Fail closed (empty allowlist ⇒ no header)
- [x] One PR for #26 and #27? Yes

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
