# Plan — GD-001 COLIN API Jinja2 bump

> Architecture and delivery approach for issue #37.

## Summary

Raise the direct `Jinja2` pin to 3.1.4 (>= 3.1.3 advisory floor) and `MarkupSafe` to 2.1.5 so the freeze installs cleanly beside Flask 1.1.2. Leave Flask/Werkzeug/flask-restx to DEP-001.

## Architecture

```text
colin-api/requirements.txt
  Jinja2==3.1.4
  MarkupSafe==2.1.5
  Flask==1.1.2 (unchanged here; DEP-001 → 2.3.3)
```

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Target | Jinja2 3.1.4 | Matches DEP-001 companion pin; clears >=3.1.3 |
| MarkupSafe | 2.1.5 | Required companion for Jinja2 3.1.x |
| Flask | leave 1.1.2 | Avoid duplicating DEP-001 scope |

## Security & privacy

- Residual: templates are not exhaustively re-audited for `xmlattr`; floor bump addresses the cited CVE path
- DEP-001 will re-pin Jinja2 alongside Flask 2.3 — keep pins aligned

## Test approach

- Static pin test `@R-37.1`
- Optional local `pip install` smoke if environment allows

## Rollout

1. Merge (human checkpoint 3)
2. Image rebuild picks up freeze
3. DEP-001 may supersede pins when merged

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Tech lead | | |
| Security | | |
