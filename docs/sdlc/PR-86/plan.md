# Plan — DEP-007 data-tool Flask / Werkzeug upgrade

> Architecture and delivery approach for issue #12.

## Summary

Upgrade `data-tool/requirements.txt` from Flask/Werkzeug 2.0.3 to Flask 3.1.x / Werkzeug 3.1.x by first raising `flask-restx` to ≥1.3 (Flask 3 support), then bumping only the companions that fail to import or resolve under Flask 3. Add pin-floor unit tests tagged `@R-707.*`.

## Architecture

```text
data-tool/requirements.txt
  flask-restx 0.5.1 → 1.3.2   (unlocks Flask ≥3)
  Flask 2.0.3 → 3.1.3
  Werkzeug 2.0.3 → 3.1.8
  companions: Flask-SQLAlchemy 3.1.1, Flask-Babel 4.0.0,
              flask-jwt-oidc 0.9.0, blinker 1.9, Flask-Migrate 4.1,
              alembic 1.14, Flask-Caching 2.3.1, Babel 2.16, pyjwt 2.12
tests/test_dep_007_flask_werkzeug.py
  parse == pins; assert major floors
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Order | flask-restx first, then Flask/Werkzeug | Finding’s stated blocker; 1.3+ documents Flask 3 support |
| Flask / Werkzeug versions | 3.1.3 / 3.1.8 | Current stable; verified install + import smoke |
| Companions | Bump only hard blockers | FSA 2 / Babel 2 / jwt-oidc 0.3 / blinker 1.4 fail on Flask 3 |
| Flask-Moment / Flask-Script | Leave pinned | Unused in flows; Moment already broken on Py3.12 `distutils` |

## Security & privacy

- Classification: outdated component (CWE-1104)
- Residual: unused Flask-Moment / Flask-Script; other EOL pins (urllib3 1.26, certifi 2020, requests 2.25, gunicorn 20.1) unchanged; full migration image smoke deferred

## Test approach

- Unit: parse `data-tool/requirements.txt`; assert Flask ≥3.1, Werkzeug ≥3.1, flask-restx ≥1.3
- Local smoke: venv install of core pins; import Flask, flask_restx, Flask-SQLAlchemy, Flask-Babel, flask-jwt-oidc
- Acceptance: Gherkin `@R-707.1`, `@R-707.2`, `@R-707.3`

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
