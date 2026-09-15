Feature: Queue service LaunchDarkly and protobuf dependency remediation
  Closes DEP-011 / #30, DEP-012 / #31, and DEP-016 / #35.

  @R-711.1
  Scenario: business-emailer LaunchDarkly SDK meets platform floor
    Given queue_services/business-emailer/pyproject.toml
    When launchdarkly-server-sdk is inspected
    Then the constraint requires at least 9.10 and flags use Context/Files APIs

  @R-712.1
  Scenario: business-emailer protobuf pin is relaxed
    Given the same emailer pyproject
    When protobuf is inspected
    Then it is no longer locked to ==3.20.* and requires at least 4.25.1 (below 6.x)

  @R-716.1
  Scenario: business-bn protobuf upper bound no longer blocks modern releases
    Given queue_services/business-bn/pyproject.toml
    When protobuf is inspected
    Then the old <3.20 ceiling is removed in favour of a modern compatible range
