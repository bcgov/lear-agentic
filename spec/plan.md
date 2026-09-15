# Plan — CONFIG-003 furnishings SFTP host-key verification

> Architecture and delivery approach for issue #2.

## Summary

Replace unconditional `AutoAddPolicy` in furnishings `SftpConnection` with fail-closed host-key verification: `RejectPolicy` plus an explicit known host key. Wire BCLaws / BCMail+ host-key config from environment. Unit tests fetch the ephemeral pytest-sftpserver host key via Transport and always use RejectPolicy.

## Architecture

```text
Furnishings job
  → SftpConnection(host, …, host_key=from config, verify_host=True)
      → SSHClient + RejectPolicy
      → host key added from vault/env
      → SFTPClient
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Default policy | Reject unknown hosts | Closes MITM; matches other LEAR SFTP jobs |
| Key material | Base64 host-key env per endpoint | Same pattern as `jobs/sftp-nuans-report` |
| Test harness | ephemeral host key fetched for fixture | pytest-sftpserver uses ephemeral keys |
| Opt-out logging | Warning when verification disabled | Makes residual risk visible in logs |

## Security & privacy

- Classification: unchanged (regulated notices in transit)
- Residual: until vault secrets `*_SFTP_HOST_KEY` are set, verified connects fail closed (preferred over AutoAdd)
- Secrets: host keys in vault / env — never commit

## Test approach

- Unit: policy selection; missing key raises when verify on; existing put/get tests with `verify_host=False`
- Acceptance: Gherkin `@R-03.1` / `@R-03.2` in `spec/features/config-003-sftp-host-key.feature`
- Provenance header on new unit test file

## Rollout

1. Merge code (human checkpoint 3)
2. Ops adds `BCLAWS_SFTP_HOST_KEY` / `BCMAIL_SFTP_HOST_KEY` to vault
3. Deploy furnishings job; confirm connects succeed

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
