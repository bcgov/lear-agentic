# Plan — DEP-009 / DEP-010 COLIN API jose + oracledb

> Architecture and delivery approach for issues #28 and #29.

## Summary

Raise `python-jose` to 3.4.0. Replace `cx-Oracle` / `cx_Oracle` with `oracledb==3.1.1` (aligned with data-tool / colin-extract-refresh). Use thin mode with `import oracledb as cx_Oracle` in `db.py` and `ops.py`, and remove `encoding` / `nencoding` SessionPool kwargs removed by the new driver.

## Architecture

```text
colin-api/requirements.txt     → python-jose==3.4.0, oracledb==3.1.1
colin-api/requirements/prod.txt → oracledb (was cx_Oracle)
src/colin_api/resources/db.py  → import oracledb as cx_Oracle; drop encoding kwargs
src/colin_api/resources/ops.py → import oracledb as cx_Oracle
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| jose target | `==3.4.0` | Matches issue floor (≥3.4.0) and emailer pin |
| Oracle driver | `oracledb==3.1.1` thin | Sibling components already on this package/version |
| Compatibility | import alias | Minimal churn for SessionPool / DatabaseError |
| Thick mode | out of scope | Instant Client not required for thin SessionPool |

## Security & privacy

- Classification: outdated dependency / CWE-1104
- Residual: python-jose CVE-2022-29217 may lack a complete upstream fix; consider joserfc later. Oracle connectivity not fully exercised in this agent environment.

## Test approach

- Unit: requirement pin floors + alias import assertions (`@R-709.1`, `@R-710.1`, `@R-710.2`)
- Acceptance: Gherkin feature for DEP-009 / DEP-010

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
