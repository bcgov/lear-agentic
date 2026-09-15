# PR evidence

## DEP-001 — COLIN API Flask / Werkzeug upgrade (issue #6)

- Spec: `spec/spec.md`, `spec/features/dep-001-colin-flask-upgrade.feature` (`@R-701.1`–`@R-701.4`)
- Plan: `spec/plan.md`
- Change: `colin-api/requirements.txt` — Flask==2.3.3, Werkzeug==2.3.8, flask-restx==1.3.0, Jinja2==3.1.4, MarkupSafe==2.1.5, itsdangerous==2.1.2, click==8.1.7, blinker==1.6.3; Flask-Script removed
- Change: `colin-api/requirements/prod.txt` — drop Flask-Script
- Change: `colin-api/src/colin_api/config.py` — set `ENV` on config classes
- Change: `colin-api/src/colin_api/services/flags.py` — read `app.config['ENV']` (Flask 2.3 removed `app.env`)
- Change: `colin-api/src/colin_api/resources/db.py` — Oracle pool on `flask.g` instead of `_app_ctx_stack`
- Change: `colin-api/manage.py` — Click CLI replaces Flask-Script Manager
- Tests: `colin-api/tests/unit/security/test_dep_001_flask_upgrade.py`
- Smoke: `create_app('development')` + `/ops/healthz`, `/ops/readyz`, `/api/v1/meta/info`, `/api/v1/swagger.json` against upgraded stack (Oracle stubbed in agent env)
- Residual: not Flask 3.x; `flask-jwt-oidc==0.3.0` still uses removed request-context stack APIs on Flask 3; full Oracle-backed suite not executed here
