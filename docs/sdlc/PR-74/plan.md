# Plan — Redact user JWT DEBUG logs (LOG-002)

> Architecture and delivery approach. Technology belongs here (not in `spec.md`).

## Summary

Replace three DEBUG interpolations of the full JWT token dict (and user object) in `business_model.models.user` with presence-only messages; after successful create, log only the internal `user.id`. Add unit tests with `caplog` that assert forbidden claim values never appear in DEBUG records.

## Architecture

```text
JWT token dict → User.create_from_jwt_token / get_or_create_user_by_jwt
                 → DB user row (unchanged)
                 → DEBUG: presence / user.id only (no claim dump)
```

## Key decisions (ADRs may expand)

| Decision | Choice | Rationale |
| --- | --- | --- |
| Log content | Presence + optional internal user id | Meets `@R-09.1+`; avoids logging SQLAlchemy user repr (would re-emit PII columns) |
| Scope | business-registry-model `user.py` only | Matches LOG-002 location; other LOG-* stay on their issues |
| Tests | Extend `tests/models/test_user.py` with caplog | Existing JWT create/lookup fixtures already exercise the path |

## Security & privacy

- Classification: identity-pii / credential-adjacent claims must not enter log aggregators via these lines
- PIA status: no new personal-data processing; logging reduced
- Secrets: n/a

## Test approach

- Default integrity tier: CODEOWNERS on acceptance criteria
- Features: `spec/features/log-002-redact-user-jwt-debug-logs.feature` (`@R-09.1`–`@R-09.3`)
- Unit: assert DEBUG messages exclude `firstname`, `lastname`, `idp_userid`, `loginSource`, `sub`, `iss` values and the stringified token dict

## Rollout

- Environments: library consumed by legal-api and other services; deploy with next consumer release
- Migration / cutover: n/a

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | *(agent-proposed — awaiting human)* | 2026-09-15 |
| Security (if required) | *(agent-proposed — awaiting human)* | 2026-09-15 |
