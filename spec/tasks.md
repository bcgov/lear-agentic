# Tasks — LOG-003–013 redact GCP auth logs

## Milestone 1

- [x] TASK-001 — Redact token/claim DEBUG + WARNING + remove finally:return in five `gcp_auth.py` modules — `@R-38.1`, `@R-38.2`, `@R-38.4`
- [x] TASK-002 — Redact email-reminder bearer DEBUG and emailer `ce.data` DEBUG — `@R-38.1`, `@R-38.3`
- [x] TASK-003 — Unit tests (caplog) + `docs/pr-evidence.md` + PR Fixes #38–#47 #57

## Backlog

- [ ] Remaining emailer processor DEBUG dumps of full email_msg (not in LOG-006 evidence path)
- [ ] LOG-014+ separate findings
