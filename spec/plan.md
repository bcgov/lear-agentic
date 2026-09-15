# Plan — VULN-003 bind remaining string-typed stringify_list paths

> Architecture and delivery approach for issue #53.

## Summary

Extend VULN-002’s `build_in_clause` pattern to remaining string-typed IN-list sites in colin-api (`reset` corp nums and cooper filters, `business` identifiers / corp types, `filing_type` matching codes). Leave trusted integer `event_ids` / `address_ids` / `delete_from_table_by_event_ids` on `stringify_list` with an explicit residual note.

## Architecture

```text
build_in_clause(values, prefix) → ':p_0,:p_1', {p_0:…, p_1:…}
  ← reset._delete_new_corps / _delete_corp_state (corp_nums)
  ← reset.get_filings_for_reset via build_cooper_reset_filings_query
  ← business._get_bn_15s (identifiers)
  ← business.find_by_identifier (corp_types)
  ← filing_type.get_most_recent_match_before_event (matching_filing_types)

stringify_list(event_ids) residual → address / office / corp_party / reset deletes / delete_from_table_by_event_ids
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Mechanism | Named bind IN-list helper | Same as VULN-002 / cx_Oracle `:name` |
| String sites | Convert all | Matches finding + user guidance |
| Int event/addr IDs | Residual | Trusted DB-sourced ints; document in evidence |
| Tests | Pure helpers + source guards | No Oracle required in unit CI |

## Security & privacy

- Classification: unchanged
- Residual: integer ID `stringify_list` call sites (address, office, corp_party, reset event deletes, `delete_from_table_by_event_ids`)
- Secrets: none

## Test approach

- Unit: `build_in_clause` never embeds raw string values in SQL fragment
- Unit: cooper reset query builder binds identifiers / filing_types
- Unit: source guard that string-typed call sites no longer pass args to `stringify_list`
- Acceptance: Gherkin `@R-53.1` / `@R-53.2` / `@R-53.3`

## Rollout

1. Draft PR Fixes #53 (human checkpoint 3 — no self-merge)
2. No config / vault changes
3. Deploy colin-api after merge

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
