# PR evidence

## DEP-017 (issue #36)
- Added `data-tool/requirements.lock` via pip-compile
- Exclusions (residual): `prefect[dask]` extras, `oracledb`, deprecated nats clients, `Flask-Script`, `reportlab`, `PyPDF2`, `numpy`, `pandas`, `lxml`, `psycopg2`, `html-sanitizer`, `minio` (direct pin remains in requirements.txt)

## DEP-019 (issue #56)
- Removed unused `Flask-Script` and direct `legacy-cgi` from `queue_services/business-emailer/pyproject.toml`
- Regenerated `poetry.lock`
- Residual: full Click CLI migration not required — Flask-Script was unused in source; no manage.py/Manager entrypoints remained
