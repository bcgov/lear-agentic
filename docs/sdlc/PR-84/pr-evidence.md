# PR evidence

## DEP-006 — ETL SFTP HTTP dependency floors (issue #11)

- Spec: `spec/spec.md`, `spec/features/dep-006-etl-sftp-http-deps.feature` (`@R-706.1`, `@R-706.2`, `@R-706.3`)
- Plan: `spec/plan.md`
- Change: `jobs/sftp-gazette|sftp-icbc-report|sftp-nuans-report/requirements.txt` and matching `requirements/prod.txt`
  - `requests==2.32.4` (≥ 2.32.3; gazette was 2.23.0; siblings already 2.32.4)
  - `urllib3==2.8.0` (gazette was 1.25.9; siblings gained direct pin)
  - `certifi==2026.7.22` (gazette was 2020.4.5.1; siblings gained direct pin)
- Not upgraded (residual): gazette `Flask==1.1.2` / `Werkzeug==0.16.1` — Flask 2/3 major needs Jinja2/Click cascade; siblings already on `Flask==2.3.3`
- Tests: `jobs/sftp-gazette/tests/test_dep_006_gazette_http_deps.py`, `jobs/sftp-icbc-report/tests/unit/test_dep_006_icbc_http_deps.py`, `jobs/sftp-nuans-report/tests/unit/test_dep_006_nuans_http_deps.py`
- Residual: gazette remains on EOL Flask/Werkzeug until a dedicated framework upgrade; full job image / OpenShift cronjob smoke not run in this PR
