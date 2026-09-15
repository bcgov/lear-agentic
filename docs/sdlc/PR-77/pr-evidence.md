# PR evidence

## CONFIG-004 — SFTP verify-host default (issue #5)

- Spec: `spec/spec.md`, `spec/features/config-004-sftp-verify-host-default.feature` (`@R-05.1`, `@R-05.2`, `@R-05.3`)
- Plan: `spec/plan.md`
- Change: `jobs/sftp-gazette|sftp-icbc-report|sftp-nuans-report/services/sftp.py` — default verify on; require `SFTP_HOST_KEY` when verify on; `SFTP_VERIFY_HOST=false` remains local opt-out with warning
- Tests: `jobs/sftp-gazette/tests/test_sftp_host_key.py`, `jobs/sftp-icbc-report/tests/unit/test_sftp_host_key.py`, `jobs/sftp-nuans-report/tests/unit/test_sftp_host_key.py`
- Residual: deployed envs can still set `SFTP_VERIFY_HOST=false`; ops must keep prod verify-on + host key populated
