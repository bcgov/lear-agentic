# Spec — Legal API HTTP security response headers (CONFIG-001)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#3** — `[CONFIG-001] Missing HTTP Security Response Headers — Legal API` (High).

## Problem

Legal API responses carry internal version metadata but omit standard browser-facing security controls (framing protection, MIME sniffing protection, transport security signalling, content policy, referrer and permissions limits). Clients and intermediaries therefore lack the usual defence-in-depth signals expected for a public-sector registry API.

## Outcome

Every Legal API HTTP response includes the agreed security headers, while existing version identification headers remain intact. Callers continue to receive JSON (and PDF report downloads) without breakage from an overly browser-SPA-oriented content policy.

## Users & personas

| Persona | Goal |
| --- | --- |
| Registry client / browser | Responses refuse framing and MIME confusion; HSTS signalled |
| Security reviewer | CONFIG-001 / CWE-16 closed for Legal API responses |
| API maintainer | Lightweight header attachment; no new heavy middleware dependency |

## Scope

### In scope (this release)

- Close CONFIG-001 for Legal API application responses
- Set Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy
- Preserve existing `API` and `SCHEMAS` version headers
- Unit coverage that required headers are present and version headers survive

### Out of scope

- COLIN API missing headers (CONFIG-002 — separate issue)
- Changing TLS termination / OpenShift route HSTS configuration beyond response headers
- Flask-Talisman or other new heavy dependencies
- Reworking report HTML templates used only for PDF generation

## Journeys

1. Security headers on responses — see `features/config-001-legal-api-security-headers.feature`
2. Version headers preserved — same feature

## Non-functional requirements

- Accessibility: n/a (API headers)
- Privacy: no change to data classification; reduces referrer leakage via Referrer-Policy
- Compatibility: CSP must remain API-oriented (`default-src 'none'`) so JSON/PDF clients are unaffected

## Open questions

- [x] Does Legal API serve interactive HTML? No — JSON API; HTML is report-template input to PDF generation
- [x] Prefer Talisman vs after_request: after_request (no new dependency)

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
