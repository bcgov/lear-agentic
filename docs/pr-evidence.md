# PR evidence

## CONFIG-006 — Oracle CPRD SSL hooks (issue #25)

- Spec: `spec/spec.md`, `spec/features/config-006-colin-oracle-ssl.feature` (`@R-25.1`, `@R-25.2`, `@R-25.3`)
- Plan: `spec/plan.md`
- Change: `colin-api/src/colin_api/resources/db.py` — `build_oracle_dsn`, TCPS SessionPool DSN, `TNS_ADMIN` from wallet, fail-closed when `ORACLE_REQUIRE_SSL` without `ORACLE_SSL`
- Change: `colin-api/src/colin_api/config.py` — `ORACLE_SSL`, `ORACLE_REQUIRE_SSL` (prod default true / test+dev default false), `ORACLE_WALLET_LOCATION`, `ORACLE_SSL_SERVER_DN`, `ORACLE_NET_ENCRYPTION`
- Sample: `colin-api/devops/vaults.ocp.env` comments for vault wiring
- Tests: `colin-api/pin_tests/test_config_006_oracle_ssl.py`
- Residual: wallet files + sqlnet.ora remain ops-owned; cleartext still possible if require-SSL is explicitly disabled
