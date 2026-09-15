# Spec — Redact GCP auth / payment bearer logs (LOG-003–013)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issues **#38–#47** (Medium LOG-003–012) and **#57** (Low LOG-013) — stop logging bearer tokens / full JWT claims at DEBUG, and emit WARNING on auth failures instead of silent `finally: return`.

## Problem

Several queue workers verify inbound GCP OAuth JWTs by logging the raw Authorization header and the full decoded claim dictionary at DEBUG. The email-reminder job also logs the payment-service bearer token before fee lookup. Separately, auth failures are captured into a return string without a WARNING, and most workers use `finally: return` which silences secondary exceptions. If DEBUG is enabled (or failures go unaudited), credentials and identity PII reach log aggregators and failed probes leave no trail (CWE-532 / CWE-778).

## Outcome

- No DEBUG (or other) log line contains a bearer token or full JWT claim dump.
- Email event processing DEBUG logs correlation fields (event type / data keys) only — not the full payload.
- Auth verification failures emit WARNING with non-PII context (exception type or mismatch reason).
- Auth helpers return the existing error string without a silent `finally: return`.

## Users & personas

| Persona | Goal |
| --- | --- |
| Operator / SRE | DEBUG still useful; WARNING on auth failure for audit |
| Security reviewer | LOG-003–013 closed for these paths |
| Queue worker | Auth behaviour unchanged for callers of `verify_gcp_jwt` |

## Scope

### In scope (this release)

- `gcp_auth.py` in business-bn, digital-credentials, emailer, filer, pay
- email-reminder `get_ar_fee` token DEBUG
- business-emailer `process_email` full `ce.data` DEBUG
- WARNING on verification / service-account mismatch failures
- Remove `finally: return` anti-pattern where present
- Unit coverage that forbidden secrets do not appear in DEBUG / WARNING

### Out of scope

- LOG-001 / LOG-002 (already separate)
- Broader emailer notification processors that still dump email_msg at DEBUG
- Changing auth success/failure HTTP behaviour beyond logging

## Journeys

1. GCP JWT verify without credential dumps — see `features/log-003-013-redact-gcp-auth.feature`
2. Auth failure WARNING without silent swallow — same feature
3. Email-reminder fee lookup without token in DEBUG — same feature

## Non-functional requirements

- Privacy: credential / identity-pii / contact-pii must not appear in these DEBUG lines
- Behaviour: returned auth error strings unchanged for callers

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | *(agent-proposed — awaiting human)* | 2026-09-15 |
| BA | *(agent-proposed — awaiting human)* | 2026-09-15 |
| QA (acceptance ownership) | *(agent-proposed — awaiting human)* | 2026-09-15 |
