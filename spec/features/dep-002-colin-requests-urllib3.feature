Feature: COLIN API pins secure requests and urllib3
  Closes DEP-002 / issue #7 — raise outdated HTTP client dependency floors.

  @R-702.1
  Scenario: requests pin meets the remediated floor
    Given colin-api/requirements.txt declares a direct requests pin
    When the pinned version is inspected
    Then it is greater than or equal to 2.32.3

  @R-702.2
  Scenario: urllib3 pin meets the remediated 2.x floor
    Given colin-api/requirements.txt declares a direct urllib3 pin
    When the pinned version is inspected
    Then it is a 2.x release greater than or equal to 2.2.0
