# Plan — DEP-004 pin business-schemas

> Architecture and delivery approach for issue #9.

## Summary

Replace the unpinned `git+https://github.com/bcgov/business-schemas.git#egg=registry_schemas` line in `colin-api/requirements.txt` with the same URL pinned at `@<commit-sha>`, using the default-branch tip SHA observed via `git ls-remote … HEAD` at remediation time. Add a unit test that enforces the pin format.

## Architecture

```text
colin-api/requirements.txt
  → git+https://github.com/bcgov/business-schemas.git@<40-char-sha>#egg=registry_schemas
pip install -r requirements.txt
  → resolves that commit only (until pin is bumped)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Pin form | `@<full sha>` on existing git+ URL | Minimal change; pip-compatible; closes floating HEAD |
| SHA source | `git ls-remote … HEAD` at fix time | Matches “current default tip” without inventing a tag |
| Package index | Keep git egg install | Out of scope to republish as versioned artifact |

## Security & privacy

- Classification: supply-chain / reproducible build (CWE-1357)
- Residual: schemas still come from git over HTTPS; pin must be refreshed deliberately; historical floating installs already happened

## Test approach

- Unit: parse `colin-api/requirements.txt`; assert registry_schemas line has `@` + 40 hex chars before `#egg=`
- Acceptance: Gherkin `@R-704.1`, `@R-704.2` in `spec/features/dep-004-pin-business-schemas.feature`

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
