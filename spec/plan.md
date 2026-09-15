# Plan — GD-002 / GD-003 COLIN API dependency pins

> Architecture and delivery approach for issues #14 and #15.

## Summary

Update the COLIN API frozen requirements so `ecdsa` and `gunicorn` are pinned at remediated versions. Add a small unit test that parses `colin-api/requirements.txt` and asserts the pins. Optionally constrain `requirements/prod.txt` so a future `make build-req` does not re-freeze vulnerable versions.

## Architecture

```text
colin-api/requirements.txt   (Docker / install freeze — source of truth for runtime)
colin-api/requirements/prod.txt  (loose prod inputs for rebuild)
  → ecdsa==0.19.1 (direct; wins over python-jose transitive)
  → gunicorn==23.0.0 (align with legal-api 23.x)
tests assert pin floors from the freeze file
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| ECDSA pin | `ecdsa==0.19.1` | Meets `>=0.19.0`; explicit 0.19.x pin |
| Gunicorn pin | `gunicorn==23.0.0` | Meets `>=22.0.0`; matches Legal API line |
| Direct ECDSA | Keep direct pin in freeze | python-jose may still suggest older ecdsa |
| Scope | colin-api only | Finding locations are colin-api requirements |
| Verification | Parse freeze + version compare | No full app smoke in this slice |

## Security & privacy

- Classification: unchanged
- Residual: python-jose remains; without a direct ecdsa pin a rebuild could regress — mitigated by direct pin (+ prod constraint)
- Residual: Gunicorn bump not smoke-tested in this PR — deferred to human/CI deploy check
- Secrets: none

## Test approach

- Unit: parse `colin-api/requirements.txt`; assert `ecdsa >= 0.19.0` and `gunicorn >= 22.0.0` (exact pins 0.19.1 / 23.0.0)
- Acceptance: Gherkin `@R-14.1`, `@R-15.1` in `spec/features/gd-002-003-ecdsa-gunicorn.feature`
- Provenance header on the new test file

## Rollout

1. Draft PR (Fixes #14, Fixes #15) — no self-merge
2. Human checkpoint 3 / Gate
3. Post-merge: smoke COLIN API boot under Gunicorn 23

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead / architect | *(agent-proposed — awaiting human)* | 2026-09-15 |
