# Plan — DEP-003
Generate `colin-api/requirements.lock` via pip-compile from requirements.txt excluding cx-Oracle, git schemas, and debugpy.
## Residual
cx-Oracle and registry_schemas still installed outside the lock; DEP-004 pins schemas.
## Approval
| Role | Name | Date |
| --- | --- | --- |
| Architect | local-agent | 2026-09-15 |
