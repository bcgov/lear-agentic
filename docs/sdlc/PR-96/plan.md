# Plan — VULN-005 Furnishings safe MRAS XMLParser

## Summary

Apply the same `XMLParser(resolve_entities=False, no_network=True)` hardening used for VULN-004 to `gcp-jobs/furnishings` `MrasService`, with unit tests tagged `@R-63.*`.

## Architecture

```text
furnishings/services/mras_service.py
  etree.fromstring(content, parser=safe_parser)
tests/unit/test_mras_service.py
  happy path + source inspection + XXE canary
```

Use a top-level `tests/test_mras_service.py` smoke file to avoid the heavy `tests/unit/__init__.py` business-model imports when exercising parser-only behaviour.

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Parser flags | Same as VULN-004 | Issue asks for parity with legal-api fix |
| Test harness | Minimal Flask app fixture | Avoid heavy create_app/DB for service-only tests |

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
