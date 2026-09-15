Feature: Ephemeral test database credentials
  Closes SECRET-007 / #61 and SECRET-008 / #62.

  @R-61.1
  Scenario: Colin API CI does not hardcode postgres password literal
    Given the colin-api CI workflow
    When the test job configures Postgres
    Then the password is derived per run rather than the literal string postgres

  @R-62.1
  Scenario: sql-versioning tests read DB URL from the environment
    Given the sql-versioning test conftest
    When the suite starts
    Then the connection string comes from SQL_VERSIONING_TEST_DATABASE_URL or a test-only default
