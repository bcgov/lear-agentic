# Plan — VULN-006 business-bn defusedxml

## Summary

Replace `xml.etree.ElementTree as Et` with `defusedxml.ElementTree as Et` in BN processors; add dependency + unit tests `@R-64.*`.

## Architecture

```text
bn_processors/{registration,admin,change_of_registration,dissolution_or_put_back_on}.py
  import defusedxml.ElementTree as Et
  Et.fromstring(...)
pyproject.toml + poetry.lock → defusedxml
tests/unit/test_vuln006_defusedxml.py
```

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
