# Plan — CONFIG-006 COLIN API Oracle CPRD TLS

> Architecture and delivery approach for issue #25.

## Summary

Add application-layer TLS hooks around `cx_Oracle.SessionPool`: build a TCPS DESCRIPTION DSN when `ORACLE_SSL` is true, export `TNS_ADMIN` from `ORACLE_WALLET_LOCATION`, and refuse pool creation when `ORACLE_REQUIRE_SSL` is true without SSL. Document that wallet files and sqlnet.ora remain ops-owned.

## Architecture

```text
Flask config (ORACLE_SSL / REQUIRE / WALLET / DN / NET_ENCRYPTION)
  → OracleDB._create_pool()
      → fail closed if REQUIRE && !SSL
      → TNS_ADMIN = wallet (optional)
      → build_oracle_dsn(...)  # Easy Connect or TCPS DESCRIPTION
      → cx_Oracle.SessionPool(..., dsn=...)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Protocol | TCPS DESCRIPTION | Works with Instant Client / cx_Oracle 8 without new driver |
| Fail closed | `ORACLE_REQUIRE_SSL` (prod default true) | Concrete control even when wallet not in-repo |
| Wallet | Env path → `TNS_ADMIN` | Standard Instant Client hook; files stay ops-owned |
| Test/Dev | require default false | Avoid breaking local Instant Client without wallets |

## Security & privacy

- Residual: enabling TCPS without a valid wallet/listener config will fail at connect time; cleartext remains possible if require-SSL is disabled
- Native network encryption (`SQLNET.ENCRYPTION_CLIENT`) still needs sqlnet.ora — `ORACLE_NET_ENCRYPTION` is the documented intent hook

## Test approach

- Unit: DSN builder, fail-closed RuntimeError, TNS_ADMIN + TCPS DSN with mocked SessionPool
- Acceptance: `@R-25.1`–`@R-25.3`

## Rollout

1. Merge code (human checkpoint 3)
2. Ops mounts wallet, sets `ORACLE_SSL=true`, confirms TCPS port
3. Leave `ORACLE_REQUIRE_SSL=true` in prod; break-glass only via explicit false

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead | | |
| Security | | |
