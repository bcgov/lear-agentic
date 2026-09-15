# Plan — DEP-006 ETL SFTP HTTP dependency floors

> Architecture and delivery approach for issue #11.

## Summary

Bump or add direct HTTP-stack pins in the three SFTP ETL jobs’ requirement freezes, assert them with unit tests that parse those files, and file evidence + draft PR. No application code changes. Leave gazette Flask / Werkzeug majors as documented residual.

## Architecture

```text
jobs/sftp-{gazette,icbc-report,nuans-report}/requirements.txt
  (+ matching requirements/prod.txt)
    requests==2.32.4     (≥ 2.32.3)
    urllib3==2.8.0       (2.x patched line; requests allows urllib3<3)
    certifi==2026.7.22   (current CA bundle at remediation time)
pip install -r requirements.txt
  → outbound HTTP / TLS trust for notebook + connector paths
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| `requests` pin | `2.32.4` | Meets ≥2.32.3; matches existing ICBC/NUANS freeze |
| `urllib3` pin | `2.8.0` | Latest 2.x; compatible with `requests` 2.32.4 |
| `certifi` pin | `2026.7.22` | Current release at remediation time |
| Flask / Werkzeug (gazette) | unchanged (`Flask==1.1.2`, `Werkzeug==0.16.1`) | Full Flask 2/3 bump needs Jinja2 / Click / related cascade; siblings already on Flask 2.3.3 — major upgrade is residual follow-up |
| Criterion IDs | `@R-706.1`–`@R-706.3` | Per issue request `@R-706.1+` |

## Security & privacy

- Closes known floors for CVE-2023-32681 (`requests` fixed ≥2.31.0) and CVE-2023-43804 (`urllib3` fixed ≥1.26.17; 2.x supersedes); refreshes CA bundle via `certifi`
- Residual: gazette still on EOL Flask 1.1.2 / Werkzeug 0.16.1 until a deliberate framework upgrade
- Secrets: none added

## Test approach

- Unit: parse each job’s `requirements.txt`; assert version floors (`@R-706.1`–`@R-706.3`)
- Acceptance: Gherkin in `spec/features/dep-006-etl-sftp-http-deps.feature`
- Smoke: optional local install of the three pins (no full job image required for this PR)

## Rollout

1. Merge code (human checkpoint 3) — no self-merge
2. Rebuild/redeploy the three SFTP ETL images so the freeze is what runs in cluster

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
