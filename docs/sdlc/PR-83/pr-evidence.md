# PR evidence

## DEP-002 — COLIN API requests / urllib3 pins (issue #7)

- Spec: `spec/spec.md`, `spec/features/dep-002-colin-requests-urllib3.feature` (`@R-702.1`, `@R-702.2`)
- Plan: `spec/plan.md`
- Change: `colin-api/requirements.txt` — `requests==2.32.5`, `urllib3==2.8.0`
- Tests: `colin-api/tests/test_dep_002_requests_urllib3.py`
- Residual: `certifi==2020.12.5` unchanged (CA bundle freshness); full COLIN API image/smoke deferred to ops after merge; urllib3 2.x install checked with requests 2.32.5 (no fallback to 1.26.x needed)

## Review receipt (checkpoint 3 — agent draft)

**Checked:** `@R-702.1` / `@R-702.2` against `colin-api/requirements.txt` pins and unit assertions; Gherkin scenarios in `spec/features/dep-002-colin-requests-urllib3.feature`; local import/HTTP smoke of `requests==2.32.5` + `urllib3==2.8.0`.

**Could not check:** Full COLIN API container build / OpenShift deploy with cx_Oracle; production outbound HTTP behaviour under the new urllib3 2.x stack.

**Residual risk:** Older `certifi` pin may still limit CA freshness independently of this finding; confirm post-deploy that COLIN outbound HTTPS clients still succeed.
