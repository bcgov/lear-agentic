# Plan — CONFIG-004 ETL SFTP verify-host default

> Architecture and delivery approach for issue #5.

## Summary

Align gazette / ICBC / NUANS `SFTPService` connection setup so host-key verification is the default. When verification is on, require `SFTP_HOST_KEY` and fail closed if missing. Keep `SFTP_VERIFY_HOST=false` as an explicit local opt-out that clears hostkeys and logs a warning. Minimal change in the existing pysftp/`CnOpts` style.

## Architecture

```text
ETL SFTP job (gazette | icbc | nuans)
  → SFTPService._connect()
      → CnOpts
      → default: require SFTP_HOST_KEY, add to cnopts.hostkeys
      → opt-out: SFTP_VERIFY_HOST=false → hostkeys=None + warning
      → pysftp.Connection(..., cnopts=cnopts)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Default | Verify on when unset | Closes MITM; matches CONFIG-003 intent |
| Missing key | Raise before connect | Fail closed, clear operator signal |
| Local opt-out | `SFTP_VERIFY_HOST=false` | Preserve existing local workflow |
| Scope | Same change in all three jobs | Finding covers all three paths |

## Security & privacy

- Classification: unchanged (registry data in transit)
- Residual: operators can still set `SFTP_VERIFY_HOST=false` in a deployed env; code cannot fully block misconfiguration without a separate prod env gate — mitigation is default-on + warning + documented ops check
- Secrets: `SFTP_HOST_KEY` remains in OpenShift/vault — never commit

## Test approach

- Unit: missing key raises when verify on; default treats unset as verify on; false clears hostkeys before connect (mocked)
- Acceptance: Gherkin `@R-05.1`–`@R-05.3` in `spec/features/config-004-sftp-verify-host-default.feature`
- Provenance headers on new unit test files

## Rollout

1. Merge code (human checkpoint 3)
2. Ops confirms `SFTP_VERIFY_HOST` is not `false` in prod and `SFTP_HOST_KEY` is set
3. Deploy three cronjobs; confirm connects succeed

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
