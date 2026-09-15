# PR evidence

## DEP-009 / DEP-010 — COLIN API python-jose + oracledb (issues #28, #29)

- Spec: `spec/spec.md`, `spec/features/dep-009-010-colin-jose-oracledb.feature` (`@R-709.1`, `@R-710.1`, `@R-710.2`)
- Plan: `spec/plan.md`
- Change: `colin-api/requirements.txt` — `python-jose==3.4.0`, `oracledb==3.1.1` (removed `cx-Oracle==8.1.0`)
- Change: `colin-api/requirements/prod.txt` — `oracledb` replaces `cx_Oracle`
- Change: `colin-api/src/colin_api/resources/db.py` — `import oracledb as cx_Oracle`; drop `encoding`/`nencoding`
- Change: `colin-api/src/colin_api/resources/ops.py` — `import oracledb as cx_Oracle`
- Tests: `colin-api/tests/unit/security/test_dep_009_010_deps.py`
- Residual: python-jose may still carry CVE-2022-29217 residual (no complete upstream fix in 3.x); thick-mode Instant Client not enabled; live Oracle pool not exercised in this agent environment
