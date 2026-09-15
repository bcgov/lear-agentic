# Plan — DEP-011 / DEP-012 / DEP-016 emailer + bn deps

## Summary

Bump business-emailer `launchdarkly-server-sdk` to `>=9.10.0,<10.0.0` and modernize `flags.py` to the public `Files` / `Context` APIs used by business-pay. Raise protobuf in emailer and business-bn to `>=4.25.1,<6.0.0`. Update poetry.lock for both services.

## Key decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| LD target | `>=9.10.0,<10.0.0` | Platform floor from legal-api / bn / furnishings |
| Flag API | Context + Files.new_data_source | Private `_FileDataSource` removed/unreliable on 9.x |
| Protobuf | `>=4.25.1,<6.0.0` | Forces modern 4.x/5.x; clears old 3.20 ceilings that blocked grpc transitives |

## Test approach

- Unit assertions on pyproject constraints and flags imports
- `poetry lock` refresh for emailer and bn

## Approval (checkpoint 2)

| Role | Name | Date |
| --- | --- | --- |
| Architect / tech lead | local-agent | 2026-09-15 |
