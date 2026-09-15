# Spec — COLIN API HTTP security response headers (CONFIG-002)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#4** — `[CONFIG-002] Missing HTTP Security Response Headers — COLIN API` (High).

## Problem

COLIN API responses currently advertise only an API version header. They do not carry standard HTTP security headers (HSTS, framing controls, content-type sniffing protection, referrer policy, permissions policy, or a content security policy). Clients and intermediaries therefore lack defence-in-depth controls on responses that carry JWT-authenticated Oracle CPRD data.

## Outcome

Every COLIN API HTTP response includes the same security header set used by Legal API for a JSON API, while continuing to expose the existing API version header unchanged.

## Users & personas

| Persona | Goal |
| --- | --- |
| Registry integrator | JSON responses remain usable; headers do not break clients |
| Security reviewer | CONFIG-002 / CWE-16 closed for COLIN API responses |
| COLIN API maintainer | One shared, documented header set aligned with Legal API |

## Scope

### In scope (this release)

- Close CONFIG-002 for COLIN API application factory responses
- Apply HSTS, X-Frame-Options DENY, X-Content-Type-Options nosniff, Referrer-Policy, Permissions-Policy, and an API-oriented CSP
- Preserve the existing `API` version response header
- Spec acceptance criteria `@R-07.1`–`@R-07.3` and unit coverage

### Out of scope

- CONFIG-001 (Legal API headers — separate issue/PR)
- CONFIG-008 (CORS wildcard origin)
- Changing TLS termination or OpenShift route configuration
- Browser SPA CSP allowances (this service is a JSON API)

## Journeys

1. Security headers on every response — see `features/config-002-colin-api-security-headers.feature`
2. Version header preserved alongside security headers — same feature
3. API-oriented CSP — same feature

## Non-functional requirements

- Accessibility: n/a (JSON API)
- Privacy: no change to data classification; reduces browser misuse risk of API responses
- Compatibility: additive response headers only; no request or body contract change

## Open questions

- [x] Header set: mirror Legal API / CONFIG-001 JSON API defaults (`@R-07.1+`)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
