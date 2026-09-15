Feature: Cooper reset filters bind request-sourced IN lists
  Closes VULN-002 / issue #23 — stop interpolating identifiers and filing_types into SQL.

  @R-04.1
  Scenario: IN-list helper emits bind placeholders only
    Given a list of filter values that may contain quote or SQL metacharacters
    When an IN-clause fragment is built for those values
    Then the SQL fragment contains only named bind placeholders
    And each original value appears only in the bind map

  @R-04.2
  Scenario: Reset lookup binds identifiers from the request
    Given a cooper reset request includes one or more identifiers
    When filings for reset are selected
    Then the identifiers filter uses bind variables
    And no identifier string is concatenated as a SQL literal into the query text

  @R-04.3
  Scenario: Reset lookup binds filing_types from the request
    Given a cooper reset request includes one or more filing_types
    When filings for reset are selected
    Then the filing_types filter uses bind variables
    And no filing_type string is concatenated as a SQL literal into the query text
