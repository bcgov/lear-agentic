# Plan — TEST-003 data-tool / ETL non-zero coverage

## Summary

Add lightweight pytest smokes that assert on real modules without live infrastructure. Tag `@R-51.1+`.

## Architecture

```text
data-tool/tests/test_test003_smoke.py
jobs/sftp-{gazette,icbc-report,nuans-report}/tests/unit/test_test003_smoke.py
jobs/colin-extract-refresh/tests/test_test003_smoke.py (+ pytest.ini, requirements-dev.txt)
jobs/dbc-message-sender/tests/test_test003_smoke.py (+ pytest.ini, requirements-dev.txt)
```

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
