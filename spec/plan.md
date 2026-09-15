# Plan — TEST-001 / TEST-002 SAST and coverage floors

> Architecture and delivery approach for issues #20 and #21.

## Summary

Commit an explicit CodeQL workflow, add a Bandit job scoped to `legal-api` and `colin-api`, and set pytest `--cov-fail-under` plus Codecov flag targets using Codecov-observed coverage as the calibration source (legalapi ~78%, colinapi ~31%).

## Architecture

```text
PR / main
  ├─ GitHub default CodeQL setup (already configured; document only)
  ├─ .github/workflows/codeql-analysis.yml  (committed advanced setup)
  └─ .github/workflows/python-sast-bandit.yml
        └─ bandit -r src -lll  for legal-api, colin-api

legal-api/pyproject.toml   → pytest --cov-fail-under=70
colin-api/setup.cfg        → pytest --cov-fail-under=25
codecov.yaml               → project status targets 70% / 25% per flag
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| CodeQL file | `codeql-analysis.yml` | Preferred when missing; makes SAST reviewable in-repo |
| Extra SAST | Bandit High-only (`-lll`) | Lightweight; avoids always-red Medium SQL findings |
| Coverage floors | 70 / 25 | Below Codecov flags; non-zero; won't always fail |
| Existing workflows | Untouched | Do not disable Tier 1 or service CI |

## Security & privacy

- Classification: testing / assurance controls (TEST-001, TEST-002)
- Residual: default CodeQL + committed workflow may duplicate analyses; Bandit Medium findings remain; other packages lack fail-under

## Test approach

- Acceptance: Gherkin `@R-20.1`–`@R-20.3`, `@R-21.1`–`@R-21.3`
- Local: Bandit High on both packages (expect clean); config assertions via file presence / addopts strings
- CI: new workflows on PR; coverage gate activates when legal/colin test jobs run

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | *(agent-proposed — awaiting human)* | 2026-09-15 |
