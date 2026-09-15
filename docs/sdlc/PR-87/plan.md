# Plan — DEP-001 COLIN API Flask / Werkzeug upgrade

> Architecture and delivery approach for issue #6.

## Summary

Upgrade `colin-api` from Flask 1.1.2 / Werkzeug 1.0.1 / flask-restx 0.3.0 to an intermediate supported-enough stack: Flask 2.3.3, Werkzeug 2.3.8, flask-restx 1.3.0, plus Jinja2 / MarkupSafe / itsdangerous / click / blinker pins required by Flask 2.3. Apply the smallest application fixes so the factory still boots (`ENV` on config, Oracle pool on `g`, Click CLI instead of Flask-Script). Leave Flask 3.x for a follow-up because `flask-jwt-oidc==0.3.0` still imports removed request-context stack APIs.

## Architecture

```text
colin-api/requirements.txt
  Flask==2.3.3  Werkzeug==2.3.8  flask-restx==1.3.0
  Jinja2 / MarkupSafe / itsdangerous / click / blinker companions
src/colin_api/config.py          → ENV on Dev/Test/Prod
src/colin_api/services/flags.py  → app.config['ENV'] (not app.env)
src/colin_api/resources/db.py    → flask.g instead of _app_ctx_stack
manage.py                        → Click group (drop Flask-Script)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Target major | Flask 2.3.3 (not 3.x) | Clears cited CVEs; jwt-oidc 0.3 blocks Flask 3 without separate modernization |
| flask-restx | 1.3.0 (from 0.3.0) | Required companion; 0.3.0 is not a viable pin on Flask 2.3 |
| Flask-Script | Remove | Broken on Flask 2.3 (`flask._compat` removed); manage CLI → Click |
| Oracle context | `g` + `has_app_context` | Replaces deprecated `_app_ctx_stack` used by the pool helper |

## Security & privacy

- Classification: outdated dependency / CWE-1104; advisories CVE-2023-30861, CVE-2023-25577
- Residual: Flask 2.3.x is not the current stable line; Flask 3 + jwt-oidc bump still needed; full Oracle-backed API regression not run in this agent environment

## Test approach

- Unit: parse `requirements.txt` for minimum pins (`@R-701.1`–`@R-701.3`); assert Flask-Script absent (`@R-701.4`)
- Smoke (local): create_app + `/ops/healthz`, `/ops/readyz`, `/api/v1/meta/info`, swagger.json with stubbed Oracle where needed
- Acceptance: Gherkin `@R-701.1`–`@R-701.4`

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
