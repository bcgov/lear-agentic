Feature: Bind remaining string-typed stringify_list IN lists
  Closes VULN-003 / issue #53 — stop interpolating string-typed lists into SQL.

  @R-53.1
  Scenario: IN-list helper emits bind placeholders for string values
    Given a list of string filter values that may contain quote or SQL metacharacters
    When an IN-clause fragment is built for those values
    Then the SQL fragment contains only named bind placeholders
    And each original value appears only in the bind map

  @R-53.2
  Scenario: Cooper reset and corp-num deletes bind string corporation identifiers
    Given reset or delete paths receive corporation numbers or filing type codes as strings
    When those values are applied in an IN list
    Then the values use bind variables
    And no string is concatenated as a SQL literal into the query text via stringify_list

  @R-53.3
  Scenario: Business and filing-type string filters bind rather than stringify
    Given business identifier / corp-type lists or matching filing type codes
    When those filters are applied in SQL
    Then the filters use bind variables
    And stringify_list is not used for those string-typed arguments
