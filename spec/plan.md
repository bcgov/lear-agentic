# Plan — VULN-002 parameterize reset IN lists

> Architecture and delivery approach for issue #23.

## Summary

Stop interpolating request-sourced `identifiers` and `filing_types` into SQL via `stringify_list`. Add `build_in_clause` / `build_cooper_reset_filings_query` helpers that emit named bind placeholders plus a bind map, and use them in `Reset.get_filings_for_reset`. Leave other internal `stringify_list` call sites for VULN-003.

## Architecture

```text
POST /reset/cooper  { identifiers, filing_types, … }
  → Reset.reset_filings(...)
      → get_filings_for_reset()
          → build_cooper_reset_filings_query(...)
              → build_in_clause(identifiers, 'ident')
              → build_in_clause(filing_types, 'ftype')
          → cursor.execute(sql_with_:binds, binds)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Fix site | `get_filings_for_reset` only | Matches VULN-002 evidence; user-controlled strings |
| Mechanism | Named bind IN-list helper | Matches existing cx_Oracle `:name` style |
| Legacy helper | Keep `stringify_list` + warn in docstring | Avoids wide blast radius; VULN-003 owns full cleanup |
| Tests | Pure helpers via source load | No Oracle required in unit CI |

## Security & privacy

- Classification: unchanged
- Residual: other `stringify_list` / f-string IN sites remain (VULN-003)
- Secrets: none

## Test approach

- Unit: `build_in_clause` never embeds raw values in SQL fragment; injection-like strings only in binds
- Unit: `build_cooper_reset_filings_query` binds identifiers and filing_types
- Acceptance: Gherkin `@R-04.1` / `@R-04.2` / `@R-04.3`
- Provenance header on new unit test file

## Rollout

1. Merge code (human checkpoint 3)
2. No config / vault changes
3. Deploy colin-api; smoke authenticated reset with normal filters

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
