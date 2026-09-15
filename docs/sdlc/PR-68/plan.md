# Plan — VULN-001 parameterize get_last_event_id

> Architecture and delivery approach for issue #22.

## Summary

Change `get_last_event_id` in legal-api `colin_sync.py` so the business identifier is passed as a SQLAlchemy bound parameter to `text()`, not interpolated via an f-string. Add unit tests on the existing colin sync resource suite with criterion provenance.

## Architecture

```text
GET /api/v2/businesses/internal/last-event-id/<identifier>
  → get_last_event_id(identifier)
      → db.session.execute(text("… WHERE businesses.identifier = :identifier"), {"identifier": identifier})
      → scalar max(colin_event_id) or 404
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Binding style | Named `:identifier` + dict params | Matches SQLAlchemy `text()` best practice already used elsewhere in LEAR |
| Scope | This function only | Matches VULN-001 evidence; keeps PR reviewable |
| Tests | Extend `test_colin_sync.py` | Same fixture/JWT patterns as sibling endpoints |

## Security & privacy

- Classification: unchanged
- Closes CWE-89 for this endpoint: path `identifier` never concatenated into SQL
- Residual: other raw SQL sites in the same module remain out of scope (tracked separately if filed)

## Test approach

- Unit: happy path returns `maxId`; missing business → 404; identifier containing SQL metacharacters does not alter query / returns 404 for non-matching value
- Acceptance: Gherkin `@R-22.1` / `@R-22.2` / `@R-22.3` in `spec/features/vuln-001-parameterize-get-last-event-id.feature`
- Provenance: `# criterion: @R-22.x` on new/adjusted tests

## Rollout

1. Merge after human checkpoint 3 (no agent self-merge)
2. Deploy legal-api as usual; no schema or config change

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
| Security (if required) | *(agent-proposed — awaiting human)* | 2026-09-15 |
