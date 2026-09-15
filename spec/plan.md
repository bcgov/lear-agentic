# Plan — LOG-001 redact OIDC JWT INFO log

> Architecture and delivery approach for issue #16.

## Summary

Change the VALID account-affiliation INFO log in legal-api `business.py` so it records only account id and business identifier. Remove `preferred_username`, the full `g.jwt_oidc_token_info` object, and the affiliated-org response dump from that INFO line. Add unit tests with criterion provenance.

## Architecture

```text
GET /api/v2/businesses/<identifier>?account=<accountId>
  → get_businesses
      → AccountService.get_account_by_affiliated_identifier (unchanged)
      → INFO: "VALID account request, for accountId: …, business: …"
      → optionally set business_json["accountId"] when org matches (unchanged)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Correlation fields | `accountId` + business `identifier` | Enough for ops; no identity-PII |
| Drop org response from INFO | Yes | Affiliation payload can include account/org details; not needed for correlation |
| Scope | This INFO call site only | Matches LOG-001 evidence; keeps PR reviewable |
| Tests | Extend `test_business.py` | Same fixtures/JWT patterns as sibling GET business tests |

## Security & privacy

- Classification: reduces identity-PII in production INFO logs
- Closes CWE-532 for this path: no full OIDC token info at INFO
- Residual: unauthorized WARNING paths still log `preferred_username`; LOG-002+ DEBUG dumps remain separate issues

## Test approach

- Unit: INFO log omits PII markers; matching org still sets `accountId`; unmatched org does not
- Acceptance: Gherkin `@R-08.1` / `@R-08.2` / `@R-08.3` in `spec/features/log-001-redact-jwt-oidc-info-log.feature`
- Provenance: `# criterion: @R-08.x` on new tests

## Rollout

1. Merge after human checkpoint 3 (no agent self-merge)
2. Deploy legal-api as usual; no schema or config change

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
| Security (if required) | *(agent-proposed — awaiting human)* | 2026-09-15 |
