# PR evidence

## VULN-005 — Furnishings safe MRAS XMLParser (issue #63)

- Spec: `spec/spec.md`, `spec/features/vuln-005-furnishings-mras-safe-xmlparser.feature` (`@R-63.1`, `@R-63.2`, `@R-63.3`)
- Plan: `spec/plan.md`
- Change: `gcp-jobs/furnishings/src/furnishings/services/mras_service.py` — `etree.fromstring` uses `XMLParser(resolve_entities=False, no_network=True)` (parity with VULN-004)
- Tests: `gcp-jobs/furnishings/tests/test_mras_service.py`

## Review receipt (checkpoint 3 — agent draft)

**Checked:** `@R-63.1`–`@R-63.3` against furnishings MrasService and unit tests; Gherkin present.

**Could not check:** Live MRAS endpoint responses in a furnishings OpenShift job run.

**Residual risk:** Furnishings still trusts the MRAS HTTP response body; safe parser closes XXE/entity expansion for this parse site only. Legal-api copy is tracked separately as VULN-004/#54.
