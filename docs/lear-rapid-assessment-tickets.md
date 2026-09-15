# LEAR rapid assessment backlog (ra-2026-07-13T170159Z)

Seeded into GitHub Issues on enrol. Source assessment: `ra-2026-07-13T170159Z`.

| ID | Severity | Title | Component |
| --- | --- | --- | --- |
| CONFIG-003 | Critical | SSH Host Key Validation Unconditionally Bypassed via AutoAddPolicy — GCP Furnishings SFTP | gcp-jobs |
| CONFIG-001 | High | Missing HTTP Security Response Headers — Legal API | legal-api |
| CONFIG-002 | High | Missing HTTP Security Response Headers — COLIN API | colin-api |
| CONFIG-004 | High | SFTP Host Key Verification Conditionally Disabled via Environment Variable — ETL SFTP Jobs | etl-jobs |
| DEP-001 | High |  | colin-api |
| DEP-002 | High |  | colin-api |
| DEP-003 | High |  | colin-api |
| DEP-004 | High |  | colin-api |
| DEP-005 | High |  | legal-api |
| DEP-006 | High |  | etl-jobs |
| DEP-007 | High |  | data-tool |
| DEP-008 | High |  | queue-services-common |
| GD-002 | High |  | colin-api |
| GD-003 | High |  | colin-api |
| LOG-001 | High | Full OIDC JWT token info object logged at INFO level | legal-api |
| LOG-002 | High | Full JWT token dictionary logged at DEBUG in user creation and lookup paths | business-registry-model |
| SECRET-001 | High | RSA JWT Private Test Key Committed in Source TestConfig Classes | legal-api |
| SECRET-002 | High | Dev OIDC Client Secret Committed in Postman Environment File | legal-api |
| TEST-001 | High | No SAST or security testing tooling integrated | legal-api |
| TEST-002 | High | No coverage enforcement threshold configured | legal-api |
| VULN-001 | High | SQL Injection via unparameterized f-string in get_last_event_id() | legal-api |
| VULN-002 | High | SQL Injection via stringify_list() with user-supplied identifiers and filing_types | colin-api |
| CONFIG-005 | Medium | PostgreSQL Connections Without SSL Enforcement — Data Tool | data-tool |
| CONFIG-006 | Medium | Oracle CPRD Database Connection Without SSL — COLIN API | colin-api |
| CONFIG-007 | Medium | CORS Wildcard Origin Configured — Legal API | legal-api |
| CONFIG-008 | Medium | CORS Wildcard Origin Configured — COLIN API | colin-api |
| DEP-009 | Medium |  | colin-api |
| DEP-010 | Medium |  | colin-api |
| DEP-011 | Medium |  | business-emailer |
| DEP-012 | Medium |  | business-emailer |
| DEP-013 | Medium |  | data-tool |
| DEP-014 | Medium |  | queue-services-common |
| DEP-015 | Medium |  | gcp-jobs |
| DEP-016 | Medium |  | business-bn |
| DEP-017 | Medium |  | data-tool |
| GD-001 | Medium |  | colin-api |
| LOG-003 | Medium | Payment-service bearer token logged at DEBUG in email-reminder job | gcp-jobs |
| LOG-004 | Medium | Bearer token and decoded JWT claim logged at DEBUG in GCP auth verification | business-bn |
| LOG-005 | Medium | Bearer token and decoded JWT claim logged at DEBUG in GCP auth verification | business-digital-credentials |
| LOG-006 | Medium | Bearer token, JWT claim, and email event data logged at DEBUG | business-emailer |
| LOG-007 | Medium | Bearer token and decoded JWT claim logged at DEBUG in GCP auth verification | business-filer |
| LOG-008 | Medium | Bearer token and decoded JWT claim logged at DEBUG in GCP auth verification | business-pay |
| LOG-009 | Medium | Authentication failure not logged and exception silenced via finally:return | business-bn |
| LOG-010 | Medium | Authentication failure not logged and exception silenced via finally:return | business-digital-credentials |
| LOG-011 | Medium | Authentication failure not logged and exception silenced via finally:return | business-emailer |
| LOG-012 | Medium | Authentication failure not logged and exception silenced via finally:return | business-pay |
| SECRET-003 | Medium | Flask SECRET_KEY Defaults to Weak Literal 'a secret' in Base Config | legal-api |
| SECRET-004 | Medium | Service Account Credential with Username=Password in Postman Collection | legal-api |
| SECRET-005 | Medium | Prefect, Hasura, and PostgreSQL Credentials Hardcoded in docker-compose | data-tool |
| TEST-003 | Medium | Data Tool and ETL Batch Jobs have zero test coverage | data-tool |
| TEST-004 | Medium | No CI/CD pipeline configuration detected in repository | legal-api |
| VULN-003 | Medium | Inadequate SQL sanitization in stringify_list() utility | colin-api |
| VULN-004 | Medium | lxml.etree.fromstring() called without explicit safe XMLParser in MrasService | legal-api |
| DEP-018 | Low |  | legal-api |
| DEP-019 | Low |  | business-emailer |
| LOG-013 | Low | Authentication failure not logged in GCP JWT verification | business-filer |
| LOG-014 | Low | Exception silently swallowed without logging in document service | legal-api |
| LOG-015 | Low | Authorization denials not consistently logged with actor and resource context | legal-api |
| SECRET-006 | Low | MinIO Test Credentials Hardcoded in TestConfig | legal-api |
| SECRET-007 | Low | CI Pipeline Hardcodes Default PostgreSQL Credentials for Test Containers | colin-api |
| SECRET-008 | Low | Test PostgreSQL Connection String with Default Credentials | business-registry-libs |
| VULN-005 | Low | lxml.etree.fromstring() without safe parser in Furnishings MrasService (copy of Legal API) | gcp-jobs |
| VULN-006 | Low | xml.etree.ElementTree.fromstring() used without safe-parser for CRA BN Hub XML responses | business-bn |
| SECRET-009 | Informational | Commented-Out SFTP Credential Persists in Source Code | etl-jobs |
| TEST-005 | Informational | Postman test collections not integrated into automated testing | legal-api |
