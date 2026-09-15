Feature: Data-tool Postgres URIs enforce TLS via sslmode
  Closes CONFIG-005 / issue #24 — stop connecting to LEAR / COLIN migr / AUTH Postgres without SSL mode.

  @R-24.1
  Scenario: Non-local environments require SSL on all three URIs
    Given FLASK_ENV is production (or another non-local setting)
    And DATABASE_SSLMODE is unset
    When data-tool config builds the LEAR, COLIN migr, and AUTH SQLAlchemy URIs
    Then each URI includes sslmode=require

  @R-24.2
  Scenario: Local development prefers TLS without hard-failing
    Given FLASK_ENV is development or DATA_LOAD_ENV signals local
    And DATABASE_SSLMODE is unset
    When data-tool config builds a Postgres URI
    Then the URI includes sslmode=prefer

  @R-24.3
  Scenario: Operators can override sslmode explicitly
    Given DATABASE_SSLMODE is set to verify-full (or disable for an approved local fixture)
    When data-tool config builds a Postgres URI
    Then the URI uses the explicit sslmode value
