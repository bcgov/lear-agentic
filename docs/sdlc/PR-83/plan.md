# Plan — DEP-002 COLIN API requests / urllib3

> Architecture and delivery approach for issue #7.

## Summary

Bump direct pins in `colin-api/requirements.txt` to secure floors, assert them with a unit test that parses the freeze, and file evidence + draft PR. No application code changes.

## Architecture

```text
colin-api/requirements.txt
  requests==2.32.5   (≥ 2.32.3; compatible with pinned certifi 2020.x)
  urllib3==2.8.0     (latest 2.x; requests declares urllib3<3,>=1.21.1)
pip install -r requirements.txt
  → HTTP client stack for outbound calls
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| `requests` pin | `2.32.5` | Meets ≥2.32.3; avoids `requests` 2.34.x requiring `certifi>=2023.5.7` while freeze still pins `certifi==2020.12.5` |
| `urllib3` pin | `2.8.0` | Latest 2.x; installs cleanly with `requests` 2.32.5; no cx_Oracle interaction |
| Fallback | (not used) | 1.26.20 only if 2.x broke install/import — residual would be documented |
| Criterion IDs | `@R-702.1` / `@R-702.2` | Avoid collision with CONFIG-002 `@R-07.x` |

## Security & privacy

- Closes known floors for CVE-2023-32681 (`requests` fixed ≥2.31.0) and CVE-2023-43804 (`urllib3` fixed ≥1.26.17; 2.x supersedes)
- Residual: `certifi` remains 2020.12.5 (CA bundle freshness — separate modernization)
- Secrets: none added

## Test approach

- Unit: parse `colin-api/requirements.txt`; assert version floors (`@R-702.1`, `@R-702.2`)
- Acceptance: Gherkin in `spec/features/dep-002-colin-requests-urllib3.feature`
- Smoke: optional local `pip install` of the two pins (no full colin-api image required for this PR)

## Rollout

1. Merge code (human checkpoint 3) — no self-merge
2. Rebuild/redeploy COLIN API image so the freeze is what runs in cluster

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
