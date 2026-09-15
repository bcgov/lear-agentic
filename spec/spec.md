# Spec — Hardened CRA BN Hub XML parse (VULN-006)

> Technology-free. Describe *what* and *why*, not frameworks or cloud products.

## Feature proposal

GitHub issue **#64** — `[VULN-006] xml.etree.ElementTree.fromstring() used without safe-parser for CRA BN Hub XML responses` (Low).

## Problem

Business BN processors parse CRA BN Hub XML with the stdlib ElementTree API. That API blocks classic network XXE but does not fully defend against entity-expansion denial-of-service; defence-in-depth requires a hardened parser.

## Outcome

All CRA BN Hub `fromstring` call sites in business-bn processors use a hardened ElementTree implementation that forbids entity expansion. Benign acknowledgement XML continues to parse.

## Scope

### In scope

- Switch processor `fromstring` imports to defusedxml ElementTree
- Add `defusedxml` dependency and lock update
- Unit assertions for import wiring, benign parse, and entity rejection (`@R-64.1+`)

### Out of scope

- VULN-004 / VULN-005 (lxml MRAS paths)
- Reworking BN Hub request/response business logic

## Sign-off (checkpoint 1)

| Role | Name | Date |
| --- | --- | --- |
| Product / PM | local-agent | 2026-09-15 |
| BA | local-agent | 2026-09-15 |
| QA | local-agent | 2026-09-15 |
