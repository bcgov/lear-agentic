# PR evidence

## CONFIG-003 — SFTP host-key verification (issue #2)

- Spec: `spec/spec.md`, `spec/features/config-003-sftp-host-key.feature` (`@R-03.1`, `@R-03.2`, `@R-03.3`)
- Plan: `spec/plan.md`
- Change: `gcp-jobs/furnishings/src/furnishings/sftp.py` uses `RejectPolicy` + configured host key by default; `verify_host=False` only for pytest-sftpserver
- Callers wired: `stage_one.py` (BCMail), `post_processor.py` (BCLaws); config + vault placeholders for `*_SFTP_HOST_KEY`
- Tests: `tests/unit/test_sftp_host_key.py`
