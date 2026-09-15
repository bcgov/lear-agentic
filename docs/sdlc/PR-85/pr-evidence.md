# PR evidence

## TEST-001 — SAST tooling (issue #20)

- Spec: `spec/spec.md`, `spec/features/test-001-002-sast-coverage.feature` (`@R-20.1`, `@R-20.2`, `@R-20.3`)
- Plan: `spec/plan.md`
- **Existing CodeQL (default setup):** repo `code-scanning/default-setup` is `configured` (languages: actions, javascript, javascript-typescript, python, typescript; weekly schedule). Analyses on recent PRs use tool `CodeQL` via `dynamic/github-code-scanning/codeql` (e.g. PR #72 head, 2026-09-15).
- Change: `.github/workflows/codeql-analysis.yml` — committed advanced-setup CodeQL for python / javascript-typescript / actions on PR + main + weekly cron
- Change: `.github/workflows/python-sast-bandit.yml` — Bandit High-only (`-lll`) for `legal-api` and `colin-api`
- Local check: Bandit High on both packages reported no High findings (exit 0)
- Tests: `tests/test_sast_coverage_controls.py` (workflow + fail-under + codecov targets)
- Residual: default setup + committed workflow may duplicate analyses; Bandit Medium findings (e.g. SQL construction) are not fail-gates here and remain on separate VULN issues

## TEST-002 — Coverage fail-under (issue #21)

- Spec criteria: `@R-21.1`, `@R-21.2`, `@R-21.3`
- Calibration (Codecov API, bcgov/lear flags): `legalapi` ≈ 78.15%, `colinapi` ≈ 30.62%
- Change: `legal-api/pyproject.toml` — `--cov-fail-under=70`
- Change: `colin-api/setup.cfg` — `--cov-fail-under=25`
- Change: `codecov.yaml` — project status targets 70% (`legalapi`) and 25% (`colinapi`)
- Residual: floors are intentionally below observed coverage; other packages still lack fail-under; colin-api CI job still gated to `github.repository == 'bcgov/lear'` so Codecov upload path on this fork may not run until that guard is addressed separately
