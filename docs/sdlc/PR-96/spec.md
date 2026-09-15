# Spec — Safe Furnishings MRAS XML parser (VULN-005)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#63** — `[VULN-005] lxml.etree.fromstring() without safe parser in Furnishings MrasService` (Low).

## Problem

The Furnishings batch job copies Legal API's MRAS jurisdiction lookup and parses XML from an external API without an explicitly hardened XML parser (same class of risk as VULN-004 / #54, lower severity as a scheduled job).

## Outcome

Furnishings MRAS jurisdiction XML is parsed only through an explicit safe parser that disables entity resolution and network access during parse — the same control as VULN-004.

## Users & personas

| Persona | Goal |
| --- | --- |
| Furnishings job | Still resolve registered foreign jurisdictions for notices |
| Security reviewer | Explicit safe-parser control for VULN-005 is closed |
| Maintainer | Minimal parity change with legal-api MrasService |

## Scope

### In scope (this release)

- Remediate VULN-005 in furnishings `MrasService.get_jurisdictions`
- Explicit safe XML parser (`resolve_entities` off, `no_network` on)
- Unit coverage for happy path, parser configuration, and entity-payload fail-closed behaviour

### Out of scope

- VULN-004 (legal-api) — separate issue #54
- VULN-006 (CRA BN Hub) — separate issue #64

## Journeys

1. Safe Furnishings MRAS XML parse — see `features/vuln-005-furnishings-mras-safe-xmlparser.feature`

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA (acceptance ownership) | local-agent | 2026-09-15 |
