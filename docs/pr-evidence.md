# PR evidence

## DEP-007 — data-tool Flask / Werkzeug upgrade (issue #12)

- Spec: `spec/spec.md`, `spec/features/dep-007-data-tool-flask.feature` (`@R-707.1`, `@R-707.2`, `@R-707.3`)
- Plan: `spec/plan.md`
- Change: `data-tool/requirements.txt`
  - `flask-restx==1.3.2` (was 0.5.1; unlocks Flask 3)
  - `Flask==3.1.3`, `Werkzeug==3.1.8` (was 2.0.3)
  - Companions required for install/import: `Flask-SQLAlchemy==3.1.1`, `Flask-Babel==4.0.0`, `Babel==2.16.0`, `flask-jwt-oidc==0.9.0`, `blinker==1.9.0`, `Flask-Migrate==4.1.0`, `alembic==1.14.1`, `Flask-Caching==2.3.1`, `cachelib>=0.13.0`, `pyjwt==2.12.1`
- Tests: `data-tool/tests/test_dep_007_flask_werkzeug.py`
- Local smoke: core requirements resolve; Flask / flask-restx / Flask-SQLAlchemy / Flask-Babel / flask-jwt-oidc import under Flask 3.1.3

## Review receipt (checkpoint 3 — agent draft)

**Checked:** `@R-707.1` / `@R-707.2` / `@R-707.3` against `data-tool/requirements.txt` pins and unit assertions; Gherkin in `spec/features/dep-007-data-tool-flask.feature`; local venv install + import smoke of the upgraded stack.

**Could not check:** Full Prefect/Oracle data-tool image build and live Auth/corp migration run against Flask 3; interaction of `legal_api.models.db` from an installed LEAR package under the new Flask-SQLAlchemy 3.x API surface.

**Residual risk:** `Flask-Moment==0.11.0` still fails on Python 3.12 (`distutils` removed) if imported; `Flask-Script==2.0.6` remains abandoned/unused; other EOL pins (e.g. `urllib3==1.26.11`, `certifi==2020.12.5`, `requests==2.25.1`, `gunicorn==20.1.0`) are unchanged and out of DEP-007 scope.
