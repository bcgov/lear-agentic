Feature: Last COLIN event id lookup uses bound SQL parameters
  Closes VULN-001 / issue #22 — stop interpolating path identifier into SQL.

  @R-22.1
  Scenario: Known business returns max COLIN event id
    Given a business with at least one COLIN event id exists
    And I am authenticated with the COLIN service role
    When I request the last event id for that business identifier
    Then the response is successful
    And the body contains the maximum COLIN event id for that business

  @R-22.2
  Scenario: Unknown business returns not found
    Given no COLIN event ids exist for the requested identifier
    And I am authenticated with the COLIN service role
    When I request the last event id for that identifier
    Then the response indicates not found

  @R-22.3
  Scenario: Identifier with SQL metacharacters does not alter the query
    Given I am authenticated with the COLIN service role
    When I request the last event id with an identifier containing SQL quote and clause fragments
    Then the identifier is treated as a single bound value
    And the response is not found (or matches only an identically stored identifier)
    And no additional SQL structure from the input is executed
